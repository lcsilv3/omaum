"""
Testes para o serviço CalculadoraEstatisticas.
"""

from decimal import Decimal
from datetime import date
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from ..models import PresencaDetalhada, ConfiguracaoPresenca
from ..services.calculadora_estatisticas import CalculadoraEstatisticas
from alunos.models import Aluno
from turmas.models import Turma
from atividades.models import Atividade

User = get_user_model()


class TestCalculadoraEstatisticas(TestCase):
    """Testes para a classe CalculadoraEstatisticas."""
    
    def setUp(self):
        """Configura dados para os testes."""
        # Criar usuário
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Criar aluno
        self.aluno = Aluno.objects.create(
            nome='João Silva',
            cpf='12345678901',
            data_nascimento=date(1990, 1, 1),
            email='joao@example.com'
        )
        
        # Criar turma
        self.turma = Turma.objects.create(
            nome='Turma A',
            ano=2024,
            semestre=1,
            perc_carencia=75.0
        )
        
        # Criar atividade
        self.atividade = Atividade.objects.create(
            nome='Atividade Teste',
            descricao='Descrição da atividade',
            tipo='academica'
        )
        
        # Criar configuração de presença
        self.configuracao = ConfiguracaoPresenca.objects.create(
            turma=self.turma,
            atividade=self.atividade,
            limite_carencia_0_25=0,
            limite_carencia_26_50=1,
            limite_carencia_51_75=2,
            limite_carencia_76_100=3,
            obrigatoria=True,
            peso_calculo=Decimal('1.00')
        )
        
        # Criar presença detalhada
        self.presenca_detalhada = PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 1),
            convocacoes=10,
            presencas=8,
            faltas=2,
            voluntario_extra=1,
            voluntario_simples=2,
            registrado_por='test'
        )
    
    def test_calcular_consolidado_aluno_com_dados(self):
        """Testa cálculo de consolidado para aluno com dados."""
        consolidado = CalculadoraEstatisticas.calcular_consolidado_aluno(
            self.aluno.id
        )
        
        # Verificar estrutura básica
        self.assertIn('aluno', consolidado)
        self.assertIn('totais', consolidado)
        self.assertIn('percentuais', consolidado)
        self.assertIn('status', consolidado)
        
        # Verificar dados do aluno
        self.assertEqual(consolidado['aluno']['id'], self.aluno.id)
        self.assertEqual(consolidado['aluno']['nome'], self.aluno.nome)
        
        # Verificar totais
        self.assertEqual(consolidado['totais']['convocacoes'], 10)
        self.assertEqual(consolidado['totais']['presencas'], 8)
        self.assertEqual(consolidado['totais']['faltas'], 2)
        self.assertEqual(consolidado['totais']['voluntario_extra'], 1)
        self.assertEqual(consolidado['totais']['voluntario_simples'], 2)
        
        # Verificar percentual
        self.assertEqual(consolidado['percentuais']['presenca'], 80.0)
    
    def test_calcular_consolidado_aluno_sem_dados(self):
        """Testa cálculo de consolidado para aluno sem dados."""
        aluno_sem_dados = Aluno.objects.create(
            nome='Maria Santos',
            cpf='98765432100',
            data_nascimento=date(1995, 5, 15),
            email='maria@example.com'
        )
        
        consolidado = CalculadoraEstatisticas.calcular_consolidado_aluno(
            aluno_sem_dados.id
        )
        
        # Verificar que retorna estrutura vazia
        self.assertEqual(consolidado['totais']['convocacoes'], 0)
        self.assertEqual(consolidado['totais']['presencas'], 0)
        self.assertEqual(consolidado['status'], 'sem_dados')
    
    def test_gerar_tabela_consolidada(self):
        """Testa geração de tabela consolidada."""
        tabela = CalculadoraEstatisticas.gerar_tabela_consolidada(
            turma_id=self.turma.id
        )
        
        # Verificar estrutura
        self.assertIn('linhas', tabela)
        self.assertIn('estatisticas_gerais', tabela)
        self.assertIn('total_alunos', tabela)
        
        # Verificar dados
        self.assertEqual(tabela['total_alunos'], 1)
        self.assertEqual(len(tabela['linhas']), 1)
        
        # Verificar linha do aluno
        linha_aluno = tabela['linhas'][0]
        self.assertEqual(linha_aluno['aluno']['id'], self.aluno.id)
        self.assertEqual(linha_aluno['percentual_geral'], 80.0)
        self.assertEqual(linha_aluno['totais']['convocacoes'], 10)
    
    def test_calcular_estatisticas_turma(self):
        """Testa cálculo de estatísticas da turma."""
        estatisticas = CalculadoraEstatisticas.calcular_estatisticas_turma(
            self.turma.id
        )
        
        # Verificar estrutura
        self.assertIn('turma', estatisticas)
        self.assertIn('totais', estatisticas)
        self.assertIn('percentuais', estatisticas)
        self.assertIn('por_atividade', estatisticas)
        self.assertIn('por_aluno', estatisticas)
        
        # Verificar dados da turma
        self.assertEqual(estatisticas['turma']['id'], self.turma.id)
        self.assertEqual(estatisticas['turma']['nome'], self.turma.nome)
        
        # Verificar totais
        self.assertEqual(estatisticas['totais']['convocacoes'], 10)
        self.assertEqual(estatisticas['totais']['presencas'], 8)
        self.assertEqual(estatisticas['totais']['alunos'], 1)
        self.assertEqual(estatisticas['totais']['atividades'], 1)
        
        # Verificar percentual médio
        self.assertEqual(estatisticas['percentuais']['presenca_media'], 80.0)
    
    def test_calcular_carencias_com_configuracao(self):
        """Testa cálculo de carências usando configuração específica."""
        resultado = CalculadoraEstatisticas.calcular_carencias(
            self.presenca_detalhada.id,
            forcar_recalculo=True
        )
        
        # Verificar estrutura
        self.assertIn('presenca_id', resultado)
        self.assertIn('carencias_novas', resultado)
        self.assertIn('metodo_calculo', resultado)
        self.assertIn('configuracao_usada', resultado)
        
        # Verificar que usou configuração específica
        self.assertEqual(resultado['metodo_calculo'], 'configuracao_especifica')
        self.assertEqual(resultado['configuracao_usada'], self.configuracao.id)
        self.assertTrue(resultado['recalculado'])
    
    def test_calcular_carencias_sem_configuracao(self):
        """Testa cálculo de carências sem configuração específica."""
        # Remover configuração
        self.configuracao.delete()
        
        resultado = CalculadoraEstatisticas.calcular_carencias(
            self.presenca_detalhada.id,
            forcar_recalculo=True
        )
        
        # Verificar que usou percentual da turma
        self.assertEqual(resultado['metodo_calculo'], 'percentual_turma')
        self.assertIsNone(resultado['configuracao_usada'])
        self.assertTrue(resultado['recalculado'])
    
    def test_recalcular_todas_carencias(self):
        """Testa recálculo de todas as carências."""
        # Criar mais presenças
        for i in range(3):
            PresencaDetalhada.objects.create(
                aluno=self.aluno,
                turma=self.turma,
                atividade=self.atividade,
                periodo=date(2024, i+2, 1),
                convocacoes=10,
                presencas=7,
                faltas=3,
                registrado_por='test'
            )
        
        resultado = CalculadoraEstatisticas.recalcular_todas_carencias(
            turma_id=self.turma.id
        )
        
        # Verificar resultado
        self.assertEqual(resultado['total_presencas'], 4)  # 1 original + 3 novas
        self.assertEqual(resultado['presencas_atualizadas'], 4)
        self.assertEqual(resultado['total_erros'], 0)
        self.assertIn('filtros_aplicados', resultado)
    
    def test_ordenacao_tabela_por_nome(self):
        """Testa ordenação da tabela por nome."""
        # Criar outro aluno
        aluno2 = Aluno.objects.create(
            nome='Ana Costa',
            cpf='11111111111',
            data_nascimento=date(1992, 3, 10),
            email='ana@example.com'
        )
        
        PresencaDetalhada.objects.create(
            aluno=aluno2,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 1),
            convocacoes=10,
            presencas=6,
            faltas=4,
            registrado_por='test'
        )
        
        tabela = CalculadoraEstatisticas.gerar_tabela_consolidada(
            turma_id=self.turma.id,
            ordenar_por='nome'
        )
        
        # Verificar ordem alfabética
        self.assertEqual(len(tabela['linhas']), 2)
        self.assertEqual(tabela['linhas'][0]['aluno']['nome'], 'Ana Costa')
        self.assertEqual(tabela['linhas'][1]['aluno']['nome'], 'João Silva')
    
    def test_ordenacao_tabela_por_percentual(self):
        """Testa ordenação da tabela por percentual."""
        # Criar outro aluno
        aluno2 = Aluno.objects.create(
            nome='Ana Costa',
            cpf='11111111111',
            data_nascimento=date(1992, 3, 10),
            email='ana@example.com'
        )
        
        PresencaDetalhada.objects.create(
            aluno=aluno2,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 1),
            convocacoes=10,
            presencas=9,  # 90% - maior que João (80%)
            faltas=1,
            registrado_por='test'
        )
        
        tabela = CalculadoraEstatisticas.gerar_tabela_consolidada(
            turma_id=self.turma.id,
            ordenar_por='percentual'
        )
        
        # Verificar ordem por percentual (decrescente)
        self.assertEqual(len(tabela['linhas']), 2)
        self.assertEqual(tabela['linhas'][0]['aluno']['nome'], 'Ana Costa')  # 90%
        self.assertEqual(tabela['linhas'][1]['aluno']['nome'], 'João Silva')  # 80%
        self.assertEqual(tabela['linhas'][0]['percentual_geral'], 90.0)
        self.assertEqual(tabela['linhas'][1]['percentual_geral'], 80.0)
    
    def test_filtro_por_periodo(self):
        """Testa filtragem por período."""
        # Criar presença em outro período
        PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 2, 1),
            convocacoes=10,
            presencas=5,
            faltas=5,
            registrado_por='test'
        )
        
        # Testar filtro por período
        consolidado = CalculadoraEstatisticas.calcular_consolidado_aluno(
            self.aluno.id,
            periodo_inicio=date(2024, 1, 1),
            periodo_fim=date(2024, 1, 31)
        )
        
        # Deve incluir apenas a presença de janeiro
        self.assertEqual(consolidado['totais']['presencas'], 8)  # Apenas janeiro
        
        # Testar sem filtro
        consolidado_completo = CalculadoraEstatisticas.calcular_consolidado_aluno(
            self.aluno.id
        )
        
        # Deve incluir ambas as presenças
        self.assertEqual(consolidado_completo['totais']['presencas'], 13)  # 8 + 5
    
    def test_status_aluno(self):
        """Testa determinação do status do aluno."""
        # Testar diferentes cenários
        
        # Excelente: 90%+ e sem carências
        status = CalculadoraEstatisticas._determinar_status_aluno(
            Decimal('95.0'), 0
        )
        self.assertEqual(status, 'excelente')
        
        # Bom: 80%+ e até 2 carências
        status = CalculadoraEstatisticas._determinar_status_aluno(
            Decimal('85.0'), 1
        )
        self.assertEqual(status, 'bom')
        
        # Regular: 70%+ e até 5 carências
        status = CalculadoraEstatisticas._determinar_status_aluno(
            Decimal('75.0'), 3
        )
        self.assertEqual(status, 'regular')
        
        # Atenção: 60%+
        status = CalculadoraEstatisticas._determinar_status_aluno(
            Decimal('65.0'), 2
        )
        self.assertEqual(status, 'atencao')
        
        # Crítico: menos de 60%
        status = CalculadoraEstatisticas._determinar_status_aluno(
            Decimal('55.0'), 1
        )
        self.assertEqual(status, 'critico')
    
    def test_error_handling(self):
        """Testa tratamento de erros."""
        # Testar com ID inválido
        with self.assertRaises(ValidationError):
            CalculadoraEstatisticas.calcular_consolidado_aluno(99999)
        
        # Testar cálculo de carências com ID inválido
        with self.assertRaises(ValidationError):
            CalculadoraEstatisticas.calcular_carencias(99999)
    
    def test_performance_query_optimization(self):
        """Testa otimização de queries."""
        # Criar múltiplos alunos e presenças
        alunos = []
        for i in range(10):
            aluno = Aluno.objects.create(
                nome=f'Aluno {i}',
                cpf=f'1234567890{i}',
                data_nascimento=date(1990, 1, 1),
                email=f'aluno{i}@example.com'
            )
            alunos.append(aluno)
            
            PresencaDetalhada.objects.create(
                aluno=aluno,
                turma=self.turma,
                atividade=self.atividade,
                periodo=date(2024, 1, 1),
                convocacoes=10,
                presencas=8,
                faltas=2,
                registrado_por='test'
            )
        
        # Testar que a query é otimizada (não deve gerar N+1 queries)
        with self.assertNumQueries(1):  # Apenas uma query principal
            tabela = CalculadoraEstatisticas.gerar_tabela_consolidada(
                turma_id=self.turma.id
            )
            
            # Verificar que todos os dados foram carregados
            self.assertEqual(len(tabela['linhas']), 11)  # 10 novos + 1 original
