"""
Serviços para o aplicativo alunos.
Contém a lógica de negócios complexa.
"""
from django.utils import timezone
from django.db.models import Q
import logging
import requests
from django.core.files.base import ContentFile
from .utils import (
    get_aluno_model, 
    get_turma_model, 
    get_matricula_model,
    get_atribuicao_cargo_model,
    get_registro_historico_model
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

def listar_alunos(query=None, curso_id=None):
    """
    Lista e filtra alunos com base na query e no curso.
    """
    Aluno = get_aluno_model()
    queryset = Aluno.objects.filter(ativo=True).order_by("nome")

    if query:
        cpf_query = ''.join(filter(str.isdigit, query))
        search_query = (
            Q(nome__icontains=query) |
            Q(email__icontains=query) |
            Q(numero_iniciatico__icontains=query) |
            Q(nome_iniciatico__icontains=query)
        )
        if cpf_query:
            search_query |= Q(cpf__icontains=cpf_query)
            search_query |= Q(matricula__icontains=cpf_query)
        queryset = queryset.filter(search_query).distinct()

    if curso_id:
        queryset = queryset.filter(matricula__turma__curso_id=curso_id).distinct()
    return queryset

def buscar_aluno_por_cpf(cpf):
    """
    Busca um aluno pelo CPF.

    Args:
        cpf (str): O CPF do aluno a ser buscado.

    Returns:
        Aluno: A instância do aluno, ou None se não for encontrado.
    """
    Aluno = get_aluno_model()
    try:
        return Aluno.objects.get(cpf=cpf)
    except Aluno.DoesNotExist:
        return None

def buscar_alunos_por_nome_ou_cpf(query):
    """
    Busca alunos por nome ou CPF.

    Args:
        query (str): O termo de busca.

    Returns:
        QuerySet: Um queryset de alunos que correspondem à busca.
    """
    Aluno = get_aluno_model()
    cpf_query = ''.join(filter(str.isdigit, query))
    return Aluno.objects.filter(
        Q(nome__icontains=query) | Q(cpf__icontains=cpf_query)
    )

def buscar_aluno_por_email(email):
    """
    Busca um aluno pelo email.

    Args:
        email (str): O email do aluno a ser buscado.

    Returns:
        Aluno: A instância do aluno, ou None se não for encontrado.
    """
    Aluno = get_aluno_model()
    try:
        return Aluno.objects.get(email=email)
    except Aluno.DoesNotExist:
        return None

def criar_aluno(aluno_data, foto_url=None):
    """
    Cria um novo aluno com os dados fornecidos e, opcionalmente, uma foto.

    Args:
        aluno_data (dict): Dicionário com os dados do aluno (nome, email, cpf, etc.).
        foto_url (str, optional): URL da foto a ser baixada.

    Returns:
        Aluno: A instância do aluno criado, ou None em caso de erro.
    """
    Aluno = get_aluno_model()
    try:
        aluno = Aluno.objects.create(**aluno_data)

        if foto_url:
            try:
                response = requests.get(foto_url, stream=True, timeout=10)
                response.raise_for_status()
                file_name = f'{aluno_data["cpf"]}_photo.jpg'
                aluno.foto.save(file_name, ContentFile(response.content), save=True)
            except requests.exceptions.RequestException as e:
                logger.error(f"Erro ao baixar a foto para o aluno {aluno_data['nome']}: {e}")
                # Continua mesmo se a foto falhar, o aluno já foi criado

        return aluno
    except Exception as e:
        logger.error(f"Erro ao criar o aluno {aluno_data.get('nome')}: {e}")
        return None

def listar_historico_aluno(aluno):
    """
    Retorna o histórico de registros (cargos, iniciações, punições) de um aluno.
    """
    RegistroHistorico = get_registro_historico_model()
    return RegistroHistorico.objects.filter(aluno=aluno).order_by('-data_registro')

def criar_registro_historico(aluno, data):
    """
    Cria um novo registro histórico para um aluno.
    """
    RegistroHistorico = get_registro_historico_model()
    data['aluno'] = aluno
    registro = RegistroHistorico.objects.create(**data)
    return registro