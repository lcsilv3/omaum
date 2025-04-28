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
            and f != "db.sqlite3"  # Excluir o arquivo db.sqlite3
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
skip-string-normalization = true
line-length = 88
exclude = '''
/(
    \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
  | alunos/views.py  # Adicione os arquivos específicos que você quer excluir
)/
'''



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

## Convenções de Código

### Nomenclatura de Parâmetros em URLs e Views

Para manter o código claro e evitar ambiguidades, seguimos estas convenções:

1. **Parâmetros de ID em URLs e Views**:
   - Usamos o formato `modelo_id` (ex: `turma_id`, `aluno_id`, `curso_id`)
   - Exemplo: `def detalhar_turma(request, turma_id):`

2. **Referências em Templates**:
   - Nos templates, continuamos usando o atributo `id` do objeto
   - Exemplo: `{% url 'turmas:detalhar_turma' turma.id %}`

3. **Múltiplos IDs em uma mesma View**:
   - Quando uma view precisa de múltiplos IDs, cada um tem seu próprio nome descritivo
   - Exemplo: `def cancelar_matricula(request, turma_id, aluno_cpf):`

Esta convenção torna o código mais legível, facilita a manutenção e reduz a chance de erros quando o sistema cresce e se torna mais complexo.
```



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



## Arquivos Estáticos


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




### Arquivo: static\css\alunos.css

text
/* Estilos para o módulo de alunos */

/* Cores para os cards */
.card.border-primary {
    border-color: #007bff !important;
}

.card.border-success {
    border-color: #28a745 !important;
}

.card.border-info {
    border-color: #17a2b8 !important;
}

.card.border-warning {
    border-color: #ffc107 !important;
}

.card.border-danger {
    border-color: #dc3545 !important;
}

.card.border-secondary {
    border-color: #6c757d !important;
}

/* Estilos para campos de formulário */
.form-control:focus {
    border-color: #80bdff;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

/* Estilos para a foto do aluno */
.foto-container {
    border-style: dashed !important;
    border-color: #007bff !important;
    border-width: 2px !important;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Estilos para informações médicas */
.info-medica {
    background-color: #f8f9fa;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 10px;
}

/* Estilos para badges de situação */
.badge-situacao {
    font-size: 0.9em;
    padding: 5px 8px;
}

/* Estilos para listas de turmas */
.lista-turmas {
    max-height: 300px;
    overflow-y: auto;
}

/* Estilos responsivos */
@media (max-width: 768px) {
    .d-flex.justify-content-between {
        flex-direction: column;
        gap: 10px;
    }
    
    .d-flex.justify-content-between div {
        display: flex;
        gap: 10px;
    }
}



### Arquivo: static\css\extra_styles.css

text
/* Adicionar estas regras para corrigir problemas de z-index e posicionamento */
.select2-container {
    z-index: 1050;
}

.select2-container--open .select2-dropdown {
    z-index: 1051;
}

/* Corrigir o posicionamento do dropdown em relação ao campo de busca */
.select2-container--bootstrap4 .select2-dropdown {
    border-color: #ced4da;
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

/* Garantir que o container pai tenha posição relativa */
.select2-container--bootstrap4 {
    width: 100% !important;
}

/* Melhorar a aparência dos itens selecionados */
.select2-container--bootstrap4 .select2-selection--single {
    height: calc(1.5em + 0.75rem + 2px) !important;
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
}

/* Corrigir o problema de sobreposição com outros elementos */
.select2-container--bootstrap4 .select2-selection__arrow {
    height: 38px !important;
}

/* Garantir que os resultados da busca apareçam corretamente */
.list-group {
    position: absolute;
    z-index: 1060;
    width: 100%;
    max-height: 300px;
    overflow-y: auto;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Corrigir posicionamento dos containers de seleção */
#selected-instrutor-container,
#selected-instrutor-auxiliar-container,
#selected-auxiliar-instrucao-container {
    position: relative;
    margin-top: 10px;
    width: 100%;
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




### Arquivo: static\css\styles.css

text
/* OMAUM - Sistema de Gestão de Iniciados */
/* Estilos globais complementares ao Bootstrap */

/* ============= Estilos Globais ============= */
:root {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
    --success-color: #198754;
    --info-color: #0dcaf0;
    --warning-color: #ffc107;
    --danger-color: #dc3545;
    --light-color: #f8f9fa;
    --dark-color: #212529;
    --body-bg: #f5f8fa;
    --sidebar-width: 250px;
}

body {
    background-color: var(--body-bg);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #333;
    line-height: 1.6;
}

/* ============= Componentes do Layout ============= */
.navbar-brand {
    font-weight: 600;
    letter-spacing: 0.5px;
}

.footer {
    margin-top: 2rem;
    padding: 1rem 0;
    border-top: 1px solid #e7e7e7;
    font-size: 0.9rem;
}

/* ============= Cards e Containers ============= */
.card {
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    margin-bottom: 1.5rem;
    border: none;
}

.card-header {
    font-weight: 600;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    background-color: #fff;
    border-top-left-radius: 0.5rem !important;
    border-top-right-radius: 0.5rem !important;
}

.card-header.bg-primary, 
.card-header.bg-success, 
.card-header.bg-info, 
.card-header.bg-warning, 
.card-header.bg-danger {
    border-bottom: none;
}

.message-container {
    position: relative;
    z-index: 1000;
}

.message-container .alert {
    margin-bottom: 0.5rem;
    border-radius: 0.25rem;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* ============= Formulários ============= */
.form-control:focus, 
.form-select:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.15);
}

.form-control, .form-select {
    border-radius: 0.375rem;
}

.invalid-feedback {
    font-size: 0.85rem;
}

.form-check-input:checked {
    background-color: var(--primary-color);
    border-color: var(--primary-color);
}

.form-label {
    margin-bottom: 0.5rem;
    font-weight: 500;
}

/* Estilização do Select2 */
.select2-container--bootstrap4 .select2-selection--single {
    height: calc(1.5em + 0.75rem + 2px) !important;
}

.select2-container--bootstrap4 .select2-selection--multiple {
    min-height: calc(1.5em + 0.75rem + 2px) !important;
}

/* ============= Tabelas ============= */
.table {
    border-collapse: separate;
    border-spacing: 0;
}

.table-striped>tbody>tr:nth-of-type(odd)>* {
    background-color: rgba(0, 0, 0, 0.02);
}

.table thead th {
    background-color: #f8f9fa;
    font-weight: 600;
    border-bottom-width: 1px;
}

/* ============= Badges e States ============= */
.status-badge {
    padding: 0.35em 0.65em;
    border-radius: 0.375rem;
    font-weight: 600;
    font-size: 0.75em;
}

/* Badges para diferentes status */
.status-active {
    background-color: rgba(25, 135, 84, 0.15);
    color: var(--success-color);
}

.status-inactive {
    background-color: rgba(108, 117, 125, 0.15);
    color: var(--secondary-color);
}

.status-pending {
    background-color: rgba(255, 193, 7, 0.15);
    color: #997404;
}

/* ============= Media Queries ============= */
@media (max-width: 767.98px) {
    .card-header, .card-body, .card-footer {
        padding: 0.75rem;
    }
    
    .table-responsive {
        border-radius: 0.5rem;
    }
    
    .navbar-brand {
        font-size: 1.1rem;
    }
}

/* ============= Utilitários Adicionais ============= */
.rounded-custom {
    border-radius: 0.5rem !important;
}

.text-small {
    font-size: 0.85rem;
}

.text-xs {
    font-size: 0.75rem;
}
/* Estilos personalizados para o sistema OMAUM */




### Arquivo: static\css\turmas.css

text
/* Estilos para o módulo de turmas */

/* Cores para os cards */
.card.border-primary {
    border-color: #007bff !important;
}

.card.border-success {
    border-color: #28a745 !important;
}

.card.border-info {
    border-color: #17a2b8 !important;
}

.card.border-warning {
    border-color: #ffc107 !important;
}

.card.border-danger {
    border-color: #dc3545 !important;
}

/* Estilos para a busca de instrutores */
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

/* Estilos para o container de instrutor selecionado */
#selected-instrutor-container,
#selected-instrutor-auxiliar-container,
#selected-auxiliar-instrucao-container {
    background-color: #f8f9fa;
    border-color: #28a745 !important;
}

/* Estilos para mensagens de erro */
#instrutor-error,
#instrutor-auxiliar-error,
#auxiliar-instrucao-error {
    margin-top: 0.5rem;
}

/* Garantir que o dropdown do Select2 seja exibido corretamente */
.select2-container--bootstrap4 .select2-dropdown {
    border-color: #ced4da;
    border-radius: 0.25rem;
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
    z-index: 1060; /* Garantir que apareça acima de outros elementos */
}

/* Melhorar a visibilidade dos resultados da busca */
.select2-container--bootstrap4 .select2-results__option {
    padding: 0.375rem 0.75rem;
    color: #212529;
}

.select2-container--bootstrap4 .select2-results__option--highlighted[aria-selected] {
    background-color: #007bff;
    color: white;
}

/* Garantir que o campo de busca seja visível */
.select2-search--dropdown .select2-search__field {
    width: 100%;
    padding: 0.375rem 0.75rem;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
}



### Arquivo: static\css\components\dias-semana.css

text
/* Estilos do componente Dias da Semana */
.dias-semana-select {
    width: 100%;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
    min-height: 38px;
    padding: 0.375rem 0.75rem;
    background-color: #fff;
    cursor: pointer;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    position: relative;
}

.dias-semana-select:hover {
    border-color: #adb5bd;
}

.dias-semana-select.focus {
    border-color: #80bdff;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.dias-semana-container {
    display: none;
    position: absolute;
    width: 100%;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
    max-height: 200px;
    overflow-y: auto;
    z-index: 9999;
    background-color: #fff;
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.dias-semana-item {
    display: block;
    padding: 0.5rem 1rem;
    width: 100%;
    text-align: left;
    border: none;
    background: none;
    cursor: pointer;
}

.dias-semana-item:hover {
    background-color: #f8f9fa;
}

.dias-semana-item.selected {
    background-color: #e9ecef;
    font-weight: bold;
    color: #495057;
}

.dias-semana-item input {
    margin-right: 8px;
}

.dropdown-arrow {
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
    border-style: solid;
    border-width: 5px 5px 0 5px;
    border-color: #888 transparent transparent transparent;
    pointer-events: none;
}



### Arquivo: static\img\favicon.ico

text


### Arquivo: c:\projetos\omaum\static\img\favicon.ico


Erro ao ler o arquivo: 'charmap' codec can't decode byte 0x98 in position 615: character maps to <undefined>



### Arquivo: static\img\logo.png

text


### Arquivo: c:\projetos\omaum\static\img\logo.png


Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte



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



### Arquivo: static\js\inicializar_select2.js

text
/**
 * Inicialização global do Select2 para o sistema OMAUM
 * Este arquivo centraliza a configuração do Select2 para garantir consistência
 */
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se o jQuery e o Select2 estão disponíveis
    if (typeof $ === 'function' && typeof $.fn.select2 === 'function') {
        // Inicializar todos os elementos com classe select2
        $('.select2').each(function() {
            // Verificar se o elemento já foi inicializado
            if (!$(this).hasClass('select2-hidden-accessible')) {
                $(this).select2({
                    theme: 'bootstrap4',
                    width: '100%',
                    language: {
                        noResults: function() {
                            return "Nenhum resultado encontrado";
                        },
                        searching: function() {
                            return "Buscando...";
                        }
                    }
                });
            }
        });
        
        // Corrigir problemas de z-index em modais
        $(document).on('shown.bs.modal', function() {
            $('.select2-container').css('z-index', '1060');
        });
        
        // Garantir que os Select2 sejam destruídos corretamente antes de reinicializar
        $(document).on('hidden.bs.modal', function() {
            $('.select2-hidden-accessible', this).select2('destroy');
        });
        
        console.log('Select2 inicializado globalmente');
    } else {
        console.warn('jQuery ou Select2 não estão disponíveis. A inicialização global do Select2 foi ignorada.');
    }
});



### Arquivo: static\js\instrutor_search.js

text
document.addEventListener('DOMContentLoaded', function() {
    // Configuração para os três tipos de instrutores
    const instrutorTypes = [
        {
            searchInputId: 'search-instrutor',
            resultsContainerId: 'search-results-instrutor',
            selectedContainerId: 'selected-instrutor-container',
            selectedInfoId: 'selected-instrutor-info',
            errorContainerId: 'instrutor-error',
            selectId: 'id_instrutor',
            clearBtnId: 'clear-instrutor-btn'
        },
        {
            searchInputId: 'search-instrutor-auxiliar',
            resultsContainerId: 'search-results-instrutor-auxiliar',
            selectedContainerId: 'selected-instrutor-auxiliar-container',
            selectedInfoId: 'selected-instrutor-auxiliar-info',
            errorContainerId: 'instrutor-auxiliar-error',
            selectId: 'id_instrutor_auxiliar',
            clearBtnId: 'clear-instrutor-auxiliar-btn'
        },
        {
            searchInputId: 'search-auxiliar-instrucao',
            resultsContainerId: 'search-results-auxiliar-instrucao',
            selectedContainerId: 'selected-auxiliar-instrucao-container',
            selectedInfoId: 'selected-auxiliar-instrucao-info',
            errorContainerId: 'auxiliar-instrucao-error',
            selectId: 'id_auxiliar_instrucao',
            clearBtnId: 'clear-auxiliar-instrucao-btn'
        }
    ];

    // Inicializar cada tipo de instrutor
    instrutorTypes.forEach(config => {
        initInstrutorSearch(config);
    });

    // Função para inicializar a busca de instrutor
    function initInstrutorSearch(config) {
        const searchInput = document.getElementById(config.searchInputId);
        const resultsContainer = document.getElementById(config.resultsContainerId);
        const selectedContainer = document.getElementById(config.selectedContainerId);
        const selectedInfo = document.getElementById(config.selectedInfoId);
        const errorContainer = document.getElementById(config.errorContainerId);
        const selectElement = document.getElementById(config.selectId);
        
        // Adicionar botão de limpar se não existir
        let clearBtn = document.getElementById(config.clearBtnId);
        if (!clearBtn && selectedContainer) {
            clearBtn = document.createElement('button');
            clearBtn.id = config.clearBtnId;
            clearBtn.type = 'button';
            clearBtn.className = 'btn btn-sm btn-outline-secondary mt-2';
            clearBtn.textContent = 'Limpar seleção';
            clearBtn.style.display = 'none';
            selectedContainer.parentNode.insertBefore(clearBtn, selectedContainer.nextSibling);
        }

        if (!searchInput || !resultsContainer || !selectedContainer || !selectedInfo || !selectElement) {
            console.error('Elementos necessários não encontrados para', config.searchInputId);
            return;
        }

        // Verificar se já existe um instrutor selecionado (para edição)
        if (selectElement.value) {
            const selectedOption = selectElement.options[selectElement.selectedIndex];
            if (selectedOption.value) {
                // Simular seleção do instrutor existente
                fetchInstrutorDetails(selectedOption.value, config);
                if (clearBtn) clearBtn.style.display = 'inline-block';
            }
        }

        // Evento de input para busca
        searchInput.addEventListener('input', debounce(function() {
            const query = searchInput.value.trim();
            
            if (query.length < 2) {
                resultsContainer.style.display = 'none';
                return;
            }
            
            // Fazer a requisição para a API
            fetch(`/alunos/api/search-instrutores/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    resultsContainer.innerHTML = '';
                    
                    if (data.length === 0) {
                        resultsContainer.innerHTML = '<div class="list-group-item">Nenhum resultado encontrado</div>';
                        resultsContainer.style.display = 'block';
                        return;
                    }
                    
                    data.forEach(aluno => {
                        const item = document.createElement('a');
                        item.href = '#';
                        item.className = 'list-group-item list-group-item-action';
                        item.dataset.cpf = aluno.cpf;
                        item.dataset.nome = aluno.nome;
                        item.dataset.numeroIniciativo = aluno.numero_iniciatico;
                        item.dataset.situacao = aluno.situacao;
                        
                        let avatarHtml = '';
                        if (aluno.foto) {
                            avatarHtml = `<img src="${aluno.foto}" width="32" height="32" class="rounded-circle">`;
                        } else {
                            avatarHtml = `<div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center" style="width: 32px; height: 32px; font-size: 14px;">
                                            ${aluno.nome.charAt(0).toUpperCase()} 
                                         </div>`;
                        }
                        
                        item.innerHTML = `
                            <div class="d-flex align-items-center">
                                <div class="me-2">
                                    ${avatarHtml}
                                </div>
                                <div>
                                    <div><strong>${aluno.nome}</strong></div>
                                    <small>CPF: ${aluno.cpf} | Nº Iniciático: ${aluno.numero_iniciatico}</small>
                                </div>
                            </div>
                        `;
                        
                        item.addEventListener('click', function(e) {
                            e.preventDefault();
                            selectInstrutor(aluno.cpf, config);
                        });
                        
                        resultsContainer.appendChild(item);
                    });
                    
                    resultsContainer.style.display = 'block';
                })
                .catch(error => {
                    console.error('Erro ao buscar instrutores:', error);
                    resultsContainer.innerHTML = '<div class="list-group-item text-danger">Erro ao buscar instrutores</div>';
                    resultsContainer.style.display = 'block';
                });
        }, 300));

        // Fechar resultados ao clicar fora
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !resultsContainer.contains(e.target)) {
                resultsContainer.style.display = 'none';
            }
        });

        // Evento para limpar seleção
        if (clearBtn) {
            clearBtn.addEventListener('click', function() {
                clearInstrutor(config);
            });
        }
    }

    // Função para selecionar um instrutor
    function selectInstrutor(cpf, config) {
        const searchInput = document.getElementById(config.searchInputId);
        const resultsContainer = document.getElementById(config.resultsContainerId);
        const clearBtn = document.getElementById(config.clearBtnId);
        
        // Limpar resultados e campo de busca
        resultsContainer.style.display = 'none';
        searchInput.value = '';
        
        // Buscar detalhes do instrutor e atualizar a UI
        fetchInstrutorDetails(cpf, config);
        
        // Mostrar botão de limpar
        if (clearBtn) clearBtn.style.display = 'inline-block';
    }

    // Função para buscar detalhes do instrutor
    function fetchInstrutorDetails(cpf, config) {
        const selectedContainer = document.getElementById(config.selectedContainerId);
        const selectedInfo = document.getElementById(config.selectedInfoId);
        const errorContainer = document.getElementById(config.errorContainerId);
        const selectElement = document.getElementById(config.selectId);
        
        // Mostrar loading
        selectedInfo.innerHTML = '<div class="text-center"><div class="spinner-border spinner-border-sm" role="status"></div> Carregando...</div>';
        selectedContainer.classList.remove('d-none');
        
        // Buscar detalhes do aluno
        fetch(`/alunos/api/get-aluno/${cpf}/`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const aluno = data.aluno;
                    
                    // Atualizar o select oculto
                    selectElement.value = aluno.cpf;
                    
                    // Verificar elegibilidade como instrutor
                    fetch(`/alunos/api/verificar-elegibilidade/${aluno.cpf}/`)
                        .then(response => response.json())
                        .then(eligibilityData => {
                            // Buscar detalhes adicionais (turmas, etc)
                            fetch(`/alunos/api/detalhes/${aluno.cpf}/`)
                                .then(response => response.json())
                                .then(detailsData => {
                                    // Atualizar UI com todas as informações
                                    updateInstrutorUI(aluno, eligibilityData, detailsData, config);
                                })
                                .catch(error => {
                                    console.error('Erro ao buscar detalhes do instrutor:', error);
                                    updateInstrutorUI(aluno, eligibilityData, { success: false }, config);
                                });
                        })
                        .catch(error => {
                            console.error('Erro ao verificar elegibilidade:', error);
                            updateInstrutorUI(aluno, { elegivel: false, motivo: 'Erro ao verificar elegibilidade' }, { success: false }, config);
                        });
                } else {
                    errorContainer.textContent = 'Erro ao buscar informações do aluno.';
                    errorContainer.classList.remove('d-none');
                    selectedContainer.classList.add('d-none');
                }
            })
            .catch(error => {
                console.error('Erro ao buscar aluno:', error);
                errorContainer.textContent = 'Erro ao buscar informações do aluno.';
                errorContainer.classList.remove('d-none');
                selectedContainer.classList.add('d-none');
            });
    }

    // Função para atualizar a UI com os detalhes do instrutor
    function updateInstrutorUI(aluno, eligibilityData, detailsData, config) {
        const selectedContainer = document.getElementById(config.selectedContainerId);
        const selectedInfo = document.getElementById(config.selectedInfoId);
        const errorContainer = document.getElementById(config.errorContainerId);
        
        // Limpar mensagens de erro
        errorContainer.classList.add('d-none');
        
        // Construir HTML para o instrutor selecionado
        let avatarHtml = '';
        if (aluno.foto) {
            avatarHtml = `<img src="${aluno.foto}" width="48" height="48" class="rounded-circle mb-2">`;
        }
        
        let statusBadge = '';
        if (aluno.situacao) {
            const badgeClass = aluno.situacao === 'ATIVO' ? 'bg-success' : 'bg-warning';
            statusBadge = `<span class="badge ${badgeClass}">${aluno.situacao}</span>`;
        }
        
        let turmasHtml = 'Nenhuma';
        if (detailsData.success && detailsData.turmas && detailsData.turmas.length > 0) {
            turmasHtml = detailsData.turmas.map(t => t.nome).join(', ');
        }
        
        let statusInstrutor = 'Não verificado';
        if (eligibilityData.elegivel) {
            statusInstrutor = '<span class="text-success">Elegível</span>';
        } else {
            statusInstrutor = `<span class="text-warning">Não elegível</span>`;
            if (eligibilityData.motivo) {
                statusInstrutor += ` - ${eligibilityData.motivo}`;
            }
        }
        
        selectedInfo.innerHTML = `
            ${avatarHtml}
            <strong>${aluno.nome}</strong><br>
            CPF: ${aluno.cpf}<br>
            Número Iniciático: ${aluno.numero_iniciatico || 'N/A'}<br>
            ${statusBadge}
            <div class="mt-2 small">
                <div><strong>Status como instrutor:</strong> ${statusInstrutor}</div>
                <div class="mt-1"><strong>Turmas:</strong> ${turmasHtml}</div>
            </div>
        `;
        
        selectedContainer.classList.remove('d-none');
        
        // Mostrar aviso se não for elegível
        if (!eligibilityData.elegivel) {
            errorContainer.textContent = eligibilityData.motivo || 'Este aluno não atende aos requisitos para ser instrutor.';
            errorContainer.classList.remove('d-none');
        }
    }

    // Função para limpar um instrutor
    function clearInstrutor(config) {
        const searchInput = document.getElementById(config.searchInputId);
        const selectedContainer = document.getElementById(config.selectedContainerId);
        const selectedInfo = document.getElementById(config.selectedInfoId);
        const errorContainer = document.getElementById(config.errorContainerId);
        const selectElement = document.getElementById(config.selectId);
        const clearBtn = document.getElementById(config.clearBtnId);
        
        // Limpar campo de busca
        searchInput.value = '';
        
        // Limpar seleção
        selectElement.value = '';
        
        // Ocultar contêiner de seleção e erro
        selectedContainer.classList.add('d-none');
        errorContainer.classList.add('d-none');
        
        // Resetar texto de info
        selectedInfo.textContent = `Nenhum ${config.searchInputId.replace('search-', '').replace(/-/g, ' ')} selecionado`;
        
        // Ocultar botão de limpar
        if (clearBtn) clearBtn.style.display = 'none';
    }

    // Função de debounce para evitar muitas requisições
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
});



