# Código da Funcionalidade: root - Parte 1/1
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
from datetime import time, date, timedelta
import random

# Django configuration
os.environ["DJANGO_SETTINGS_MODULE"] = "omaum.settings"
django.setup()

from faker import Faker
from django.utils import timezone
from alunos.models import Aluno
from cursos.models import Curso
from turmas.models import Turma

# Initialize Faker with Brazilian locale
fake = Faker("pt_BR")

def criar_cursos_teste():
    """Cria cursos de teste para associar aos alunos"""
    cursos_dados = [
        {"codigo_curso": 101, "nome": "Iniciação Básica", "descricao": "Curso introdutório aos princípios da OmAum", "duracao": 3},
        {"codigo_curso": 102, "nome": "Meditação Avançada", "descricao": "Técnicas avançadas de meditação e concentração", "duracao": 6},
        {"codigo_curso": 103, "nome": "Filosofia Oriental", "descricao": "Estudo dos fundamentos filosóficos orientais", "duracao": 12},
        {"codigo_curso": 104, "nome": "Práticas Ritualísticas", "descricao": "Aprendizado e prática de rituais tradicionais", "duracao": 9},
        {"codigo_curso": 105, "nome": "Desenvolvimento Espiritual", "descricao": "Técnicas para desenvolvimento da espiritualidade", "duracao": 18}
    ]
    
    cursos_criados = []
    print("Criando cursos de teste...")
    
    for curso_dados in cursos_dados:
        curso, created = Curso.objects.update_or_create(
            codigo_curso=curso_dados["codigo_curso"],
            defaults=curso_dados
        )
        cursos_criados.append(curso)
        status = "Criado" if created else "Atualizado"
        print(f"  {status}: {curso.codigo_curso} - {curso.nome}")
    
    return cursos_criados

def criar_turmas_teste(cursos):
    """Cria turmas de teste para os cursos"""
    turmas_criadas = []
    print("\nCriando turmas de teste...")
    
    # Criar turmas em diferentes estados (passadas, atuais, futuras)
    hoje = timezone.now().date()
    
    for curso in cursos:
        # Turma passada (concluída)
        inicio_passada = hoje - timedelta(days=365)
        fim_passada = inicio_passada + timedelta(days=curso.duracao * 30)
        
        # Turma atual (em andamento)
        inicio_atual = hoje - timedelta(days=curso.duracao * 15)
        fim_atual = inicio_atual + timedelta(days=curso.duracao * 30)
        
        # Turma futura
        inicio_futura = hoje + timedelta(days=30)
        fim_futura = inicio_futura + timedelta(days=curso.duracao * 30)
        
        turmas_dados = [
            {"nome": f"Turma {curso.nome} - Concluída", "data_inicio": inicio_passada, "data_fim": fim_passada, "vagas": 20},
            {"nome": f"Turma {curso.nome} - Em Andamento", "data_inicio": inicio_atual, "data_fim": fim_atual, "vagas": 15},
            {"nome": f"Turma {curso.nome} - Futura", "data_inicio": inicio_futura, "data_fim": fim_futura, "vagas": 25}
        ]
        
        for turma_dados in turmas_dados:
            try:
                turma, created = Turma.objects.update_or_create(
                    nome=turma_dados["nome"],
                    defaults={
                        "curso": curso,
                        "data_inicio": turma_dados["data_inicio"],
                        "data_fim": turma_dados["data_fim"],
                        "vagas": turma_dados["vagas"]
                    }
                )
                turmas_criadas.append(turma)
                status = "Criada" if created else "Atualizada"
                print(f"  {status}: {turma.nome}")
            except Exception as e:
                print(f"  Erro ao criar turma {turma_dados['nome']}: {str(e)}")
    
    return turmas_criadas

