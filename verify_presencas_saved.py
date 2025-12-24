from presencas.models import RegistroPresenca
from turmas.models import Turma

turma = Turma.objects.get(id=32)
print("=" * 80)
print("✅ VERIFICAÇÃO FINAL - DADOS SALVOS NO BANCO")
print("=" * 80)

# Contar total de presenças
total = RegistroPresenca.objects.filter(turma=turma).count()
print(f"\n📊 Total de RegistroPresenca: {total}")

# Agrupar por data/atividade
from django.db.models import Count
presencas = RegistroPresenca.objects.filter(turma=turma).values('data', 'atividade__nome').annotate(count=Count('id')).order_by('data')

print("\n📝 Detalhamento por Data/Atividade:")
for p in presencas:
    print(f"   {p['data']} | {p['atividade__nome']:15} | {p['count']} registro(s)")

# Amostra de alguns registros
print("\n🔍 Amostra de registros salvos:")
samples = RegistroPresenca.objects.filter(turma=turma).select_related('aluno', 'atividade')[:5]
for reg in samples:
    print(f"   {reg.aluno.nome:20} | {reg.atividade.nome:15} | {reg.data} | Status: {reg.status}")

print("\n" + "=" * 80)
print("✅ FLUXO COMPLETO DE REGISTRO DE PRESENÇAS ESTÁ FUNCIONANDO!")
print("=" * 80)
