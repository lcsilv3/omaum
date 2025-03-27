from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CargoAdministrativo
from .formulario_cargo import CargoAdministrativoForm

def listar_cargos(request):
    cargos = CargoAdministrativo.objects.all()
    return render(request, 'cargos/listar_cargos.html', {'cargos': cargos})

def criar_cargo(request):
    if request.method == 'POST':
        form = CargoAdministrativoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cargo administrativo criado com sucesso!')
            return redirect('cargos:listar_cargos')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CargoAdministrativoForm()
    return render(request, 'cargos/criar_cargo.html', {'form': form})

def editar_cargo(request, id):
    cargo = get_object_or_404(CargoAdministrativo, id=id)
    if request.method == 'POST':
        form = CargoAdministrativoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cargo administrativo atualizado com sucesso!')
            return redirect('cargos:listar_cargos')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CargoAdministrativoForm(instance=cargo)
    return render(request, 'cargos/editar_cargo.html', {'form': form, 'cargo': cargo})

def excluir_cargo(request, id):
    cargo = get_object_or_404(CargoAdministrativo, id=id)
    if request.method == 'POST':
        cargo.delete()
        messages.success(request, 'Cargo administrativo excluído com sucesso!')
        return redirect('cargos:listar_cargos')
    return render(request, 'cargos/excluir_cargo.html', {'cargo': cargo})

def detalhes_cargo(request, id):
    cargo = get_object_or_404(CargoAdministrativo, id=id)
    return render(request, 'cargos/detalhes_cargo.html', {'cargo': cargo})
