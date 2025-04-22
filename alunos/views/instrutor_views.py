"""
Views relacionadas a instrutores.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import logging

from ..utils import get_aluno_model, get_turma_model, get_atribuicao_cargo_model
from ..services import remover_instrutor_de_turmas

logger = logging.getLogger(__name__)

@login_required
def confirmar_remocao_instrutoria(request, cpf, nova_situacao):
    """Confirma a remoção da instrutoria de um aluno."""
    Aluno = get_aluno_model()
    aluno = get_object_or_404(Aluno, cpf=cpf)
    
    # Importar os modelos necessários
    try:
        Turma = get_turma_model()
        AtribuicaoCargo = get_atribuicao_cargo_model()
        
        # Buscar turmas onde o aluno é instrutor
        turmas_instrutor = Turma.objects.filter(instrutor=aluno, status="A")
        turmas_instrutor_auxiliar = Turma.objects.filter(
            instrutor_auxiliar=aluno, status="A"
        )
        turmas_auxiliar_instrucao = Turma.objects.filter(
            auxiliar_instrucao=aluno, status="A"
        )
        
        # Juntar todas as turmas
        turmas = (
            list(turmas_instrutor)
            + list(turmas_instrutor_auxiliar)
            + list(turmas_auxiliar_instrucao)
        )
        
        # Se não houver turmas, redirecionar para a edição
        if not turmas:
            return redirect("alunos:editar_aluno", cpf=aluno.cpf)
        # Se o método for POST, processar a confirmação
        if request.method == "POST":
            # Atualizar a situação do aluno
            aluno.situacao = nova_situacao
            aluno.save()
            
            # Remover o aluno das turmas como instrutor
            resultado = remover_instrutor_de_turmas(aluno, nova_situacao)
            if resultado["sucesso"]:
                messages.success(
                    request,
                    "Aluno atualizado com sucesso e removido das turmas como instrutor!"
                )
            else:
                messages.error(request, resultado["mensagem"])
            
            return redirect("alunos:detalhar_aluno", cpf=aluno.cpf)
        
        # Renderizar a página de confirmação
        return render(
            request,
            "alunos/confirmar_remocao_instrutoria.html",
            {
                "aluno": aluno,
                "nova_situacao": dict(Aluno.SITUACAO_CHOICES).get(
                    nova_situacao
                ),
                "turmas_instrutor": turmas_instrutor,
                "turmas_instrutor_auxiliar": turmas_instrutor_auxiliar,
                "turmas_auxiliar_instrucao": turmas_auxiliar_instrucao,
                "total_turmas": len(turmas),
            },
        )
    except Exception as e:
        messages.error(request, f"Erro ao processar a solicitação: {str(e)}")
        logger.error(f"Erro ao confirmar remoção de instrutoria: {str(e)}")
        return redirect("alunos:editar_aluno", cpf=aluno.cpf)

@login_required
def diagnostico_instrutores(request):
    """
    Página de diagnóstico para depurar problemas com a seleção de instrutores.
    Mostra informações detalhadas sobre alunos e sua elegibilidade para serem instrutores.
    """
    try:
        Aluno = get_aluno_model()
        # Buscar todos os alunos ativos
        alunos_ativos = Aluno.objects.filter(situacao="ATIVO")
        
        # Coletar informações de diagnóstico para cada aluno
        diagnostico = []
        for aluno in alunos_ativos:
            info = {
                "cpf": aluno.cpf,
                "nome": aluno.nome,
                "numero_iniciatico": aluno.numero_iniciatico or "N/A",
                "situacao": aluno.get_situacao_display(),
                "tem_metodo": hasattr(aluno, 'pode_ser_instrutor'),
            }
            
            # Verificar se o método pode_ser_instrutor existe e executá-lo
            if info["tem_metodo"]:
                try:
                    info["elegivel"] = aluno.pode_ser_instrutor
                    
                    # Se não for elegível, tentar determinar o motivo
                    if not info["elegivel"]:
                        # Verificar matrículas em cursos pré-iniciáticos
                        from importlib import import_module
                        try:
                            matriculas_module = import_module("matriculas.models")
                            Matricula = getattr(matriculas_module, "Matricula")
                            
                            matriculas_pre_iniciatico = Matricula.objects.filter(
                                aluno=aluno, turma__curso__nome__icontains="Pré-iniciático"
                            )
                            
                            if matriculas_pre_iniciatico.exists():
                                cursos = [m.turma.curso.nome for m in matriculas_pre_iniciatico]
                                info["motivo_inelegibilidade"] = f"Matriculado em cursos pré-iniciáticos: {', '.join(cursos)}"
                            else:
                                info["motivo_inelegibilidade"] = "Não atende aos requisitos (motivo desconhecido)"
                        except Exception as e:
                            info["motivo_inelegibilidade"] = f"Erro ao verificar matrículas: {str(e)}"
                except Exception as e:
                    info["erro"] = str(e)
            
            diagnostico.append(info)
        
        return render(
            request,
            "alunos/diagnostico_instrutores.html",
            {
                "diagnostico": diagnostico,
                "total_alunos": len(alunos_ativos),
                "total_elegiveis": sum(1 for info in diagnostico if info.get("elegivel", False)),
            },
        )
    except Exception as e:
        import traceback
        error_msg = str(e)
        stack_trace = traceback.format_exc()
        logger.error(f"Erro na página de diagnóstico: {error_msg}")
        logger.error(f"Traceback: {stack_trace}")
        
        return render(
            request,
            "alunos/erro.html",
            {
                "erro": error_msg,
                "traceback": stack_trace,
            },
        )