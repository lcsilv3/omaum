"""Converte a planilha Excel `scripts/Planilha de Códigos.xlsx` para CSV no caminho `scripts/docs/Planilha de Códigos.csv`.
Uso:
  python scripts/convert_xlsx_to_csv.py

Requisitos: pandas (pip install pandas openpyxl)
"""

from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parents[1]
input_xlsx = repo_root / "scripts" / "Planilha de Códigos.xlsx"
output_dir = repo_root / "scripts" / "docs"
output_csv = output_dir / "Planilha de Códigos.csv"

if not input_xlsx.exists():
    print(f"Arquivo de entrada não encontrado: {input_xlsx}")
    sys.exit(1)

try:
    import pandas as pd
except ImportError:
    print(
        "Biblioteca 'pandas' não encontrada. Instale com: pip install pandas openpyxl"
    )
    sys.exit(2)

output_dir.mkdir(parents=True, exist_ok=True)

print(f"Lendo {input_xlsx}...")
df = pd.read_excel(input_xlsx)
print(f"Escrevendo {output_csv} (encoding latin1, separador ';')...")
df.to_csv(output_csv, sep=";", index=False, encoding="latin1")
print("Concluído.")
