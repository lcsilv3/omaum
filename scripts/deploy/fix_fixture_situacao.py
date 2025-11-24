"""
Script para corrigir valores de situacao e situacao_iniciatica no fixture.

Converte valores como "ATIVO" para "a", "DESLIGADO" para "d", etc.
"""
import json
import sys
from pathlib import Path

# Mapeamento de valores incorretos para corretos
SITUACAO_MAP = {
    "ATIVO": "a",
    "DESLIGADO": "d",
    "FALECIDO": "f",
    "EXCLUIDO": "e",
    "EXCLUÍDO": "e",
    "ativo": "a",
    "desligado": "d",
    "falecido": "f",
    "excluido": "e",
    "excluído": "e",
}


def fix_fixture(input_file: Path, output_file: Path = None):
    """Corrige valores de situacao nos fixtures."""
    if output_file is None:
        output_file = input_file
    
    print(f"Lendo fixture: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_fixed = 0
    
    for item in data:
        if item.get('model') == 'alunos.aluno':
            fields = item.get('fields', {})
            
            # Corrigir campo situacao
            if 'situacao' in fields and fields['situacao'] in SITUACAO_MAP:
                old_value = fields['situacao']
                fields['situacao'] = SITUACAO_MAP[old_value]
                print(f"  Aluno pk={item['pk']}: situacao '{old_value}' -> '{fields['situacao']}'")
                total_fixed += 1
            
            # Corrigir campo situacao_iniciatica
            if 'situacao_iniciatica' in fields and fields['situacao_iniciatica'] in SITUACAO_MAP:
                old_value = fields['situacao_iniciatica']
                fields['situacao_iniciatica'] = SITUACAO_MAP[old_value]
                print(f"  Aluno pk={item['pk']}: situacao_iniciatica '{old_value}' -> '{fields['situacao_iniciatica']}'")
                total_fixed += 1
    
    print(f"\nTotal de correções: {total_fixed}")
    
    print(f"Salvando fixture corrigido: {output_file}")
    # Salvar sem BOM UTF-8
    with open(output_file, 'w', encoding='utf-8-sig') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Remover BOM se existir
    with open(output_file, 'rb') as f:
        content = f.read()
    
    # Verificar e remover BOM UTF-8 (EF BB BF)
    if content.startswith(b'\xef\xbb\xbf'):
        print("Removendo BOM UTF-8...")
        with open(output_file, 'wb') as f:
            f.write(content[3:])
    
    print("✓ Fixture corrigido com sucesso (sem BOM)!")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python fix_fixture_situacao.py <arquivo_fixture> [arquivo_saida]")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    
    if not input_path.exists():
        print(f"Erro: Arquivo não encontrado: {input_path}")
        sys.exit(1)
    
    fix_fixture(input_path, output_path)
