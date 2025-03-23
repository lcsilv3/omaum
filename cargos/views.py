from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import models
from .models import CargoAdministrativo
from .forms import CargoAdministrativoForm


def listar_cargos_administrativos(request):
    search_query = request.GET.get('search', '')
   
    if search_query:
        cargos = CargoAdministrativo.objects.filter(
            models.Q(codigo_cargo__icontains=search_query) |
            models.Q(nome__icontains=search_query) |
            models.Q(descricao__icontains=search_query)
        )
    else:
        cargos = CargoAdministrativo.objects.all()
   
    return render(request, 'cargos/listar_cargos.html', {
        'cargos': cargos,
        'search_query': search_query
    })


def detalhe_cargo(request, codigo_cargo):
    cargo = get_object_or_404(CargoAdministrativo, codigo_cargo=codigo_cargo)
    return render(request, 'cargos/detalhe_cargo.html', {'cargo': cargo})


def criar_cargo(request):
    if request.method == 'POST':
        form = CargoAdministrativoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cargo administrativo criado com sucesso!')
            return redirect('cargos:listar_cargos_administrativos')
    else:
        form = CargoAdministrativoForm()
   
    return render(request, 'cargos/form_cargo.html', {'form': form, 'titulo': 'Novo Cargo Administrativo'})


def editar_cargo(request, codigo_cargo):
    cargo = get_object_or_404(CargoAdministrativo, codigo_cargo=codigo_cargo)
   
    if request.method == 'POST':
        form = CargoAdministrativoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cargo administrativo atualizado com sucesso!')
            return redirect('cargos:listar_cargos_administrativos')
    else:
        form = CargoAdministrativoForm(instance=cargo)
   
    return render(request, 'cargos/form_cargo.html', {'form': form, 'titulo': 'Editar Cargo Administrativo'})


def excluir_cargo(request, codigo_cargo):
    cargo = get_object_or_404(CargoAdministrativo, codigo_cargo=codigo_cargo)
   
    if request.method == 'POST':
        cargo.delete()
        messages.success(request, 'Cargo administrativo excluído com sucesso!')
        return redirect('cargos:listar_cargos_administrativos')
   
    return render(request, 'cargos/confirmar_exclusao.html', {'cargo': cargo})
