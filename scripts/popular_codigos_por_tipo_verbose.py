#!/usr/bin/env python
"""
Versão verbosa do importador de códigos.
- cria `TipoCodigo` ausente quando necessário
- imprime ação por linha (criado/atualizado/existia)

Uso: definir DJANGO_SETTINGS_MODULE no ambiente ou exportá-lo antes de executar.
"""

import os
import csv
import django

# Configurar Django (respeita DJANGO_SETTINGS_MODULE já definido no ambiente)
if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings.production")
django.setup()

from alunos.utils import get_tipo_codigo_model, get_codigo_model

TipoCodigo = get_tipo_codigo_model()
Codigo = get_codigo_model()

CSV_PATH = os.path.join(os.path.dirname(__file__), "docs", "Planilha de Códigos.csv")


def popular_codigos_create_types():
    if not os.path.exists(CSV_PATH):
        print(f"CSV não encontrado em: {CSV_PATH}")
        return

    with open(CSV_PATH, encoding="latin1") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        import unicodedata

        def pick_field(row, candidates):
            # tenta várias chaves possíveis (ignorando acentos e case)
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

        for row in reader:
            nome_tipo = pick_field(row, ["Tipo", "tipo", "codigo tipo", "código tipo", "c�digo tipo", "unnamed: 0"]) or ""
            nome_codigo = pick_field(row, ["Nome", "nome", "codigo", "código", "c�digo"]) or ""
            descricao = pick_field(row, ["Descrição", "descricao", "Descri��o", "Descri\u00e7\u00e3o", "Descri\u00e7\u00e3o tipo"]) or ""
            if not nome_tipo or not nome_codigo:
                continue

            # Normalizar para comparação
            def normaliza(texto):
                return (
                    unicodedata.normalize("NFKD", texto or "")
                    .encode("ASCII", "ignore")
                    .decode("ASCII")
                    .strip()
                )

            nome_tipo_normalizado = normaliza(nome_tipo).lower()

            # Tenta encontrar o tipo por comparação normalizada
            tipo = None
            for t in TipoCodigo.objects.all():
                if normaliza(t.nome).lower() == nome_tipo_normalizado:
                    tipo = t
                    break

            if not tipo:
                tipo = TipoCodigo.objects.create(nome=nome_tipo, descricao=descricao or "")
                print(f"Tipo criado: {tipo.id} - {tipo.nome}")

            # Descrição final para o Código
            desc_merge = f"{nome_codigo} - {descricao}" if descricao else nome_codigo

            obj, created = Codigo.objects.get_or_create(
                tipo_codigo=tipo, nome=nome_codigo, defaults={"descricao": desc_merge}
            )
            if not created and obj.descricao != desc_merge:
                obj.descricao = desc_merge
                obj.save()
                print(f"Atualizado: {nome_codigo} (Tipo: {tipo.nome})")
            else:
                acao = "Criado" if created else "Já existia"
                print(f"{acao}: {nome_codigo} (Tipo: {tipo.nome})")


if __name__ == "__main__":
    print("Populando (verboso) códigos e tipos a partir do CSV...")
    popular_codigos_create_types()
    print("Concluído")
