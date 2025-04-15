import importlib
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse

# Set up logger
logger = logging.getLogger(__name__)

print(
    "ARQUIVO VIEWS.PY CARREGADO:",
    importlib.import_module("django.conf").settings.BASE_DIR,
)


def get_return_url(request, default_url):
    """Obtém a URL de retorno do request ou usa o valor padrão."""
    return_url = request.GET.get("return_url", "")
    # Verificação básica de segurança
    if not return_url or not return_url.startswith("/"):
        return default_url
    return return_url


def get_form_class(form_name):
    """Importa dinamicamente uma classe de formulário para evitar importações circulares."""
    forms_module = importlib.import_module("atividades.forms")
    return getattr(forms_module, form_name)


def get_model_class(model_name, module_name="atividades.models"):
    """Importa dinamicamente uma classe de modelo para evitar importações circulares."""
    models_module = importlib.import_module(module_name)
    return getattr(models_module, model_name)


@login_required
def index(request):
    """Página inicial do módulo de atividades."""
    return render(request, "atividades/index.html")


@login_required
def listar_atividades_academicas(request):
    """Lista todas as atividades acadêmicas."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividades = AtividadeAcademica.objects.all()

    # Armazenar a URL atual na sessão para uso posterior
    request.session["last_academicas_list_url"] = request.get_full_path()

    return render(
        request,
        "atividades/listar_atividades_academicas.html",
        {
            "atividades": atividades,
            "return_url": request.path,  # Armazena URL atual para retorno
        },
    )


@login_required
def listar_atividades_ritualisticas(request):
    """Lista todas as atividades ritualísticas."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividades = AtividadeRitualistica.objects.all()

    # Armazenar a URL atual na sessão para uso posterior
    request.session["last_ritualisticas_list_url"] = request.get_full_path()

    # Salvar URL referenciadora, exceto se vier do próprio formulário de atividade ritualística
    referer = request.META.get("HTTP_REFERER", "")
    if referer and not any(
        x in referer
        for x in [
            "criar_atividade_ritualistica",
            "editar_atividade_ritualistica",
        ]
    ):
        request.session["atividade_ritualistica_referer"] = referer

    # Usar a URL referenciadora armazenada ou a página inicial como fallback
    previous_url = request.session.get("atividade_ritualistica_referer", "/")

    return render(
        request,
        "atividades/listar_atividades_ritualisticas.html",
        {
            "atividades": atividades,
            "previous_url": previous_url,
        },
    )


@login_required
def criar_atividade_academica(request):
    """Função para criar uma nova atividade acadêmica."""
    AtividadeAcademicaForm = get_form_class("AtividadeAcademicaForm")
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )

    if request.method == "POST":
        form = AtividadeAcademicaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Atividade acadêmica criada com sucesso."
            )
            return redirect(return_url)
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = AtividadeAcademicaForm()

    return render(
        request,
        "atividades/formulario_atividade_academica.html",
        {"form": form, "return_url": return_url},
    )


@login_required
def editar_atividade_academica(request, pk):
    """Função para editar uma atividade acadêmica existente."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    AtividadeAcademicaForm = get_form_class("AtividadeAcademicaForm")
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )

    if request.method == "POST":
        try:
            form = AtividadeAcademicaForm(request.POST, instance=atividade)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Atividade acadêmica atualizada com sucesso."
                )
                return redirect(return_url)
            else:
                messages.error(request, "Corrija os erros no formulário.")
        except Exception as e:
            messages.error(
                request,
                f"Erro ao processar formulário de atividade acadêmica: {str(e)}",
            )
    else:
        form = AtividadeAcademicaForm(instance=atividade)

    return render(
        request,
        "atividades/formulario_atividade_academica.html",
        {"form": form, "atividade": atividade, "return_url": return_url},
    )


@login_required
def excluir_atividade_academica(request, pk):
    """Função para excluir uma atividade acadêmica."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )

    if request.method == "POST":
        try:
            atividade.delete()
            messages.success(
                request, "Atividade acadêmica excluída com sucesso."
            )
            return redirect(return_url)
        except Exception as e:
            messages.error(
                request, f"Erro ao excluir atividade acadêmica: {str(e)}"
            )
            return redirect("atividades:listar_atividades_academicas")

    return render(
        request,
        "atividades/confirmar_exclusao_academica.html",
        {"atividade": atividade, "return_url": return_url},
    )


@login_required
def confirmar_exclusao_academica(request, pk):
    """Função para confirmar a exclusão de uma atividade acadêmica."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )

    if request.method == "POST":
        try:
            atividade.delete()
            messages.success(
                request, "Atividade acadêmica excluída com sucesso."
            )
            return redirect(return_url)
        except Exception as e:
            messages.error(
                request, f"Erro ao excluir atividade acadêmica: {str(e)}"
            )
            return redirect("atividades:detalhar_atividade_academica", pk=pk)

    return render(
        request,
        "atividades/confirmar_exclusao_academica.html",
        {"atividade": atividade, "return_url": return_url},
    )


@login_required
def detalhar_atividade_academica(request, pk):
    """Função para mostrar detalhes de uma atividade acadêmica."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )

    return render(
        request,
        "atividades/detalhar_atividade_academica.html",
        {"atividade": atividade, "return_url": return_url},
    )


