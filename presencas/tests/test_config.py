"""
Configurações específicas para testes do aplicativo presencas.
"""

from django.test import TestCase, override_settings
import tempfile
import os


# Settings específicas para testes
TEST_SETTINGS = {
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    'PASSWORD_HASHERS': [
        'django.contrib.auth.hashers.MD5PasswordHasher',  # Mais rápido para testes
    ],
    'EMAIL_BACKEND': 'django.core.mail.backends.locmem.EmailBackend',
    'MEDIA_ROOT': tempfile.mkdtemp(),
    'STATIC_ROOT': tempfile.mkdtemp(),
    'CELERY_TASK_ALWAYS_EAGER': True,  # Se usando Celery
    'CACHES': {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'test-cache',
        }
    },
    'LOGGING': {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'null': {
                'class': 'logging.NullHandler',
            },
        },
        'root': {
            'handlers': ['null'],
        },
    }
}


class BaseTestCase(TestCase):
    """Classe base para todos os testes do aplicativo presencas."""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Configurações globais para os testes
        
    def setUp(self):
        """Configuração executada antes de cada teste."""
        super().setUp()
        
        # Limpar cache
        from django.core.cache import cache
        cache.clear()
        
        # Configurar timezone para testes
        from django.utils import timezone
        timezone.activate('America/Sao_Paulo')
    
    def tearDown(self):
        """Limpeza executada após cada teste."""
        super().tearDown()
        
        # Limpar arquivos temporários se necessário
        import shutil
        
        # Limpar diretórios de mídia temporários
        if hasattr(self, 'temp_media_dir'):
            shutil.rmtree(self.temp_media_dir, ignore_errors=True)


class DatabaseTestCase(BaseTestCase):
    """Classe base para testes que precisam de transações de banco."""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Configurações específicas para testes de banco
        
    def setUp(self):
        super().setUp()
        # Configurar transações
        from django.db import transaction
        self.transaction = transaction.atomic()
        self.transaction.__enter__()
    
    def tearDown(self):
        # Reverter transações
        if hasattr(self, 'transaction'):
            self.transaction.__exit__(None, None, None)
        super().tearDown()


class APITestCase(BaseTestCase):
    """Classe base para testes de API."""
    
    def setUp(self):
        super().setUp()
        from rest_framework.test import APIClient
        self.api_client = APIClient()
        
        # Criar usuário padrão para autenticação
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.test_user = User.objects.create_user(
            username='test_api_user',
            password='testpass123',
            email='api@test.com'
        )
    
    def authenticate_api(self, user=None):
        """Autentica o cliente da API."""
        user = user or self.test_user
        self.api_client.force_authenticate(user=user)
    
    def assert_api_response(self, response, expected_status, expected_keys=None):
        """Assertion helper para respostas de API."""
        self.assertEqual(response.status_code, expected_status)
        
        if expected_keys and hasattr(response, 'data'):
            for key in expected_keys:
                self.assertIn(key, response.data)


class PerformanceTestCase(BaseTestCase):
    """Classe base para testes de performance."""
    
    def setUp(self):
        super().setUp()
        # Configurar métricas de performance
        self.query_count_threshold = 10
        self.response_time_threshold = 1.0  # segundos
    
    def assert_query_count(self, expected_count):
        """Context manager para verificar número de queries."""
        return self.assertNumQueries(expected_count)
    
    def assert_max_queries(self, max_count):
        """Verifica que o número de queries não excede o máximo."""
        from django.db import connection
        initial_queries = len(connection.queries)
        
        class QueryAssertionContext:
            def __enter__(self):
                return self
            
            def __exit__(self, type, value, traceback):
                final_queries = len(connection.queries)
                query_count = final_queries - initial_queries
                if query_count > max_count:
                    raise AssertionError(
                        f"Too many queries: {query_count} > {max_count}"
                    )
        
        return QueryAssertionContext()


class IntegrationTestCase(BaseTestCase):
    """Classe base para testes de integração."""
    
    def setUp(self):
        super().setUp()
        # Configurar dados de integração
        self.create_integration_data()
    
    def create_integration_data(self):
        """Cria dados necessários para testes de integração."""
        from .factories import (
            UserFactory, CursoFactory, TurmaFactory,
            AlunoFactory, AtividadeFactory
        )
        
        # Criar dados básicos
        self.user = UserFactory()
        self.curso = CursoFactory()
        self.turma = TurmaFactory(curso=self.curso)
        self.aluno = AlunoFactory()
        self.atividade = AtividadeFactory()


# Decorators para configurações específicas de teste

def skip_if_no_db(test_func):
    """Pula teste se não há banco de dados disponível."""
    def wrapper(*args, **kwargs):
        try:
            from django.db import connection
            connection.ensure_connection()
            return test_func(*args, **kwargs)
        except Exception:
            import unittest
            raise unittest.SkipTest("Database not available")
    return wrapper


def with_temp_media_root(test_func):
    """Decorator para usar diretório temporário para mídia."""
    def wrapper(self, *args, **kwargs):
        import tempfile
        import shutil
        
        temp_dir = tempfile.mkdtemp()
        self.temp_media_dir = temp_dir
        
        with override_settings(MEDIA_ROOT=temp_dir):
            try:
                return test_func(self, *args, **kwargs)
            finally:
                shutil.rmtree(temp_dir, ignore_errors=True)
    
    return wrapper


