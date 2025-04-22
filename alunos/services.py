"""
Serviços para o aplicativo alunos.
Contém a lógica de negócios complexa.
"""
from django.utils import timezone
from django.db.models import Q
import logging
from .utils import (
    get_aluno_model, 
    get_turma_model, 
    get_matricula_model,
    get_atribuicao_cargo_model
)

logger = logging.getLogger(__name__)

def verificar_elegibilidade_instrutor(aluno):
    """
    Verifica se um aluno pode ser instrutor.
    
    Args:
        aluno: Instância do modelo Aluno
        
    Returns:
        dict: Dicionário com chaves 'elegivel' (bool) e 'motivo' (str)
    """
    # Verificar se o aluno está ativo
    if aluno.situacao != "ATIVO":
        return {
            "elegivel": False,
            "motivo": f"O aluno não está ativo. Situação atual: {aluno.get_situacao_display()}"
        }
    
    # Verificar se o método pode_ser_instrutor existe
    if not hasattr(aluno, 'pode_ser_instrutor'):
        return {
            "elegivel": False,
            "motivo": "Erro na verificação: o método 'pode_ser_instrutor' não existe."
        }
    
    # Verificar se o aluno pode ser instrutor
    try:
        pode_ser_instrutor = aluno.pode_ser_instrutor
        
        if not pode_ser_instrutor:
            # Verificar matrículas em cursos pré-iniciáticos
            Matricula = get_matricula_model()
            if Matricula:
                matriculas_pre_iniciatico = Matricula.objects.filter(
                    aluno=aluno, turma__curso__nome__icontains="Pré-iniciático"
                )
                
                if matriculas_pre_iniciatico.exists():
                    cursos = ", ".join([f"{m.turma.curso.nome}" for m in matriculas_pre_iniciatico])
                    return {
                        "elegivel": False,
                        "motivo": f"O aluno está matriculado em cursos pré-iniciáticos: {cursos}"
                    }
            
            return {
                "elegivel": False,
                "motivo": "O aluno não atende aos requisitos para ser instrutor."
            }
        
        return {"elegivel": True}
    
    except Exception as e:
        logger.error(f"Erro ao verificar elegibilidade do instrutor: {str(e)}")
        return {
            "elegivel": False,
            "motivo": f"Erro ao verificar requisitos de instrutor: {str(e)}"
        }

def remover_instrutor_de_turmas(aluno, nova_situacao):
    """
    Remove um aluno de todas as turmas onde ele é instrutor.
    
    Args:
        aluno: Instância do modelo Aluno
        nova_situacao: Nova situação do aluno
        
    Returns:
        dict: Resultado da operação com chaves 'sucesso' e 'mensagem'
    """
    try:
        Turma = get_turma_model()
        AtribuicaoCargo = get_atribuicao_cargo_model()
        
        # Buscar turmas onde o aluno é instrutor
        turmas_instrutor = Turma.objects.filter(instrutor=aluno, status="A")
        turmas_instrutor_auxiliar = Turma.objects.filter(instrutor_auxiliar=aluno, status="A")
        turmas_auxiliar_instrucao = Turma.objects.filter(auxiliar_instrucao=aluno, status="A")
        
        # Atualizar as turmas
        for turma in turmas_instrutor:
            turma.instrutor = None
            turma.alerta_instrutor = True
            turma.alerta_mensagem = f"O instrutor {aluno.nome} foi removido devido à mudança de situação para '{aluno.get_situacao_display()}'."
            turma.save()
            
            # Finalizar os cargos administrativos relacionados
            if AtribuicaoCargo:
                atribuicoes = AtribuicaoCargo.objects.filter(
                    aluno=aluno,
                    cargo__nome__icontains="Instrutor Principal",
                    data_fim__isnull=True,
                )
                for atribuicao in atribuicoes:
                    atribuicao.data_fim = timezone.now().date()
                    atribuicao.save()
        
        for turma in turmas_instrutor_auxiliar:
            turma.instrutor_auxiliar = None
            turma.alerta_instrutor = True
            turma.alerta_mensagem = f"O instrutor auxiliar {aluno.nome} foi removido devido à mudança de situação para '{aluno.get_situacao_display()}'."
            turma.save()
            
            # Finalizar os cargos administrativos relacionados
            if AtribuicaoCargo:
                atribuicoes = AtribuicaoCargo.objects.filter(
                    aluno=aluno,
                    cargo__nome__icontains="Instrutor Auxiliar",
                    data_fim__isnull=True,
                )
                for atribuicao in atribuicoes:
                    atribuicao.data_fim = timezone.now().date()
                    atribuicao.save()
        
        for turma in turmas_auxiliar_instrucao:
            turma.auxiliar_instrucao = None
            turma.alerta_instrutor = True
            turma.alerta_mensagem = f"O auxiliar de instrução {aluno.nome} foi removido devido à mudança de situação para '{aluno.get_situacao_display()}'."
            turma.save()
            
            # Finalizar os cargos administrativos relacionados
            if AtribuicaoCargo:
                atribuicoes = AtribuicaoCargo.objects.filter(
                    aluno=aluno,
                    cargo__nome__icontains="Auxiliar de Instrução",
                    data_fim__isnull=True,
                )
                for atribuicao in atribuicoes:
                    atribuicao.data_fim = timezone.now().date()
                    atribuicao.save()
        
        total_turmas = len(turmas_instrutor) + len(turmas_instrutor_auxiliar) + len(turmas_auxiliar_instrucao)
        
        return {
            "sucesso": True,
            "mensagem": f"Aluno removido de {total_turmas} turmas com sucesso."
        }
    
    except Exception as e:
        logger.error(f"Erro ao remover instrutor de turmas: {str(e)}")
        return {
            "sucesso": False,
            "mensagem": f"Erro ao remover instrutor de turmas: {str(e)}"
        }