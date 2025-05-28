from django.contrib import admin
from .models import AtividadeAcademica, AtividadeRitualistica

@admin.register(AtividadeAcademica)
class AtividadeAcademicaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_atividade', 'data_inicio', 'data_fim', 
                    'status', 'curso')
    list_filter = ('status', 'tipo_atividade', 'curso')
    search_fields = ('nome', 'descricao')
    date_hierarchy = 'data_inicio'
    filter_horizontal = ('turmas',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'tipo_atividade', 'responsavel')
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
    list_display = ('nome', 'data', 'hora_inicio', 'status')
    list_filter = ('status',)
    search_fields = ('nome', 'descricao')
    date_hierarchy = 'data'
    filter_horizontal = ('participantes',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'responsavel')
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