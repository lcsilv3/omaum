import unicodedata


def normaliza(texto: str) -> str:
    """Normaliza texto para comparação: remove acentos, decoda caracteres não-ASCII e lower."""
    return (
        unicodedata.normalize("NFKD", texto or "")
        .encode("ASCII", "ignore")
        .decode("ASCII")
        .strip()
        .lower()
    )


def pick_field(row: dict, candidates: list[str]) -> str | None:
    """Tenta extrair um campo de `row` testando vários nomes possíveis em `candidates`.

    A comparação ignora acentos e case (usa `normaliza`). Retorna o valor encontrado
    ou None.
    """
    keys = list(row.keys())
    norm_keys = {normaliza(k): k for k in keys}
    for cand in candidates:
        nk = normaliza(cand)
        if nk in norm_keys:
            return row.get(norm_keys[nk])
    return None
