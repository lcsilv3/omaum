from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from importlib import import_module
import logging
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def get_models():
    """Obtém os modelos FrequenciaMensal e Carencia."""
    frequencias_module = import_module("frequencias.models")
    FrequenciaMensal = getattr(frequencias_module, "FrequenciaMensal")
    Carencia = getattr(frequencias_module, "Carencia")
    return FrequenciaMensal, Carencia


def get_forms():
    """Obtém os formulários relacionados a frequências."""
    frequencias_forms = import_module("frequencias.forms")
    return (
        getattr(frequencias_forms, "FrequenciaMensalForm"),
        getattr(frequencias_forms, "FiltroPainelFrequenciasForm"),
    )


def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)


@login_required
def dashboard(request):
    """Exibe um dashboard com estatísticas de frequência."""
    try:
        FrequenciaMensal, Carencia = get_models()

        # Obter parâmetros de filtro
        periodo = request.GET.get("periodo")
        curso_id = request.GET.get("curso")
        turma_id = request.GET.get("turma")

        # Construir query base
        frequencias = FrequenciaMensal.objects.all().select_related("turma")
        carencias = Carencia.objects.all().select_related("frequencia_mensal", "aluno")

        # Aplicar filtros
        if periodo:
            ano, mes = periodo.split("-")
            frequencias = frequencias.filter(ano=ano, mes=mes)
            carencias = carencias.filter(
                frequencia_mensal__ano=ano, frequencia_mensal__mes=mes
            )

        if curso_id:
            frequencias = frequencias.filter(turma__curso_id=curso_id)
            carencias = carencias.filter(frequencia_mensal__turma__curso_id=curso_id)

        if turma_id:
            frequencias = frequencias.filter(turma__id=turma_id)
            carencias = carencias.filter(frequencia_mensal__turma__id=turma_id)

        # Calcular estatísticas
        total_alunos = carencias.values("aluno").distinct().count()
        alunos_regulares = (
            carencias.filter(percentual_presenca__gte=75)
            .values("aluno")
            .distinct()
            .count()
        )
        alunos_carencia = (
            carencias.filter(percentual_presenca__lt=75)
            .values("aluno")
            .distinct()
            .count()
        )

        # Calcular média de frequência
        from django.db.models import Avg

        media_frequencia = (
            carencias.aggregate(Avg("percentual_presenca"))["percentual_presenca__avg"]
            or 0
        )

        # Obter turmas com menor frequência
        turmas_menor_frequencia = []
        turmas_ids = frequencias.values_list("turma__id", flat=True).distinct()

        for turma_id in turmas_ids:
            carencias_turma = carencias.filter(frequencia_mensal__turma__id=turma_id)
            if carencias_turma.exists():
                media_turma = (
                    carencias_turma.aggregate(Avg("percentual_presenca"))[
                        "percentual_presenca__avg"
                    ]
                    or 0
                )
                alunos_carencia_turma = carencias_turma.filter(
                    percentual_presenca__lt=75
                ).count()
                total_alunos_turma = carencias_turma.count()

                # Obter informações da turma
                turma = get_turma_model().objects.get(id=turma_id)

                # Obter período (mês/ano) da frequência mais recente
                ultima_frequencia = (
                    frequencias.filter(turma__id=turma_id)
                    .order_by("-ano", "-mes")
                    .first()
                )

                turmas_menor_frequencia.append(
                    {
                        "id": turma_id,
                        "nome": turma.nome,
                        "curso": turma.curso,
                        "media_frequencia": media_turma,
                        "alunos_carencia": alunos_carencia_turma,
                        "total_alunos": total_alunos_turma,
                        "periodo_mes": ultima_frequencia.get_mes_display()
                        if ultima_frequencia
                        else "",
                        "periodo_ano": ultima_frequencia.ano
                        if ultima_frequencia
                        else "",
                    }
                )

        # Ordenar turmas por média de frequência (ascendente)
        turmas_menor_frequencia.sort(key=lambda x: x["media_frequencia"])

        # Limitar a 5 turmas
        turmas_menor_frequencia = turmas_menor_frequencia[:5]

        # Obter alunos com menor frequência
        alunos_menor_frequencia = []
        alunos_ids = (
            carencias.filter(percentual_presenca__lt=75)
            .values_list("aluno__cpf", flat=True)
            .distinct()
        )

        for aluno_id in alunos_ids:
            carencia_aluno = (
                carencias.filter(aluno__cpf=aluno_id)
                .order_by("percentual_presenca")
                .first()
            )
            if carencia_aluno:
                alunos_menor_frequencia.append(
                    {
                        "cpf": aluno_id,
                        "nome": carencia_aluno.aluno.nome,
                        "email": carencia_aluno.aluno.email,
                        "foto": carencia_aluno.aluno.foto.url
                        if carencia_aluno.aluno.foto
                        else None,
                        "turma": carencia_aluno.frequencia_mensal.turma.nome,
                        "curso": carencia_aluno.frequencia_mensal.turma.curso.nome,
                        "percentual_presenca": carencia_aluno.percentual_presenca,
                        "periodo_mes": carencia_aluno.frequencia_mensal.get_mes_display(),
                        "periodo_ano": carencia_aluno.frequencia_mensal.ano,
                        "carencia_id": carencia_aluno.id,
                        "status_carencia": carencia_aluno.status
                        if hasattr(carencia_aluno, "status")
                        else "PENDENTE",
                    }
                )

        # Ordenar alunos por percentual de presença (ascendente)
        alunos_menor_frequencia.sort(key=lambda x: x["percentual_presenca"])

        # Limitar a 10 alunos
        alunos_menor_frequencia = alunos_menor_frequencia[:10]

        # Dados para gráficos
        # 1. Frequência por curso
        cursos_labels = []
        frequencia_por_curso = []

        Curso = get_model_dynamically("cursos", "Curso")
        cursos = Curso.objects.all()

        for curso in cursos:
            carencias_curso = carencias.filter(frequencia_mensal__turma__curso=curso)
            if carencias_curso.exists():
                media_curso = (
                    carencias_curso.aggregate(Avg("percentual_presenca"))[
                        "percentual_presenca__avg"
                    ]
                    or 0
                )
                cursos_labels.append(curso.nome)
                frequencia_por_curso.append(float(media_curso))

        # 2. Evolução da frequência por período
        periodos_labels = []
        evolucao_frequencia = []

        # Obter últimos 6 meses
        hoje = datetime.now()
        for i in range(5, -1, -1):
            data = hoje - timedelta(days=30 * i)
            mes = data.month
            ano = data.year

            # Obter frequências do mês
            carencias_periodo = carencias.filter(
                frequencia_mensal__mes=mes, frequencia_mensal__ano=ano
            )
            if carencias_periodo.exists():
                media_periodo = (
                    carencias_periodo.aggregate(Avg("percentual_presenca"))[
                        "percentual_presenca__avg"
                    ]
                    or 0
                )
                mes_nome = dict(FrequenciaMensal.MES_CHOICES).get(mes)
                periodos_labels.append(f"{mes_nome}/{ano}")
                evolucao_frequencia.append(float(media_periodo))
            else:
                mes_nome = dict(FrequenciaMensal.MES_CHOICES).get(mes)
                periodos_labels.append(f"{mes_nome}/{ano}")
                evolucao_frequencia.append(0)

        # Obter dados para filtros
        anos = (
            FrequenciaMensal.objects.values_list("ano", flat=True)
            .distinct()
            .order_by("-ano")
        )
        meses = FrequenciaMensal.MES_CHOICES

        # Obter contagem por status
        status_counts = {}
        for status, _ in getattr(FrequenciaMensal, "STATUS_CHOICES", []):
            count = FrequenciaMensal.objects.filter(status=status).count()
            status_counts[status] = count

        # Obter contagem por tipo
        academicas_por_tipo = {}
        for tipo, _ in getattr(FrequenciaMensal, "TIPO_CHOICES", []):
            count = FrequenciaMensal.objects.filter(tipo_atividade=tipo).count()
            academicas_por_tipo[tipo] = count

        context = {
            "estatisticas": {
                "total_alunos": total_alunos,
                "alunos_regulares": alunos_regulares,
                "alunos_carencia": alunos_carencia,
                "media_frequencia": media_frequencia,
            },
            "turmas_menor_frequencia": turmas_menor_frequencia,
            "alunos_menor_frequencia": alunos_menor_frequencia,
            "cursos_labels": json.dumps(cursos_labels),
            "frequencia_por_curso": json.dumps(frequencia_por_curso),
            "periodos_labels": json.dumps(periodos_labels),
            "evolucao_frequencia": json.dumps(evolucao_frequencia),
            "filtros": {"periodo": periodo, "curso": curso_id, "turma": turma_id},
            "anos": anos,
            "meses": meses,
            "cursos": cursos,
            "turmas": get_turma_model().objects.filter(status="A"),
            "status_counts": status_counts,
            "academicas_por_tipo": academicas_por_tipo,
        }

        return render(request, "frequencias/dashboard.html", context)

    except Exception as e:
        logger.error(f"Erro ao exibir dashboard: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao exibir dashboard: {str(e)}")
        return redirect("frequencias:listar_frequencias")


