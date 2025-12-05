import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


def _obter_credenciais_padrao():
    """Retorna credenciais padrão conforme o ambiente atual."""
    settings_module = os.getenv("DJANGO_SETTINGS_MODULE", "")
    if settings_module.endswith("production"):
        return ("admin", "admin@omaum.org", "admin123")
    if settings_module.endswith("development"):
        return ("desenv", "desenv@omaum.org", "desenv123")
    return ("admin", "admin@omaum.org", "admin123")


class Command(BaseCommand):
    """
    Cria um superusuário se nenhum existir.
    Ideal para ser usado em scripts de deploy/inicialização.
    """

    help = "Cria um superusuário se nenhum usuário (ou superusuário) existir no banco de dados."

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.SUCCESS("Superusuário já existe. Nenhuma ação necessária.")  # type: ignore[attr-defined]
            )
            return

        username, email, password = _obter_credenciais_padrao()
        username = os.getenv("SUPERUSER_USERNAME", username)
        email = os.getenv("SUPERUSER_EMAIL", email)
        password = os.getenv("SUPERUSER_PASSWORD", password)

        self.stdout.write("Nenhum superusuário encontrado. Criando um novo.")
        User.objects.create_superuser(username, email, password)
        self.stdout.write(
            self.style.SUCCESS(f'Superusuário "{username}" criado com sucesso.')  # type: ignore[attr-defined]
        )
