from django.contrib import admin
from .models import CargoAdministrativo

@admin.register(CargoAdministrativo)
class CargoAdministrativoAdmin(admin.ModelAdmin):
    list_display = ['codigo_cargo', 'nome', 'descricao']
    search_fields = ['codigo_cargo', 'nome']
    list_filter = ['codigo_cargo']
