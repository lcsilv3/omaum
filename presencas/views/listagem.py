"""
Views para listagem e visualização de presenças.
Consolidado de views_main.py com otimizações de cache e paginação.
"""

import logging
from importlib import import_module

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import F

from presencas.models import RegistroPresenca
from alunos.services import (
    listar_alunos as listar_alunos_service,
    buscar_aluno_por_cpf as buscar_aluno_por_cpf_service,
)


def _get_model(app_name: str, model_name: str):
    """Importa modelo dinamicamente para evitar circularidade."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)


Atividade = _get_model("atividades", "Atividade")
Turma = _get_model("turmas", "Turma")
Curso = _get_model("cursos", "Curso")

logger = logging.getLogger(__name__)


@login_required
def listar_presencas_academicas(request):
    """
    Lista presenças com filtros, paginação e cache.
    
    Parâmetros GET:
    - aluno: CPF ou ID do aluno
    - turma: ID da turma
    - atividade: ID da atividade
    - data_inicio: Data inicial (YYYY-MM-DD)
    - data_fim: Data final (YYYY-MM-DD)
    """
    aluno_id = request.GET.get("aluno", "")
    turma_id = request.GET.get("turma", "")
    atividade_id = request.GET.get("atividade", "")
    data_inicio = request.GET.get("data_inicio", "")
    data_fim = request.GET.get("data_fim", "")

    # Cache para queries de filtros complexos
    cache_key = f"presencas_filtros_{aluno_id}_{turma_id}_{atividade_id}_{data_inicio}_{data_fim}"
    cached_result = cache.get(cache_key)

    if cached_result:
        presencas_qs, total_count = cached_result
        logger.debug(f"Cache hit para presencas: {cache_key}")
    else:
        # Query otimizada com relacionamentos e agregações
        presencas_qs = (
            RegistroPresenca.objects.select_related(
                "aluno", "turma__curso", "atividade"
            )
            .prefetch_related("aluno__historico")
            .annotate(
                turma_nome=F("turma__nome"),
                curso_nome=F("turma__curso__nome"),
                aluno_nome=F("aluno__nome"),
            )
        )

        if aluno_id:
            presencas_qs = presencas_qs.filter(aluno__cpf=aluno_id)
        if turma_id:
            presencas_qs = presencas_qs.filter(turma__id=turma_id)
        if atividade_id:
            presencas_qs = presencas_qs.filter(atividade__id=atividade_id)
        if data_inicio:
            presencas_qs = presencas_qs.filter(data__gte=data_inicio)
        if data_fim:
            presencas_qs = presencas_qs.filter(data__lte=data_fim)

        # Ordenação consistente com índices
        presencas_qs = presencas_qs.order_by("-data", "aluno__nome")

        # Cache do queryset base
        total_count = presencas_qs.count()
        cache.set(cache_key, (presencas_qs, total_count), 300)  # 5 minutos
        logger.debug(f"Cache set para presencas: {cache_key}")

    # Paginação eficiente
    paginator = Paginator(presencas_qs, 25)  # 25 itens por página
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    try:
        alunos_queryset = listar_alunos_service()
        alunos = list(alunos_queryset) if alunos_queryset else []
    except Exception as e:
        logger.error(f"Erro ao listar alunos: {str(e)}")
        alunos = []

    # Carregamento otimizado de listas de referência com cache
    turmas_cache_key = "turmas_listagem"
    atividades_cache_key = "atividades_listagem"
    cursos_cache_key = "cursos_listagem"

    cursos = cache.get(cursos_cache_key)
    if not cursos:
        cursos = list(Curso.objects.only("id", "nome").order_by("nome"))
        cache.set(cursos_cache_key, cursos, 600)  # 10 minutos

    turmas = cache.get(turmas_cache_key)
    if not turmas:
        turmas = list(
            Turma.objects.select_related("curso").only("id", "nome", "curso__nome")
        )
        cache.set(turmas_cache_key, turmas, 600)  # 10 minutos

    atividades = cache.get(atividades_cache_key)
    if not atividades:
        atividades = list(Atividade.objects.only("id", "nome", "tipo_atividade"))
        cache.set(atividades_cache_key, atividades, 600)  # 10 minutos

    context = {
        "page_obj": page_obj,
        "presencas": page_obj.object_list,
        "total_count": total_count,
        "alunos": alunos,
        "cursos": cursos,
        "turmas": turmas,
        "atividades": atividades,
        "filtros": {
            "aluno": aluno_id,
            "turma": turma_id,
            "atividade": atividade_id,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
        },
    }
    return render(
        request, "presencas/academicas/listar_presencas_academicas.html", context
    )


@login_required
def registrar_presenca_academica(request):
    """Registro simples de presença via formulário."""
    if request.method == "POST":
        aluno_id = request.POST.get("aluno")
        turma_id = request.POST.get("turma")
        atividade_id = request.POST.get("atividade")
        data = request.POST.get("data")
        presente = request.POST.get("presente") == "on"
        status = "P" if presente else "F"

        try:
            aluno = buscar_aluno_por_cpf_service(aluno_id)
            turma = get_object_or_404(Turma, id=turma_id)
            atividade = get_object_or_404(Atividade, id=atividade_id)
            
            if not aluno:
                messages.error(request, f"Aluno com CPF {aluno_id} não encontrado.")
                return redirect("presencas:listar_presencas_academicas")

            presenca, created = RegistroPresenca.objects.get_or_create(
                aluno=aluno,
                turma=turma,
                atividade=atividade,
                data=data,
                defaults={
                    "status": status,
                    "registrado_por": request.user.username,
                    "data_registro": timezone.now(),
                },
            )
            
            if not created:
                presenca.status = status
                presenca.registrado_por = request.user.username
                presenca.data_registro = timezone.now()
                
            presenca.save()
            messages.success(request, "Presença registrada com sucesso!")
            return redirect("presencas:listar_presencas_academicas")
            
        except (Turma.DoesNotExist, Atividade.DoesNotExist) as e:
            messages.error(request, f"Dados inválidos: {str(e)}")
            return redirect("presencas:listar_presencas_academicas")
        except Exception as e:
            logger.error(f"Erro ao registrar presença: {str(e)}")
            messages.error(request, f"Erro ao registrar presença: {str(e)}")
            return redirect("presencas:listar_presencas_academicas")

    try:
        alunos_queryset = listar_alunos_service()
        alunos = list(alunos_queryset) if alunos_queryset else []
    except Exception as e:
        logger.error(f"Erro ao listar alunos: {str(e)}")
        alunos = []

    turmas = Turma.objects.select_related("curso").only("id", "nome", "curso__nome")
    atividades = Atividade.objects.only("id", "nome", "tipo_atividade")

    context = {
        "alunos": alunos,
        "turmas": turmas,
        "atividades": atividades,
        "data_hoje": timezone.now().date(),
    }
    return render(
        request, "presencas/academicas/registrar_presenca_academica.html", context
    )


@login_required
def editar_presenca_academica(request, pk):
    """Edição de presença individual."""
    presenca = get_object_or_404(RegistroPresenca, pk=pk)

    if request.method == "POST":
        presente = request.POST.get("presente") == "on"
        presenca.status = "P" if presente else "F"
        presenca.save()

        messages.success(request, "Presença atualizada com sucesso!")
        return redirect("presencas:listar_presencas_academicas")

    context = {"presenca": presenca, "data_hoje": timezone.now().date()}
    return render(
        request, "presencas/academicas/editar_presenca_academica.html", context
    )


@login_required
def excluir_presenca_academica(request, pk):
    """Exclusão de presença individual."""
    presenca = get_object_or_404(RegistroPresenca, pk=pk)

    if request.method == "POST":
        presenca.delete()
        messages.success(request, "Presença excluída com sucesso!")
        return redirect("presencas:listar_presencas_academicas")

    context = {"presenca": presenca}
    return render(
        request, "presencas/academicas/excluir_presenca_academica.html", context
    )


@login_required
def detalhar_presenca_academica(request, pk):
    """Visualização detalhada de uma presença."""
    presenca = get_object_or_404(RegistroPresenca, pk=pk)
    context = {"presenca": presenca}
    return render(
        request, "presencas/academicas/detalhar_presenca_academica.html", context
    )


# Helpers para fluxos indisponíveis (em desenvolvimento)

def _redirect_fluxo_indisponivel(request, mensagem):
    """Redireciona com mensagem informativa."""
    messages.info(request, mensagem)
    return redirect("presencas:listar_presencas_academicas")


def _json_fluxo_indisponivel():
    """Retorna erro JSON para fluxos indisponíveis."""
    return JsonResponse(
        {
            "success": False,
            "message": "Fluxo avançado em atualização. Use o formulário rápido.",
        },
        status=501,
    )


@login_required
def registrar_presenca_dados_basicos(request):
    """Placeholder: registro guiado (Em desenvolvimento)."""
    return _redirect_fluxo_indisponivel(
        request,
        "Fluxo guiado de registro está em atualização.",
    )


@login_required
def registrar_presenca_dados_basicos_ajax(request):
    """Placeholder AJAX: registro guiado (Em desenvolvimento)."""
    return _json_fluxo_indisponivel()


@login_required
def registrar_presenca_totais_atividades(request):
    """Placeholder: totalização de atividades (Em desenvolvimento)."""
    return registrar_presenca_dados_basicos(request)


@login_required
def registrar_presenca_totais_atividades_ajax(request):
    """Placeholder AJAX: totalização (Em desenvolvimento)."""
    return _json_fluxo_indisponivel()


@login_required
def registrar_presenca_dias_atividades(request):
    """Placeholder: registro por dias (Em desenvolvimento)."""
    return registrar_presenca_dados_basicos(request)


@login_required
def registrar_presenca_dias_atividades_ajax(request):
    """Placeholder AJAX: registro por dias (Em desenvolvimento)."""
    return _json_fluxo_indisponivel()


@login_required
def registrar_presenca_alunos(request):
    """Placeholder: seleção de alunos (Em desenvolvimento)."""
    return registrar_presenca_dados_basicos(request)


@login_required
def registrar_presenca_alunos_ajax(request):
    """Placeholder AJAX: seleção de alunos (Em desenvolvimento)."""
    return _json_fluxo_indisponivel()


@login_required
def registrar_presenca_confirmar(request):
    """Placeholder: confirmação (Em desenvolvimento)."""
    return registrar_presenca_dados_basicos(request)


@login_required
def registrar_presenca_confirmar_ajax(request):
    """Placeholder AJAX: confirmação (Em desenvolvimento)."""
    return _json_fluxo_indisponivel()


@login_required
def registrar_presenca_convocados(request):
    """Placeholder: registro de convocados (Em desenvolvimento)."""
    return registrar_presenca_dados_basicos(request)


@login_required
def registrar_presenca_convocados_ajax(request):
    """Placeholder AJAX: convocados (Em desenvolvimento)."""
    return _json_fluxo_indisponivel()


@login_required
def toggle_convocacao_ajax(request):
    """Placeholder AJAX: toggle de convocação (Em desenvolvimento)."""
    return _json_fluxo_indisponivel()


@login_required
def editar_presencas_lote(request):
    """Placeholder: edição em lote (Em desenvolvimento)."""
    return _redirect_fluxo_indisponivel(
        request,
        "Edição em lote está em atualização.",
    )


@login_required
def editar_lote_dados_basicos(request):
    """Placeholder: dados básicos lote (Em desenvolvimento)."""
    return editar_presencas_lote(request)


@login_required
def editar_lote_totais_atividades(request):
    """Placeholder: totais lote (Em desenvolvimento)."""
    return editar_presencas_lote(request)


@login_required
def editar_lote_dias_atividades(request):
    """Placeholder: dias lote (Em desenvolvimento)."""
    return editar_presencas_lote(request)


@login_required
def editar_lote_dias_atividades_ajax(request):
    """Placeholder AJAX: dias lote (Em desenvolvimento)."""
    return _json_fluxo_indisponivel()


@login_required
def editar_presenca_dados_basicos(request, pk):
    """Placeholder: edição individual guiada (Em desenvolvimento)."""
    return _redirect_fluxo_indisponivel(
        request,
        "Edição guiada está em atualização.",
    )


@login_required
def editar_presenca_totais_atividades(request, pk):
    """Placeholder: totalização individual (Em desenvolvimento)."""
    return editar_presenca_dados_basicos(request, pk)


@login_required
def editar_presenca_dias_atividades(request, pk):
    """Placeholder: dias individual (Em desenvolvimento)."""
    return editar_presenca_dados_basicos(request, pk)


@login_required
def editar_presenca_alunos(request, pk):
    """Placeholder: edição de alunos individual (Em desenvolvimento)."""
    return editar_presenca_dados_basicos(request, pk)


@login_required
def detalhar_presenca_dados_basicos(request, pk):
    """Placeholder: detalhamento guiado (Em desenvolvimento)."""
    return _redirect_fluxo_indisponivel(
        request,
        "Detalhamento guiado está em atualização.",
    )


@login_required
def detalhar_presenca_totais_atividades(request, pk):
    """Placeholder: totalização detalhes (Em desenvolvimento)."""
    return detalhar_presenca_dados_basicos(request, pk)


@login_required
def detalhar_presenca_dias_atividades(request, pk):
    """Placeholder: dias detalhes (Em desenvolvimento)."""
    return detalhar_presenca_dados_basicos(request, pk)


@login_required
def detalhar_presenca_alunos(request, pk):
    """Placeholder: alunos detalhes (Em desenvolvimento)."""
    return detalhar_presenca_dados_basicos(request, pk)


@login_required
def exportar_presencas_academicas(request):
    """Placeholder: função de exportação em desenvolvimento."""
    return HttpResponse("Função de exportação em desenvolvimento - usar relatórios")


@login_required
def importar_presencas_academicas(request):
    """Placeholder: função de importação em desenvolvimento."""
    return HttpResponse("Função de importação em desenvolvimento")


@login_required
def listar_observacoes_presenca(request):
    """Placeholder: observações migradas para fluxo unificado."""
    messages.info(
        request,
        "O histórico de observações está em atualização.",
    )
    return redirect("presencas:listar_presencas_academicas")


