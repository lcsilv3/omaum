"""
Views para edição em lote de presenças.
Implementa o mesmo fluxo do registro de presenças, mas para edição.
IMPORTANTE: Não permite diminuição de dias (apenas manter ou aumentar).
"""

import logging
from datetime import date
from calendar import monthrange
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.apps import apps

from presencas.models import RegistroPresenca
from presencas.repositories.presenca_repo import (
    mapa_presencas_periodo,
    mapa_convocacoes_periodo,
    invalidate_period_cache,
)
from presencas.permissions import PresencaPermissionEngine
# from presencas.forms import TotaisAtividadesPresencaForm  # Mantido como referência se necessário futuramente

logger = logging.getLogger(__name__)


# Função para obter modelos dinamicamente
def get_model_class(model_name):
    """Obtém classe de modelo dinamicamente para evitar imports circulares."""
    if model_name == "Turma":
        return apps.get_model("turmas", model_name)
    elif model_name == "Curso":
        return apps.get_model("cursos", model_name)
    elif model_name == "Atividade":
        return apps.get_model("atividades", model_name)
    elif model_name == "Aluno":
        return apps.get_model("alunos", model_name)
    elif model_name == "Matricula":
        return apps.get_model("matriculas", model_name)
    else:
        return apps.get_model("atividades", model_name)


@login_required
def editar_presencas_lote(request):
    """
    Página inicial de seleção para edição em lote.
    Permite selecionar critérios para carregar um lote de presenças existentes.
    """
    Turma = get_model_class("Turma")
    Curso = get_model_class("Curso")

    # Obter anos e meses únicos onde há presenças registradas
    anos_disponiveis = RegistroPresenca.objects.dates("data", "year").distinct()
    anos = [ano.year for ano in anos_disponiveis]
    anos.sort(reverse=True)

    meses = [
        (1, "Janeiro"),
        (2, "Fevereiro"),
        (3, "Março"),
        (4, "Abril"),
        (5, "Maio"),
        (6, "Junho"),
        (7, "Julho"),
        (8, "Agosto"),
        (9, "Setembro"),
        (10, "Outubro"),
        (11, "Novembro"),
        (12, "Dezembro"),
    ]

    cursos = Curso.objects.filter(ativo=True).order_by("nome")
    turmas = Turma.objects.filter(ativo=True).order_by("curso__nome", "nome")

    if request.method == "POST":
        turma_id = request.POST.get("turma")
        ano = request.POST.get("ano")
        mes = request.POST.get("mes")

        if not all([turma_id, ano, mes]):
            messages.error(request, "Todos os campos são obrigatórios.")
            return redirect("presencas:editar_presencas_lote")

        # Verificar se há presenças no período selecionado
        primeiro_dia = date(int(ano), int(mes), 1)
        ultimo_dia = date(int(ano), int(mes), monthrange(int(ano), int(mes))[1])

        presencas_existentes = RegistroPresenca.objects.filter(
            turma_id=turma_id, data__range=[primeiro_dia, ultimo_dia]
        ).count()

        if presencas_existentes == 0:
            messages.warning(
                request, "Não há presenças registradas para o período selecionado."
            )
            # Manter os parâmetros para facilitar nova pesquisa
            context = {
                "turmas": turmas,
                "cursos": cursos,
                "anos": anos,
                "meses": meses,
                "turma_selecionada": turma_id,
                "ano_selecionado": ano,
                "mes_selecionado": int(mes),
                "breadcrumb": [
                    {"etapa": "Seleção do Período", "ativa": True},
                    {"etapa": "Dados Básicos", "ativa": False},
                    {"etapa": "Totais de Atividades", "ativa": False},
                    {"etapa": "Dias e Edição", "ativa": False},
                ],
                "titulo_pagina": "Edição em Lote - Seleção do Período",
                "descricao_pagina": "Selecione o período das presenças que deseja editar em lote.",
            }
            return render(
                request, "presencas/edicao_lote/selecionar_periodo.html", context
            )

        # Salvar dados na sessão para edição
        request.session["edicao_lote_turma_id"] = turma_id
        request.session["edicao_lote_ano"] = ano
        request.session["edicao_lote_mes"] = mes

        return redirect("presencas:editar_lote_dados_basicos")

    context = {
        "turmas": turmas,
        "cursos": cursos,
        "anos": anos,
        "meses": meses,
        "breadcrumb": [
            {"etapa": "Seleção do Período", "ativa": True},
            {"etapa": "Dados Básicos", "ativa": False},
            {"etapa": "Totais de Atividades", "ativa": False},
            {"etapa": "Dias e Edição", "ativa": False},
        ],
        "titulo_pagina": "Edição em Lote - Seleção do Período",
        "descricao_pagina": "Selecione o período das presenças que deseja editar em lote.",
    }
    return render(request, "presencas/edicao_lote/selecionar_periodo.html", context)


