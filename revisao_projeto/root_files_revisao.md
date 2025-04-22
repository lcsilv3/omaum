# Arquivos da Raiz do Projeto Django


### Arquivo: collect_code.py

python
import os
import chardet
import shutil


def collect_files_by_app(project_root):
    # Dicionário para armazenar arquivos por app/funcionalidade
    apps_files = {}
    for root, dirs, files in os.walk(project_root):
        # Ignorar diretórios de ambiente virtual e cache
        if "venv" in root or "__pycache__" in root:
            continue
        # Identificar o app/funcionalidade com base no caminho
        relative_path = os.path.relpath(root, project_root)
        app_name = (
            relative_path.split(os.path.sep)[0]
            if relative_path != "."
            else "core"
        )
        # Inicializar a estrutura para o app se ainda não existir
        if app_name not in apps_files:
            apps_files[app_name] = {
                "forms.py": [],
                "views.py": [],
                "urls.py": [],
                "models.py": [],
                "templates": [],
            }
        for file in files:
            if file in ["forms.py", "views.py", "urls.py", "models.py"]:
                apps_files[app_name][file].append(os.path.join(root, file))
            elif file.endswith(".html"):
                apps_files[app_name]["templates"].append(
                    os.path.join(root, file)
                )
    return apps_files


def write_file_contents(output_file, filepath):
    # Detectar codificação do arquivo
    with open(filepath, "rb") as raw_file:
        raw_data = raw_file.read()
        result = chardet.detect(raw_data)
        encoding = result["encoding"] or "utf-8"  # Fallback para utf-8
    try:
        with open(filepath, "r", encoding=encoding) as file:
            relative_path = os.path.relpath(filepath)
            output_file.write(f"\n\n### Arquivo: {relative_path}\n\n")
            # Determinar o tipo de linguagem para o bloco de código
            if filepath.endswith(".html"):
                language = "html"
            elif filepath.endswith(".py"):
                language = "python"
            else:
                language = "text"
            output_file.write(f"{language}\n")
            output_file.write(file.read())
            output_file.write("\n\n")
    except Exception as e:
        output_file.write(f"\n\n### Arquivo: {filepath}\n\n")
        output_file.write(f"\nErro ao ler o arquivo: {str(e)}\n\n")


def collect_root_files(project_root, output_dir):
    """Coleta arquivos da raiz do projeto Django."""
    output_filename = os.path.join(output_dir, "root_files_revisao.md")
    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write("# Arquivos da Raiz do Projeto Django\n")

        # Listar arquivos na raiz do projeto
        root_files = [
            f
            for f in os.listdir(project_root)
            if os.path.isfile(os.path.join(project_root, f))
            and not f.startswith(".")
        ]

        for file in root_files:
            filepath = os.path.join(project_root, file)
            write_file_contents(output_file, filepath)

        # Verificar e incluir arquivos estáticos
        static_dir = os.path.join(project_root, "static")
        if os.path.exists(static_dir) and os.path.isdir(static_dir):
            output_file.write("\n## Arquivos Estáticos\n")
            for root, dirs, files in os.walk(static_dir):
                for file in files:
                    filepath = os.path.join(root, file)
                    write_file_contents(output_file, filepath)

    print(f"Arquivos da raiz do projeto foram escritos em {output_filename}")


def generate_project_structure(project_root, output_dir):
    """Gera um arquivo com a estrutura completa do projeto."""
    output_filename = os.path.join(output_dir, "project_structure.md")
    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write("# Estrutura do Projeto Django\n\n")
        output_file.write("\n")

        for root, dirs, files in os.walk(project_root):
            # Ignorar diretórios de ambiente virtual e cache
            if "venv" in root or "__pycache__" in root:
                continue

            level = root.replace(project_root, "").count(os.sep)
            indent = " " * 4 * level
            output_file.write(f"{indent}{os.path.basename(root)}/\n")

            sub_indent = " " * 4 * (level + 1)
            for file in files:
                output_file.write(f"{sub_indent}{file}\n")

        output_file.write("\n")

    print(f"Estrutura do projeto foi escrita em {output_filename}")


def check_template_dirs(project_root, output_dir):
    """Verifica e documenta as configurações de diretórios de templates."""
    output_filename = os.path.join(output_dir, "template_dirs_check.md")
    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write("# Verificação de Diretórios de Templates\n\n")

        # Verificar settings.py para configurações de TEMPLATES
        settings_files = []
        for root, dirs, files in os.walk(project_root):
            if "settings.py" in files:
                settings_files.append(os.path.join(root, "settings.py"))

        if settings_files:
            output_file.write(
                "## Configurações de Templates no settings.py\n\n"
            )
            for settings_file in settings_files:
                write_file_contents(output_file, settings_file)

        # Listar todos os diretórios de templates encontrados
        output_file.write("\n## Diretórios de Templates Encontrados\n\n")
        template_dirs = []
        for root, dirs, files in os.walk(project_root):
            if "templates" in dirs:
                template_dir = os.path.join(root, "templates")
                template_dirs.append(template_dir)
                output_file.write(
                    f"- {os.path.relpath(template_dir, project_root)}\n"
                )

                # Listar arquivos de template neste diretório
                output_file.write("  Arquivos:\n")
                for template_root, template_dirs, template_files in os.walk(
                    template_dir
                ):
                    for file in template_files:
                        output_file.write(
                            f"  - {os.path.relpath(os.path.join(template_root, file), template_dir)}\n"
                        )

        # Verificar especificamente o template listar_alunos.html
        output_file.write("\n## Busca pelo template listar_alunos.html\n\n")
        found = False
        for root, dirs, files in os.walk(project_root):
            for file in files:
                if file == "listar_alunos.html":
                    found = True
                    output_file.write(
                        f"Encontrado em: {os.path.relpath(os.path.join(root, file), project_root)}\n"
                    )

        if not found:
            output_file.write(
                "O arquivo listar_alunos.html não foi encontrado no projeto.\n"
            )

    print(
        f"Verificação de diretórios de templates foi escrita em {output_filename}"
    )


