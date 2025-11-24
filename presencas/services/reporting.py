# c:/omaum/presencas/services/reporting.py
from importlib import import_module
from django.db.models import Sum

# Mapeamento de campos do modelo PresencaDetalhada para permitir ajuste ao schema real
FIELDS = {
    "model_path": "presencas.models",
    "model_name": "PresencaDetalhada",
    "aluno": "aluno",
    "aluno_nome": "aluno__nome",
    "turma": "turma",
    "turma_nome": "turma__nome",
    "atividade": "atividade",
    "periodo": "periodo",  # Campo DateField no modelo (primeiro dia do mês)
    "convocacoes": "convocacoes",
    "presencas": "presencas",
    "faltas": "faltas",
    "voluntario_extra": "voluntario_extra",  # V1
    "voluntario_simples": "voluntario_simples",  # V2
    "carencias": "carencias",
}

LIMITE_PERCENTUAL = 70  # Limite % exibido nas planilhas


def _pd_model():
    """Obtém o modelo PresencaDetalhada dinamicamente."""
    mdl = import_module(FIELDS["model_path"])
    return getattr(mdl, FIELDS["model_name"])


def _safe_pct(p, c):
    """Calcula percentual de forma segura (evita divisão por zero)."""
    try:
        p = p or 0
        c = c or 0
        return round((p / c) * 100, 2) if c > 0 else 0.0
    except Exception:
        return 0.0


def _build_period_filter(mes, ano):
    """Constrói filtro de período baseado no campo periodo (DateField)."""
    from datetime import date

    if mes and ano:
        try:
            mes_int = int(mes)
            ano_int = int(ano)
            if 1 <= mes_int <= 12:
                periodo = date(ano_int, mes_int, 1)
                return {FIELDS["periodo"]: periodo}
        except (ValueError, TypeError):
            pass
    return {}


def get_boletim_aluno(aluno_id, mes, ano, turma_id=None):
    """
    Obtém dados do boletim mensal de um aluno específico.

    Args:
        aluno_id: ID do aluno
        mes: Mês (1-12)
        ano: Ano
        turma_id: ID da turma (opcional)

    Returns:
        dict: Contexto com dados agregados do aluno
    """
    PD = _pd_model()

    # Monta filtros básicos
    filtros = {}
    if aluno_id:
        filtros[FIELDS["aluno"] + "_id"] = aluno_id
    if turma_id:
        filtros[FIELDS["turma"] + "_id"] = turma_id

    # Adiciona filtro de período
    filtros.update(_build_period_filter(mes, ano))

    # Remove filtros vazios
    filtros = {k: v for k, v in filtros.items() if v}

    if not filtros:
        # Retorna dados zerados se não há filtros válidos
        return _get_empty_boletim_context(aluno_id, turma_id, mes, ano)

    # Executa agregação
    agg = PD.objects.filter(**filtros).aggregate(
        convocacoes=Sum(FIELDS["convocacoes"]),
        presencas=Sum(FIELDS["presencas"]),
        faltas=Sum(FIELDS["faltas"]),
        v1=Sum(FIELDS["voluntario_extra"]),
        v2=Sum(FIELDS["voluntario_simples"]),
        carencias=Sum(FIELDS["carencias"]),
    )

    # Extrai valores com fallback para 0
    convocacoes = agg.get("convocacoes") or 0
    presencas = agg.get("presencas") or 0
    faltas = agg.get("faltas") or 0
    v1 = agg.get("v1") or 0
    v2 = agg.get("v2") or 0
    carencias = agg.get("carencias") or 0

    # Calcula métricas derivadas
    pct = _safe_pct(presencas, convocacoes)
    vol = v1 + v2

    contexto = {
        "aluno_id": aluno_id,
        "turma_id": turma_id,
        "mes": mes,
        "ano": ano,
        "dados": {
            "convocacoes": convocacoes,
            "presencas": presencas,
            "faltas": faltas,
            "percentual": pct,
            "v1": v1,
            "v2": v2,
            "vol": vol,
            "carencias": carencias,
            "limite_percentual": LIMITE_PERCENTUAL,
        },
    }
    return contexto


