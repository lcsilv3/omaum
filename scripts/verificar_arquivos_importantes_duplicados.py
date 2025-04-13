import os
import filecmp
import hashlib
from collections import defaultdict

def get_file_hash(filepath):
    """Calcula o hash MD5 de um arquivo."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest()

def find_duplicate_files(root_dir, critical_files):
    """
    Procura por duplicatas dos arquivos críticos no diretório do projeto.
    
    :param root_dir: Diretório raiz do projeto
    :param critical_files: Lista de tuplas (nome_arquivo, caminho_esperado)
    :return: Dicionário com os resultados
    """
    results = defaultdict(list)

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename in [cf[0] for cf in critical_files]:
                file_path = os.path.join(dirpath, filename)
                file_hash = get_file_hash(file_path)
                results[filename].append((file_path, file_hash))

    return results

def generate_report(results, critical_files):
    """Gera um relatório baseado nos resultados da busca."""
    print("Relatório de Verificação de Arquivos Críticos")
    print("============================================")

    for cf_name, cf_path in critical_files:
        print(f"\nVerificando: {cf_name}")
        print(f"Localização esperada: {cf_path}")
        
        if cf_name in results:
            locations = results[cf_name]
            if len(locations) > 1:
                print("  ALERTA: Múltiplas cópias encontradas!")
                for loc, file_hash in locations:
                    status = "CORRETO" if loc == cf_path else "DUPLICATA"
                    print(f"  - {loc} ({status})")
            elif locations[0][0] != cf_path:
                print(f"  ALERTA: Arquivo encontrado em local inesperado: {locations[0][0]}")
            else:
                print("  OK: Arquivo encontrado apenas na localização correta.")
        else:
            print("  ERRO: Arquivo não encontrado!")

    print("\nRevisão concluída.")

if __name__ == "__main__":
    project_root = "C:\\projetos\\omaum"
    critical_files = [
        ("base.html", r"omaum\templates\base.html"),
        ("home.html", r"omaum\Templates\home.html"),
        ("settings.py", "omaum\\settings.py"),
        ("urls.py", "omaum\\urls.py"),
        ("views.py", "core\views.py),
        # Adicione outros arquivos críticos conforme necessário
    ]

    results = find_duplicate_files(project_root, critical_files)
    generate_report(results, critical_files)