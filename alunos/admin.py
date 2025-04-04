from django.contrib import admin
from .models import Aluno

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'numero_iniciatico', 'email', 'cpf', 'sexo']
    search_fields = ['nome', 'numero_iniciatico', 'email', 'cpf']
    list_filter = ['sexo', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        ('Dados Pessoais', {
            'fields': ['cpf', 'nome', 'data_nascimento', 'hora_nascimento', 'email', 'foto', 'sexo']
        }),
        ('Dados Iniciáticos', {
            'fields': ['numero_iniciatico', 'nome_iniciatico']
        }),
        ('Nacionalidade e Naturalidade', {
            'fields': ['nacionalidade', 'naturalidade']
        }),
        ('Endereço', {
            'fields': ['rua', 'numero_imovel', 'complemento', 'bairro', 'cidade', 'estado', 'cep']
        }),
        ('Contatos de Emergência', {
            'fields': [
                'nome_primeiro_contato', 'celular_primeiro_contato', 'tipo_relacionamento_primeiro_contato',
                'nome_segundo_contato', 'celular_segundo_contato', 'tipo_relacionamento_segundo_contato'
            ]
        }),
        ('Informações Médicas', {
            'fields': [
                'tipo_sanguineo', 'fator_rh', 'alergias', 'condicoes_medicas_gerais', 
                'convenio_medico', 'hospital'
            ]
        }),
        ('Metadados', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