def main():
    project_root = input("Digite o diretório raiz do seu projeto Django: ")
    output_dir = "revisao_projeto"
    # Criar diretório de saída se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Coletar arquivos por app
    apps_files = collect_files_by_app(project_root)
    for app_name, file_types in apps_files.items():
        # Verificar se há arquivos para este app
        has_files = any(files for files in file_types.values())
        if not has_files:
            continue
        output_filename = os.path.join(output_dir, f"{app_name}_revisao.md")
        with open(output_filename, "w", encoding="utf-8") as output_file:
            output_file.write(f"# Revisão da Funcionalidade: {app_name}\n")
            for file_type, file_paths in file_types.items():
                if not file_paths:
                    continue
                if file_type == "templates":
                    output_file.write(f"\n## Arquivos de Template:\n")
                else:
                    output_file.write(f"\n## Arquivos {file_type}:\n")
                for filepath in sorted(file_paths):
                    write_file_contents(output_file, filepath)
        print(
            f"Conteúdo da funcionalidade '{app_name}' foi escrito em {output_filename}"
        )

    # Coletar arquivos da raiz e arquivos estáticos
    collect_root_files(project_root, output_dir)

    # Gerar estrutura do projeto
    generate_project_structure(project_root, output_dir)

    # Verificar diretórios de templates
    check_template_dirs(project_root, output_dir)

    print(f"Revisão completa! Arquivos gerados no diretório '{output_dir}'")


if __name__ == "__main__":
    main()




### Arquivo: collect_django_files.py

python
import os
import chardet


def collect_files(project_root):
    relevant_files = {
        "forms.py": [],
        "views.py": [],
        "urls.py": [],
        "models.py": [],
        "templates": [],
    }

    for root, dirs, files in os.walk(project_root):
        # Ignorar diretórios de ambiente virtual e cache
        if "venv" in root or "__pycache__" in root:
            continue

        for file in files:
            if file in relevant_files:
                relevant_files[file].append(os.path.join(root, file))
            elif file.endswith(".html"):
                relevant_files["templates"].append(os.path.join(root, file))

    return relevant_files


def write_file_contents(output_file, filepath):
    # Detectar codificação do arquivo
    with open(filepath, "rb") as raw_file:
        raw_data = raw_file.read()
        result = chardet.detect(raw_data)
        encoding = result["encoding"] or "utf-8"  # Fallback para utf-8

    try:
        with open(filepath, "r", encoding=encoding) as file:
            relative_path = os.path.relpath(filepath)
            output_file.write(f"\n\n### Arquivo: {relative_path}\n")

            # Determinar o tipo de linguagem para o bloco de código
            if filepath.endswith(".html"):
                language = "html"
            elif filepath.endswith(".py"):
                language = "python"
            else:
                language = "text"

            output_file.write(f"{language}\n")
            output_file.write(file.read())
            output_file.write("\n\n")
    except Exception as e:
        output_file.write(f"\n\n### Arquivo: {filepath}\n")
        output_file.write(f"\nErro ao ler o arquivo: {str(e)}\n\n")


def main():
    project_root = input("Digite o diretório raiz do seu projeto Django: ")
    output_filename = "arquivos_projeto_para_revisao.md"

    relevant_files = collect_files(project_root)

    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write("# Arquivos do Projeto Django para Revisão\n")

        for file_type, file_paths in relevant_files.items():
            if file_type == "templates":
                output_file.write(f"\n## Arquivos de Template:\n")
            else:
                output_file.write(f"\n## Arquivos {file_type}:\n")

            for filepath in sorted(file_paths):
                write_file_contents(output_file, filepath)

    print(f"Conteúdo dos arquivos foi escrito em {output_filename}")


if __name__ == "__main__":
    main()




### Arquivo: collect_os.py

python
import os


def collect_files(project_root):
    relevant_files = {
        "forms.py": [],
        "views.py": [],
        "urls.py": [],
        "models.py": [],
        "templates": [],
    }

    for root, dirs, files in os.walk(project_root):
        for file in files:
            if file in relevant_files:
                relevant_files[file].append(os.path.join(root, file))
            elif file.endswith(".html"):
                relevant_files["templates"].append(os.path.join(root, file))

    return relevant_files


