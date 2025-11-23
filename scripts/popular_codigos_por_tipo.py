#!/usr/bin/env python
"""
Script para popular códigos associados aos tipos existentes no banco.
"""

import os
import csv
import django

# Configurar Django
if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings.production")
django.setup()

from alunos.utils import get_tipo_codigo_model, get_codigo_model
from scripts.import_utils import pick_field, normaliza

TipoCodigo = get_tipo_codigo_model()
Codigo = get_codigo_model()

CSV_PATH = os.path.join(os.path.dirname(__file__), "docs", "Planilha de Códigos.csv")


def pick_field(row, candidates):
    import unicodedata

    def norm(k):
        return (
            unicodedata.normalize("NFKD", (k or ""))
            .encode("ASCII", "ignore")
            .decode("ASCII")
            .strip()
            .lower()
        )

    keys = list(row.keys())
    norm_keys = {norm(k): k for k in keys}
    for cand in candidates:
        nk = norm(cand)
        if nk in norm_keys:
            return row.get(norm_keys[nk])
    return None


def popular_codigos(create_types=False):
    created_count = 0
    updated_count = 0
    skipped_count = 0

    if not os.path.exists(CSV_PATH):
        print(f"CSV não encontrado em: {CSV_PATH}")
        return

    with open(CSV_PATH, encoding="latin1") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")

        # normaliza e pick_field importados de scripts.import_utils

        # cache tipos para evitar consultas repetidas
        tipos_cache = {normaliza(t.nome): t for t in TipoCodigo.objects.all()}

        for row in reader:
            nome_tipo = pick_field(row, ["Tipo", "tipo", "codigo tipo", "código tipo", "unnamed: 0"]) or ""
            nome_codigo = pick_field(row, ["Nome", "nome", "codigo", "código"]) or ""
            descricao = pick_field(row, ["Descrição", "descricao", "Descri��o"]) or ""

            if not nome_tipo or not nome_codigo:
                skipped_count += 1
                continue

            nome_tipo_normalizado = normaliza(nome_tipo)
            tipo = tipos_cache.get(nome_tipo_normalizado)

            if not tipo:
                if create_types:
                    tipo = TipoCodigo.objects.create(nome=nome_tipo, descricao=descricao or "")
                    tipos_cache[normaliza(tipo.nome)] = tipo
                    print(f"Tipo criado: {tipo.id} - {tipo.nome}")
                else:
                    print(f"Ignorado (tipo ausente): {nome_tipo}")
                    skipped_count += 1
                    continue

            desc_merge = f"{nome_codigo} - {descricao}" if descricao else nome_codigo
            obj, created = Codigo.objects.get_or_create(
                tipo_codigo=tipo, nome=nome_codigo, defaults={"descricao": desc_merge}
            )
            if not created and (obj.descricao or "") != desc_merge:
                obj.descricao = desc_merge
                obj.save()
                updated_count += 1
                print(f"Atualizado: {nome_codigo} (Tipo: {tipo.nome})")
            elif created:
                created_count += 1
                print(f"Criado: {nome_codigo} (Tipo: {tipo.nome})")
            else:
                print(f"Já existia: {nome_codigo} (Tipo: {tipo.nome})")

    print("\nResumo:")
    print(f"Criados: {created_count}")
    print(f"Atualizados: {updated_count}")
    print(f"Ignorados: {skipped_count}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Importa códigos a partir de uma planilha CSV")
    parser.add_argument("--create-types", action="store_true", help="Criar Tipos ausentes automaticamente")
    args = parser.parse_args()

    print("Populando códigos associados aos tipos a partir do CSV...")
    popular_codigos(create_types=args.create_types)
    print("Concluído!")
