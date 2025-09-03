"""
FASE 3C: Configurações específicas para monitoramento e métricas.
"""

# Configurações de monitoramento
MONITORING_SETTINGS = {
    # Thresholds de performance
    "SLOW_QUERY_THRESHOLD": 1.0,  # segundos
    "SLOW_REQUEST_THRESHOLD": 2.0,  # segundos
    "HIGH_MEMORY_THRESHOLD": 80,  # porcentagem
    "MAX_DB_CONNECTIONS": 50,
    # Cache settings
    "METRICS_CACHE_TIMEOUT": 300,  # 5 minutos
    "CACHE_HIT_RATE_THRESHOLD": 80,  # porcentagem
    # Rate limiting
    "DEFAULT_RATE_LIMIT": 60,  # requests por minuto
    "API_RATE_LIMIT": 30,  # requests por minuto para APIs
    "BURST_LIMIT": 10,  # requests em 10 segundos
    # Alertas
    "ALERT_EMAIL": "admin@omaum.com",
    "SLACK_WEBHOOK": None,
    # Health check
    "HEALTH_CHECK_INTERVAL": 300,  # 5 minutos
    "CRITICAL_SERVICES": ["database", "cache", "celery"],
}

# Configurações do Celery para produção
CELERY_PRODUCTION_SETTINGS = {
    "task_serializer": "json",
    "accept_content": ["json"],
    "result_serializer": "json",
    "timezone": "America/Sao_Paulo",
    "enable_utc": True,
    # Performance
    "worker_prefetch_multiplier": 4,
    "worker_max_tasks_per_child": 1000,
    "worker_max_memory_per_child": 200000,  # 200MB
    # Queues
    "task_routes": {
        "presencas.tasks.processar_exportacao_pesada": {"queue": "heavy"},
        "presencas.tasks.recalcular_estatisticas": {"queue": "statistics"},
        "presencas.tasks.enviar_relatorio_email": {"queue": "email"},
        "presencas.tasks.processar_bulk_presencas": {"queue": "bulk"},
    },
    # Beat schedule
    "beat_schedule": {
        "limpar-cache-antigo": {
            "task": "presencas.tasks.limpar_cache_antigo",
            "schedule": 3600.0,  # 1 hora
        },
        "backup-dados-criticos": {
            "task": "presencas.tasks.backup_dados_criticos",
            "schedule": 21600.0,  # 6 horas
        },
    },
}

# Configurações de logging estruturado
LOGGING_STRUCTURED_SETTINGS = {
    "formatters": {
        "json": {
            "format": (
                '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
                '"logger": "%(name)s", "message": "%(message)s"}'
            ),
        },
        "structured": {
            "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        },
    },
    "log_retention": {
        "general": 30,  # dias
        "performance": 14,  # dias
        "security": 90,  # dias
        "errors": 90,  # dias
    },
    "log_rotation": {
        "max_bytes": 1024 * 1024 * 15,  # 15MB
        "backup_count": 10,
    },
}

# Configurações de segurança avançada
SECURITY_ADVANCED_SETTINGS = {
    # Rate limiting por endpoint
    "endpoint_limits": {
        "/api/presencas/": {"rpm": 30, "burst": 5},
        "/api/exportacao/": {"rpm": 5, "burst": 2},
        "/api/estatisticas/": {"rpm": 20, "burst": 3},
        "/admin/": {"rpm": 10, "burst": 2},
    },
    # Padrões suspeitos
    "suspicious_patterns": [
        "union select",
        "drop table",
        "delete from",
        "../",
        "script>",
        "javascript:",
    ],
    # IPs bloqueados (exemplo)
    "blocked_ips": [
        # Adicionar IPs problemáticos aqui
    ],
    # Headers de segurança
    "security_headers": {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    },
}

# Configurações de cache otimizado
CACHE_OPTIMIZATION_SETTINGS = {
    # Timeouts por tipo de cache
    "timeouts": {
        "presencas_listagem": 300,  # 5 minutos
        "estatisticas": 900,  # 15 minutos
        "turmas_listagem": 3600,  # 1 hora
        "atividades_listagem": 1800,  # 30 minutos
        "user_sessions": 3600,  # 1 hora
    },
    # Patterns de invalidação
    "invalidation_patterns": {
        "presenca_created": ["presencas_*", "estatisticas_*"],
        "presenca_updated": ["presencas_*", "estatisticas_*"],
        "aluno_created": ["alunos_*", "turmas_*"],
        "atividade_created": ["atividades_*", "estatisticas_*"],
    },
    # Compressão
    "compression": {
        "enabled": True,
        "level": 6,  # Balanço entre velocidade e tamanho
    },
}

# Configurações de banco de dados otimizado
DATABASE_OPTIMIZATION_SETTINGS = {
    # Connection pooling
    "connection_pool": {
        "max_connections": 20,
        "max_overflow": 10,
        "pool_timeout": 30,
        "pool_recycle": 3600,
    },
    # Query optimization
    "query_optimization": {
        "enable_select_related": True,
        "enable_prefetch_related": True,
        "max_query_time_warning": 1.0,
    },
    # Índices a criar
    "indexes_to_create": [
        "idx_presenca_periodo_turma",
        "idx_presenca_aluno_periodo",
        "idx_presenca_atividade_presente",
        "idx_presenca_curso_periodo",
        "idx_presenca_export",
        "idx_aluno_turma_nome",
        "idx_atividade_curso_data",
    ],
}
