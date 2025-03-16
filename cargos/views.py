from django.shortcuts import render, get_object_or_404
from .models import CargoAdministrativo

def listar_cargos_administrativos(request):
    cargos = CargoAdministrativo.objects.all()
    return render(request, 'cargos/listar_cargos.html', {'cargos': cargos})

def detalhe_cargo(request, codigo_cargo):
    cargo = get_object_or_404(CargoAdministrativo, codigo_cargo=codigo_cargo)
    return render(request, 'cargos/detalhe_cargo.html', {'cargo': cargo})
