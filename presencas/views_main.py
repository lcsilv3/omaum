"""
Views do aplicativo Presenças.
"""

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from atividades.models import Atividade
from presencas.models import ObservacaoPresenca, Presenca
from alunos.services import listar_alunos as listar_alunos_service, buscar_aluno_por_cpf as buscar_aluno_por_cpf_service
from turmas.models import Turma

logger = logging.getLogger(__name__)

@login_required
def listar_presencas_academicas(request):
    aluno_id = request.GET.get('aluno', '')
    turma_id = request.GET.get('turma', '')
    atividade_id = request.GET.get('atividade', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    # Query otimizada com relacionamentos e paginação
    presencas = Presenca.objects.select_related(
        'aluno', 'turma__curso', 'atividade'
    ).prefetch_related(
        'aluno__historicos'  # Se necessário para dados relacionados
    )
    
    if aluno_id:
        presencas = presencas.filter(aluno__cpf=aluno_id)
    if turma_id:
        presencas = presencas.filter(turma__id=turma_id)
    if atividade_id:
        presencas = presencas.filter(atividade__id=atividade_id)
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)

    # Ordenação consistente
    presencas = presencas.order_by('-data', 'aluno__nome')

    try:
        alunos_queryset = listar_alunos_service()
        # listar_alunos_service agora retorna um queryset, não um objeto paginado
        alunos = list(alunos_queryset) if alunos_queryset else []
    except Exception as e:
        logger.error(f"Erro ao listar alunos: {str(e)}")
        alunos = []
    
    # Carregamento otimizado de listas de referência  
    turmas = Turma.objects.select_related('curso').only('id', 'nome', 'curso__nome')
    atividades = Atividade.objects.only('id', 'nome', 'tipo')

    context = {
        'presencas': presencas,
        'alunos': alunos,
        'turmas': turmas,
        'atividades': atividades,
        'filtros': {
            'aluno': aluno_id,
            'turma': turma_id,
            'atividade': atividade_id,
            'data_inicio': data_inicio,
            'data_fim': data_fim
        }
    }
    return render(request, 'presencas/academicas/listar_presencas_academicas.html', context)

@login_required
def registrar_presenca_academica(request):
    if request.method == 'POST':
        aluno_id = request.POST.get('aluno')
        turma_id = request.POST.get('turma')
        atividade_id = request.POST.get('atividade')
        data = request.POST.get('data')
        presente = request.POST.get('presente') == 'on'
        observacao = request.POST.get('observacao', '')
        try:
            aluno = buscar_aluno_por_cpf_service(aluno_id)
            # Otimização: usar get_object_or_404 para melhor performance
            turma = get_object_or_404(Turma, id=turma_id)
            atividade = get_object_or_404(Atividade, id=atividade_id)
            if not aluno:
                messages.error(request, f'Aluno com CPF {aluno_id} não encontrado.')
                return redirect('presencas:listar_presencas_academicas')
            
            presenca, created = Presenca.objects.get_or_create(
                aluno=aluno,
                turma=turma,
                atividade=atividade,
                data=data,
                defaults={
                    'presente': presente,
                    'registrado_por': request.user.username,
                    'data_registro': timezone.now()
                }
            )
            if not created:
                presenca.presente = presente
                presenca.registrado_por = request.user.username
                presenca.data_registro = timezone.now()
            presenca.save()
            if observacao:
                ObservacaoPresenca.objects.create(
                    aluno=aluno,
                    turma=turma,
                    data=data,
                    atividade=atividade,
                    texto=observacao,
                    registrado_por=request.user.username,
                    data_registro=timezone.now()
                )
            messages.success(request, 'Presença registrada com sucesso!')
            return redirect('presencas:listar_presencas_academicas')
        except (Turma.DoesNotExist, Atividade.DoesNotExist) as e:
            messages.error(request, f'Dados inválidos: {str(e)}')
            return redirect('presencas:listar_presencas_academicas')
        except Exception as e:
            logger.error(f"Erro ao registrar presença: {str(e)}")
            messages.error(request, f'Erro ao registrar presença: {str(e)}')
            return redirect('presencas:listar_presencas_academicas')
    
    try:
        alunos_queryset = listar_alunos_service()
        # listar_alunos_service agora retorna um queryset, não um objeto paginado
        alunos = list(alunos_queryset) if alunos_queryset else []
    except Exception as e:
        logger.error(f"Erro ao listar alunos: {str(e)}")
        alunos = []
    
    # Carregamento otimizado de listas de referência
    turmas = Turma.objects.select_related('curso').only('id', 'nome', 'curso__nome')
    atividades = Atividade.objects.only('id', 'nome', 'tipo')
    
    context = {
        'alunos': alunos,
        'turmas': turmas,
        'atividades': atividades,
        'data_hoje': timezone.now().date()
    }
    return render(request, 'presencas/academicas/registrar_presenca_academica.html', context)

