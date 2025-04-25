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

from importlib import import_module
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Importar a função de verificação de elegibilidade
from alunos.utils import verificar_elegibilidade_instrutor

@login_required
def diagnostico_instrutores(request):
    """Exibe um diagnóstico de elegibilidade de todos os alunos ativos para serem instrutores."""
    # Importar o modelo Aluno dinamicamente para evitar importações circulares
    alunos_module = import_module('alunos.models')
    Aluno = alunos_module.Aluno
    
    # Obter todos os alunos ativos
    alunos_ativos = Aluno.objects.filter(situacao='ATIVO')
    
    # Verificar elegibilidade de cada aluno
    alunos_diagnostico = []
    alunos_elegiveis = 0
    
    for aluno in alunos_ativos:
        elegivel, motivo = verificar_elegibilidade_instrutor(aluno)
        alunos_diagnostico.append({
            'aluno': aluno,
            'elegivel': elegivel,
            'motivo': motivo
        })
        if elegivel:
            alunos_elegiveis += 1
    
    # Calcular total de alunos inelegíveis
    total_alunos = len(alunos_ativos)
    alunos_inelegiveis = total_alunos - alunos_elegiveis
    
    # Calcular porcentagens
    porcentagem_elegiveis = (alunos_elegiveis / total_alunos * 100) if total_alunos > 0 else 0
    porcentagem_inelegiveis = (alunos_inelegiveis / total_alunos * 100) if total_alunos > 0 else 0
    
    context = {
        'alunos_diagnostico': alunos_diagnostico,
        'total_alunos': total_alunos,
        'alunos_elegiveis': alunos_elegiveis,
        'alunos_inelegiveis': alunos_inelegiveis,
        'porcentagem_elegiveis': round(porcentagem_elegiveis, 1),
        'porcentagem_inelegiveis': round(porcentagem_inelegiveis, 1),
    }
    
    return render(request, 'alunos/diagnostico_instrutores.html', context)