"""
FASE 3C: Configuração Celery para Background Tasks
"""

import os
from celery import Celery

# Configurar Django settings para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')

app = Celery('omaum')

# Usar Django settings para configuração do Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks de todos os apps registrados
app.autodiscover_tasks()

# Configurações específicas para produção
app.conf.update(
    # Broker e Result Backend
    broker_url=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    result_backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
    
    # Serialização
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Sao_Paulo',
    enable_utc=True,
    
    # Performance
    task_compression='gzip',
    result_compression='gzip',
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_disable_rate_limits=False,
    
    # Retry policy
    task_default_retry_delay=60,
    task_max_retry_delay=3600,
    
    # Task routing
    task_routes={
        'presencas.tasks.processar_exportacao_pesada': {'queue': 'heavy'},
        'presencas.tasks.recalcular_estatisticas': {'queue': 'statistics'},
        'presencas.tasks.enviar_relatorio_email': {'queue': 'email'},
    },
    
    # Queues
    task_default_queue='default',
    
    # Worker settings
    worker_max_tasks_per_child=1000,
    worker_max_memory_per_child=200000,  # 200MB
    
    # Beat schedule (agendamentos)
    beat_schedule={
        'limpar-cache-estatisticas': {
            'task': 'presencas.tasks.limpar_cache_antigo',
            'schedule': 3600.0,  # A cada hora
        },
        'backup-dados-criticos': {
            'task': 'presencas.tasks.backup_dados_criticos',
            'schedule': 86400.0,  # Diário
        },
    },
)


@app.task(bind=True)
def debug_task(self):
    """Task de debug para testar configuração."""
    print(f'Request: {self.request!r}')
