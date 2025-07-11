"""
Views do aplicativo Presenças.
"""

import logging
from datetime import datetime, date
from calendar import monthrange
from types import SimpleNamespace

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from atividades.models import Atividade
from presencas.models import ObservacaoPresenca, TotalAtividadeMes
from alunos.services import listar_alunos as listar_alunos_service, buscar_aluno_por_cpf as buscar_aluno_por_cpf_service
from turmas.models import Turma
from presencas.forms import TotaisAtividadesPresencaForm

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
    atividades = AtividadeAcademica.objects.all()

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
    # Corrigido o caminho do template:
    return render(request, 'presencas/academicas/listar_presencas_academicas.html', context)

@login_required
def listar_presencas_ritualisticas(request):
    aluno_id = request.GET.get('aluno', '')
    turma_id = request.GET.get('turma', '')
    atividade_id = request.GET.get('atividade', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    presencas = PresencaRitualistica.objects.all().select_related('aluno', 'turma', 'atividade')
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
    atividades = AtividadeRitualistica.objects.all()

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
    return render(request, 'presencas/ritualisticas/listar_presencas_ritualisticas.html', context)

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
            atividade = AtividadeAcademica.objects.get(id=atividade_id)
            if not aluno:
                messages.error(request, f'Aluno com CPF {aluno_id} não encontrado.')
                return redirect('presencas:listar_presencas_academicas')
        except (Turma.DoesNotExist, AtividadeAcademica.DoesNotExist) as e:
            messages.error(request, f'Erro ao localizar dados: {str(e)}')
            return redirect('presencas:listar_presencas_academicas')
        if PresencaAcademica.objects.filter(aluno=aluno, turma=turma, atividade=atividade, data=data).exists():
            messages.warning(
                request,
                f'Já existe um registro de presença para {aluno.nome} na turma {turma.nome} na data {data}.'
            )
            return redirect('presencas:listar_presencas_academicas')
        presenca = PresencaAcademica(
            aluno=aluno,
            turma=turma,
            atividade=atividade,
            data=data,
            presente=presente,
            registrado_por=request.user.username,
            data_registro=timezone.now()
        )
        presenca.save()
        if observacao:
            ObservacaoPresenca.objects.create(
                aluno=aluno,
                turma=turma,
                data=data,
                atividade_academica=atividade,
                texto=observacao,
                registrado_por=request.user.username,
                data_registro=timezone.now()
            )
        messages.success(request, f'Presença registrada com sucesso para {aluno.nome}.')
        return redirect('presencas:listar_presencas_academicas')
    alunos = listar_alunos_service()
    turmas = Turma.objects.all()
    atividades = AtividadeAcademica.objects.all()
    context = {
        'alunos': alunos,
        'turmas': turmas,
        'atividades': atividades,
        'data_hoje': timezone.now().date()
    }
    return render(request, 'presencas/academicas/registrar_presenca_academica.html', context)

@login_required
def registrar_presenca_ritualistica(request):
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
            atividade = AtividadeRitualistica.objects.get(id=atividade_id)
            if not aluno:
                messages.error(request, f'Aluno com CPF {aluno_id} não encontrado.')
                return redirect('presencas:listar_presencas_ritualisticas')
        except (Turma.DoesNotExist, AtividadeRitualistica.DoesNotExist) as e:
            messages.error(request, f'Erro ao localizar dados: {str(e)}')
            return redirect('presencas:listar_presencas_ritualisticas')
        if PresencaRitualistica.objects.filter(aluno=aluno, turma=turma, atividade=atividade, data=data).exists():
            messages.warning(
                request,
                f'Já existe um registro de presença para {aluno.nome} na turma {turma.nome} na data {data}.'
            )
            return redirect('presencas:listar_presencas_ritualisticas')
        presenca = PresencaRitualistica(
            aluno=aluno,
            turma=turma,
            atividade=atividade,
            data=data,
            presente=presente,
            registrado_por=request.user.username,
            data_registro=timezone.now()
        )
        presenca.save()
        if observacao:
            ObservacaoPresenca.objects.create(
                aluno=aluno,
                turma=turma,
                data=data,
                atividade_ritualistica=atividade,
                texto=observacao,
                registrado_por=request.user.username,
                data_registro=timezone.now()
            )
        messages.success(request, f'Presença registrada com sucesso para {aluno.nome}.')
        return redirect('presencas:listar_presencas_ritualisticas')
    alunos = listar_alunos_service()
    turmas = Turma.objects.all()
    atividades = AtividadeRitualistica.objects.all()
    context = {
        'alunos': alunos,
        'turmas': turmas,
        'atividades': atividades,
        'data_hoje': timezone.now().date()
    }
    return render(request, 'presencas/registrar_presenca_ritualistica.html', context)

@login_required
def editar_presenca_academica(request, pk):
    presenca = get_object_or_404(PresencaAcademica, pk=pk)
    if request.method == 'POST':
        presenca.presente = request.POST.get('presente') == 'on'
        presenca.data = request.POST.get('data')
        presenca.save()
        messages.success(request, 'Presença acadêmica atualizada com sucesso.')
        return redirect('presencas:listar_presencas_academicas')
    return render(request, 'presencas/editar_presenca_academica.html', {'presenca': presenca})

@login_required
def excluir_presenca_academica(request, pk):
    presenca = get_object_or_404(PresencaAcademica, pk=pk)
    if request.method == 'POST':
        presenca.delete()
        messages.success(request, 'Presença acadêmica excluída com sucesso.')
        return redirect('presencas:listar_presencas_academicas')
    return render(request, 'presencas/confirmar_exclusao_academica.html', {'presenca': presenca})

@login_required
def detalhar_presenca_academica(request, pk):
    presenca = get_object_or_404(PresencaAcademica, pk=pk)
    return render(request, 'presencas/detalhar_presenca_academica.html', {'presenca': presenca})

@login_required
def editar_presenca_ritualistica(request, pk):
    presenca = get_object_or_404(PresencaRitualistica, pk=pk)
    if request.method == 'POST':
        presenca.presente = request.POST.get('presente') == 'on'
        presenca.data = request.POST.get('data')
        presenca.save()
        messages.success(request, 'Presença ritualística atualizada com sucesso.')
        return redirect('presencas:listar_presencas_ritualisticas')
    return render(request, 'presencas/editar_presenca_ritualistica.html', {'presenca': presenca})

@login_required
def excluir_presenca_ritualistica(request, pk):
    presenca = get_object_or_404(PresencaRitualistica, pk=pk)
    if request.method == 'POST':
        presenca.delete()
        messages.success(request, 'Presença ritualística excluída com sucesso.')
        return redirect('presencas:listar_presencas_ritualisticas')
    return render(request, 'presencas/confirmar_exclusao_ritualistica.html', {'presenca': presenca})

@login_required
def detalhar_presenca_ritualistica(request, pk):
    presenca = get_object_or_404(PresencaRitualistica, pk=pk)
    return render(request, 'presencas/detalhar_presenca_ritualistica.html', {'presenca': presenca})

@login_required
def listar_observacoes_presenca(request):
    observacoes = ObservacaoPresenca.objects.select_related('aluno', 'turma', 'atividade_academica', 'atividade_ritualistica')
    return render(request, 'presencas/listar_observacoes_presenca.html', {'observacoes': observacoes})

@login_required
def exportar_presencas_academicas(request):
    # Exemplo simples: renderiza um template de exportação
    return render(request, 'presencas/academicas/exportar_presencas_academicas.html')

@login_required
def exportar_presencas_ritualisticas(request):
    # Exemplo simples: renderiza um template de exportação
    return render(request, 'presencas/ritualisticas/exportar_presencas_ritualisticas.html')

@login_required
def importar_presencas_academicas(request):
    # Exemplo simples: renderiza um template de importação
    return render(request, 'presencas/academicas/importar_presencas_academicas.html')

@login_required
def importar_presencas_ritualisticas(request):
    # Exemplo simples: renderiza um template de importação
    return render(request, 'presencas/ritualisticas/importar_presencas_ritualisticas.html')

@login_required
def registrar_presenca_totais_atividades(request):
    turma_id = request.session.get('presenca_turma_id')
    ano = request.session.get('presenca_ano')
    mes = request.session.get('presenca_mes')
    turma = Turma.objects.get(id=turma_id) if turma_id else None
    curso = turma.curso if turma else None
    atividades = []
    if turma and ano and mes:
        primeiro_dia = date(int(ano), int(mes), 1)
        ultimo_dia = date(int(ano), int(mes), monthrange(int(ano), int(mes))[1])
        atividades = AtividadeAcademica.objects.filter(
            turmas__id=turma.id
        ).filter(
            Q(data_inicio__lte=ultimo_dia) &
            (Q(data_fim__isnull=True) | Q(data_fim__gte=primeiro_dia))
        ).distinct()
    totais_registrados = []
    if turma and ano and mes:
        totais_registrados = TotalAtividadeMes.objects.filter(
            turma=turma, ano=ano, mes=mes
        ).select_related('atividade')
    if request.method == 'POST':
        form = TotaisAtividadesPresencaForm(request.POST, atividades=atividades)
        if form.is_valid():
            request.session['presenca_totais_atividades'] = {
                key: value for key, value in form.cleaned_data.items() if key.startswith('qtd_ativ_')
            }
            return redirect('presencas:registrar_presenca_dias_atividades')
    else:
        form = TotaisAtividadesPresencaForm(atividades=atividades)
    return render(request, 'presencas/registrar_presenca_totais_atividades.html', {
        'form': form,
        'turma': turma,
        'curso': curso,
        'ano': ano,
        'mes': mes,
        'atividades': atividades,
        'totais_registrados': totais_registrados,
    })

@login_required
def registrar_presenca_dias_atividades(request):
    """
    GET: Exibe o formulário para seleção dos dias e observações das atividades.
    POST: Salva no banco os dias e observações selecionados para cada atividade.
    """
    if request.method == 'GET':
        turma_id = request.session.get('presenca_turma_id')
        ano = request.session.get('presenca_ano')
        mes = request.session.get('presenca_mes')
        turma = Turma.objects.get(id=turma_id) if turma_id else None
        totais_atividades = request.session.get('presenca_totais_atividades', {})
        atividades = []
        resumo_atividades = []
        if turma and ano and mes:
            primeiro_dia = date(int(ano), int(mes), 1)
            ultimo_dia = date(int(ano), int(mes), monthrange(int(ano), int(mes))[1])
            atividades_queryset = AtividadeAcademica.objects.filter(
                turmas__id=turma.id
            ).filter(
                Q(data_inicio__lte=ultimo_dia) &
                (Q(data_fim__isnull=True) | Q(data_fim__gte=primeiro_dia))
            ).distinct().order_by('nome')
            atividades = list(atividades_queryset)
            for atividade in atividades:
                key = f'qtd_ativ_{atividade.id}'
                try:
                    qtd = int(totais_atividades.get(key, 0))
                except (ValueError, TypeError):
                    qtd = 0
                resumo_atividades.append(SimpleNamespace(
                    id=atividade.id,
                    nome=atividade.nome,
                    qtd_ativ_mes=qtd
                ))
        qtd_dias = monthrange(int(ano), int(mes))[1]
        dias_do_mes = list(range(1, qtd_dias + 1))
        presencas = {}
        presencas_obs = {}
        if turma and ano and mes and atividades:
            observacoes = ObservacaoPresenca.objects.filter(
                turma=turma,
                data__year=ano,
                data__month=mes,
                atividade_academica__in=[a.id for a in atividades]
            )
            for obs in observacoes:
                aid = obs.atividade_academica_id
                dia = obs.data.day
                presencas.setdefault(aid, []).append(dia)
                presencas_obs.setdefault(aid, {})[dia] = obs.texto
        context = {
            'atividades': atividades,
            'dias_do_mes': dias_do_mes,
            'mes': mes,
            'ano': ano,
            'presencas': presencas,
            'presencas_obs': presencas_obs,
            'resumo_atividades': resumo_atividades,
        }
        return render(request, 'presencas/registrar_presenca_dias_atividades.html', context)
    # POST
    turma_id = request.session.get('presenca_turma_id')
    ano = request.session.get('presenca_ano')
    mes = request.session.get('presenca_mes')
    turma = Turma.objects.get(id=turma_id) if turma_id else None
    for key in request.POST:
        if key.startswith('presenca_'):
            atividade_id = key.replace('presenca_', '')
            dias = request.POST.getlist(key)
            for dia in dias:
                obs = request.POST.get(f'obs_{atividade_id}_{dia}', '')
                try:
                    atividade = AtividadeAcademica.objects.get(id=atividade_id)
                except AtividadeAcademica.DoesNotExist:
                    continue
                try:
                    data = date(int(ano), int(mes), int(dia))
                except (ValueError, TypeError):
                    continue
                ObservacaoPresenca.objects.create(
                    aluno=None,  # ou defina o aluno se necessário
                    turma=turma,
                    data=data,
                    atividade_academica=atividade,
                    texto=obs,
                    registrado_por=request.user.username,
                    data_registro=timezone.now()
                )
    return redirect('presencas:registrar_presenca_alunos')

@login_required
@require_POST
@csrf_exempt
def registrar_presenca_totais_atividades_ajax(request):
    turma_id = request.session.get('presenca_turma_id')
    ano = request.session.get('presenca_ano')
    mes = request.session.get('presenca_mes')
    turma = Turma.objects.get(id=turma_id) if turma_id else None
    atividades = []
    if turma and ano and mes:
        primeiro_dia = date(int(ano), int(mes), 1)
        ultimo_dia = date(int(ano), int(mes), monthrange(int(ano), int(mes))[1])
        atividades = AtividadeAcademica.objects.filter(
            turmas__id=turma.id
        ).filter(
            Q(data_inicio__lte=ultimo_dia) &
            (Q(data_fim__isnull=True) | Q(data_fim__gte=primeiro_dia))
        ).distinct()
    form = TotaisAtividadesPresencaForm(request.POST, atividades=atividades)
    if form.is_valid():
        request.session['presenca_totais_atividades'] = {
            key: value for key, value in form.cleaned_data.items() if key.startswith('qtd_ativ_')
        }
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})

