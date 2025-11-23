#!/usr/bin/env python
"""Script utilitário: limpa e repovoa a tabela ``Codigo`` a partir de CSVs."""

from __future__ import annotations

import csv
import os
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple

SCRIPT_ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = SCRIPT_ROOT.parent
PROJ_ROOT = SCRIPTS_DIR.parent

if str(PROJ_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJ_ROOT))

import django
from django.db import IntegrityError, models

# Configurar Django antes de importar módulos dependentes
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from alunos.utils import get_codigo_model, get_tipo_codigo_model  # noqa: E402
from scripts.import_utils import normaliza, pick_field  # noqa: E402

Codigo = get_codigo_model()
TipoCodigo = get_tipo_codigo_model()
if not Codigo or not TipoCodigo:
    raise RuntimeError("Modelos iniciáticos (Codigo/TipoCodigo) indisponíveis.")

CODIGOS_CSV = SCRIPTS_DIR / "codigos.csv"
PLANILHA_CODIGOS_CSV = SCRIPTS_DIR / "docs" / "Planilha de Códigos.csv"


def limpar_tabela() -> None:
    """Apaga todos os registros de ``Codigo`` antes da importação."""
    print("🧹 Limpando a tabela Codigo...")
    count = Codigo.objects.count()
    print(f"📊 Registros encontrados: {count}")

    if count > 0:
        Codigo.objects.all().delete()
        print("✅ Tabela limpa com sucesso!")
    else:
        print("ℹ️  Tabela já estava vazia.")


def detectar_delimitador(csv_path: Path, encoding: str) -> str:
    """Detecta o delimitador mais provável (vírgula ou ponto e vírgula)."""
    linha = ""
    try:
        with csv_path.open("r", encoding=encoding, errors="ignore") as handle:
            linha = handle.readline()
    except OSError:
        return ";"

    return ";" if linha.count(";") >= linha.count(",") else ","


def localizar_csv() -> Optional[Tuple[Path, str, str, str]]:
    """Retorna o CSV disponível com delimitador, encoding e origem."""
    if CODIGOS_CSV.exists():
        encoding = "utf-8"
        delimiter = detectar_delimitador(CODIGOS_CSV, encoding)
        return CODIGOS_CSV, delimiter, encoding, "codigos.csv"

    if PLANILHA_CODIGOS_CSV.exists():
        return PLANILHA_CODIGOS_CSV, ";", "latin1", "Planilha de Códigos.csv"

    return None


def obter_tipos_codigo() -> Dict[str, object]:
    """Carrega todos os ``TipoCodigo`` e indexa por nome/descrição normalizados."""
    print("\n🔍 Verificando tipos de código disponíveis...")
    tipos: Dict[str, object] = {}

    for tipo in TipoCodigo.objects.all().order_by("nome"):
        print(f"  • {tipo.nome}: {tipo.descricao}")
        for chave in {tipo.nome, tipo.descricao}:
            normalizado = normaliza(chave or "")
            if normalizado:
                tipos[normalizado] = tipo

    return tipos


def resolver_tipo(
    mapa_tipos: Dict[str, object], valores: Iterable[Optional[str]]
) -> Optional[object]:
    """Encontra o ``TipoCodigo`` a partir das possíveis chaves do CSV."""
    for valor in valores:
        if not valor:
            continue
        chave = normaliza(valor)
        if chave and chave in mapa_tipos:
            return mapa_tipos[chave]
    return None


def atualizar_descricao(codigo_obj: Any, nova_descricao: str) -> bool:
    """Adiciona uma nova descrição ao código, evitando duplicidades."""
    nova_descricao = (nova_descricao or "").strip()
    if not nova_descricao:
        return False

    existentes = [
        item.strip()
        for item in (codigo_obj.descricao or "").split("\n")
        if item.strip()
    ]

    if not existentes:
        codigo_obj.descricao = nova_descricao
        return True

    if nova_descricao in existentes:
        return False

    existentes.append(nova_descricao)
    codigo_obj.descricao = "\n".join(existentes)
    return True