### Arquivo: static\js\alunos\mascaras.js

text
/**
 * Funções para aplicar máscaras e validações nos formulários de alunos
 */

$(document).ready(function() {
    // Aplicar máscaras
    $('#id_cpf').mask('000.000.000-00');
    $('#id_cep').mask('00000-000');
    $('#id_celular_primeiro_contato').mask('(00) 00000-0000');
    $('#id_celular_segundo_contato').mask('(00) 00000-0000');
    
    // Remover máscaras antes do envio do formulário
    $('form').on('submit', function() {
        console.log("Formulário sendo enviado - removendo máscaras");
        
        // Remover máscaras dos campos
        var cpf = $('#id_cpf').val().replace(/\D/g, '');
        var cep = $('#id_cep').val().replace(/\D/g, '');
        var celular1 = $('#id_celular_primeiro_contato').val().replace(/\D/g, '');
        var celular2 = $('#id_celular_segundo_contato').val().replace(/\D/g, '');
        
        // Atualizar os campos com valores sem máscara
        $('#id_cpf').val(cpf);
        $('#id_cep').val(cep);
        $('#id_celular_primeiro_contato').val(celular1);
        $('#id_celular_segundo_contato').val(celular2);
        
        // Não usar preventDefault() para permitir o envio normal do formulário
        return true;
    });
});