@login_required
def editar_lote_dados_basicos(request):
    """
    Exibe dados básicos do lote selecionado.
    Similar ao registro, mas com dados carregados das presenças existentes.
    """
    turma_id = request.session.get("edicao_lote_turma_id")
    ano = request.session.get("edicao_lote_ano")
    mes = request.session.get("edicao_lote_mes")

    if not all([turma_id, ano, mes]):
        messages.error(
            request, "Dados de seleção não encontrados. Reinicie o processo."
        )
        return redirect("presencas:editar_presencas_lote")

    Turma = get_model_class("Turma")
    turma = get_object_or_404(Turma, id=turma_id)
    curso = turma.curso

    # Carregar estatísticas do período
    primeiro_dia = date(int(ano), int(mes), 1)
    ultimo_dia = date(int(ano), int(mes), monthrange(int(ano), int(mes))[1])

    presencas_periodo = Presenca.objects.filter(
        turma=turma, data__range=[primeiro_dia, ultimo_dia]
    )

    total_presencas = presencas_periodo.count()
    atividades_distintas = presencas_periodo.values("atividade").distinct().count()
    alunos_distintos = presencas_periodo.values("aluno").distinct().count()

    if request.method == "POST":
        # Validar permissões antes de continuar
        permissoes_ok = True
        for presenca in presencas_periodo:
            pode_editar, motivo = PresencaPermissionEngine.pode_alterar_presenca(
                presenca, request.user
            )
            if not pode_editar:
                messages.error(
                    request,
                    f"Sem permissão para editar presença de {presenca.aluno.nome}: {motivo}",
                )
                permissoes_ok = False
                break

        if not permissoes_ok:
            return redirect("presencas:editar_lote_dados_basicos")

        messages.success(
            request, "Dados básicos validados. Prosseguindo para edição..."
        )
        return redirect("presencas:editar_lote_totais_atividades")

    context = {
        "turma": turma,
        "curso": curso,
        "ano": ano,
        "mes": mes,
        "total_presencas": total_presencas,
        "atividades_distintas": atividades_distintas,
        "alunos_distintos": alunos_distintos,
        "presencas_periodo": presencas_periodo[:10],  # Amostra para visualização
        "breadcrumb": [
            {"etapa": "Seleção do Período", "ativa": False},
            {"etapa": "Dados Básicos", "ativa": True},
            {"etapa": "Totais de Atividades", "ativa": False},
            {"etapa": "Dias e Edição", "ativa": False},
        ],
        "titulo_pagina": "Edição em Lote - Dados Básicos",
        "descricao_pagina": "Visualize os dados básicos do período selecionado.",
    }
    return render(request, "presencas/edicao_lote/dados_basicos.html", context)


