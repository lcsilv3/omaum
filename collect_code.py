import os
import chardet

def collect_code(root_dir, output_dir, max_files_per_chunk=10, enable_chunking=True):
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
            # Skip collect*.py files
            if file.startswith('collect') and file.endswith('.py'):
                continue
                
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
                
                # Adicionar abertura do bloco de código com a linguagem correta
                content += f"{language}\n"
                
                # Detect encoding
                with open(file_path, 'rb') as f:
                    raw_data = f.read()
                    result = chardet.detect(raw_data)
                    encoding = result['encoding']
                
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        file_content = f.read()
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    continue
                    # Verificar se o conteúdo está vazio ou contém apenas espaços em branco
                    if not file_content.strip():
                        continue  # Pular arquivos com conteúdo vazio
                    content += file_content
                except IOError as e:
                    content += f"Error reading file: {e}"
                
                # Adicionar fechamento do bloco de código
                content += "\n\n\n"
                
                functionality_content[functionality].append(content)

    # Dividindo em chunks menores ao salvar (ou não, dependendo da opção)
    for functionality, content_list in functionality_content.items():
        if not content_list:
            continue
        
        if enable_chunking:
            # Dividir em chunks
            chunks = [content_list[i:i + max_files_per_chunk] for i in range(0, len(content_list), max_files_per_chunk)]
            
            for i, chunk in enumerate(chunks):
                chunk_file = os.path.join(output_dir, f"{functionality}_part{i+1}_code.md")
                
                with open(chunk_file, 'w', encoding='utf-8') as out:
                    out.write(f"# Código da Funcionalidade: {functionality} - Parte {i+1}/{len(chunks)}\n")
                    out.write(f"*Gerado automaticamente*\n\n")
                    out.write(''.join(chunk))
                
                print(f"Código da funcionalidade '{functionality}' (parte {i+1}) salvo em {chunk_file}")
        else:
            # Sem chunking - salvar tudo em um único arquivo
            output_file = os.path.join(output_dir, f"{functionality}_code.md")
            
            with open(output_file, 'w', encoding='utf-8') as out:
                out.write(f"# Código da Funcionalidade: {functionality}\n")
                out.write(f"*Gerado automaticamente*\n\n")
                out.write(''.join(content_list))
            
            print(f"Código da funcionalidade '{functionality}' salvo em {output_file}")

if __name__ == "__main__":
    project_root = "."  # Caminho para a raiz do seu projeto
    output_dir = "project_code_output"  # Diretório para armazenar os arquivos de saída
    
    # Você pode modificar estes parâmetros conforme necessário
    collect_code(
        project_root, 
        output_dir,
        max_files_per_chunk=10,  # Número máximo de arquivos por chunk
        enable_chunking=False     # Definir como False para desativar o chunking
    )
    
    print(f"Coleta de código concluída. Arquivos Markdown salvos em {output_dir}")