### Arquivo: static\js\components\dias-semana.js

text
// Redirecionamento para o módulo correto
console.warn('O arquivo dias-semana.js foi movido para /static/js/modules/. Por favor, atualize suas referências.');
import('/static/js/modules/dias-semana.js')
  .then(module => {
    window.DiasSemana = module.default || module;
  })
  .catch(error => {
    console.error('Erro ao carregar o módulo dias-semana.js:', error);
  });



### Arquivo: static\js\modules\dias-semana.js

text
// Módulo para gerenciar o seletor de dias da semana
const DiasSemana = {
    init: function() {
        const diasSemanaDisplay = document.getElementById('dias-semana-display');
        const diasSemanaDropdown = document.getElementById('dias-semana-dropdown');
        const diasSemanaTexto = document.getElementById('dias-semana-texto');
        const diasSemanaHidden = document.getElementById('dias_semana_hidden');
        
        if (!diasSemanaDisplay || !diasSemanaDropdown || !diasSemanaTexto || !diasSemanaHidden) {
            console.warn('Elementos para dias da semana não encontrados');
            return;
        }
        
        // Configuração dos dias da semana
        const diaItems = document.querySelectorAll('.dia-semana-item');
        let diasSelecionados = diasSemanaHidden.value ? diasSemanaHidden.value.split(', ') : [];
        
        // Marcar os dias já selecionados
        diaItems.forEach(item => {
            const dia = item.dataset.dia;
            const checkbox = item.querySelector('input[type="checkbox"]');
            
            if (diasSelecionados.includes(dia)) {
                item.classList.add('selected');
                checkbox.checked = true;
            }
            
            item.addEventListener('click', () => {
                item.classList.toggle('selected');
                checkbox.checked = !checkbox.checked;
                
                // Atualizar a lista de dias selecionados
                diasSelecionados = Array.from(document.querySelectorAll('.dia-semana-item.selected'))
                    .map(el => el.dataset.dia);
                
                // Atualizar o texto exibido
                diasSemanaTexto.textContent = diasSelecionados.length > 0 ?
                    diasSelecionados.join(', ') : 'Selecione os dias da semana';
                
                // Atualizar o campo oculto
                diasSemanaHidden.value = diasSelecionados.join(', ');
            });
        });
        
        // Mostrar/esconder o dropdown
        diasSemanaDisplay.addEventListener('click', () => {
            const isVisible = diasSemanaDropdown.style.display === 'block';
            diasSemanaDropdown.style.display = isVisible ? 'none' : 'block';
            diasSemanaDisplay.classList.toggle('focus', !isVisible);
        });
        
        // Fechar dropdown ao clicar fora
        document.addEventListener('click', (e) => {
            if (!diasSemanaDisplay.contains(e.target) && !diasSemanaDropdown.contains(e.target)) {
                diasSemanaDropdown.style.display = 'none';
                diasSemanaDisplay.classList.remove('focus');
            }
        });
    }
};




