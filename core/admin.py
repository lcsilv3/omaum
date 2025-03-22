from django.contrib import admin
from .models import Aluno, Categoria, Item

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'data_nascimento', 'ativo')
    search_fields = ('nome', 'email', 'telefone')
    list_filter = ('ativo', 'data_cadastro')
    list_editable = ('ativo',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'data_criacao')
    search_fields = ('nome',)
    list_filter = ('data_criacao',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'disponivel', 'data_criacao')
    list_filter = ('categoria', 'disponivel', 'data_criacao')
    search_fields = ('nome', 'descricao')
    list_editable = ('preco', 'disponivel')
