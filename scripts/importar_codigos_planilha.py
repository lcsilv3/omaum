import sys
import os
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
import django

BASE_DIR = Path(__file__).resolve().parent.parent


def main():
    # Configuração do Django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
    django.setup()

    from alunos.models import Codigo, TipoCodigo

    # Caminho da planilha (relativo ao repo)
    xlsx_path = BASE_DIR / "docs" / "Planilha de Códigos.xlsx"
    df = pd.read_excel(xlsx_path)

    # Limpa todos os códigos existentes (opcional, cuidado!)
    Codigo.objects.all().delete()

    for _, row in df.iterrows():
        tipo_codigo_id = int(row["código tipo"])
        nome = str(row["código"])  # número do código
        descricao = str(row["Descrição código"])
        # Garante que o tipo existe
        tipo, _ = TipoCodigo.objects.get_or_create(
            id=tipo_codigo_id, defaults={"nome": row["Descrição tipo"]}
        )
        Codigo.objects.create(nome=nome, descricao=descricao, tipo_codigo=tipo)
    print("Importação concluída.")


if __name__ == "__main__":
    main()
