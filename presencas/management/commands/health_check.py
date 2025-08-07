"""
FASE 3C: Management command para monitoramento de saúde do sistema.
"""

import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List

from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.db import connection, transaction
from django.conf import settings
from django.contrib.auth.models import User

from presencas.models import PresencaDetalhada, Aluno, Atividade
from presencas.bulk_operations import BulkPresencaOperations


class Command(BaseCommand):
    """
    Command para verificação de saúde do sistema e métricas de performance.
    """
    
    help = 'Executa verificação de saúde do sistema OMAUM'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger('presencas.health_check')
        self.results = {}
    
    def add_arguments(self, parser):
        """Adiciona argumentos do comando."""
        parser.add_argument(
            '--format',
            choices=['json', 'table', 'summary'],
            default='summary',
            help='Formato de saída dos resultados'
        )
        
        parser.add_argument(
            '--checks',
            nargs='+',
            choices=['database', 'cache', 'celery', 'performance', 'security', 'all'],
            default=['all'],
            help='Tipos de verificação a executar'
        )
        
        parser.add_argument(
            '--threshold',
            type=float,
            default=1.0,
            help='Threshold para queries lentas (segundos)'
        )
        
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Saída verbose com detalhes'
        )
    
    def handle(self, *args, **options):
        """Executa as verificações de saúde."""
        
        self.stdout.write(
            self.style.SUCCESS('🏥 OMAUM System Health Check')
        )
        self.stdout.write('=' * 50)
        
        start_time = time.time()
        
        # Executar verificações baseadas nos argumentos
        checks_to_run = options['checks']
        if 'all' in checks_to_run:
            checks_to_run = ['database', 'cache', 'celery', 'performance', 'security']
        
        for check in checks_to_run:
            self.stdout.write(f'\n🔍 Executando verificação: {check.upper()}')
            
            try:
                check_method = getattr(self, f'check_{check}')
                result = check_method(options)
                self.results[check] = result
                
                status = '✅ PASS' if result.get('status') == 'healthy' else '❌ FAIL'
                self.stdout.write(f'{status} {check.upper()}: {result.get("summary", "N/A")}')
                
            except Exception as e:
                self.results[check] = {
                    'status': 'error',
                    'error': str(e),
                    'summary': f'Erro na verificação: {e}'
                }
                self.stdout.write(
                    self.style.ERROR(f'❌ ERRO {check.upper()}: {e}')
                )
        
        # Relatório final
        total_time = time.time() - start_time
        self.generate_report(options, total_time)
    
    def check_database(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """Verifica saúde do banco de dados."""
        
        start_time = time.time()
        issues = []
        
        try:
            # Teste de conectividade
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                
                if result[0] != 1:
                    issues.append("Conectividade com banco de dados falhou")
            
            # Contar registros principais
            total_presencas = PresencaDetalhada.objects.count()
            total_alunos = Aluno.objects.count()
            total_atividades = Atividade.objects.count()
            
            # Verificar integridade referencial
            presencas_orfas = PresencaDetalhada.objects.filter(
                aluno__isnull=True
            ).count()
            
            if presencas_orfas > 0:
                issues.append(f"{presencas_orfas} presenças órfãs encontradas")
            
            # Verificar performance de queries principais
            slow_queries = []
            
            # Query de listagem de presenças
            query_start = time.time()
            list(PresencaDetalhada.objects.select_related('aluno', 'atividade')[:100])
            query_time = time.time() - query_start
            
            if query_time > options['threshold']:
                slow_queries.append(f"Listagem de presenças: {query_time:.3f}s")
            
            # Query de estatísticas
            query_start = time.time()
            stats = BulkPresencaOperations.otimizar_queries_estatisticas()
            query_time = time.time() - query_start
            
            if query_time > options['threshold']:
                slow_queries.append(f"Estatísticas: {query_time:.3f}s")
            
            if slow_queries:
                issues.extend(slow_queries)
            
            # Verificar tamanho do banco
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        pg_size_pretty(pg_total_relation_size('presencas_presencadetalhada')) as presencas_size,
                        pg_size_pretty(pg_database_size(current_database())) as total_size
                """)
                sizes = cursor.fetchone()
            
            duration = time.time() - start_time
            
            return {
                'status': 'healthy' if not issues else 'warning',
                'duration': duration,
                'summary': f"{total_presencas} presenças, {total_alunos} alunos",
                'details': {
                    'total_presencas': total_presencas,
                    'total_alunos': total_alunos,
                    'total_atividades': total_atividades,
                    'presencas_orfas': presencas_orfas,
                    'database_size': sizes[1] if sizes else 'N/A',
                    'presencas_table_size': sizes[0] if sizes else 'N/A',
                    'issues': issues,
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'summary': f'Erro na verificação de banco: {e}'
            }
    
    def check_cache(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """Verifica saúde do sistema de cache."""
        
        start_time = time.time()
        issues = []
        
        try:
            # Teste básico de cache
            test_key = f"health_check_{int(time.time())}"
            test_value = "test_value"
            
            # Set
            cache.set(test_key, test_value, timeout=60)
            
            # Get
            retrieved_value = cache.get(test_key)
            
            if retrieved_value != test_value:
                issues.append("Cache set/get não está funcionando")
            
            # Delete
            cache.delete(test_key)
            
            # Verificar se foi realmente deletado
            if cache.get(test_key) is not None:
                issues.append("Cache delete não está funcionando")
            
            # Verificar estatísticas de cache (se disponível)
            cache_stats = {}
            try:
                # Tentar obter stats do Redis
                if hasattr(cache, '_cache') and hasattr(cache._cache, 'get_client'):
                    client = cache._cache.get_client()
                    info = client.info()
                    cache_stats = {
                        'used_memory': info.get('used_memory_human', 'N/A'),
                        'connected_clients': info.get('connected_clients', 'N/A'),
                        'hits': info.get('keyspace_hits', 0),
                        'misses': info.get('keyspace_misses', 0),
                    }
            except Exception:
                cache_stats = {'error': 'Não foi possível obter estatísticas'}
            
            duration = time.time() - start_time
            
            return {
                'status': 'healthy' if not issues else 'warning',
                'duration': duration,
                'summary': f"Cache funcional ({duration:.3f}s)",
                'details': {
                    'issues': issues,
                    'stats': cache_stats,
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'summary': f'Erro na verificação de cache: {e}'
            }
    
    def check_celery(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """Verifica saúde do Celery."""
        
        start_time = time.time()
        issues = []
        
        try:
            # Importar Celery
            from celery import current_app
            
            # Verificar workers ativos
            inspect = current_app.control.inspect()
            
            # Stats dos workers
            stats = inspect.stats()
            active_tasks = inspect.active()
            
            if not stats:
                issues.append("Nenhum worker Celery ativo encontrado")
            else:
                worker_count = len(stats)
                total_active_tasks = sum(len(tasks) for tasks in active_tasks.values()) if active_tasks else 0
                
                # Verificar se há muitas tasks ativas
                if total_active_tasks > 50:
                    issues.append(f"Muitas tasks ativas: {total_active_tasks}")
            
            # Verificar broker (Redis)
            try:
                from celery.app.control import Inspect
                i = Inspect(app=current_app)
                broker_info = i.stats()
                
                if not broker_info:
                    issues.append("Broker (Redis) não está respondendo")
                    
            except Exception as e:
                issues.append(f"Erro ao verificar broker: {e}")
            
            duration = time.time() - start_time
            
            return {
                'status': 'healthy' if not issues else 'warning',
                'duration': duration,
                'summary': f"{len(stats) if stats else 0} workers ativos",
                'details': {
                    'workers': stats or {},
                    'active_tasks_count': total_active_tasks if 'total_active_tasks' in locals() else 0,
                    'issues': issues,
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'summary': f'Erro na verificação do Celery: {e}'
            }
    
    def check_performance(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """Verifica métricas de performance."""
        
        start_time = time.time()
        issues = []
        
        try:
            # Verificar métricas de cache
            cache_key = f"metrics_aggregated_{datetime.now().strftime('%Y%m%d_%H')}"
            metrics = cache.get(cache_key, {})
            
            if metrics:
                total_requests = metrics.get('total_requests', 0)
                slow_requests = metrics.get('slow_requests', 0)
                
                if total_requests > 0:
                    slow_percentage = (slow_requests / total_requests) * 100
                    if slow_percentage > 10:  # Mais de 10% de requests lentas
                        issues.append(f"Alto percentual de requests lentas: {slow_percentage:.1f}%")
            
            # Verificar uso de memória (se possível)
            try:
                import psutil
                memory_usage = psutil.virtual_memory().percent
                if memory_usage > 80:
                    issues.append(f"Alto uso de memória: {memory_usage:.1f}%")
            except ImportError:
                pass  # psutil não está disponível
            
            # Verificar conexões ativas do banco
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT count(*) FROM pg_stat_activity 
                    WHERE state = 'active' AND datname = current_database()
                """)
                active_connections = cursor.fetchone()[0]
                
                if active_connections > 20:
                    issues.append(f"Muitas conexões ativas: {active_connections}")
            
            duration = time.time() - start_time
            
            return {
                'status': 'healthy' if not issues else 'warning',
                'duration': duration,
                'summary': f"{len(issues)} problemas de performance",
                'details': {
                    'metrics': metrics,
                    'active_connections': active_connections,
                    'issues': issues,
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'summary': f'Erro na verificação de performance: {e}'
            }
    
    def check_security(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """Verifica aspectos de segurança."""
        
        start_time = time.time()
        issues = []
        warnings = []
        
        try:
            # Verificar configurações de segurança
            if settings.DEBUG:
                warnings.append("DEBUG está ativado")
            
            if not settings.SECRET_KEY or settings.SECRET_KEY == 'your-production-secret-key-here':
                issues.append("SECRET_KEY não está configurada adequadamente")
            
            # Verificar HTTPS settings (se aplicável)
            if not getattr(settings, 'SECURE_SSL_REDIRECT', False):
                warnings.append("SECURE_SSL_REDIRECT não está ativado")
            
            # Verificar rate limiting
            try:
                from omaum.middleware.rate_limiting import RateLimitMiddleware
                # Se chegou até aqui, middleware está configurado
            except ImportError:
                warnings.append("Middleware de rate limiting não encontrado")
            
            # Verificar usuários com senhas fracas
            weak_password_users = User.objects.filter(
                password__in=['pbkdf2_sha256$', 'admin', '123456']
            ).count()
            
            if weak_password_users > 0:
                issues.append(f"{weak_password_users} usuários com senhas fracas")
            
            # Verificar usuários superuser
            superuser_count = User.objects.filter(is_superuser=True).count()
            if superuser_count > 5:
                warnings.append(f"Muitos usuários superuser: {superuser_count}")
            
            duration = time.time() - start_time
            
            all_issues = issues + warnings
            
            return {
                'status': 'healthy' if not issues else 'warning',
                'duration': duration,
                'summary': f"{len(issues)} problemas, {len(warnings)} avisos",
                'details': {
                    'issues': issues,
                    'warnings': warnings,
                    'superuser_count': superuser_count,
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'summary': f'Erro na verificação de segurança: {e}'
            }
    
    def generate_report(self, options: Dict[str, Any], total_time: float):
        """Gera relatório final das verificações."""
        
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(
            self.style.SUCCESS(f'🏁 Verificação concluída em {total_time:.2f}s')
        )
        
        # Contar status
        healthy_count = sum(1 for r in self.results.values() if r.get('status') == 'healthy')
        warning_count = sum(1 for r in self.results.values() if r.get('status') == 'warning')
        error_count = sum(1 for r in self.results.values() if r.get('status') == 'error')
        
        self.stdout.write(f'\n📊 Resumo:')
        self.stdout.write(f'  ✅ Saudável: {healthy_count}')
        self.stdout.write(f'  ⚠️  Avisos: {warning_count}')
        self.stdout.write(f'  ❌ Erros: {error_count}')
        
        # Output detalhado se solicitado
        if options['verbose'] or options['format'] != 'summary':
            self.stdout.write('\n📋 Detalhes:')
            
            for check_name, result in self.results.items():
                self.stdout.write(f'\n🔍 {check_name.upper()}:')
                
                if 'details' in result:
                    for key, value in result['details'].items():
                        self.stdout.write(f'  {key}: {value}')
        
        # Status geral do sistema
        overall_status = 'healthy'
        if error_count > 0:
            overall_status = 'error'
        elif warning_count > 0:
            overall_status = 'warning'
        
        status_icon = {'healthy': '✅', 'warning': '⚠️', 'error': '❌'}[overall_status]
        self.stdout.write(f'\n{status_icon} Status Geral: {overall_status.upper()}')
