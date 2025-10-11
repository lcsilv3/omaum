from datetime import date, timedelta

from django.test import TestCase

from alunos.models import Aluno, Codigo, TipoCodigo
from alunos.services import (
    HistoricoEventoDados,
    HistoricoService,
    HistoricoValidationError,
)


class HistoricoServiceTestCase(TestCase):
    """Testes para a camada de serviços do histórico iniciático."""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.aluno = Aluno.objects.create(
            cpf="12345678901",
            nome="Aluno Teste",
            data_nascimento=date(1990, 1, 1),
            email="aluno@example.com",
            sexo="M",
            numero_iniciatico="0001",
        )
        cls.tipo = TipoCodigo.objects.create(nome="Progressao", descricao="")
        cls.codigo = Codigo.objects.create(
            tipo_codigo=cls.tipo,
            nome="Grau I",
            descricao="Primeiro grau",
        )

    def test_criar_evento_normaliza_ordem_servico(self) -> None:
        registro = HistoricoService.criar_evento(
            self.aluno,
            {
                "codigo_id": self.codigo.id,
                "data_os": date(2024, 1, 15),
                "ordem_servico": "OS/24",
                "observacoes": "Cerimônia realizada",
            },
        )

        self.assertEqual(registro.ordem_servico, "OS/2024")
        self.assertEqual(registro.codigo, self.codigo)

        self.aluno.refresh_from_db()
        self.assertEqual(self.aluno.historico_iniciatico[0]["ordem_servico"], "OS/2024")

    def test_criar_evento_rejeita_data_futura(self) -> None:
        with self.assertRaises(HistoricoValidationError):
            HistoricoService.criar_evento(
                self.aluno,
                HistoricoEventoDados(
                    codigo_id=self.codigo.id,
                    data_os=date.today() + timedelta(days=1),
                ),
            )

    def test_nao_permite_duplicacao_codigo_ordem(self) -> None:
        HistoricoService.criar_evento(
            self.aluno,
            {
                "codigo_id": self.codigo.id,
                "data_os": date(2023, 5, 20),
                "ordem_servico": "ABC/2023",
            },
        )

        with self.assertRaises(HistoricoValidationError):
            HistoricoService.criar_evento(
                self.aluno,
                {
                    "codigo_id": self.codigo.id,
                    "data_os": date(2023, 6, 1),
                    "ordem_servico": "ABC/2023",
                },
            )

    def test_desativar_e_reativar_evento(self) -> None:
        registro = HistoricoService.criar_evento(
            self.aluno,
            {
                "codigo_id": self.codigo.id,
                "data_os": date(2022, 3, 10),
                "observacoes": "Registro ativo",
            },
        )

        HistoricoService.desativar_evento(registro, motivo="Correção solicitada")
        registro.refresh_from_db()
        self.assertFalse(registro.ativo)
        self.assertIn("Correção solicitada", registro.observacoes)

        HistoricoService.reativar_evento(registro)
        registro.refresh_from_db()
        self.assertTrue(registro.ativo)

    def test_listar_incluir_inativos(self) -> None:
        ativo = HistoricoService.criar_evento(
            self.aluno,
            {
                "codigo_id": self.codigo.id,
                "data_os": date(2021, 7, 1),
            },
        )
        inativo = HistoricoService.criar_evento(
            self.aluno,
            {
                "codigo_id": self.codigo.id,
                "data_os": date(2020, 5, 1),
            },
        )
        HistoricoService.desativar_evento(inativo)

        ativos = list(HistoricoService.listar(self.aluno))
        todos = list(HistoricoService.listar(self.aluno, incluir_inativos=True))

        self.assertIn(ativo, ativos)
        self.assertNotIn(inativo, ativos)
        self.assertIn(inativo, todos)

    def test_converter_evento_legado_usando_descricao(self) -> None:
        evento = {
            "descricao": "Grau I",
            "tipo": "Progressao",
            "data": "2024-01-01",
            "ordem_servico": "OS/2024",
            "observacoes": "Gerado via JSON",
        }

        payload = HistoricoService.converter_evento_legado(evento)

        self.assertEqual(payload.codigo_id, self.codigo.id)
        self.assertEqual(payload.data_os, date(2024, 1, 1))
        self.assertEqual(payload.ordem_servico, "OS/2024")

    def test_converter_evento_legado_rejeita_sem_data(self) -> None:
        evento = {
            "codigo_id": self.codigo.id,
        }

        with self.assertRaises(HistoricoValidationError):
            HistoricoService.converter_evento_legado(evento)
