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
    fieldsets = (
        ("Informações Básicas", {
            "fields": ("nome", "curso", "descricao", "data_inicio_ativ", "data_termino_atividades")
        }),
        ("Dados Iniciáticos", {
            "fields": (
                "num_livro",
                "perc_carencia",
                "data_iniciacao",
                "data_prim_aula",
            )
        }),
    )
    list_display = (
        "nome",
        "curso",
        "data_inicio_ativ",
        "data_termino_atividades",
        "vagas",
        "status",
    )
    list_display_links = ("nome",)
    search_fields = ("nome", "curso__nome")
    list_filter = ("curso", "data_inicio_ativ")
    ordering = ("-data_inicio_ativ",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("curso")
