from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from importlib import import_module

from ..models import AtividadeAcademica

@login_required
def dashboard_atividades(request):
    """
    Dashboard de atividades com filtros dinâmicos por curso e turma.
    Suporta AJAX para atualização dos cards/gráficos/tabelas.
    """
    Curso = import_module("cursos.models").Curso
    Turma = import_module("turmas.models").Turma

    cursos = Curso.objects.all()
    turmas = Turma.objects.all()

    curso_id = request.GET.get("curso")
    turma_id = request.GET.get("turma")

    atividades = AtividadeAcademica.objects.all()

    if curso_id:
        atividades = atividades.filter(turma__curso_id=curso_id)
        turmas = turmas.filter(curso_id=curso_id)
    if turma_id:
        atividades = atividades.filter(turma_id=turma_id)

    atividades = atividades.select_related("turma__curso").distinct()

    # Exemplo de dados para cards
    total_atividades = atividades.count()
    total_turmas = turmas.count()
    total_cursos = cursos.count()

    context = {
        "atividades": atividades,
        "cursos": cursos,
        "turmas": turmas,
        "curso_selecionado": curso_id,
        "turma_selecionada": turma_id,
        "total_atividades": total_atividades,
        "total_turmas": total_turmas,
        "total_cursos": total_cursos,
    }

    # AJAX: retorna apenas o conteúdo do dashboard para atualização dinâmica
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "atividades/_dashboard_conteudo.html", context)

    return render(request, "atividades/dashboard.html", context)

@require_GET
@login_required
def ajax_turmas_por_curso_dashboard(request):
    """
    Endpoint AJAX: retorna as turmas de um curso em JSON (para dashboard).
    """
    curso_id = request.GET.get("curso_id")
    Turma = import_module("turmas.models").Turma
    turmas = Turma.objects.filter(curso_id=curso_id).values("id", "nome")
    return JsonResponse(list(turmas), safe=False)

@require_GET
@login_required
def ajax_dashboard_conteudo(request):
    """
    Endpoint AJAX: retorna conteúdo do dashboard filtrado.
    """
    return dashboard_atividades(request)
