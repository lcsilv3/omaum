from django.contrib import admin
from .models import Atividade, Presenca


@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_atividade', 'data_inicio', 'data_fim', 'status', 'curso', 'convocacao')
    list_filter = ('status', 'tipo_atividade', 'curso')
    search_fields = ('nome', 'descricao')
    date_hierarchy = 'data_inicio'
    filter_horizontal = ('turmas',)
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'tipo_atividade', 'responsavel', 'convocacao')
        }),
        ('Datas e Horários', {
            'fields': ('data_inicio', 'data_fim', 'hora_inicio', 'hora_fim')
        }),
        ('Localização', {
            'fields': ('local',)
        }),
        ('Relacionamentos', {
            'fields': ('curso', 'turmas')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )


@admin.register(Presenca)
class PresencaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'turma', 'atividade', 'data', 'presente', 'registrado_por')
    list_filter = ('presente', 'turma', 'atividade', 'data')
    search_fields = ('aluno__nome', 'aluno__cpf', 'turma__nome', 'atividade__nome')
    date_hierarchy = 'data'

