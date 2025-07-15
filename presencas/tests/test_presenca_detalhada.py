"""
Testes para o modelo PresencaDetalhada.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date

from presencas.models import PresencaDetalhada
from alunos.models import Aluno
from turmas.models import Turma
from atividades.models import Atividade
from cursos.models import Curso


class PresencaDetalhadaTest(TestCase):
    """Testes para o modelo PresencaDetalhada."""

    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar curso
        self.curso = Curso.objects.create(
            nome="Curso Teste",
            descricao="Descrição do curso teste"
        )
        
        # Criar turma
        self.turma = Turma.objects.create(
            nome="Turma 1",
            curso=self.curso,
            perc_carencia=75.0,
            data_inicio=date.today()
        )
        
        # Criar aluno
        self.aluno = Aluno.objects.create(
            cpf="12345678901",
            nome="João Silva",
            data_nascimento=date(1990, 1, 1),
            hora_nascimento="10:00",
            sexo="M",
            cor="Branco",
            fator_rh="+",
            tipo_sanguineo="O",
            naturalidade="São Paulo",
            uf_naturalidade="SP",
            situacao="ATIVO"
        )
        
        # Criar atividade
        self.atividade = Atividade.objects.create(
            nome="Atividade Teste",
            descricao="Descrição da atividade teste",
            tipo="ACADEMICA"
        )
        
        # Período (primeiro dia do mês)
        self.periodo = date(2024, 3, 1)

    def test_criacao_presenca_detalhada_valida(self):
        """Testa criação de presença detalhada válida."""
        presenca = PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=self.periodo,
            convocacoes=10,
            presencas=8,
            faltas=2,
            voluntario_extra=1,
            voluntario_simples=2
        )
        
        self.assertEqual(presenca.aluno, self.aluno)
        self.assertEqual(presenca.turma, self.turma)
        self.assertEqual(presenca.atividade, self.atividade)
        self.assertEqual(presenca.periodo, self.periodo)
        self.assertEqual(presenca.convocacoes, 10)
        self.assertEqual(presenca.presencas, 8)
        self.assertEqual(presenca.faltas, 2)
        self.assertEqual(presenca.voluntario_extra, 1)
        self.assertEqual(presenca.voluntario_simples, 2)

    def test_calculos_automaticos(self):
        """Testa os cálculos automáticos do modelo."""
        presenca = PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=self.periodo,
            convocacoes=10,
            presencas=8,
            faltas=2,
            voluntario_extra=1,
            voluntario_simples=2
        )
        
        # Verifica cálculo do percentual
        self.assertEqual(presenca.percentual_presenca, Decimal('80.00'))
        
        # Verifica cálculo do total de voluntários
        self.assertEqual(presenca.total_voluntarios, 3)
        
        # Verifica cálculo de carências (80% > 75% = 0 carências)
        self.assertEqual(presenca.carencias, 0)

    def test_calculo_carencias_abaixo_minimo(self):
        """Testa cálculo de carências quando abaixo do mínimo."""
        presenca = PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=self.periodo,
            convocacoes=10,
            presencas=6,  # 60% < 75%
            faltas=4,
            voluntario_extra=0,
            voluntario_simples=0
        )
        
        # Deve calcular carências
        self.assertGreater(presenca.carencias, 0)
        self.assertEqual(presenca.percentual_presenca, Decimal('60.00'))

    def test_validacao_presencas_faltas_maior_convocacoes(self):
        """Testa validação quando P + F > C."""
        with self.assertRaises(ValidationError):
            presenca = PresencaDetalhada(
                aluno=self.aluno,
                turma=self.turma,
                atividade=self.atividade,
                periodo=self.periodo,
                convocacoes=10,
                presencas=8,
                faltas=5,  # 8 + 5 = 13 > 10
                voluntario_extra=0,
                voluntario_simples=0
            )
            presenca.full_clean()

    def test_validacao_periodo_nao_primeiro_dia(self):
        """Testa validação quando período não é primeiro dia do mês."""
        with self.assertRaises(ValidationError):
            presenca = PresencaDetalhada(
                aluno=self.aluno,
                turma=self.turma,
                atividade=self.atividade,
                periodo=date(2024, 3, 15),  # Não é primeiro dia
                convocacoes=10,
                presencas=8,
                faltas=2,
                voluntario_extra=0,
                voluntario_simples=0
            )
            presenca.full_clean()

    def test_validacao_valores_negativos(self):
        """Testa validação para valores negativos."""
        with self.assertRaises(ValidationError):
            presenca = PresencaDetalhada(
                aluno=self.aluno,
                turma=self.turma,
                atividade=self.atividade,
                periodo=self.periodo,
                convocacoes=-1,  # Negativo
                presencas=8,
                faltas=2,
                voluntario_extra=0,
                voluntario_simples=0
            )
            presenca.full_clean()

    def test_unique_constraint(self):
        """Testa constraint único por aluno+turma+atividade+periodo."""
        # Criar primeira presença
        PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=self.periodo,
            convocacoes=10,
            presencas=8,
            faltas=2
        )
        
        # Tentar criar duplicata deve falhar
        with self.assertRaises(Exception):
            PresencaDetalhada.objects.create(
                aluno=self.aluno,
                turma=self.turma,
                atividade=self.atividade,
                periodo=self.periodo,  # Mesmo período
                convocacoes=5,
                presencas=4,
                faltas=1
            )

    def test_str_representation(self):
        """Testa representação string do modelo."""
        presenca = PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=self.periodo,
            convocacoes=10,
            presencas=8,
            faltas=2
        )
        
        expected = f"{self.aluno.nome} - 03/2024 - {self.atividade}"
        self.assertEqual(str(presenca), expected)

    def test_compatibilidade_sistema_atual(self):
        """Testa que o modelo não quebra o sistema atual."""
        # Verificar que o modelo Presenca original ainda funciona
        from presencas.models import Presenca
        
        presenca_original = Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            data=date.today(),
            presente=True,
            registrado_por="Sistema"
        )
        
        self.assertTrue(presenca_original.presente)
        self.assertEqual(presenca_original.aluno, self.aluno)
        
        # Verificar que aliases ainda funcionam
        from presencas.models import PresencaAcademica
        
        presenca_academica = PresencaAcademica.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            data=date.today(),
            presente=True,
            registrado_por="Sistema"
        )
        
        self.assertTrue(presenca_academica.presente)
