from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand
from django.db import transaction

from alunos.models import Aluno
from alunos.services import (
    HistoricoService,
    HistoricoValidationError,
    sincronizar_historico_iniciatico,
)


class Command(BaseCommand):
    """Migra eventos legados do campo JSON para ``RegistroHistorico``."""

    help = (
        "Migra registros do campo historico_iniciatico (JSON) para RegistroHistorico."
    )

    def add_arguments(self, parser) -> None:  # noqa: D401 - Descrição no help
        parser.add_argument(
            "--cpf",
            nargs="*",
            dest="cpfs",
            help="Lista opcional de CPFs (apenas dígitos) a serem processados.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            dest="limit",
            help="Limita a quantidade de alunos processados.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            dest="dry_run",
            help="Executa a migração sem persistir alterações no banco.",
        )
        parser.add_argument(
            "--saida",
            dest="saida",
            help="Caminho opcional para salvar o relatório CSV gerado.",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        cpfs = options.get("cpfs") or []
        limit = options.get("limit")
        dry_run = bool(options.get("dry_run"))
        saida = options.get("saida")

        relatorio: list[dict[str, str]] = []
        total_eventos = total_criados = total_erros = total_ignorados = 0

        queryset = Aluno.objects.all().order_by("id")
        if cpfs:
            cpfs_limpos = [
                cpf.strip().replace(".", "").replace("-", "") for cpf in cpfs if cpf
            ]
            queryset = queryset.filter(cpf__in=cpfs_limpos)

        if limit is not None:
            queryset = queryset[:limit]

        self.stdout.write(
            self.style.WARNING(
                f"Iniciando migração de históricos (alunos={queryset.count()}, dry_run={dry_run})."
            )
        )

        cache_codigos: dict[str, int] = {}
        for aluno in queryset.iterator():
            eventos_json = (
                aluno.historico_iniciatico
                if isinstance(aluno.historico_iniciatico, list)
                else []
            )
            if not eventos_json:
                continue

            with transaction.atomic():
                for evento in eventos_json:
                    total_eventos += 1
                    try:
                        payload = HistoricoService.converter_evento_legado(
                            evento,
                            cache_codigos=cache_codigos,
                        )
                    except HistoricoValidationError as exc:
                        total_erros += 1
                        relatorio.append(
                            self._montar_linha_relatorio(
                                aluno, evento, "erro", exc.messages
                            )
                        )
                        continue

                    try:
                        HistoricoService.criar_evento(aluno, payload)
                    except HistoricoValidationError as exc:
                        total_ignorados += 1
                        relatorio.append(
                            self._montar_linha_relatorio(
                                aluno, evento, "ignorado", exc.messages
                            )
                        )
                        continue

                    total_criados += 1
                    relatorio.append(
                        self._montar_linha_relatorio(aluno, evento, "migrado", [])
                    )

                if dry_run:
                    transaction.set_rollback(True)
                else:
                    sincronizar_historico_iniciatico(aluno)

        caminho_csv = self._gravar_relatorio(relatorio, saida)

        resumo = (
            f"Eventos lidos: {total_eventos} | Criados: {total_criados} | "
            f"Ignorados: {total_ignorados} | Erros: {total_erros}"
        )
        self.stdout.write(self.style.SUCCESS(resumo))
        self.stdout.write(self.style.SUCCESS(f"Relatório salvo em: {caminho_csv}"))

    def _montar_linha_relatorio(
        self,
        aluno: Aluno,
        evento: Any,
        status: str,
        mensagens: list[str],
    ) -> dict[str, str]:
        ordem_servico = str(
            evento.get("ordem_servico") or evento.get("ordemservico") or ""
        ).strip()
        codigo_repr = str(
            evento.get("codigo_id") or evento.get("descricao") or ""
        ).strip()
        data_repr = str(evento.get("data") or evento.get("data_os") or "").strip()

        return {
            "aluno_id": str(aluno.id),
            "cpf": aluno.cpf,
            "ordem_servico": ordem_servico,
            "codigo": codigo_repr,
            "data_os": data_repr,
            "status": status,
            "mensagem": " | ".join(mensagens) if mensagens else "",
        }

    def _gravar_relatorio(self, linhas: list[dict[str, str]], saida: str | None) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = (
            Path(saida).expanduser()
            if saida
            else Path.cwd() / f"historicos_migracao_{timestamp}.csv"
        )

        with caminho.open("w", encoding="utf-8", newline="") as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=[
                    "aluno_id",
                    "cpf",
                    "ordem_servico",
                    "codigo",
                    "data_os",
                    "status",
                    "mensagem",
                ],
            )
            writer.writeheader()
            for linha in linhas:
                writer.writerow(linha)

        return str(caminho)
