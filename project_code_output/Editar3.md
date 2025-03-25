# Código da Funcionalidade: templates
*Gerado automaticamente*



## templates\base.html

html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Sistema OMAUM{% endblock %}</title>
    <!-- Bootstrap CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css" rel="stylesheet">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="/">Sistema OMAUM</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'turmas:listar_turmas' %}">Turmas</a>
                </li>
                <!-- Adicione mais itens de menu conforme necessário -->
            </ul>
        </div>
    </nav>

    <main class="container mt-4">
        {% block content %}{% endblock %}
    </main>

    <footer class="mt-5 py-3 bg-light text-center">
        <div class="container">
            <span class="text-muted">© 2023 Sistema OMAUM. Todos os direitos reservados.</span>
        </div>
    </footer>

    <!-- Bootstrap JS, Popper.js, and jQuery -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>





## templates\csrf_test.html

html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSRF Test</title>
</head>
<body>
    <h1>CSRF Test</h1>
    <form method="post">
        {% csrf_token %}
        <input type="submit" value="Test CSRF">
    </form>
    <script>
        console.log("CSRF cookie:", document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken=')));
    </script>
</body>
</html>






## templates\home.html

html
{% extends 'base.html' %}

{% block title %}Home - OMAUM{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="jumbotron">
        <h1 class="display-4">Bem-vindo ao OMAUM</h1>
        <p class="lead">Sistema de Gestão para Organizações Maçônicas</p>
        <hr class="my-4">
        <p>Utilize o menu acima para navegar pelo sistema.</p>
        <a class="btn btn-primary btn-lg" href="{% url 'home' %}" role="button">Início</a>
        {% if user.is_authenticated %}
            <a class="btn btn-success btn-lg" href="{% url 'atividades:atividade_academica_list' %}" role="button">Atividades Acadêmicas</a>
            <a class="btn btn-info btn-lg" href="{% url 'atividades:atividade_ritualistica_list' %}" role="button">Atividades Ritualísticas</a>
        {% else %}
            <a class="btn btn-outline-secondary btn-lg" href="{% url 'login' %}" role="button">Login</a>
        {% endif %}
    </div>
</div>
{% endblock %}





## templates\core\base.html

html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}OMAUM{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    
    <!-- Custom CSS -->
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">OMAUM</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'home' %}">Home</a>
                    </li>
                    {% if user.is_authenticated %}
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="atividadesDropdown" role="button" data-bs-toggle="dropdown">
                            Atividades
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="{% url 'atividades:atividade_academica_list' %}">Acadêmicas</a></li>
                            <li><a class="dropdown-item" href="{% url 'atividades:atividade_ritualistica_list' %}">Ritualísticas</a></li>
                        </ul>
                    </li>
                    {% endif %}
                </ul>
                <ul class="navbar-nav">
                    {% if user.is_authenticated %}
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                            {{ user.username }}
                        </a>
                        <ul class="dropdown-menu dropdown-menu-end">
                            {% if user.is_staff %}
                            <li><a class="dropdown-item" href="{% url 'admin:index' %}">Admin</a></li>
                            {% endif %}
                            <li><a class="dropdown-item" href="{% url 'logout' %}">Sair</a></li>
                        </ul>
                    </li>
                    {% else %}
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'login' %}">Login</a>
                    </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main>
        {% if messages %}
        <div class="container mt-3">
            {% for message in messages %}
            <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
            {% endfor %}
        </div>
        {% endif %}

        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-light text-center text-muted py-4 mt-5">
        <div class="container">
            <p>© {% now "Y" %} OMAUM - Todos os direitos reservados</p>
        </div>
    </footer>

    <!-- Bootstrap JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Custom JavaScript -->
    {% block extra_js %}{% endblock %}
</body>
</html>





## templates\includes\form_errors.html

html
{% if form.non_field_errors %}
    <div class="alert alert-




## templates\registration\login.html

html
{% extends 'base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
<div class="container mt-5">
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card">
        <div class="card-header">
          <h4 class="mb-0">Login</h4>
        </div>
        <div class="card-body">
          <form method="post" class="needs-validation" novalidate>
            {% csrf_token %}

            {% if form.errors %}
              <div class="alert alert-danger">
                Seu nome de usuário e senha não correspondem. Por favor, tente novamente.
              </div>
            {% endif %}

            <div class="mb-3">
              <label for="id_username" class="form-label">Nome de usuário</label>
              <input type="text" name="username" id="id_username" class="form-control" required>
            </div>

            <div class="mb-3">
              <label for="id_password" class="form-label">Senha</label>
              <input type="password" name="password" id="id_password" class="form-control" required>
            </div>

            <input type="hidden" name="next" value="{{ next }}">

            <div class="d-grid">
              <button type="submit" class="btn btn-primary">Entrar</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}





## templates\registration\registro.html

html
{% extends 'base.html' %}
{% load widget_tweaks %}

{% block title %}Registrar - OMAUM{% endblock %}
{% block content %}
<div class="container mt-5">
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card">
        <div class="card-header">
          <h4 class="mb-0">Registrar</h4>
        </div>
        <div class="card-body">
          <p class="mb-3">Por favor, preencha os campos abaixo para criar uma nova conta.</p>
          <form method="post" class="needs-validation" novalidate>
            {% csrf_token %}

            {% if form.errors %}
              <div class="alert alert-danger">
                Por favor, corrija os erros abaixo.
              </div>
            {% endif %}

            {% for field in form %}
              <div class="mb-3">
                <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                {{ field|add_class:"form-control" }}
                {% if field.errors %}
                  <div class="invalid-feedback d-block">
                    {% for error in field.errors %}
                      {{ error }}
                    {% endfor %}
                  </div>
                {% endif %}
              </div>
            {% endfor %}

            <div class="d-grid">
              <button type="submit" class="btn btn-primary">Registrar</button>
            </div>
          </form>

          <div class="mt-3 text-center">
            <p>Já tem uma conta? <a href="{% url 'login' %}">Faça login aqui</a></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}


