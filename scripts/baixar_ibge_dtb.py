"""Baixa o pacote DTB (Divisão Territorial Brasileira) do IBGE e extrai o CSV de municípios.

Uso rápido:
  python scripts/baixar_ibge_dtb.py            # baixa ano padrão (2024) e grava em docs/ibge_municipios.csv
  python scripts/baixar_ibge_dtb.py --ano 2023 # outro ano
  python scripts/baixar_ibge_dtb.py --force    # sobrescreve arquivo existente

Requisitos: somente biblioteca padrão + chardet (já no requirements.txt).
Fonte oficial: https://geoftp.ibge.gov.br/organizacao_do_territorio/estrutura_territorial/divisao_territorial/{ANO}/DTB_{ANO}.zip
"""

from __future__ import annotations

import argparse
import io
import sys
import zipfile
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

import chardet  # type: ignore


def detectar_encoding(data: bytes) -> str:
    result = chardet.detect(data)
    enc = (result.get("encoding") or "latin-1").lower()
    # IBGE costuma vir como ISO-8859-1 (latin-1)
    if enc in {"iso-8859-1", "windows-1252"}:
        return "latin-1"
    return enc


def baixar_zip(ano: int) -> bytes:
    url = f"https://geoftp.ibge.gov.br/organizacao_do_territorio/estrutura_territorial/divisao_territorial/{ano}/DTB_{ano}.zip"
    print(f"[*] Baixando: {url}")
    try:
        with urlopen(url) as resp:  # nosec B310 - URL controlada
            return resp.read()
    except HTTPError as e:  # pragma: no cover - fluxo de erro simples
        raise SystemExit(f"Falha HTTP {e.code} ao baixar ZIP: {e.reason}")
    except URLError as e:  # pragma: no cover
        raise SystemExit(
            f"Erro de rede ao baixar ZIP: {e.reason}\nVerifique conexão ou se o ano {ano} já está disponível."
        )


def _converter_xls_para_csv(xls_bytes: bytes) -> str:
    """Converte planilha XLS em CSV (UTF-8) usando xlrd.

    Mantém ordem das colunas e converte números inteiros sem sufixo .0.
    """
    try:
        import xlrd  # type: ignore
    except ImportError:  # pragma: no cover - fluxo de dependência
        raise SystemExit(
            "Dependência 'xlrd' não encontrada para ler arquivo XLS. Instale com: pip install xlrd"
        )

    book = xlrd.open_workbook(file_contents=xls_bytes)
    sheet = book.sheet_by_index(0)
    linhas_out: list[str] = []

    def fmt(cell) -> str:  # type: ignore
        import xlrd  # local import para tipos

        if cell.ctype == xlrd.XL_CELL_NUMBER:
            val = cell.value
            try:
                if float(val).is_integer():  # evita 1234.0
                    return str(int(val))
            except Exception:  # pragma: no cover
                return str(val)
            return str(val)
        return str(cell.value)

    for r in range(sheet.nrows):
        row = [fmt(sheet.cell(r, c)).strip() for c in range(sheet.ncols)]
        # Remover separadores de linha internos e normalizar ; se aparecer vírgula no futuro
        row_norm = [col.replace("\n", " ").replace("\r", " ") for col in row]
        linhas_out.append(",".join(row_norm))
    return "\n".join(linhas_out)


