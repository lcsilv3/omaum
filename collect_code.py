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
