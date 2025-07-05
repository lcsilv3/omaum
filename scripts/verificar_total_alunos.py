
import os
import django
import sys

# Adiciona o caminho do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configura o ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from alunos.models import Aluno

def verificar_total_alunos():
    """
    Verifica e imprime o número total de alunos no banco de dados.
    """
    try:
        total_alunos = Aluno.objects.count()
        print(f"Total de alunos no banco de dados: {total_alunos}")
    except Exception as e:
        print(f"Ocorreu um erro ao verificar o total de alunos: {e}")

if __name__ == "__main__":
    verificar_total_alunos()
