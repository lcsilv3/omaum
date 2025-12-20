from alunos.models import Aluno
from turmas.models import Turma

print("="*80)
print("VERIFICAÇÃO DE DADOS PARA MATRÍCULA")
print("="*80)

alunos_ativos = Aluno.objects.filter(situacao='a')
print(f"\nTotal de alunos ativos (situacao='a'): {alunos_ativos.count()}")

if alunos_ativos.exists():
    print("\nPrimeiros 5 alunos ativos:")
    for aluno in alunos_ativos[:5]:
        print(f"  - ID {aluno.id}: {aluno.nome} (situação={aluno.situacao})")
else:
    print("\n⚠ ATENÇÃO: Nenhum aluno ativo encontrado!")

turmas_ativas = Turma.objects.filter(ativo=True)
print(f"\nTotal de turmas ativas: {turmas_ativas.count()}")

if turmas_ativas.exists():
    print("\nPrimeiras 5 turmas ativas:")
    for turma in turmas_ativas[:5]:
        print(f"  - ID {turma.id}: {turma.nome} (ativo={turma.ativo})")

from django.db.models import Count
situacoes = Aluno.objects.values('situacao').annotate(total=Count('id')).order_by('-total')
print("\nDistribuição de alunos por situação:")
for s in situacoes:
    situacao_label = dict(Aluno.SITUACAO_CHOICES).get(s['situacao'], 'Desconhecida')
    print(f"  Situação '{s['situacao']}' ({situacao_label}): {s['total']} alunos")
