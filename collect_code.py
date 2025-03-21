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
                
                content += "\n\n"
                functionality_content[functionality].append(content)

    # Escreve o conteúdo de cada funcionalidade em um arquivo Markdown separado
    for functionality, content in functionality_content.items():
        # Ignorar diretórios vazios ou especiais
        if functionality == '.' or not content:
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
