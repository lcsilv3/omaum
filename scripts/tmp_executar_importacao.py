#!/usr/bin/env python
"""Executa importação de códigos com caminhos ajustados para produção."""

import os
import sys
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings.production")

import django

django.setup()

# Importar função do script principal
import importlib.util

spec = importlib.util.spec_from_file_location(
    "limpar_importar", "/app/limpar_importar.py"
)
modulo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(modulo)
sincronizar_tipos = modulo.sincronizar_tipos
sincronizar_codigos = modulo.sincronizar_codigos
imprimir_resumo = modulo.imprimir_resumo

# Caminhos ajustados para produção
DOCS_DIR = Path("/app/docs")
ARQUIVO_TIPOS = DOCS_DIR / "Planilha Tipos de  Códigos.csv"
ARQUIVO_CODIGOS = DOCS_DIR / "Planilha de Códigos.csv"

print("🚀 Iniciando sincronização de códigos iniciáticos...")
print(f"📁 Diretório docs: {DOCS_DIR}")
print(f"📄 Arquivo tipos: {ARQUIVO_TIPOS.exists()}")
print(f"📄 Arquivo códigos: {ARQUIVO_CODIGOS.exists()}")
print()

# Executar sincronização
tipos_por_id, resumo_tipos = sincronizar_tipos(ARQUIVO_TIPOS)
imprimir_resumo("Tipos de Código", resumo_tipos)

if tipos_por_id:
    resumo_codigos = sincronizar_codigos(tipos_por_id, ARQUIVO_CODIGOS)
    imprimir_resumo("Códigos Iniciáticos", resumo_codigos)
else:
    print("\n⚠️  Nenhum tipo foi importado; sincronização de códigos cancelada.")

print("\n✅ Sincronização concluída!")
