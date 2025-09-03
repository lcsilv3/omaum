from django.contrib import admin
from .models import FrequenciaMensal, Carencia


class CarenciaInline(admin.TabularInline):
    model = Carencia
    extra = 0
    readonly_fields = [
        "aluno",
        "total_presencas",
        "total_atividades",
        "percentual_presenca",
        "numero_carencias",
    ]
    fields = [
        "aluno",
        "total_presencas",
        "total_atividades",
        "percentual_presenca",
        "numero_carencias",
        "liberado",
        "observacoes",
    ]
    can_delete = False


class FrequenciaMensalAdmin(admin.ModelAdmin):
    list_display = ("turma", "mes", "ano", "percentual_minimo", "created_at")
    list_filter = ("turma", "mes", "ano")
    search_fields = ("turma__nome",)
    date_hierarchy = "created_at"
    readonly_fields = ["created_at", "updated_at"]
    inlines = [CarenciaInline]
    actions = ["recalcular_carencias"]

    def alunos_com_carencia(self, obj):
        """Retorna o número de alunos com carência."""
        return obj.carencia_set.filter(liberado=False).count()

    alunos_com_carencia.short_description = "Alunos com Carência"

    def recalcular_carencias(self, request, queryset):
        """Recalcula as carências para as frequências selecionadas."""
        for frequencia in queryset:
            frequencia.calcular_carencias()
        self.message_user(
            request, f"Carências recalculadas para {queryset.count()} frequências."
        )

    recalcular_carencias.short_description = "Recalcular carências"


class CarenciaAdmin(admin.ModelAdmin):
    # Atualizando list_display para incluir o campo status
    list_display = (
        "aluno",
        "frequencia_mensal",
        "percentual_presenca",
        "numero_carencias",
        "liberado",
        "status",
    )

    # Atualizando list_filter para incluir o campo status
    list_filter = ("liberado", "status", "frequencia_mensal__turma")
    search_fields = ("aluno__nome", "aluno__cpf")
    date_hierarchy = "created_at"
    readonly_fields = [
        "frequencia_mensal",
        "aluno",
        "total_presencas",
        "total_atividades",
        "percentual_presenca",
        "numero_carencias",
    ]
    fieldsets = [
        (
            "Informações da Carência",
            {
                "fields": [
                    "frequencia_mensal",
                    "aluno",
                    "total_presencas",
                    "total_atividades",
                    "percentual_presenca",
                    "numero_carencias",
                ]
            },
        ),
        (
            "Status e Resolução",
            {
                "fields": [
                    "liberado",
                    "status",
                    "observacoes",
                    "data_identificacao",
                    "data_acompanhamento",
                    "acompanhado_por",
                    "data_resolucao",
                    "resolvido_por",
                    "motivo_resolucao",
                    "observacoes_resolucao",
                ]
            },
        ),
    ]


admin.site.register(FrequenciaMensal, FrequenciaMensalAdmin)
admin.site.register(Carencia, CarenciaAdmin)