def criar_alunos_ficticios(quantidade=50, cursos=None, turmas=None):
    """Cria alunos fictícios e os associa a cursos e turmas"""
    alunos_criados = 0
    
    print(f"\nIniciando criação de {quantidade} alunos fictícios...")
    
    # Garantir diversidade de dados para testes
    sexos = ["M", "F", "O"]
    tipos_sanguineos = ["A", "B", "AB", "O"]
    fatores_rh = ["+", "-"]
    
    # Criar alguns alunos com características específicas para testes
    alunos_especiais = [
        # Aluno menor de idade
        {"nome": "Aluno Menor de Idade", "data_nascimento": fake.date_of_birth(minimum_age=16, maximum_age=17), "sexo": "M"},
        # Aluno idoso
        {"nome": "Aluno Idoso", "data_nascimento": fake.date_of_birth(minimum_age=65, maximum_age=80), "sexo": "M"},
        # Aluno com necessidades especiais
        {"nome": "Aluno com Necessidades Especiais", "condicoes_medicas_gerais": "Cadeirante, necessita de acessibilidade", "sexo": "M"},
        # Aluna gestante
        {"nome": "Aluna Gestante", "sexo": "F", "condicoes_medicas_gerais": "Gestante de 6 meses, necessita de cuidados especiais"},
        # Aluno estrangeiro
        {"nome": "Aluno Estrangeiro", "nacionalidade": "Portuguesa", "sexo": "M"}
    ]
    
    # Primeiro criar os alunos especiais
    for i, aluno_especial in enumerate(alunos_especiais):
        try:
            # Generate random time for hora_nascimento
            random_hour = random.randint(0, 23)
            random_minute = random.randint(0, 59)
            hora_nascimento = time(hour=random_hour, minute=random_minute)
            
            # Gerar CPF válido (apenas números, 11 dígitos)
            cpf = "".join([str(random.randint(0, 9)) for _ in range(11)])
            
            # Gerar número de celular válido (formato brasileiro)
            celular1 = f"({random.randint(11, 99)}) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            celular2 = f"({random.randint(11, 99)}) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            
            # Valores padrão
            dados_aluno = {
                "cpf": cpf,
                "nome": aluno_especial.get("nome", fake.name()),
                "data_nascimento": aluno_especial.get("data_nascimento", fake.date_of_birth(minimum_age=18, maximum_age=65)),
                "hora_nascimento": hora_nascimento,
                "email": fake.unique.email(),
                "foto": None,
                "numero_iniciatico": fake.unique.numerify("######"),
                "nome_iniciatico": fake.name(),
                "sexo": aluno_especial.get("sexo", fake.random_element(elements=sexos)),
                "nacionalidade": aluno_especial.get("nacionalidade", "Brasileira"),
                "naturalidade": fake.city(),
                "rua": fake.street_name(),
                "numero_imovel": fake.building_number(),
                "complemento": fake.random_element(elements=["Apto 101", "Casa 1", "Bloco A", "Fundos"]),
                "cidade": fake.city(),
                "estado": fake.estado_sigla(),
                "bairro": fake.bairro(),
                "cep": fake.postcode().replace("-", ""),
                "nome_primeiro_contato": fake.name(),
                "celular_primeiro_contato": celular1,
                "tipo_relacionamento_primeiro_contato": fake.random_element(elements=("Pai", "Mãe", "Irmão", "Amigo")),
                "nome_segundo_contato": fake.name(),
                "celular_segundo_contato": celular2,
                "tipo_relacionamento_segundo_contato": fake.random_element(elements=("Pai", "Mãe", "Irmão", "Amigo")),
                "tipo_sanguineo": fake.random_element(elements=tipos_sanguineos),
                "fator_rh": fake.random_element(elements=fatores_rh),
                "alergias": aluno_especial.get("alergias", fake.text(max_nb_chars=200)),
                "condicoes_medicas_gerais": aluno_especial.get("condicoes_medicas_gerais", fake.text(max_nb_chars=200)),
                "convenio_medico": fake.company(),
                "hospital": fake.company()
            }
            
            aluno = Aluno.objects.create(**dados_aluno)
            
            # Associar a um curso, se disponível
            if cursos and len(cursos) > 0:
                curso = cursos[i % len(cursos)]
                # Aqui você associaria o aluno ao curso, dependendo da estrutura do seu modelo
                # Se houver um campo curso no modelo Aluno:
                # aluno.curso = curso
                # aluno.save()
            
            # Associar a uma turma, se disponível
            if turmas and len(turmas) > 0:
                turma = turmas[i % len(turmas)]
                # Aqui você associaria o aluno à turma, dependendo da estrutura do seu modelo
                # Se houver um relacionamento ManyToMany:
                # aluno.turmas.add(turma)
                # Ou se for uma relação direta:
                # aluno.turma = turma
                # aluno.save()
            
            alunos_criados += 1
            print(f"  Criado aluno especial: {aluno.nome}")
                
        except Exception as e:
            print(f"  Erro ao criar aluno especial #{i+1}: {str(e)}")
    
    # Criar o restante dos alunos regulares
    for i in range(quantidade - len(alunos_especiais)):
        try:
            # Generate random time for hora_nascimento
            random_hour = random.randint(0, 23)
            random_minute = random.randint(0, 59)
            hora_nascimento = time(hour=random_hour, minute=random_minute)
            
            # Gerar CPF válido (apenas números, 11 dígitos)
            cpf = "".join([str(random.randint(0, 9)) for _ in range(11)])
            
            # Gerar número de celular válido (formato brasileiro)
            celular1 = f"({random.randint(11, 99)}) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            celular2 = f"({random.randint(11, 99)}) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            
            # Garantir diversidade de dados
            sexo = sexos[i % len(sexos)]
            tipo_sanguineo = tipos_sanguineos[i % len(tipos_sanguineos)]
            fator_rh = fatores_rh[i % len(fatores_rh)]
            
            aluno = Aluno.objects.create(
                cpf=cpf,
                nome=fake.name(),
                data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=65),
                hora_nascimento=hora_nascimento,
                email=fake.unique.email(),
                foto=None,
                numero_iniciatico=fake.unique.numerify("######"),
                nome_iniciatico=fake.name(),
                sexo=sexo,
                nacionalidade="Brasileira",
                naturalidade=fake.city(),
                rua=fake.street_name(),
                numero_imovel=fake.building_number(),
                complemento=fake.random_element(elements=["Apto 101", "Casa 1", "Bloco A", "Fundos"]),
                cidade=fake.city(),
                estado=fake.estado_sigla(),
                bairro=fake.bairro(),
                cep=fake.postcode().replace("-", ""),
                nome_primeiro_contato=fake.name(),
                celular_primeiro_contato=celular1,
                tipo_relacionamento_primeiro_contato=fake.random_element(elements=("Pai", "Mãe", "Irmão", "Amigo")),
                nome_segundo_contato=fake.name(),
                celular_segundo_contato=celular2,
                tipo_relacionamento_segundo_contato=fake.random_element(elements=("Pai", "Mãe", "Irmão", "Amigo")),
                tipo_sanguineo=tipo_sanguineo,
                fator_rh=fator_rh,
                alergias=fake.text(max_nb_chars=200),
                condicoes_medicas_gerais=fake.text(max_nb_chars=200),
                convenio_medico=fake.company(),
                hospital=fake.company()
            )
            
            # Associar a um curso e turma, se disponíveis
            if cursos and len(cursos) > 0:
                curso = cursos[i % len(cursos)]
                # Aqui você associaria o aluno ao curso
            
            if turmas and len(turmas) > 0:
                turma = turmas[i % len(turmas)]
                # Aqui você associaria o aluno à turma
            
            alunos_criados += 1
            
            # Mostrar progresso a cada 10 alunos
            if (i + 1) % 10 == 0 or i == 0:
                print(f"  Criados {i + 1 + len(alunos_especiais)} alunos de {quantidade}...")
                
        except Exception as e:
            print(f"  Erro ao criar aluno #{i+1+len(alunos_especiais)}: {str(e)}")
    
    print(f"\n{alunos_criados} alunos fictícios criados com sucesso!")
    return alunos_criados

