"""
Configuração do admin para o aplicativo de pagamentos.
"""

from django.contrib import admin
from .models import Pagamento


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    """Configuração do admin para o modelo Pagamento."""

    list_display = ("aluno", "valor", "status", "data_vencimento", "data_pagamento")
    search_fields = ("aluno__nome", "aluno__cpf", "status")
    list_filter = ("status", "data_vencimento")

    fieldsets = [
        (
            "Informações Básicas",
            {
                "fields": [
                    "aluno",
                    "valor",
                    "data_vencimento",
                    "status",
                ]
            },
        ),
        (
            "Informações de Pagamento",
            {
                "fields": [
                    "data_pagamento",
                    "valor_pago",
                    "metodo_pagamento",
                ],
                "classes": ["collapse"],
            },
        ),
        (
            "Observações",
            {
                "fields": ["observacoes"],
                "classes": ["collapse"],
            },
        ),
    ]

    def get_queryset(self, request):
        """Otimiza as consultas ao banco de dados."""
        return super().get_queryset(request).select_related("aluno")