@login_required
def painel_frequencias(request):
    """Exibe um painel de frequências para uma turma."""
    try:
        _, FiltroPainelFrequenciasForm = get_forms()

        if request.method == "POST":
            form = FiltroPainelFrequenciasForm(request.POST)
            if form.is_valid():
                # Redirecionar para a página do painel com os parâmetros
                return redirect(
                    "frequencias:visualizar_painel_frequencias",
                    turma_id=form.cleaned_data["turma"].id,
                    mes_inicio=form.cleaned_data["mes_inicio"],
                    ano_inicio=form.cleaned_data["ano_inicio"],
                    mes_fim=form.cleaned_data["mes_fim"],
                    ano_fim=form.cleaned_data["ano_fim"],
                )
        else:
            form = FiltroPainelFrequenciasForm()

        context = {"form": form}

        return render(request, "frequencias/painel_frequencias_form.html", context)

    except Exception as e:
        logger.error(f"Erro ao acessar painel de frequências: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao acessar painel de frequências: {str(e)}")
        return redirect("frequencias:listar_frequencias")


@login_required
def visualizar_painel_frequencias(
    request, turma_id, mes_inicio, ano_inicio, mes_fim, ano_fim
):
    """Visualiza o painel de frequências para uma turma em um período."""
    try:
        FrequenciaMensal, _ = get_models()
        Turma = get_turma_model()

        # Obter turma
        turma = get_object_or_404(Turma, id=turma_id)

        # Converter parâmetros para inteiros
        mes_inicio = int(mes_inicio)
        ano_inicio = int(ano_inicio)
        mes_fim = int(mes_fim)
        ano_fim = int(ano_fim)

        # Calcular período em meses
        data_inicio = ano_inicio * 12 + mes_inicio
        data_fim = ano_fim * 12 + mes_fim

        # Obter frequências no período
        frequencias = FrequenciaMensal.objects.filter(turma=turma).prefetch_related(
            "turmas"
        )

        # Filtrar pelo período
        frequencias_filtradas = [
            f for f in frequencias if data_inicio <= (f.ano * 12 + f.mes) <= data_fim
        ]

        # Ordenar por ano e mês
        frequencias_filtradas.sort(key=lambda x: (x.ano, x.mes))

        context = {
            "turma": turma,
            "mes_inicio": mes_inicio,
            "ano_inicio": ano_inicio,
            "mes_fim": mes_fim,
            "ano_fim": ano_fim,
            "frequencias": frequencias_filtradas,
        }

        return render(
            request, "frequencias/visualizar_painel_frequencias.html", context
        )

    except Exception as e:
        logger.error(
            f"Erro ao visualizar painel de frequências: {str(e)}", exc_info=True
        )
        messages.error(request, f"Erro ao visualizar painel de frequências: {str(e)}")
        return redirect("frequencias:painel_frequencias")
