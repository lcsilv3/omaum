from django.contrib import admin
from .models import Presenca


@admin.register(Presenca)
class PresencaAdmin(admin.ModelAdmin):
    list_display = ("aluno", "turma", "data", "status")
    search_fields = ("aluno__nome", "turma__nome")
    list_filter = ("turma", "data", "status")
    ordering = ("-data",)
