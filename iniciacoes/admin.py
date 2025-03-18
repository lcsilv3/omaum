from django.contrib import admin
from .models import Iniciacao

@admin.register(Iniciacao)
class IniciacaoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'nome_curso', 'data_iniciacao')
    list_filter = ('nome_curso', 'data_iniciacao')
    search_fields = ('aluno__nome', 'nome_curso')
