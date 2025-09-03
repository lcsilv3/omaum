#!/usr/bin/env python3
"""
Script para validar a documentação do Sistema OMAUM.
Verifica se todos os documentos estão presentes e bem formatados.
"""

import sys
from pathlib import Path


def validar_arquivos_documentacao():
    """Valida se todos os arquivos de documentação estão presentes."""

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

    arquivos_faltando = []

    for arquivo in arquivos_obrigatorios:
        caminho = docs_dir / arquivo
        if not caminho.exists():
            arquivos_faltando.append(arquivo)
        else:
            # Verificar se arquivo não está vazio
            if caminho.stat().st_size == 0:
                arquivos_faltando.append(f"{arquivo} (vazio)")

    if arquivos_faltando:
        print("❌ Arquivos de documentação faltando ou vazios:")
        for arquivo in arquivos_faltando:
            print(f"   - {arquivo}")
        return False
    else:
        print("✅ Todos os arquivos de documentação estão presentes")
        return True


def validar_estrutura_markdown():
    """Valida a estrutura básica dos arquivos Markdown."""

    docs_dir = Path(__file__).parent.parent / "docs"
    problemas = []

    for arquivo_md in docs_dir.glob("*.md"):
        with open(arquivo_md, "r", encoding="utf-8") as f:
            conteudo = f.read()

        # Verificar se tem título principal
        if not conteudo.startswith("#"):
            problemas.append(f"{arquivo_md.name}: Falta título principal (# Título)")

        # Verificar se tem conteúdo suficiente
        if len(conteudo.split("\n")) < 10:
            problemas.append(f"{arquivo_md.name}: Conteúdo muito curto")

        # Verificar encoding de caracteres especiais
        try:
            conteudo.encode("utf-8")
        except UnicodeEncodeError:
            problemas.append(f"{arquivo_md.name}: Problemas de encoding")

    if problemas:
        print("⚠️  Problemas na estrutura Markdown:")
        for problema in problemas:
            print(f"   - {problema}")
        return False
    else:
        print("✅ Estrutura Markdown está correta")
        return True


def validar_links_internos():
    """Valida se os links internos entre documentos estão funcionando."""

    docs_dir = Path(__file__).parent.parent / "docs"
    links_quebrados = []

    for arquivo_md in docs_dir.glob("*.md"):
        with open(arquivo_md, "r", encoding="utf-8") as f:
            conteudo = f.read()

        # Buscar links para outros arquivos .md
        import re

        links = re.findall(r"\[.*?\]\((.*?\.md)\)", conteudo)

        for link in links:
            # Remover âncoras (#secao)
            link_arquivo = link.split("#")[0]

            if link_arquivo and not link_arquivo.startswith("http"):
                caminho_link = docs_dir / link_arquivo
                if not caminho_link.exists():
                    links_quebrados.append(f"{arquivo_md.name} -> {link_arquivo}")

    if links_quebrados:
        print("❌ Links internos quebrados:")
        for link in links_quebrados:
            print(f"   - {link}")
        return False
    else:
        print("✅ Todos os links internos estão funcionando")
        return True


def validar_readme_principal():
    """Valida se o README principal está atualizado."""

    readme_path = Path(__file__).parent.parent / "README.md"

    if not readme_path.exists():
        print("❌ README.md principal não encontrado")
        return False

    with open(readme_path, "r", encoding="utf-8") as f:
        conteudo = f.read()

    elementos_obrigatorios = [
        "# Sistema OMAUM",
        "Quick Start",
        "Tecnologias Utilizadas",
        "docs/",
        "Documentação",
    ]

    elementos_faltando = []
    for elemento in elementos_obrigatorios:
        if elemento not in conteudo:
            elementos_faltando.append(elemento)

    if elementos_faltando:
        print("❌ README principal está incompleto. Faltam:")
        for elemento in elementos_faltando:
            print(f"   - {elemento}")
        return False
    else:
        print("✅ README principal está completo")
        return True


def validar_agent_md():
    """Valida se o AGENT.md está presente e atualizado."""

    agent_path = Path(__file__).parent.parent / "AGENT.md"

    if not agent_path.exists():
        print("❌ AGENT.md não encontrado")
        return False

    with open(agent_path, "r", encoding="utf-8") as f:
        conteudo = f.read()

    elementos_obrigatorios = [
        "Comandos Importantes",
        "python manage.py",
        "presencas/",
        "Estrutura do Projeto",
    ]

    elementos_faltando = []
    for elemento in elementos_obrigatorios:
        if elemento not in conteudo:
            elementos_faltando.append(elemento)

    if elementos_faltando:
        print("❌ AGENT.md está incompleto. Faltam:")
        for elemento in elementos_faltando:
            print(f"   - {elemento}")
        return False
    else:
        print("✅ AGENT.md está completo")
        return True


def gerar_relatorio():
    """Gera relatório completo da documentação."""

    print("Validando documentacao do Sistema OMAUM...")
    print("=" * 50)

    resultados = [
        validar_arquivos_documentacao(),
        validar_estrutura_markdown(),
        validar_links_internos(),
        validar_readme_principal(),
        validar_agent_md(),
    ]

    print("=" * 50)

    if all(resultados):
        print("Documentacao esta completa e valida!")
        print("\nEstatisticas:")

        docs_dir = Path(__file__).parent.parent / "docs"
        total_arquivos = len(list(docs_dir.glob("*.md")))
        total_linhas = 0

        for arquivo in docs_dir.glob("*.md"):
            with open(arquivo, "r", encoding="utf-8") as f:
                total_linhas += len(f.readlines())

        print("Arquivos de documentacao: {}".format(total_arquivos))
        print("Total de linhas: {}".format(total_linhas))
        print("README principal: OK")
        print("AGENT.md: OK")

        return 0
    else:
        print("Documentacao tem problemas que precisam ser corrigidos")
        return 1


if __name__ == "__main__":
    sys.exit(gerar_relatorio())
