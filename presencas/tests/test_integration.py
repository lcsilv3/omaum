"""
Testes de integração para o sistema de presenças.
Testa fluxos completos end-to-end e interações entre componentes.
"""

import json
from datetime import date, datetime
from django.test import TestCase, TransactionTestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import transaction
from unittest.mock import patch

from alunos.services import criar_aluno
from turmas.models import Turma
from atividades.models import Atividade
from presencas.models import (
    PresencaAcademica, 
    TotalAtividadeMes, 
    ObservacaoPresenca,
    Presenca
)


class PresencaIntegrationTestCase(TestCase):
    """Classe base para testes de integração do sistema de presenças."""
    
    def setUp(self):
        """Setup com dados realistas para testes."""
        # Criar usuário
        self.user = User.objects.create_user(
            username='professor_teste',
            email='professor@teste.com',
            password='senha123'
        )
        
        # Criar turma
        self.turma = Turma.objects.create(
            codigo_turma="TURMA001",
            nome="Iniciação Primeira Turma",
            ativa=True
        )
        
        # Criar atividades
        self.atividade_ritual = Atividade.objects.create(
            nome="Ritual de Abertura",
            tipo="RITUAL",
            ativa=True
        )
        
        self.atividade_aula = Atividade.objects.create(
            nome="Aula Teórica",
            tipo="AULA",
            ativa=True
        )
        
        # Criar alunos realistas
        self.alunos = []
        for i in range(5):
            aluno_data = {
                "cpf": f"1234567890{i}",
                "nome": f"Aluno Teste {i+1}",
                "data_nascimento": "1990-01-01",
                "hora_nascimento": "14:30",
                "email": f"aluno{i+1}@teste.com",
                "sexo": "M" if i % 2 == 0 else "F",
                "nacionalidade": "Brasileira",
                "naturalidade": "São Paulo",
                "rua": f"Rua Teste {i+1}",
                "numero_imovel": str(100 + i),
                "cidade": "São Paulo",
                "estado": "SP",
                "bairro": "Centro",
                "cep": "01234567",
                "nome_primeiro_contato": f"Contato {i+1}",
                "celular_primeiro_contato": f"1199999999{i}",
                "tipo_relacionamento_primeiro_contato": "Mãe",
                "nome_segundo_contato": f"Contato2 {i+1}",
                "celular_segundo_contato": f"1198888888{i}",
                "tipo_relacionamento_segundo_contato": "Pai",
                "tipo_sanguineo": "A",
                "fator_rh": "+",
            }
            aluno = criar_aluno(aluno_data)
            self.alunos.append(aluno)
        
        # Cliente para requisições
        self.client = Client()
        self.client.login(username='professor_teste', password='senha123')
        
        # Data padrão para testes
        self.data_teste = date.today()


