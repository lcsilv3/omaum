"""
Testes para os modelos do aplicativo presencas.
Cobre models: Presenca, PresencaDetalhada, ConfiguracaoPresenca, TotalAtividadeMes, ObservacaoPresenca.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date, timedelta

from presencas.models import (
    Presenca, PresencaDetalhada, ConfiguracaoPresenca, 
    TotalAtividadeMes, ObservacaoPresenca, AgendamentoRelatorio
)
from alunos.models import Aluno
from turmas.models import Turma
from atividades.models import Atividade
from django.contrib.auth import get_user_model

User = get_user_model()


class PresencaModelTest(TestCase):
    """Testes para o modelo Presenca."""
    
    def setUp(self):
        self.aluno = Aluno.objects.create(
            nome='João Silva',
            cpf='12345678901',
            data_nascimento=date(1990, 1, 1),
            email='joao@example.com'
        )
        
        self.turma = Turma.objects.create(
            nome='Turma A',
            ano=2024,
            semestre=1
        )
        
        self.atividade = Atividade.objects.create(
            nome='Atividade Teste',
            descricao='Descrição da atividade',
            tipo='academica'
        )
    
    def test_criar_presenca_basica(self):
        """Testa criação básica de presença."""
        presenca = Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            data=date.today(),
            presente=True
        )
        
        self.assertEqual(presenca.aluno, self.aluno)
        self.assertEqual(presenca.turma, self.turma)
        self.assertEqual(presenca.atividade, self.atividade)
        self.assertTrue(presenca.presente)
        self.assertEqual(presenca.registrado_por, "Sistema")
    
    def test_str_representation(self):
        """Testa representação string do modelo."""
        presenca = Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            data=date(2024, 1, 15),
            presente=True
        )
        
        expected = f"{self.aluno.nome} - 2024-01-15 - Presente"
        self.assertEqual(str(presenca), expected)
    
    def test_clean_data_futura(self):
        """Testa validação de data futura."""
        presenca = Presenca(
            aluno=self.aluno,
            turma=self.turma,
            data=date.today() + timedelta(days=1),
            presente=True
        )
        
        with self.assertRaises(ValidationError) as context:
            presenca.clean()
        
        self.assertIn('data', context.exception.message_dict)
        self.assertIn('futura', context.exception.message_dict['data'][0])
    
    def test_clean_justificativa_obrigatoria_ausencia(self):
        """Testa validação de justificativa obrigatória para ausência."""
        presenca = Presenca(
            aluno=self.aluno,
            turma=self.turma,
            data=date.today(),
            presente=False,
            justificativa=""
        )
        
        with self.assertRaises(ValidationError) as context:
            presenca.clean()
        
        self.assertIn('justificativa', context.exception.message_dict)
    
    def test_unique_together_constraint(self):
        """Testa constraint unique_together."""
        # Criar primeira presença
        Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            data=date.today(),
            presente=True
        )
        
        # Tentar criar presença duplicada
        with self.assertRaises(Exception):  # IntegrityError
            Presenca.objects.create(
                aluno=self.aluno,
                turma=self.turma,
                data=date.today(),
                presente=False
            )
    
    def test_ordering(self):
        """Testa ordenação padrão do modelo."""
        data1 = date(2024, 1, 10)
        data2 = date(2024, 1, 15)
        
        # Criar aluno adicional para testar ordenação secundária
        aluno2 = Aluno.objects.create(
            nome='Ana Silva',
            cpf='98765432100',
            data_nascimento=date(1992, 5, 15),
            email='ana@example.com'
        )
        
        presenca1 = Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            data=data1,
            presente=True
        )
        
        presenca2 = Presenca.objects.create(
            aluno=aluno2,
            turma=self.turma,
            data=data2,
            presente=True
        )
        
        presencas = list(Presenca.objects.all())
        
        # Deve estar ordenado por -data, depois por aluno__nome
        self.assertEqual(presencas[0], presenca2)  # Data mais recente
        self.assertEqual(presencas[1], presenca1)


class PresencaDetalhadaModelTest(TestCase):
    """Testes para o modelo PresencaDetalhada."""
    
    def setUp(self):
        self.aluno = Aluno.objects.create(
            nome='João Silva',
            cpf='12345678901',
            data_nascimento=date(1990, 1, 1),
            email='joao@example.com'
        )
        
        self.turma = Turma.objects.create(
            nome='Turma A',
            ano=2024,
            semestre=1,
            perc_carencia=75.0
        )
        
        self.atividade = Atividade.objects.create(
            nome='Atividade Teste',
            descricao='Descrição da atividade',
            tipo='academica'
        )
    
    def test_criar_presenca_detalhada(self):
        """Testa criação de presença detalhada."""
        presenca = PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 1),
            convocacoes=10,
            presencas=8,
            faltas=2,
            voluntario_extra=1,
            voluntario_simples=2
        )
        
        self.assertEqual(presenca.convocacoes, 10)
        self.assertEqual(presenca.presencas, 8)
        self.assertEqual(presenca.faltas, 2)
        self.assertEqual(presenca.percentual_presenca, Decimal('80.00'))
        self.assertEqual(presenca.total_voluntarios, 3)
    
    def test_calcular_percentual(self):
        """Testa cálculo do percentual de presença."""
        presenca = PresencaDetalhada(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 1),
            convocacoes=10,
            presencas=8
        )
        
        percentual = presenca.calcular_percentual()
        self.assertEqual(percentual, Decimal('80.00'))
        
        # Teste com convocações zero
        presenca.convocacoes = 0
        percentual_zero = presenca.calcular_percentual()
        self.assertEqual(percentual_zero, Decimal('0.00'))
    
    def test_calcular_voluntarios(self):
        """Testa cálculo do total de voluntários."""
        presenca = PresencaDetalhada(
            voluntario_extra=3,
            voluntario_simples=2
        )
        
        total = presenca.calcular_voluntarios()
        self.assertEqual(total, 5)
    
    def test_calcular_carencias_sem_configuracao(self):
        """Testa cálculo de carências sem configuração específica."""
        presenca = PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 1),
            convocacoes=10,
            presencas=6,  # 60% - abaixo do limite da turma (75%)
            faltas=4
        )
        
        carencias = presenca.calcular_carencias()
        # 75% de 10 = 7.5, então precisa de 8 presenças (arredondado)
        # Tem 6, faltam 2 carências
        self.assertGreater(carencias, 0)
    
    def test_clean_presencas_faltas_maior_convocacoes(self):
        """Testa validação: P + F <= C."""
        presenca = PresencaDetalhada(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 1),
            convocacoes=10,
            presencas=7,
            faltas=5  # 7 + 5 = 12 > 10
        )
        
        with self.assertRaises(ValidationError) as context:
            presenca.clean()
        
        self.assertIn('soma de presenças e faltas', str(context.exception))
    
    def test_clean_periodo_primeiro_dia_mes(self):
        """Testa validação: período deve ser primeiro dia do mês."""
        presenca = PresencaDetalhada(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 15),  # Não é primeiro dia
            convocacoes=10
        )
        
        with self.assertRaises(ValidationError) as context:
            presenca.clean()
        
        self.assertIn('periodo', context.exception.message_dict)
    
    def test_clean_valores_negativos(self):
        """Testa validação de valores negativos."""
        presenca = PresencaDetalhada(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 1),
            convocacoes=-1  # Valor negativo
        )
        
        with self.assertRaises(ValidationError) as context:
            presenca.clean()
        
        self.assertIn('convocacoes', context.exception.message_dict)
    
    def test_save_calcula_campos_automaticos(self):
        """Testa que save() calcula campos automaticamente."""
        presenca = PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 1),
            convocacoes=10,
            presencas=8,
            faltas=2,
            voluntario_extra=1,
            voluntario_simples=2
        )
        
        # Verificar que campos foram calculados
        self.assertEqual(presenca.percentual_presenca, Decimal('80.00'))
        self.assertEqual(presenca.total_voluntarios, 3)
        self.assertIsNotNone(presenca.carencias)
    
    def test_str_representation(self):
        """Testa representação string do modelo."""
        presenca = PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 1),
            convocacoes=10,
            presencas=8
        )
        
        expected = f"{self.aluno.nome} - 01/2024 - {self.atividade.nome}"
        self.assertEqual(str(presenca), expected)
    
    def test_unique_together_constraint(self):
        """Testa constraint unique_together."""
        # Criar primeira presença
        PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 1),
            convocacoes=10
        )
        
        # Tentar criar presença duplicada
        with self.assertRaises(Exception):  # IntegrityError
            PresencaDetalhada.objects.create(
                aluno=self.aluno,
                turma=self.turma,
                atividade=self.atividade,
                periodo=date(2024, 1, 1),
                convocacoes=8
            )


class ConfiguracaoPresencaModelTest(TestCase):
    """Testes para o modelo ConfiguracaoPresenca."""
    
    def setUp(self):
        self.turma = Turma.objects.create(
            nome='Turma A',
            ano=2024,
            semestre=1
        )
        
        self.atividade = Atividade.objects.create(
            nome='Atividade Teste',
            descricao='Descrição da atividade',
            tipo='academica'
        )
    
    def test_criar_configuracao(self):
        """Testa criação de configuração de presença."""
        config = ConfiguracaoPresenca.objects.create(
            turma=self.turma,
            atividade=self.atividade,
            limite_carencia_0_25=0,
            limite_carencia_26_50=1,
            limite_carencia_51_75=2,
            limite_carencia_76_100=3,
            obrigatoria=True,
            peso_calculo=Decimal('1.50')
        )
        
        self.assertEqual(config.turma, self.turma)
        self.assertEqual(config.atividade, self.atividade)
        self.assertTrue(config.obrigatoria)
        self.assertEqual(config.peso_calculo, Decimal('1.50'))
    
    def test_get_limite_carencia_por_percentual(self):
        """Testa método get_limite_carencia_por_percentual."""
        config = ConfiguracaoPresenca.objects.create(
            turma=self.turma,
            atividade=self.atividade,
            limite_carencia_0_25=0,
            limite_carencia_26_50=1,
            limite_carencia_51_75=2,
            limite_carencia_76_100=3
        )
        
        # Testar diferentes faixas
        self.assertEqual(config.get_limite_carencia_por_percentual(Decimal('20')), 0)
        self.assertEqual(config.get_limite_carencia_por_percentual(Decimal('40')), 1)
        self.assertEqual(config.get_limite_carencia_por_percentual(Decimal('60')), 2)
        self.assertEqual(config.get_limite_carencia_por_percentual(Decimal('80')), 3)
    
    def test_calcular_carencia_permitida(self):
        """Testa método calcular_carencia_permitida."""
        config = ConfiguracaoPresenca.objects.create(
            turma=self.turma,
            atividade=self.atividade,
            limite_carencia_76_100=3,
            peso_calculo=Decimal('1.50')
        )
        
        # Criar presença detalhada mockada
        class MockPresencaDetalhada:
            percentual_presenca = Decimal('80.00')
        
        presenca_mock = MockPresencaDetalhada()
        carencia_permitida = config.calcular_carencia_permitida(presenca_mock)
        
        # 3 * 1.50 = 4.5, int() = 4
        self.assertEqual(carencia_permitida, 4)
    
    def test_clean_peso_positivo(self):
        """Testa validação de peso positivo."""
        config = ConfiguracaoPresenca(
            turma=self.turma,
            atividade=self.atividade,
            peso_calculo=Decimal('0.00')  # Peso zero
        )
        
        with self.assertRaises(ValidationError) as context:
            config.clean()
        
        self.assertIn('peso_calculo', context.exception.message_dict)
    
    def test_clean_limites_nao_negativos(self):
        """Testa validação de limites não negativos."""
        config = ConfiguracaoPresenca(
            turma=self.turma,
            atividade=self.atividade,
            limite_carencia_0_25=-1  # Valor negativo
        )
        
        with self.assertRaises(ValidationError) as context:
            config.clean()
        
        self.assertIn('limite_carencia_0_25', context.exception.message_dict)
    
    def test_str_representation(self):
        """Testa representação string do modelo."""
        config = ConfiguracaoPresenca.objects.create(
            turma=self.turma,
            atividade=self.atividade
        )
        
        expected = f"{self.turma} - {self.atividade}"
        self.assertEqual(str(config), expected)
    
    def test_unique_together_constraint(self):
        """Testa constraint unique_together."""
        # Criar primeira configuração
        ConfiguracaoPresenca.objects.create(
            turma=self.turma,
            atividade=self.atividade
        )
        
        # Tentar criar configuração duplicada
        with self.assertRaises(Exception):  # IntegrityError
            ConfiguracaoPresenca.objects.create(
                turma=self.turma,
                atividade=self.atividade
            )


class TotalAtividadeMesModelTest(TestCase):
    """Testes para o modelo TotalAtividadeMes."""
    
    def setUp(self):
        self.turma = Turma.objects.create(
            nome='Turma A',
            ano=2024,
            semestre=1
        )
        
        self.atividade = Atividade.objects.create(
            nome='Atividade Teste',
            descricao='Descrição da atividade',
            tipo='academica'
        )
    
    def test_criar_total_atividade_mes(self):
        """Testa criação de total de atividade no mês."""
        total = TotalAtividadeMes.objects.create(
            atividade=self.atividade,
            turma=self.turma,
            ano=2024,
            mes=1,
            qtd_ativ_mes=15
        )
        
        self.assertEqual(total.atividade, self.atividade)
        self.assertEqual(total.turma, self.turma)
        self.assertEqual(total.ano, 2024)
        self.assertEqual(total.mes, 1)
        self.assertEqual(total.qtd_ativ_mes, 15)
    
    def test_str_representation(self):
        """Testa representação string do modelo."""
        total = TotalAtividadeMes.objects.create(
            atividade=self.atividade,
            turma=self.turma,
            ano=2024,
            mes=3,
            qtd_ativ_mes=12
        )
        
        expected = f"{self.atividade} - {self.turma} - 3/2024: 12"
        self.assertEqual(str(total), expected)
    
    def test_unique_together_constraint(self):
        """Testa constraint unique_together."""
        # Criar primeiro total
        TotalAtividadeMes.objects.create(
            atividade=self.atividade,
            turma=self.turma,
            ano=2024,
            mes=1,
            qtd_ativ_mes=10
        )
        
        # Tentar criar total duplicado
        with self.assertRaises(Exception):  # IntegrityError
            TotalAtividadeMes.objects.create(
                atividade=self.atividade,
                turma=self.turma,
                ano=2024,
                mes=1,
                qtd_ativ_mes=15
            )


class ObservacaoPresencaModelTest(TestCase):
    """Testes para o modelo ObservacaoPresenca."""
    
    def setUp(self):
        self.aluno = Aluno.objects.create(
            nome='João Silva',
            cpf='12345678901',
            data_nascimento=date(1990, 1, 1),
            email='joao@example.com'
        )
        
        self.turma = Turma.objects.create(
            nome='Turma A',
            ano=2024,
            semestre=1
        )
        
        self.atividade = Atividade.objects.create(
            nome='Atividade Teste',
            descricao='Descrição da atividade',
            tipo='academica'
        )
    
    def test_criar_observacao_com_aluno(self):
        """Testa criação de observação com aluno."""
        obs = ObservacaoPresenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            data=date.today(),
            texto="Aluno chegou atrasado"
        )
        
        self.assertEqual(obs.aluno, self.aluno)
        self.assertEqual(obs.turma, self.turma)
        self.assertEqual(obs.atividade, self.atividade)
        self.assertEqual(obs.texto, "Aluno chegou atrasado")
    
    def test_criar_observacao_sem_aluno(self):
        """Testa criação de observação geral da turma."""
        obs = ObservacaoPresenca.objects.create(
            turma=self.turma,
            data=date.today(),
            texto="Atividade cancelada devido à chuva"
        )
        
        self.assertIsNone(obs.aluno)
        self.assertEqual(obs.turma, self.turma)
        self.assertEqual(obs.texto, "Atividade cancelada devido à chuva")
    
    def test_str_representation_com_atividade(self):
        """Testa representação string com atividade."""
        obs = ObservacaoPresenca.objects.create(
            turma=self.turma,
            atividade=self.atividade,
            data=date(2024, 1, 15),
            texto="Texto longo que deve ser truncado para teste"
        )
        
        expected = "2024-01-15 - Atividade Teste - Texto longo que deve ser trun"
        self.assertEqual(str(obs), expected)
    
    def test_str_representation_sem_atividade(self):
        """Testa representação string sem atividade."""
        obs = ObservacaoPresenca.objects.create(
            turma=self.turma,
            data=date(2024, 1, 15),
            texto="Observação geral"
        )
        
        expected = "2024-01-15 - Sem atividade - Observação geral"
        self.assertEqual(str(obs), expected)


class AgendamentoRelatorioModelTest(TestCase):
    """Testes para o modelo AgendamentoRelatorio."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        self.turma = Turma.objects.create(
            nome='Turma A',
            ano=2024,
            semestre=1
        )
    
    def test_criar_agendamento_basico(self):
        """Testa criação básica de agendamento."""
        agendamento = AgendamentoRelatorio.objects.create(
            nome="Relatório Mensal",
            usuario=self.user,
            formato='excel_avancado',
            template='consolidado_geral',
            periodo='mensal',
            frequencia='mensal',
            dia_mes=1,
            emails_destino='admin@example.com'
        )
        
        self.assertEqual(agendamento.nome, "Relatório Mensal")
        self.assertEqual(agendamento.usuario, self.user)
        self.assertEqual(agendamento.formato, 'excel_avancado')
        self.assertTrue(agendamento.ativo)
    
    def test_clean_periodo_personalizado_sem_datas(self):
        """Testa validação de período personalizado sem datas."""
        agendamento = AgendamentoRelatorio(
            nome="Teste",
            usuario=self.user,
            periodo='personalizado',
            emails_destino='test@example.com'
        )
        
        with self.assertRaises(ValidationError) as context:
            agendamento.clean()
        
        self.assertIn('Data início e fim são obrigatórias', str(context.exception))
    
    def test_clean_data_inicio_posterior_fim(self):
        """Testa validação de data início posterior à fim."""
        agendamento = AgendamentoRelatorio(
            nome="Teste",
            usuario=self.user,
            periodo='personalizado',
            data_inicio=date(2024, 2, 1),
            data_fim=date(2024, 1, 1),  # Anterior à data início
            emails_destino='test@example.com'
        )
        
        with self.assertRaises(ValidationError) as context:
            agendamento.clean()
        
        self.assertIn('Data início deve ser anterior', str(context.exception))
    
    def test_clean_frequencia_semanal_sem_dia_semana(self):
        """Testa validação de frequência semanal sem dia da semana."""
        agendamento = AgendamentoRelatorio(
            nome="Teste",
            usuario=self.user,
            frequencia='semanal',
            emails_destino='test@example.com'
        )
        
        with self.assertRaises(ValidationError) as context:
            agendamento.clean()
        
        self.assertIn('Dia da semana é obrigatório', str(context.exception))
    
    def test_clean_email_invalido(self):
        """Testa validação de email inválido."""
        agendamento = AgendamentoRelatorio(
            nome="Teste",
            usuario=self.user,
            emails_destino='email_invalido'
        )
        
        with self.assertRaises(ValidationError) as context:
            agendamento.clean()
        
        self.assertIn('Email inválido', str(context.exception))
    
    def test_calcular_proxima_execucao_diaria(self):
        """Testa cálculo de próxima execução diária."""
        agendamento = AgendamentoRelatorio(
            nome="Teste",
            usuario=self.user,
            frequencia='diario',
            hora_execucao='08:00',
            emails_destino='test@example.com'
        )
        
        agendamento.calcular_proxima_execucao()
        
        self.assertIsNotNone(agendamento.proxima_execucao)
        self.assertEqual(agendamento.proxima_execucao.hour, 8)
        self.assertEqual(agendamento.proxima_execucao.minute, 0)
    
    def test_str_representation(self):
        """Testa representação string do modelo."""
        agendamento = AgendamentoRelatorio.objects.create(
            nome="Relatório Mensal",
            usuario=self.user,
            frequencia='mensal',
            emails_destino='test@example.com'
        )
        
        expected = "Relatório Mensal - Mensal"
        self.assertEqual(str(agendamento), expected)
