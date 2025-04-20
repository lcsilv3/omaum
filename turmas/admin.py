from django.contrib import admin
from importlib import import_module


# Função para obter o modelo Turma dinamicamente
def get_turma_model():
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


# Registrar o modelo Turma no admin
Turma = get_turma_model()


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "curso",
        "data_inicio",
        "data_fim",
        "vagas",
        "status",
    )
    list_display_links = ("nome",)
    search_fields = ("nome", "curso__nome")
    list_filter = ("curso", "data_inicio")
    ordering = ("-data_inicio",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("curso_nome")
