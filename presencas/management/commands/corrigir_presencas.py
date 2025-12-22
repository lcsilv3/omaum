"""Comando para corrigir inconsistências no módulo de presenças."""

from django.core.management.base import BaseCommand
from django.db import transaction
from presencas.models import RegistroPresenca


class Command(BaseCommand):
    """Comando para corrigir presenças com dados inconsistentes."""

    help = "Corrige registros de presença com dados inconsistentes (turmas, atividades, etc.)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Executa sem salvar alterações, apenas mostra o que seria feito",
        )

    def handle(self, *args, **options):
        """Executa a correção."""
        dry_run = options["dry_run"]

        if dry_run:
            self.stdout.write("🔍 Modo DRY-RUN: Nenhuma alteração será salva")

        self.stdout.write("🔍 Verificando registros de presença que precisam de correção...")

        with transaction.atomic():
            # 1. Corrigir registros de presença sem turma quando há atividade
            self.stdout.write("\n📋 Verificando registros de presença sem turma...")
            presencas_sem_turma = RegistroPresenca.objects.filter(
                turma__isnull=True, atividade__isnull=False
            ).select_related("atividade")

            corrigidas_turma = 0
            for presenca in presencas_sem_turma:
                if (
                    hasattr(presenca.atividade, "turmas")
                    and presenca.atividade.turmas.exists()
                ):
                    primeira_turma = presenca.atividade.turmas.first()

                    self.stdout.write(
                        f"  → RegistroPresenca ID {presenca.id} receberá turma: {primeira_turma.nome}"
                    )

                    if not dry_run:
                        presenca.turma = primeira_turma
                        presenca.save()

                    corrigidas_turma += 1

            if dry_run:
                # Rollback no dry-run
                transaction.set_rollback(True)

        # Estatísticas finais
        total_presencas = RegistroPresenca.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ {'Simulação concluída' if dry_run else 'Correção concluída'}!"
            )
        )
        self.stdout.write("📊 Estatísticas:")
        self.stdout.write(f"   • Total de registros de presença: {total_presencas}")
        self.stdout.write(f"   • Registros corrigidos (turmas): {corrigidas_turma}")

        if dry_run:
            self.stdout.write("\n💡 Execute sem --dry-run para aplicar as correções")
