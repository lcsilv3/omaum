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
