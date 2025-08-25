#!/usr/bin/env python
"""
Script para popular códigos associados aos tipos existentes no banco.
"""

import os
import csv
import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from alunos.utils import get_tipo_codigo_model, get_codigo_model

TipoCodigo = get_tipo_codigo_model()
Codigo = get_codigo_model()

CSV_PATH = os.path.join(os.path.dirname(__file__), "docs", "Planilha de Códigos.csv")


def popular_codigos():
    with open(CSV_PATH, encoding="latin1") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        import unicodedata

        for row in reader:
            nome_tipo = row.get("Tipo") or row.get("tipo")
            nome_codigo = row.get("Nome") or row.get("nome")
            descricao = (
                row.get("Descrição") or row.get("descricao") or row.get("Descri��o")
            )
            if not nome_tipo or not nome_codigo:
                continue

            # Normalizar para remover caracteres estranhos e acentuação corrompida
            def normaliza(texto):
                return (
                    unicodedata.normalize("NFKD", texto or "")
                    .encode("ASCII", "ignore")
                    .decode("ASCII")
                    .strip()
                    .lower()
                )

            nome_tipo_normalizado = normaliza(nome_tipo)
            tipo = None
            for t in TipoCodigo.objects.all():
                if normaliza(t.nome) == nome_tipo_normalizado:
                    tipo = t
                    break
            if not tipo:
                print(
                    f"Tipo não encontrado: {nome_tipo} (normalizado: {nome_tipo_normalizado})"
                )
                continue
            # Se houver descrição, salva como 'NÚMERO - DESCRIÇÃO', senão só o número
            desc_merge = f"{nome_codigo} - {descricao}" if descricao else nome_codigo
            obj, created = Codigo.objects.get_or_create(
                tipo_codigo=tipo, nome=nome_codigo, defaults={"descricao": desc_merge}
            )
            # Atualiza descrição se já existe e está diferente
            if not created and obj.descricao != desc_merge:
                obj.descricao = desc_merge
                obj.save()
            acao = "Criado" if created else "Já existia"
            print(f"{acao}: {nome_codigo} (Tipo: {nome_tipo})")


if __name__ == "__main__":
    print("Populando códigos associados aos tipos a partir do CSV...")
    popular_codigos()
    print("Concluído!")
