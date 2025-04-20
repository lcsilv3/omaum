from django.apps import AppConfig
import os


class FrequenciasConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "frequencias"
    path = os.path.dirname(os.path.abspath(__file__))