# Código da Funcionalidade: static
*Gerado automaticamente*



## static\css\accessibility_fixes.css

css
/* Fix for list structure accessibility issues */
ul, ol {
  font-size: 0;  /* Collapse whitespace between list items */
  list-style-position: inside;  /* Ensure bullets/numbers are within the list item's text flow */
}

li {
  font-size: 1rem;  /* Restore font size for list items */
  margin-bottom: 0.5em;  /* Add some vertical spacing between list items for better readability */
}

ul *, ol * {
  font-size: 1rem;  /* Restore font size for nested elements */
}

/* Fix for Bootstrap components */
.navbar-nav, .dropdown-menu {
  font-size: 0;  /* Collapse whitespace between nav items */
}

.navbar-nav *, .dropdown-menu * {
  font-size: 1rem;  /* Restore font size for nav items and dropdowns */
}

/* Additional accessibility improvements */
:focus {
  outline: 2px solid #007bff;  /* Add a visible focus indicator */
  outline-offset: 2px;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Improve color contrast for better readability */
body {
  color: #333;  /* Darker text color for better contrast */
}

a {
  color: #0056b3;  /* Darker link color for better contrast */
}

/* Ensure sufficient line height for readability */
p, li {
  line-height: 1.5;
}



# Código da Funcionalidade: root
*Gerado automaticamente*



## alunostests__init__.py

python
# Alunos app




## collect_atividade_ritualistica_code.py

python
import os
root_dir = "C:\\projetos\\omaum\\punicoes"
def collect_code(root_dir, output_file):
    files_to_check = [
        ('atividades/models.py', 'AtividadeRitualistica Model'),
        ('atividades/forms.py', 'AtividadeRitualisticaForm'),
        ('atividades/views.py', 'AtividadeRitualistica Views'),
        ('atividades/urls.py', 'AtividadeRitualistica URLs'),
        ('atividades/templates/atividades/criar_atividade_ritualistica.html', 'Create AtividadeRitualistica Template'),
        ('atividades/templates/atividades/editar_atividade_ritualistica.html', 'Edit AtividadeRitualistica Template'),
        ('atividades/templates/atividades/listar_atividades_ritualisticas.html', 'List AtividadeRitualistica Template'),
    ]

    with open(output_file, 'w', encoding='utf-8') as md_file:
        md_file.write("# AtividadeRitualistica Code Review\n\n")

        for file_path, section_title in files_to_check:
            full_path = os.path.join(root_dir, file_path)
            if os.path.exists(full_path):
                md_file.write(f"## {section_title}\n\n")
                md_file.write(f"**File: {file_path}**\n\n")
                md_file.write("```python\n")
                with open(full_path, 'r', encoding='utf-8') as code_file:
                    md_file.write(code_file.read())
                md_file.write("```\n\n")
            else:
                md_file.write(f"## {section_title}\n\n")
                md_file.write(f"**File: {file_path}**\n\n")
                md_file.write("File not found.\n\n")

if __name__ == "__main__":
    project_root = "C:/projetos/omaum"  # Update this to your project root
    output_file = "atividade_ritualistica_code_review.md"
    collect_code(project_root, output_file)
    print(f"Code review file generated: {output_file}")




## collect_code.py

python
import os

def collect_code(root_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Dicionário para armazenar o conteúdo de cada funcionalidade
    functionality_content = {}
    
    for root, dirs, files in os.walk(root_dir):
        # Ignorar diretórios de ambiente virtual e cache
        if 'venv' in root or '__pycache__' in root:
            continue
            
        # Pega o primeiro diretório após o root_dir como a funcionalidade
        relative_path = os.path.relpath(root, root_dir)
        
        # Special handling for root files - assign them to "root" functionality
        if relative_path == '.':
            functionality = "root"
        else:
            functionality = relative_path.split(os.path.sep)[0]

        if functionality not in functionality_content:
            functionality_content[functionality] = []

        for file in files:
            if file.endswith(('.py', '.html', '.js', '.css')):
                file_path = os.path.join(root, file)
                
                # Verificar se o arquivo está vazio
                if os.path.getsize(file_path) == 0:
                    continue  # Pular arquivos vazios
                
                relative_file_path = os.path.relpath(file_path, root_dir)
                
                # Formatação Markdown aprimorada
                content = f"\n\n## {relative_file_path}\n\n"
                
                # Determinar a linguagem para o bloco de código
                extension = file.split('.')[-1]
                language = extension
                if extension == 'py':
                    language = 'python'
                elif extension == 'js':
                    language = 'javascript'
                
                content += f"{language}\n"
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                        # Verificar se o conteúdo está vazio ou contém apenas espaços em branco
                        if not file_content.strip():
                            continue  # Pular arquivos com conteúdo vazio
                        content += file_content
                except IOError as e:
                    content += f"Error reading file: {e}"
                
                content += "\n\n\n"
                functionality_content[functionality].append(content)

    # Escreve o conteúdo de cada funcionalidade em um arquivo Markdown separado
    for functionality, content in functionality_content.items():
        # Ignorar diretórios vazios (mas não mais ignorando '.')
        if not content:
            continue
            
        output_file = os.path.join(output_dir, f"{functionality}_code.md")
        
        with open(output_file, 'w', encoding='utf-8') as out:
            # Adicionar título principal
            out.write(f"# Código da Funcionalidade: {functionality}\n")
            out.write(f"*Gerado automaticamente*\n\n")
            out.write(''.join(content))
        
        print(f"Código da funcionalidade '{functionality}' coletado e salvo em {output_file}")

if __name__ == "__main__":
    project_root = "."  # Caminho para a raiz do seu projeto
    output_dir = "project_code_output"  # Diretório para armazenar os arquivos de saída
    
    collect_code(project_root, output_dir)
    
    print(f"Coleta de código concluída. Arquivos Markdown salvos em {output_dir}")





## collect_os.py

python
import os

def collect_files(project_root):
    relevant_files = {
        'forms.py': [],
        'views.py': [],
        'urls.py': [],
        'models.py': [],
        'templates': []
    }

    for root, dirs, files in os.walk(project_root):
        for file in files:
            if file in relevant_files:
                relevant_files[file].append(os.path.join(root, file))
            elif file.endswith('.html'):
                relevant_files['templates'].append(os.path.join(root, file))

    return relevant_files

def write_file_contents(output_file, filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        output_file.write(f"\n\nFile: {filepath}\n")
        output_file.write("```python\n")
        output_file.write(file.read())
        output_file.write("\n```\n")

def main():
    project_root = input("Enter the root directory of your Django project: ")
    output_filename = "project_files_for_review.md"

    relevant_files = collect_files(project_root)

    with open(output_filename, 'w', encoding='utf-8') as output_file:
        output_file.write("# Django Project Files for Review\n")

        for file_type, file_paths in relevant_files.items():
            output_file.write(f"\n## {file_type.capitalize()} Files:\n")
            for filepath in file_paths:
                write_file_contents(output_file, filepath)

    print(f"File contents have been written to {output_filename}")

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




## run_omaum.py

python
import os
import sys
import subprocess
import webbrowser
import time

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()
    return process.returncode, output, error

def activate_venv():
    venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv')
    if sys.platform == "win32":
        activate_script = os.path.join(venv_path, 'Scripts', 'activate.bat')
        if os.path.exists(activate_script):
            return f"call {activate_script} &&"
    else:
        activate_script = os.path.join(venv_path, 'bin', 'activate')
        if os.path.exists(activate_script):
            return f"source {activate_script} &&"
    return ""

def main():
    # Change to the directory containing manage.py
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # Activate virtual environment if it exists
    activate_cmd = activate_venv()

    # Start Django server
    command = f"{activate_cmd} python manage.py runserver"
    returncode, output, error = run_command(command)

    if returncode != 0:
        print("An error occurred while running the server:")
        print(error)
        input("Press Enter to exit...")
        return

    # Open web browser
    webbrowser.open("http://127.0.0.1:8000/")

    print("Server is running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping server...")

if __name__ == "__main__":
    main()





## settings-Produção.py

python
"""
Django settings for omaum project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
import os
GETTEXT_PATH = r'C:\msys64\usr\bin'  # Adjust this path to where gettext is actually installed
os.environ['PATH'] += os.pathsep + GETTEXT_PATH
from .utils import verify  # assumindo que a função está em um arquivo utils.py na mesma pasta
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1odw#x&ng-if-cpk9zupxzv&)y7sqxe&-(g3isa6l!l6oh(ht%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['seu-dominio.com', 'www.seu-dominio.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps de terceiros
    'crispy_forms',

    # Seus apps
    'core',
    'alunos',
    'turmas',
    'atividades',
    'presencas',
    'cargos',
    'relatorios',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']


CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Adicione esta linha
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'omaum.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core/templates'],  # Adicione esta linha
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'omaum.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = verify(BASE_DIR / 'staticfiles')
MEDIA_ROOT = verify(BASE_DIR / 'media')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Specifies the directory paths for localization (translation) files in the Django project
# BASE_DIR / 'locale' points to a 'locale' directory relative to the project's base directory
LOCALE_PATHS = (
    BASE_DIR / 'locale',
)




## settings.py

python
"""
Django settings for omaum project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Adjust this path to where gettext is actually installed
GETTEXT_PATH = r'C:\msys64\usr\bin'
os.environ['PATH'] += os.pathsep + GETTEXT_PATH

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1odw#x&ng-if-cpk9zupxzv&)y7sqxe&-(g3isa6l!l6oh(ht%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Your custom apps
    'alunos',
    'atividades',
    'cargos',
    'core',
    'cursos',
    'frequencias',
    'iniciacoes',
    'presencas',
    'professores',
    'punicoes',
    'relatorios',
    'turmas',
    # Other apps as needed
]


MIDDLEWARE = [
    'core.middleware.ManutencaoMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']

CRISPY_TEMPLATE_PACK = 'bootstrap4'

ROOT_URLCONF = 'omaum.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Make sure this points to your templates directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'omaum.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'pt-BR'
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'  # Adjust this if your login URL name is different

# Specifies the directory paths for localization (translation) files in the Django project
LOCALE_PATHS = (
    BASE_DIR / 'locale',
)





## temp.py

python
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
urlpatterns = [
]
from django.contrib.auth import views as auth_views
urlpatterns += [
]





## urls.py

python
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('alunos/', include('alunos.urls')),
    path('turmas/', include('turmas.urls')),
    path('atividades/', include('atividades.urls')),
    path('frequencias/', include('frequencias.urls')),
    path('presencas/', include('presencas.urls')),
    path('relatorios/', include('relatorios.urls')),
    path('cargos/', include('cargos.urls')),
    path('iniciacoes/', include('iniciacoes.urls')),
    path('punicoes/', include('punicoes.urls')),
    path('cursos/', include('cursos.urls')),
    path('professores/', include('professores.urls')),
    path('home/', include('home.urls')),
    path('', RedirectView.as_view(pattern_name='home'), name='root'),
]



# Código da Funcionalidade: omaum
*Gerado automaticamente*



## omaum\asgi.py

python
"""
ASGI config for omaum project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')

application = get_asgi_application()





## omaum\settings.py

python
"""
Django settings for omaum project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
GETTEXT_PATH = os.path.join(BASE_DIR, r'msys64\usr\bin\gettext.dll')
from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1odw#x&ng-if-cpk9zupxzv&)y7sqxe&-(g3isa6l!l6oh(ht%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # ...
    'atividades',
    # ...
]


