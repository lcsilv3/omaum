from django.core.management.base import BaseCommand
from django.db import transaction
from alunos.models import Aluno
from alunos.services import _calcular_checksum, sincronizar_historico_iniciatico


class Command(BaseCommand):
    help = "Verifica integridade dos históricos iniciáticos (checksum) e opcionalmente reconcilia."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reparar",
            action="store_true",
            help="Recalcula e salva checksum para divergências detectadas.",
        )

    def handle(self, *args, **options):
        reparar = options["reparar"]
        divergencias = 0
        total = 0
        for aluno in Aluno.objects.all().only(
            "cpf", "historico_iniciatico", "historico_checksum"
        ):
            total += 1
            eventos = (
                aluno.historico_iniciatico
                if isinstance(aluno.historico_iniciatico, list)
                else []
            )
            recomputado = _calcular_checksum(eventos)
            if recomputado != aluno.historico_checksum:
                divergencias += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"Divergência: {aluno.cpf} checksum_atual={aluno.historico_checksum} recomputado={recomputado}"
                    )
                )
                if reparar:
                    with transaction.atomic():
                        sincronizar_historico_iniciatico(aluno)
                        self.stdout.write(self.style.SUCCESS(f"Reparado: {aluno.cpf}"))
        if divergencias == 0:
            self.stdout.write(self.style.SUCCESS(f"Todos íntegros ({total})."))
        else:
            self.stdout.write(
                self.style.NOTICE(
                    f"{divergencias} divergências em {total} alunos (use --reparar para corrigir)."
                )
            )
