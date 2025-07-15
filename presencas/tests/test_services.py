"""
Testes para os serviços do aplicativo presencas.
Cobre services.py e CalculadoraEstatisticas.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date, timedelta
from unittest.mock import patch

from presencas.models import (
    Presenca, PresencaDetalhada, ConfiguracaoPresenca, 
    TotalAtividadeMes
)
from presencas.services import (
    listar_presencas, buscar_presencas_por_filtros, registrar_presenca,
    registrar_presencas_multiplas, atualizar_presenca, excluir_presenca,
    obter_presencas_por_aluno, obter_presencas_por_turma,
    calcular_frequencia_aluno, criar_observacao_presenca,
    registrar_total_atividade_mes
)
from presencas.services.calculadora_estatisticas import CalculadoraEstatisticas
from alunos.models import Aluno
from turmas.models import Turma
from atividades.models import Atividade


class PresencaServicesTest(TestCase):
    """Testes para os serviços básicos de presença."""
    
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
    
    def test_listar_presencas_todas(self):
        """Testa listagem de todas as presenças."""
        # Criar algumas presenças
        Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            data=date.today(),
            presente=True
        )
        
        presencas = listar_presencas('todas')
        self.assertEqual(presencas.count(), 1)
        self.assertEqual(presencas.first().aluno, self.aluno)
    
    def test_buscar_presencas_por_filtros(self):
        """Testa busca de presenças com filtros."""
        # Criar presenças
        presenca1 = Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            data=date(2024, 1, 15),
            presente=True
        )
        
        # Criar outro aluno para teste
        aluno2 = Aluno.objects.create(
            nome='Maria Santos',
            cpf='98765432100',
            data_nascimento=date(1992, 5, 15),
            email='maria@example.com'
        )
        
        Presenca.objects.create(
            aluno=aluno2,
            turma=self.turma,
            data=date(2024, 1, 20),
            presente=False
        )
        
        # Testar filtro por CPF
        filtros = {'aluno_cpf': '12345678901'}
        presencas = buscar_presencas_por_filtros(filtros)
        self.assertEqual(presencas.count(), 1)
        self.assertEqual(presencas.first().aluno.cpf, '12345678901')
        
        # Testar filtro por turma
        filtros = {'turma_id': self.turma.id}
        presencas = buscar_presencas_por_filtros(filtros)
        self.assertEqual(presencas.count(), 2)
        
        # Testar filtro por data
        filtros = {
            'data_inicio': date(2024, 1, 1),
            'data_fim': date(2024, 1, 18)
        }
        presencas = buscar_presencas_por_filtros(filtros)
        self.assertEqual(presencas.count(), 1)
        self.assertEqual(presencas.first(), presenca1)
        
        # Testar filtro por presença
        filtros = {'presente': True}
        presencas = buscar_presencas_por_filtros(filtros)
        self.assertEqual(presencas.count(), 1)
        self.assertTrue(presencas.first().presente)
    
    def test_registrar_presenca_sucesso(self):
        """Testa registro de presença com sucesso."""
        dados = {
            'aluno_cpf': self.aluno.cpf,
            'turma_id': self.turma.id,
            'atividade_id': self.atividade.id,
            'data': date.today(),
            'presente': True,
            'registrado_por': 'TestUser'
        }
        
        presenca = registrar_presenca(dados)
        
        self.assertIsNotNone(presenca)
        self.assertEqual(presenca.aluno, self.aluno)
        self.assertEqual(presenca.turma, self.turma)
        self.assertEqual(presenca.atividade, self.atividade)
        self.assertTrue(presenca.presente)
        self.assertEqual(presenca.registrado_por, 'TestUser')
    
    def test_registrar_presenca_data_futura(self):
        """Testa erro ao registrar presença com data futura."""
        dados = {
            'aluno_cpf': self.aluno.cpf,
            'turma_id': self.turma.id,
            'data': date.today() + timedelta(days=1),
            'presente': True
        }
        
        with self.assertRaises(ValidationError) as context:
            registrar_presenca(dados)
        
        self.assertIn('futura', str(context.exception))
    
    def test_registrar_presenca_duplicada(self):
        """Testa erro ao registrar presença duplicada."""
        # Criar primeira presença
        Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            data=date.today(),
            presente=True
        )
        
        # Tentar registrar presença duplicada
        dados = {
            'aluno_cpf': self.aluno.cpf,
            'turma_id': self.turma.id,
            'data': date.today(),
            'presente': False
        }
        
        with self.assertRaises(ValidationError) as context:
            registrar_presenca(dados)
        
        self.assertIn('Já existe registro', str(context.exception))
    
    def test_registrar_presenca_aluno_inexistente(self):
        """Testa erro com aluno inexistente."""
        dados = {
            'aluno_cpf': '99999999999',  # CPF inexistente
            'turma_id': self.turma.id,
            'data': date.today(),
            'presente': True
        }
        
        with self.assertRaises(ValidationError) as context:
            registrar_presenca(dados)
        
        self.assertIn('não encontrado', str(context.exception))
    
    def test_registrar_presencas_multiplas(self):
        """Testa registro de múltiplas presenças."""
        # Criar outro aluno
        aluno2 = Aluno.objects.create(
            nome='Maria Santos',
            cpf='98765432100',
            data_nascimento=date(1992, 5, 15),
            email='maria@example.com'
        )
        
        lista_presencas = [
            {
                'aluno_cpf': self.aluno.cpf,
                'turma_id': self.turma.id,
                'data': date.today(),
                'presente': True
            },
            {
                'aluno_cpf': aluno2.cpf,
                'turma_id': self.turma.id,
                'data': date.today(),
                'presente': False,
                'justificativa': 'Motivo pessoal'
            },
            {
                'aluno_cpf': '99999999999',  # CPF inexistente - erro
                'turma_id': self.turma.id,
                'data': date.today(),
                'presente': True
            }
        ]
        
        resultado = registrar_presencas_multiplas(lista_presencas)
        
        self.assertEqual(resultado['total_criadas'], 2)
        self.assertEqual(resultado['total_erros'], 1)
        self.assertEqual(len(resultado['criadas']), 2)
        self.assertEqual(len(resultado['erros']), 1)
    
    def test_atualizar_presenca(self):
        """Testa atualização de presença."""
        presenca = Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            data=date.today(),
            presente=True
        )
        
        dados_atualizacao = {
            'presente': False,
            'justificativa': 'Motivo médico',
            'registrado_por': 'UpdateUser'
        }
        
        presenca_atualizada = atualizar_presenca(presenca.id, dados_atualizacao)
        
        self.assertFalse(presenca_atualizada.presente)
        self.assertEqual(presenca_atualizada.justificativa, 'Motivo médico')
        self.assertEqual(presenca_atualizada.registrado_por, 'UpdateUser')
    
    def test_atualizar_presenca_inexistente(self):
        """Testa erro ao atualizar presença inexistente."""
        with self.assertRaises(ValidationError) as context:
            atualizar_presenca(99999, {'presente': False})
        
        self.assertIn('não encontrada', str(context.exception))
    
    def test_excluir_presenca(self):
        """Testa exclusão de presença."""
        presenca = Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            data=date.today(),
            presente=True
        )
        
        resultado = excluir_presenca(presenca.id)
        
        self.assertTrue(resultado)
        self.assertFalse(Presenca.objects.filter(id=presenca.id).exists())
    
    def test_excluir_presenca_inexistente(self):
        """Testa erro ao excluir presença inexistente."""
        with self.assertRaises(ValidationError) as context:
            excluir_presenca(99999)
        
        self.assertIn('não encontrada', str(context.exception))
    
    def test_obter_presencas_por_aluno(self):
        """Testa obtenção de presenças por aluno."""
        # Criar presenças
        Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            data=date(2024, 1, 15),
            presente=True
        )
        
        presenca2 = Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            data=date(2024, 1, 20),
            presente=False
        )
        
        # Obter todas as presenças do aluno
        presencas = obter_presencas_por_aluno(self.aluno.cpf)
        self.assertEqual(presencas.count(), 2)
        
        # Obter presenças com filtro de data
        presencas_filtradas = obter_presencas_por_aluno(
            self.aluno.cpf,
            data_inicio=date(2024, 1, 16)
        )
        self.assertEqual(presencas_filtradas.count(), 1)
        self.assertEqual(presencas_filtradas.first(), presenca2)
    
    def test_obter_presencas_por_turma(self):
        """Testa obtenção de presenças por turma."""
        # Criar outro aluno
        aluno2 = Aluno.objects.create(
            nome='Maria Santos',
            cpf='98765432100',
            data_nascimento=date(1992, 5, 15),
            email='maria@example.com'
        )
        
        # Criar presenças
        Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            data=date.today(),
            presente=True
        )
        
        Presenca.objects.create(
            aluno=aluno2,
            turma=self.turma,
            data=date.today(),
            presente=False
        )
        
        presencas = obter_presencas_por_turma(self.turma.id)
        self.assertEqual(presencas.count(), 2)
    
    def test_calcular_frequencia_aluno(self):
        """Testa cálculo de frequência do aluno."""
        # Criar presenças
        for i in range(8):
            Presenca.objects.create(
                aluno=self.aluno,
                turma=self.turma,
                data=date(2024, 1, i+1),
                presente=True
            )
        
        for i in range(2):
            Presenca.objects.create(
                aluno=self.aluno,
                turma=self.turma,
                data=date(2024, 1, i+9),
                presente=False
            )
        
        frequencia = calcular_frequencia_aluno(self.aluno.cpf, self.turma.id)
        
        self.assertEqual(frequencia['total_registros'], 10)
        self.assertEqual(frequencia['total_presencas'], 8)
        self.assertEqual(frequencia['total_faltas'], 2)
        self.assertEqual(frequencia['percentual_presenca'], 80.0)
    
    def test_criar_observacao_presenca(self):
        """Testa criação de observação de presença."""
        dados = {
            'aluno_cpf': self.aluno.cpf,
            'turma_id': self.turma.id,
            'data': date.today(),
            'texto': 'Aluno chegou atrasado',
            'registrado_por': 'TestUser'
        }
        
        observacao = criar_observacao_presenca(dados)
        
        self.assertEqual(observacao.aluno, self.aluno)
        self.assertEqual(observacao.turma, self.turma)
        self.assertEqual(observacao.texto, 'Aluno chegou atrasado')
        self.assertEqual(observacao.registrado_por, 'TestUser')
    
    def test_criar_observacao_sem_aluno(self):
        """Testa criação de observação geral da turma."""
        dados = {
            'turma_id': self.turma.id,
            'data': date.today(),
            'texto': 'Atividade cancelada',
            'registrado_por': 'TestUser'
        }
        
        observacao = criar_observacao_presenca(dados)
        
        self.assertIsNone(observacao.aluno)
        self.assertEqual(observacao.turma, self.turma)
        self.assertEqual(observacao.texto, 'Atividade cancelada')
    
    def test_registrar_total_atividade_mes(self):
        """Testa registro de total de atividade no mês."""
        total = registrar_total_atividade_mes(
            self.turma.id,
            self.atividade.id,
            2024,
            1,
            15
        )
        
        self.assertEqual(total.turma, self.turma)
        self.assertEqual(total.atividade, self.atividade)
        self.assertEqual(total.ano, 2024)
        self.assertEqual(total.mes, 1)
        self.assertEqual(total.qtd_ativ_mes, 15)
    
    def test_registrar_total_atividade_mes_atualizacao(self):
        """Testa atualização de total existente."""
        # Criar total inicial
        total_inicial = TotalAtividadeMes.objects.create(
            atividade=self.atividade,
            turma=self.turma,
            ano=2024,
            mes=1,
            qtd_ativ_mes=10
        )
        
        # Atualizar
        total_atualizado = registrar_total_atividade_mes(
            self.turma.id,
            self.atividade.id,
            2024,
            1,
            20
        )
        
        # Deve ter atualizado o mesmo registro
        self.assertEqual(total_atualizado.id, total_inicial.id)
        self.assertEqual(total_atualizado.qtd_ativ_mes, 20)


class CalculadoraEstatisticasExtendedTest(TestCase):
    """Testes adicionais para CalculadoraEstatisticas."""
    
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
    
    def test_performance_com_dataset_grande(self):
        """Testa performance com dataset grande."""
        # Criar múltiplos alunos e presenças
        alunos = []
        for i in range(50):
            aluno = Aluno.objects.create(
                nome=f'Aluno {i}',
                cpf=f'1234567890{i:02d}',
                data_nascimento=date(1990, 1, 1),
                email=f'aluno{i}@example.com'
            )
            alunos.append(aluno)
            
            # Criar presenças para cada aluno
            for mes in range(1, 7):
                PresencaDetalhada.objects.create(
                    aluno=aluno,
                    turma=self.turma,
                    atividade=self.atividade,
                    periodo=date(2024, mes, 1),
                    convocacoes=10,
                    presencas=8,
                    faltas=2,
                    registrado_por='test'
                )
        
        # Testar que a query é otimizada
        with self.assertNumQueries(1):  # Apenas uma query principal
            tabela = CalculadoraEstatisticas.gerar_tabela_consolidada(
                turma_id=self.turma.id
            )
            
            # Verificar resultados
            self.assertEqual(len(tabela['linhas']), 50)
            self.assertEqual(tabela['estatisticas_gerais']['total_alunos'], 50)
    
    def test_edge_cases_percentuais(self):
        """Testa casos extremos de percentuais."""
        # Caso 1: 100% de presença
        presenca_100 = PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 1),
            convocacoes=10,
            presencas=10,
            faltas=0
        )
        
        consolidado = CalculadoraEstatisticas.calcular_consolidado_aluno(
            self.aluno.id
        )
        self.assertEqual(consolidado['percentuais']['presenca'], 100.0)
        
        # Caso 2: 0% de presença
        presenca_100.presencas = 0
        presenca_100.faltas = 10
        presenca_100.save()
        
        consolidado = CalculadoraEstatisticas.calcular_consolidado_aluno(
            self.aluno.id
        )
        self.assertEqual(consolidado['percentuais']['presenca'], 0.0)
        
        # Caso 3: Zero convocações
        presenca_100.convocacoes = 0
        presenca_100.presencas = 0
        presenca_100.faltas = 0
        presenca_100.save()
        
        consolidado = CalculadoraEstatisticas.calcular_consolidado_aluno(
            self.aluno.id
        )
        self.assertEqual(consolidado['percentuais']['presenca'], 0.0)
    
    def test_calcular_carencias_configuracao_complexa(self):
        """Testa cálculo de carências com configuração complexa."""
        # Criar configuração com pesos diferentes
        config = ConfiguracaoPresenca.objects.create(
            turma=self.turma,
            atividade=self.atividade,
            limite_carencia_0_25=0,
            limite_carencia_26_50=1,
            limite_carencia_51_75=2,
            limite_carencia_76_100=3,
            peso_calculo=Decimal('2.0')  # Peso dobrado
        )
        
        presenca = PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 1),
            convocacoes=10,
            presencas=8,  # 80% - faixa 76-100%
            faltas=2
        )
        
        resultado = CalculadoraEstatisticas.calcular_carencias(
            presenca.id,
            forcar_recalculo=True
        )
        
        # Limite base: 3, com peso 2.0 = 6 carências permitidas
        # Com 8 presenças em 10 convocações, não deve ter carências
        self.assertEqual(resultado['metodo_calculo'], 'configuracao_especifica')
        self.assertEqual(resultado['configuracao_usada'], config.id)
    
    def test_distribuicao_carencias(self):
        """Testa cálculo de distribuição de carências."""
        # Criar alunos com diferentes níveis de carência
        alunos_dados = [
            ('Aluno Sem Carencia', 0),
            ('Aluno 1 Carencia', 1),
            ('Aluno 2 Carencias', 2),
            ('Aluno 4 Carencias', 4),
            ('Aluno 6 Carencias', 6),
            ('Aluno 10 Carencias', 10)
        ]
        
        for nome, carencias in alunos_dados:
            aluno = Aluno.objects.create(
                nome=nome,
                cpf=f'1111111111{carencias}',
                data_nascimento=date(1990, 1, 1),
                email=f'aluno{carencias}@example.com'
            )
            
            PresencaDetalhada.objects.create(
                aluno=aluno,
                turma=self.turma,
                atividade=self.atividade,
                periodo=date(2024, 1, 1),
                convocacoes=10,
                presencas=10 - carencias,
                faltas=carencias,
                carencias=carencias,  # Definir diretamente para teste
                registrado_por='test'
            )
        
        estatisticas = CalculadoraEstatisticas.calcular_estatisticas_turma(
            self.turma.id
        )
        
        distribuicao = estatisticas['distribuicao_carencias']
        
        # Verificar distribuição esperada
        self.assertEqual(distribuicao['sem_carencia'], 1)  # 0 carências
        self.assertEqual(distribuicao['1_a_2_carencias'], 2)  # 1 e 2 carências
        self.assertEqual(distribuicao['3_a_5_carencias'], 1)  # 4 carências
        self.assertEqual(distribuicao['mais_de_5_carencias'], 2)  # 6 e 10 carências
    
    def test_filtros_combinados(self):
        """Testa aplicação de múltiplos filtros."""
        # Criar outro aluno e atividade
        aluno2 = Aluno.objects.create(
            nome='Maria Santos',
            cpf='98765432100',
            data_nascimento=date(1992, 5, 15),
            email='maria@example.com'
        )
        
        atividade2 = Atividade.objects.create(
            nome='Atividade 2',
            descricao='Segunda atividade',
            tipo='academica'
        )
        
        # Criar presenças em diferentes períodos e atividades
        dados_presencas = [
            (self.aluno, self.atividade, date(2024, 1, 1)),
            (self.aluno, self.atividade, date(2024, 2, 1)),
            (self.aluno, atividade2, date(2024, 1, 1)),
            (aluno2, self.atividade, date(2024, 1, 1)),
        ]
        
        for aluno, atividade, periodo in dados_presencas:
            PresencaDetalhada.objects.create(
                aluno=aluno,
                turma=self.turma,
                atividade=atividade,
                periodo=periodo,
                convocacoes=10,
                presencas=8,
                faltas=2,
                registrado_por='test'
            )
        
        # Testar filtro por aluno e atividade
        consolidado = CalculadoraEstatisticas.calcular_consolidado_aluno(
            self.aluno.id,
            atividade_id=self.atividade.id
        )
        # Deve incluir apenas 2 registros (jan e fev da atividade 1)
        self.assertEqual(consolidado['totais']['registros'], 2)
        
        # Testar filtro por período
        tabela = CalculadoraEstatisticas.gerar_tabela_consolidada(
            turma_id=self.turma.id,
            periodo_inicio=date(2024, 1, 1),
            periodo_fim=date(2024, 1, 31)
        )
        # Deve incluir apenas registros de janeiro
        total_registros = sum(
            len(linha['atividades']) for linha in tabela['linhas']
        )
        self.assertEqual(total_registros, 3)  # 3 presenças em janeiro
    
    def test_error_handling_dados_corrompidos(self):
        """Testa tratamento de erros com dados corrompidos."""
        # Testar com dados inconsistentes
        PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 1),
            convocacoes=0,  # Zero convocações
            presencas=5,    # Mas com presenças - inconsistente
            faltas=0
        )
        
        # Deve lidar graciosamente com dados inconsistentes
        consolidado = CalculadoraEstatisticas.calcular_consolidado_aluno(
            self.aluno.id
        )
        
        # Percentual deve ser 0 quando convocações = 0
        self.assertEqual(consolidado['percentuais']['presenca'], 0.0)
    
    @patch('presencas.services.calculadora_estatisticas.logger')
    def test_logging_operacoes(self, mock_logger):
        """Testa logging das operações."""
        PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 1),
            convocacoes=10,
            presencas=8,
            faltas=2
        )
        
        # Executar operação que gera log
        CalculadoraEstatisticas.calcular_consolidado_aluno(self.aluno.id)
        
        # Verificar se log foi chamado
        mock_logger.info.assert_called()
        
        # Verificar conteúdo do log
        log_calls = [call[0][0] for call in mock_logger.info.call_args_list]
        consolidado_log = any('Consolidado calculado' in call for call in log_calls)
        self.assertTrue(consolidado_log)
