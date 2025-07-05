"""
Views de registro de presença acadêmica (multi-etapas).
"""

import logging
from datetime import date
from calendar import monthrange
from types import SimpleNamespace

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from presencas.forms import (
    RegistrarPresencaForm,
    TotaisAtividadesPresencaForm,
    AlunosPresencaForm
)
from cursos.models import Curso
from turmas.models import Turma
from atividades.models import AtividadeAcademica, PresencaAcademica
from presencas.models import TotalAtividadeMes, ObservacaoPresenca
from alunos.models import Aluno

logger = logging.getLogger(__name__)

@login_required
def registrar_presenca_dados_basicos(request):
    """Exibe o formulário de dados básicos para registro de presença acadêmica."""
    form = RegistrarPresencaForm()
    return render(request, 'presencas/registrar_presenca_dados_basicos.html', {
        'form': form,
    })

@login_required
@require_POST
def registrar_presenca_dados_basicos_ajax(request):
    """Recebe dados básicos via AJAX e armazena na sessão."""
    form = RegistrarPresencaForm(request.POST)
    if form.is_valid():
        request.session['presenca_turma_id'] = form.cleaned_data['turma'].id
        request.session['presenca_ano'] = form.cleaned_data['ano']
        request.session['presenca_mes'] = form.cleaned_data['mes']
        return JsonResponse({'success': True, 'redirect_url': '/presencas/registrar-presenca/totais-atividades/'})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})

@login_required
def registrar_presenca_totais_atividades(request):
    """Exibe e processa o formulário de totais de atividades."""
    turma_id = request.session.get('presenca_turma_id')
    ano = request.session.get('presenca_ano')
    mes = request.session.get('presenca_mes')
    turma = Turma.objects.get(id=turma_id) if turma_id else None
    curso = turma.curso if turma else None
    atividades = []
    if turma and curso and ano and mes:
        totais_atividades = request.session.get('presenca_totais_atividades', {})
        if totais_atividades:
            atividades_ids = [int(key.replace('qtd_ativ_', '')) for key in totais_atividades.keys() if int(totais_atividades[key]) > 0]
            atividades = AtividadeAcademica.objects.filter(
                id__in=atividades_ids,
                turmas__id=turma.id,
            )
        else:
            primeiro_dia = date(int(ano), int(mes), 1)
            ultimo_dia = date(int(ano), int(mes), monthrange(int(ano), int(mes))[1])
            atividades = AtividadeAcademica.objects.filter(
                turmas__id=turma.id,
                curso=curso
            ).filter(
                Q(data_inicio__lte=ultimo_dia) &
                (Q(data_fim__isnull=True) | Q(data_fim__gte=primeiro_dia))
            ).distinct()
    totais_registrados = []
    if turma and ano and mes:
        totais_registrados = TotalAtividadeMes.objects.filter(
            turma=turma, ano=ano, mes=mes
        ).select_related('atividade')
    logger.debug("IDs das atividades passadas para o formulário: %s", [a.id for a in atividades])
    request.session['presenca_atividades_ids'] = [a.id for a in atividades]
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
@require_POST
@csrf_exempt
def registrar_presenca_totais_atividades_ajax(request):
    turma_id = request.session.get('presenca_turma_id')
    ano = request.session.get('presenca_ano')
    mes = request.session.get('presenca_mes')
    turma = Turma.objects.get(id=turma_id) if turma_id else None

    atividades = []
    if turma and ano and mes:
        atividades_ids = request.session.get('presenca_atividades_ids', [])
        if atividades_ids:
            atividades = AtividadeAcademica.objects.filter(
                id__in=atividades_ids,
                turmas__id=turma.id
            )
        else:
            # Fallback para o filtro padrão
            primeiro_dia = date(int(ano), int(mes), 1)
            ultimo_dia = date(int(ano), int(mes), monthrange(int(ano), int(mes))[1])
            atividades = AtividadeAcademica.objects.filter(
                turmas__id=turma.id
            ).filter(
                Q(data_inicio__lte=ultimo_dia) &
                (Q(data_fim__isnull=True) | Q(data_fim__gte=primeiro_dia))
            ).distinct()

    logger.debug("[AJAX] IDs das atividades passadas para o formulário: %s", [a.id for a in atividades])

    form = TotaisAtividadesPresencaForm(request.POST, atividades=atividades)
    if form.is_valid():
        request.session['presenca_totais_atividades'] = {
            key: value for key, value in form.cleaned_data.items() if key.startswith('qtd_ativ_')
        }
        request.session.modified = True
        return JsonResponse({
            'success': True,
            'redirect_url': '/presencas/registrar-presenca/dias-atividades/'
        })
    else:
        return JsonResponse({'success': False, 'errors': form.errors})

