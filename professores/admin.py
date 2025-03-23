from django.contrib import admin
from .models import Professor

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'especialidade', 'ativo', 'data_cadastro')
    list_filter = ('ativo', 'especialidade', 'data_cadastro')
    search_fields = ('nome', 'email', 'especialidade')
    list_editable = ('ativo',)
    readonly_fields = ('data_cadastro',)
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'email', 'telefone')
        }),
        ('Informações Profissionais', {
            'fields': ('especialidade', 'ativo', 'observacoes')
        }),
        ('Informações do Sistema', {
            'fields': ('data_cadastro',),
            'classes': ('collapse',)
        }),
    )
