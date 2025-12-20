#!/usr/bin/env python
"""
Script para localizar a definição real de uma view no projeto.

Uso:
    python scripts/find_view.py <nome_da_view>
    python scripts/find_view.py listar_atividades_academicas
"""
import sys
import os
import re
from pathlib import Path


def find_view_definition(view_name, project_root=None):
    """Encontra onde uma view está definida no projeto."""
    if project_root is None:
        project_root = Path(__file__).parent.parent

    print(f"\n🔍 Procurando view: {view_name}")
    print("=" * 60)

    # 1. Procurar em urls.py para ver de onde é importada
    print("\n📁 1. Verificando imports em urls.py...")
    urls_files = list(project_root.glob("**/urls.py"))
    
    for urls_file in urls_files:
        try:
            content = urls_file.read_text(encoding='utf-8')
            
            # Procurar import direto
            import_pattern = rf"from .* import.*{view_name}"
            if re.search(import_pattern, content):
                print(f"\n   ✅ Encontrado em: {urls_file.relative_to(project_root)}")
                
                # Extrair linha do import
                for line in content.split('\n'):
                    if view_name in line and ('import' in line or 'from' in line):
                        print(f"   📌 {line.strip()}")
                        
                        # Tentar identificar o módulo
                        if 'from' in line:
                            match = re.search(r'from\s+([^\s]+)\s+import', line)
                            if match:
                                module = match.group(1)
                                print(f"   📦 Módulo: {module}")
        except Exception as e:
            pass

    # 2. Procurar definição real da função
    print(f"\n📁 2. Procurando definição de 'def {view_name}('...")
    py_files = [
        f for f in project_root.glob("**/*.py") 
        if not any(x in str(f) for x in ['migrations', '__pycache__', 'venv', '.git'])
    ]
    
    found_definitions = []
    for py_file in py_files:
        try:
            content = py_file.read_text(encoding='utf-8')
            pattern = rf"^def {view_name}\s*\("
            
            for i, line in enumerate(content.split('\n'), 1):
                if re.match(pattern, line):
                    found_definitions.append((py_file, i, line.strip()))
        except Exception:
            pass
    
    if found_definitions:
        print(f"\n   ✅ Encontradas {len(found_definitions)} definição(ões):\n")
        for file_path, line_num, line_content in found_definitions:
            print(f"   📄 {file_path.relative_to(project_root)}:{line_num}")
            print(f"      {line_content[:80]}...")
            
            # Mostrar decorator acima (se houver)
            try:
                lines = file_path.read_text(encoding='utf-8').split('\n')
                if line_num > 1 and lines[line_num-2].strip().startswith('@'):
                    print(f"      {lines[line_num-2].strip()}")
            except:
                pass
            print()
    else:
        print(f"   ❌ Nenhuma definição encontrada para '{view_name}'")

    # 3. Sugestões
    print("\n💡 Dicas:")
    print("   • Sempre verifique urls.py primeiro")
    print("   • Use 'grep -r \"def nome_view\" .' para buscar rápida")
    print("   • Procure por @login_required ou @require_GET nos decorators")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/find_view.py <nome_da_view>")
        print("Exemplo: python scripts/find_view.py listar_atividades_academicas")
        sys.exit(1)
    
    view_name = sys.argv[1]
    find_view_definition(view_name)