@login_required
def editar_lote_totais_atividades(request):
    """
    Exibe totais de atividades do período selecionado.
    Permite ajustar totais antes da edição detalhada.
    IMPORTANTE: Apenas permite manter ou aumentar dias, não diminuir.
    """
    turma_id = request.session.get("edicao_lote_turma_id")
    ano = request.session.get("edicao_lote_ano")
    mes = request.session.get("edicao_lote_mes")

    if not all([turma_id, ano, mes]):
        messages.error(
            request, "Dados de seleção não encontrados. Reinicie o processo."
        )
        return redirect("presencas:editar_presencas_lote")

    Turma = get_model_class("Turma")
    Atividade = get_model_class("Atividade")
    turma = get_object_or_404(Turma, id=turma_id)
    curso = turma.curso

    # Carregar atividades e totais atuais
    primeiro_dia = date(int(ano), int(mes), 1)
    ultimo_dia = date(int(ano), int(mes), monthrange(int(ano), int(mes))[1])

    presencas_periodo = Presenca.objects.filter(
        turma=turma, data__range=[primeiro_dia, ultimo_dia]
    )

    # Calcular totais atuais por atividade
    totais_atuais = {}
    atividades_com_presenca = presencas_periodo.values("atividade").distinct()

    for item in atividades_com_presenca:
        atividade_id = item["atividade"]
        total_dias = (
            presencas_periodo.filter(atividade_id=atividade_id)
            .values("data")
            .distinct()
            .count()
        )
        totais_atuais[f"qtd_ativ_{atividade_id}"] = total_dias

    # Obter atividades do período
    atividades = Atividade.objects.filter(
        id__in=[item["atividade"] for item in atividades_com_presenca]
    )

    # Criar lista de atividades com seus totais para facilitar no template
    atividades_com_totais = []
    for atividade in atividades:
        total_atual = totais_atuais.get(f"qtd_ativ_{atividade.id}", 0)
        atividades_com_totais.append(
            {
                "atividade": atividade,
                "total_atual": total_atual,
                "valor_minimo": total_atual,  # Valor mínimo permitido (não pode diminuir)
            }
        )

    if request.method == "POST":
        # Processar alterações nos totais com validação
        novos_totais = {}
        erros_validacao = []

        for key, value in request.POST.items():
            if key.startswith("qtd_ativ_") and value.isdigit():
                novo_valor = int(value)
                valor_atual = totais_atuais.get(key, 0)

                # VALIDAÇÃO: não permitir diminuição de dias
                if novo_valor < valor_atual:
                    atividade_id = key.replace("qtd_ativ_", "")
                    atividade_nome = next(
                        (a.nome for a in atividades if str(a.id) == atividade_id),
                        "Desconhecida",
                    )
                    erros_validacao.append(
                        (
                            f'Atividade "{atividade_nome}": não é possível diminuir '
                            f"de {valor_atual} para {novo_valor} dias. "
                            f"Valor mínimo permitido: {valor_atual} dias. "
                            'Para remover dias, use a funcionalidade "Exclusão em Lote".'
                        )
                    )
                else:
                    novos_totais[key] = novo_valor

        # Se há erros de validação, exibir e não continuar
        if erros_validacao:
            for erro in erros_validacao:
                messages.error(request, erro)

            # Retornar para a mesma tela mantendo os dados
            # Recriar atividades_com_totais com valores mínimos para o template
            atividades_com_totais_erro = []
            for atividade in atividades:
                total_atual = totais_atuais.get(f"qtd_ativ_{atividade.id}", 0)
                atividades_com_totais_erro.append(
                    {
                        "atividade": atividade,
                        "total_atual": total_atual,
                        "valor_minimo": total_atual,
                    }
                )

            context = {
                "turma": turma,
                "curso": curso,
                "ano": ano,
                "mes": mes,
                "atividades": atividades,
                "atividades_com_totais": atividades_com_totais_erro,
                "totais_atuais": totais_atuais,
                "breadcrumb": [
                    {"etapa": "Seleção do Período", "ativa": False},
                    {"etapa": "Dados Básicos", "ativa": False},
                    {"etapa": "Totais de Atividades", "ativa": True},
                    {"etapa": "Dias e Edição", "ativa": False},
                ],
                "titulo_pagina": "Edição em Lote - Totais de Atividades",
                "descricao_pagina": "Ajuste os totais de atividades antes da edição detalhada.",
                "aviso_exclusao": False,  # Não duplicar aviso (já está no messages)
            }
            return render(
                request, "presencas/edicao_lote/totais_atividades.html", context
            )

        # Salvar novos totais na sessão (apenas os válidos)
        request.session["edicao_lote_totais_atividades"] = novos_totais

        # Mensagem de sucesso apropriada
        if novos_totais:
            alteracoes = sum(
                1 for k, v in novos_totais.items() if v != totais_atuais.get(k, 0)
            )
            if alteracoes > 0:
                messages.success(
                    request,
                    (
                        "✅ Configuração atualizada: "
                        f"{alteracoes} atividade(s) terão dias adicionais para seleção."
                    ),
                )
            else:
                messages.success(
                    request,
                    "✅ Configuração confirmada. Prosseguindo para seleção de dias...",
                )
        else:
            messages.success(
                request,
                "✅ Configuração confirmada. Prosseguindo para seleção de dias...",
            )

        return redirect("presencas:editar_lote_dias_atividades")

    context = {
        "turma": turma,
        "curso": curso,
        "ano": ano,
        "mes": mes,
        "atividades": atividades,
        "atividades_com_totais": atividades_com_totais,
        "totais_atuais": totais_atuais,
        "breadcrumb": [
            {"etapa": "Seleção do Período", "ativa": False},
            {"etapa": "Dados Básicos", "ativa": False},
            {"etapa": "Totais de Atividades", "ativa": True},
            {"etapa": "Dias e Edição", "ativa": False},
        ],
        "titulo_pagina": "Edição em Lote - Totais de Atividades",
        "descricao_pagina": "Ajuste os totais de atividades antes da edição detalhada.",
        "aviso_exclusao": False,  # Não mostrar aviso inicialmente
    }
    return render(request, "presencas/edicao_lote/totais_atividades.html", context)