### Arquivo: static\js\modules\instrutor-search.js

text
// Módulo de busca de instrutores
const InstrutorSearch = {
    ignoreEligibility: false,
    csrfToken: null,
    
    init: function(csrfToken, ignoreEligibility) {
        this.csrfToken = csrfToken;
        this.ignoreEligibility = ignoreEligibility || false;
        
        // Configuração única para todos os campos de busca de instrutor
        const camposInstrutor = [
            {
                inputId: 'search-instrutor',
                resultsId: 'search-results-instrutor',
                containerId: 'selected-instrutor-container',
                infoId: 'selected-instrutor-info',
                selectId: 'id_instrutor',
                errorId: 'instrutor-error'
            },
            {
                inputId: 'search-instrutor-auxiliar',
                resultsId: 'search-results-instrutor-auxiliar',
                containerId: 'selected-instrutor-auxiliar-container',
                infoId: 'selected-instrutor-auxiliar-info',
                selectId: 'id_instrutor_auxiliar',
                errorId: 'instrutor-auxiliar-error'
            },
            {
                inputId: 'search-auxiliar-instrucao',
                resultsId: 'search-results-auxiliar-instrucao',
                containerId: 'selected-auxiliar-instrucao-container',
                infoId: 'selected-auxiliar-instrucao-info',
                selectId: 'id_auxiliar_instrucao',
                errorId: 'auxiliar-instrucao-error'
            }
        ];
        
        // Configurar cada campo de busca
        camposInstrutor.forEach(campo => {
            const inputElement = document.getElementById(campo.inputId);
            if (inputElement) {
                this.configurarBuscaInstrutores(
                    campo.inputId,
                    campo.resultsId,
                    campo.containerId,
                    campo.infoId,
                    campo.selectId,
                    campo.errorId
                );
                
                // Garantir que cada botão "Limpar seleção" seja único
                this.garantirBotaoLimparUnico(campo.containerId);
            }
        });
    },
    
    setIgnoreEligibility: function(value) {
        this.ignoreEligibility = value;
    },
    
    configurarBuscaInstrutores: function(inputId, resultadosId, selecionadoContainerId, selecionadoInfoId, selectId, errorId) {
        const inputBusca = document.getElementById(inputId);
        const resultadosContainer = document.getElementById(resultadosId);
        const selecionadoContainer = document.getElementById(selecionadoContainerId);
        const selecionadoInfo = document.getElementById(selecionadoInfoId);
        const selectElement = document.getElementById(selectId);
        const errorElement = document.getElementById(errorId);
        
        if (!inputBusca || !resultadosContainer || !selecionadoContainer || !selectElement) {
            console.error('Elementos não encontrados para configurar busca:', inputId);
            return;
        }
        
        // Função para buscar alunos
        const buscarAlunos = (query) => {
            if (query.length < 2) {
                resultadosContainer.style.display = 'none';
                return;
            }
            
            // Fazer requisição AJAX para buscar alunos
            fetch(`/alunos/api/search-instrutores/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    // Limpar resultados anteriores
                    resultadosContainer.innerHTML = '';
                    
                    if (data.length === 0) {
                        // Nenhum resultado encontrado
                        const noResults = document.createElement('div');
                        noResults.className = 'list-group-item';
                        noResults.textContent = 'Nenhum resultado encontrado';
                        resultadosContainer.appendChild(noResults);
                    } else {
                        // Adicionar cada aluno encontrado à lista de resultados
                        data.forEach(aluno => {
                            const item = document.createElement('a');
                            item.href = '#';
                            item.className = 'list-group-item list-group-item-action';
                            item.dataset.cpf = aluno.cpf;
                            item.dataset.nome = aluno.nome;
                            item.dataset.numeroIniciativo = aluno.numero_iniciatico;
                            item.dataset.situacao = aluno.situacao;
                            
                            // Verificar se o aluno está ativo
                            if (aluno.situacao_codigo !== 'ATIVO') {
                                item.classList.add('text-danger');
                            }
                            
                            // Criar HTML para o item de resultado
                            item.innerHTML = `
                                <div class="d-flex align-items-center">
                                    <div class="me-2">
                                        ${aluno.foto ? `<img src="${aluno.foto}" width="32" height="32" class="rounded-circle">` :
                                        `<div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center"
                                              style="width: 32px; height: 32px; font-size: 14px;">
                                            ${aluno.nome.charAt(0).toUpperCase()}
                                         </div>`}
                                    </div>
                                    <div>
                                        <div><strong>${aluno.nome}</strong></div>
                                        <small>CPF: ${aluno.cpf} | Nº Iniciático: ${aluno.numero_iniciatico || 'N/A'}</small>
                                    </div>
                                </div>
                            `;
                            
                            // Adicionar evento de clique para selecionar o aluno
                            item.addEventListener('click', (e) => {
                                e.preventDefault();
                                
                                // Verificar elegibilidade do aluno se necessário
                                fetch(`/alunos/api/verificar-elegibilidade/${aluno.cpf}/`)
                                    .then(response => response.json())
                                    .then(data => {
                                        // Selecionar o aluno
                                        inputBusca.value = aluno.nome;
                                        
                                        // Atualizar o select oculto
                                        selectElement.value = aluno.cpf;
                                        
                                        // Atualizar a exibição do aluno selecionado
                                        selecionadoInfo.innerHTML = `
                                            <strong>${aluno.nome}</strong><br>
                                            CPF: ${aluno.cpf}<br>
                                            Número Iniciático: ${aluno.numero_iniciatico || 'N/A'}<br>
                                            <span class="badge bg-${getSituacaoClass(aluno.situacao)}">${aluno.situacao}</span>
                                            <div class="mt-2 small">
                                                <div><strong>Status como instrutor:</strong> <span id="${tipo}-status">Verificando...</span></div>
                                                <div class="mt-1"><strong>Turmas:</strong> <span id="${tipo}-turmas">Carregando...</span></div>
                                            </div>
                                        `;
                                        
                                        // Fazer uma requisição adicional para obter mais informações sobre o aluno
                                        fetch(`/alunos/api/detalhes/${aluno.cpf}/`)
                                            .then(response => response.json())
                                            .then(data => {
                                                // Para instrutor principal
                                                $(`#instrutor-status`).text(data.e_instrutor ? 'É instrutor' : 'Não é instrutor');
                                                $(`#instrutor-turmas`).html(turmasHtml);

                                                // Para instrutor auxiliar
                                                $(`#instrutor-auxiliar-status`).text(data.e_instrutor ? 'É instrutor' : 'Não é instrutor');
                                                $(`#instrutor-auxiliar-turmas`).html(turmasHtml);

                                                // Para auxiliar de instrução
                                                $(`#auxiliar-instrucao-status`).text(data.e_instrutor ? 'É instrutor' : 'Não é instrutor');
                                                $(`#auxiliar-instrucao-turmas`).html(turmasHtml);
                                            })
                                            .catch(error => {
                                                console.error('Erro ao buscar detalhes do aluno:', error);
                                                $(`#${tipo}-status`).text('Informação não disponível');
                                                $(`#${tipo}-turmas`).text('Informação não disponível');
                                            });
                                        
                                        // Exibir o container do aluno selecionado
                                        selecionadoContainer.classList.remove('d-none');
                                        
                                        // Exibir aviso se o aluno não for elegível
                                        if (!data.elegivel && errorElement && !this.ignoreEligibility) {
                                            errorElement.innerHTML = `<strong>Aviso:</strong> ${data.motivo}`;
                                            errorElement.classList.remove('d-none');
                                        } else if (errorElement) {
                                            errorElement.classList.add('d-none');
                                        }
                                        
                                        // Ocultar os resultados da busca
                                        resultadosContainer.style.display = 'none';
                                    });
                            });
                            
                            resultadosContainer.appendChild(item);
                        });
                    }
                    
                    // Mostrar container de resultados
                    resultadosContainer.style.display = 'block';
                })
                .catch(error => {
                    console.error('Erro ao buscar alunos:', error);
                    // Mostrar erro no console mas não interromper a experiência do usuário
                });
        };
        
        // Adicionar evento de input para buscar alunos enquanto digita
        inputBusca.addEventListener('input', function() {
            const query = this.value.trim();
            buscarAlunos(query);
        });
        
        // Adicionar evento de clique para limpar e fechar ao clicar fora
        document.addEventListener('click', function(e) {
            if (!inputBusca.contains(e.target) && !resultadosContainer.contains(e.target)) {
                resultadosContainer.style.display = 'none';
            }
        });
        
        // Adicionar evento de foco para mostrar resultados novamente
        inputBusca.addEventListener('focus', function() {
            const query = this.value.trim();
            if (query.length >= 2) {
                buscarAlunos(query);
            }
        });
        
        // Adicionar botão para limpar a seleção se ainda não existir
        if (!selecionadoContainer.nextElementSibling || !selecionadoContainer.nextElementSibling.classList.contains('btn-outline-secondary')) {
            const limparBtn = document.createElement('button');
            limparBtn.type = 'button';
            limparBtn.className = 'btn btn-sm btn-outline-secondary mt-2';
            limparBtn.textContent = 'Limpar seleção';
            limparBtn.addEventListener('click', function() {
                // Limpar o input de busca
                inputBusca.value = '';
                
                // Limpar o select oculto
                selectElement.value = '';
                
                // Esconder o container de aluno selecionado
                selecionadoContainer.classList.add('d-none');
                
                // Esconder mensagens de erro
                if (errorElement) {
                    errorElement.classList.add('d-none');
                }
            });
            
            // Adicionar o botão após o container de aluno selecionado
            selecionadoContainer.parentNode.insertBefore(limparBtn, selecionadoContainer.nextSibling);
        }
    }
};

