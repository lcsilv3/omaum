'''
# Arquivos da Raiz do Projeto Django


### Arquivo: collect_code.py

python
"""
OMAUM - Sistema de Gestão de Iniciados
Script: collect_code.py
Descrição: Utilitário para coletar e documentar arquivos do projeto Django por app.
Uso: python collect_code.py
Responsável: Equipe OMAUM
Última atualização: 2025-06-15
"""

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
                "views_modulares": [],
                "templates": [],
            }
        for file in files:
            # Coletar arquivos principais
            if file in ["forms.py", "views.py", "urls.py", "models.py"]:
                apps_files[app_name][file].append(os.path.join(root, file))
            # Coletar todos os arquivos .py dentro de subdiretórios 'views'
            elif "views" in root and file.endswith(".py"):
                apps_files[app_name]["views_modulares"].append(os.path.join(root, file))
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

def write_to_file_with_size_limit(content, base_filename, max_chars=100000):
    """
    Escreve o conteúdo em um ou mais arquivos, dividindo-o se necessário para
    não ultrapassar o limite de caracteres por arquivo.
    """
    if len(content) <= max_chars:
        # Se o conteúdo for menor que o limite, escreve em um único arquivo
        with open(base_filename, "w", encoding="utf-8") as f:
            f.write(content)
        return [base_filename]

    # Dividir o conteúdo em partes
    parts = []
    part_num = 1

    # Obter o diretório e o nome do arquivo base
    dir_name = os.path.dirname(base_filename)
    file_base_name = os.path.basename(base_filename)
    name_parts = os.path.splitext(file_base_name)

    # Dividir o conteúdo em blocos lógicos (por arquivo)
    file_blocks = content.split("\n\n### Arquivo:")
    header = file_blocks[0]  # Cabeçalho do documento
    file_blocks = file_blocks[1:]  # Blocos de arquivos

    current_content = header
    files_created = []

    for block in file_blocks:
        block_content = "\n\n### Arquivo:" + block

        # Se adicionar este bloco ultrapassar o limite, salvar o conteúdo atual e começar um novo arquivo
        if len(current_content + block_content) > max_chars and current_content != header:
            # Criar nome do arquivo para esta parte
            part_filename = os.path.join(dir_name, f"{name_parts[0]}_parte{part_num}{name_parts[1]}")

            # Adicionar a linha de separação no início e no final do arquivo
            final_content = "'''\n" + current_content + "\n'''"

            # Escrever o conteúdo atual
            with open(part_filename, "w", encoding="utf-8") as f:
                f.write(final_content)

            files_created.append(part_filename)
            part_num += 1

            # Iniciar novo conteúdo com o cabeçalho e o bloco atual
            current_content = header + block_content
        else:
            # Adicionar o bloco ao conteúdo atual
            current_content += block_content

    # Escrever a última parte
    if current_content:
        part_filename = os.path.join(dir_name, f"{name_parts[0]}_parte{part_num}{name_parts[1]}")
        # Adicionar a linha de separação no início e no final do arquivo
        final_content = "'''\n" + current_content + "\n'''"
        with open(part_filename, "w", encoding="utf-8") as f:
            f.write(final_content)
        files_created.append(part_filename)

    return files_created

def collect_root_files(project_root, output_dir):
    """Coleta arquivos da raiz do projeto Django."""
    output_filename = os.path.join(output_dir, "root_files_revisao.md")

    content = "# Arquivos da Raiz do Projeto Django\n"
    # Listar arquivos na raiz do projeto
    root_files = [
        f
        for f in os.listdir(project_root)
        if os.path.isfile(os.path.join(project_root, f))
        and not f.startswith(".")
        and f != "db.sqlite3"  # Excluir o arquivo db.sqlite3
    ]

    # Usar StringIO para capturar o conteúdo
    from io import StringIO
    temp_output = StringIO()
    temp_output.write(content)

    for file in root_files:
        filepath = os.path.join(project_root, file)
        write_file_contents(temp_output, filepath)

    # Verificar e incluir arquivos estáticos
    static_dir = os.path.join(project_root, "static")
    if os.path.exists(static_dir) and os.path.isdir(static_dir):
        temp_output.write("\n## Arquivos Estáticos\n")
        for root, dirs, files in os.walk(static_dir):
            for file in files:
                filepath = os.path.join(root, file)
                write_file_contents(temp_output, filepath)

    # Obter o conteúdo completo
    full_content = temp_output.getvalue()
    temp_output.close()

    # Escrever o conteúdo em um ou mais arquivos
    files_created = write_to_file_with_size_limit(full_content, output_filename)

    if len(files_created) == 1:
        print(f"Arquivos da raiz do projeto foram escritos em {output_filename}")
    else:
        print(f"Arquivos da raiz do projeto foram divididos em {len(files_created)} partes devido ao tamanho")
        for file in files_created:
            print(f"  - {file}")

def generate_project_structure(project_root, output_dir):
    """Gera um arquivo com a estrutura completa do projeto."""
    output_filename = os.path.join(output_dir, "project_structure.md")

    content = "# Estrutura do Projeto Django\n\n\n"

    for root, dirs, files in os.walk(project_root):
        # Ignorar diretórios de ambiente virtual e cache
        if "venv" in root or "__pycache__" in root:
            continue
        level = root.replace(project_root, "").count(os.sep)
        indent = " " * 4 * level
        content += f"{indent}{os.path.basename(root)}/\n"
        sub_indent = " " * 4 * (level + 1)
        for file in files:
            content += f"{sub_indent}{file}\n"

    content += "\n"

    # Escrever o conteúdo em um ou mais arquivos
    files_created = write_to_file_with_size_limit(content, output_filename)

    if len(files_created) == 1:
        print(f"Estrutura do projeto foi escrita em {output_filename}")
    else:
        print(f"Estrutura do projeto foi dividida em {len(files_created)} partes devido ao tamanho")
        for file in files_created:
            print(f"  - {file}")

def check_template_dirs(project_root, output_dir):
    """Verifica e documenta as configurações de diretórios de templates."""
    output_filename = os.path.join(output_dir, "template_dirs_check.md")

    content = "# Verificação de Diretórios de Templates\n\n"

    # Usar StringIO para capturar o conteúdo
    from io import StringIO
    temp_output = StringIO()
    temp_output.write(content)

    # Verificar settings.py para configurações de TEMPLATES
    settings_files = []
    for root, dirs, files in os.walk(project_root):
        if "settings.py" in files:
            settings_files.append(os.path.join(root, "settings.py"))

    if settings_files:
        temp_output.write("## Configurações de Templates no settings.py\n\n")
        for settings_file in settings_files:
            write_file_contents(temp_output, settings_file)

    # Listar todos os diretórios de templates encontrados
    temp_output.write("\n## Diretórios de Templates Encontrados\n\n")
    template_dirs = []
    for root, dirs, files in os.walk(project_root):
        if "templates" in dirs:
            template_dir = os.path.join(root, "templates")
            template_dirs.append(template_dir)
            temp_output.write(f"- {os.path.relpath(template_dir, project_root)}\n")
            # Listar arquivos de template neste diretório
            temp_output.write("  Arquivos:\n")
            for template_root, template_dirs2, template_files in os.walk(template_dir):
                for file in template_files:
                    temp_output.write(
                        f"  - {os.path.relpath(os.path.join(template_root, file), template_dir)}\n"
                    )

    # Verificar especificamente o template listar_alunos.html
    temp_output.write("\n## Busca pelo template listar_alunos.html\n\n")
    found = False
    for root, dirs, files in os.walk(project_root):
        for file in files:
            if file == "listar_alunos.html":
                found = True
                temp_output.write(
                    f"Encontrado em: {os.path.relpath(os.path.join(root, file), project_root)}\n"
                )

    if not found:
        temp_output.write("O arquivo listar_alunos.html não foi encontrado no projeto.\n")

    # Obter o conteúdo completo
    full_content = temp_output.getvalue()
    temp_output.close()

    # Escrever o conteúdo em um ou mais arquivos
    files_created = write_to_file_with_size_limit(full_content, output_filename)

    if len(files_created) == 1:
        print(f"Verificação de diretórios de templates foi escrita em {output_filename}")
    else:
        print(f"Verificação de diretórios de templates foi dividida em {len(files_created)} partes devido ao tamanho")
        for file in files_created:
            print(f"  - {file}")

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

        # Usar StringIO para capturar o conteúdo
        from io import StringIO
        temp_output = StringIO()

        # Escrever o cabeçalho
        temp_output.write(f"# Revisão da Funcionalidade: {app_name}\n")

        for file_type, file_paths in file_types.items():
            if not file_paths:
                continue
            if file_type == "templates":
                temp_output.write(f"\n## Arquivos de Template:\n")
            elif file_type == "views_modulares":
                temp_output.write(f"\n## Arquivos de Views Modulares:\n")
            else:
                temp_output.write(f"\n## Arquivos {file_type}:\n")
            for filepath in sorted(file_paths):
                write_file_contents(temp_output, filepath)

        # Obter o conteúdo completo
        full_content = temp_output.getvalue()
        temp_output.close()

        # Definir o nome base do arquivo de saída
        output_filename = os.path.join(output_dir, f"{app_name}_revisao.md")

        # Escrever o conteúdo em um ou mais arquivos
        files_created = write_to_file_with_size_limit(full_content, output_filename)

        if len(files_created) == 1:
            print(f"Conteúdo da funcionalidade '{app_name}' foi escrito em {output_filename}")
        else:
            print(f"Conteúdo da funcionalidade '{app_name}' foi dividido em {len(files_created)} partes devido ao tamanho")
            for file in files_created:
                print(f"  - {file}")

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


### Arquivo: c:/projetos/omaum\Cursos.JPG


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
("base.html", r"omaum/omaum/templates/base.html"),
("home.html", r"omaum/omaum/templates/home.html"),

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
astroid==3.3.9
black==25.1.0
chardet==5.2.0
click==8.1.8
colorama==0.4.6
dill==0.3.9
Django==5.2.2
django-crispy-forms==2.3
django-debug-toolbar==5.1.0
django-extensions==3.2.3
django-widget-tweaks==1.5.0
djangorestframework==3.16.0
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




### Arquivo: script_revisao_projeto.py

python
"""
OMAUM - Sistema de Gestão de Iniciados
Script: script_revisao_projeto.py
Descrição: Utilitário para revisão e documentação da estrutura do projeto Django.
Uso: python script_revisao_projeto.py
Responsável: Equipe OMAUM
Última atualização: 2025-06-15
"""

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
/*
 * OMAUM - Sistema de Gestão de Iniciados
 * Arquivo: alunos.css
 * Descrição: Estilos específicos para telas e componentes do módulo de alunos.
 * Responsável: Equipe OMAUM
 * Última atualização: 2025-06-15
 */

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



### Arquivo: static\css\buttons.css

text
/* Estilos padronizados para bot천es */
.btn-action-primary {
    color: #fff;
    background-color: #0d6efd;
    border-color: #0d6efd;
    padding: 0.375rem 0.75rem;
}

.btn-action-secondary {
    color: #fff;
    background-color: #6c757d;
    border-color: #6c757d;
    padding: 0.375rem 0.75rem;
}

.btn-action-success {
    color: #fff;
    background-color: #198754;
    border-color: #198754;
    padding: 0.375rem 0.75rem;
}

.btn-action-danger {
    color: #fff;
    background-color: #dc3545;
    border-color: #dc3545;
    padding: 0.375rem 0.75rem;
}

.btn-action-warning {
    color: #000;
    background-color: #ffc107;
    border-color: #ffc107;
    padding: 0.375rem 0.75rem;
}

.btn-action-info {
    color: #fff;
    background-color: #0dcaf0;
    border-color: #0dcaf0;
    padding: 0.375rem 0.75rem;
}

/* Padr천es de posicionamento */
.actions-container {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1rem;
}

.actions-container-end {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

/* Padr천es para bot천es em tabelas */
.table-actions {
    display: flex;
    gap: 0.25rem;
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

@keyframes piscar {
    0%, 100% { box-shadow: 0 0 0 2px #dc3545; }
    50% { box-shadow: 0 0 8px 4px #dc3545; }
}

.is-required-error {
    border-color: #dc3545 !important;
    animation: piscar 1s linear 3;
    background-color: #fff0f0 !important;
}



### Arquivo: static\css\Piscar.css

text
<!-- No bloco head ou em um arquivo CSS separado -->
<style>
    @keyframes piscar {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    
    .blink {
        animation: piscar 1s linear infinite;
    }
</style>




### Arquivo: static\css\styles.css

text
/*
 * OMAUM - Sistema de Gestão de Iniciados
 * Arquivo: styles.css
 * Descrição: Estilos globais complementares ao Bootstrap para todo o sistema.
 * Responsável: Equipe OMAUM
 * Última atualização: 2025-06-15
 */

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

select.form-control {
    background-image: url("data:image/svg+xml,%3Csvg width='16' height='16' fill='gray' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M4 6l4 4 4-4' stroke='gray' stroke-width='2' fill='none'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 0.75rem center;
    background-size: 1.2em;
    padding-right: 2.5em;
}

select.form-select {
    background-image: url("data:image/svg+xml,%3Csvg width='16' height='16' fill='gray' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M4 6l4 4 4-4' stroke='gray' stroke-width='2' fill='none'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 0.75rem center;
    background-size: 1.2em;
    padding-right: 2.5em;
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

.curso-dropdown {
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    background-color: #fff;
    padding-right: 2rem;
    position: relative;
}

.dropdown-arrow {
    position: absolute;
    right: 18px;
    top: 50%;
    width: 0;
    height: 0;
    pointer-events: none;
    border-style: solid;
    border-width: 6px 6px 0 6px;
    border-color: #888 transparent transparent transparent;
    transform: translateY(-50%);
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


### Arquivo: c:/projetos/omaum\static\img\favicon.ico


Erro ao ler o arquivo: 'charmap' codec can't decode byte 0x98 in position 615: character maps to <undefined>



### Arquivo: static\img\logo.png

text


### Arquivo: c:/projetos/omaum\static\img\logo.png


Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte



### Arquivo: static\js\aluno-search.js

text
/**
 * OMAUM - Sistema de Gestão de Iniciados
 * Arquivo: aluno-search.js
 * Descrição: Busca dinâmica de alunos via AJAX para formulários.
 * Responsável: Equipe OMAUM
 * Última atualização: 2025-06-15
 */

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
                                ${aluno.numero_iniciatico !== "N/A" ? `<small class="ms-2">Nº: ${aluno.numero_iniciatico}</small>` : ''}
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




### Arquivo: static\js\atividades_ajax.js

text
/**
 * Centraliza o carregamento dinâmico das turmas ao selecionar um curso.
 * Para funcionar, os campos devem ter os IDs padrão: id_curso e id_turmas.
 * Opcional: inclua um elemento com id="no-turmas-msg" para mensagens.
 * 
 * Chame: window.initTurmasAjax({ url: '/atividades/ajax/turmas-por-curso/' });
 */
window.initTurmasAjax = function(options) {
    const cursoSelect = document.getElementById('id_curso');
    const turmasSelect = document.getElementById('id_turmas');
    const selectAllTurmas = document.getElementById('select-all-turmas');
    let noTurmasMsg = document.getElementById('no-turmas-msg');
    const url = options && options.url ? options.url : '/atividades/ajax/turmas-por-curso/';

    if (!cursoSelect || !turmasSelect) return;

    if (!noTurmasMsg) {
        noTurmasMsg = document.createElement('div');
        noTurmasMsg.id = 'no-turmas-msg';
        noTurmasMsg.className = 'text-muted mt-2';
        turmasSelect.parentNode.appendChild(noTurmasMsg);
    }

    function atualizarTurmas(cursoId, turmasSelecionadas=[]) {
        if (!cursoId) {
            turmasSelect.innerHTML = '';
            noTurmasMsg.textContent = '';
            return;
        }
        fetch(`${url}?curso=${cursoId}`)
            .then(response => response.json())
            .then(data => {
                turmasSelect.innerHTML = '';
                if (data.turmas.length === 0) {
                    noTurmasMsg.textContent = 'Não há turmas para este curso.';
                } else {
                    noTurmasMsg.textContent = '';
                    data.turmas.forEach(function(turma) {
                        const option = document.createElement('option');
                        option.value = turma.id;
                        option.textContent = turma.nome;
                        if (turmasSelecionadas.includes(String(turma.id))) {
                            option.selected = true;
                        }
                        turmasSelect.appendChild(option);
                    });
                }
            });
    }

    cursoSelect.addEventListener('change', function() {
        atualizarTurmas(this.value);
    });

    // Ao carregar a página, filtra as turmas se já houver curso selecionado
    const turmasSelecionadas = Array.from(turmasSelect.selectedOptions).map(opt => opt.value);
    if (cursoSelect.value) {
        atualizarTurmas(cursoSelect.value, turmasSelecionadas);
    } else {
        turmasSelect.innerHTML = '';
        noTurmasMsg.textContent = '';
    }

    // Selecionar todas as turmas (se existir o checkbox)
    if (selectAllTurmas && turmasSelect) {
        selectAllTurmas.addEventListener('change', function() {
            for (let option of turmasSelect.options) {
                option.selected = this.checked;
            }
        });
        turmasSelect.addEventListener('change', function() {
            selectAllTurmas.checked = Array.from(turmasSelect.options).every(opt => opt.selected);
        });
    }
};



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
 * OMAUM - Sistema de Gestão de Iniciados
 * Arquivo: inicializar_select2.js
 * Descrição: Inicialização global do Select2 para garantir consistência visual e funcional.
 * Responsável: Equipe OMAUM
 * Última atualização: 2025-06-15
 */

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

// Adicionar este script para garantir que o Select2 seja inicializado corretamente
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar Select2 para campos de seleção múltipla
    if (typeof $.fn.select2 === 'function') {
        $('.form-control[multiple]').select2({
            theme: 'bootstrap4',
            placeholder: 'Selecione as opções',
            allowClear: true,
            width: '100%'
        });
        
        // Desabilitar o campo de turmas quando "todas as turmas" estiver marcado
        const todasTurmasCheckbox = document.getElementById('id_todas_turmas');
        const turmasSelect = document.getElementById('id_turmas');
        
        if (todasTurmasCheckbox && turmasSelect) {
            function toggleTurmasField() {
                if (todasTurmasCheckbox.checked) {
                    $(turmasSelect).prop('disabled', true).trigger('change');
                } else {
                    $(turmasSelect).prop('disabled', false).trigger('change');
                }
            }
            
            // Inicializar
            toggleTurmasField();
            
            // Adicionar listener para mudanças
            todasTurmasCheckbox.addEventListener('change', toggleTurmasField);
        }
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



### Arquivo: static\js\atividades\atividades_filtros.js

text
document.addEventListener('DOMContentLoaded', function() {
    console.log('Inicializando script de filtros de atividades');
    
    // Encontrar os elementos do formulário
    const cursoSelect = document.querySelector('#id_curso');
    const turmaSelect = document.querySelector('#id_turmas');
    
    if (!cursoSelect || !turmaSelect) {
        console.log('Elementos de filtro não encontrados', {
            cursoSelect: cursoSelect ? cursoSelect.id : 'não encontrado',
            turmaSelect: turmaSelect ? turmaSelect.id : 'não encontrado'
        });
        return;
    }
    
    console.log('Elementos encontrados:', {
        cursoSelect: cursoSelect.id,
        turmaSelect: turmaSelect.id
    });
    
    // Função para atualizar as turmas quando o curso mudar
    cursoSelect.addEventListener('change', function() {
        const cursoId = this.value;
        console.log('Curso selecionado:', cursoId);
        
        // Se não houver curso selecionado, limpa as turmas
        if (!cursoId) {
            // Manter apenas a primeira opção (Todas as turmas)
            const primeiraOpcao = turmaSelect.options[0];
            turmaSelect.innerHTML = '';
            turmaSelect.appendChild(primeiraOpcao);
            return;
        }
        
        // Buscar as turmas do curso selecionado
        fetch(`/atividades/ajax/turmas-por-curso/?curso_id=${cursoId}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro na resposta: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Turmas recebidas:', data);
            
            // Limpar o select de turmas mantendo a primeira opção
            const primeiraOpcao = turmaSelect.options[0];
            turmaSelect.innerHTML = '';
            turmaSelect.appendChild(primeiraOpcao);
            
            // Adicionar as novas opções
            if (data.turmas && data.turmas.length > 0) {
                data.turmas.forEach(turma => {
                    const option = document.createElement('option');
                    option.value = turma.id;
                    option.textContent = turma.nome;
                    turmaSelect.appendChild(option);
                });
            }
        })
        .catch(error => {
            console.error('Erro ao buscar turmas:', error);
        });
    });
});



### Arquivo: static\js\atividades\filtros.js

text
document.addEventListener('DOMContentLoaded', function () {
    const $form = document.getElementById('filtro-atividades');
    const $q = document.getElementById('id_q');
    const $curso = document.getElementById('id_curso');
    const $turma = document.getElementById('id_turmas');
    const $tabela = document.querySelector('.table-responsive tbody');
    const $alerta = document.getElementById('alerta-nenhum-resultado');

    // Dica extra: sempre inicia o alerta oculto
    $alerta.style.display = 'none';

    function atualizaFiltros(mantemCurso = true, mantemTurma = true) {
        const params = new URLSearchParams(new FormData($form)).toString();
        fetch('/atividades/api/filtrar-atividades/?' + params, {
            headers: { 'x-requested-with': 'XMLHttpRequest' }
        })
            .then(resp => resp.json())
            .then(data => {
                // Atualiza tabela
                $tabela.innerHTML = data.atividades_html;

                // Mostra/oculta alerta de nenhum resultado
                if (
                    data.atividades_html.includes('Nenhuma atividade encontrada')
                ) {
                    $alerta.style.display = 'block';
                } else {
                    $alerta.style.display = 'none';
                }

                // Atualiza cursos mantendo seleção
                const cursoSelecionado = mantemCurso ? $curso.value : '';
                $curso.innerHTML = '';
                const optTodosCursos = document.createElement('option');
                optTodosCursos.value = '';
                optTodosCursos.textContent = 'Todos os cursos';
                $curso.appendChild(optTodosCursos);

                if (data.cursos.length > 0) {
                    data.cursos.forEach(curso => {
                        const opt = document.createElement('option');
                        opt.value = curso.id;
                        opt.textContent = curso.nome;
                        if (String(curso.id) === String(cursoSelecionado)) {
                            opt.selected = true;
                        }
                        $curso.appendChild(opt);
                    });
                } else {
                    // Se não houver cursos, mantém apenas a opção "Todos"
                    optTodosCursos.selected = true;
                }

                // Atualiza turmas mantendo seleção
                const turmaSelecionada = mantemTurma ? $turma.value : '';
                $turma.innerHTML = '';
                const optTodasTurmas = document.createElement('option');
                optTodasTurmas.value = '';
                optTodasTurmas.textContent = 'Todas as turmas';
                $turma.appendChild(optTodasTurmas);

                if (data.turmas.length > 0) {
                    data.turmas.forEach(turma => {
                        const opt = document.createElement('option');
                        opt.value = turma.id;
                        opt.textContent = turma.nome;
                        if (String(turma.id) === String(turmaSelecionada)) {
                            opt.selected = true;
                        }
                        $turma.appendChild(opt);
                    });
                } else {
                    // Se não houver turmas, mantém apenas a opção "Todas"
                    optTodasTurmas.selected = true;
                }

                // Se só houver um curso possível para a turma selecionada, seleciona automaticamente
                if (!cursoSelecionado && data.cursos.length === 1) {
                    $curso.value = data.cursos[0].id;
                }
                // Se só houver uma turma possível para o curso selecionado, seleciona automaticamente
                if (!turmaSelecionada && data.turmas.length === 1) {
                    $turma.value = data.turmas[0].id;
                }
            });
    }

    // Atualiza a tabela automaticamente ao digitar (com debounce)
    let debounceTimer;
    $q.addEventListener('input', function () {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            atualizaFiltros(true, true);
        }, 300); // 300ms de atraso
    });

    $curso.addEventListener('change', function () {
        // Ao trocar o curso, limpa turma selecionada
        $turma.value = '';
        atualizaFiltros(true, false);
    });

    $turma.addEventListener('change', function () {
        // Ao trocar a turma, pode ser necessário ajustar o curso
        atualizaFiltros(false, true);
    });

    $form.addEventListener('submit', function (e) {
        e.preventDefault();
        atualizaFiltros(true, true);
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



'''