@login_required
def editar_lote_dias_atividades(request):
    """
    Etapa principal - modal com TODAS as presenças do período.
    REUTILIZA o template de registro_presenca_dias_atividades.html
    Carrega presenças EXISTENTES no lugar de inicializar vazias.
    """
    turma_id = request.session.get("edicao_lote_turma_id")
    ano = request.session.get("edicao_lote_ano")
    mes = request.session.get("edicao_lote_mes")

    if not all([turma_id, ano, mes]):
        messages.error(
            request, "Dados de seleção não encontrados. Reinicie o processo."
        )
        return redirect("presencas:editar_presencas_lote")

    Turma = get_model_class("Turma")
    Atividade = get_model_class("Atividade")
    Aluno = get_model_class("Aluno")

    turma = get_object_or_404(Turma, id=turma_id)

    # Carregar dados das presenças existentes (via repositório)

    # Usar repositório para montar estruturas agregadas
    presencas_por_atividade = mapa_presencas_periodo(turma.id, int(ano), int(mes))
    dias_por_atividade = {
        aid: sorted(list(dias.keys())) for aid, dias in presencas_por_atividade.items()
    }
    totais_atividades = request.session.get("edicao_lote_totais_atividades", {})

    # Pré-carregar convocações do período para reduzir queries
    convoc_map = mapa_convocacoes_periodo(turma.id, int(ano), int(mes))
    # Acrescentar campo 'convocado' aos registros existentes
    for atividade_id, dias in presencas_por_atividade.items():
        for dia, alunos in dias.items():
            for cpf, dados in alunos.items():
                dados["convocado"] = convoc_map.get((atividade_id, dia, cpf))

    # Converter sets para listas e calcular estatísticas
    for atividade_id in dias_por_atividade:
        dias_por_atividade[atividade_id] = sorted(
            list(dias_por_atividade[atividade_id])
        )

    # Obter atividades e alunos
    atividades = Atividade.objects.filter(
        id__in=[int(k) for k in presencas_por_atividade.keys()]
    ).order_by("nome")

    # Adicionar estatísticas às atividades
    atividades_com_stats = []
    for atividade in atividades:
        atividade_id = str(atividade.id)
        total_dias_existentes = len(dias_por_atividade.get(atividade_id, []))
        total_presencas = 0
        if atividade_id in presencas_por_atividade:
            for dia, alunos_dia in presencas_por_atividade[atividade_id].items():
                total_presencas += len(alunos_dia)

        # Verificar se há novos totais definidos na sessão
        novo_total_key = f"qtd_ativ_{atividade.id}"
        total_dias_esperados = totais_atividades.get(
            novo_total_key, total_dias_existentes
        )

        # Adicionar atributos dinâmicos
        atividade.total_dias = (
            total_dias_esperados  # Total esperado (pode ser maior que existente)
        )
        atividade.total_dias_existentes = (
            total_dias_existentes  # Dias realmente existentes
        )
        atividade.total_presencas = total_presencas
        atividade.dias_adicionais_necessarios = max(
            0, total_dias_esperados - total_dias_existentes
        )
        atividade.tem_dias_adicionais = total_dias_esperados > total_dias_existentes
        # Adicionar lista de dias existentes para esta atividade específica
        atividade.dias_existentes = dias_por_atividade.get(atividade_id, [])
        atividade.dias_existentes_str = ",".join(map(str, atividade.dias_existentes))
        atividades_com_stats.append(atividade)

    # Obter alunos através das matrículas ativas
    alunos = (
        Aluno.objects.filter(
            matricula__turma=turma, matricula__ativa=True, situacao="a"
        )
        .distinct()
        .order_by("nome")
    )

    if request.method == "POST":
        # Processar finalização da edição
        try:
            messages.success(request, "Presenças editadas com sucesso!")

            # Limpar sessão
            session_keys = [
                "edicao_lote_turma_id",
                "edicao_lote_ano",
                "edicao_lote_mes",
                "edicao_lote_totais_atividades",
            ]
            for key in session_keys:
                if key in request.session:
                    del request.session[key]

            return redirect("presencas:listar_presencas_academicas")

        except Exception as e:
            logger.error(f"Erro ao finalizar edição em lote: {e}")
            messages.error(request, "Erro ao processar edição. Tente novamente.")
            return redirect("presencas:editar_lote_dias_atividades")

    context = {
        "turma": turma,
        "ano": ano,
        "mes": mes,
        "atividades": atividades_com_stats,
        "alunos": alunos,
        "presencas_existentes": presencas_por_atividade,
        "dias_por_atividade": dias_por_atividade,
        "totais_atividades": totais_atividades,
        "modo_edicao": True,  # Sinaliza que é edição, não criação
        "breadcrumb": [
            {"etapa": "Seleção do Período", "ativa": False},
            {"etapa": "Dados Básicos", "ativa": False},
            {"etapa": "Totais de Atividades", "ativa": False},
            {"etapa": "Dias e Edição", "ativa": True},
        ],
        "titulo_pagina": "Edição em Lote - Dias e Presenças",
        "descricao_pagina": "Edite as presenças existentes diretamente no calendário.",
    }
    return render(request, "presencas/edicao_lote/dias_atividades.html", context)


