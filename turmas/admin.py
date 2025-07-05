from django.contrib import admin
from importlib import import_module
from django.urls import path
from .actions import desativar_turmas_action, get_desativar_turmas_impacto_view


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
                "ativo",
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
        "ativo",
    )
    list_display_links = ("nome",)
    search_fields = ("nome", "curso__nome")
    list_filter = ("curso", "data_inicio_ativ", "ativo")
    ordering = ("-data_inicio_ativ",)
    actions = [desativar_turmas_action]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'desativar-impacto/',
                self.admin_site.admin_view(
                    get_desativar_turmas_impacto_view(self)
                ),
                name='desativar_turmas_impacto',
            ),
        ]
        return custom_urls + urls

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("curso")
