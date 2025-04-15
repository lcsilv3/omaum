from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import importlib


# Importando modelos e formulários usando importlib para evitar importações circulares
def get_model(app_name, model_name):
    module = importlib.import_module(f"{app_name}.models")
    return getattr(module, model_name)


def get_form(app_name, form_name):
    module = importlib.import_module(f"{app_name}.forms")
    return getattr(module, form_name)


@login_required
def listar_punicoes(request):
    Punicao = get_model("punicoes", "Punicao")
    Aluno = get_model("alunos", "Aluno")
    TipoPunicao = get_model("punicoes", "TipoPunicao")

    # Filtros
    filtro_aluno = request.GET.get("aluno")
    filtro_tipo = request.GET.get("tipo")
    filtro_status = request.GET.get("status")

    punicoes = Punicao.objects.all().order_by("-data_aplicacao")

    if filtro_aluno:
        punicoes = punicoes.filter(aluno_id=filtro_aluno)

    if filtro_tipo:
        punicoes = punicoes.filter(tipo_punicao_id=filtro_tipo)

    if filtro_status:
        punicoes = punicoes.filter(status=filtro_status)

    # Paginação
    paginator = Paginator(punicoes, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Dados para filtros
    alunos = Aluno.objects.all().order_by("nome")
    tipos_punicao = TipoPunicao.objects.all().order_by("nome")

    context = {
        "punicoes": page_obj,
        "alunos": alunos,
        "tipos_punicao": tipos_punicao,
    }

    return render(request, "punicoes/listar_punicoes.html", context)


@login_required
def criar_punicao(request):
    PunicaoForm = get_form("punicoes", "PunicaoForm")

    if request.method == "POST":
        form = PunicaoForm(request.POST)
        if form.is_valid():
            punicao = form.save(commit=False)
            punicao.registrado_por = request.user
            punicao.save()
            messages.success(request, "Punição registrada com sucesso!")
            return redirect("punicoes:listar_punicoes")
    else:
        form = PunicaoForm()

    return render(request, "punicoes/criar_punicao.html", {"form": form})


@login_required
def aplicar_punicao(request):
    """Aplica uma punição a um aluno."""
    if request.method == "POST":
        form = PunicaoForm(request.POST)
        if form.is_valid():
            punicao = form.save(commit=False)
            punicao.aplicada_por = request.user
            punicao.save()
            messages.success(request, "Punição aplicada com sucesso!")
            return redirect("punicoes:listar_punicoes")
    else:
        form = PunicaoForm()

    return render(request, "punicoes/aplicar_punicao.html", {"form": form})


@login_required
def editar_punicao(request, id):
    """Edita uma punição."""
    punicao = get_object_or_404(Punicao, id=id)

    if request.method == "POST":
        form = PunicaoForm(request.POST, instance=punicao)
        if form.is_valid():
            form.save()
            messages.success(request, "Punição atualizada com sucesso!")
            return redirect("punicoes:listar_punicoes")
    else:
        form = PunicaoForm(instance=punicao)

    return render(
        request,
        "punicoes/editar_punicao.html",
        {"form": form, "punicao": punicao},
    )


@login_required
def excluir_punicao(request, id):
    Punicao = get_model("punicoes", "Punicao")

    punicao = get_object_or_404(Punicao, id=id)

    if request.method == "POST":
        punicao.delete()
        messages.success(request, "Punição excluída com sucesso!")
        return redirect("punicoes:listar_punicoes")

    return render(
        request, "punicoes/excluir_punicao.html", {"punicao": punicao}
    )


@login_required
def detalhar_punicao(request, id):
    Punicao = get_model("punicoes", "Punicao")

    punicao = get_object_or_404(Punicao, id=id)

    return render(
        request, "punicoes/detalhar_punicao.html", {"punicao": punicao}
    )


@login_required
def listar_tipos_punicao(request):
    TipoPunicao = get_model("punicoes", "TipoPunicao")

    tipos_punicao = TipoPunicao.objects.all().order_by("nome")

    return render(
        request,
        "punicoes/listar_tipos_punicao.html",
        {"tipos_punicao": tipos_punicao},
    )


@login_required
def criar_tipo_punicao(request):
    TipoPunicaoForm = get_form("punicoes", "TipoPunicaoForm")

    if request.method == "POST":
        form = TipoPunicaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de punição criado com sucesso!")
            return redirect("punicoes:listar_tipos_punicao")
    else:
        form = TipoPunicaoForm()

    return render(request, "punicoes/criar_tipo_punicao.html", {"form": form})


@login_required
def editar_tipo_punicao(request, id):
    TipoPunicao = get_model("punicoes", "TipoPunicao")
    TipoPunicaoForm = get_form("punicoes", "TipoPunicaoForm")

    tipo_punicao = get_object_or_404(TipoPunicao, id=id)

    if request.method == "POST":
        form = TipoPunicaoForm(request.POST, instance=tipo_punicao)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Tipo de punição atualizado com sucesso!"
            )
            return redirect("punicoes:listar_tipos_punicao")
    else:
        form = TipoPunicaoForm(instance=tipo_punicao)

    return render(
        request,
        "punicoes/editar_tipo_punicao.html",
        {"form": form, "tipo_punicao": tipo_punicao},
    )


@login_required
def excluir_tipo_punicao(request, id):
    TipoPunicao = get_model("punicoes", "TipoPunicao")
    Punicao = get_model("punicoes", "Punicao")

    tipo_punicao = get_object_or_404(TipoPunicao, id=id)

    # Verificar se existem punições associadas a este tipo
    punicoes_associadas = Punicao.objects.filter(
        tipo_punicao=tipo_punicao
    ).count()

    if request.method == "POST":
        tipo_punicao.delete()
        messages.success(request, "Tipo de punição excluído com sucesso!")
        return redirect("punicoes:listar_tipos_punicao")

    return render(
        request,
        "punicoes/excluir_tipo_punicao.html",
        {
            "tipo_punicao": tipo_punicao,
            "punicoes_associadas": punicoes_associadas,
        },
    )
