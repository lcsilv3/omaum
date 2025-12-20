"""
Management command para verificar dados disponíveis para matrícula.
"""

from django.core.management.base import BaseCommand
from django.db.models import Count
from alunos.models import Aluno
from turmas.models import Turma


class Command(BaseCommand):
    help = "Verifica alunos e turmas disponíveis para matrícula"

    def handle(self, *args, **options):
        self.stdout.write("=" * 80)
        self.stdout.write(self.style.SUCCESS("VERIFICAÇÃO DE DADOS PARA MATRÍCULA"))
        self.stdout.write("=" * 80)

        # Verificar alunos ativos
        alunos_ativos = Aluno.objects.filter(situacao='a')
        self.stdout.write(f"\n✓ Total de alunos ativos (situacao='a'): {alunos_ativos.count()}")

        if alunos_ativos.exists():
            self.stdout.write("\nPrimeiros 5 alunos ativos:")
            for aluno in alunos_ativos[:5]:
                self.stdout.write(f"  - ID {aluno.id}: {aluno.nome} (situação={aluno.situacao})")
        else:
            self.stdout.write(self.style.WARNING("\n⚠ ATENÇÃO: Nenhum aluno ativo encontrado!"))

        # Verificar turmas ativas
        turmas_ativas = Turma.objects.filter(ativo=True)
        self.stdout.write(f"\n✓ Total de turmas ativas: {turmas_ativas.count()}")

        if turmas_ativas.exists():
            self.stdout.write("\nPrimeiras 5 turmas ativas:")
            for turma in turmas_ativas[:5]:
                self.stdout.write(f"  - ID {turma.id}: {turma.nome} (ativo={turma.ativo})")
        else:
            self.stdout.write(self.style.WARNING("\n⚠ ATENÇÃO: Nenhuma turma ativa encontrada!"))

        # Distribuição de alunos por situação
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("DISTRIBUIÇÃO DE ALUNOS POR SITUAÇÃO:")
        self.stdout.write("=" * 80)
        
        situacoes = Aluno.objects.values('situacao').annotate(total=Count('id')).order_by('-total')
        for s in situacoes:
            situacao_label = dict(Aluno.SITUACAO_CHOICES).get(s['situacao'], 'Desconhecida')
            self.stdout.write(f"  Situação '{s['situacao']}' ({situacao_label}): {s['total']} alunos")

        self.stdout.write("\n" + "=" * 80)
