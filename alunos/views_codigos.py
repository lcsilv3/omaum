from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from importlib import import_module
from .forms_codigos import TipoCodigoForm, CodigoForm

TipoCodigo = import_module("alunos.utils").get_tipo_codigo_model()
Codigo = import_module("alunos.utils").get_codigo_model()


def _exibir_inativos(request):
    """Retorna se a listagem deve incluir registros inativos."""

    return request.GET.get("exibir_inativos") == "1"


@login_required
@permission_required("alunos.gerenciar_tipocodigo", raise_exception=True)
def listar_tipocodigos(request):
    incluir_inativos = _exibir_inativos(request)
    tipos = TipoCodigo.objects.all()
    if not incluir_inativos:
        tipos = tipos.filter(ativo=True)
    return render(
        request,
        "alunos/listar_tipocodigos.html",
        {"tipos": tipos, "exibir_inativos": incluir_inativos},
    )


@login_required
@permission_required("alunos.gerenciar_tipocodigo", raise_exception=True)
def criar_tipocodigo(request):
    if request.method == "POST":
        form = TipoCodigoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_tipocodigos")
    else:
        form = TipoCodigoForm()
    return render(request, "alunos/formulario_tipocodigo.html", {"form": form})


@login_required
@permission_required("alunos.gerenciar_tipocodigo", raise_exception=True)
def editar_tipocodigo(request, pk):
    tipo = get_object_or_404(TipoCodigo, pk=pk)
    if request.method == "POST":
        form = TipoCodigoForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            return redirect("listar_tipocodigos")
    else:
        form = TipoCodigoForm(instance=tipo)
    return render(
        request, "alunos/formulario_tipocodigo.html", {"form": form, "editar": True}
    )


@login_required
@permission_required("alunos.gerenciar_tipocodigo", raise_exception=True)
def excluir_tipocodigo(request, pk):
    tipo = get_object_or_404(TipoCodigo, pk=pk)
    if request.method == "POST":
        tipo.delete()
        return redirect("listar_tipocodigos")
    return render(request, "alunos/confirmar_exclusao_tipocodigo.html", {"obj": tipo})


@login_required
@permission_required("alunos.gerenciar_codigo", raise_exception=True)
def listar_codigos(request):
    incluir_inativos = _exibir_inativos(request)
    codigos = Codigo.objects.select_related("tipo_codigo").all()
    tipos = TipoCodigo.objects.all()
    if not incluir_inativos:
        codigos = codigos.filter(ativo=True, tipo_codigo__ativo=True)
        tipos = tipos.filter(ativo=True)
    tipo_filtro = request.GET.get("tipo_codigo")
    if tipo_filtro:
        codigos = codigos.filter(tipo_codigo_id=tipo_filtro)
    return render(
        request,
        "alunos/listar_codigos.html",
        {
            "codigos": codigos,
            "tipos": tipos,
            "tipo_filtro": tipo_filtro,
            "exibir_inativos": incluir_inativos,
        },
    )


@login_required
@permission_required("alunos.gerenciar_codigo", raise_exception=True)
def criar_codigo(request):
    if request.method == "POST":
        form = CodigoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_codigos")
    else:
        form = CodigoForm()
    return render(request, "alunos/formulario_codigo.html", {"form": form})


@login_required
@permission_required("alunos.gerenciar_codigo", raise_exception=True)
def editar_codigo(request, pk):
    codigo = get_object_or_404(Codigo, pk=pk)
    if request.method == "POST":
        form = CodigoForm(request.POST, instance=codigo)
        if form.is_valid():
            form.save()
            return redirect("listar_codigos")
    else:
        form = CodigoForm(instance=codigo)
    return render(
        request, "alunos/formulario_codigo.html", {"form": form, "editar": True}
    )


@login_required
@permission_required("alunos.gerenciar_codigo", raise_exception=True)
def excluir_codigo(request, pk):
    codigo = get_object_or_404(Codigo, pk=pk)
    if request.method == "POST":
        codigo.delete()
        return redirect("listar_codigos")
    return render(request, "alunos/confirmar_exclusao_codigo.html", {"obj": codigo})
