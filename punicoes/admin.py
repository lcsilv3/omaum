from django.contrib import admin
from .models import Punicao, TipoPunicao


@admin.register(Punicao)
class PunicaoAdmin(admin.ModelAdmin):
    list_display = ["aluno"]
    list_filter = []
    search_fields = ("aluno__nome", "descricao")
    date_hierarchy = "data_aplicacao"


@admin.register(TipoPunicao)
class TipoPunicaoAdmin(admin.ModelAdmin):
    list_display = ["nome", "descricao"]
    list_filter = []
    search_fields = ("nome", "descricao")
