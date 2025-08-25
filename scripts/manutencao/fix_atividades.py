import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from atividades.models import Atividade

print("🔍 Verificando atividades que precisam de correção...")

# Buscar atividades sem curso
atividades_sem_curso = Atividade.objects.filter(curso__isnull=True)
print(f"📊 Encontradas {atividades_sem_curso.count()} atividades sem curso")

# Corrigir uma por uma
corrigidas = 0
for atividade in atividades_sem_curso:
    print(f"📝 Processando atividade: {atividade.nome}")
    
    turmas = atividade.turmas.all()
    if turmas.exists():
        primeira_turma = turmas.first()
        if primeira_turma and primeira_turma.curso:
            print(f"   🔧 Corrigindo: curso = {primeira_turma.curso.nome}")
            atividade.curso = primeira_turma.curso
            atividade.save()
            corrigidas += 1
        else:
            print(f"   ❌ Turma sem curso: {primeira_turma}")
    else:
        print(f"   ❌ Atividade sem turmas")

print(f"✅ Correção concluída! {corrigidas} atividades foram corrigidas.")

# Verificar resultado
atividades_corrigidas = Atividade.objects.exclude(curso__isnull=True)
print(f"📈 Total de atividades com curso: {atividades_corrigidas.count()}")
