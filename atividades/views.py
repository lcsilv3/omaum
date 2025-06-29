from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from .utils import get_models, get_cursos


def relatorio_atividades(request):
    models = get_models()
    AtividadeAcademica = models['AtividadeAcademica']
    Curso = models['Curso']

    atividades = AtividadeAcademica.objects.prefetch_related('turmas__curso').all()
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
    return render(request, "atividades/relatorio_atividades.html", {
        "atividades": atividades,
        "cursos_dict": cursos_dict,
        "cursos": cursos,
        "curso_id": curso_id,
    })


@login_required
def listar_atividades_academicas(request):
    """
    Lista atividades acadêmicas com filtros dinâmicos por curso e turma.
    Suporta AJAX para atualização parcial da tabela e dos selects.
    """
    query = request.GET.get("q", "")
    curso_id = request.GET.get("curso", "")
    turma_id = request.GET.get("turma", "")
    models = get_models()
    Curso = models['Curso']
    Turma = models['Turma']
    AtividadeAcademica = models['AtividadeAcademica']

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
        cursos = cursos.filter(id__in=Turma.objects.filter(id=turma_id).values_list('curso_id', flat=True))

    context = {
        "atividades": atividades,
        "cursos": cursos,
        "turmas": turmas,
        "query": query,
        "curso_selecionado": curso_id,
        "turma_selecionada": turma_id,
    }
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        tabela_html = render_to_string("atividades/academicas/partials/atividades_tabela.html", context, request=request)
        cursos_html = render_to_string("atividades/academicas/partials/cursos_options.html", context, request=request)
        turmas_html = render_to_string("atividades/academicas/partials/turmas_options.html", context, request=request)
        return JsonResponse({
            "tabela_html": tabela_html,
            "cursos_html": cursos_html,
            "turmas_html": turmas_html,
        })
    return render(request, "atividades/academicas/listar_atividades_academicas.html", context)


def ajax_atividades_filtradas(request):
    # ... lógica de filtro ...
    # Sugestão: use get_models() e get_cursos() se necessário
    return render(request, "atividades/partials/atividades_tabela_body.html", {"atividades": atividades})
    return render(request, "atividades/partials/atividades_tabela_body.html", {"atividades": atividades})