def extrair_csv_municipios(zip_bytes: bytes, listar: bool = False) -> tuple[str, str]:
    """Retorna (nome_arquivo_original_no_zip, conteudo_csv_utf8).

    Fluxo:
      1. Procura CSV direto (anos antigos).
      2. Senão, procura XLS (ex: 2024) e converte.
      3. Senão, tenta ODS (se biblioteca disponível) e converte (TODO).
    """
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        nomes = zf.namelist()
        if listar:
            print("Arquivos dentro do ZIP:")
            for n in nomes:
                print(" -", n)
            raise SystemExit(0)

        # 1) CSV direto
        padroes_base = [
            "RELATORIO_DTB_BRASIL_MUNICIPIO",
            "RELATORIO_DTB_BRASIL_MUNICIPIOS",
            "MUNICIPIO",
            "MUNICIPIOS",
        ]
        candidatos_csv: list[str] = []
        for p in padroes_base:
            for n in nomes:
                up = n.upper()
                if p in up and n.lower().endswith(".csv"):
                    candidatos_csv.append(n)
            if candidatos_csv:
                break
        if not candidatos_csv:  # fallback genérico
            for n in nomes:
                if "MUN" in n.upper() and n.lower().endswith(".csv"):
                    candidatos_csv.append(n)
        if candidatos_csv:
            alvo = sorted(candidatos_csv)[0]
            raw = zf.read(alvo)
            encoding = detectar_encoding(raw)
            texto = raw.decode(encoding, errors="replace").replace("\r\n", "\n")
            return alvo, texto

        # 2) XLS (cenário 2024)
        candidatos_xls: list[str] = []
        for p in padroes_base:
            for n in nomes:
                up = n.upper()
                if p in up and n.lower().endswith(".xls"):
                    candidatos_xls.append(n)
            if candidatos_xls:
                break
        if candidatos_xls:
            alvo = sorted(candidatos_xls)[0]
            raw = zf.read(alvo)
            texto = _converter_xls_para_csv(raw)
            return alvo, texto

        # 3) (Futuro) ODS
        candidatos_ods: list[str] = []
        for p in padroes_base:
            for n in nomes:
                up = n.upper()
                if p in up and n.lower().endswith(".ods"):
                    candidatos_ods.append(n)
            if candidatos_ods:
                break
        if candidatos_ods:
            alvo = sorted(candidatos_ods)[0]
            try:
                # Implementação adiada para evitar dependências pesadas se não for necessária
                import pandas as pd  # type: ignore
            except ImportError:  # pragma: no cover
                raise SystemExit(
                    "Arquivo ODS encontrado mas dependência 'pandas' (e 'odfpy') não estão instaladas. Instale com: pip install pandas odfpy"
                )
            raw = zf.read(alvo)
            # pandas lê direto bytes via BytesIO
            df = pd.read_excel(io.BytesIO(raw), engine=None)  # type: ignore
            texto = df.to_csv(index=False)
            return alvo, texto

        print(
            "Nenhum arquivo de municípios encontrado em formatos suportados (CSV/XLS/ODS)."
        )
        print("Arquivos no ZIP:")
        for n in nomes:
            print(" -", n)
        raise SystemExit(
            "Falha na extração: padrões MUNICIPIO/MUNICIPIOS não localizaram CSV/XLS/ODS compatível."
        )


def salvar_conteudo(dest: Path, conteudo: str, force: bool) -> None:
    if dest.exists() and not force:
        print(f"[!] Arquivo já existe: {dest} (use --force para sobrescrever)")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(conteudo, encoding="utf-8")
    print(f"[+] Salvo CSV em: {dest} ({dest.stat().st_size/1024:.1f} KB)")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Baixa e extrai CSV de municípios IBGE (DTB)"
    )
    parser.add_argument(
        "--ano", type=int, default=2024, help="Ano da DTB (padrão: 2024)"
    )
    parser.add_argument(
        "--dest",
        default="docs/ibge_municipios.csv",
        help="Destino do CSV (padrão: docs/ibge_municipios.csv)",
    )
    parser.add_argument(
        "--force", action="store_true", help="Sobrescreve arquivo destino se existir"
    )
    parser.add_argument(
        "--listar-zip",
        action="store_true",
        help="Apenas lista arquivos dentro do ZIP e sai (debug)",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    zip_bytes = baixar_zip(args.ano)
    nome_zip, conteudo = extrair_csv_municipios(zip_bytes, listar=args.listar_zip)
    print(f"[*] Arquivo encontrado no ZIP: {nome_zip}")
    linhas = conteudo.strip().splitlines()
    print(f"[*] Linhas detectadas (inclui cabeçalho): {len(linhas)}")
    salvar_conteudo(Path(args.dest), conteudo, args.force)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
