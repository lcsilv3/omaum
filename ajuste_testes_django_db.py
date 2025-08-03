import os
import re
from pathlib import Path

# Diretório base dos testes
BASE_DIR = Path(__file__).parent
TESTS_DIR = BASE_DIR / 'tests'

# 1. Adiciona o marcador pytest.mark.django_db em classes/funções de teste

def add_django_db_marker(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    new_lines = []
    modified = False
    for i, line in enumerate(lines):
        # Detecta classes de teste que usam TestCase e não possuem o marcador
        if re.match(r'class .*\(TestCase\):', line) and (i == 0 or 'pytest.mark.django_db' not in lines[i-1]):
            new_lines.append('@pytest.mark.django_db\n')
            modified = True
        new_lines.append(line)
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Marcador adicionado em: {file_path}")

# 2. Renomeia arquivos duplicados de test_models.py

def rename_duplicate_test_models():
    for root, dirs, files in os.walk(TESTS_DIR):
        for file in files:
            if file == 'test_models.py':
                pasta = Path(root).name
                novo_nome = f'test_models_{pasta}.py'
                old_path = Path(root) / file
                new_path = Path(root) / novo_nome
                os.rename(old_path, new_path)
                print(f"Arquivo renomeado: {old_path} -> {new_path}")

# 3. Remove arquivos .pyc e pastas __pycache__
def clean_pycache():
    for root, dirs, files in os.walk(TESTS_DIR):
        for d in dirs:
            if d == '__pycache__':
                pycache_path = Path(root) / d
                for f in pycache_path.glob('*.pyc'):
                    f.unlink()
                os.rmdir(pycache_path)
                print(f"Removido: {pycache_path}")

if __name__ == '__main__':
    # Adiciona marcador em todos arquivos de teste
    for root, dirs, files in os.walk(TESTS_DIR):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                add_django_db_marker(Path(root) / file)
    # Renomeia arquivos duplicados
    rename_duplicate_test_models()
    # Limpa pycache
    clean_pycache()
    print('Ajustes concluídos.')