@login_required
def registrar_presenca_dias_atividades(request):
    if request.method == 'GET':
        turma_id = request.session.get('presenca_turma_id')
        ano = request.session.get('presenca_ano')
        mes = request.session.get('presenca_mes')
        turma = Turma.objects.get(id=turma_id) if turma_id else None

        totais_atividades = request.session.get('presenca_totais_atividades', {})
        atividades = []
        resumo_atividades = []
        atividades_ids_totais = []
        if turma and ano and mes:
            # Filtro único: todas as atividades da turma para o mês/ano
            primeiro_dia = date(int(ano), int(mes), 1)
            ultimo_dia = date(int(ano), int(mes), monthrange(int(ano), int(mes))[1])
            atividades_queryset = AtividadeAcademica.objects.filter(
                turmas__id=turma.id,
            ).filter(
                Q(data_inicio__lte=ultimo_dia) &
                (Q(data_fim__isnull=True) | Q(data_fim__gte=primeiro_dia))
            ).distinct().order_by('nome')
            atividades = list(atividades_queryset)
            # Monta o resumo: nome e total (zero se não informado) como objeto
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
                if qtd > 0:
                    atividades_ids_totais.append(atividade.id)
            # Filtra atividades para exibir apenas as selecionadas na etapa de totais
            atividades = [a for a in atividades if a.id in atividades_ids_totais]
            # Preenche qtd_ativ_mes em cada atividade
            for atividade in atividades:
                key = f'qtd_ativ_{atividade.id}'
                try:
                    qtd = int(totais_atividades.get(key, 0))
                except (ValueError, TypeError):
                    qtd = 0
                atividade.qtd_ativ_mes = qtd
        # Dias do mês
        qtd_dias = monthrange(int(ano), int(mes))[1]
        dias_do_mes = list(range(1, qtd_dias + 1))

        # Busca dias já selecionados para cada atividade
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
                    registrado_por=request.user.username
                )
    return redirect('presencas:registrar_presenca_alunos')

@login_required
def registrar_presenca_alunos(request):
    turma_id = request.session.get('presenca_turma_id')
    if not turma_id:
        messages.error(request, 'Selecione a turma antes de marcar presença nos alunos.')
        return redirect('presencas:registrar_presenca_dados_basicos')
    turma = Turma.objects.get(id=turma_id)
    convocados_dict = request.session.get('presenca_convocados', {})
    alunos = Aluno.objects.filter(matricula__turma=turma, situacao='ATIVO').distinct()
    # Se houver convocação, filtra apenas os convocados
    if convocados_dict:
        alunos_ids = set()
        for ids in convocados_dict.values():
            alunos_ids.update(ids)
        alunos = alunos.filter(id__in=alunos_ids)
    # Loga caso não haja alunos
    if not alunos.exists():
        logger.warning(f"Nenhum aluno encontrado para a turma {turma} (ID: {turma.id}) ou filtro de convocados. Usuário: {request.user}")
        messages.warning(request, "Nenhum aluno disponível para marcação de presença nesta etapa. Revise as etapas anteriores ou contate o suporte.")
    form = AlunosPresencaForm(alunos=alunos)
    return render(request, 'presencas/registrar_presenca_alunos.html', {
        'form': form,
        'alunos': alunos,
        'turma': turma,
    })

