from django.apps import AppConfig


class TurmasConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "turmas"

    def ready(self):
        """
        Importa os signals quando a aplicação está pronta.
        """
        import turmas.signals  # noqa: F401
