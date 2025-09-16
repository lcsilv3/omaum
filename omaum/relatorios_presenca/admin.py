"""
Admin para o app relatorios_presenca.
Configurações administrativas para gerenciar relatórios.
"""

from django.contrib import admin
from .models import (
    ConfiguracaoRelatorio,
    HistoricoRelatorio,
    AgendamentoRelatorio,
    TemplatePersonalizado,
)


@admin.register(ConfiguracaoRelatorio)
class ConfiguracaoRelatorioAdmin(admin.ModelAdmin):
    """Admin para configurações de relatório."""

    list_display = ["nome", "tipo_relatorio", "formato_saida", "ativo", "criado_em"]
    list_filter = ["tipo_relatorio", "formato_saida", "ativo", "criado_em"]
    search_fields = ["nome", "tipo_relatorio"]
    ordering = ["tipo_relatorio", "nome"]

    fieldsets = (
        (
            "Informações Básicas",
            {"fields": ("nome", "tipo_relatorio", "formato_saida")},
        ),
        ("Configurações", {"fields": ("template_excel", "parametros_padrao", "ativo")}),
        ("Metadados", {"fields": ("criado_por",), "classes": ("collapse",)}),
    )

    readonly_fields = ["criado_por"]

    def save_model(self, request, obj, form, change):
        """Salva modelo definindo usuário criador."""
        if not change:  # Novo objeto
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(HistoricoRelatorio)
class HistoricoRelatorioAdmin(admin.ModelAdmin):
    """Admin para histórico de relatórios."""

    list_display = [
        "tipo_relatorio",
        "usuario",
        "status",
        "tamanho_arquivo_formatado",
        "data_geracao",
    ]
    list_filter = ["tipo_relatorio", "status", "data_geracao"]
    search_fields = ["usuario__username", "tipo_relatorio", "nome_arquivo"]
    ordering = ["-data_geracao"]

    fieldsets = (
        (
            "Informações do Relatório",
            {"fields": ("usuario", "tipo_relatorio", "configuracao")},
        ),
        ("Parâmetros", {"fields": ("parametros",), "classes": ("collapse",)}),
        (
            "Arquivo Gerado",
            {"fields": ("arquivo_gerado", "nome_arquivo", "tamanho_arquivo")},
        ),
        ("Status", {"fields": ("status", "mensagem_erro", "tempo_processamento")}),
    )

    readonly_fields = ["data_geracao", "tamanho_arquivo_formatado"]

    def tamanho_arquivo_formatado(self, obj):
        """Retorna tamanho formatado."""
        return obj.tamanho_arquivo_formatado

    tamanho_arquivo_formatado.short_description = "Tamanho"


@admin.register(AgendamentoRelatorio)
class AgendamentoRelatorioAdmin(admin.ModelAdmin):
    """Admin para agendamentos de relatório."""

    list_display = ["nome", "configuracao", "frequencia", "ativo", "proxima_execucao"]
    list_filter = ["frequencia", "ativo", "criado_em"]
    search_fields = ["nome", "configuracao__nome"]
    ordering = ["nome"]

    fieldsets = (
        ("Informações Básicas", {"fields": ("nome", "configuracao", "usuario")}),
        ("Agendamento", {"fields": ("frequencia", "hora_execucao", "ativo")}),
        ("Destinatários", {"fields": ("emails_destino",)}),
        ("Parâmetros", {"fields": ("parametros_fixos",), "classes": ("collapse",)}),
        (
            "Execução",
            {
                "fields": ("proxima_execucao", "ultima_execucao"),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = ["proxima_execucao", "ultima_execucao"]


@admin.register(TemplatePersonalizado)
class TemplatePersonalizadoAdmin(admin.ModelAdmin):
    """Admin para templates personalizados."""

    list_display = ["nome", "tipo_relatorio", "ativo", "criado_em"]
    list_filter = ["tipo_relatorio", "ativo", "criado_em"]
    search_fields = ["nome", "tipo_relatorio"]
    ordering = ["tipo_relatorio", "nome"]

    fieldsets = (
        ("Informações Básicas", {"fields": ("nome", "tipo_relatorio", "descricao")}),
        ("Template", {"fields": ("arquivo_template", "ativo")}),
        ("Metadados", {"fields": ("criado_por",), "classes": ("collapse",)}),
    )

    readonly_fields = ["criado_por"]

    def save_model(self, request, obj, form, change):
        """Salva modelo definindo usuário criador."""
        if not change:  # Novo objeto
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)