@login_required
@require_POST
@csrf_exempt
def registrar_presenca_alunos_ajax(request):
    turma_id = request.session.get('presenca_turma_id')
    turma = Turma.objects.get(id=turma_id) if turma_id else None
    # Recupera lista de alunos convocados da sessão (por atividade, se necessário)
    convocados_dict = request.session.get('presenca_convocados', {})
    alunos = Aluno.objects.filter(matricula__turma=turma, situacao='ATIVO').distinct() if turma else []
    # Se houver convocação, filtra apenas os convocados
    if convocados_dict:
        alunos_ids = set()
        for ids in convocados_dict.values():
            alunos_ids.update(ids)
        alunos = alunos.filter(id__in=alunos_ids)
    # Processa status de cada aluno
    resultado = {}
    for aluno in alunos:
        status = request.POST.get(f'aluno_{aluno.id}_status', 'presente')
        justificativa = request.POST.get(f'aluno_{aluno.id}_justificativa', '')
        resultado[aluno.id] = {'status': status, 'justificativa': justificativa}
    request.session['presenca_alunos_status'] = resultado
    return JsonResponse({'success': True, 'redirect_url': '/presencas/registrar-presenca/confirmar/'})

@login_required
def turmas_por_curso_ajax(request):
    curso_id = request.GET.get('curso_id')
    turmas = Turma.objects.filter(curso_id=curso_id).values('id', 'nome')
    return JsonResponse(list(turmas), safe=False)

@login_required
def atividades_por_turma_ajax(request):
    turma_id = request.GET.get('turma_id')
    atividades = AtividadeAcademica.objects.filter(turmas__id=turma_id).values('id', 'nome')
    return JsonResponse(list(atividades), safe=False)

@login_required
def registrar_presenca_confirmar(request):
    turma_id = request.session.get('presenca_turma_id')
    ano = request.session.get('presenca_ano')
    mes = request.session.get('presenca_mes')
    turma = Turma.objects.get(id=turma_id) if turma_id else None
    alunos_status = request.session.get('presenca_alunos_status', {})
    alunos = Aluno.objects.filter(id__in=alunos_status.keys()) if alunos_status else []
    alunos_info = []
    for aluno in alunos:
        status = alunos_status.get(str(aluno.id)) or alunos_status.get(aluno.id) or {}
        alunos_info.append({
            'aluno': aluno,
            'status': status.get('status', 'presente'),
            'justificativa': status.get('justificativa', ''),
        })
    return render(request, 'presencas/registrar_presenca_confirmar.html', {
        'turma': turma,
        'ano': ano,
        'mes': mes,
        'alunos_info': alunos_info,
    })

@login_required
@require_POST
@transaction.atomic
def registrar_presenca_confirmar_ajax(request):
    turma_id = request.session.get('presenca_turma_id')
    ano = request.session.get('presenca_ano')
    mes = request.session.get('presenca_mes')
    turma = Turma.objects.get(id=turma_id) if turma_id else None
    alunos_status = request.session.get('presenca_alunos_status', {})
    atividades = AtividadeAcademica.objects.filter(turmas__id=turma.id) if turma else []
    dias_atividades = request.session.get('presenca_totais_atividades', {})
    for atividade in atividades:
        # Para cada atividade, obter dias e alunos convocados
        dias = []
        key = f'qtd_ativ_{atividade.id}'
        qtd = int(dias_atividades.get(key, 0))
        if qtd > 0:
            dias = range(1, qtd + 1)
        # Filtra alunos convocados se necessário
        convocados_dict = request.session.get('presenca_convocados', {})
        if atividade.convocacao and str(atividade.id) in convocados_dict:
            alunos_ids = convocados_dict[str(atividade.id)]
        else:
            alunos_ids = alunos_status.keys()
        for aluno_id in alunos_ids:
            status_info = alunos_status.get(str(aluno_id)) or alunos_status.get(aluno_id) or {}
            presente = status_info.get('status', 'presente') == 'presente'
            justificativa = status_info.get('justificativa', '')
            for dia in dias:
                data = date(int(ano), int(mes), dia)
                PresencaAcademica.objects.create(
                    aluno_id=aluno_id,
                    turma=turma,
                    atividade=atividade,
                    data=data,
                    presente=presente,
                    registrado_por=request.user.username,
                    data_registro=date.today(),
                    justificativa=justificativa if not presente else ''
                )
    # Limpa sessão
    for key in [
        'presenca_turma_id', 'presenca_ano', 'presenca_mes',
        'presenca_atividade_id', 'presenca_alunos_presentes',
        'presenca_totais_atividades', 'presenca_convocados',
        'presenca_alunos_status'
    ]:
        if key in request.session:
            del request.session[key]
    return JsonResponse({'success': True, 'redirect_url': '/presencas/'})