// Função auxiliar para determinar a classe do badge de situação
function getSituacaoClass(situacao) {
    switch(situacao) {
        case 'Ativo': return 'success';
        case 'Inativo': return 'warning';
        case 'Afastado': return 'warning';
        case 'Excluído': return 'danger';
        case 'Falecido': return 'dark';
        default: return 'secondary';
    }
}




### Arquivo: static\js\turmas\form.js

text
// Inicialização dos módulos para o formulário de turmas
document.addEventListener('DOMContentLoaded', function() {
    // PARTE 1: Corrigir carregamento das datas
    function formatarDataParaInput(dataStr) {
        if (!dataStr) return '';
        
        // Se já estiver no formato correto, retorna
        if (/^\d{4}-\d{2}-\d{2}$/.test(dataStr)) return dataStr;
        
        // Tentar extrair data do formato DD/MM/YYYY
        const partes = dataStr.split('/');
        if (partes.length === 3) {
            return `${partes[2]}-${partes[1].padStart(2, '0')}-${partes[0].padStart(2, '0')}`;
        }
        
        return '';
    }
    
    const dataInicioInput = document.getElementById('id_data_inicio');
    const dataFimInput = document.getElementById('id_data_fim');
    
    if (dataInicioInput) {
        const dataInicioTexto = dataInicioInput.nextElementSibling ? dataInicioInput.nextElementSibling.textContent : '';
        const match = dataInicioTexto.match(/Data atual: (\d{2}\/\d{2}\/\d{4})/);
        if (match && match[1]) {
            dataInicioInput.value = formatarDataParaInput(match[1]);
            console.log('Data início definida como:', dataInicioInput.value);
        }
    }
    
    if (dataFimInput) {
        const dataFimTexto = dataFimInput.nextElementSibling ? dataFimInput.nextElementSibling.textContent : '';
        const match = dataFimTexto.match(/Data atual: (\d{2}\/\d{2}\/\d{4})/);
        if (match && match[1]) {
            dataFimInput.value = formatarDataParaInput(match[1]);
            console.log('Data fim definida como:', dataFimInput.value);
        }
    }
    
    // PARTE 2: Remover botões "Limpar seleção" duplicados
    function removerBotoesDuplicados() {
        // Definir os elementos que devem ter apenas um botão de limpar
        const containers = [
            'selected-instrutor-container',
            'selected-instrutor-auxiliar-container',
            'selected-auxiliar-instrucao-container'
        ];
        
        containers.forEach(containerId => {
            const container = document.getElementById(containerId);
            if (!container) return;
            
            // Encontrar todos os botões de limpar após este container
            const botoes = [];
            let proximoElemento = container.nextElementSibling;
            
            while (proximoElemento) {
                if (proximoElemento.tagName === 'BUTTON' && 
                    proximoElemento.textContent.trim() === 'Limpar seleção') {
                    botoes.push(proximoElemento);
                }
                proximoElemento = proximoElemento.nextElementSibling;
            }
            
            // Manter apenas o primeiro botão e remover os outros
            if (botoes.length > 1) {
                for (let i = 1; i < botoes.length; i++) {
                    if (botoes[i].parentNode) {
                        botoes[i].parentNode.removeChild(botoes[i]);
                    }
                }
            }
        });
    }
    
    // Executar a remoção de botões duplicados após um pequeno atraso
    // para garantir que todos os elementos estejam carregados
    setTimeout(removerBotoesDuplicados, 500);
});

