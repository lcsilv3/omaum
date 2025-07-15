"""
Views do aplicativo Presenças.
"""

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from atividades.models import Atividade
from presencas.models import ObservacaoPresenca, PresencaAcademica
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

    presencas = PresencaAcademica.objects.all().select_related('aluno', 'turma', 'atividade')
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

    alunos = listar_alunos_service()
    turmas = Turma.objects.all()
    atividades = Atividade.objects.all()

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
            turma = Turma.objects.get(id=turma_id)
            atividade = Atividade.objects.get(id=atividade_id)
            if not aluno:
                messages.error(request, f'Aluno com CPF {aluno_id} não encontrado.')
                return redirect('presencas:listar_presencas_academicas')
            
            presenca, created = PresencaAcademica.objects.get_or_create(
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
        except Exception as e:
            messages.error(request, f'Erro ao registrar presença: {str(e)}')
            return redirect('presencas:listar_presencas_academicas')
    
    alunos = listar_alunos_service()
    turmas = Turma.objects.all()
    atividades = Atividade.objects.all()
    
    context = {
        'alunos': alunos,
        'turmas': turmas,
        'atividades': atividades,
        'data_hoje': timezone.now().date()
    }
    return render(request, 'presencas/academicas/registrar_presenca_academica.html', context)

@login_required
def editar_presenca_academica(request, pk):
    presenca = get_object_or_404(PresencaAcademica, pk=pk)
    
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
    presenca = get_object_or_404(PresencaAcademica, pk=pk)
    
    if request.method == 'POST':
        presenca.delete()
        messages.success(request, 'Presença excluída com sucesso!')
        return redirect('presencas:listar_presencas_academicas')
    
    context = {'presenca': presenca}
    return render(request, 'presencas/academicas/excluir_presenca_academica.html', context)

@login_required
def detalhar_presenca_academica(request, pk):
    presenca = get_object_or_404(PresencaAcademica, pk=pk)
    context = {'presenca': presenca}
    return render(request, 'presencas/academicas/detalhar_presenca_academica.html', context)

@login_required
def exportar_presencas_academicas(request):
    return render(request, 'presencas/academicas/exportar_presencas_academicas.html')

@login_required
def importar_presencas_academicas(request):
    return render(request, 'presencas/academicas/importar_presencas_academicas.html')

@login_required
def listar_observacoes_presenca(request):
    observacoes = ObservacaoPresenca.objects.all().order_by('-data_registro')
    context = {'observacoes': observacoes}
    return render(request, 'presencas/listar_observacoes_presenca.html', context)

# Stubs para views ritualísticas (removidas)
@login_required
def listar_presencas_ritualisticas(request):
    messages.warning(request, 'Presenças ritualísticas não estão mais disponíveis.')
    return redirect('presencas:listar_presencas_academicas')

@login_required
def registrar_presenca_ritualistica(request):
    messages.warning(request, 'Presenças ritualísticas não estão mais disponíveis.')
    return redirect('presencas:listar_presencas_academicas')

@login_required
def editar_presenca_ritualistica(request, pk):
    messages.warning(request, 'Presenças ritualísticas não estão mais disponíveis.')
    return redirect('presencas:listar_presencas_academicas')

@login_required
def excluir_presenca_ritualistica(request, pk):
    messages.warning(request, 'Presenças ritualísticas não estão mais disponíveis.')
    return redirect('presencas:listar_presencas_academicas')

@login_required
def detalhar_presenca_ritualistica(request, pk):
    messages.warning(request, 'Presenças ritualísticas não estão mais disponíveis.')
    return redirect('presencas:listar_presencas_academicas')

@login_required
def exportar_presencas_ritualisticas(request):
    messages.warning(request, 'Presenças ritualísticas não estão mais disponíveis.')
    return redirect('presencas:listar_presencas_academicas')

@login_required
def importar_presencas_ritualisticas(request):
    messages.warning(request, 'Presenças ritualísticas não estão mais disponíveis.')
    return redirect('presencas:listar_presencas_academicas')
