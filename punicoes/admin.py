from django.contrib import admin
from .models import Punicao, TipoPunicao

@admin.register(Punicao)
class PunicaoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'tipo_punicao', 'data_aplicacao', 'status')
    list_filter = ('tipo_punicao', 'status', 'data_aplicacao')
    search_fields = ('aluno__nome', 'descricao')
    date_hierarchy = 'data_aplicacao'

@admin.register(TipoPunicao)
class TipoPunicaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'gravidade')
    list_filter = ('gravidade',)
    search_fields = ('nome', 'descricao')