def main():
    # Verificar se já existem alunos no banco
    total_alunos = Aluno.objects.count()
    if total_alunos > 0:
        print(f"Já existem {total_alunos} alunos no banco de dados.")
        resposta = input("Deseja criar mais alunos e dados de teste? (s/n): ")
        if resposta.lower() != "s":
            print("Operação cancelada.")
            return
    
    # Criar cursos
    cursos = criar_cursos_teste()
    
    # Criar turmas
    turmas = criar_turmas_teste(cursos)
    
    # Perguntar quantos alunos criar
    try:
        qtd = int(input("Quantos alunos deseja criar? (padrão: 50): ") or "50")
    except ValueError:
        qtd = 50
        print("Valor inválido. Usando o padrão de 50 alunos.")
    
    # Criar alunos e associá-los a cursos e turmas
    criar_alunos_ficticios(qtd, cursos, turmas)
    
    print("\nProcesso de criação de dados de teste concluído!")
    print("Agora você pode testar todas as funcionalidades do sistema com estes dados.")

if __name__ == "__main__":
    main()




## popular_cursos.py

python
import os
import django
import random

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from faker import Faker
from cursos.models import Curso
from django.db import IntegrityError

# Inicializar o Faker com localização brasileira
fake = Faker('pt_BR')

# Lista de possíveis áreas de estudo para gerar nomes de cursos mais realistas
areas_estudo = [
    "Filosofia", "Psicologia", "Meditação", "Yoga", "Astrologia", 
    "Numerologia", "Tarô", "Alquimia", "Metafísica", "Espiritualidade",
    "Terapia", "Cura", "Energias", "Xamanismo", "Rituais",
    "Mantras", "Chakras", "Cristais", "Reiki", "Ayurveda"
]

