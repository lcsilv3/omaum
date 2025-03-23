from django.contrib import admin
from .models import Curso

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['codigo_curso', 'nome', 'duracao']
    search_fields = ('codigo_curso', 'nome')
    list_filter = ('duracao',)
