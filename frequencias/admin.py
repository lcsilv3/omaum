from django.contrib import admin
from .models import Frequencia

@admin.register(Frequencia)
class FrequenciaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'turma', 'data', 'presente', 'registrado_por', 'data_registro')
    list_filter = ('presente', 'data', 'turma', 'registrado_por')
    search_fields = ('aluno__nome', 'turma__codigo_turma', 'justificativa')
    date_hierarchy = 'data'
    readonly_fields = ('data_registro', 'data_atualizacao')
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
