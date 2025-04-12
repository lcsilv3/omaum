import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

# Import your models
from cursos.models import Curso
from alunos.models import Aluno
from turmas.models import Turma
# Import other models as needed

# Create sample data
def populate():
    # Create courses
    curso1 = Curso.objects.create(
        codigo_curso="CS101",
        nome="Introdução à Computação",
        descricao="Curso básico de computação",
        duracao=6
    )
    
    # Create students
    aluno1 = Aluno.objects.create(
        nome="João Silva",
        matricula="2023001",
        curso=curso1
        # Add other fields as needed
    )
    
    # Create classes
    turma1 = Turma.objects.create(
        nome="Turma A - 2023",
        curso=curso1,
        # Add other fields as needed
    )
    
    print("Database populated successfully!")

if __name__ == '__main__':
    print("Starting population script...")
    populate()
