import os

def collect_code(root_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as out:
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith(('.py', '.html', '.js', '.css')):
                    file_path = os.path.join(root, file)
                    out.write(f"\n\nFile: {file_path}\n")
                    out.write("```" + file.split('.')[-1] + "\n")
                    with open(file_path, 'r', encoding='utf-8') as f:
                        out.write(f.read())
                    out.write("\n```\n")

if __name__ == "__main__":
    project_root = "."  # Caminho para a raiz do seu projeto
    output_file = "project_code.txt"
    collect_code(project_root, output_file)
    print(f"Código coletado e salvo em {output_file}")