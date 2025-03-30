# Código da Funcionalidade: root
*Gerado automaticamente*



## alunostests__init__.py

python
# Alunos app




## clean_migrations.py

python
import os
import shutil
import datetime

def backup_database():
    """Create a backup of the database file if it exists"""
    if os.path.exists('db.sqlite3'):
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'db_backup_{timestamp}.sqlite3')
        
        shutil.copy2('db.sqlite3', backup_file)
        print(f"Database backed up to {backup_file}")
    else:
        print("No database file found to backup")

def delete_migrations():
    """Delete all migration files except __init__.py"""
    # Get all directories in the current folder
    dirs = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.') and d != 'venv' and d != 'backups']
    
    migration_files_deleted = 0
    
    for app_dir in dirs:
        migrations_dir = os.path.join(app_dir, 'migrations')
        if os.path.exists(migrations_dir):
            print(f"Checking migrations in {app_dir}...")
            
            # Get all Python files in the migrations directory
            migration_files = [f for f in os.listdir(migrations_dir) 
                              if f.endswith('.py') and f != '__init__.py']
            
            # Delete each migration file
            for migration_file in migration_files:
                file_path = os.path.join(migrations_dir, migration_file)
                os.remove(file_path)
                print(f"  Deleted: {file_path}")
                migration_files_deleted += 1
                
            # Make sure __init__.py exists
            init_file = os.path.join(migrations_dir, '__init__.py')
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    pass  # Create an empty file
                print(f"  Created: {init_file}")
    
    return migration_files_deleted

def delete_database():
    """Delete the SQLite database file"""
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print("Database file deleted: db.sqlite3")
        return True
    else:
        print("No database file found to delete")
        return False

def main():
    print("Django Migration Cleaner")
    print("=======================")
    
    # Ask for confirmation
    confirm = input("This will delete all migration files and the database. Continue? (y/n): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return
    
    # Ask about backup
    backup = input("Create a backup of the database before deleting? (y/n): ")
    if backup.lower() == 'y':
        backup_database()
    
    # Delete migrations
    migration_count = delete_migrations()
    print(f"Deleted {migration_count} migration files")
    
    # Delete database
    db_deleted = delete_database()
    
    print("\nCleanup complete!")
    print("Next steps:")
    print("1. Run: python manage.py makemigrations")
    print("2. Run: python manage.py migrate")
    print("3. Run: python manage.py createsuperuser")
    print("4. Run: python popular_alunos.py (if you want sample data)")

if __name__ == "__main__":
    main()





## manage.py

python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()





## popular_alunos.py

python
import os
import django
from datetime import time
import random

# Django configuration
os.environ['DJANGO_SETTINGS_MODULE'] = 'omaum.settings'
django.setup()

from faker import Faker
from alunos.models import Aluno

# Initialize Faker with Brazilian locale
fake = Faker('pt_BR')

def criar_alunos_ficticios(quantidade=50):
    for _ in range(quantidade):
        # Generate random time for hora_nascimento
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        hora_nascimento = time(hour=random_hour, minute=random_minute)

        Aluno.objects.create(
            cpf=fake.unique.numerify('###########'),
            nome=fake.name(),
            data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=65),
            hora_nascimento=hora_nascimento,  # Add this field
            email=fake.unique.email(),
            foto=None,
            numero_iniciatico=fake.unique.numerify('######'),
            nome_iniciatico=fake.name(),
            sexo=fake.random_element(elements=('M', 'F', 'O')),
            nacionalidade='Brasileira',
            naturalidade=fake.city(),
            rua=fake.street_name(),
            numero_imovel=fake.building_number(),
            complemento=fake.random_element(elements=['Apto 101', 'Casa 1', 'Bloco A', 'Fundos']),  # Brazilian-style complements
            cidade=fake.city(),
            estado=fake.estado_sigla(),
            bairro=fake.bairro(),
            cep=fake.postcode(),
            nome_primeiro_contato=fake.name(),
            celular_primeiro_contato=fake.cellphone_number(),
            tipo_relacionamento_primeiro_contato=fake.random_element(elements=('Pai', 'Mãe', 'Irmão', 'Amigo')),
            nome_segundo_contato=fake.name(),
            celular_segundo_contato=fake.cellphone_number(),
            tipo_relacionamento_segundo_contato=fake.random_element(elements=('Pai', 'Mãe', 'Irmão', 'Amigo')),
            tipo_sanguineo=fake.random_element(elements=('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
            fator_rh=fake.random_element(elements=('+', '-')),
            alergias=fake.text(max_nb_chars=200),
            condicoes_medicas_gerais=fake.text(max_nb_chars=200),
            convenio_medico=fake.company(),
            hospital=fake.company()
        )
    print(f"{quantidade} alunos fictícios criados com sucesso!")

if __name__ == '__main__':
    criar_alunos_ficticios()




## populate_db.py

python
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



