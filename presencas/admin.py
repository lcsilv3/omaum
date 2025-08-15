from django.contrib import admin
from presencas.models import ObservacaoPresenca, ConvocacaoPresenca


@admin.register(ConvocacaoPresenca)
class ConvocacaoPresencaAdmin(admin.ModelAdmin):
    list_display = (
        "aluno",
        "turma",
        "atividade",
        "data",
        "convocado",
        "registrado_por",
        "data_registro",
    )
    list_filter = ("turma", "atividade", "data", "convocado")
    search_fields = ("aluno__nome", "aluno__cpf", "turma__nome", "atividade__nome")
    date_hierarchy = "data"
    ordering = ("-data", "aluno__nome")


@admin.register(ObservacaoPresenca)
class ObservacaoPresencaAdmin(admin.ModelAdmin):
    list_display = ("aluno", "turma", "data", "atividade", "registrado_por")
    list_filter = ("turma", "data", "atividade")
    search_fields = ("aluno__nome", "aluno__cpf", "turma__nome")
    date_hierarchy = "data"
    fieldsets = (
        (
            "Informações Básicas",
            {"fields": ("aluno", "turma", "data", "registrado_por")},
        ),
        ("Atividade", {"fields": ("atividade",)}),
        ("Observação", {"fields": ("texto",)}),
    )
