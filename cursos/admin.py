from django.contrib import admin
from .models import Curso

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'duracao', 'descricao')  # Make sure 'duracao' is included only if it exists in the model
    search_fields = ('nome',)
