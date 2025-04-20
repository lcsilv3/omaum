from django.contrib import admin
from importlib import import_module


# Função para obter o modelo Pagamento dinamicamente
def get_pagamento_model():
    pagamentos_module = import_module("pagamentos.models")
    return getattr(pagamentos_module, "Pagamento")


# Registrar o modelo Pagamento no admin
Pagamento = get_pagamento_model()


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ("aluno", "valor", "data_pagamento", "status")
    search_fields = ("aluno__nome", "status")
    list_filter = ("status", "data_pagamento")
    ordering = ("-data_pagamento",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("aluno")
