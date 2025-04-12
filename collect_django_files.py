import os
import chardet

def collect_files(project_root):
    relevant_files = {
        'forms.py': [],
        'views.py': [],
        'urls.py': [],
        'models.py': [],
        'templates': []
    }
    
    for root, dirs, files in os.walk(project_root):
        # Ignorar diretórios de ambiente virtual e cache
        if 'venv' in root or '__pycache__' in root:
            continue
            
        for file in files:
            if file in relevant_files:
                relevant_files[file].append(os.path.join(root, file))
            elif file.endswith('.html'):
                relevant_files['templates'].append(os.path.join(root, file))
    
    return relevant_files

def write_file_contents(output_file, filepath):
    # Detectar codificação do arquivo
    with open(filepath, 'rb') as raw_file:
        raw_data = raw_file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding'] or 'utf-8'  # Fallback para utf-8
    
    try:
        with open(filepath, 'r', encoding=encoding) as file:
            relative_path = os.path.relpath(filepath)
            output_file.write(f"\n\n### Arquivo: {relative_path}\n")
            
            # Determinar o tipo de linguagem para o bloco de código
            if filepath.endswith('.html'):
                language = 'html'
            elif filepath.endswith('.py'):
                language = 'python'
            else:
                language = 'text'
                
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
    
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        output_file.write("# Arquivos do Projeto Django para Revisão\n")
        
        for file_type, file_paths in relevant_files.items():
            if file_type == 'templates':
                output_file.write(f"\n## Arquivos de Template:\n")
            else:
                output_file.write(f"\n## Arquivos {file_type}:\n")
                
            for filepath in sorted(file_paths):
                write_file_contents(output_file, filepath)
    
    print(f"Conteúdo dos arquivos foi escrito em {output_filename}")

if __name__ == "__main__":
    main()
