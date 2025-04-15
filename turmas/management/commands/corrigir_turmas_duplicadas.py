from django.core.management.base import BaseCommand
from turmas.models import Turma


class Command(BaseCommand):
    help = "Corrige turmas duplicadas com diferenças apenas na capitalização"

    def handle(self, *args, **options):
        # Encontrar nomes de turmas que existem em diferentes capitalizações
        nomes_turmas = Turma.objects.values_list("nome", flat=True)
        nomes_lower = [nome.lower() for nome in nomes_turmas]

        # Contar ocorrências de cada nome (em lowercase)
        duplicados = {}
        for nome in nomes_lower:
            if nome in duplicados:
                duplicados[nome] += 1
            else:
                duplicados[nome] = 1

        # Filtrar apenas os nomes que aparecem mais de uma vez
        nomes_duplicados = [
            nome for nome, count in duplicados.items() if count > 1
        ]

        self.stdout.write(
            f"Encontradas {len(nomes_duplicados)} turmas com nomes duplicados."
        )

        # Para cada nome duplicado, manter apenas uma turma e excluir as outras
        for nome_lower in nomes_duplicados:
            turmas = Turma.objects.filter(nome__iexact=nome_lower).order_by(
                "id"
            )

            if turmas.count() > 1:
                # Manter a primeira turma (geralmente a mais antiga)
                turma_principal = turmas.first()
                self.stdout.write(
                    f"Mantendo turma '{turma_principal.nome}' (ID: {turma_principal.id})"
                )

                # Excluir as outras turmas
                for turma in turmas[1:]:
                    self.stdout.write(
                        f"Excluindo turma duplicada '{turma.nome}' (ID: {turma.id})"
                    )
                    turma.delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Correção de turmas duplicadas concluída com sucesso!"
            )
        )
