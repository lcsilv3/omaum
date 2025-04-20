from django.apps import AppConfig
import os


class MatriculasConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "matriculas"
    path = os.path.join(os.path.dirname(__file__), "matriculas")
