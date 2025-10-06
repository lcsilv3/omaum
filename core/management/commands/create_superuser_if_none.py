from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


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
                self.style.SUCCESS("Superusuário já existe. Nenhuma ação necessária.")
            )
            return

        username = "admin"
        email = "admin@omaum.org"
        password = "admin123"

        self.stdout.write("Nenhum superusuário encontrado. Criando um novo.")
        User.objects.create_superuser(username, email, password)
        self.stdout.write(
            self.style.SUCCESS(f'Superusuário "{username}" criado com sucesso.')
        )
