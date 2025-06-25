from django.contrib import admin
from presencas.models import ObservacaoPresenca

@admin.register(ObservacaoPresenca)
class ObservacaoPresencaAdmin(admin.ModelAdmin):
    list_display = (
        'aluno',
        'turma',
        'data',
        'atividade_academica',
        'atividade_ritualistica',
        'registrado_por'
    )
    list_filter = (
        'turma',
        'data',
        'atividade_academica',
        'atividade_ritualistica'
    )
    search_fields = (
        'aluno__nome',
        'aluno__cpf',
        'turma__nome'
    )
    date_hierarchy = 'data'
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('aluno', 'turma', 'data', 'registrado_por')
        }),
        ('Atividades', {
            'fields': ('atividade_academica', 'atividade_ritualistica')
        }),
        ('Observação', {
            'fields': ('texto',)
        }),
    )