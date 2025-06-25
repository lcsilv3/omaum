from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from importlib import import_module
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
import logging
from datetime import datetime
from calendar import monthrange
from django.db.models import Q
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

def get_model_academica():
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "PresencaAcademica")

def get_model_ritualistica():
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "PresencaRitualistica")

def get_model_observacao():
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "ObservacaoPresenca")

def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

def get_turma_model():
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

def get_atividade_academica_model():
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "AtividadeAcademica")

def get_atividade_ritualistica_model():
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "AtividadeRitualistica")

@login_required
def listar_presencas_academicas(request):
    Presenca = get_model_academica()
    Aluno = get_aluno_model()
    Turma = get_turma_model()
    Atividade = get_atividade_academica_model()

    aluno_id = request.GET.get('aluno', '')
    turma_id = request.GET.get('turma', '')
    atividade_id = request.GET.get('atividade', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    presencas = Presenca.objects.all().select_related('aluno', 'turma', 'atividade')
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

    alunos = Aluno.objects.all()
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
    # Corrigido o caminho do template:
    return render(request, 'presencas/academicas/listar_presencas_academicas.html', context)

@login_required
def listar_presencas_ritualisticas(request):
    Presenca = get_model_ritualistica()
    Aluno = get_aluno_model()
    Turma = get_turma_model()
    Atividade = get_atividade_ritualistica_model()

    aluno_id = request.GET.get('aluno', '')
    turma_id = request.GET.get('turma', '')
    atividade_id = request.GET.get('atividade', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    presencas = Presenca.objects.all().select_related('aluno', 'turma', 'atividade')
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

    alunos = Aluno.objects.all()
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
    # Corrigido o caminho do template:
    return render(request, 'presencas/ritualisticas/listar_presencas_ritualisticas.html', context)

@login_required
def registrar_presenca_academica(request):
    Presenca = get_model_academica()
    Aluno = get_aluno_model()
    Turma = get_turma_model()
    Atividade = get_atividade_academica_model()

    if request.method == 'POST':
        aluno_id = request.POST.get('aluno')
        turma_id = request.POST.get('turma')
        atividade_id = request.POST.get('atividade')
        data = request.POST.get('data')
        presente = request.POST.get('presente') == 'on'
        observacao = request.POST.get('observacao', '')

        try:
            aluno = Aluno.objects.get(cpf=aluno_id)
            turma = Turma.objects.get(id=turma_id)
            atividade = Atividade.objects.get(id=atividade_id)
            if Presenca.objects.filter(aluno=aluno, turma=turma, atividade=atividade, data=data).exists():
                messages.warning(request, f'Já existe um registro de presença para {aluno.nome} na turma {turma.nome} na data {data}.')
                return redirect('presencas:listar_presencas_academicas')
            presenca = Presenca(
                aluno=aluno,
                turma=turma,
                atividade=atividade,
                data=data,
                presente=presente,
                registrado_por=request.user.username,
                data_registro=timezone.now()
            )
            presenca.save()
            # Salvar observação, se houver
            if observacao:
                ObservacaoPresenca = get_model_observacao()
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
        except Exception as e:
            messages.error(request, f'Erro ao registrar presença: {str(e)}')

    alunos = Aluno.objects.all()
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
def registrar_presenca_ritualistica(request):
    Presenca = get_model_ritualistica()
    Aluno = get_aluno_model()
    Turma = get_turma_model()
    Atividade = get_atividade_ritualistica_model()

    if request.method == 'POST':
        aluno_id = request.POST.get('aluno')
        turma_id = request.POST.get('turma')
        atividade_id = request.POST.get('atividade')
        data = request.POST.get('data')
        presente = request.POST.get('presente') == 'on'
        observacao = request.POST.get('observacao', '')

        try:
            aluno = Aluno.objects.get(cpf=aluno_id)
            turma = Turma.objects.get(id=turma_id)
            atividade = Atividade.objects.get(id=atividade_id)
            if Presenca.objects.filter(aluno=aluno, turma=turma, atividade=atividade, data=data).exists():
                messages.warning(request, f'Já existe um registro de presença para {aluno.nome} na turma {turma.nome} na data {data}.')
                return redirect('presencas:listar_presencas_ritualisticas')
            presenca = Presenca(
                aluno=aluno,
                turma=turma,
                atividade=atividade,
                data=data,
                presente=presente,
                registrado_por=request.user.username,
                data_registro=timezone.now()
            )
            presenca.save()
            # Salvar observação, se houver
            if observacao:
                ObservacaoPresenca = get_model_observacao()
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
        except Exception as e:
            messages.error(request, f'Erro ao registrar presença: {str(e)}')

    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()
    atividades = Atividade.objects.all()
    context = {
        'alunos': alunos,
        'turmas': turmas,
        'atividades': atividades,
        'data_hoje': timezone.now().date()
    }
    return render(request, 'presencas/registrar_presenca_ritualistica.html', context)

@login_required
def editar_presenca_academica(request, pk):
    Presenca = get_model_academica()
    presenca = get_object_or_404(Presenca, pk=pk)
    if request.method == 'POST':
        presenca.presente = request.POST.get('presente') == 'on'
        presenca.data = request.POST.get('data')
        presenca.save()
        messages.success(request, 'Presença acadêmica atualizada com sucesso.')
        return redirect('presencas:listar_presencas_academicas')
    return render(request, 'presencas/editar_presenca_academica.html', {'presenca': presenca})

@login_required
def excluir_presenca_academica(request, pk):
    Presenca = get_model_academica()
    presenca = get_object_or_404(Presenca, pk=pk)
    if request.method == 'POST':
        presenca.delete()
        messages.success(request, 'Presença acadêmica excluída com sucesso.')
        return redirect('presencas:listar_presencas_academicas')
    return render(request, 'presencas/confirmar_exclusao_academica.html', {'presenca': presenca})

@login_required
def detalhar_presenca_academica(request, pk):
    Presenca = get_model_academica()
    presenca = get_object_or_404(Presenca, pk=pk)
    return render(request, 'presencas/detalhar_presenca_academica.html', {'presenca': presenca})

@login_required
def editar_presenca_ritualistica(request, pk):
    Presenca = get_model_ritualistica()
    presenca = get_object_or_404(Presenca, pk=pk)
    if request.method == 'POST':
        presenca.presente = request.POST.get('presente') == 'on'
        presenca.data = request.POST.get('data')
        presenca.save()
        messages.success(request, 'Presença ritualística atualizada com sucesso.')
        return redirect('presencas:listar_presencas_ritualisticas')
    return render(request, 'presencas/editar_presenca_ritualistica.html', {'presenca': presenca})

@login_required
def excluir_presenca_ritualistica(request, pk):
    Presenca = get_model_ritualistica()
    presenca = get_object_or_404(Presenca, pk=pk)
    if request.method == 'POST':
        presenca.delete()
        messages.success(request, 'Presença ritualística excluída com sucesso.')
        return redirect('presencas:listar_presencas_ritualisticas')
    return render(request, 'presencas/confirmar_exclusao_ritualistica.html', {'presenca': presenca})

@login_required
def detalhar_presenca_ritualistica(request, pk):
    Presenca = get_model_ritualistica()
    presenca = get_object_or_404(Presenca, pk=pk)
    return render(request, 'presencas/detalhar_presenca_ritualistica.html', {'presenca': presenca})

# Exemplo para ObservacaoPresenca:
@login_required
def listar_observacoes_presenca(request):
    ObservacaoPresenca = get_model_observacao()
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
    Turma = get_turma_model()
    turma = Turma.objects.get(id=turma_id) if turma_id else None

    curso = turma.curso if turma else None

    atividades = []
    if turma and ano and mes:
        # Calcule o primeiro e último dia do mês selecionado
        from datetime import date
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
    from datetime import date
    from calendar import monthrange
    from atividades.models import AtividadeAcademica
    from turmas.models import Turma
    from presencas.models import ObservacaoPresenca

    if request.method == 'GET':
        turma_id = request.session.get('presenca_turma_id')
        ano = request.session.get('presenca_ano')
        mes = request.session.get('presenca_mes')
        turma = Turma.objects.get(id=turma_id) if turma_id else None

        atividades = []
        if turma and ano and mes:
            totais_atividades = request.session.get('presenca_totais_atividades', {})
            logger.warning(f"DEBUG - presenca_totais_atividades na sessão: {totais_atividades}")
            atividades_ids = [
                int(key.replace('qtd_ativ_', ''))
                for key, value in totais_atividades.items()
                if str(value).isdigit() and int(value) > 0
            ]
            primeiro_dia = date(int(ano), int(mes), 1)
            ultimo_dia = date(int(ano), int(mes), monthrange(int(ano), int(mes))[1])
            if atividades_ids:
                atividades = AtividadeAcademica.objects.filter(
                    id__in=atividades_ids,
                    turmas__id=turma.id
                ).filter(
                    Q(data_inicio__lte=ultimo_dia) &
                    (Q(data_fim__isnull=True) | Q(data_fim__gte=ultimo_dia))
                ).distinct()
            else:
                atividades = []
        qtd_dias = monthrange(int(ano), int(mes))[1]
        dias_do_mes = list(range(1, qtd_dias + 1))

        presencas = {}
        presencas_obs = {}
        if turma and ano and mes and atividades:
            observacoes = ObservacaoPresenca.objects.filter(
                turma=turma,
                data__year=ano,
                data__month=mes,
                atividade_academica__in=atividades
            )
            for obs in observacoes:
                aid = obs.atividade_academica_id
                dia = obs.data.day
                presencas.setdefault(aid, []).append(dia)
                presencas_obs.setdefault(aid, {})[dia] = obs.texto

        # Adiciona qtd_ativ_mes em cada atividade
        totais_atividades = request.session.get('presenca_totais_atividades', {})
        for atividade in atividades:
            key = f'qtd_ativ_{atividade.id}'
            atividade.qtd_ativ_mes = int(totais_atividades.get(key, 0))

        context = {
            'atividades': atividades,
            'dias_do_mes': dias_do_mes,
            'mes': mes,
            'ano': ano,
            'presencas': presencas,
            'presencas_obs': presencas_obs,
        }
        return render(request, 'presencas/registrar_presenca_dias_atividades.html', context)

@login_required
@require_POST
@csrf_exempt  # Se necessário, dependendo do seu setup de CSRF
def registrar_presenca_totais_atividades_ajax(request):
    Turma = get_turma_model()
    turma_id = request.session.get('presenca_turma_id')
    ano = request.session.get('presenca_ano')
    mes = request.session.get('presenca_mes')
    turma = Turma.objects.get(id=turma_id) if turma_id else None

    atividades = []
    if turma and ano and mes:
        from datetime import date
        primeiro_dia = date(int(ano), int(mes), 1)
        ultimo_dia = date(int(ano), int(mes), monthrange(int(ano), int(mes))[1])
        atividades = get_atividade_academica_model().objects.filter(
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

    return render(request, 'presencas/registrar_presenca_totais_atividades.html', {
        'form': form,
        'turma': turma,
        'curso': curso,
        'ano': ano,
        'mes': mes,
        'atividades': atividades,
        'totais_registrados': totais_registrados,
    })