def _get_empty_boletim_context(aluno_id, turma_id, mes, ano):
    """Retorna contexto vazio para boletim sem dados."""
    return {
        "aluno_id": aluno_id,
        "turma_id": turma_id,
        "mes": mes,
        "ano": ano,
        "dados": {
            "convocacoes": 0,
            "presencas": 0,
            "faltas": 0,
            "percentual": 0.0,
            "v1": 0,
            "v2": 0,
            "vol": 0,
            "carencias": 0,
            "limite_percentual": LIMITE_PERCENTUAL,
        },
    }


def csv_boletim_aluno(contexto):
    """
    Formata dados do boletim para exportação CSV.

    Args:
        contexto: Dados do boletim obtidos via get_boletim_aluno

    Returns:
        tuple: (rows, headers, filename)
    """
    dados = contexto["dados"]
    headers = [
        "AlunoID",
        "TurmaID",
        "Mês",
        "Ano",
        "Convocações",
        "Presenças",
        "Faltas",
        "%",
        "V1",
        "V2",
        "Vol",
        "Car",
        "Limite%",
    ]
    row = [
        contexto.get("aluno_id"),
        contexto.get("turma_id"),
        contexto.get("mes"),
        contexto.get("ano"),
        dados["convocacoes"],
        dados["presencas"],
        dados["faltas"],
        dados["percentual"],
        dados["v1"],
        dados["v2"],
        dados["vol"],
        dados["carencias"],
        dados["limite_percentual"],
    ]
    filename = (
        f"boletim_aluno_{contexto.get('aluno_id', 'NA')}_"
        f"{contexto.get('mes', 'NA')}-{contexto.get('ano', 'NA')}.csv"
    )
    return [row], headers, filename


def get_consolidado_turma(turma_id, mes, ano):
    """
    Obtém consolidado de frequência de todos os alunos de uma turma.

    Args:
        turma_id: ID da turma
        mes: Mês (1-12)
        ano: Ano

    Returns:
        dict: Contexto com lista de alunos e suas métricas
    """
    PD = _pd_model()

    # Monta filtros
    filtros = {}
    if turma_id:
        filtros[FIELDS["turma"] + "_id"] = turma_id

    # Adiciona filtro de período
    filtros.update(_build_period_filter(mes, ano))

    # Remove filtros vazios
    filtros = {k: v for k, v in filtros.items() if v}

    if not filtros:
        # Retorna lista vazia se não há filtros válidos
        return {
            "turma_id": turma_id,
            "mes": mes,
            "ano": ano,
            "linhas": [],
        }

    # Executa consulta agregada por aluno
    qs = (
        PD.objects.filter(**filtros)
        .values(
            FIELDS["aluno"] + "_id",
            FIELDS["aluno_nome"],
        )
        .annotate(
            convocacoes=Sum(FIELDS["convocacoes"]),
            presencas=Sum(FIELDS["presencas"]),
            faltas=Sum(FIELDS["faltas"]),
            v1=Sum(FIELDS["voluntario_extra"]),
            v2=Sum(FIELDS["voluntario_simples"]),
            carencias=Sum(FIELDS["carencias"]),
        )
        .order_by(FIELDS["aluno_nome"])
    )

    # Processa resultados
    linhas = []
    for r in qs:
        c = r["convocacoes"] or 0
        p = r["presencas"] or 0
        f = r["faltas"] or 0
        v1 = r["v1"] or 0
        v2 = r["v2"] or 0
        car = r["carencias"] or 0
        pct = _safe_pct(p, c)
        vol = v1 + v2

        linhas.append(
            {
                "aluno_id": r[FIELDS["aluno"] + "_id"],
                "aluno_nome": r[FIELDS["aluno_nome"]],
                "convocacoes": c,
                "presencas": p,
                "faltas": f,
                "percentual": pct,
                "v1": v1,
                "v2": v2,
                "vol": vol,
                "carencias": car,
                "limite_percentual": LIMITE_PERCENTUAL,
            }
        )

    contexto = {
        "turma_id": turma_id,
        "mes": mes,
        "ano": ano,
        "linhas": linhas,
    }
    return contexto


