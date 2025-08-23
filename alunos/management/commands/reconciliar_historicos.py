from django.core.management.base import BaseCommand
from django.db import transaction
from alunos.models import Aluno
from alunos.services import reconciliar_historico_if_divergente


class Command(BaseCommand):
    help = "Reconcilia historico_iniciatico JSON a partir de RegistroHistorico quando divergente."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apenas", nargs="*", type=str, help="Lista de CPFs a processar (opcional)"
        )
        parser.add_argument(
            "--dry-run", action="store_true", help="Não persiste alterações, só relata"
        )

    def handle(self, *args, **options):  # noqa: D401
        cpfs = options.get("apenas") or []
        dry = options.get("dry_run")
        qs = Aluno.objects.all()
        if cpfs:
            qs = qs.filter(cpf__in=cpfs)
        total = qs.count()
        corrigidos = 0
        self.stdout.write(f"Processando {total} alunos (dry-run={dry})...")
        for aluno in qs.iterator():
            historico_antes = list(aluno.historico_iniciatico) if isinstance(aluno.historico_iniciatico, list) else []
            with transaction.atomic():
                novo = reconciliar_historico_if_divergente(aluno)
                if novo != historico_antes:
                    corrigidos += 1
                    if dry:
                        transaction.set_rollback(True)
        self.stdout.write(self.style.SUCCESS(f"Concluído. Corrigidos: {corrigidos}"))