@login_required
def registrar_presenca_dados_basicos(request):
    """
    Primeira etapa do fluxo multi-etapas de registro de presenças acadêmicas.
    Exibe formulário para seleção de turma, ano e mês.
    Limpa variáveis de sessão para evitar sobreposição de dados antigos.
    """
    for key in [
        'presenca_totais_atividades',
        'presenca_turma_id',
        'presenca_ano',
        'presenca_mes'
    ]:
        request.session.pop(key, None)
    turmas = Turma.objects.all()
    anos = list(range(datetime.now().year - 5, datetime.now().year + 2))
    meses = [
        {'numero': i, 'nome': date(1900, i, 1).strftime('%B').capitalize()}
        for i in range(1, 13)
    ]
    if request.method == 'POST':
        turma_id = request.POST.get('turma')
        ano = request.POST.get('ano')
        mes = request.POST.get('mes')
        if not turma_id or not ano or not mes:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return render(request, 'presencas/registrar_presenca_dados_basicos.html', {
                'turmas': turmas,
                'anos': anos,
                'meses': meses
            })
        request.session['presenca_turma_id'] = turma_id
        request.session['presenca_ano'] = ano
        request.session['presenca_mes'] = mes
        return redirect('presencas:registrar_presenca_totais_atividades')
    context = {
        'turmas': turmas,
        'anos': anos,
        'meses': meses,
        'breadcrumb': [
            {'etapa': 'Dados Básicos', 'ativa': True},
            {'etapa': 'Totais de Atividades', 'ativa': False},
            {'etapa': 'Dias de Atividades', 'ativa': False},
            {'etapa': 'Alunos', 'ativa': False},
        ],
        'titulo_pagina': 'Registrar Presença - Dados Básicos',
        'descricao_pagina': 'Selecione a turma, ano e mês para iniciar o registro de presenças.',
    }
    return render(request, 'presencas/registrar_presenca_dados_basicos.html', context)