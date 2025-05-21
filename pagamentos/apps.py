"""
Configuração do aplicativo de pagamentos.
"""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PagamentosConfig(AppConfig):
    """Configuração do aplicativo de pagamentos."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pagamentos'
    verbose_name = _('Pagamentos')
    
    def ready(self):
        """
        Inicializa o aplicativo quando o Django estiver pronto.
        Importa os signals para garantir que sejam registrados.
        """
        try:
            import pagamentos.signals  # noqa
        except ImportError:
            pass
    # path = os.path.dirname(__file__)