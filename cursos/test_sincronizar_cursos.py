from django.test import TestCase

from cursos import services
from cursos.models import Curso


class SincronizarCursosServiceTest(TestCase):
    """Testes para a rotina de sincronização de cursos."""

    def test_criar_e_reativar_cursos(self):
        """Cria novo curso e reativa um curso previamente inativo."""

        curso_inativo = Curso.objects.create(
            nome="Curso Antigo",
            descricao="Versao antiga",
            ativo=False,
        )

        dados = [
            {
                "linha": 2,
                "nome": "Curso Novo",
                "descricao": "Entrada nova",
                "ativo": "1",
            },
            {
                "linha": 3,
                "nome": "Curso Antigo",
                "descricao": "Atualizado",
                "ativo": "sim",
            },
        ]

        resumo = services.sincronizar_cursos(dados)

        self.assertEqual(resumo["criados"], 1)
        self.assertEqual(resumo["reativados"], 1)
        self.assertEqual(resumo["desativados"], 0)
        self.assertEqual(resumo["processados"], 2)

        curso_novo = Curso.objects.get(nome="Curso Novo")
        self.assertTrue(curso_novo.ativo)

        curso_inativo.refresh_from_db()
        self.assertTrue(curso_inativo.ativo)
        self.assertEqual(curso_inativo.descricao, "Atualizado")

    def test_desativar_cursos_nao_listados(self):
        """Desativa cursos ativos que não aparecem na planilha."""

        Curso.objects.create(nome="Curso 1", descricao="Descricao 1", ativo=True)
        curso_desativado = Curso.objects.create(
            nome="Curso 2",
            descricao="Descricao 2",
            ativo=True,
        )

        resumo = services.sincronizar_cursos(
            [{"linha": 2, "nome": "Curso 1", "descricao": "Atualizado"}]
        )

        curso_desativado.refresh_from_db()
        self.assertFalse(curso_desativado.ativo)
        self.assertEqual(resumo["desativados"], 1)
        self.assertEqual(resumo["criados"], 0)

    def test_ignorar_linha_sem_nome_e_id(self):
        """Ignora registros que não possuem identificador nem nome."""

        resumo = services.sincronizar_cursos(
            [{"linha": 5, "descricao": "Sem nome", "ativo": "1"}]
        )

        self.assertEqual(resumo["processados"], 0)
        self.assertEqual(len(resumo["avisos"]), 1)
        self.assertIn("Linha 5", resumo["avisos"][0])