CRISPY_TEMPLATE_PACK = 'bootstrap4'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]




# Adicione estas configurações se não estiverem presentes
CSRF_COOKIE_SECURE = False  # Mude para True em produção com HTTPS
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS = False
CSRF_COOKIE_NAME = 'csrftoken'
SESSION_COOKIE_SECURE = False  # Mude para True em produção com HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'


ROOT_URLCONF = 'omaum.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Adicione esta linha se não estiver presente
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



WSGI_APPLICATION = 'omaum.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Add this new setting
LANGUAGE_COOKIE_NAME = 'django_language'



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'login'
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Authentication settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Authentication settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'





## omaum\urls.py

python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('alunos/', include('alunos.urls')),
    path('atividades/', include('atividades.urls')),
    path('turmas/', include('turmas.urls')),
    path('presencas/', include('presencas.urls')),
    path('relatorios/', include('relatorios.urls')),
    # Add other apps here
]

from django.contrib.auth import views as auth_views
urlpatterns += [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]





## omaum\utils.py

python
from pathlib import Path

def verify(path):
    """
    Verifica se um caminho existe e retorna o caminho absoluto.
    Se o caminho não existir, lança uma exceção ValueError.

    :param path: O caminho a ser verificado (pode ser uma string ou um objeto Path)
    :return: O caminho absoluto como um objeto Path
    :raises ValueError: Se o caminho não existir
    """
    path = Path(path)
    if path.exists():
        return path.resolve()
    else:
        raise ValueError(f"O caminho {path} não existe")

