import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..views.utils import get_cursos, get_turmas, get_atividades_academicas

logger = logging.getLogger(__name__)

@login_required
def relatorio_atividades_academicas(request):
    cursos = get_cursos()
    curso_id = request.GET.get("curso")
    turma_id = request.GET.get("turma")
    query = request.GET.get("q", "")

    atividades = get_atividades_academicas(curso_id=curso_id, turma_id=turma_id, query=query)

    # Organiza atividades por curso
    cursos_dict = {}
    for atividade in atividades:
        curso_nome = atividade.curso.nome if atividade.curso else "Sem curso"
        cursos_dict.setdefault(curso_nome, []).append(atividade)

    context = {
        "cursos": cursos,
        "curso_id": curso_id,
        "cursos_dict": cursos_dict,
    }
    return render(request, "atividades/academicas/relatorio_atividades_academicas.html", context)