@login_required
def editar_presenca_academica(request, pk):
    presenca = get_object_or_404(Presenca, pk=pk)
    
    if request.method == 'POST':
        # Lógica de edição
        presente = request.POST.get('presente') == 'on'
        request.POST.get('observacao', '')
        
        presenca.presente = presente
        presenca.save()
        
        messages.success(request, 'Presença atualizada com sucesso!')
        return redirect('presencas:listar_presencas_academicas')
    
    context = {
        'presenca': presenca,
        'data_hoje': timezone.now().date()
    }
    return render(request, 'presencas/academicas/editar_presenca_academica.html', context)

@login_required
def excluir_presenca_academica(request, pk):
    presenca = get_object_or_404(Presenca, pk=pk)
    
    if request.method == 'POST':
        presenca.delete()
        messages.success(request, 'Presença excluída com sucesso!')
        return redirect('presencas:listar_presencas_academicas')
    
    context = {'presenca': presenca}
    return render(request, 'presencas/academicas/excluir_presenca_academica.html', context)

@login_required
def detalhar_presenca_academica(request, pk):
    presenca = get_object_or_404(Presenca, pk=pk)
    context = {'presenca': presenca}
    return render(request, 'presencas/academicas/detalhar_presenca_academica.html', context)

# ===== FUNÇÕES ACADÊMICAS IMPLEMENTADAS =====

@login_required
def listar_observacoes_presenca(request):
    """Lista todas as observações de presença."""
    observacoes = ObservacaoPresenca.objects.all().order_by('-data_registro')
    context = {'observacoes': observacoes}
    return render(request, 'presencas/listar_observacoes_presenca.html', context)

# ===== FUNÇÕES PLACEHOLDER - IMPLEMENTAÇÃO FUTURA =====

@login_required
def exportar_presencas_academicas(request):
    """Placeholder: função de exportação será implementada conforme demanda."""
    return HttpResponse("Função de exportação em desenvolvimento - usar relatórios")

@login_required
def importar_presencas_academicas(request):
    """Placeholder: função de importação será implementada conforme demanda."""
    return HttpResponse("Função de importação em desenvolvimento")

# ===== STUBS PARA VIEWS RITUALÍSTICAS (DESCONTINUADAS) =====

@login_required
def listar_presencas_ritualisticas(request):
    messages.warning(request, 'Presenças ritualísticas foram descontinuadas. Use o sistema acadêmico.')
    return redirect('presencas:listar_presencas_academicas')

@login_required
def registrar_presenca_ritualistica(request):
    messages.warning(request, 'Presenças ritualísticas foram descontinuadas. Use o sistema acadêmico.')
    return redirect('presencas:listar_presencas_academicas')

@login_required
def editar_presenca_ritualistica(request, pk):
    messages.warning(request, 'Presenças ritualísticas foram descontinuadas. Use o sistema acadêmico.')
    return redirect('presencas:listar_presencas_academicas')

@login_required
def excluir_presenca_ritualistica(request, pk):
    messages.warning(request, 'Presenças ritualísticas foram descontinuadas. Use o sistema acadêmico.')
    return redirect('presencas:listar_presencas_academicas')

@login_required
def detalhar_presenca_ritualistica(request, pk):
    messages.warning(request, 'Presenças ritualísticas foram descontinuadas. Use o sistema acadêmico.')
    return redirect('presencas:listar_presencas_academicas')

@login_required
def exportar_presencas_ritualisticas(request):
    messages.warning(request, 'Presenças ritualísticas foram descontinuadas. Use o sistema acadêmico.')
    return redirect('presencas:listar_presencas_academicas')

@login_required
def importar_presencas_ritualisticas(request):
    messages.warning(request, 'Presenças ritualísticas foram descontinuadas. Use o sistema acadêmico.')
    return redirect('presencas:listar_presencas_academicas')
