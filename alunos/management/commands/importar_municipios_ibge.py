import csv
import unicodedata
from pathlib import Path
from typing import Dict, Optional, List

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from alunos.models import Estado, Cidade

REGIOES_UF = {
    "AC": "Norte",
    "AL": "Nordeste",
    "AP": "Norte",
    "AM": "Norte",
    "BA": "Nordeste",
    "CE": "Nordeste",
    "DF": "Centro-Oeste",
    "ES": "Sudeste",
    "GO": "Centro-Oeste",
    "MA": "Nordeste",
    "MT": "Centro-Oeste",
    "MS": "Centro-Oeste",
    "MG": "Sudeste",
    "PA": "Norte",
    "PB": "Nordeste",
    "PR": "Sul",
    "PE": "Nordeste",
    "PI": "Nordeste",
    "RJ": "Sudeste",
    "RN": "Nordeste",
    "RS": "Sul",
    "RO": "Norte",
    "RR": "Norte",
    "SC": "Sul",
    "SP": "Sudeste",
    "SE": "Nordeste",
    "TO": "Norte",
}


class Command(BaseCommand):
    help = "Importa (ou atualiza) municípios a partir do CSV da DTB IBGE salvando em Cidade.codigo_ibge."

    def add_arguments(self, parser):  # pragma: no cover - argumentos simples
        parser.add_argument(
            "--csv",
            default="docs/ibge_municipios.csv",
            help="Caminho para CSV baixado (padrão: docs/ibge_municipios.csv)",
        )
        parser.add_argument(
            "--limit-uf",
            nargs="*",
            help="Importar apenas estas UFs (ex: --limit-uf SP RJ MG)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Mostra contagens sem gravar no banco",
        )
        parser.add_argument(
            "--replace-names",
            action="store_true",
            help=(
                "Se cidade já existir pela combinação (nome, estado) mas com codigo_ibge diferente, "
                "atualiza o codigo. Se nome divergir mas mesmo codigo_ibge existir em outra cidade, renomeia."
            ),
        )

    def handle(self, *args, **options):
        caminho = Path(options["--csv"] if "--csv" in options else options["csv"])
        if not caminho.exists():
            raise CommandError(f"CSV não encontrado: {caminho}")

        limit_ufs = set([u.upper() for u in (options.get("limit_uf") or [])])
        dry_run = options["dry_run"]
        replace_names = options["replace_names"]

        self.stdout.write(self.style.NOTICE(f"Lendo CSV: {caminho}"))
        with caminho.open("r", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f)
            linhas = list(reader)
        if not linhas:
            raise CommandError("CSV vazio")

        # Normalização de cabeçalhos: remove acentos, substitui _ por espaço, uppercase
        def norm(text: str) -> str:
            nfkd = unicodedata.normalize("NFD", text)
            sem_acento = "".join(ch for ch in nfkd if not unicodedata.combining(ch))
            return sem_acento.replace("_", " ").strip().upper()

        # Encontrar a primeira linha que contenha os cabeçalhos de interesse
        header_raw: Optional[List[str]] = None
        header_idx = 0
        for i, row in enumerate(linhas):
            if not row:
                continue
            normed = [norm(c) for c in row]
            if any("MUNICIPIO" in c for c in normed) and any("UF" == c or c.endswith(" UF") or c == "UF" for c in normed):
                # Heurística: linha com 'MUNICIPIO' e 'UF' e algum 'CODIGO' possivelmente
                if any("CODIGO" in c and "MUNICIPIO" in c for c in normed) or any("CD MUN" in c for c in normed):
                    header_raw = row
                    header_idx = i
                    break
        if header_raw is None:
            raise CommandError("Cabeçalho de municípios não encontrado (verifique se o arquivo é o correto da DTB).")

        header_norm = [norm(h) for h in header_raw]

        def idx(*possiveis) -> Optional[int]:
            for p in possiveis:
                p_norm = norm(p)
                for j, col in enumerate(header_norm):
                    if col == p_norm:
                        return j
            return None

        idx_codigo_mun = idx(
            "CD_MUN",
            "CODIGO_MUNICIPIO_COMPLETO",
            "CODIGO MUNICIPIO COMPLETO",
            "CODIGO_MUNICIPIO",
            "CODIGO MUNICIPIO",
        )
        idx_nome_mun = idx(
            "NM_MUN",
            "NOME_MUNICIPIO",
            "NOME MUNICIPIO",
            "MUNICIPIO",
            "NOME_MUNICIPIO",
            "NOME MUNICIPIO",
        )
        idx_sigla_uf = idx("SIGLA_UF", "UF", "SG_UF")

        if None in (idx_codigo_mun, idx_nome_mun, idx_sigla_uf):
            raise CommandError(
                "Não foi possível detectar colunas obrigatórias (código município, nome município, sigla/UF)."
            )

        # Mapear código numérico de UF -> sigla se encontrado número em vez de sigla
        CODIGO_UF_TO_SIGLA = {
            "11": "RO",
            "12": "AC",
            "13": "AM",
            "14": "RR",
            "15": "PA",
            "16": "AP",
            "17": "TO",
            "21": "MA",
            "22": "PI",
            "23": "CE",
            "24": "RN",
            "25": "PB",
            "26": "PE",
            "27": "AL",
            "28": "SE",
            "29": "BA",
            "31": "MG",
            "32": "ES",
            "33": "RJ",
            "35": "SP",
            "41": "PR",
            "42": "SC",
            "43": "RS",
            "50": "MS",
            "51": "MT",
            "52": "GO",
            "53": "DF",
        }

        total_linhas = 0
        criadas_cidades = 0
        atualizadas_codigo = 0
        renomeadas = 0
        ignoradas_uf = 0

        estados_cache: Dict[str, Estado] = {e.codigo: e for e in Estado.objects.all()}

        @transaction.atomic
        def processar():
            nonlocal total_linhas, criadas_cidades, atualizadas_codigo, renomeadas, ignoradas_uf
            for row in linhas[header_idx + 1 :]:
                if not row or len(row) <= idx_sigla_uf:
                    continue
                try:
                    uf_val = row[idx_sigla_uf].strip().upper()
                    # Converter número -> sigla quando necessário
                    if uf_val.isdigit() and uf_val in CODIGO_UF_TO_SIGLA:
                        sigla = CODIGO_UF_TO_SIGLA[uf_val]
                    else:
                        sigla = uf_val
                    if limit_ufs and sigla not in limit_ufs:
                        ignoradas_uf += 1
                        continue
                    cod_mun = row[idx_codigo_mun].strip()
                    nome_mun = row[idx_nome_mun].strip()
                    if not cod_mun or not nome_mun or not sigla:
                        continue
                    estado = estados_cache.get(sigla)
                    if not estado:
                        regiao = REGIOES_UF.get(sigla, "Sudeste")
                        estado = Estado.objects.create(codigo=sigla, nome=sigla, regiao=regiao)
                        estados_cache[sigla] = estado
                    existente_por_codigo = Cidade.objects.filter(codigo_ibge=cod_mun).first()
                    if existente_por_codigo:
                        if (
                            replace_names
                            and existente_por_codigo.nome != nome_mun
                            and existente_por_codigo.estado == estado
                        ):
                            existente_por_codigo.nome = nome_mun
                            existente_por_codigo.save(update_fields=["nome"])
                            renomeadas += 1
                        total_linhas += 1
                        continue
                    cidade = Cidade.objects.filter(nome=nome_mun, estado=estado).first()
                    if cidade:
                        if not cidade.codigo_ibge:
                            cidade.codigo_ibge = cod_mun
                            cidade.save(update_fields=["codigo_ibge"])
                            atualizadas_codigo += 1
                    else:
                        Cidade.objects.create(
                            nome=nome_mun,
                            estado=estado,
                            codigo_ibge=cod_mun,
                        )
                        criadas_cidades += 1
                    total_linhas += 1
                except Exception as exc:  # pragma: no cover
                    self.stderr.write(f"Linha ignorada por erro: {exc}")

        if dry_run:
            try:
                with transaction.atomic():
                    processar()
                    raise RuntimeError("rollback")
            except RuntimeError:
                pass
        else:
            processar()

        resumo_parte1 = (
            f"Processadas: {total_linhas} | Criadas: {criadas_cidades} | "
            f"Atualizadas codigo: {atualizadas_codigo} | Renomeadas: {renomeadas} | "
        )
        resumo_parte2 = f"Ignoradas UF: {ignoradas_uf} | Dry-run: {dry_run}"
        self.stdout.write(self.style.SUCCESS(resumo_parte1 + resumo_parte2))
