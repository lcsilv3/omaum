from .base import *  # noqa

# Configurações específicas de desenvolvimento

# Adicione IPs de ferramentas de desenvolvimento se necessário
INTERNAL_IPS += ["127.0.0.1"]

ENVIRONMENT_LABEL = "Ambiente de Desenvolvimento"
ENVIRONMENT_BADGE_CLASSES = "bg-warning text-dark"
ENVIRONMENT_HINT = "Use credenciais de testes (contas DEV)."
