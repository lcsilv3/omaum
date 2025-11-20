#!/usr/bin/env python
"""Script para limpar e popular a tabela TipoCodigo."""

import csv
import os
import sys
from pathlib import Path
from typing import Any

import django
from django.db.models.deletion import ProtectedError

# Configuração de diretórios e Django
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings.development")
django.setup()

from alunos.utils import get_tipo_codigo_model  # noqa: E402

TipoCodigo: Any = get_tipo_codigo_model()
if not TipoCodigo:
    raise RuntimeError("Modelo TipoCodigo indisponível.")


def limpar_tabela() -> bool:
    """Tenta limpar a tabela TipoCodigo, retornando True em caso de sucesso."""
    print("🧹 Limpando a tabela TipoCodigo...")
    count = TipoCodigo.objects.count()
    print(f"📊 Registros encontrados: {count}")

    if count > 0:
        try:
            TipoCodigo.objects.all().delete()
            print("✅ Tabela limpa com sucesso!")
            return True
        except ProtectedError:
            print(
                "⚠️  Não foi possível limpar a tabela; existem registros relacionados em uso."
            )
            return False
    else:
        print("ℹ️  Tabela já estava vazia.")
        return True

    return True


def importar_csv(tabela_limpa: bool):
    """Importa dados do arquivo CSV para a tabela TipoCodigo."""
    print("\n📥 Importando dados do CSV...")

    csv_file = PROJECT_ROOT / "docs" / "Planilha Tipos de  Códigos.csv"
    if not csv_file.exists():
        print(f"❌ Arquivo {csv_file} não encontrado!")
        return False

    try:
        with open(csv_file, "r", encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader, None)  # descarta cabeçalho
            count = 0

            for row in reader:
                if not row or len([col for col in row if col.strip()]) < 2:
                    continue

                nome = row[1].strip()
                descricao = row[2].strip() if len(row) > 2 else ""

                if not nome:
                    continue

                if tabela_limpa:
                    tipo_codigo = TipoCodigo.objects.create(
                        nome=nome, descricao=descricao
                    )
                    print(f"✅ Criado: {tipo_codigo.nome}")
                else:
                    tipo_codigo, created = TipoCodigo.objects.update_or_create(
                        nome=nome, defaults={"descricao": descricao}
                    )
                    acao = "✅ Criado" if created else "♻️ Atualizado"
                    print(f"{acao}: {tipo_codigo.nome}")

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
    tabela_limpa = limpar_tabela()

    # Etapa 2: Importar CSV
    if importar_csv(tabela_limpa):
        # Etapa 3: Verificar dados
        verificar_dados()
        print("\n✅ Processo concluído com sucesso!")
    else:
        print("\n❌ Processo falhou durante a importação!")