# Você pode adicionar outras funções utilitárias aqui, se necessário




## omaum\wsgi.py

python
"""
WSGI config for omaum project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')

application = get_wsgi_application()



# Código da Funcionalidade: core
*Gerado automaticamente*



## core\admin.py

python
from django.contrib import admin
from .models import ConfiguracaoSistema, LogAtividade

@admin.register(ConfiguracaoSistema)
class ConfiguracaoSistemaAdmin(admin.ModelAdmin):
    list_display = ('nome_sistema', 'versao', 'data_atualizacao', 'manutencao_ativa')
    list_editable = ('manutencao_ativa',)
    readonly_fields = ('data_atualizacao',)

@admin.register(LogAtividade)
class LogAtividadeAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'acao', 'usuario', 'data')
    list_filter = ('tipo', 'data', 'usuario')
    search_fields = ('acao', 'usuario', 'detalhes')
    readonly_fields = ('data',)





## core\apps.py

python
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'





## core\forms.py

python
from django import forms
from core.models import Aluno, Curso, Turma, AtividadeAcademica, AtividadeRitualistica
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ('nome', 'matricula', 'curso')

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ('nome', 'descricao')

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ('nome', 'curso', 'data_inicio', 'data_fim', 'vagas')

class AtividadeAcademicaForm(forms.ModelForm):
    class Meta:
        model = AtividadeAcademica
        # Corrigir para usar os campos corretos
        fields = ('nome', 'descricao', 'data_inicio', 'data_fim', 'turma')

class AtividadeRitualisticaForm(forms.ModelForm):
    class Meta:
        model = AtividadeRitualistica
        fields = ['nome', 'descricao', 'turma', 'alunos']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['turma'].queryset = Turma.objects.all()
        self.fields['alunos'].queryset = Aluno.objects.all()
        self.fields['alunos'].widget = forms.CheckboxSelectMultiple()

class AlunoTurmaForm(forms.Form):
    aluno = forms.ModelChoiceField(queryset=Aluno.objects.all(), label="Aluno")

    def __init__(self, *args, **kwargs):
        turma = kwargs.pop('turma', None)
        super().__init__(*args, **kwargs)
        if turma:
            self.fields['aluno'].queryset = Aluno.objects.exclude(turmas=turma)

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user




## core\middleware.py

python
from django.shortcuts import render
from .utils import garantir_configuracao_sistema

class ManutencaoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar se o sistema está em manutenção
        config = garantir_configuracao_sistema()
        
        # Ignorar verificação para staff e para a página de login
        if (config.manutencao_ativa and 
            not request.user.is_staff and 
            not request.path.startswith('/admin') and
            not request.path.endswith('/entrar/')):
            return render(request, 'core/manutencao.html', {
                'mensagem': config.mensagem_manutencao
            })
            
        response = self.get_response(request)
        return response





## core\models.py

python
from django.db import models
from django.utils import timezone

class ConfiguracaoSistema(models.Model):
    """Configurações globais do sistema"""
    nome_sistema = models.CharField(max_length=100, default="OMAUM")
    versao = models.CharField(max_length=20, default="1.0.0")
    data_atualizacao = models.DateTimeField(default=timezone.now)
    manutencao_ativa = models.BooleanField(default=False)
    mensagem_manutencao = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.nome_sistema} v{self.versao}"
    
    class Meta:
        verbose_name = 'Configuração do Sistema'
        verbose_name_plural = 'Configurações do Sistema'

class LogAtividade(models.Model):
    """Registro de atividades do sistema"""
    TIPO_CHOICES = [
        ('INFO', 'Informação'),
        ('AVISO', 'Aviso'),
        ('ERRO', 'Erro'),
        ('DEBUG', 'Depuração'),
    ]
    
    usuario = models.CharField(max_length=100)
    acao = models.CharField(max_length=255)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='INFO')
    data = models.DateTimeField(default=timezone.now)
    detalhes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.tipo}: {self.acao} por {self.usuario}"
    
    class Meta:
        verbose_name = 'Log de Atividade'
        verbose_name_plural = 'Logs de Atividades'
        ordering = ['-data']




## core\tests.py

python
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware

from .models import ConfiguracaoSistema, LogAtividade
from .views import pagina_inicial, entrar, painel_controle, atualizar_configuracao
from .utils import registrar_log, adicionar_mensagem, garantir_configuracao_sistema
from .middleware import ManutencaoMiddleware


class ConfiguracaoSistemaTests(TestCase):
    """Testes para o modelo ConfiguracaoSistema"""
    
    def test_criacao_configuracao(self):
        """Testa a criação de uma configuração do sistema"""
        config = ConfiguracaoSistema.objects.create(
            nome_sistema="Sistema de Teste",
            versao="1.0.0",
            manutencao_ativa=False
        )
        self.assertEqual(config.nome_sistema, "Sistema de Teste")
        self.assertEqual(config.versao, "1.0.0")
        self.assertFalse(config.manutencao_ativa)
    
    def test_str_representation(self):
        """Testa a representação string do modelo"""
        config = ConfiguracaoSistema.objects.create(
            nome_sistema="Sistema de Teste",
            versao="1.0.0"
        )
        self.assertEqual(str(config), "Sistema de Teste v1.0.0")


class LogAtividadeTests(TestCase):
    """Testes para o modelo LogAtividade"""
    
    def test_criacao_log(self):
        """Testa a criação de um log de atividade"""
        log = LogAtividade.objects.create(
            usuario="usuario_teste",
            acao="Ação de teste",
            tipo="INFO",
            detalhes="Detalhes da ação de teste"
        )
        self.assertEqual(log.usuario, "usuario_teste")
        self.assertEqual(log.acao, "Ação de teste")
        self.assertEqual(log.tipo, "INFO")
        self.assertEqual(log.detalhes, "Detalhes da ação de teste")
    
    def test_str_representation(self):
        """Testa a representação string do modelo"""
        log = LogAtividade.objects.create(
            usuario="usuario_teste",
            acao="Ação de teste",
            tipo="INFO"
        )
        self.assertEqual(str(log), "INFO: Ação de teste por usuario_teste")
    
    def test_ordering(self):
        """Testa a ordenação dos logs (mais recentes primeiro)"""
        log1 = LogAtividade.objects.create(usuario="user1", acao="acao1")
        log2 = LogAtividade.objects.create(usuario="user2", acao="acao2")
        logs = LogAtividade.objects.all()
        self.assertEqual(logs[0], log2)  # O segundo log deve aparecer primeiro


class UtilsTests(TestCase):
    """Testes para as funções utilitárias"""
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword'
        )
    
    def test_registrar_log(self):
        """Testa o registro de logs"""
        request = self.factory.get('/')
        request.user = self.user
        
        # Registra um log
        registrar_log(request, "Teste de log", "INFO", "Detalhes do teste")
        
        # Verifica se o log foi criado
        log = LogAtividade.objects.last()
        self.assertEqual(log.usuario, "testuser")
        self.assertEqual(log.acao, "Teste de log")
        self.assertEqual(log.tipo, "INFO")
        self.assertEqual(log.detalhes, "Detalhes do teste")
    
    def test_registrar_log_anonimo(self):
        """Testa o registro de logs para usuários anônimos"""
        request = self.factory.get('/')
        request.user = AnonymousUser()
        
        # Registra um log
        registrar_log(request, "Teste de log anônimo")
        
        # Verifica se o log foi criado
        log = LogAtividade.objects.last()
        self.assertEqual(log.usuario, "Anônimo")
        self.assertEqual(log.acao, "Teste de log anônimo")
    
    def test_garantir_configuracao_sistema(self):
        """Testa a função que garante a existência de uma configuração"""
        # Inicialmente não deve haver configurações
        self.assertEqual(ConfiguracaoSistema.objects.count(), 0)
        
        # Chama a função para garantir uma configuração
        config = garantir_configuracao_sistema()
        
        # Deve haver exatamente uma configuração
        self.assertEqual(ConfiguracaoSistema.objects.count(), 1)
        self.assertEqual(config.nome_sistema, "OMAUM")
        
        # Chamar novamente não deve criar outra configuração
        config2 = garantir_configuracao_sistema()
        self.assertEqual(ConfiguracaoSistema.objects.count(), 1)
        self.assertEqual(config, config2)


class ViewsTests(TestCase):
    """Testes para as views"""
    
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        
        # Cria um usuário normal
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword'
        )
        
        # Cria um usuário staff
        self.staff_user = User.objects.create_user(
            username='staffuser', 
            email='staff@example.com', 
            password='staffpassword',
            is_staff=True
        )
        
        # Garante que existe uma configuração
        self.config = garantir_configuracao_sistema()
    
    def test_pagina_inicial(self):
        """Testa a página inicial"""
        response = self.client.get(reverse('core:pagina_inicial'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
        self.assertContains(response, self.config.nome_sistema)
    
    def test_pagina_inicial_em_manutencao(self):
        """Testa a página inicial quando o sistema está em manutenção"""
        # Ativa o modo de manutenção
        self.config.manutencao_ativa = True
        self.config.mensagem_manutencao = "Sistema em manutenção para testes"
        self.config.save()
        
        # Usuário anônimo deve ver a página de manutenção
        response = self.client.get(reverse('core:pagina_inicial'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/manutencao.html')
        self.assertContains(response, "Sistema em manutenção para testes")
        
        # Usuário staff deve ver a página normal mesmo em manutenção
        self.client.login(username='staffuser', password='staffpassword')
        response = self.client.get(reverse('core:pagina_inicial'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
    
    def test_entrar_get(self):
        """Testa a página de login (GET)"""
        response = self.client.get(reverse('core:entrar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')
    
    def test_entrar_post_sucesso(self):
        """Testa o login com sucesso"""
        response = self.client.post(reverse('core:entrar'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertRedirects(response, reverse('core:pagina_inicial'))
        
        # Verifica se o log foi registrado
        log = LogAtividade.objects.last()
        self.assertEqual(log.usuario, "testuser")
        self.assertEqual(log.acao, "Login realizado com sucesso")
    
    def test_entrar_post_falha(self):
        """Testa o login com credenciais inválidas"""
        response = self.client.post(reverse('core:entrar'), {
            'username': 'testuser',
            'password': 'senhaerrada'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')
    
    def test_sair(self):
        """Testa o logout"""
        # Primeiro faz login
        self.client.login(username='testuser', password='testpassword')
        
        # Depois faz logout
        response = self.client.get(reverse('core:sair'))
        self.assertRedirects(response, reverse('core:pagina_inicial'))
        
        # Verifica se o usuário está deslogado
        response = self.client.get(reverse('core:painel_controle'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("core:painel_controle")}')
    
    def test_painel_controle_sem_permissao(self):
        """Testa acesso ao painel de controle sem permissão"""
        # Usuário não autenticado deve ser redirecionado para login
        response = self.client.get(reverse('core:painel_controle'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("core:painel_controle")}')
        
        # Usuário normal não deve ter acesso
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('core:painel_controle'))
        self.assertRedirects(response, reverse('core:pagina_inicial'))
    
    def test_painel_controle_com_permissao(self):
        """Testa acesso ao painel de controle com permissão"""
        self.client.login(username='staffuser', password='staffpassword')
        response = self.client.get(reverse('core:painel_controle'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/painel_controle.html')
    
    def test_atualizar_configuracao_sem_permissao(self):
        """Testa atualização de configuração sem permissão"""
        # Usuário não autenticado deve ser redirecionado para login
        response = self.client.get(reverse('core:atualizar_configuracao'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("core:atualizar_configuracao")}')
        
        # Usuário normal não deve ter acesso
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('core:atualizar_configuracao'))
        self.assertRedirects(response, reverse('core:pagina_inicial'))
    
    def test_atualizar_configuracao_get(self):
        """Testa a página de atualização de configuração (GET)"""
        self.client.login(username='staffuser', password='staffpassword')
        response = self.client.get(reverse('core:atualizar_configuracao'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/atualizar_configuracao.html')
    
    def test_atualizar_configuracao_post(self):
        """Testa a atualização de configuração (POST)"""
        self.client.login(username='staffuser', password='staffpassword')
        response = self.client.post(reverse('core:atualizar_configuracao'), {
            'nome_sistema': 'Sistema Atualizado',
            'versao': '2.0.0',
            'manutencao_ativa': 'on',
            'mensagem_manutencao': 'Mensagem de manutenção atualizada'
        })
        self.assertRedirects(response, reverse('core:painel_controle'))
        
        # Verifica se a configuração foi atualizada
        config = ConfiguracaoSistema.objects.get(pk=1)
        self.assertEqual(config.nome_sistema, 'Sistema Atualizado')
        self.assertEqual(config.versao, '2.0.0')
        self.assertTrue(config.manutencao_ativa)
        self.assertEqual(config.mensagem_manutencao, 'Mensagem de manutenção atualizada')
        
        # Verifica se o log foi registrado
        log = LogAtividade.objects.last()
        self.assertEqual(log.acao, 'Configurações do sistema atualizadas')


class MiddlewareTests(TestCase):
    """Testes para o middleware de manutenção"""
    
    def setUp(self):
        self.factory = RequestFactory()
        
        # Cria um usuário normal
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword'
        )
        
        # Cria um usuário staff
        self.staff_user = User.objects.create_user(
            username='staffuser', 
            email='staff@example.com', 
            password='staffpassword',
            is_staff=True
        )
        
        # Garante que existe uma configuração
        self.config = garantir_configuracao_sistema()
        
        # Define uma função simples para o middleware chamar
        def get_response(request):
            return "response"
        
        self.middleware = ManutencaoMiddleware(get_response)
    
    def test_middleware_sem_manutencao(self):
        """Testa o middleware quando o sistema não está em manutenção"""
        self.config.manutencao_ativa = False
        self.config.save()
        
        request = self.factory.get('/')
        request.user = self.user
        
        response = self.middleware(request)
        self.assertEqual(response, "response")
    
    def test_middleware_com_manutencao_usuario_normal(self):
        """Testa o middleware quando o sistema está em manutenção para usuário normal"""
        self.config.manutencao_ativa = True
        self.config.mensagem_manutencao = "Sistema em manutenção para testes"
        self.config.save()
        
        request = self.factory.get('/')
        request.user = self.user
        
        #




## core\urls.py

python
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('entrar/', views.entrar, name='entrar'),
    path('sair/', views.sair, name='sair'),
    path('painel-controle/', views.painel_controle, name='painel_controle'),
    path('atualizar-configuracao/', views.atualizar_configuracao, name='atualizar_configuracao'),
]




## core\utils.py

python
from django.contrib import messages
from .models import LogAtividade

def registrar_log(request, acao, tipo='INFO', detalhes=None):
    """
    Registra uma ação no log de atividades do sistema
    
    Args:
        request: O objeto request do Django
        acao: Descrição da ação realizada
        tipo: Tipo de log (INFO, AVISO, ERRO, DEBUG)
        detalhes: Detalhes adicionais sobre a ação
    """
    usuario = request.user.username if request.user.is_authenticated else 'Anônimo'
    
    LogAtividade.objects.create(
        usuario=usuario,
        acao=acao,
        tipo=tipo,
        detalhes=detalhes
    )

def adicionar_mensagem(request, tipo, texto):
    """
    Adiciona uma mensagem para o usuário
    
    Args:
        request: O objeto request do Django
        tipo: Tipo de mensagem (success, error, warning, info)
        texto: Texto da mensagem
    """
    tipos_mensagem = {
        'sucesso': messages.SUCCESS,
        'erro': messages.ERROR,
        'aviso': messages.WARNING,
        'info': messages.INFO,
    }
    
    nivel = tipos_mensagem.get(tipo, messages.INFO)
    messages.add_message(request, nivel, texto)

def garantir_configuracao_sistema():
    """
    Garante que exista pelo menos uma configuração do sistema.
    Retorna a configuração existente ou cria uma nova.
    """
    from .models import ConfiguracaoSistema
    
    config, criado = ConfiguracaoSistema.objects.get_or_create(
        pk=1,
        defaults={
            'nome_sistema': 'OMAUM',
            'versao': '1.0.0',
            'manutencao_ativa': False,
            'mensagem_manutencao': 'Sistema em manutenção. Tente novamente mais tarde.'
        }
    )
    
    return config





## core\views.py

python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .utils import registrar_log, adicionar_mensagem, garantir_configuracao_sistema
from .models import ConfiguracaoSistema
from django.utils import timezone

def pagina_inicial(request):
    """Renderiza a página inicial do sistema"""
    config = garantir_configuracao_sistema()

    # If the system is under maintenance and the user is not staff
    if config.manutencao_ativa and not request.user.is_staff:
        return render(request, 'core/manutencao.html', {
            'mensagem': config.mensagem_manutencao
        })

    return render(request, 'core/home.html', {
        'titulo': config.nome_sistema,
        # Add any other context data needed for displaying functionalities
    })

def entrar(request):
    """Página de login do sistema"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                registrar_log(request, f'Login realizado com sucesso')
                adicionar_mensagem(request, 'sucesso', 'Login realizado com sucesso!')
                return redirect('core:pagina_inicial')
            else:
                adicionar_mensagem(request, 'erro', 'Nome de usuário ou senha inválidos.')
        else:
            adicionar_mensagem(request, 'erro', 'Nome de usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

@login_required
def painel_controle(request):
    """Painel de controle do sistema (apenas para staff)"""
    if not request.user.is_staff:
        adicionar_mensagem(request, 'erro', 'Você não tem permissão para acessar esta página.')
        return redirect('core:pagina_inicial')
    
    config = ConfiguracaoSistema.objects.first()
    logs_recentes = LogAtividade.objects.all()[:10]
    
    return render(request, 'core/painel_controle.html', {
        'config': config,
        'logs_recentes': logs_recentes
    })

@login_required
def atualizar_configuracao(request):
    """Atualiza as configurações do sistema"""
    if not request.user.is_staff:
        adicionar_mensagem(request, 'erro', 'Você não tem permissão para acessar esta página.')
        return redirect('core:pagina_inicial')
    
    config = garantir_configuracao_sistema()
    
    if request.method == 'POST':
        nome_sistema = request.POST.get('nome_sistema')
        versao = request.POST.get('versao')
        manutencao_ativa = request.POST.get('manutencao_ativa') == 'on'
        mensagem_manutencao = request.POST.get('mensagem_manutencao')
        
        config.nome_sistema = nome_sistema
        config.versao = versao
        config.manutencao_ativa = manutencao_ativa
        config.mensagem_manutencao = mensagem_manutencao
        config.data_atualizacao = timezone.now()
        config.save()
        
        registrar_log(request, 'Configurações do sistema atualizadas', 'INFO')
        adicionar_mensagem(request, 'sucesso', 'Configurações atualizadas com sucesso!')
        
        return redirect('core:painel_controle')
    
    return render(request, 'core/atualizar_configuracao.html', {
        'config': config
    })

from django.contrib.auth import logout

def sair(request):
    """Realiza o logout do usuário"""
    if request.user.is_authenticated:
        registrar_log(request, 'Logout realizado com sucesso')
        logout(request)
        adicionar_mensagem(request, 'info', 'Você saiu do sistema com sucesso.')
    
    return redirect('core:pagina_inicial')





## core\migrations\0001_initial.py

python
# Generated by Django 5.1.7 on 2025-03-23 21:21

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracaoSistema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_sistema', models.CharField(default='OMAUM', max_length=100)),
                ('versao', models.CharField(default='1.0.0', max_length=20)),
                ('data_atualizacao', models.DateTimeField(default=django.utils.timezone.now)),
                ('manutencao_ativa', models.BooleanField(default=False)),
                ('mensagem_manutencao', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Configuração do Sistema',
                'verbose_name_plural': 'Configurações do Sistema',
            },
        ),
        migrations.CreateModel(
            name='LogAtividade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=100)),
                ('acao', models.CharField(max_length=255)),
                ('tipo', models.CharField(choices=[('INFO', 'Informação'), ('AVISO', 'Aviso'), ('ERRO', 'Erro'), ('DEBUG', 'Depuração')], default='INFO', max_length=10)),
                ('data', models.DateTimeField(default=django.utils.timezone.now)),
                ('detalhes', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Log de Atividade',
                'verbose_name_plural': 'Logs de Atividades',
                'ordering': ['-data'],
            },
        ),
    ]