def mock_time(mock_datetime):
    """Decorator para mockar datetime em testes."""
    def decorator(test_func):
        def wrapper(*args, **kwargs):
            from unittest.mock import patch
            with patch('django.utils.timezone.now', return_value=mock_datetime):
                return test_func(*args, **kwargs)
        return wrapper
    return decorator


# Mixins para funcionalidades específicas

class AssertionMixin:
    """Mixin com assertions customizadas para presencas."""
    
    def assertPresencaEquals(self, presenca, expected_data):
        """Verifica se presença tem os dados esperados."""
        for field, value in expected_data.items():
            actual_value = getattr(presenca, field)
            self.assertEqual(
                actual_value, value,
                f"Field {field}: expected {value}, got {actual_value}"
            )
    
    def assertConsolidadoValid(self, consolidado):
        """Verifica se consolidado tem estrutura válida."""
        required_keys = ['aluno', 'totais', 'percentuais', 'status']
        for key in required_keys:
            self.assertIn(key, consolidado)
        
        # Verificar totais
        totals = consolidado['totais']
        self.assertGreaterEqual(totals['presencas'], 0)
        self.assertGreaterEqual(totals['faltas'], 0)
        self.assertGreaterEqual(totals['convocacoes'], 0)
        
        # Verificar percentuais
        percentuais = consolidado['percentuais']
        self.assertGreaterEqual(percentuais['presenca'], 0)
        self.assertLessEqual(percentuais['presenca'], 100)
    
    def assertStatisticsValid(self, statistics):
        """Verifica se estatísticas têm estrutura válida."""
        required_keys = ['turma', 'totais', 'percentuais']
        for key in required_keys:
            self.assertIn(key, statistics)


class DataMixin:
    """Mixin para criação de dados de teste comuns."""
    
    def create_test_data(self):
        """Cria conjunto padrão de dados para testes."""
        from .factories import ConsolidadoCompletoFactory
        return ConsolidadoCompletoFactory.create()
    
    def create_performance_data(self, size='small'):
        """Cria dados para testes de performance."""
        from .factories import criar_dataset_performance
        
        sizes = {
            'small': (2, 10),
            'medium': (5, 25),
            'large': (10, 50)
        }
        
        turmas_count, alunos_count = sizes.get(size, sizes['small'])
        return criar_dataset_performance(turmas_count, alunos_count)


class MockMixin:
    """Mixin para mocks comuns."""
    
    def mock_datetime_now(self, fixed_datetime):
        """Mock para datetime.now."""
        from unittest.mock import patch
        return patch('django.utils.timezone.now', return_value=fixed_datetime)
    
    def mock_email_backend(self):
        """Mock para backend de email."""
        from unittest.mock import patch
        return patch('django.core.mail.backends.locmem.EmailBackend.send_messages')
    
    def mock_logger(self, logger_name):
        """Mock para logger específico."""
        from unittest.mock import patch
        return patch(f'{logger_name}.logger')


# Context managers para testes específicos

class CaptureQueries:
    """Context manager para capturar queries SQL."""
    
    def __init__(self):
        self.queries = []
    
    def __enter__(self):
        from django.db import connection
        self.initial_queries = len(connection.queries)
        return self
    
    def __exit__(self, type, value, traceback):
        from django.db import connection
        self.queries = connection.queries[self.initial_queries:]
    
    def count(self):
        return len(self.queries)
    
    def get_queries(self):
        return self.queries


class TempDirectory:
    """Context manager para diretório temporário."""
    
    def __init__(self):
        self.path = None
    
    def __enter__(self):
        import tempfile
        self.path = tempfile.mkdtemp()
        return self.path
    
    def __exit__(self, type, value, traceback):
        import shutil
        if self.path:
            shutil.rmtree(self.path, ignore_errors=True)


# Utilitários para testes

def create_test_file(content, filename='test.txt'):
    """Cria arquivo temporário para testes."""
    import tempfile
    
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, filename)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return file_path


def compare_querysets(qs1, qs2):
    """Compara dois querysets ignorando ordem."""
    return set(qs1.values_list('pk', flat=True)) == set(qs2.values_list('pk', flat=True))


def generate_test_cpf():
    """Gera CPF válido para testes."""
    import random
    
    def calculate_digit(digits):
        s = sum(a * b for a, b in zip(digits, range(len(digits) + 1, 1, -1)))
        return (11 - s % 11) % 10 if s % 11 >= 2 else 0
    
    digits = [random.randint(0, 9) for _ in range(9)]
    digits.append(calculate_digit(digits))
    digits.append(calculate_digit(digits))
    
    return ''.join(map(str, digits))


def assert_json_response(response, expected_status=200, expected_keys=None):
    """Helper para verificar respostas JSON."""
    import json
    
    assert response.status_code == expected_status
    assert response['Content-Type'] == 'application/json'
    
    data = json.loads(response.content)
    
    if expected_keys:
        for key in expected_keys:
            assert key in data, f"Key '{key}' not found in response"
    
    return data