@login_required
def obter_limites_calendario_ajax(request):
    turma_id = request.GET.get('turma_id')
    if not turma_id:
        return JsonResponse({'erro': 'Turma não informada.'}, status=400)
    try:
        turma = Turma.objects.get(id=turma_id)
        data_inicio = turma.data_inicio_ativ
        data_fim = turma.data_termino_atividades

        if not data_inicio or not data_fim:
            return JsonResponse({'erro': 'A turma selecionada não possui datas de início ou término definidas. Por favor, verifique o cadastro da turma.'}, status=400)

        return JsonResponse({
            'data_inicio': data_inicio.strftime('%Y-%m'),
            'data_fim': data_fim.strftime('%Y-%m')
        })
    except Turma.DoesNotExist:
        return JsonResponse({'erro': 'Turma não encontrada.'}, status=404)

@login_required
@require_POST
def registrar_presenca_dias_atividades_ajax(request):
    from datetime import date
    turma_id = request.session.get('presenca_turma_id')
    ano = request.session.get('presenca_ano')
    mes = request.session.get('presenca_mes')
    turma = Turma.objects.get(id=turma_id) if turma_id else None

    if not turma or not ano or not mes:
        return JsonResponse({'success': False, 'message': 'Dados de sessão ausentes. Refaça o processo.'})

    # Remove observações anteriores para evitar duplicidade
    atividades = AtividadeAcademica.objects.filter(
        turmas__id=turma.id,
        data_inicio__year=ano,
        data_inicio__month=mes
    )
    ObservacaoPresenca.objects.filter(
        turma=turma,
        data__year=ano,
        data__month=mes,
        atividade_academica__in=atividades
    ).delete()

    try:
        for key in request.POST:
            if key.startswith('presenca_'):
                atividade_id = key.replace('presenca_', '')
                dias = request.POST.getlist(key)
                for dia in dias:
                    obs = request.POST.get(f'obs_{atividade_id}_{dia}', '')
                    try:
                        atividade = AtividadeAcademica.objects.get(id=atividade_id)
                        data = date(int(ano), int(mes), int(dia))
                        ObservacaoPresenca.objects.create(
                            aluno=None,
                            turma=turma,
                            data=data,
                            atividade_academica=atividade,
                            texto=obs,
                            registrado_por=request.user.username
                        )
                    except (AtividadeAcademica.DoesNotExist, ValueError, TypeError) as e:
                        logger.exception('Erro ao registrar observação para atividade %s, dia %s: %s', atividade_id, dia, e)
                        continue
        return JsonResponse({'success': True, 'redirect_url': '/presencas/registrar-presenca/alunos/', 'message': 'Presenças salvas com sucesso!'})
    except Exception as e:
        logger.exception('Erro inesperado ao salvar presenças: %s', e)
        return JsonResponse({'success': False, 'message': f'Erro ao salvar: {str(e)}'})

@login_required
def editar_presenca_dados_basicos(request, pk):
    presenca = get_object_or_404(PresencaAcademica, pk=pk)
    if request.method == 'POST':
        form = DadosBasicosPresencaForm(request.POST, instance=presenca)
        if form.is_valid():
            form.save()
            return redirect('editar_presenca_totais_atividades', pk=pk)
    else:
        form = DadosBasicosPresencaForm(instance=presenca)
    return render(request, 'presencas/academicas/editar_presenca_dados_basicos.html', {'form': form, 'presenca': presenca})

