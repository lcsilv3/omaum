from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from importlib import import_module
from .forms import PresencaForm


def get_model(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)


@login_required
def listar_presencas(request):
    """Lista todas as presenças registradas."""
    Presenca = get_model("presencas", "Presenca")
    presencas = Presenca.objects.all()
    return render(
        request, "presencas/listar_presencas.html", {"presencas": presencas}
    )


@login_required
def detalhar_presenca(request, presenca_id):
    """Exibe os detalhes de uma presença específica."""
    Presenca = get_model("presencas", "Presenca")
    presenca = get_object_or_404(Presenca, id=presenca_id)
    return render(
        request, "presencas/detalhar_presenca.html", {"presenca": presenca}
    )


@login_required
def criar_presenca(request):
    """Cria uma nova presença."""
    if request.method == "POST":
        form = PresencaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Presença registrada com sucesso!")
            return redirect("presencas:listar_presencas")
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = PresencaForm()
    return render(request, "presencas/form_presenca.html", {"form": form})


@login_required
def editar_presenca(request, presenca_id):
    """Edita uma presença existente."""
    Presenca = get_model("presencas", "Presenca")
    presenca = get_object_or_404(Presenca, id=presenca_id)
    if request.method == "POST":
        form = PresencaForm(request.POST, instance=presenca)
        if form.is_valid():
            form.save()
            messages.success(request, "Presença atualizada com sucesso!")
            return redirect("presencas:listar_presencas")
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = PresencaForm(instance=presenca)
    return render(request, "presencas/form_presenca.html", {"form": form})


@login_required
def excluir_presenca(request, presenca_id):
    """Exclui uma presença."""
    Presenca = get_model("presencas", "Presenca")
    presenca = get_object_or_404(Presenca, id=presenca_id)
    if request.method == "POST":
        presenca.delete()
        messages.success(request, "Presença excluída com sucesso!")
        return redirect("presencas:listar_presencas")
    return render(
        request, "presencas/confirmar_exclusao.html", {"presenca": presenca}
    )


@login_required
def relatorio_presencas(request):
    """Gera um relatório de presenças."""
    Presenca = get_model("presencas", "Presenca")
    presencas = Presenca.objects.all()
    return render(
        request, "presencas/relatorio_presencas.html", {"presencas": presencas}
    )
