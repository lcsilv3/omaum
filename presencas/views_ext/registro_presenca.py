from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db import transaction
from datetime import date
from presencas.forms import DadosBasicosPresencaForm, TotaisAtividadesPresencaForm, AlunosPresencaForm
from importlib import import_module
from cursos.models import Curso
from turmas.models import Turma
from atividades.models import AtividadeAcademica
from presencas.models import TotalAtividadeMes, ObservacaoPresenca
from calendar import monthrange
from alunos.models import Aluno
import logging
logger = logging.getLogger(__name__)

def get_turma_model():
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

@login_required
def registrar_presenca_dados_basicos(request):
    hoje = date.today()
    ano_corrente = hoje.year
    mes_corrente = hoje.month

    form = DadosBasicosPresencaForm(initial={'ano': ano_corrente, 'mes': mes_corrente})

    return render(request, 'presencas/registrar_presenca_dados_basicos.html', {
        'form': form,
        'ano_corrente': ano_corrente,
        'mes_corrente': mes_corrente,
    })

@login_required
@require_POST
def registrar_presenca_dados_basicos_ajax(request):
    form = DadosBasicosPresencaForm(request.POST)
    if form.is_valid():
        request.session['presenca_turma_id'] = form.cleaned_data['turma'].id
        request.session['presenca_ano'] = form.cleaned_data['ano']
        request.session['presenca_mes'] = form.cleaned_data['mes']
        return JsonResponse({'success': True, 'redirect_url': '/presencas/registrar-presenca/totais-atividades/'})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})

@login_required
def registrar_presenca_totais_atividades(request):
    turma_id = request.session.get('presenca_turma_id')
    ano = request.session.get('presenca_ano')
    mes = request.session.get('presenca_mes')
    Turma = get_turma_model()
    turma = Turma.objects.get(id=turma_id) if turma_id else None

    curso = turma.curso if turma else None

    atividades = []
    if turma and curso and ano and mes:
        totais_atividades = request.session.get('presenca_totais_atividades', {})
        atividades_ids = [int(key.replace('qtd_ativ_', '')) for key in totais_atividades.keys() if int(totais_atividades[key]) > 0]
        atividades = AtividadeAcademica.objects.filter(
            id__in=atividades_ids,
            turmas__id=turma.id,
            # ...outros filtros se houver...
        )

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
            # Redireciona para a etapa de designação dos dias
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
def registrar_presenca_totais_atividades_ajax(request):
    turma_id = request.session.get('presenca_turma_id')
    ano = request.session.get('presenca_ano')
    mes = request.session.get('presenca_mes')
    Turma = get_turma_model()
    turma = Turma.objects.get(id=turma_id) if turma_id else None

    curso = turma.curso if turma else None

    atividades = []
    if turma and curso and ano and mes:
        totais_atividades = request.session.get('presenca_totais_atividades', {})
        atividades_ids = [int(key.replace('qtd_ativ_', '')) for key in totais_atividades.keys() if int(totais_atividades[key]) > 0]
        atividades = AtividadeAcademica.objects.filter(
            id__in=atividades_ids,
            turmas__id=turma.id,
            # ...outros filtros se houver...
        )

    form = TotaisAtividadesPresencaForm(request.POST, atividades=atividades)
    if form.is_valid():
        request.session['presenca_totais_atividades'] = {
            key: value for key, value in form.cleaned_data.items() if key.startswith('qtd_ativ_')
        }
        # Redireciona para a etapa de designação dos dias (AJAX)
        return JsonResponse({'success': True, 'redirect_url': '/presencas/registrar-presenca/dias-atividades/'})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})

@login_required
def registrar_presenca_dias_atividades(request):
    """
    GET: Exibe o formulário para seleção dos dias e observações das atividades.
    POST: Salva no banco os dias e observações selecionados para cada atividade.
    """
    from django.shortcuts import render, redirect
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
            atividades_ids = [
                int(key.replace('qtd_ativ_', ''))
                for key, value in totais_atividades.items()
                if int(value) > 0
            ]
            if atividades_ids:
                atividades = AtividadeAcademica.objects.filter(
                    id__in=atividades_ids,
                    turmas__id=turma.id,
                    data_inicio__year=ano,
                    data_inicio__month=mes
                )
            else:
                atividades = []

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
                atividade_academica__in=atividades
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
                except Exception:
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
    Turma = get_turma_model()
    turma = Turma.objects.get(id=turma_id) if turma_id else None

    form = AlunosPresencaForm(turma=turma)

    return render(request, 'presencas/registrar_presenca_alunos.html', {
        'form': form,
        'turma': turma,
    })

@login_required
@require_POST
def registrar_presenca_alunos_ajax(request):
    turma_id = request.session.get('presenca_turma_id')
    Turma = get_turma_model()
    turma = Turma.objects.get(id=turma_id) if turma_id else None

    form = AlunosPresencaForm(request.POST, turma=turma)
    if form.is_valid():
        request.session['presenca_alunos_presentes'] = list(form.cleaned_data['alunos_presentes'].values_list('id', flat=True))
        return JsonResponse({'success': True, 'redirect_url': '/presencas/registrar-presenca/confirmar/'})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})

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
    atividade_id = request.session.get('presenca_atividade_id')
    alunos_presentes_ids = request.session.get('presenca_alunos_presentes', [])

    Turma = get_turma_model()
    turma = Turma.objects.get(id=turma_id) if turma_id else None

    Atividade = import_module("atividades.models").AtividadeAcademica
    atividade = Atividade.objects.get(id=atividade_id) if atividade_id else None

    alunos_presentes = Aluno.objects.filter(id__in=alunos_presentes_ids)

    return render(request, 'presencas/registrar_presenca_confirmar.html', {
        'turma': turma,
        'ano': ano,
        'mes': mes,
        'atividade': atividade,
        'alunos_presentes': alunos_presentes,
    })

@login_required
@require_POST
@transaction.atomic
def registrar_presenca_confirmar_ajax(request):
    # Exemplo de lógica mínima para não quebrar o fluxo
    # Implemente aqui o salvamento definitivo das presenças, se necessário

    # Limpa sessão (ajuste conforme sua lógica)
    for key in [
        'presenca_turma_id', 'presenca_ano', 'presenca_mes',
        'presenca_atividade_id', 'presenca_alunos_presentes', 'presenca_totais_atividades'
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
    from atividades.models import AtividadeAcademica
    from turmas.models import Turma
    from presencas.models import ObservacaoPresenca

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
                    except Exception as e:
                        logger.exception(f'Erro ao registrar observação para atividade {atividade_id}, dia {dia}: {e}')
                        continue
        return JsonResponse({'success': True, 'redirect_url': '/presencas/registrar-presenca/alunos/', 'message': 'Presenças salvas com sucesso!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erro ao salvar: {str(e)}'})