def csv_consolidado_turma(contexto):
    """
    Formata dados do consolidado para exportação CSV.

    Args:
        contexto: Dados do consolidado obtidos via get_consolidado_turma

    Returns:
        tuple: (rows, headers, filename)
    """
    headers = [
        "AlunoID",
        "Aluno",
        "Convocações",
        "Presenças",
        "Faltas",
        "%",
        "V1",
        "V2",
        "Vol",
        "Car",
        "Limite%",
    ]
    rows = []
    for r in contexto["linhas"]:
        rows.append(
            [
                r["aluno_id"],
                r["aluno_nome"],
                r["convocacoes"],
                r["presencas"],
                r["faltas"],
                r["percentual"],
                r["v1"],
                r["v2"],
                r["vol"],
                r["carencias"],
                r["limite_percentual"],
            ]
        )

    filename = (
        f"consolidado_turma_{contexto.get('turma_id', 'NA')}_"
        f"{contexto.get('mes', 'NA')}-{contexto.get('ano', 'NA')}.csv"
    )
    return rows, headers, filename


# ===== CATEGORIA 3: RELATÓRIOS ANALÍTICOS =====


def get_alunos_em_risco(turma_id, mes, ano, nivel_carencia=1):
    """
    Obtém lista de alunos em risco (com carências acima do limite).

    Args:
        turma_id: ID da turma
        mes: Mês (1-12)
        ano: Ano
        nivel_carencia: Número mínimo de carências para considerar "em risco"

    Returns:
        dict: Contexto com lista de alunos em risco
    """
    PD = _pd_model()

    # Monta filtros
    filtros = {}
    if turma_id:
        filtros[FIELDS["turma"] + "_id"] = turma_id

    # Adiciona filtro de período
    filtros.update(_build_period_filter(mes, ano))

    # Remove filtros vazios
    filtros = {k: v for k, v in filtros.items() if v}

    if not filtros:
        return {
            "turma_id": turma_id,
            "mes": mes,
            "ano": ano,
            "nivel_carencia": nivel_carencia,
            "alunos_em_risco": [],
            "total_alunos_risco": 0,
        }

    try:
        nivel_carencia_int = int(nivel_carencia)
    except (ValueError, TypeError):
        nivel_carencia_int = 1

    # Consulta alunos com carências >= nivel_carencia
    qs = (
        PD.objects.filter(**filtros)
        .values(
            FIELDS["aluno"] + "_id",
            FIELDS["aluno_nome"],
            FIELDS["turma_nome"],
        )
        .annotate(
            convocacoes=Sum(FIELDS["convocacoes"]),
            presencas=Sum(FIELDS["presencas"]),
            faltas=Sum(FIELDS["faltas"]),
            carencias=Sum(FIELDS["carencias"]),
        )
        .filter(carencias__gte=nivel_carencia_int)
        .order_by("-carencias", FIELDS["aluno_nome"])
    )

    # Processa resultados
    alunos_em_risco = []
    for r in qs:
        c = r["convocacoes"] or 0
        p = r["presencas"] or 0
        f = r["faltas"] or 0
        car = r["carencias"] or 0
        pct = _safe_pct(p, c)

        alunos_em_risco.append(
            {
                "aluno_id": r[FIELDS["aluno"] + "_id"],
                "aluno_nome": r[FIELDS["aluno_nome"]],
                "turma_nome": r[FIELDS["turma_nome"]],
                "convocacoes": c,
                "presencas": p,
                "faltas": f,
                "percentual": pct,
                "carencias": car,
                "limite_percentual": LIMITE_PERCENTUAL,
                "status_risco": "Alto"
                if car >= 3
                else "Médio"
                if car >= 2
                else "Baixo",
            }
        )

    contexto = {
        "turma_id": turma_id,
        "mes": mes,
        "ano": ano,
        "nivel_carencia": nivel_carencia_int,
        "alunos_em_risco": alunos_em_risco,
        "total_alunos_risco": len(alunos_em_risco),
    }
    return contexto