# Lista de prefixos para os cursos
prefixos = [
    "Introdução a", "Fundamentos de", "Avançado em", "Prática de", 
    "Teoria e Prática de", "Estudos em", "Imersão em", "Workshop de",
    "Especialização em", "Técnicas de", "Princípios de", "Aplicação de",
    "Desenvolvimento de", "Aprofundamento em", "Iniciação em"
]

def limpar_cursos_existentes():
    """Remove todos os cursos existentes para evitar conflitos"""
    try:
        count = Curso.objects.all().delete()[0]
        print(f"Removidos {count} cursos existentes.")
    except Exception as e:
        print(f"Erro ao remover cursos existentes: {e}")

def criar_cursos_para_testes():
    """Cria cursos específicos para cobrir casos de teste"""
    
    # Lista de cursos específicos para testes
    cursos_teste = [
        # Curso com código 101 (usado em test_criar_curso_com_dados_validos)
        {
            'codigo_curso': 101,
            'nome': 'Curso de Teste',
            'descricao': 'Descrição do curso de teste',
            'duracao': 6
        },
        # Curso com código 102 (usado em test_str_representation)
        {
            'codigo_curso': 102,
            'nome': 'Curso de Python',
            'descricao': 'Aprenda Python do zero',
            'duracao': 3
        },
        # Cursos para test_ordering
        {
            'codigo_curso': 103,
            'nome': 'Curso A',
            'descricao': 'Primeiro curso na ordenação',
            'duracao': 6
        },
        {
            'codigo_curso': 104,
            'nome': 'Curso M',
            'descricao': 'Segundo curso na ordenação',
            'duracao': 6
        },
        {
            'codigo_curso': 105,
            'nome': 'Curso Z',
            'descricao': 'Terceiro curso na ordenação',
            'duracao': 6
        },
        # Curso para test_form_valid
        {
            'codigo_curso': 201,
            'nome': 'Curso de Teste para Formulário',
            'descricao': 'Descrição do curso para teste de formulário',
            'duracao': 6
        },
        # Curso para test_editar_curso_view_post_valido
        {
            'codigo_curso': 301,
            'nome': 'Curso de Teste para Edição',
            'descricao': 'Descrição do curso para teste de edição',
            'duracao': 6
        },
        # Curso para test_fluxo_completo_curso
        {
            'codigo_curso': 401,
            'nome': 'Curso de Integração',
            'descricao': 'Descrição do curso de integração',
            'duracao': 8
        },
        # Curso com duração mínima
        {
            'codigo_curso': 501,
            'nome': 'Curso Rápido',
            'descricao': 'Curso com duração mínima',
            'duracao': 1
        },
        # Curso com duração máxima
        {
            'codigo_curso': 502,
            'nome': 'Curso Extenso',
            'descricao': 'Curso com duração máxima',
            'duracao': 24
        },
        # Curso com nome longo
        {
            'codigo_curso': 503,
            'nome': 'Curso com Nome Extremamente Longo para Testar o Limite de Caracteres do Campo Nome do Modelo Curso',
            'descricao': 'Descrição de curso com nome longo',
            'duracao': 12
        },
        # Curso com descrição longa
        {
            'codigo_curso': 504,
            'nome': 'Curso com Descrição Longa',
            'descricao': fake.text(max_nb_chars=1000),  # Descrição longa
            'duracao': 12
        }
    ]
    
    # Criar os cursos de teste
    for curso_data in cursos_teste:
        try:
            curso = Curso.objects.create(**curso_data)
            print(f"Curso de teste criado: {curso.codigo_curso} - {curso.nome} ({curso.duracao} meses)")
        except IntegrityError:
            print(f"Curso com código {curso_data['codigo_curso']} já existe. Pulando.")
        except Exception as e:
            print(f"Erro ao criar curso de teste: {e}")

