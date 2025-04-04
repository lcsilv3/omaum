from django.contrib import admin
from .models import AtividadeAcademica, AtividadeRitualistica

@admin.register(AtividadeAcademica)
class AtividadeAcademicaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'data_inicio', 'data_fim', 'turma')
    list_filter = ('turma',)
    search_fields = ('nome', 'descricao')

@admin.register(AtividadeRitualistica)
class AtividadeRitualisticaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    list_filter = ('turma',)
    search_fields = ('nome', 'descricao')
    filter_horizontal = []