def write_file_contents(output_file, filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        output_file.write(f"\n\nFile: {filepath}\n")
        output_file.write("```python\n")
        output_file.write(file.read())
        output_file.write("\n```\n")


def main():
    project_root = input("Enter the root directory of your Django project: ")
    output_filename = "project_files_for_review.md"

    relevant_files = collect_files(project_root)

    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write("# Django Project Files for Review\n")

        for file_type, file_paths in relevant_files.items():
            output_file.write(f"\n## {file_type.capitalize()} Files:\n")
            for filepath in file_paths:
                write_file_contents(output_file, filepath)

    print(f"File contents have been written to {output_filename}")


if __name__ == "__main__":
    main()




### Arquivo: cspell.json

text
{
    "version": "0.2",
    "language": "en,pt,pt-BR",
    "words": [
      "OMAUM",
      "academica",
      "academicas",
      "ritualistica",
      "ritualisticas",
      "alunos",
      "turmas",
      "cadastrar",
      "listar",
      "excluir",
      "editar",
      "criar",
      "todos",
      "direitos",
      "reservados",
      "sair",
      "fechar"
    ],
    "ignorePaths": [
      "node_modules/**",
      "venv/**",
      "*.min.*",
      "static/**",
      "media/**",
      "migrations/**"
    ],
    "ignoreRegExpList": [
      "{% [\\s\\S]*? %}",
      "{{ [\\s\\S]*? }}"
    ],
    "allowCompoundWords": true
  }
  

### Arquivo: Cursos.JPG

text


### Arquivo: c:\projetos\omaum\Cursos.JPG


Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte



### Arquivo: manage.py

python
#!/usr/bin/env python
"""Utilitário de linha de comando do Django para tarefas administrativas."""
import os
import sys


def main():
    """Executa tarefas administrativas."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Não foi possível importar o Django."
            "Tem certeza de que ele está instalado e disponível"
            "Na sua variável de ambiente PYTHONPATH? "
            "Você esqueceu de ativar um ambiente virtual?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()




### Arquivo: pyproject.toml

text
[tool.black]
line-length = 79
include = '\.pyi?



### Arquivo: README.md

text
# Sistema OMAUM

Sistema de gestão acadêmica desenvolvido para [descrição da instituição/propósito].

## Funcionalidades

- Gestão de alunos
- Controle de atividades acadêmicas e ritualísticas
- Gerenciamento de cursos e turmas
- Controle de presenças e notas
- Relatórios acadêmicos
- [outras funcionalidades]

## Tecnologias Utilizadas

- Django
- Python
- SQLite (desenvolvimento)
- [outras tecnologias]

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Instale as dependências: `pip install -r requirements.txt`
5. Execute as migrações: `python manage.py migrate`
6. Inicie o servidor: `python manage.py runserver`

## Estrutura do Projeto

O projeto está organizado em módulos funcionais, cada um responsável por uma área específica do sistema:

- **alunos**: Gerenciamento de estudantes
- **atividades**: Controle de atividades acadêmicas e ritualísticas
- **cursos**: Administração de cursos oferecidos
- **turmas**: Gerenciamento de turmas e períodos letivos
- [outros módulos]

## Desenvolvimento

### Linting e Formatação de Código

Este projeto usa Pylint e Flake8 para garantir a qualidade do código. Para executar os linters:

```bash
python scripts/lint.py
```

Recomendamos configurar seu editor para executar o linter automaticamente ao salvar os arquivos.

Para o VS Code, instale as extensões:
- Python (Microsoft)
- Pylint
- Flake8

As configurações recomendadas já estão no arquivo `.vscode/settings.json`.
```

## 7. Corrigindo o Arquivo verificar_arquivos_importantes_duplicados.py

Agora, vamos corrigir o problema específico que você encontrou no arquivo `scripts/verificar_arquivos_importantes_duplicados.py`:

```python:scripts/verificar_arquivos_importantes_duplicados.py
# Nas linhas 61-62, substitua:
("base.html", "omaum\\templates\\base.html"),
("home.html", "omaum\templates\home.html"),

# Por:
("base.html", r"omaum\templates\base.html"),
("home.html", r"omaum\templates\home.html"),



### Arquivo: requirements-dev.txt

text
asgiref==3.8.1
astroid==3.3.9
black==25.1.0
chardet==5.2.0
click==8.1.8
colorama==0.4.6
dill==0.3.9
Django==5.1.7
django-crispy-forms==2.3
django-debug-toolbar==5.1.0
django-extensions==3.2.3
django-widget-tweaks==1.5.0
Faker==37.1.0
flake8==7.2.0
isort==6.0.1
mccabe==0.7.0
mypy-extensions==1.0.0
packaging==24.2
pathspec==0.12.1
pillow==11.1.0
platformdirs==4.3.7
pycodestyle==2.13.0
pyflakes==3.3.2
pylint==3.3.6
reportlab==4.3.1
sqlparse==0.5.3
tomlkit==0.13.2
tzdata==2025.1
XlsxWriter==3.2.2




### Arquivo: requirements.txt

text
asgiref==3.8.1
chardet==5.2.0
Django==5.1.7
django-crispy-forms==2.3
django-debug-toolbar==5.1.0
django-extensions==3.2.3
django-widget-tweaks==1.5.0
pillow==11.1.0
reportlab==4.3.1
sqlparse==0.5.3
tzdata==2025.1




### Arquivo: script_revisao_projeto.py

python
import os
import chardet
import shutil


def collect_files_by_app(project_root):
    # Dicionário para armazenar arquivos por app/funcionalidade
    apps_files = {}
    for root, dirs, files in os.walk(project_root):
        # Ignorar diretórios de ambiente virtual e cache
        if "venv" in root or "__pycache__" in root:
            continue
        # Identificar o app/funcionalidade com base no caminho
        relative_path = os.path.relpath(root, project_root)
        app_name = (
            relative_path.split(os.path.sep)[0]
            if relative_path != "."
            else "core"
        )
        # Inicializar a estrutura para o app se ainda não existir
        if app_name not in apps_files:
            apps_files[app_name] = {
                "forms.py": [],
                "views.py": [],
                "urls.py": [],
                "models.py": [],
                "templates": [],
            }
        for file in files:
            if file in ["forms.py", "views.py", "urls.py", "models.py"]:
                apps_files[app_name][file].append(os.path.join(root, file))
            elif file.endswith(".html"):
                apps_files[app_name]["templates"].append(
                    os.path.join(root, file)
                )
    return apps_files


def write_file_contents(output_file, filepath):
    # Detectar codificação do arquivo
    with open(filepath, "rb") as raw_file:
        raw_data = raw_file.read()
        result = chardet.detect(raw_data)
        encoding = result["encoding"] or "utf-8"  # Fallback para utf-8
    try:
        with open(filepath, "r", encoding=encoding) as file:
            relative_path = os.path.relpath(filepath)
            output_file.write(f"\n\n### Arquivo: {relative_path}\n\n")
            # Determinar o tipo de linguagem para o bloco de código
            if filepath.endswith(".html"):
                language = "html"
            elif filepath.endswith(".py"):
                language = "python"
            else:
                language = "text"
            output_file.write(f"{language}\n")
            output_file.write(file.read())
            output_file.write("\n\n")
    except Exception as e:
        output_file.write(f"\n\n### Arquivo: {filepath}\n\n")
        output_file.write(f"\nErro ao ler o arquivo: {str(e)}\n\n")


def collect_root_files(project_root, output_dir):
    """Coleta arquivos da raiz do projeto Django."""
    output_filename = os.path.join(output_dir, "root_files_revisao.md")
    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write("# Arquivos da Raiz do Projeto Django\n")

        # Listar arquivos na raiz do projeto
        root_files = [
            f
            for f in os.listdir(project_root)
            if os.path.isfile(os.path.join(project_root, f))
            and not f.startswith(".")
        ]

        for file in root_files:
            filepath = os.path.join(project_root, file)
            write_file_contents(output_file, filepath)

        # Verificar e incluir arquivos estáticos
        static_dir = os.path.join(project_root, "static")
        if os.path.exists(static_dir) and os.path.isdir(static_dir):
            output_file.write("\n## Arquivos Estáticos\n")
            for root, dirs, files in os.walk(static_dir):
                for file in files:
                    filepath = os.path.join(root, file)
                    write_file_contents(output_file, filepath)

    print(f"Arquivos da raiz do projeto foram escritos em {output_filename}")


def generate_project_structure(project_root, output_dir):
    """Gera um arquivo com a estrutura completa do projeto."""
    output_filename = os.path.join(output_dir, "project_structure.md")
    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write("# Estrutura do Projeto Django\n\n")
        output_file.write("\n")

        for root, dirs, files in os.walk(project_root):
            # Ignorar diretórios de ambiente virtual e cache
            if "venv" in root or "__pycache__" in root:
                continue

            level = root.replace(project_root, "").count(os.sep)
            indent = " " * 4 * level
            output_file.write(f"{indent}{os.path.basename(root)}/\n")

            sub_indent = " " * 4 * (level + 1)
            for file in files:
                output_file.write(f"{sub_indent}{file}\n")

        output_file.write("\n")

    print(f"Estrutura do projeto foi escrita em {output_filename}")


def check_template_dirs(project_root, output_dir):
    """Verifica e documenta as configurações de diretórios de templates."""
    output_filename = os.path.join(output_dir, "template_dirs_check.md")
    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write("# Verificação de Diretórios de Templates\n\n")

        # Verificar settings.py para configurações de TEMPLATES
        settings_files = []
        for root, dirs, files in os.walk(project_root):
            if "settings.py" in files:
                settings_files.append(os.path.join(root, "settings.py"))

        if settings_files:
            output_file.write(
                "## Configurações de Templates no settings.py\n\n"
            )
            for settings_file in settings_files:
                write_file_contents(output_file, settings_file)

        # Listar todos os diretórios de templates encontrados
        output_file.write("\n## Diretórios de Templates Encontrados\n\n")
        template_dirs = []
        for root, dirs, files in os.walk(project_root):
            if "templates" in dirs:
                template_dir = os.path.join(root, "templates")
                template_dirs.append(template_dir)
                output_file.write(
                    f"- {os.path.relpath(template_dir, project_root)}\n"
                )

                # Listar arquivos de template neste diretório
                output_file.write("  Arquivos:\n")
                for template_root, template_dirs, template_files in os.walk(
                    template_dir
                ):
                    for file in template_files:
                        output_file.write(
                            f"  - {os.path.relpath(os.path.join(template_root, file), template_dir)}\n"
                        )

        # Verificar especificamente o template listar_alunos.html
        output_file.write("\n## Busca pelo template listar_alunos.html\n\n")
        found = False
        for root, dirs, files in os.walk(project_root):
            for file in files:
                if file == "listar_alunos.html":
                    found = True
                    output_file.write(
                        f"Encontrado em: {os.path.relpath(os.path.join(root, file), project_root)}\n"
                    )

        if not found:
            output_file.write(
                "O arquivo listar_alunos.html não foi encontrado no projeto.\n"
            )

    print(
        f"Verificação de diretórios de templates foi escrita em {output_filename}"
    )


def main():
    project_root = input("Digite o diretório raiz do seu projeto Django: ")
    output_dir = "revisao_projeto"
    # Criar diretório de saída se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Coletar arquivos por app
    apps_files = collect_files_by_app(project_root)
    for app_name, file_types in apps_files.items():
        # Verificar se há arquivos para este app
        has_files = any(files for files in file_types.values())
        if not has_files:
            continue
        output_filename = os.path.join(output_dir, f"{app_name}_revisao.md")
        with open(output_filename, "w", encoding="utf-8") as output_file:
            output_file.write(f"# Revisão da Funcionalidade: {app_name}\n")
            for file_type, file_paths in file_types.items():
                if not file_paths:
                    continue
                if file_type == "templates":
                    output_file.write(f"\n## Arquivos de Template:\n")
                else:
                    output_file.write(f"\n## Arquivos {file_type}:\n")
                for filepath in sorted(file_paths):
                    write_file_contents(output_file, filepath)
        print(
            f"Conteúdo da funcionalidade '{app_name}' foi escrito em {output_filename}"
        )

    # Coletar arquivos da raiz e arquivos estáticos
    collect_root_files(project_root, output_dir)

    # Gerar estrutura do projeto
    generate_project_structure(project_root, output_dir)

    # Verificar diretórios de templates
    check_template_dirs(project_root, output_dir)

    print(f"Revisão completa! Arquivos gerados no diretório '{output_dir}'")


if __name__ == "__main__":
    main()




### Arquivo: settings.py

python
# Configuração de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'debug.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'alunos': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'turmas': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Criar diretório de logs se não existir
import os
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)


## Arquivos Estáticos


### Arquivo: static\favicon.ico

text


### Arquivo: c:\projetos\omaum\static\favicon.ico


Erro ao ler o arquivo: 'charmap' codec can't decode byte 0x98 in position 615: character maps to <undefined>



### Arquivo: static\css\accessibility_fixes.css

text
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




### Arquivo: static\css\extra_styles.css

text
.list-group {
    position: absolute;
    z-index: 1000;
    width: 100%;
    max-height: 300px;
    overflow-y: auto;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.list-group-item-action:hover {
    background-color: #f8f9fa;
}

/* Garantir que o container do instrutor selecionado tenha a mesma largura do campo de pesquisa */
.selected-instructor-container {
    background-color: #f8f9fa;
    border-radius: 4px;
    padding: 10px;
    margin-top: 10px;
    width: 100%; /* Garante que ocupe toda a largura disponível */
    box-sizing: border-box; /* Inclui padding e border na largura total */
}

/* Estilo para a informação do instrutor selecionado */
.selected-instructor-info {
    font-size: 0.9rem;
    word-break: break-word; /* Evita que textos longos quebrem o layout */
}
/* Estilos para itens não elegíveis na busca de instrutores */
.list-group-item.ineligible {
    opacity: 0.7;
    background-color: #fff0f0;
    cursor: not-allowed;
}

.list-group-item.ineligible:hover {
    background-color: #ffe0e0;
}

/* Estilo para o ícone X vermelho */
.list-group-item .text-danger i {
    font-size: 1.1em;
}



### Arquivo: static\css\Piscar.css

text
<!-- No bloco head ou em um arquivo CSS separado -->
<style>
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .blink {
        animation: blink 1s linear infinite;
    }
</style>




### Arquivo: static\css\style.css

text
/* Estilos personalizados para o sistema OMAUM */




### Arquivo: static\js\aluno-search.js

text
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-aluno');
    const searchResults = document.getElementById('search-results');
    
    if (!searchInput || !searchResults) return;
    
    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        
        const query = this.value.trim();
        
        // Clear results if query is too short
        if (query.length < 2) {
            searchResults.innerHTML = '';
            searchResults.style.display = 'none';
            return;
        }
        
        // Set a timeout to avoid making too many requests
        searchTimeout = setTimeout(function() {
            // Show loading indicator
            searchResults.innerHTML = '<div class="list-group-item text-muted">Buscando...</div>';
            searchResults.style.display = 'block';
            
            // Get CSRF token
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch(`/alunos/search/?q=${encodeURIComponent(query)}`, {
                headers: {
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                searchResults.innerHTML = '';
                
                if (data.error) {
                    // Handle error response
                    searchResults.innerHTML = `<div class="list-group-item text-danger">Erro ao buscar alunos: ${data.error}</div>`;
                    return;
                }
                
                if (data.length === 0) {
                    searchResults.innerHTML = '<div class="list-group-item">Nenhum aluno encontrado</div>';
                    return;
                }
                
                // Display results
                data.forEach(aluno => {
                    const item = document.createElement('a');
                    item.href = '#';
                    item.className = 'list-group-item list-group-item-action';
                    item.innerHTML = `
                        <div class="d-flex justify-content-between">
                            <div>${aluno.nome}</div>
                            <div class="text-muted">
                                <small>CPF: ${aluno.cpf}</small>
                                ${aluno.numero_iniciatico !== "N/A" ? `<small class="ms-2">NÂº: ${aluno.numero_iniciatico}</small>` : ''}
                            </div>
                        </div>
                    `;
                    
                    // Add click event to select this aluno
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        selectAluno(aluno);
                    });
                    
                    searchResults.appendChild(item);
                });
            })
            .catch(error => {
                console.error('Error:', error);
                searchResults.innerHTML = '<div class="list-group-item text-danger">Erro ao buscar alunos</div>';
            });
        }, 300);
    });
    
    // Hide results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });
    
    // Function to select an aluno
    function selectAluno(aluno) {
        // Get the hidden input field for the aluno ID
        const alunoIdField = document.getElementById('id_aluno');
        if (alunoIdField) {
            alunoIdField.value = aluno.cpf;
        }
        
        // Update the search input with the selected aluno's name
        searchInput.value = aluno.nome;
        
        // Hide the search results
        searchResults.style.display = 'none';
        
        // Trigger any additional actions needed when an aluno is selected
        const event = new CustomEvent('alunoSelected', { detail: aluno });
        document.dispatchEvent(event);
    }
});




### Arquivo: static\js\csrf_refresh.js

text
// Variáveis para controle de inatividade
let inactivityTimer;
const inactivityTimeout = 30 * 60 * 1000; // 30 minutos em milissegundos

// Função para verificar o status da sessão e do token CSRF
function checkSessionStatus() {
    // Fazer uma requisição AJAX para verificar o status da sessão
    fetch('/core/csrf_check/', {  // Corrigir o caminho para incluir 'core/'
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            // Se a resposta não for OK, mostrar alerta de sessão expirada
            showSessionExpiredAlert();
        }
    })
    .catch(error => {
        console.error('Erro ao verificar status da sessão:', error);
        // Em caso de erro, também mostrar o alerta
        showSessionExpiredAlert();
    });
}

// Função para mostrar alerta de sessão expirada
function showSessionExpiredAlert() {
    // Verificar se o alerta já existe para não duplicar
    if (!document.getElementById('session-expired-alert')) {
        const alertDiv = document.createElement('div');
        alertDiv.id = 'session-expired-alert';
        alertDiv.className = 'alert alert-warning alert-dismissible fade show session-alert';
        alertDiv.innerHTML = `
            <strong>Atenção!</strong> Sua sessão pode ter expirado devido à inatividade. 
            <button type="button" class="btn btn-sm btn-primary mx-2" onclick="refreshPage()">Recarregar Página</button>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
        `;
        
        // Estilo para o alerta fixo no topo da página
        alertDiv.style.position = 'fixed';
        alertDiv.style.top = '10px';
        alertDiv.style.left = '50%';
        alertDiv.style.transform = 'translateX(-50%)';
        alertDiv.style.zIndex = '9999';
        alertDiv.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
        
        document.body.appendChild(alertDiv);
    }
}

// Função para recarregar a página
function refreshPage() {
    window.location.reload();
}

// Função para reiniciar o timer de inatividade
function resetInactivityTimer() {
    // Limpar o timer existente
    clearTimeout(inactivityTimer);
    
    // Iniciar um novo timer
    inactivityTimer = setTimeout(() => {
        // Após 30 minutos de inatividade, verificar a sessão
        checkSessionStatus();
    }, inactivityTimeout);
}

// Lista de eventos que indicam atividade do usuário
const userActivityEvents = [
    'mousedown', 'mousemove', 'keypress', 
    'scroll', 'touchstart', 'click', 'keydown'
];

// Inicializar o monitoramento de atividade do usuário
function initInactivityMonitoring() {
    // Adicionar listeners para todos os eventos de atividade
    userActivityEvents.forEach(eventType => {
        document.addEventListener(eventType, resetInactivityTimer, { passive: true });
    });
    
    // Iniciar o timer pela primeira vez
    resetInactivityTimer();
}

// Também verificar quando o usuário retorna à aba
document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        // Reiniciar o timer quando o usuário volta para a aba
        resetInactivityTimer();
    }
});

// Inicializar o monitoramento de inatividade quando a página carrega
document.addEventListener('DOMContentLoaded', function() {
    // Iniciar o monitoramento de inatividade
    initInactivityMonitoring();
});



### Arquivo: static\js\instrutor_search.js

text
/**
 * Módulo para gerenciamento de busca e seleção de instrutores
 */
const InstrutorSearch = (function() {
    // Variáveis privadas do módulo
    let instrutoresElegiveis = [];
    let csrfToken;

    /**
     * Inicializa o módulo de busca de instrutores
     * @param {string} csrfTokenValue - Token CSRF para requisições AJAX
     */
    function init(csrfTokenValue) {
        csrfToken = csrfTokenValue;
        carregarInstrutoresElegiveis();
        
        // Configurar os campos de busca
        setupInstructorSearch(
            'search-instrutor',
            'search-results-instrutor',
            'selected-instrutor-container',
            'selected-instrutor-info',
            'id_instrutor'
        );
        
        setupInstructorSearch(
            'search-instrutor-auxiliar',
            'search-results-instrutor-auxiliar',
            'selected-instrutor-auxiliar-container',
            'selected-instrutor-auxiliar-info',
            'id_instrutor_auxiliar'
        );
        
        setupInstructorSearch(
            'search-auxiliar-instrucao',
            'search-results-auxiliar-instrucao',
            'selected-auxiliar-instrucao-container',
            'selected-auxiliar-instrucao-info',
            'id_auxiliar_instrucao'
        );
        
        // Configurar validação do formulário
        setupFormValidation();
    }

    /**
     * Carrega a lista de instrutores elegíveis via AJAX
     */
    function carregarInstrutoresElegiveis() {
        fetch('/alunos/api/search-instrutores/', {
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            instrutoresElegiveis = data;
            console.log(`Carregados ${instrutoresElegiveis.length} instrutores elegíveis`);
        })
        .catch(error => {
            console.error('Erro ao carregar instrutores elegíveis:', error);
        });
    }

    /**
     * Configura a busca de instrutores para um campo específico
     */
    function setupInstructorSearch(searchId, resultsId, containerId, infoId, selectId) {
        const searchInput = document.getElementById(searchId);
        const searchResults = document.getElementById(resultsId);
        const selectedContainer = document.getElementById(containerId);
        const selectedInfo = document.getElementById(infoId);
        const selectElement = document.getElementById(selectId);
        
        // Criar elemento para mensagens de erro
        const errorElement = document.createElement('div');
        errorElement.className = 'alert alert-danger mt-2 d-none';
        selectedContainer.after(errorElement);
        
        let searchTimeout;
        
        // Configurar eventos de busca
        searchInput.addEventListener('input', handleSearchInput);
        
        // Ocultar resultados ao clicar fora
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
        
        /**
         * Manipula o evento de input no campo de busca
         */
        function handleSearchInput() {
            clearTimeout(searchTimeout);
            
            const query = this.value.trim();
            
            // Limpar mensagens de erro
            errorElement.classList.add('d-none');
            
            // Limpar resultados se a consulta for muito curta
            if (query.length < 2) {
                searchResults.innerHTML = '';
                searchResults.style.display = 'none';
                return;
            }
            
            // Definir timeout para evitar muitas requisições
            searchTimeout = setTimeout(function() {
                // Mostrar indicador de carregamento
                searchResults.innerHTML = '<div class="list-group-item text-muted">Buscando...</div>';
                searchResults.style.display = 'block';
                
                // Buscar alunos que correspondem à consulta
                fetch(`/alunos/search/?q=${encodeURIComponent(query)}`, {
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    searchResults.innerHTML = '';
                    
                    if (data.error) {
                        searchResults.innerHTML = `<div class="list-group-item text-danger">Erro ao buscar alunos: ${data.error}</div>`;
                        return;
                    }
                    
                    if (data.length === 0) {
                        searchResults.innerHTML = '<div class="list-group-item">Nenhum aluno encontrado</div>';
                        return;
                    }
                    
                    // Exibir resultados
                    data.forEach(aluno => {
                        const item = document.createElement('a');
                        item.href = '#';
                        item.className = 'list-group-item list-group-item-action';
                        item.innerHTML = `
                            <div class="d-flex justify-content-between">
                                <div>${aluno.nome}</div>
                                <div class="text-muted">
                                    <small>CPF: ${aluno.cpf}</small>
                                    ${aluno.numero_iniciatico !== "N/A" ? `<small class="ms-2">Nº: ${aluno.numero_iniciatico}</small>` : ''}
                                </div>
                            </div>
                        `;
                        
                        // Adicionar evento de clique para selecionar o aluno
                        item.addEventListener('click', function(e) {
                            e.preventDefault();
                            verificarElegibilidadeInstrutor(aluno);
                        });
                        
                        searchResults.appendChild(item);
                    });
                })
                .catch(error => {
                    console.error('Error:', error);
                    searchResults.innerHTML = '<div class="list-group-item text-danger">Erro ao buscar alunos</div>';
                });
            }, 300);
        }
        
        /**
         * Verifica se um aluno pode ser instrutor
         * @param {Object} aluno - Dados do aluno a ser verificado
         */
        function verificarElegibilidadeInstrutor(aluno) {
            // Verificar se o aluno já foi selecionado em outro campo
            const outrosSelects = Array.from(document.querySelectorAll('select[name^="instrutor"]')).filter(s => s.id !== selectId);
            const jaEstaEmUso = outrosSelects.some(select => select.value === aluno.cpf);
            
            if (jaEstaEmUso) {
                errorElement.textContent = `O aluno ${aluno.nome} já está selecionado como instrutor em outro campo.`;
                errorElement.classList.remove('d-none');
                return;
            }
            
            // Mostrar mensagem de carregamento
            errorElement.innerHTML = `<div class="spinner-border spinner-border-sm text-primary me-2" role="status"></div> Verificando elegibilidade de ${aluno.nome}...`;
            errorElement.classList.remove('d-none');
            errorElement.classList.remove('alert-danger');
            errorElement.classList.add('alert-info');
            
            // Verificar se o aluno pode ser instrutor
            fetch(`/alunos/api/verificar-elegibilidade/${aluno.cpf}/`)
                .then(response => response.json())
                .then(data => {
                    if (!data.elegivel) {
                        errorElement.textContent = data.motivo || "Este aluno não pode ser instrutor.";
                        errorElement.classList.remove('d-none');
                        console.error(`Aluno inelegível: ${data.motivo}`);
                    } else {
                        errorElement.classList.add('d-none');
                        console.log("Aluno elegível para ser instrutor");
                        selecionarInstrutor(aluno);
                    }
                })
                .catch(error => {
                    console.error("Erro ao verificar elegibilidade:", error);
                    errorElement.textContent = "Erro na busca: Não foi possível verificar a elegibilidade.";
                    errorElement.classList.remove('d-none');
                });        }
        
        /**
         * Seleciona um instrutor após verificação de elegibilidade
         * @param {Object} aluno - Dados do aluno a ser selecionado
         */
        function selecionarInstrutor(aluno) {
            // Limpar as opções existentes no select
            while (selectElement.options.length > 0) {
                selectElement.remove(0);
            }
            
            // Criar e adicionar a opção para o aluno selecionado
            const option = new Option(aluno.nome, aluno.cpf, true, true);
            selectElement.appendChild(option);
            
            // Atualizar a interface
            searchInput.value = aluno.nome;
            selectedInfo.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <strong>${aluno.nome}</strong><br>
                        CPF: ${aluno.cpf}<br>
                        ${aluno.numero_iniciatico !== "N/A" ? `Número Iniciático: ${aluno.numero_iniciatico}` : ''}
                    </div>
                    <button type="button" class="btn btn-sm btn-outline-danger" id="remove-${selectId}">
                        <i class="fas fa-times"></i> Remover
                    </button>
                </div>
            `;
            
            selectedContainer.classList.remove('d-none');
            searchResults.style.display = 'none';
            errorElement.classList.add('d-none');
            
            // Adicionar evento para remover o instrutor
            document.getElementById(`remove-${selectId}`).addEventListener('click', function() {
                selectElement.value = '';
                searchInput.value = '';
                selectedContainer.classList.add('d-none');
            });
        }
    }

    /**
     * Configura a validação do formulário antes do envio
     */
    function setupFormValidation() {
        const form = document.querySelector('form');
        form.addEventListener('submit', function(e) {
            // Verificar se há erros visíveis
            const errosVisiveis = document.querySelectorAll('.alert-danger:not(.d-none)');
            if (errosVisiveis.length > 0) {
                e.preventDefault();
                alert('Por favor, corrija os erros antes de enviar o formulário.');
                return;
            }
            
            // Verificar se os instrutores são diferentes entre si
            const instrutorPrincipal = document.getElementById('id_instrutor').value;
            const instrutorAuxiliar = document.getElementById('id_instrutor_auxiliar').value;
            const auxiliarInstrucao = document.getElementById('id_auxiliar_instrucao').value;
            
            const instrutoresSelecionados = [instrutorPrincipal, instrutorAuxiliar, auxiliarInstrucao].filter(Boolean);
            const instrutoresUnicos = new Set(instrutoresSelecionados);
            
            if (instrutoresSelecionados.length !== instrutoresUnicos.size) {
                e.preventDefault();
                alert('Não é possível selecionar o mesmo aluno para diferentes funções de instrução.');
                return;
            }
            
            // Mostrar os selects antes do envio
            document.getElementById('id_instrutor').style.display = '';
            document.getElementById('id_instrutor_auxiliar').style.display = '';
            document.getElementById('id_auxiliar_instrucao').style.display = '';
        });
    }

    // API pública do módulo
    return {
        init: init
    };
})();




### Arquivo: static\js\turmas\instrutor_search.js

text
/**
 * Módulo para busca e seleção de instrutores
 */
const InstrutorSearch = (function() {
    let csrfToken = '';
    let showAllStudents = false;
    let ignoreEligibility = false;
    
    // Função para verificar elegibilidade
    function verificarElegibilidade(cpf, tipoInstrutor) {
        console.log(`Verificando elegibilidade do instrutor ${tipoInstrutor} com CPF: ${cpf}`);
        
        const errorElement = document.getElementById(`${tipoInstrutor}-error`);
        if (!errorElement) {
            console.error(`Elemento de erro não encontrado para ${tipoInstrutor}`);
            return;
        }
        
        // Limpar mensagem de erro anterior
        errorElement.textContent = '';
        errorElement.classList.add('d-none');
        
        // Se estamos ignorando verificações de elegibilidade, não fazer a verificação
        if (ignoreEligibility) {
            console.log('Ignorando verificação de elegibilidade (modo de depuração ativo)');
            return;
        }
        
        // Fazer requisição para verificar elegibilidade
        fetch(`/alunos/api/verificar-elegibilidade/${cpf}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro HTTP: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log(`Resposta da verificação de elegibilidade:`, data);
                
                if (!data.elegivel) {
                    // Mostrar mensagem de erro específica
                    errorElement.textContent = data.motivo || "Este aluno não pode ser instrutor.";
                    errorElement.classList.remove('d-none');
                    
                    // Se estamos mostrando todos os alunos, não bloqueamos a seleção
                    if (!showAllStudents) {
                        // Limpar seleção
                        const selectElement = document.getElementById(`id_${tipoInstrutor}`);
                        if (selectElement) {
                            selectElement.value = '';
                        }
                    }
                }
            })
            .catch(error => {
                console.error(`Erro ao verificar elegibilidade: ${error.message}`);
                errorElement.textContent = `Erro na busca: ${error.message}`;
                errorElement.classList.remove('d-none');
            });
    }
    
    // Função para selecionar um instrutor
    function selectInstructor(cpf, nome, numero, tipoInstrutor) {
        console.log(`Selecionando ${tipoInstrutor}: ${nome} (${cpf})`);
        
        // Atualizar o select oculto
        const selectElement = document.getElementById(`id_${tipoInstrutor}`);
        if (selectElement) {
            selectElement.value = cpf;
        }
        
        // Atualizar a exibição
        const containerElement = document.getElementById(`selected-${tipoInstrutor}-container`);
        const infoElement = document.getElementById(`selected-${tipoInstrutor}-info`);
        
        if (containerElement && infoElement) {
            infoElement.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <strong>${nome}</strong><br>
                        CPF: ${cpf} | Nº Iniciático: ${numero || 'N/A'}
                    </div>
                    <button type="button" class="btn btn-sm btn-danger remove-instructor">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
            
            containerElement.classList.remove('d-none');
            
            // Adicionar evento para remover instrutor
            const removeButton = infoElement.querySelector('.remove-instructor');
            if (removeButton) {
                removeButton.addEventListener('click', function() {
                    selectElement.value = '';
                    containerElement.classList.add('d-none');
                    infoElement.innerHTML = '';
                    
                    // Limpar mensagem de erro
                    const errorElement = document.getElementById(`${tipoInstrutor}-error`);
                    if (errorElement) {
                        errorElement.textContent = '';
                        errorElement.classList.add('d-none');
                    }
                });
            }
        }
        
        // Verificar elegibilidade
        verificarElegibilidade(cpf, tipoInstrutor);
    }
    
    // Função para configurar a busca de instrutores
    function setupInstructorSearch(tipoInstrutor) {
        console.log(`Configurando busca para ${tipoInstrutor}`);
        
        const searchInput = document.getElementById(`search-${tipoInstrutor}`);
        const searchResults = document.getElementById(`search-results-${tipoInstrutor}`);
        
        if (!searchInput || !searchResults) {
            console.error(`Elementos de busca não encontrados para ${tipoInstrutor}`);
            return;
        }
        
        // Evento de digitação
        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            
            if (query.length < 2) {
                searchResults.style.display = 'none';
                return;
            }
            
            // Fazer requisição para buscar alunos
            const url = showAllStudents || ignoreEligibility ? 
                `/alunos/search/?q=${encodeURIComponent(query)}` : 
                `/alunos/api/search-instrutores/?q=${encodeURIComponent(query)}`;
            
            fetch(url, {
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log(`Resultados da busca para ${tipoInstrutor}:`, data);
                
                // Limpar resultados anteriores
                searchResults.innerHTML = '';
                
                if (data.length === 0) {
                    searchResults.innerHTML = '<div class="list-group-item">Nenhum resultado encontrado</div>';
                    searchResults.style.display = 'block';
                    return;
                }
                
                // Adicionar resultados
                data.forEach(aluno => {
                    const item = document.createElement('a');
                    item.href = '#';
                    item.className = 'list-group-item list-group-item-action ';
                    item.dataset.cpf = aluno.cpf;
                    item.dataset.nome = aluno.nome;
                    item.dataset.numero = aluno.numero_iniciatico;
                    
                    item.innerHTML = `
                        <strong>${aluno.nome}</strong> - Nº ${aluno.numero_iniciatico || 'N/A'} (CPF: ${aluno.cpf})
                    `;
                    
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        selectInstructor(
                            this.dataset.cpf,
                            this.dataset.nome,
                            this.dataset.numero,
                            tipoInstrutor
                        );
                        searchResults.style.display = 'none';
                        searchInput.value = '';
                    });
                    
                    searchResults.appendChild(item);
                });
                
                searchResults.style.display = 'block';
            })
            .catch(error => {
                console.error(`Erro na busca de ${tipoInstrutor}: ${error.message}`);
                searchResults.innerHTML = `<div class="list-group-item text-danger">Erro na busca: ${error.message}</div>`;
                searchResults.style.display = 'block';
            });
        });
        
        // Esconder resultados ao clicar fora
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
    }
    
    return {
        init: function(token, allowAllStudents = false) {
            console.log('Inicializando módulo de busca de instrutores');
            csrfToken = token;
            showAllStudents = allowAllStudents;
            
            // Configurar busca para cada tipo de instrutor
            setupInstructorSearch('instrutor');
            setupInstructorSearch('instrutor-auxiliar');
            setupInstructorSearch('auxiliar-instrucao');
            
            console.log(`Modo de exibição: ${showAllStudents ? 'todos os alunos' : 'apenas elegíveis'}`);
            
            // Verificar se o modo de depuração está ativo
            const debugSwitch = document.getElementById('ignore-eligibility');
            if (debugSwitch) {
                ignoreEligibility = debugSwitch.checked;
                console.log(`Modo de depuração: ${ignoreEligibility ? 'ativo' : 'inativo'}`);
            }
        },
        
        setIgnoreEligibility: function(value) {
            ignoreEligibility = value;
            console.log(`Modo de depuração ${ignoreEligibility ? 'ativado' : 'desativado'}`);
        }
    };
})();

