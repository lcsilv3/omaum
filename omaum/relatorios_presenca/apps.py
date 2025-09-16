"""
Configuração do app relatorios_presenca.
"""

from django.apps import AppConfig


class RelatoriosPresencaConfig(AppConfig):
    """Configuração do aplicativo de relatórios de presença."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "omaum.relatorios_presenca"
    verbose_name = "Relatórios de Presença e Frequência"

    def ready(self):
        """Executado quando o app está pronto."""
        # Importar signals se necessário
        pass
