"""
Comando de gerenciamento para criar o registro do país "Brasil" se ele não existir.
"""

from django.core.management.base import BaseCommand
from alunos.models import Pais


class Command(BaseCommand):
    help = 'Cria o registro para o país "Brasil" com a nacionalidade "Brasileira" se não existir.'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                "--- Verificando/Criando registro para o País: Brasil ---"
            )
        )

        # Usa get_or_create para criar o objeto apenas se ele não existir.
        # Isso torna o script seguro para ser executado múltiplas vezes.
        pais, created = Pais.objects.get_or_create(
            nome__iexact="Brasil",
            defaults={"nome": "Brasil", "nacionalidade": "Brasileira"},
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    'O país "Brasil" foi criado com sucesso com a nacionalidade "Brasileira".'
                )
            )
        else:
            # Se o país já existe, garante que a nacionalidade está correta.
            if not pais.nacionalidade or pais.nacionalidade.lower() != "brasileira":
                pais.nacionalidade = "Brasileira"
                pais.save()
                self.stdout.write(
                    self.style.WARNING(
                        'O país "Brasil" já existia e seu campo "nacionalidade" foi corrigido para "Brasileira".'
                    )
                )
            else:
                self.stdout.write(
                    self.style.NOTICE(
                        'O país "Brasil" já existe e seus dados estão corretos. Nenhuma ação necessária.'
                    )
                )

        self.stdout.write(self.style.SUCCESS("--- Operação concluída ---"))
