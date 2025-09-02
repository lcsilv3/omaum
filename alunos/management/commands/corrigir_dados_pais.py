"""
Comando de gerenciamento para corrigir o campo 'nacionalidade' no modelo Pais.
"""

from django.core.management.base import BaseCommand
from alunos.models import Pais


class Command(BaseCommand):
    help = 'Define a nacionalidade para o país "Brasil" como "Brasileira".'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("--- Iniciando correção de dados do País: Brasil ---")
        )

        try:
            # Busca pelo país "Brasil"
            pais_brasil = Pais.objects.get(nome__iexact="Brasil")

            # Verifica se a correção é necessária
            if (
                pais_brasil.nacionalidade
                and pais_brasil.nacionalidade.lower() == "brasileira"
            ):
                self.stdout.write(
                    self.style.NOTICE(
                        'O país "Brasil" já possui a nacionalidade "Brasileira". Nenhuma ação necessária.'
                    )
                )
            else:
                # Atualiza o campo
                pais_brasil.nacionalidade = "Brasileira"
                pais_brasil.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        'O campo "nacionalidade" do país "Brasil" foi atualizado para "Brasileira".'
                    )
                )

        except Pais.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    'Erro: O país "Brasil" não foi encontrado na tabela de Países. A correção não pôde ser aplicada.'
                )
            )
        except Pais.MultipleObjectsReturned:
            self.stdout.write(
                self.style.ERROR(
                    'Erro: Múltiplos países com o nome "Brasil" foram encontrados. A correção não pôde ser aplicada devido à ambiguidade.'
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ocorreu um erro inesperado: {e}"))

        self.stdout.write(self.style.SUCCESS("--- Correção concluída ---"))
