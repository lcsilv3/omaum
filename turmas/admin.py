from django.contrib import admin
from .models import Turma


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ("nome", "curso", "data_inicio", "data_fim", "status", "capacidade")
    search_fields = ("nome", "curso__nome")
    list_filter = ("status", "curso")