// Adicione este código ao seu arquivo JavaScript para inicializar o Select2
$(document).ready(function() {
    // Inicializar Select2 para o dropdown de cursos
    $('.curso-select').select2({
        theme: 'bootstrap4',
        width: '100%'
    });
});




### Arquivo: static\js\turmas\form_fix.js

text
/**
 * Script para corrigir problemas no formulário de turmas
 * Especificamente para resolver o problema de duplicação do Select2
 */
document.addEventListener('DOMContentLoaded', function() {
    // Destruir qualquer instância existente do Select2 antes de inicializar
    if ($.fn.select2) {
        $('.curso-select').select2('destroy');
        
        // Inicializar Select2 para o campo de curso com configurações corretas
        $('.curso-select').select2({
            theme: 'bootstrap4',
            placeholder: 'Selecione um curso',
            width: '100%',
            dropdownParent: $('body') // Garantir que o dropdown seja anexado ao body
        });
        
        // Remover qualquer dropdown duplicado que possa ter sido criado
        $('.select2-container--open').not(':first').remove();
    }
    
    // Corrigir botões duplicados de "Limpar seleção"
    const containers = [
        'selected-instrutor-container',
        'selected-instrutor-auxiliar-container',
        'selected-auxiliar-instrucao-container'
    ];
    
    containers.forEach(containerId => {
        const botoes = document.querySelectorAll(`#${containerId} + button`);
        // Se houver mais de um botão, remover os extras
        if (botoes.length > 1) {
            for (let i = 1; i < botoes.length; i++) {
                botoes[i].remove();
            }
        }
    });
});