def csv_alunos_em_risco(contexto):
    """Formata dados de alunos em risco para CSV."""
    headers = [
        "AlunoID",
        "Aluno",
        "Turma",
        "Convocações",
        "Presenças",
        "Faltas",
        "%",
        "Carências",
        "Status Risco",
        "Limite%",
    ]
    rows = []
    for r in contexto["alunos_em_risco"]:
        rows.append(
            [
                r["aluno_id"],
                r["aluno_nome"],
                r["turma_nome"],
                r["convocacoes"],
                r["presencas"],
                r["faltas"],
                r["percentual"],
                r["carencias"],
                r["status_risco"],
                r["limite_percentual"],
            ]
        )

    filename = (
        f"alunos_em_risco_{contexto.get('turma_id', 'todas')}_"
        f"{contexto.get('mes', 'NA')}-{contexto.get('ano', 'NA')}.csv"
    )
    return rows, headers, filename


def get_ranking_engajamento(turma_id, mes, ano):
    """
    Obtém ranking de alunos por engajamento (atividades voluntárias).
    """
    PD = _pd_model()

    # Monta filtros
    filtros = {}
    if turma_id:
        filtros[FIELDS["turma"] + "_id"] = turma_id

    # Adiciona filtro de período
    filtros.update(_build_period_filter(mes, ano))

    # Remove filtros vazios
    filtros = {k: v for k, v in filtros.items() if v}

    if not filtros:
        return {
            "turma_id": turma_id,
            "mes": mes,
            "ano": ano,
            "ranking": [],
        }

    # Consulta ordenada por total de voluntariado
    qs = (
        PD.objects.filter(**filtros)
        .values(
            FIELDS["aluno"] + "_id",
            FIELDS["aluno_nome"],
            FIELDS["turma_nome"],
        )
        .annotate(
            convocacoes=Sum(FIELDS["convocacoes"]),
            presencas=Sum(FIELDS["presencas"]),
            v1=Sum(FIELDS["voluntario_extra"]),
            v2=Sum(FIELDS["voluntario_simples"]),
            total_voluntario=Sum(FIELDS["voluntario_extra"])
            + Sum(FIELDS["voluntario_simples"]),
        )
        .filter(
            total_voluntario__gt=0  # Apenas alunos com atividades voluntárias
        )
        .order_by("-total_voluntario", "-presencas", FIELDS["aluno_nome"])
    )

    # Processa resultados com posição no ranking
    ranking = []
    posicao = 1
    for r in qs:
        c = r["convocacoes"] or 0
        p = r["presencas"] or 0
        v1 = r["v1"] or 0
        v2 = r["v2"] or 0
        vol_total = r["total_voluntario"] or 0
        pct = _safe_pct(p, c)

        ranking.append(
            {
                "posicao": posicao,
                "aluno_id": r[FIELDS["aluno"] + "_id"],
                "aluno_nome": r[FIELDS["aluno_nome"]],
                "turma_nome": r[FIELDS["turma_nome"]],
                "convocacoes": c,
                "presencas": p,
                "percentual": pct,
                "v1": v1,
                "v2": v2,
                "total_voluntario": vol_total,
                "classificacao": "Excelente"
                if vol_total >= 5
                else "Bom"
                if vol_total >= 3
                else "Regular",
            }
        )
        posicao += 1

    contexto = {
        "turma_id": turma_id,
        "mes": mes,
        "ano": ano,
        "ranking": ranking,
        "total_participantes": len(ranking),
    }
    return contexto


def csv_ranking_engajamento(contexto):
    """Formata dados do ranking para CSV."""
    headers = [
        "Posição",
        "AlunoID",
        "Aluno",
        "Turma",
        "Total Voluntário",
        "V1",
        "V2",
        "Presenças",
        "%",
        "Classificação",
    ]
    rows = []
    for r in contexto["ranking"]:
        rows.append(
            [
                r["posicao"],
                r["aluno_id"],
                r["aluno_nome"],
                r["turma_nome"],
                r["total_voluntario"],
                r["v1"],
                r["v2"],
                r["presencas"],
                r["percentual"],
                r["classificacao"],
            ]
        )

    filename = (
        f"ranking_engajamento_{contexto.get('turma_id', 'todas')}_"
        f"{contexto.get('mes', 'NA')}-{contexto.get('ano', 'NA')}.csv"
    )
    return rows, headers, filename


