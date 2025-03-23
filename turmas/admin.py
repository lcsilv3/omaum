from django.contrib import admin
from .models import Turma, Matricula

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'curso', 'data_inicio', 'data_fim', 'status', 'capacidade']
    list_filter = ['status', 'curso']
    search_fields = ['nome', 'curso__nome']
    date_hierarchy = 'data_inicio'

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'turma', 'data_matricula', 'status']
    list_filter = ['status', 'turma']
    search_fields = ['aluno__nome', 'turma__nome']
    date_hierarchy = 'data_matricula'
