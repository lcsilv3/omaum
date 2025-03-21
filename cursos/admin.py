from django.contrib import admin
from .models import Curso

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['nome']  # Ajuste conforme os campos do seu modelo
    search_fields = ('nome',)