def importar_csv() -> bool:
    """Importa dados do CSV preenchendo ``Codigo`` conforme mapeamento solicitado."""
    info = localizar_csv()
    if not info:
        print(
            "❌ Nenhum arquivo de códigos encontrado (codigos.csv ou Planilha de Códigos.csv)."
        )
        return False

    csv_path, delimiter, encoding, origem = info
    print(f"\n📥 Importando dados do CSV ({origem})...")

    tipos_codigo = obter_tipos_codigo()
    if not tipos_codigo:
        print("ℹ️  Nenhum TipoCodigo encontrado. Novos tipos serão criados automaticamente." )

    total_processado = 0
    criados = 0
    atualizados = 0
    sem_alteracao = 0
    erros = 0

    with csv_path.open("r", encoding=encoding, newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        for row_num, row in enumerate(reader, start=1):
            tipo_valores = (
                pick_field(row, ["código tipo", "codigo tipo", "tipo"]),
                pick_field(row, ["descrição tipo", "descricao tipo"]),
            )
            tipo_codigo = resolver_tipo(tipos_codigo, tipo_valores)
            if not tipo_codigo:
                codigo_tipo_valor, descricao_tipo_valor = tipo_valores
                nome_tipo = (descricao_tipo_valor or codigo_tipo_valor or "").strip()

                if not nome_tipo:
                    print(
                        f"⚠️  Linha {row_num}: Tipo não identificado (valores={tipo_valores})."
                    )
                    erros += 1
                    continue

                defaults_tipo = {
                    "descricao": (descricao_tipo_valor or nome_tipo or None),
                }

                tipo_codigo, created_tipo = TipoCodigo.objects.get_or_create(
                    nome=nome_tipo,
                    defaults=defaults_tipo,
                )

                if created_tipo:
                    print(
                        f"➕ TipoCodigo criado automaticamente: nome='{tipo_codigo.nome}'"
                    )

                for chave in {nome_tipo, descricao_tipo_valor, codigo_tipo_valor}:
                    normalizado = normaliza(chave or "")
                    if normalizado:
                        tipos_codigo[normalizado] = tipo_codigo

            nome_codigo = (tipo_codigo.descricao or tipo_codigo.nome or "").strip()
            if not nome_codigo:
                nome_codigo = str(tipo_codigo.pk)

            descricao_codigo = pick_field(row, ["descrição código", "descricao codigo"])
            codigo_bruto = pick_field(row, ["código", "codigo"])
            descricao_final = (descricao_codigo or codigo_bruto or "").strip()

            defaults = {
                "tipo_codigo": tipo_codigo,
                "descricao": descricao_final or None,
            }

            try:
                codigo_obj, created = Codigo.objects.get_or_create(
                    nome=nome_codigo,
                    defaults=defaults,
                )
            except IntegrityError as err:
                print(
                    f"⚠️  Linha {row_num}: não foi possível criar/atualizar registro "
                    f"para '{nome_codigo}'. {err}"
                )
                erros += 1
                continue

            if created:
                criados += 1
            else:
                campos_alterados = []
                if codigo_obj.tipo_codigo_id != tipo_codigo.id:
                    codigo_obj.tipo_codigo = tipo_codigo
                    campos_alterados.append("tipo_codigo")

                if atualizar_descricao(codigo_obj, descricao_final):
                    if "descricao" not in campos_alterados:
                        campos_alterados.append("descricao")

                if campos_alterados:
                    codigo_obj.save(update_fields=campos_alterados)
                    atualizados += 1
                else:
                    sem_alteracao += 1

            total_processado += 1
            if total_processado % 50 == 0:
                print(f"📊 Processadas {total_processado} linhas...")

    print("\n📊 Importação concluída:")
    print(f"  • Total de linhas processadas: {total_processado}")
    print(f"  • Novos códigos criados: {criados}")
    print(f"  • Códigos atualizados: {atualizados}")
    print(f"  • Linhas sem alteração relevante: {sem_alteracao}")
    print(f"  • Total de erros: {erros}")

    return erros == 0


def verificar_dados() -> None:
    """Exibe um resumo rápido dos registros importados."""
    print("\n🔍 Verificando dados importados...")
    codigos = Codigo.objects.select_related("tipo_codigo")

    if not codigos.exists():
        print("⚠️  Nenhum registro encontrado!")
        return

    total = codigos.count()
    print(f"📊 Total de registros: {total}")

    print("\n📋 Registros por tipo:")
    por_tipo = (
        codigos.values("tipo_codigo__nome")
        .annotate(total=models.Count("id"))
        .order_by("tipo_codigo__nome")
    )
    for item in por_tipo:
        print(f"  • {item['tipo_codigo__nome']}: {item['total']} códigos")

    print("\n📝 Exemplos de registros:")
    for codigo in codigos.order_by("tipo_codigo__nome", "nome")[:5]:
        print(
            f"  • {codigo.tipo_codigo.nome} | nome='{codigo.nome}' | "
            f"descrição='{(codigo.descricao or '')[:60]}'"
        )


def validar_integridade() -> None:
    """Executa verificações simples pós-importação."""
    print("\n🔍 Validando integridade dos dados...")

    duplicados = (
        Codigo.objects.values("nome")
        .annotate(total=models.Count("id"))
        .filter(total__gt=1)
    )
    if duplicados.exists():
        print("⚠️  Códigos com o mesmo campo 'nome':")
        for dup in duplicados:
            print(f"  • '{dup['nome']}' aparece {dup['total']} vezes")
    else:
        print("✅ Nenhum duplicado encontrado pelo campo 'nome'.")

    sem_tipo = Codigo.objects.filter(tipo_codigo__isnull=True)
    if sem_tipo.exists():
        print("⚠️  Existem códigos sem vínculo de tipo (IDs):")
        print("  ", list(sem_tipo.values_list("id", flat=True)))
    else:
        print("✅ Todos os códigos possuem TipoCodigo vinculado.")


if __name__ == "__main__":
    print("🚀 Iniciando processo de limpeza e importação da tabela Codigo")

    limpar_tabela()

    if importar_csv():
        verificar_dados()
        validar_integridade()
        print("\n✅ Processo concluído com sucesso!")
    else:
        print("\n❌ Processo falhou durante a importação!")
