from django.apps import AppConfig
import os


class PagamentosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pagamentos"
    # Remova a linha abaixo ou corrija-a para:
    # path = os.path.dirname(__file__)