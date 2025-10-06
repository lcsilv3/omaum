from __future__ import annotations

import csv
import tempfile
from io import StringIO
from pathlib import Path
from typing import Any

from django.core.management import call_command
from django.test import TestCase

from alunos.models import Aluno, Codigo, RegistroHistorico, TipoCodigo


class MigrarHistoricosCommandTests(TestCase):
    """Cenários de integração para o comando ``migrar_historicos``."""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.tipo = TipoCodigo.objects.create(nome="Progressao", descricao="")
        cls.codigo = Codigo.objects.create(
            tipo_codigo=cls.tipo,
            nome="Grau I",
            descricao="Primeiro Grau",
        )

    def _criar_aluno(self, **extra: Any) -> Aluno:
        defaults = {
            "cpf": "98765432100",
            "nome": "Aluno Migração",
            "data_nascimento": "1995-01-01",
            "email": "migracao@example.com",
            "sexo": "M",
            "numero_iniciatico": "M0001",
        }
        defaults.update(extra)
        return Aluno.objects.create(**defaults)

    def test_migracao_cria_registros_e_relatorio(self) -> None:
        aluno = self._criar_aluno()
        aluno.historico_iniciatico = [
            {
                "codigo_id": self.codigo.id,
                "data": "2023-05-10",
                "ordem_servico": "OS/2023",
                "observacoes": "Entrada via JSON",
            }
        ]
        aluno.save(update_fields=["historico_iniciatico"])

        with tempfile.TemporaryDirectory() as tmpdir:
            relatorio = Path(tmpdir) / "relatorio.csv"
            out = StringIO()

            call_command("migrar_historicos", "--saida", str(relatorio), stdout=out)

            aluno.refresh_from_db()
            registros = RegistroHistorico.objects.filter(aluno=aluno)

            self.assertEqual(registros.count(), 1)
            self.assertTrue(relatorio.exists())
            with relatorio.open(encoding="utf-8") as csvfile:
                linhas = list(csv.DictReader(csvfile))
            self.assertEqual(linhas[0]["status"], "migrado")

    def test_dry_run_nao_persiste_registros(self) -> None:
        aluno = self._criar_aluno(
            cpf="11122233344", email="dry@example.com", numero_iniciatico="M0002"
        )
        aluno.historico_iniciatico = [
            {
                "codigo_id": self.codigo.id,
                "data": "2022-01-15",
            }
        ]
        aluno.save(update_fields=["historico_iniciatico"])

        with tempfile.TemporaryDirectory() as tmpdir:
            relatorio = Path(tmpdir) / "relatorio.csv"
            out = StringIO()
            call_command(
                "migrar_historicos", "--dry-run", "--saida", str(relatorio), stdout=out
            )

        self.assertEqual(RegistroHistorico.objects.filter(aluno=aluno).count(), 0)
        aluno.refresh_from_db()
        self.assertEqual(
            aluno.historico_iniciatico,
            [
                {
                    "codigo_id": self.codigo.id,
                    "data": "2022-01-15",
                }
            ],
        )
