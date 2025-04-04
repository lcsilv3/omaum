from django.contrib import admin
from .models import Frequencia

@admin.register(Frequencia)
class FrequenciaAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'data']  # Remove fields that don't exist
    list_filter = ['data']  # Remove fields that don't exist
    search_fields = ('aluno__nome', 'turma__codigo_turma', 'justificativa')
    date_hierarchy = 'data'
    readonly_fields = []  # Remove fields that don't exist
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('aluno', 'turma', 'data', 'presente')
        }),
        ('Justificativa', {
            'fields': ('justificativa',),
            'classes': ('collapse',),
        }),
        ('Informações de Registro', {
            'fields': ('registrado_por', 'data_registro', 'data_atualizacao'),
            'classes': ('collapse',),
        }),
    )
