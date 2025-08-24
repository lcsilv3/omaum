#!/usr/bin/env python
"""Script para limpar e popular a tabela TipoCodigo."""

import os
import csv
import django
from typing import Any

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from alunos.utils import get_tipo_codigo_model  # noqa: E402

TipoCodigo: Any = get_tipo_codigo_model()
if not TipoCodigo:
    raise RuntimeError("Modelo TipoCodigo indisponível.")


def limpar_tabela():
    """Limpa todos os registros da tabela TipoCodigo."""
    print("🧹 Limpando a tabela TipoCodigo...")
    count = TipoCodigo.objects.count()
    print(f"📊 Registros encontrados: {count}")

    if count > 0:
        TipoCodigo.objects.all().delete()
        print("✅ Tabela limpa com sucesso!")
    else:
        print("ℹ️  Tabela já estava vazia.")


def importar_csv():
    """Importa dados do arquivo CSV para a tabela TipoCodigo."""
    print("\n📥 Importando dados do CSV...")

    csv_file = "tipo_codigo.csv"
    if not os.path.exists(csv_file):
        print(f"❌ Arquivo {csv_file} não encontrado!")
        return False

    try:
        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            count = 0

            for row in reader:
                tipo_codigo = TipoCodigo.objects.create(
                    nome=row["nome"], descricao=row["descricao"]
                )
                print(f"✅ Criado: {tipo_codigo.nome}")
                count += 1

            print(f"\n📊 Total de registros importados: {count}")
            return True

    except Exception as e:
        print(f"❌ Erro ao importar CSV: {e}")
        return False


def verificar_dados():
    """Verifica os dados importados."""
    print("\n🔍 Verificando dados importados...")
    tipos = TipoCodigo.objects.all()

    if not tipos.exists():
        print("⚠️  Nenhum registro encontrado!")
        return

    print(f"📊 Total de registros: {tipos.count()}")
    print("\n📋 Registros encontrados:")
    for tipo in tipos:
        print(f"  • {tipo.nome}: {tipo.descricao}")


if __name__ == "__main__":
    print("🚀 Iniciando processo de limpeza e importação da tabela TipoCodigo")
    print("=" * 60)

    # Etapa 1: Limpar tabela
    limpar_tabela()

    # Etapa 2: Importar CSV
    if importar_csv():
        # Etapa 3: Verificar dados
        verificar_dados()
        print("\n✅ Processo concluído com sucesso!")
    else:
        print("\n❌ Processo falhou durante a importação!")
