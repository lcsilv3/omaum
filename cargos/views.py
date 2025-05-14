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
    CargoAdministrativo = get_cargo_administrativo_model()
    cargos = CargoAdministrativo.objects.all()
    return render(request, "cargos/listar_cargos.html", {"cargos": cargos})


@login_required
def criar_cargo(request):
    """Cria um novo cargo administrativo."""
    CargoAdministrativoForm = get_cargo_administrativo_form()

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
    CargoAdministrativo = get_cargo_administrativo_model()
    cargo = get_object_or_404(CargoAdministrativo, id=id)
    return render(request, "cargos/detalhar_cargo.html", {"cargo": cargo})


@login_required
def editar_cargo(request, id):
    """Edita um cargo administrativo existente."""
    CargoAdministrativo = get_cargo_administrativo_model()
    CargoAdministrativoForm = get_cargo_administrativo_form()

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
    CargoAdministrativo = get_cargo_administrativo_model()
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


@login_required
def exportar_cargos(request):
    """Exporta os dados dos cargos para um arquivo CSV."""
    try:
        import csv
        from django.http import HttpResponse
        
        CargoAdministrativo = get_cargo_administrativo_model()
        cargos = CargoAdministrativo.objects.all()
        
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="cargos.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "ID",
            "Código",
            "Nome",
            "Descrição"
        ])
        
        for cargo in cargos:
            writer.writerow([
                cargo.id,
                cargo.codigo_cargo,
                cargo.nome,
                cargo.descricao
            ])
        
        return response
    except Exception as e:
        messages.error(request, f"Erro ao exportar cargos: {str(e)}")
        return redirect("cargos:listar_cargos")


@login_required
def importar_cargos(request):
    """Importa cargos de um arquivo CSV."""
    if request.method == "POST" and request.FILES.get("csv_file"):
        try:
            import csv
            from io import TextIOWrapper
            
            CargoAdministrativo = get_cargo_administrativo_model()
            
            csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")
            reader = csv.DictReader(csv_file)
            count = 0
            errors = []
            
            for row in reader:
                try:
                    # Verificar se já existe um cargo com este código
                    codigo_cargo = row.get("Código", "").strip()
                    if not codigo_cargo:
                        errors.append("Código do cargo não especificado")
                        continue
                    
                    if CargoAdministrativo.objects.filter(codigo_cargo=codigo_cargo).exists():
                        errors.append(f"Já existe um cargo com o código {codigo_cargo}")
                        continue
                    
                    # Criar o cargo
                    CargoAdministrativo.objects.create(
                        codigo_cargo=codigo_cargo,
                        nome=row.get("Nome", "").strip(),
                        descricao=row.get("Descrição", "").strip()
                    )
                    
                    count += 1
                except Exception as e:
                    errors.append(f"Erro na linha {count+1}: {str(e)}")
            
            if errors:
                messages.warning(
                    request,
                    f"{count} cargos importados com {len(errors)} erros.",
                )
                for error in errors[:5]:  # Mostrar apenas os 5 primeiros erros
                    messages.error(request, error)
                if len(errors) > 5:
                    messages.error(
                        request, f"... e mais {len(errors) - 5} erros."
                    )
            else:
                messages.success(
                    request, f"{count} cargos importados com sucesso!"
                )
            return redirect("cargos:listar_cargos")
        except Exception as e:
            messages.error(request, f"Erro ao importar cargos: {str(e)}")
    
    return render(request, "cargos/importar_cargos.html")
