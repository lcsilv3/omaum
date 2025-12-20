from turmas.models import Turma
from atividades.models import Atividade

# Buscar turma 2005
turmas = Turma.objects.filter(nome__icontains='2005').order_by('id')
print(f'Turmas encontradas com "2005" no nome: {turmas.count()}')
for t in turmas:
    print(f'  - ID: {t.id}, Nome: {t.nome}')

print()
print('Todas as turmas (primeiras 10):')
todas = Turma.objects.all().order_by('id')[:10]
for t in todas:
    print(f'  - ID: {t.id}, Nome: {t.nome}')
    # Verificar atividades
    atividades = Atividade.objects.filter(turmas=t)
    print(f'    Atividades: {atividades.count()}')
    for ativ in atividades:
        print(f'      - {ativ.nome} ({ativ.get_tipo_atividade_display()})')