## core\templates\core\atualizar_configuracao.html

html
{% extends "core/base.html" %}

{% block title %}Atualizar Configurações do Sistema{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Atualizar Configurações do Sistema</h1>
    
    <div class="card mt-4">
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="nome_sistema" class="form-label">Nome do Sistema</label>
                    <input type="text" class="form-control" id="nome_sistema" name="nome_sistema" value="{{ config.nome_sistema }}" required>
                </div>
                
                <div class="mb-3">
                    <label for="versao" class="form-label">Versão</label>
                    <input type="text" class="form-control" id="versao" name="versao" value="{{ config.versao }}" required>
                </div>
                
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="manutencao_ativa" name="manutencao_ativa" {% if config.manutencao_ativa %}checked{% endif %}>
                    <label class="form-check-label" for="manutencao_ativa">Sistema em Manutenção</label>
                </div>
                
                <div class="mb-3">
                    <label for="mensagem_manutencao" class="form-label">Mensagem de Manutenção</label>
                    <textarea class="form-control" id="mensagem_manutencao" name="mensagem_manutencao" rows="3">{{ config.mensagem_manutencao }}</textarea>
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'core:painel_controle' %}" class="btn btn-secondary">Cancelar</a>
                    <button type="submit" class="btn btn-primary">Salvar Alterações</button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}





