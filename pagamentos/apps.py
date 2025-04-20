from django.apps import AppConfig
import os


class PagamentosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pagamentos"
    path = os.path.join(os.path.dirname(__file__), "pagamentos")