def get_comparativo_frequencias(turma_id, periodo1, periodo2):
    """Compara frequência entre dois períodos."""
    mes1, ano1 = periodo1
    mes2, ano2 = periodo2

    # Obtém dados dos dois períodos
    dados1 = get_consolidado_turma(turma_id, mes1, ano1)
    dados2 = get_consolidado_turma(turma_id, mes2, ano2)

    # Cria dicionário por aluno para comparação
    periodo1_dict = {r["aluno_id"]: r for r in dados1["linhas"]}
    periodo2_dict = {r["aluno_id"]: r for r in dados2["linhas"]}

    # Monta comparativo
    comparativo = []
    todos_alunos = set(periodo1_dict.keys()) | set(periodo2_dict.keys())

    for aluno_id in todos_alunos:
        p1 = periodo1_dict.get(aluno_id, {})
        p2 = periodo2_dict.get(aluno_id, {})

        pct1 = p1.get("percentual", 0)
        pct2 = p2.get("percentual", 0)
        delta = pct2 - pct1

        comparativo.append(
            {
                "aluno_id": aluno_id,
                "aluno_nome": p1.get("aluno_nome") or p2.get("aluno_nome", "N/A"),
                "periodo1_percentual": pct1,
                "periodo2_percentual": pct2,
                "delta": delta,
                "delta_abs": abs(delta),
                "tendencia": "Melhora"
                if delta > 0
                else "Piora"
                if delta < 0
                else "Estável",
                "periodo1_presencas": p1.get("presencas", 0),
                "periodo2_presencas": p2.get("presencas", 0),
                "periodo1_carencias": p1.get("carencias", 0),
                "periodo2_carencias": p2.get("carencias", 0),
            }
        )

    # Ordena por maior variação (absoluta) primeiro
    comparativo.sort(key=lambda x: x["delta_abs"], reverse=True)

    contexto = {
        "turma_id": turma_id,
        "periodo1": {"mes": mes1, "ano": ano1},
        "periodo2": {"mes": mes2, "ano": ano2},
        "comparativo": comparativo,
        "total_alunos": len(comparativo),
        "melhorias": len([c for c in comparativo if c["delta"] > 0]),
        "pioras": len([c for c in comparativo if c["delta"] < 0]),
        "estaveis": len([c for c in comparativo if c["delta"] == 0]),
    }
    return contexto


def csv_comparativo_frequencias(contexto):
    """Formata dados do comparativo para CSV."""
    headers = [
        "AlunoID",
        "Aluno",
        "Período 1 %",
        "Período 2 %",
        "Variação (Δ)",
        "Tendência",
        "P1 Presenças",
        "P2 Presenças",
        "P1 Carências",
        "P2 Carências",
    ]
    rows = []
    for r in contexto["comparativo"]:
        rows.append(
            [
                r["aluno_id"],
                r["aluno_nome"],
                r["periodo1_percentual"],
                r["periodo2_percentual"],
                r["delta"],
                r["tendencia"],
                r["periodo1_presencas"],
                r["periodo2_presencas"],
                r["periodo1_carencias"],
                r["periodo2_carencias"],
            ]
        )

    p1 = contexto["periodo1"]
    p2 = contexto["periodo2"]
    filename = (
        f"comparativo_frequencia_{contexto.get('turma_id', 'todas')}_"
        f"{p1['mes']}-{p1['ano']}_vs_{p2['mes']}-{p2['ano']}.csv"
    )
    return rows, headers, filename


