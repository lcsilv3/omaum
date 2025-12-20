"""
⚠️ ATENÇÃO: Este arquivo está sendo DESCONTINUADO!

As views principais de atividades foram movidas para views_ext/:
- views_ext/academicas.py: CRUD de atividades acadêmicas
- views_ext/relatorios.py: Relatórios de atividades
- views_ext/dashboard.py: Dashboard de atividades
- views_ext/calendario.py: Calendário de atividades

Antes de editar uma view, SEMPRE verifique atividades/urls.py 
para confirmar de onde a view é realmente importada!
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from .views_ext.utils import get_models, get_cursos
import logging

logger = logging.getLogger(__name__)


def relatorio_atividades(request):
    models = get_models()
    AtividadeAcademica = models["AtividadeAcademica"]

    atividades = AtividadeAcademica.objects.prefetch_related("turmas__curso").all()
    curso_id = request.GET.get("curso")
    if curso_id:
        atividades = atividades.filter(turmas__curso_id=curso_id)
    cursos_dict = {}
    for atividade in atividades:
        curso = atividade.curso
        if curso not in cursos_dict:
            cursos_dict[curso] = []
        cursos_dict[curso].append(atividade)
    cursos = get_cursos()
    return render(
        request,
        "atividades/relatorio_atividades.html",
        {
            "atividades": atividades,
            "cursos_dict": cursos_dict,
            "cursos": cursos,
            "curso_id": curso_id,
        },
    )


@login_required
def listar_atividades_academicas(request):
    import sys
    print("=" * 80, flush=True)
    print("🚀🚀🚀 VIEW ATIVIDADES EXECUTANDO!", flush=True)
    print("=" * 80, flush=True)
    sys.stdout.flush()
    sys.stderr.write("🔥 VIEW EXECUTANDO VIA STDERR\n")
    sys.stderr.flush()
    """
    Lista atividades acadêmicas com filtros dinâmicos por curso e turma.
    Suporta AJAX para atualização parcial da tabela e dos selects.
    """
    print("🚀 VIEW ATIVIDADES EXECUTANDO - TIMESTAMP:", __import__('datetime').datetime.now(), flush=True)
    query = request.GET.get("q", "")
    curso_id = request.GET.get("curso", "")
    turma_id = request.GET.get("turma", "")
    models = get_models()
    Curso = models["Curso"]
    Turma = models["Turma"]
    AtividadeAcademica = models["AtividadeAcademica"]

    cursos = Curso.objects.all()
    turmas = Turma.objects.all()
    atividades = AtividadeAcademica.objects.all()

    if query:
        atividades = atividades.filter(nome__icontains=query)
    if curso_id:
        atividades = atividades.filter(curso_id=curso_id)
        turmas = turmas.filter(curso_id=curso_id)
    if turma_id:
        atividades = atividades.filter(turmas__id=turma_id)
        cursos = cursos.filter(
            id__in=Turma.objects.filter(id=turma_id).values_list("curso_id", flat=True)
        )

    atividades = atividades.order_by("nome")

    paginator = Paginator(atividades, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "atividades": page_obj.object_list,
        "page_obj": page_obj,
        "total_atividades": paginator.count,
        "cursos": cursos,
        "turmas": turmas,
        "query": query,
        "curso_selecionado": curso_id,
        "turma_selecionada": turma_id,
    }
    
    # Debug: verificar headers recebidos
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"
    logger.info(f"🔍 [ATIVIDADES] Method: {request.method}, Path: {request.path}")
    logger.info(f"🔍 [ATIVIDADES] Headers recebidos: {dict(request.headers)}")
    logger.info(f"🔍 [ATIVIDADES] X-Requested-With value: '{request.headers.get('x-requested-with')}'")
    logger.info(f"🔍 [ATIVIDADES] is_ajax={is_ajax}")
    
    if is_ajax:
        tabela_html = render_to_string(
            "atividades/academicas/partials/atividades_tabela.html",
            context,
            request=request,
        )
        cursos_html = render_to_string(
            "atividades/academicas/partials/cursos_options.html",
            context,
            request=request,
        )
        turmas_html = render_to_string(
            "atividades/academicas/partials/turmas_options.html",
            context,
            request=request,
        )
        paginacao_html = render_to_string(
            "atividades/academicas/partials/paginacao_atividades.html",
            context,
            request=request,
        )
        rodape_html = render_to_string(
            "atividades/academicas/partials/rodape_atividades.html",
            context,
            request=request,
        )
        return JsonResponse(
            {
                "tabela_html": tabela_html,
                "cursos_html": cursos_html,
                "turmas_html": turmas_html,
                "paginacao_html": paginacao_html,
                "rodape_html": rodape_html,
            }
        )
    return render(
        request, "atividades/academicas/listar_atividades_academicas.html", context
    )


def ajax_atividades_filtradas(request):
    """Filtra atividades via AJAX aplicando busca, curso e turma."""
    models = get_models()
    AtividadeAcademica = models["AtividadeAcademica"]

    query = request.GET.get("q", "")
    curso_id = request.GET.get("curso", "")
    turma_id = request.GET.get("turma", "")

    atividades = AtividadeAcademica.objects.prefetch_related("turmas__curso").all()

    if query:
        atividades = atividades.filter(nome__icontains=query)
    if curso_id:
        atividades = atividades.filter(curso_id=curso_id)
    if turma_id:
        atividades = atividades.filter(turmas__id=turma_id)

    atividades = atividades.order_by("nome")

    return render(
        request,
        "atividades/partials/atividades_tabela_body.html",
        {"atividades": atividades},
    )

# Reload trigger: 2025-12-20 12:16:29
