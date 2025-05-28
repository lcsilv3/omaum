from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from importlib import import_module
from .models import AtividadeAcademica
from .forms import AtividadeAcademicaForm
from cursos.models import Curso
from turmas.models import Turma

def listar_atividades_academicas(request):
    query = request.GET.get("q", "")
    codigo_curso = request.GET.get("codigo_curso", "")
    turma_selecionada = request.GET.get("turma", "")

    cursos = Curso.objects.all()
    turmas = Turma.objects.all()
    if codigo_curso:
        turmas = turmas.filter(curso__codigo_curso=codigo_curso)

    atividades = AtividadeAcademica.objects.all()
    if query:
        atividades = atividades.filter(nome__icontains=query)
    if codigo_curso:
        atividades = atividades.filter(curso__codigo_curso=codigo_curso)
    if turma_selecionada:
        atividades = atividades.filter(turmas__id=turma_selecionada)

    context = {
        "cursos": cursos,
        "turmas": turmas,
        "codigo_curso_selecionado": codigo_curso,
        "turma_selecionada": turma_selecionada,
        "atividades": atividades,
        "query": query,
    }
    return render(request, "atividades/listar_atividades_academicas.html", context)


def relatorio_atividades(request):
    atividades = AtividadeAcademica.objects.prefetch_related('turmas__curso').all()

    curso_id = request.GET.get("curso")
    if curso_id:
        atividades = atividades.filter(turmas__curso__codigo_curso=curso_id)

    cursos_dict = {}
    for atividade in atividades:
        curso = atividade.curso
        if curso not in cursos_dict:
            cursos_dict[curso] = []
        cursos_dict[curso].append(atividade)

    Curso = import_module("cursos.models").Curso
    cursos = Curso.objects.all()

    return render(request, "atividades/relatorio_atividades.html", {
        "atividades": atividades,
        "cursos_dict": cursos_dict,
        "cursos": cursos,
        "curso_id": curso_id,
    })

def criar_atividade_academica(request):
    """
    Cria uma nova atividade acadêmica.
    """
    if request.method == "POST":
        form = AtividadeAcademicaForm(request.POST)
        if form.is_valid():
            atividade = form.save()
            messages.success(request, "Atividade acadêmica criada com sucesso!")
            return redirect(reverse("atividades:detalhar_atividade_academica", args=[atividade.pk]))
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = AtividadeAcademicaForm()
    return render(request, "atividades/form_atividade_academica.html", {"form": form})

def editar_atividade_academica(request, pk):
    """
    Edita uma atividade acadêmica existente.
    """
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    if request.method == "POST":
        form = AtividadeAcademicaForm(request.POST, instance=atividade)
        if form.is_valid():
            atividade = form.save()
            messages.success(request, "Atividade acadêmica atualizada com sucesso!")
            return redirect(reverse("atividades:detalhar_atividade_academica", args=[atividade.pk]))
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = AtividadeAcademicaForm(instance=atividade)
    return render(request, "atividades/form_atividade_academica.html", {"form": form, "atividade": atividade})

def detalhar_atividade_academica(request, pk):
    """
    Exibe os detalhes de uma atividade acadêmica.
    """
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    curso = atividade.curso  # propriedade do model, obtida via turma
    return render(request, "atividades/detalhar_atividade_academica.html", {
        "atividade": atividade,
        "curso": curso,
    })

def excluir_atividade_academica(request, pk):
    """
    Exclui uma atividade acadêmica.
    """
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    if request.method == "POST":
        atividade.delete()
        messages.success(request, "Atividade acadêmica excluída com sucesso!")
        return redirect(reverse("atividades:listar_atividades_academicas"))
    return render(request, "atividades/excluir_atividade_academica.html", {"atividade": atividade})
def relatorio_atividades(request):
    """
    Relatório de atividades acadêmicas agrupadas por curso (via turma).
    """
    atividades = AtividadeAcademica.objects.prefetch_related('turmas__curso').all()

    # Filtro por curso
    curso_id = request.GET.get("curso")
    if curso_id:
        atividades = atividades.filter(turmas__curso__codigo_curso=curso_id)

    # Agrupamento por curso para estatísticas
    cursos_dict = {}
    for atividade in atividades:
        curso = atividade.curso
        if curso not in cursos_dict:
            cursos_dict[curso] = []
        cursos_dict[curso].append(atividade)

    # Buscar todos os cursos para o filtro
    Curso = import_module("cursos.models").Curso
    cursos = Curso.objects.all()

    return render(request, "atividades/relatorio_atividades.html", {
        "atividades": atividades,
        "cursos_dict": cursos_dict,
        "cursos": cursos,
        "curso_id": curso_id,
    })

def ajax_atividades_filtradas(request):
    # ... lógica de filtro ...
    return render(request, "atividades/partials/atividades_tabela_body.html", {"atividades": atividades})