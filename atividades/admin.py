from django.contrib import admin
from .models import (
    AtividadeAcademica,
    AtividadeRitualistica,
    PresencaAcademica,
    PresencaRitualistica,
    ObservacaoPresenca,
)

@admin.register(AtividadeAcademica)
class AtividadeAcademicaAdmin(admin.ModelAdmin):
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

@admin.register(AtividadeRitualistica)
class AtividadeRitualisticaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data', 'hora_inicio', 'status', 'convocacao')
    list_filter = ('status',)
    search_fields = ('nome', 'descricao')
    date_hierarchy = 'data'
    filter_horizontal = ('participantes',)
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'responsavel', 'convocacao')
        }),
        ('Datas e Horários', {
            'fields': ('data', 'hora_inicio', 'hora_fim')
        }),
        ('Localização', {
            'fields': ('local',)
        }),
        ('Participantes', {
            'fields': ('participantes',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )

@admin.register(PresencaAcademica)
class PresencaAcademicaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'turma', 'atividade', 'data', 'presente', 'registrado_por')
    list_filter = ('presente', 'turma', 'atividade', 'data')
    search_fields = ('aluno__nome', 'aluno__cpf', 'turma__nome', 'atividade__nome')
    date_hierarchy = 'data'

@admin.register(PresencaRitualistica)
class PresencaRitualisticaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'turma', 'atividade', 'data', 'presente', 'registrado_por')
    list_filter = ('presente', 'turma', 'atividade', 'data')
    search_fields = ('aluno__nome', 'aluno__cpf', 'turma__nome', 'atividade__nome')
    date_hierarchy = 'data'

@admin.register(ObservacaoPresenca)
class ObservacaoPresencaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'turma', 'data', 'atividade_academica', 'atividade_ritualistica', 'registrado_por')
    list_filter = ('turma', 'data', 'atividade_academica', 'atividade_ritualistica')
    search_fields = ('aluno__nome', 'aluno__cpf', 'turma__nome')
    date_hierarchy = 'data'