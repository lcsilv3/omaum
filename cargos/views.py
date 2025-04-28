from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Importar a função utilitária centralizada
from core.utils import get_model_dynamically, get_form_dynamically

# Importar o formulário diretamente, pois está no mesmo aplicativo
from .forms import AtribuirCargoForm
from .models import AtribuicaoCargo

def get_cargo_administrativo_model():
    """Obtém o modelo CargoAdministrativo dinamicamente."""
    return get_model_dynamically("cargos", "CargoAdministrativo")

def get_cargo_administrativo_form():
    """Obtém o formulário CargoAdministrativoForm dinamicamente."""
    return get_form_dynamically("cargos", "CargoAdministrativoForm")


@login_required
def listar_cargos(request):
    """Lista todos os cargos administrativos."""
    CargoAdministrativo = get_models()
    cargos = CargoAdministrativo.objects.all()
    return render(request, "cargos/listar_cargos.html", {"cargos": cargos})


@login_required
def criar_cargo(request):
    """Cria um novo cargo administrativo."""
    CargoAdministrativoForm = get_forms()

    if request.method == "POST":
        form = CargoAdministrativoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Cargo administrativo criado com sucesso!"
            )
            return redirect("cargos:listar_cargos")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = CargoAdministrativoForm()

    return render(request, "cargos/criar_cargo.html", {"form": form})


@login_required
def detalhar_cargo(request, id):
    """Exibe os detalhes de um cargo administrativo."""
    CargoAdministrativo = get_models()
    cargo = get_object_or_404(CargoAdministrativo, id=id)
    return render(request, "cargos/detalhar_cargo.html", {"cargo": cargo})


@login_required
def editar_cargo(request, id):
    """Edita um cargo administrativo existente."""
    CargoAdministrativo = get_models()
    CargoAdministrativoForm = get_forms()

    cargo = get_object_or_404(CargoAdministrativo, id=id)

    if request.method == "POST":
        form = CargoAdministrativoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Cargo administrativo atualizado com sucesso!"
            )
            return redirect("cargos:listar_cargos")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = CargoAdministrativoForm(instance=cargo)

    return render(
        request, "cargos/editar_cargo.html", {"form": form, "cargo": cargo}
    )


@login_required
def excluir_cargo(request, id):
    """Exclui um cargo administrativo."""
    CargoAdministrativo = get_models()
    cargo = get_object_or_404(CargoAdministrativo, id=id)

    if request.method == "POST":
        cargo.delete()
        messages.success(request, "Cargo administrativo excluído com sucesso!")
        return redirect("cargos:listar_cargos")

    return render(request, "cargos/excluir_cargo.html", {"cargo": cargo})


@login_required
def atribuir_cargo(request):
    if request.method == "POST":
        form = AtribuirCargoForm(request.POST)
        if form.is_valid():
            atribuicao = AtribuicaoCargo(
                aluno=form.cleaned_data["aluno"],
                cargo=form.cleaned_data["cargo"],
                data_inicio=form.cleaned_data["data_inicio"],
                data_fim=form.cleaned_data["data_fim"],
            )
            atribuicao.save()
            messages.success(request, "Cargo atribuído com sucesso!")
            return redirect("cargos:listar_cargos")
    else:
        form = AtribuirCargoForm()

    return render(request, "cargos/atribuir_cargo.html", {"form": form})


@login_required
def remover_atribuicao_cargo(request, id):
    """Remove a atribuição de um cargo a um aluno."""
    # Implementação pendente
    return render(request, "cargos/remover_atribuicao.html")
