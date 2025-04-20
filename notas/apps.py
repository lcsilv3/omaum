from django.apps import AppConfig
import os


class NotasConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notas"
    path = os.path.join(os.path.dirname(__file__), "notas")
