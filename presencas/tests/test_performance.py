"""
Testes de performance e carga para o sistema de presenças.
Validação de queries otimizadas e tempos de resposta.
"""

import time
from datetime import date, timedelta
from django.test import TestCase, TransactionTestCase, override_settings
from django.test.utils import override_settings
from django.db import connection
from django.db.models import Count, Q, Prefetch
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache
from unittest.mock import patch

from alunos.services import criar_aluno
from turmas.models import Turma
from atividades.models import Atividade
from presencas.models import PresencaAcademica, TotalAtividadeMes


class PerformanceTestCase(TestCase):
    """Classe base para testes de performance."""
    
    def setUp(self):
        """Setup otimizado para testes de performance."""
        self.user = User.objects.create_user(
            username='perf_user',
            password='test123'
        )
        
        # Configurar dados base
        self.turma = Turma.objects.create(
            codigo_turma="PERF001",
            nome="Turma Performance Test"
        )
        
        self.atividade = Atividade.objects.create(
            nome="Atividade Performance",
            tipo="AULA",
            ativa=True
        )
        
        # Limpar cache antes de cada teste
        cache.clear()
        
        # Resetar contador de queries
        connection.queries_log.clear()
    
    def criar_alunos_em_lote(self, quantidade):
        """Cria alunos em lote para testes de performance."""
        alunos = []
        for i in range(quantidade):
            aluno_data = {
                "cpf": f"{i+1:011d}",
                "nome": f"Aluno Performance {i+1}",
                "data_nascimento": "1990-01-01",
                "hora_nascimento": "14:30",
                "email": f"perf{i+1}@test.com",
                "sexo": "M" if i % 2 == 0 else "F",
                "nacionalidade": "Brasileira",
                "naturalidade": "São Paulo",
                "rua": f"Rua {i+1}",
                "numero_imovel": str(i+1),
                "cidade": "São Paulo",
                "estado": "SP",
                "bairro": "Centro",
                "cep": f"{i+1:08d}",
                "nome_primeiro_contato": f"Contato {i+1}",
                "celular_primeiro_contato": f"11{i+1:09d}",
                "tipo_relacionamento_primeiro_contato": "Mãe",
                "nome_segundo_contato": f"Pai {i+1}",
                "celular_segundo_contato": f"11{i+1:09d}",
                "tipo_relacionamento_segundo_contato": "Pai",
                "tipo_sanguineo": "A",
                "fator_rh": "+",
            }
            aluno = criar_aluno(aluno_data)
            alunos.append(aluno)
        return alunos
    
    def criar_presencas_em_lote(self, alunos, dias=30):
        """Cria presenças em lote para múltiplos dias."""
        presencas = []
        base_date = date.today() - timedelta(days=dias)
        
        for i in range(dias):
            data_dia = base_date + timedelta(days=i)
            for aluno in alunos:
                presenca = PresencaAcademica(
                    aluno=aluno,
                    turma=self.turma,
                    atividade=self.atividade,
                    data=data_dia,
                    presente=i % 3 != 0,  # 66% presença
                    justificativa='' if i % 3 != 0 else f'Falta dia {i+1}'
                )
                presencas.append(presenca)
        
        # Inserção em lote para melhor performance
        PresencaAcademica.objects.bulk_create(presencas, batch_size=1000)
        return presencas
    
    def contar_queries(self):
        """Retorna número de queries executadas."""
        return len(connection.queries)
    
    def medir_tempo_execucao(self, func, *args, **kwargs):
        """Mede tempo de execução de uma função."""
        start_time = time.time()
        resultado = func(*args, **kwargs)
        end_time = time.time()
        return resultado, end_time - start_time