@login_required
@require_POST
@csrf_exempt
def editar_lote_dias_atividades_ajax(request):
    """
    AJAX para salvar alterações em lote.
    REUTILIZA lógica de registrar_presenca_dias_atividades_ajax
    Identifica se é UPDATE ou CREATE para cada presença.
    """
    try:
        import json

        dados = json.loads(request.body)

        turma_id = request.session.get("edicao_lote_turma_id")
        ano = request.session.get("edicao_lote_ano")
        mes = request.session.get("edicao_lote_mes")

        if not all([turma_id, ano, mes]):
            return JsonResponse({"success": False, "erro": "Sessão inválida"})

        Turma = get_model_class("Turma")
        Atividade = get_model_class("Atividade")
        Aluno = get_model_class("Aluno")

        turma = get_object_or_404(Turma, id=turma_id)

        alteracoes_realizadas = 0
        exclusoes_realizadas = 0

        with transaction.atomic():
            # Processar exclusões primeiro
            for atividade_id, dias_exclusoes in dados.get("exclusoes", {}).items():
                atividade = get_object_or_404(Atividade, id=atividade_id)
                for dia, lista_cpfs in dias_exclusoes.items():
                    data_presenca = date(int(ano), int(mes), int(dia))
                    for cpf_aluno in lista_cpfs:
                        aluno = get_object_or_404(Aluno, cpf=cpf_aluno)
                        try:
                            presenca_existente = Presenca.objects.get(
                                turma=turma,
                                atividade=atividade,
                                aluno=aluno,
                                data=data_presenca,
                            )
                            pode_excluir, motivo = (
                                PresencaPermissionEngine.pode_alterar_presenca(
                                    presenca_existente, request.user
                                )
                            )
                            if not pode_excluir:
                                continue
                            presenca_existente.delete()
                            exclusoes_realizadas += 1
                        except Presenca.DoesNotExist:
                            pass
                        # Também remover eventual convocação
                        ConvocacaoPresenca.objects.filter(
                            aluno=aluno,
                            turma=turma,
                            atividade=atividade,
                            data=data_presenca,
                        ).delete()

            # Depois processar criações/atualizações
            for atividade_id, dias_dados in dados.get("presencas", {}).items():
                atividade = get_object_or_404(Atividade, id=atividade_id)

                for dia, alunos_dados in dias_dados.items():
                    data_presenca = date(int(ano), int(mes), int(dia))

                    for cpf_aluno, dados_presenca in alunos_dados.items():
                        aluno = get_object_or_404(Aluno, cpf=cpf_aluno)

                        # Verificar permissões
                        pode_editar = True
                        presenca_existente = None

                        try:
                            presenca_existente = Presenca.objects.get(
                                turma=turma,
                                atividade=atividade,
                                aluno=aluno,
                                data=data_presenca,
                            )
                            pode_editar, motivo = (
                                PresencaPermissionEngine.pode_alterar_presenca(
                                    presenca_existente, request.user
                                )
                            )
                        except Presenca.DoesNotExist:
                            pass

                        if not pode_editar:
                            continue

                        # Atualizar ou criar presença
                        if presenca_existente:
                            # UPDATE
                            presenca_existente.presente = dados_presenca.get(
                                "presente", True
                            )
                            presenca_existente.justificativa = dados_presenca.get(
                                "justificativa", ""
                            )
                            presenca_existente.registrado_por = request.user.username
                            presenca_existente.save()
                        else:
                            # CREATE
                            Presenca.objects.create(
                                turma=turma,
                                atividade=atividade,
                                aluno=aluno,
                                data=data_presenca,
                                presente=dados_presenca.get("presente", True),
                                justificativa=dados_presenca.get("justificativa", ""),
                                registrado_por=request.user.username,
                            )

                        alteracoes_realizadas += 1

                        # Atualizar/guardar convocação se houver campo no payload e se a atividade for de convocação
                        if "convocado" in dados_presenca:
                            try:
                                ConvocacaoPresenca.objects.update_or_create(
                                    aluno=aluno,
                                    turma=turma,
                                    atividade=atividade,
                                    data=data_presenca,
                                    defaults={
                                        "convocado": bool(
                                            dados_presenca.get("convocado")
                                        ),
                                        "registrado_por": request.user.username,
                                    },
                                )
                            except Exception as e:
                                logger.warning(
                                    f"Falha ao atualizar convocação para {aluno.cpf} em {data_presenca}: {e}"
                                )

        # Invalida cache do período afetado
        try:
            invalidate_period_cache(turma.id, int(ano), int(mes))
        except Exception as _:
            # Apenas loga silenciosamente; não deve falhar a resposta
            logger.debug(
                "Falha ao invalidar cache do período após edição em lote", exc_info=True
            )

        return JsonResponse(
            {
                "success": True,
                "message": f"{alteracoes_realizadas} alterações e {exclusoes_realizadas} exclusões realizadas com sucesso!",
                "alteracoes": alteracoes_realizadas,
                "exclusoes": exclusoes_realizadas,
            }
        )

    except Exception as e:
        logger.error(f"Erro ao salvar edição em lote: {e}")
        return JsonResponse({"success": False, "erro": "Erro interno do servidor"})


@csrf_exempt
@require_POST
def excluir_presenca(request):
    turma_id = request.POST.get("turma_id")
    ano = request.POST.get("ano")
    mes = request.POST.get("mes")
    presenca_id = request.POST.get("presenca_id")

    if not all([turma_id, ano, mes, presenca_id]):
        return JsonResponse({"error": "Parâmetros incompletos."}, status=400)

    try:
        presenca = Presenca.objects.get(id=presenca_id)
        presenca.delete()

        # Invalida o cache após exclusão
        invalidate_period_cache(turma_id, int(ano), int(mes))

        return JsonResponse({"success": True})
    except Presenca.DoesNotExist:
        return JsonResponse({"error": "Presença não encontrada."}, status=404)
    except Exception as e:
        logger.error(f"Erro ao excluir presença: {e}")
        return JsonResponse({"error": "Erro interno."}, status=500)