def criar_cursos_aleatorios(quantidade=8):
    """Cria cursos aleatórios adicionais"""
    
    # Lista para armazenar os códigos de curso já utilizados
    codigos_existentes = list(Curso.objects.values_list("codigo_curso", flat=True))
    
    cursos_criados = 0
    tentativas = 0
    max_tentativas = 100  # Limite de tentativas para evitar loop infinito
    
    # Começar a partir do código 600 para não conflitar com os cursos de teste
    codigo_base = 600
    
    while cursos_criados < quantidade and tentativas < max_tentativas:
        tentativas += 1
        
        # Gerar código de curso único
        codigo_curso = codigo_base + cursos_criados
        if codigo_curso in codigos_existentes:
            continue
        
        # Gerar nome do curso
        prefixo = random.choice(prefixos)
        area = random.choice(areas_estudo)
        nome = f"{prefixo} {area}"
        
        # Gerar descrição
        descricao = fake.paragraph(nb_sentences=3)
        
        # Gerar duração (entre 1 e 24 meses)
        duracao = random.randint(1, 24)
        
        # Criar o curso
        try:
            curso = Curso.objects.create(
                codigo_curso=codigo_curso,
                nome=nome,
                descricao=descricao,
                duracao=duracao
            )
            codigos_existentes.append(codigo_curso)
            cursos_criados += 1
            print(f"Curso aleatório criado: {curso.codigo_curso} - {curso.nome} ({curso.duracao} meses)")
        except Exception as e:
            print(f"Erro ao criar curso aleatório: {e}")
    
    print(f"\nTotal de cursos aleatórios criados: {cursos_criados}")

def main():
    """Função principal para popular o banco de dados com cursos"""
    print("Iniciando criação de cursos para testes...")
    
    # Perguntar se deseja limpar os cursos existentes
    resposta = input("Deseja remover todos os cursos existentes antes de criar novos? (s/n): ")
    if resposta.lower() == 's':
        limpar_cursos_existentes()
    
    # Criar cursos específicos para testes
    criar_cursos_para_testes()
    
    # Criar cursos aleatórios adicionais
    criar_cursos_aleatorios(8)
    
    # Contar total de cursos no banco de dados
    total_cursos = Curso.objects.count()
    print(f"\nTotal de cursos no banco de dados: {total_cursos}")
    print("Processo concluído!")

if __name__ == "__main__":
    main()




## popular_cursos_simples.py

python
import os
import django
import random

# Configuração do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from faker import Faker
from cursos.models import Curso

# Inicializar o Faker com localização brasileira
fake = Faker("pt_BR")

# Criar alguns cursos básicos
cursos_basicos = [
    {
        "codigo_curso": 101,
        "nome": "Curso de Teste",
        "descricao": "Descrição do curso de teste",
        "duracao": 6
    },
    {
        "codigo_curso": 102,
        "nome": "Curso de Python",
        "descricao": "Aprenda Python do zero",
        "duracao": 3
    },
    {
        "codigo_curso": 103,
        "nome": "Meditação Avançada",
        "descricao": "Técnicas avançadas de meditação",
        "duracao": 12
    }
]

print("Criando cursos básicos...")
for curso_data in cursos_basicos:
    try:
        curso, created = Curso.objects.update_or_create(
            codigo_curso=curso_data["codigo_curso"],
            defaults=curso_data
        )
        if created:
            print(f"Curso criado: {curso.codigo_curso} - {curso.nome}")
        else:
            print(f"Curso atualizado: {curso.codigo_curso} - {curso.nome}")
    except Exception as e:
        print(f"Erro ao criar curso {curso_data['codigo_curso']}: {e}")

print(f"\nTotal de cursos após criação: {Curso.objects.count()}")




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