## core\templates\core\base.html

html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Sistema{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'core:pagina_inicial' %}">OMAUM</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    {% if user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'alunos:listar' %}">Alunos</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'atividades:atividade_academica_list' %}">Atividades Acadêmicas</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'atividades:atividade_ritualistica_list' %}">Atividades Ritualísticas</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'turmas:listar' %}">Turmas</a>
                        </li>
                        <!-- Add more navigation items for other functionalities -->
                        {% if user.is_staff %}
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'core:painel_controle' %}">Painel de Controle</a>
                            </li>
                        {% endif %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'core:sair' %}">Sair</a>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'core:entrar' %}">Entrar</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>


    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
        
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>





## core\templates\core\home.html

html
{% extends "core/base.html" %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Bem-vindo ao {{ titulo }}</h1>
    {% if user.is_authenticated %}
        <div class="row mt-4">
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Alunos</h5>
                        <a href="{% url 'alunos:listar' %}" class="btn btn-primary">Gerenciar Alunos</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Atividades Acadêmicas</h5>
                        <a href="{% url 'atividades:atividade_academica_list' %}" class="btn btn-primary">Gerenciar Atividades Acadêmicas</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Atividades Ritualísticas</h5>
                        <a href="{% url 'atividades:atividade_ritualistica_list' %}" class="btn btn-primary">Gerenciar Atividades Ritualísticas</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Turmas</h5>
                        <a href="{% url 'turmas:listar' %}" class="btn btn-primary">Gerenciar Turmas</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Presenças</h5>
                        <a href="{% url 'presencas:listar' %}" class="btn btn-primary">Gerenciar Presenças</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Relatórios</h5>
                        <a href="{% url 'relatorios:listar' %}" class="btn btn-primary">Gerar Relatórios</a>
                    </div>
                </div>
            </div>
            {% if user.is_staff %}
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Painel de Controle</h5>
                        <a href="{% url 'core:painel_controle' %}" class="btn btn-primary">Acessar Painel</a>
                    </div>
                </div>
            </div>
            {% endif %}
        </div>
    {% else %}
        <p>Por favor, faça login para acessar as funcionalidades do sistema.</p>
        <a href="{% url 'core:entrar' %}" class="btn btn-primary">Entrar</a>
    {% endif %}
</div>
{% endblock %}






## core\templates\core\lista_categorias.html

html
{% extends "core/base.html" %}

{% block title %}Categorias{% endblock %}

{% block content %}
    <h1>Categorias</h1>
    
    <div class="row mt-4">
        {% for categoria in categorias %}
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ categoria.nome }}</h5>
                        <p class="card-text">{{ categoria.descricao|truncatewords:20 }}</p>
                        <a href="{% url 'core:detalhe_categoria' categoria.id %}" class="btn btn-primary">Ver detalhes</a>
                    </div>
                </div>
            </div>
        {% empty %}
            <div class="col-12">
                <p>Nenhuma categoria encontrada.</p>
            </div>
        {% endfor %}
    </div>
{% endblock %}