@login_required
def editar_presenca_totais_atividades(request, pk):
    presenca = get_object_or_404(PresencaAcademica, pk=pk)
    if request.method == 'POST':
        form = TotaisAtividadesPresencaForm(request.POST, instance=presenca)
        if form.is_valid():
            form.save()
            return redirect('editar_presenca_dias_atividades', pk=pk)
    else:
        form = TotaisAtividadesPresencaForm(instance=presenca)
    return render(request, 'presencas/academicas/editar_presenca_totais_atividades.html', {'form': form, 'presenca': presenca})

@login_required
def editar_presenca_dias_atividades(request, pk):
    presenca = get_object_or_404(PresencaAcademica, pk=pk)
    if request.method == 'POST':
        form = DiasAtividadesPresencaForm(request.POST, instance=presenca)
        if form.is_valid():
            form.save()
            return redirect('editar_presenca_alunos', pk=pk)
    else:
        form = DiasAtividadesPresencaForm(instance=presenca)
    return render(request, 'presencas/academicas/editar_presenca_dias_atividades.html', {'form': form, 'presenca': presenca})

from django.contrib import messages

@login_required
def editar_presenca_alunos(request, pk):
    presenca = get_object_or_404(PresencaAcademica, pk=pk)
    if request.method == 'POST':
        form = AlunosPresencaForm(request.POST, instance=presenca)
        if form.is_valid():
            form.save()
            messages.success(request, 'Presença acadêmica atualizada com sucesso.')
            return redirect('listar_presencas_academicas')
    else:
        form = AlunosPresencaForm(instance=presenca)
    return render(request, 'presencas/academicas/editar_presenca_alunos.html', {'form': form, 'presenca': presenca})

@login_required
def detalhar_presenca_dados_basicos(request, pk):
    presenca = get_object_or_404(PresencaAcademica, pk=pk)
    return render(request, 'presencas/academicas/detalhar_presenca_dados_basicos.html', {'presenca': presenca})

@login_required
def detalhar_presenca_totais_atividades(request, pk):
    presenca = get_object_or_404(PresencaAcademica, pk=pk)
    return render(request, 'presencas/academicas/detalhar_presenca_totais_atividades.html', {'presenca': presenca})

@login_required
def detalhar_presenca_dias_atividades(request, pk):
    presenca = get_object_or_404(PresencaAcademica, pk=pk)
    return render(request, 'presencas/academicas/detalhar_presenca_dias_atividades.html', {'presenca': presenca})

@login_required
def detalhar_presenca_alunos(request, pk):
    presenca = get_object_or_404(PresencaAcademica, pk=pk)
    return render(request, 'presencas/academicas/detalhar_presenca_alunos.html', {'presenca': presenca})

@login_required
@csrf_exempt
def registrar_presenca_convocados(request):
    turma_id = request.session.get('presenca_turma_id')
    ano = request.session.get('presenca_ano')
    mes = request.session.get('presenca_mes')
    turma = Turma.objects.get(id=turma_id) if turma_id else None
    atividades = AtividadeAcademica.objects.filter(turmas__id=turma.id) if turma else []
    alunos = Aluno.objects.filter(matricula__turma=turma, situacao='ATIVO').distinct() if turma else []
    return render(request, 'presencas/registrar_presenca_convocados.html', {
        'atividades': atividades,
        'alunos': alunos,
    })

@login_required
@require_POST
@csrf_exempt
def registrar_presenca_convocados_ajax(request):
    turma_id = request.session.get('presenca_turma_id')
    turma = Turma.objects.get(id=turma_id) if turma_id else None
    atividades = AtividadeAcademica.objects.filter(turmas__id=turma.id) if turma else []
    convocados_dict = {}
    for atividade in atividades:
        if atividade.convocacao:
            convocados = request.POST.getlist(f'convocados_{atividade.id}')
            convocados_dict[str(atividade.id)] = [int(aid) for aid in convocados]
    request.session['presenca_convocados'] = convocados_dict
    return JsonResponse({'success': True, 'redirect_url': '/presencas/registrar-presenca/alunos/'})