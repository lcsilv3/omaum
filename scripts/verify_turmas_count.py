import os
import sys
import django

# Configuração do ambiente Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from turmas.models import Turma

try:
    num_turmas = Turma.objects.count()
    print(f"Total de turmas no banco de dados: {num_turmas}")
    turmas = Turma.objects.all()
    if num_turmas > 0:
        print("Nomes das turmas:")
        for turma in turmas:
            print(f"- {turma.nome}")
except Exception as e:
    print(f"Ocorreu um erro ao contar as turmas: {e}")