## core\templates\core\login.html

html
{% extends "core/base.html" %}

{% block title %}Entrar no Sistema{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h4 class="mb-0">Entrar no Sistema</h4>
                </div>
                <div class="card-body">
                    <form method="post" class="needs-validation" novalidate>
                        {% csrf_token %}
                        
                        {% if form.errors %}
                            <div class="alert alert-danger">
                                Seu nome de usuário e senha não correspondem. Por favor, tente novamente.
                            </div>
                        {% endif %}
                        
                        <div class="mb-3">
                            <label for="id_username" class="form-label">Nome de usuário</label>
                            <input type="text" name="username" id="id_username" class="form-control" required>
                        </div>
                        
                        <div class="mb-3">
                            <label for="id_password" class="form-label">Senha</label>
                            <input type="password" name="password" id="id_password" class="form-control" required>
                        </div>
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary">Entrar</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}





## core\templates\core\manutencao.html

html
{% extends "core/base.html" %}

{% block title %}Sistema em Manutenção{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-8 text-center">
            <div class="alert alert-warning">
                <h2><i class="fas fa-tools"></i> Sistema em Manutenção</h2>
                <p class="lead mt-3">
                    Estamos realizando melhorias no sistema. Por favor, tente novamente mais tarde.
                </p>
                {% if mensagem %}
                    <div class="mt-4">
                        <p>{{ mensagem }}</p>
                    </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}





## core\templates\core\painel_controle.html

html
{% extends "core/base.html" %}

{% block title %}Painel de Controle{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Painel de Controle</h1>
    
    <div class="row mt-4">
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">Configurações do Sistema</h5>
                </div>
                <div class="card-body">
                    <p><strong>Nome do Sistema:</strong> {{ config.nome_sistema }}</p>
                    <p><strong>Versão:</strong> {{ config.versao }}</p>
                    <p><strong>Última Atualização:</strong> {{ config.data_atualizacao|date:"d/m/Y H:i" }}</p>
                    <p>
                        <strong>Status:</strong> 
                        {% if config.manutencao_ativa %}
                            <span class="badge bg-warning">Em Manutenção</span>
                        {% else %}
                            <span class="badge bg-success">Operacional</span>
                        {% endif %}
                    </p>
                    
                    <a href="{% url 'core:atualizar_configuracao' %}" class="btn btn-primary">
                        Editar Configurações
                    </a>
                </div>
            </div>
        </div>
        
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Logs Recentes</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Tipo</th>
                                    <th>Ação</th>
                                    <th>Usuário</th>
                                    <th>Data</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for log in logs_recentes %}
                                <tr>
                                    <td>
                                        {% if log.tipo == 'INFO' %}
                                            <span class="badge bg-info">INFO</span>
                                        {% elif log.tipo == 'AVISO' %}
                                            <span class="badge bg-warning">AVISO</span>
                                        {% elif log.tipo == 'ERRO' %}
                                            <span class="badge bg-danger">ERRO</span>
                                        {% else %}
                                            <span class="badge bg-secondary">{{ log.tipo }}</span>
                                        {% endif %}
                                    </td>
                                    <td>{{ log.acao }}</td>
                                    <td>{{ log.usuario }}</td>
                                    <td>{{ log.data|date:"d/m/Y H:i" }}</td>
                                </tr>
                                {% empty %}
                                <tr>
                                    <td colspan="4" class="text-center">Nenhum log encontrado</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    
                    <a href="{% url 'admin:core_logatividade_changelist' %}" class="btn btn-primary">
                        Ver Todos os Logs
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}