@login_required
def criar_atividade_ritualistica(request):
    """Função para criar uma nova atividade ritualística."""
    AtividadeRitualisticaForm = get_form_class("AtividadeRitualisticaForm")
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    if request.method == "POST":
        try:
            form = AtividadeRitualisticaForm(request.POST)
            if form.is_valid():
                atividade = form.save(commit=False)
                atividade.save()

                # Processar o campo todos_alunos se existir
                if hasattr(form, "cleaned_data") and form.cleaned_data.get(
                    "todos_alunos"
                ):
                    # Obter todos os alunos da turma e adicioná-los à atividade
                    Aluno = get_model_class(
                        "Aluno", module_name="alunos.models"
                    )
                    alunos_da_turma = Aluno.objects.filter(
                        turmas=atividade.turma
                    )
                    for aluno in alunos_da_turma:
                        atividade.participantes.add(aluno)
                else:
                    # Salvar apenas os participantes selecionados no formulário
                    form.save_m2m()

                messages.success(
                    request, "Atividade ritualística criada com sucesso."
                )
                return redirect(return_url)
            else:
                messages.error(request, "Corrija os erros no formulário.")
        except Exception as e:
            messages.error(
                request,
                f"Erro ao processar formulário de atividade ritualística: {str(e)}",
            )
    else:
        form = AtividadeRitualisticaForm()

    return render(
        request,
        "atividades/criar_atividade_ritualistica.html",
        {"form": form, "return_url": return_url},
    )


@login_required
def editar_atividade_ritualistica(request, pk):
    """Função para editar uma atividade ritualística existente."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    AtividadeRitualisticaForm = get_form_class("AtividadeRitualisticaForm")
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    if request.method == "POST":
        try:
            form = AtividadeRitualisticaForm(request.POST, instance=atividade)
            if form.is_valid():
                atividade = form.save(commit=False)
                atividade.save()

                # Processar o campo todos_alunos se existir
                if hasattr(form, "cleaned_data") and form.cleaned_data.get(
                    "todos_alunos"
                ):
                    # Limpar participantes existentes
                    atividade.participantes.clear()
                    # Obter todos os alunos da turma e adicioná-los à atividade
                    Aluno = get_model_class(
                        "Aluno", module_name="alunos.models"
                    )
                    alunos_da_turma = Aluno.objects.filter(
                        turmas=atividade.turma
                    )
                    for aluno in alunos_da_turma:
                        atividade.participantes.add(aluno)
                else:
                    # Salvar apenas os participantes selecionados no formulário
                    form.save_m2m()

                messages.success(
                    request, "Atividade ritualística atualizada com sucesso."
                )
                return redirect(return_url)
            else:
                messages.error(request, "Corrija os erros no formulário.")
        except Exception as e:
            messages.error(
                request,
                f"Erro ao processar formulário de atividade ritualística: {str(e)}",
            )
    else:
        form = AtividadeRitualisticaForm(instance=atividade)

    return render(
        request,
        "atividades/editar_atividade_ritualistica.html",
        {"form": form, "atividade": atividade, "return_url": return_url},
    )


@login_required
def excluir_atividade_ritualistica(request, pk):
    """Função para excluir uma atividade ritualística."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    if request.method == "POST":
        try:
            atividade.delete()
            messages.success(
                request, "Atividade ritualística excluída com sucesso."
            )
            return redirect(return_url)
        except Exception as e:
            messages.error(
                request, f"Erro ao excluir atividade ritualística: {str(e)}"
            )
            return redirect("atividades:listar_atividades_ritualisticas")

    return render(
        request,
        "atividades/confirmar_exclusao_ritualistica.html",
        {"atividade": atividade, "return_url": return_url},
    )


@login_required
def confirmar_exclusao_ritualistica(request, pk):
    """Função para confirmar a exclusão de uma atividade ritualística."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    if request.method == "POST":
        try:
            atividade.delete()
            messages.success(
                request, "Atividade ritualística excluída com sucesso."
            )
            return redirect(return_url)
        except Exception as e:
            messages.error(
                request, f"Erro ao excluir atividade ritualística: {str(e)}"
            )
            return redirect(
                "atividades:detalhar_atividade_ritualistica", pk=pk
            )

    return render(
        request,
        "atividades/confirmar_exclusao_ritualistica.html",
        {"atividade": atividade, "return_url": return_url},
    )


@login_required
def detalhar_atividade_ritualistica(request, pk):
    """Função para mostrar detalhes de uma atividade ritualística."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    return render(
        request,
        "atividades/detalhar_atividade_ritualistica.html",
        {"atividade": atividade, "return_url": return_url},
    )