def get_dashboard_presencas():
    """Obtém dados para o painel executivo."""
    from datetime import date
    from django.db.models import Count

    PD = _pd_model()
    hoje = date.today()

    # KPIs principais
    total_alunos = PD.objects.values(FIELDS["aluno"] + "_id").distinct().count()

    # Taxa de presença geral (último mês)
    filtro_ultimo_mes = _build_period_filter(hoje.month, hoje.year)
    if filtro_ultimo_mes:
        stats_mes = PD.objects.filter(**filtro_ultimo_mes).aggregate(
            total_convocacoes=Sum(FIELDS["convocacoes"]),
            total_presencas=Sum(FIELDS["presencas"]),
            alunos_com_carencia=Count(FIELDS["aluno"] + "_id", distinct=True),
        )

        taxa_geral = _safe_pct(
            stats_mes.get("total_presencas", 0), stats_mes.get("total_convocacoes", 0)
        )
        alunos_risco = stats_mes.get("alunos_com_carencia", 0)
    else:
        taxa_geral = 0
        alunos_risco = 0

    # Top 5 turmas (melhores percentuais)
    top_turmas = []
    if filtro_ultimo_mes:
        turmas_stats = (
            PD.objects.filter(**filtro_ultimo_mes)
            .values(
                FIELDS["turma"] + "_id",
                FIELDS["turma_nome"],
            )
            .annotate(
                total_convocacoes=Sum(FIELDS["convocacoes"]),
                total_presencas=Sum(FIELDS["presencas"]),
            )
            .order_by("-total_presencas")[:5]
        )

        for t in turmas_stats:
            pct = _safe_pct(t["total_presencas"], t["total_convocacoes"])
            top_turmas.append(
                {
                    "turma_id": t[FIELDS["turma"] + "_id"],
                    "turma_nome": t[FIELDS["turma_nome"]],
                    "percentual": pct,
                    "presencas": t["total_presencas"],
                    "convocacoes": t["total_convocacoes"],
                }
            )

    # Evolução mensal (últimos 6 meses)
    evolucao_mensal = []
    for i in range(6):
        mes = hoje.month - i
        ano = hoje.year
        if mes <= 0:
            mes += 12
            ano -= 1

        filtro_mes = _build_period_filter(mes, ano)

        if filtro_mes:
            stats = PD.objects.filter(**filtro_mes).aggregate(
                convocacoes=Sum(FIELDS["convocacoes"]),
                presencas=Sum(FIELDS["presencas"]),
            )

            pct = _safe_pct(stats.get("presencas", 0), stats.get("convocacoes", 0))
        else:
            pct = 0

        evolucao_mensal.append(
            {
                "mes": mes,
                "ano": ano,
                "label": f"{mes:02d}/{ano}",
                "percentual": pct,
            }
        )

    evolucao_mensal.reverse()  # Ordem cronológica

    contexto = {
        "kpis": {
            "total_alunos": total_alunos,
            "taxa_presenca_geral": taxa_geral,
            "alunos_em_risco": alunos_risco,
            "limite_percentual": LIMITE_PERCENTUAL,
        },
        "top_turmas": top_turmas,
        "evolucao_mensal": evolucao_mensal,
        "dados_json": {
            "evolucao": evolucao_mensal,
            "turmas": top_turmas,
            "kpis": {
                "total_alunos": total_alunos,
                "taxa_geral": taxa_geral,
                "alunos_risco": alunos_risco,
            },
        },
    }
    return contexto


def csv_dashboard_presencas(contexto):
    """Formata dados do dashboard para CSV."""
    from datetime import date

    headers = ["Métrica", "Valor", "Período"]
    rows = [
        ["Total de Alunos", contexto["kpis"]["total_alunos"], "Geral"],
        [
            "Taxa de Presença Geral (%)",
            contexto["kpis"]["taxa_presenca_geral"],
            "Último Mês",
        ],
        ["Alunos em Risco", contexto["kpis"]["alunos_em_risco"], "Último Mês"],
        [
            "Limite Percentual (%)",
            contexto["kpis"]["limite_percentual"],
            "Configuração",
        ],
    ]

    # Adiciona evolução mensal
    for item in contexto["evolucao_mensal"]:
        rows.append([f"Taxa Presença {item['label']}", item["percentual"], "Mensal"])

    # Adiciona top turmas
    for i, turma in enumerate(contexto["top_turmas"], 1):
        rows.append(
            [f"Top {i} - {turma['turma_nome']}", turma["percentual"], "Último Mês"]
        )

    filename = f"dashboard_presencas_{date.today().strftime('%Y-%m-%d')}.csv"
    return rows, headers, filename