class RegistroPresencaFluxoCompletoTest(PresencaIntegrationTestCase):
    """Testa o fluxo completo de registro de presenças."""
    
    def test_fluxo_registro_presenca_turma_completa(self):
        """Testa registro de presença para turma completa."""
        # 1. Acessar página de registro
        url = reverse('presencas:registro_rapido')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Registro Rápido')
        
        # 2. Enviar dados de presença via POST
        presenca_data = {
            'turma': self.turma.id,
            'atividade': self.atividade_aula.id,
            'data': self.data_teste.strftime('%Y-%m-%d'),
        }
        
        # Adicionar presenças para todos os alunos
        for i, aluno in enumerate(self.alunos):
            presenca_data[f'aluno_{aluno.id}_presente'] = 'on' if i < 3 else ''
            if i >= 3:  # Últimos 2 alunos ausentes com justificativa
                presenca_data[f'aluno_{aluno.id}_justificativa'] = f'Justificativa aluno {i+1}'
        
        response = self.client.post(url, presenca_data)
        
        # 3. Verificar redirecionamento de sucesso
        self.assertEqual(response.status_code, 302)
        
        # 4. Verificar se presenças foram salvas corretamente
        presencas = PresencaAcademica.objects.filter(
            turma=self.turma,
            data=self.data_teste
        )
        self.assertEqual(presencas.count(), 5)
        
        # Verificar presenças
        presentes = presencas.filter(presente=True)
        ausentes = presencas.filter(presente=False)
        
        self.assertEqual(presentes.count(), 3)
        self.assertEqual(ausentes.count(), 2)
        
        # Verificar justificativas
        for ausente in ausentes:
            self.assertIsNotNone(ausente.justificativa)
            self.assertIn('Justificativa', ausente.justificativa)
    
    def test_fluxo_edicao_presenca_individual(self):
        """Testa edição de presença individual."""
        # Criar presença inicial
        presenca = PresencaAcademica.objects.create(
            aluno=self.alunos[0],
            turma=self.turma,
            atividade=self.atividade_aula,
            data=self.data_teste,
            presente=True
        )
        
        # 1. Acessar página de edição
        url = reverse('presencas:editar_presenca', args=[presenca.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # 2. Editar para ausente com justificativa
        edit_data = {
            'presente': False,
            'justificativa': 'Doente - atestado médico'
        }
        response = self.client.post(url, edit_data)
        
        # 3. Verificar se foi atualizada
        presenca.refresh_from_db()
        self.assertFalse(presenca.presente)
        self.assertEqual(presenca.justificativa, 'Doente - atestado médico')


class VisualizacaoConsolidadaFluxoTest(PresencaIntegrationTestCase):
    """Testa fluxos de visualização consolidada."""
    
    def setUp(self):
        super().setUp()
        # Criar dados de presença para testes
        for i, aluno in enumerate(self.alunos):
            for dia in range(1, 6):  # 5 dias de presença
                PresencaAcademica.objects.create(
                    aluno=aluno,
                    turma=self.turma,
                    atividade=self.atividade_aula,
                    data=date(2024, 1, dia),
                    presente=i % 2 == 0 or dia <= 3  # Variação nas presenças
                )
    
    def test_fluxo_visualizacao_consolidada_mensal(self):
        """Testa visualização consolidada mensal."""
        url = reverse('presencas:consolidado')
        
        # 1. Acessar sem filtros
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Relatório Consolidado')
        
        # 2. Aplicar filtros específicos
        filtros = {
            'turma': self.turma.id,
            'mes': 1,
            'ano': 2024
        }
        response = self.client.get(url, filtros)
        self.assertEqual(response.status_code, 200)
        
        # 3. Verificar dados na resposta
        context = response.context
        self.assertIn('relatorio_data', context)
        self.assertIn('estatisticas', context)
        
        # 4. Verificar cálculos de estatísticas
        estatisticas = context['estatisticas']
        self.assertIsInstance(estatisticas, dict)
        self.assertIn('total_alunos', estatisticas)
        self.assertIn('presencas_registradas', estatisticas)
    
    def test_fluxo_detalhamento_aluno_especifico(self):
        """Testa fluxo de detalhamento para aluno específico."""
        aluno = self.alunos[0]
        url = reverse('presencas:detalhes_aluno', args=[aluno.id])
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Verificar dados do aluno na resposta
        self.assertContains(response, aluno.nome)
        self.assertContains(response, 'Histórico de Presenças')


class ExportacaoRelatoriosFluxoTest(PresencaIntegrationTestCase):
    """Testa fluxos de exportação de relatórios."""
    
    def setUp(self):
        super().setUp()
        # Criar dados para exportação
        for aluno in self.alunos[:3]:  # Apenas 3 alunos para teste
            PresencaAcademica.objects.create(
                aluno=aluno,
                turma=self.turma,
                atividade=self.atividade_aula,
                data=self.data_teste,
                presente=True
            )
    
    def test_fluxo_exportacao_excel(self):
        """Testa exportação para Excel."""
        url = reverse('presencas:exportar_excel')
        
        # Dados de filtro para exportação
        export_data = {
            'turma': self.turma.id,
            'data_inicio': self.data_teste.strftime('%Y-%m-%d'),
            'data_fim': self.data_teste.strftime('%Y-%m-%d'),
            'formato': 'excel'
        }
        
        response = self.client.post(url, export_data)
        
        # Verificar response de download
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get('Content-Type'),
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        self.assertIn('attachment', response.get('Content-Disposition', ''))
    
    def test_fluxo_exportacao_pdf(self):
        """Testa exportação para PDF."""
        url = reverse('presencas:exportar_pdf')
        
        export_data = {
            'turma': self.turma.id,
            'data_inicio': self.data_teste.strftime('%Y-%m-%d'),
            'data_fim': self.data_teste.strftime('%Y-%m-%d')
        }
        
        response = self.client.post(url, export_data)
        
        # Verificar response de PDF
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'application/pdf')


class PainelEstatisticasFluxoTest(PresencaIntegrationTestCase):
    """Testa fluxos do painel de estatísticas."""
    
    def setUp(self):
        super().setUp()
        # Criar dados estatísticos variados
        for i, aluno in enumerate(self.alunos):
            for dia in range(1, 11):  # 10 dias
                PresencaAcademica.objects.create(
                    aluno=aluno,
                    turma=self.turma,
                    atividade=self.atividade_aula,
                    data=date(2024, 1, dia),
                    presente=(i + dia) % 3 != 0  # Padrão variado de presenças
                )
    
    def test_fluxo_painel_estatisticas_geral(self):
        """Testa carregamento do painel geral de estatísticas."""
        url = reverse('presencas:painel_estatisticas')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Verificar elementos do painel
        self.assertContains(response, 'Painel de Estatísticas')
        self.assertContains(response, 'Total de Alunos')
        self.assertContains(response, 'Taxa de Presença')
    
    def test_fluxo_api_estatisticas_ajax(self):
        """Testa APIs AJAX para estatísticas."""
        url = reverse('presencas:api_estatisticas_turma')
        
        # Requisição AJAX para estatísticas da turma
        response = self.client.get(url, {
            'turma_id': self.turma.id,
            'mes': 1,
            'ano': 2024
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        
        # Verificar se retorna JSON válido
        data = json.loads(response.content)
        self.assertIn('total_alunos', data)
        self.assertIn('total_presencas', data)
        self.assertIn('taxa_presenca', data)
        self.assertIsInstance(data['taxa_presenca'], (int, float))


class APIAjaxFluxosTest(PresencaIntegrationTestCase):
    """Testa fluxos das APIs AJAX."""
    
    def test_api_buscar_alunos_turma(self):
        """Testa API para buscar alunos por turma."""
        url = reverse('presencas:api_alunos_turma')
        
        response = self.client.get(url, {
            'turma_id': self.turma.id
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('alunos', data)
        self.assertEqual(len(data['alunos']), 5)  # 5 alunos criados no setUp
    
    def test_api_salvar_presenca_rapida(self):
        """Testa API para salvamento rápido de presença."""
        url = reverse('presencas:api_salvar_presenca')
        
        presenca_data = {
            'aluno_id': self.alunos[0].id,
            'turma_id': self.turma.id,
            'atividade_id': self.atividade_aula.id,
            'data': self.data_teste.strftime('%Y-%m-%d'),
            'presente': True
        }
        
        response = self.client.post(
            url,
            json.dumps(presenca_data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Verificar se presença foi salva
        presenca = PresencaAcademica.objects.filter(
            aluno=self.alunos[0],
            turma=self.turma,
            data=self.data_teste
        ).first()
        
        self.assertIsNotNone(presenca)
        self.assertTrue(presenca.presente)


class NavegacaoEntrepaginasFluxoTest(PresencaIntegrationTestCase):
    """Testa fluxos de navegação entre páginas."""
    
    def test_navegacao_menu_principal(self):
        """Testa navegação pelo menu principal de presenças."""
        # Página inicial de presenças
        url = reverse('presencas:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Links para outras páginas devem estar presentes
        self.assertContains(response, 'Registro Rápido')
        self.assertContains(response, 'Relatório Consolidado')
        self.assertContains(response, 'Estatísticas')
    
    def test_fluxo_navegacao_breadcrumb(self):
        """Testa navegação via breadcrumb."""
        # Ir para página específica
        url = reverse('presencas:consolidado')
        response = self.client.get(url)
        
        # Verificar breadcrumb
        self.assertContains(response, 'Home')
        self.assertContains(response, 'Presenças')
        self.assertContains(response, 'Consolidado')
    
    def test_fluxo_voltar_pagina_anterior(self):
        """Testa funcionalidade de voltar para página anterior."""
        # Simular fluxo: index -> registro -> voltar
        index_url = reverse('presencas:index')
        registro_url = reverse('presencas:registro_rapido')
        
        # Acessar index
        response = self.client.get(index_url)
        self.assertEqual(response.status_code, 200)
        
        # Ir para registro
        response = self.client.get(registro_url)
        self.assertEqual(response.status_code, 200)
        
        # Verificar link de voltar
        self.assertContains(response, 'Voltar')


class WorkflowCompletosTest(PresencaIntegrationTestCase):
    """Testa workflows completos do sistema."""
    
    def test_workflow_professor_diario(self):
        """Testa workflow típico de um professor durante o dia."""
        # 1. Login e acesso ao sistema
        self.assertTrue(self.client.login(username='professor_teste', password='senha123'))
        
        # 2. Visualizar presenças do dia
        url = reverse('presencas:presencas_hoje')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # 3. Registrar presenças da primeira turma
        registro_url = reverse('presencas:registro_rapido')
        presenca_data = {
            'turma': self.turma.id,
            'atividade': self.atividade_ritual.id,
            'data': self.data_teste.strftime('%Y-%m-%d'),
        }
        
        for aluno in self.alunos:
            presenca_data[f'aluno_{aluno.id}_presente'] = 'on'
        
        response = self.client.post(registro_url, presenca_data)
        self.assertEqual(response.status_code, 302)
        
        # 4. Verificar registro foi salvo
        presencas = PresencaAcademica.objects.filter(
            turma=self.turma,
            data=self.data_teste,
            atividade=self.atividade_ritual
        )
        self.assertEqual(presencas.count(), 5)
        
        # 5. Consultar relatório do dia
        consolidado_url = reverse('presencas:consolidado')
        response = self.client.get(consolidado_url, {
            'data_inicio': self.data_teste.strftime('%Y-%m-%d'),
            'data_fim': self.data_teste.strftime('%Y-%m-%d')
        })
        self.assertEqual(response.status_code, 200)
    
    def test_workflow_coordenador_semanal(self):
        """Testa workflow típico de coordenador fazendo análise semanal."""
        # Criar dados da semana
        from datetime import timedelta
        
        for i in range(7):  # 7 dias
            data_dia = self.data_teste - timedelta(days=i)
            for aluno in self.alunos:
                PresencaAcademica.objects.create(
                    aluno=aluno,
                    turma=self.turma,
                    atividade=self.atividade_aula,
                    data=data_dia,
                    presente=i % 2 == 0  # Presença alternada
                )
        
        # 1. Acessar painel de estatísticas
        painel_url = reverse('presencas:painel_estatisticas')
        response = self.client.get(painel_url)
        self.assertEqual(response.status_code, 200)
        
        # 2. Gerar relatório semanal
        data_inicio = self.data_teste - timedelta(days=6)
        relatorio_url = reverse('presencas:consolidado')
        response = self.client.get(relatorio_url, {
            'turma': self.turma.id,
            'data_inicio': data_inicio.strftime('%Y-%m-%d'),
            'data_fim': self.data_teste.strftime('%Y-%m-%d')
        })
        self.assertEqual(response.status_code, 200)
        
        # 3. Exportar para análise
        export_url = reverse('presencas:exportar_excel')
        response = self.client.post(export_url, {
            'turma': self.turma.id,
            'data_inicio': data_inicio.strftime('%Y-%m-%d'),
            'data_fim': self.data_teste.strftime('%Y-%m-%d'),
            'formato': 'excel'
        })
        self.assertEqual(response.status_code, 200)


class TransacionalTest(TransactionTestCase):
    """Testes que requerem controle de transações."""
    
    def test_integridade_transacional_registro_multiplo(self):
        """Testa integridade transacional em registro múltiplo."""
        # Configurar dados
        user = User.objects.create_user('test', 'test@test.com', 'pass')
        turma = Turma.objects.create(codigo_turma="TX001", nome="Test")
        
        # Simular erro durante transação
        with self.assertRaises(Exception):
            with transaction.atomic():
                # Criar algumas presenças
                for i in range(3):
                    PresencaAcademica.objects.create(
                        aluno_id=999,  # ID inválido que causará erro
                        turma=turma,
                        data=date.today(),
                        presente=True
                    )
        
        # Verificar que nenhuma presença foi salva devido ao rollback
        self.assertEqual(PresencaAcademica.objects.count(), 0)


class CacheTest(PresencaIntegrationTestCase):
    """Testes relacionados a cache e performance."""
    
    @patch('django.core.cache.cache')
    def test_cache_estatisticas(self, mock_cache):
        """Testa cache de estatísticas."""
        mock_cache.get.return_value = None
        mock_cache.set.return_value = True
        
        url = reverse('presencas:api_estatisticas_turma')
        response = self.client.get(url, {
            'turma_id': self.turma.id,
            'mes': 1,
            'ano': 2024
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        
        # Verificar se cache foi utilizado
        mock_cache.get.assert_called()
        mock_cache.set.assert_called()
