import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from presencas.models import RegistroPresenca
from django.db.models import Count, Q

registros = RegistroPresenca.objects.filter(
    turma_id=32,
    data__year=2025,
    data__month=12
).select_related('aluno', 'atividade')

print(f"Total de registros: {registros.count()}")
print("\nDetalhes por dia:")
for registro in registros.order_by('data', 'aluno__nome'):
    status = "Presente" if registro.presente else "Ausente"
    print(f"  {registro.data.strftime('%d/%m')} - {registro.atividade.nome:20s} - {registro.aluno.nome:30s} - {status}")

print("\n\nResumo por Atividade e Dia:")
resumo = registros.values('data', 'atividade__nome').annotate(
    total=Count('id'),
    presentes=Count('id', filter=Q(presente=True))
).order_by('data', 'atividade__nome')

for item in resumo:
    data = item['data'].strftime('%d/%m/%Y')
    atividade = item['atividade__nome']
    total = item['total']
    presentes = item['presentes']
    ausentes = total - presentes
    print(f"  {data} - {atividade:20s} - {presentes} presentes, {ausentes} ausentes (total: {total})")
