from django.contrib import admin
from .models import Turma


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = [
        "nome",
        "curso",
        "data_inicio",
        "data_fim",
        "vagas",
        "status",
    ]
    list_filter = ["curso", "status"]
    search_fields = ["nome", "curso__nome"]