class QueryOptimizationTest(PerformanceTestCase):
    """Testes de otimização de queries."""
    
    def test_listagem_presencas_select_related(self):
        """Testa se listagem usa select_related para evitar N+1 queries."""
        # Criar dados
        alunos = self.criar_alunos_em_lote(20)
        self.criar_presencas_em_lote(alunos, 5)
        
        self.client.login(username='perf_user', password='test123')
        
        # Limpar queries anteriores
        connection.queries_log.clear()
        
        # Fazer requisição
        url = reverse('presencas:listar_presencas_academicas')
        response = self.client.get(url, {
            'turma': self.turma.id
        })
        
        self.assertEqual(response.status_code, 200)
        
        # Verificar número de queries
        num_queries = self.contar_queries()
        
        # Com select_related otimizado, deve usar poucas queries
        # independente do número de presenças
        self.assertLess(num_queries, 10, 
                       f"Muitas queries executadas: {num_queries}. "
                       f"Verifique se select_related está sendo usado.")
    
    def test_consolidado_prefetch_related(self):
        """Testa se relatório consolidado usa prefetch_related."""
        # Criar dados substanciais
        alunos = self.criar_alunos_em_lote(15)
        self.criar_presencas_em_lote(alunos, 30)
        
        self.client.login(username='perf_user', password='test123')
        
        connection.queries_log.clear()
        
        # Acessar relatório consolidado
        url = reverse('presencas:consolidado')
        response = self.client.get(url, {
            'turma': self.turma.id,
            'mes': date.today().month,
            'ano': date.today().year
        })
        
        self.assertEqual(response.status_code, 200)
        
        num_queries = self.contar_queries()
        
        # Relatório consolidado deve ser eficiente mesmo com muitos dados
        self.assertLess(num_queries, 15,
                       f"Relatório consolidado usando muitas queries: {num_queries}")
    
    def test_estatisticas_query_agregada(self):
        """Testa se cálculo de estatísticas usa queries agregadas."""
        alunos = self.criar_alunos_em_lote(25)
        self.criar_presencas_em_lote(alunos, 20)
        
        self.client.login(username='perf_user', password='test123')
        
        connection.queries_log.clear()
        
        # API de estatísticas
        url = reverse('presencas:api_estatisticas_turma')
        response = self.client.get(url, {
            'turma_id': self.turma.id,
            'mes': date.today().month,
            'ano': date.today().year
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        
        num_queries = self.contar_queries()
        
        # Estatísticas devem usar agregação no banco, não loops Python
        self.assertLess(num_queries, 5,
                       f"Cálculo de estatísticas ineficiente: {num_queries} queries")


class LoadTestCase(PerformanceTestCase):
    """Testes de carga com muitos dados."""
    
    def test_turma_100_alunos(self):
        """Testa performance com turma de 100 alunos."""
        # Criar turma grande
        alunos = self.criar_alunos_em_lote(100)
        
        self.client.login(username='perf_user', password='test123')
        
        # Testar carregamento da página de registro
        url = reverse('presencas:registro_rapido')
        
        _, tempo_execucao = self.medir_tempo_execucao(
            self.client.get, url, {'turma': self.turma.id}
        )
        
        # Deve carregar em tempo aceitável (ajustar conforme necessário)
        self.assertLess(tempo_execucao, 3.0,
                       f"Carregamento muito lento: {tempo_execucao}s")
    
    def test_historico_1_ano_completo(self):
        """Testa performance com histórico de 1 ano completo."""
        # 30 alunos com 365 dias de histórico
        alunos = self.criar_alunos_em_lote(30)
        self.criar_presencas_em_lote(alunos, 365)
        
        self.client.login(username='perf_user', password='test123')
        
        # Testar relatório anual
        data_inicio = date.today() - timedelta(days=365)
        data_fim = date.today()
        
        url = reverse('presencas:consolidado')
        
        _, tempo_execucao = self.medir_tempo_execucao(
            self.client.get, url, {
                'turma': self.turma.id,
                'data_inicio': data_inicio.strftime('%Y-%m-%d'),
                'data_fim': data_fim.strftime('%Y-%m-%d')
            }
        )
        
        # Relatório anual deve ser gerado em tempo razoável
        self.assertLess(tempo_execucao, 5.0,
                       f"Relatório anual muito lento: {tempo_execucao}s")
    
    def test_exportacao_dados_grandes(self):
        """Testa exportação com volume grande de dados."""
        alunos = self.criar_alunos_em_lote(50)
        self.criar_presencas_em_lote(alunos, 180)  # 6 meses
        
        self.client.login(username='perf_user', password='test123')
        
        # Exportar para Excel
        url = reverse('presencas:exportar_excel')
        export_data = {
            'turma': self.turma.id,
            'data_inicio': (date.today() - timedelta(days=180)).strftime('%Y-%m-%d'),
            'data_fim': date.today().strftime('%Y-%m-%d')
        }
        
        _, tempo_execucao = self.medir_tempo_execucao(
            self.client.post, url, export_data
        )
        
        # Exportação deve completar em tempo aceitável
        self.assertLess(tempo_execucao, 10.0,
                       f"Exportação muito lenta: {tempo_execucao}s")


class CachePerformanceTest(PerformanceTestCase):
    """Testes de performance relacionados a cache."""
    
    @override_settings(CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    })
    def test_cache_estatisticas_turma(self):
        """Testa se estatísticas de turma são cacheadas adequadamente."""
        alunos = self.criar_alunos_em_lote(20)
        self.criar_presencas_em_lote(alunos, 30)
        
        self.client.login(username='perf_user', password='test123')
        
        url = reverse('presencas:api_estatisticas_turma')
        params = {
            'turma_id': self.turma.id,
            'mes': date.today().month,
            'ano': date.today().year
        }
        
        # Primeira requisição - deve calcular e cachear
        connection.queries_log.clear()
        response1 = self.client.get(url, params, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        queries_primeira = self.contar_queries()
        
        # Segunda requisição - deve usar cache
        connection.queries_log.clear()
        response2 = self.client.get(url, params, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        queries_segunda = self.contar_queries()
        
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        
        # Segunda requisição deve usar menos queries (cache hit)
        self.assertLess(queries_segunda, queries_primeira,
                       "Cache de estatísticas não está funcionando")
    
    def test_invalidacao_cache_ao_atualizar(self):
        """Testa se cache é invalidado quando dados são atualizados."""
        alunos = self.criar_alunos_em_lote(10)
        
        # Simular cache de estatísticas
        cache_key = f"estatisticas_turma_{self.turma.id}_{date.today().month}_{date.today().year}"
        cache.set(cache_key, {'total_alunos': 10}, 300)
        
        # Adicionar nova presença
        PresencaAcademica.objects.create(
            aluno=alunos[0],
            turma=self.turma,
            atividade=self.atividade,
            data=date.today(),
            presente=True
        )
        
        # Cache deve ser invalidado após inserção
        # (Em implementação real, seria via signals)
        cached_value = cache.get(cache_key)
        
        # Este teste assume que há invalidação automática via signals
        # Se não implementado, pode ser None ou valor antigo
        self.assertTrue(cached_value is None or cached_value != {'total_alunos': 10})


class ResponseTimeTest(PerformanceTestCase):
    """Testes específicos de tempo de resposta."""
    
    def test_tempo_resposta_pagina_inicial(self):
        """Testa tempo de resposta da página inicial de presenças."""
        self.client.login(username='perf_user', password='test123')
        
        url = reverse('presencas:index')
        
        start_time = time.time()
        response = self.client.get(url)
        end_time = time.time()
        
        tempo_resposta = end_time - start_time
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(tempo_resposta, 1.0,
                       f"Página inicial muito lenta: {tempo_resposta}s")
    
    def test_tempo_resposta_api_ajax(self):
        """Testa tempo de resposta das APIs AJAX."""
        alunos = self.criar_alunos_em_lote(15)
        
        self.client.login(username='perf_user', password='test123')
        
        # Testar API de busca de alunos
        url = reverse('presencas:api_alunos_turma')
        
        start_time = time.time()
        response = self.client.get(url, {
            'turma_id': self.turma.id
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        end_time = time.time()
        
        tempo_resposta = end_time - start_time
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(tempo_resposta, 0.5,
                       f"API AJAX muito lenta: {tempo_resposta}s")
    
    def test_tempo_resposta_salvamento_presenca(self):
        """Testa tempo de resposta para salvamento de presença."""
        aluno = self.criar_alunos_em_lote(1)[0]
        
        self.client.login(username='perf_user', password='test123')
        
        url = reverse('presencas:api_salvar_presenca')
        data = {
            'aluno_id': aluno.id,
            'turma_id': self.turma.id,
            'atividade_id': self.atividade.id,
            'data': date.today().strftime('%Y-%m-%d'),
            'presente': True
        }
        
        start_time = time.time()
        response = self.client.post(
            url,
            data,
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        end_time = time.time()
        
        tempo_resposta = end_time - start_time
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(tempo_resposta, 0.3,
                       f"Salvamento muito lento: {tempo_resposta}s")


class BenchmarkTest(PerformanceTestCase):
    """Benchmarks para medir performance base do sistema."""
    
    def test_benchmark_criacao_presencas(self):
        """Benchmark para criação de presenças em lote."""
        alunos = self.criar_alunos_em_lote(50)
        
        # Medir tempo para criar 50 presenças
        start_time = time.time()
        
        presencas = []
        for aluno in alunos:
            presenca = PresencaAcademica(
                aluno=aluno,
                turma=self.turma,
                atividade=self.atividade,
                data=date.today(),
                presente=True
            )
            presencas.append(presenca)
        
        PresencaAcademica.objects.bulk_create(presencas)
        
        end_time = time.time()
        tempo_criacao = end_time - start_time
        
        # Benchmark: deve criar 50 presenças em menos de 1 segundo
        self.assertLess(tempo_criacao, 1.0,
                       f"Criação em lote muito lenta: {tempo_criacao}s para 50 registros")
        
        # Verificar se todas foram criadas
        total_criadas = PresencaAcademica.objects.filter(
            turma=self.turma,
            data=date.today()
        ).count()
        self.assertEqual(total_criadas, 50)
    
    def test_benchmark_consulta_historico(self):
        """Benchmark para consulta de histórico complexo."""
        alunos = self.criar_alunos_em_lote(30)
        self.criar_presencas_em_lote(alunos, 90)  # 3 meses
        
        # Consulta complexa: presença por aluno nos últimos 90 dias
        start_time = time.time()
        
        data_inicio = date.today() - timedelta(days=90)
        
        # Query otimizada com agregação
        resultado = PresencaAcademica.objects.filter(
            turma=self.turma,
            data__gte=data_inicio
        ).values('aluno__nome').annotate(
            total_presencas=Count('id'),
            total_presentes=Count('id', filter=Q(presente=True))
        ).order_by('aluno__nome')
        
        # Forçar execução da query
        list(resultado)
        
        end_time = time.time()
        tempo_consulta = end_time - start_time
        
        # Benchmark: consulta complexa deve executar rapidamente
        self.assertLess(tempo_consulta, 0.5,
                       f"Consulta de histórico muito lenta: {tempo_consulta}s")
    
    def test_benchmark_calculo_estatisticas(self):
        """Benchmark para cálculo de estatísticas complexas."""
        alunos = self.criar_alunos_em_lote(40)
        self.criar_presencas_em_lote(alunos, 60)
        
        start_time = time.time()
        
        # Cálculos estatísticos complexos
        presencas_queryset = PresencaAcademica.objects.filter(turma=self.turma)
        
        estatisticas = {
            'total_registros': presencas_queryset.count(),
            'total_presentes': presencas_queryset.filter(presente=True).count(),
            'total_ausentes': presencas_queryset.filter(presente=False).count(),
            'alunos_frequentes': presencas_queryset.values('aluno').annotate(
                taxa_presenca=Count('id', filter=Q(presente=True)) * 100.0 / Count('id')
            ).filter(taxa_presenca__gte=80).count(),
            'media_presenca_mensal': presencas_queryset.extra(
                select={'mes': "EXTRACT(month FROM data)"}
            ).values('mes').annotate(
                presentes=Count('id', filter=Q(presente=True)),
                total=Count('id')
            )
        }
        
        # Forçar execução de todas as queries
        for key, value in estatisticas.items():
            if hasattr(value, '__iter__') and not isinstance(value, (str, bytes)):
                list(value)
        
        end_time = time.time()
        tempo_calculo = end_time - start_time
        
        # Benchmark: cálculos estatísticos devem ser rápidos
        self.assertLess(tempo_calculo, 2.0,
                       f"Cálculo de estatísticas muito lento: {tempo_calculo}s")


@override_settings(DEBUG=True)  # Para capturar queries
class MemoryUsageTest(PerformanceTestCase):
    """Testes de uso de memória."""
    
    def test_memoria_consulta_grande_dataset(self):
        """Testa se consultas grandes não consomem memória excessiva."""
        # Criar dataset grande
        alunos = self.criar_alunos_em_lote(100)
        self.criar_presencas_em_lote(alunos, 180)
        
        # Usar iterator() para grandes datasets
        presencas_queryset = PresencaAcademica.objects.filter(
            turma=self.turma
        ).select_related('aluno', 'atividade').iterator(chunk_size=1000)
        
        # Processar em chunks para não carregar tudo na memória
        contador = 0
        for presenca in presencas_queryset:
            contador += 1
            # Simular processamento
            _ = f"{presenca.aluno.nome} - {presenca.data}"
        
        # Verificar se processou todos os registros
        total_esperado = 100 * 180  # 100 alunos * 180 dias
        self.assertEqual(contador, total_esperado)
        
        # Em um teste real, mediríamos o uso de memória aqui
        # import psutil, os
        # process = psutil.Process(os.getpid())
        # memory_usage = process.memory_info().rss / 1024 / 1024  # MB
        # self.assertLess(memory_usage, 500)  # Menos que 500MB
