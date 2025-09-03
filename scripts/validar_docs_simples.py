#!/usr/bin/env python3
"""
Script simples para validar documentacao do Sistema OMAUM.
"""

import sys
from pathlib import Path


def main():
    print("Validando documentacao do Sistema OMAUM...")
    print("=" * 50)

    docs_dir = Path(__file__).parent.parent / "docs"
    arquivos_obrigatorios = [
        "README.md",
        "ARQUITETURA_PRESENCAS.md",
        "MANUAL_USUARIO.md",
        "GUIA_INSTALACAO.md",
        "API_DOCUMENTATION.md",
        "GUIA_DESENVOLVEDOR.md",
        "CHANGELOG.md",
    ]

    todos_presentes = True

    for arquivo in arquivos_obrigatorios:
        caminho = docs_dir / arquivo
        if caminho.exists() and caminho.stat().st_size > 0:
            print("OK: {}".format(arquivo))
        else:
            print("ERRO: {} nao encontrado ou vazio".format(arquivo))
            todos_presentes = False

    # Verificar README principal
    readme_path = Path(__file__).parent.parent / "README.md"
    if readme_path.exists():
        print("OK: README.md principal")
    else:
        print("ERRO: README.md principal nao encontrado")
        todos_presentes = False

    # Verificar AGENT.md
    agent_path = Path(__file__).parent.parent / "AGENT.md"
    if agent_path.exists():
        print("OK: AGENT.md")
    else:
        print("ERRO: AGENT.md nao encontrado")
        todos_presentes = False

    print("=" * 50)

    if todos_presentes:
        total_arquivos = len(list(docs_dir.glob("*.md")))
        print("SUCESSO: Documentacao completa!")
        print("Total de arquivos: {}".format(total_arquivos))
        return 0
    else:
        print("ERRO: Documentacao incompleta")
        return 1


if __name__ == "__main__":
    sys.exit(main())
