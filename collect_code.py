import os

def collect_code(root_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Dicionário para armazenar o conteúdo de cada funcionalidade
    functionality_content = {}
    for root, dirs, files in os.walk(root_dir):
        # Pega o primeiro diretório após o root_dir como a funcionalidade
        relative_path = os.path.relpath(root, root_dir)
        functionality = relative_path.split(os.path.sep)[0]

        if functionality not in functionality_content:
            functionality_content[functionality] = []

        for file in files:
            if file.endswith(('.py', '.html', '.js', '.css')):
                file_path = os.path.join(root, file)
                content = f"\n\nFile: {file_path}\n"
                content += "```" + file.split('.')[-1] + "\n"
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content += f.read()
                except IOError as e:
                    content += f"Error reading file: {e}"
                content += "\n```\n"
                functionality_content[functionality].append(content)

    # Escreve o conteúdo de cada funcionalidade em um arquivo separado
    for functionality, content in functionality_content.items():
        output_file = os.path.join(output_dir, f"{functionality}_code.txt")
        with open(output_file, 'w', encoding='utf-8') as out:
            out.write(''.join(content))
        print(f"Código da funcionalidade '{functionality}' coletado e salvo em {output_file}")

if __name__ == "__main__":
    project_root = "."  # Caminho para a raiz do seu projeto
    output_dir = "project_code_output"  # Diretório para armazenar os arquivos de saída
    collect_code(project_root, output_dir)
    print(f"Coleta de código concluída. Arquivos salvos em {output_dir}")
