from django.contrib import admin
from .models import Aluno

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    # Remova 'telefone' se esse campo não existir no modelo Aluno
    # list_display = ['nome', 'email', 'telefone']  # Linha com erro
    
    # Use apenas campos que existem no modelo
    list_display = ['nome', 'email']  # Ajuste conforme os campos reais do seu modelo
    search_fields = ['nome', 'email']
