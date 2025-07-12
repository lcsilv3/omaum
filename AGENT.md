# AGENT.md - Sistema OMAUM

Este arquivo contém informações importantes para agentes de IA e desenvolvedores sobre o Sistema OMAUM.

## Comandos Importantes

### Desenvolvimento
```bash
# Ativar ambiente virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Executar servidor de desenvolvimento
python manage.py runserver

# Executar testes
python manage.py test
python manage.py test presencas  # Apenas módulo de presenças

# Migrações
python manage.py makemigrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Linting e qualidade de código
python scripts/lint.py
black .
isort .
flake8 .

# Coverage de testes
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Produção
```bash
# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Verificar configuração para produção
python manage.py check --deploy

# Backup de dados
python manage.py dumpdata > backup.json

# Restaurar dados
python manage.py loaddata backup.json
```

## Estrutura do Projeto

### Módulos Principais
- **presencas/**: Sistema completo de controle de frequência ⭐ (FOCO PRINCIPAL)
- **alunos/**: Gestão de estudantes
- **turmas/**: Organização de turmas e períodos
- **atividades/**: Controle de atividades acadêmicas/ritualísticas
- **cursos/**: Estrutura de cursos oferecidos
- **core/**: Utilitários e configurações comuns

### Sistema de Presenças (Módulo Principal)
```
presencas/
├── models.py              # Modelos: Presenca, PresencaDetalhada, ConfiguracaoPresenca
├── views/                 # Views organizadas por funcionalidade
│   ├── consolidado.py     # Relatórios consolidados
│   ├── painel.py          # Dashboard estatísticas
│   ├── registro_rapido.py # Interface otimizada
│   └── exportacao_simplificada.py # Exportações avançadas
├── api/                   # API REST endpoints
├── services/              # Lógica de negócio
├── templates/             # Templates HTML
└── tests/                 # Testes automatizados
```

## Padrões de Código

### Nomenclatura
- **Modelos**: PascalCase (ex: `PresencaDetalhada`)
- **Views**: PascalCase + "View" (ex: `RegistrarPresencaView`)
- **Funções**: snake_case (ex: `calcular_carencias`)
- **URLs**: snake_case com hífens (ex: `registro-rapido`)
- **Parâmetros URL**: `modelo_id` (ex: `turma_id`, `aluno_id`)

### Docstrings Obrigatórias
```python
def calcular_estatisticas(turma_id, periodo):
    """
    Calcula estatísticas de presença para uma turma.
    
    Args:
        turma_id (int): ID da turma
        periodo (str): Período no formato 'YYYY-MM'
        
    Returns:
        dict: Estatísticas calculadas
        
    Raises:
        ValidationError: Se dados forem inválidos
    """
```

### Validações Multi-camadas
1. **Frontend**: Validação JavaScript em tempo real
2. **Forms**: Validação Django forms
3. **Models**: Método `clean()` para regras de negócio
4. **Services**: Validações complexas de negócio

## Configurações Importantes

### Banco de Dados
- **Desenvolvimento**: SQLite (`db.sqlite3`)
- **Produção**: PostgreSQL (recomendado)

### Cache
- **Desenvolvimento**: Memória local
- **Produção**: Redis (recomendado)

### Arquivos Estáticos
- **Desenvolvimento**: Django dev server
- **Produção**: Nginx para servir estáticos

### Logs
- **Localização**: `logs/` directory
- **Níveis**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Módulos principais**: `presencas`, `django.db.backends`

## Features Implementadas (v2.0)

### ✅ Sistema de Presenças
- [x] Registro Multi-etapas (5 etapas guiadas)
- [x] Registro Rápido (interface AJAX otimizada)
- [x] Cálculos automáticos (percentuais, carências)
- [x] Configurações flexíveis por turma/atividade
- [x] Validações robustas em múltiplas camadas

### ✅ Relatórios e Análises
- [x] Painel de Estatísticas (gráficos Chart.js)
- [x] Exportação avançada (Excel, PDF, CSV)
- [x] Agendamento automático de relatórios
- [x] Relatórios consolidados por período/turma

### ✅ API REST
- [x] Endpoints documentados (Swagger/ReDoc)
- [x] Autenticação por token
- [x] Rate limiting
- [x] Versionamento de API

### ✅ Performance
- [x] Queries otimizadas (select_related/prefetch_related)
- [x] Cache estratégico
- [x] Paginação eficiente
- [x] Processamento em lote

## Testes

### Estrutura de Testes
```
tests/
├── test_models.py         # Testes de modelos
├── test_views.py          # Testes de views
├── test_api.py            # Testes de API
├── test_services.py       # Testes de serviços
└── factories.py           # Factory Boy para fixtures
```

### Cobertura Atual
- **Modelos**: 90%+
- **Views**: 80%+
- **API**: 85%+
- **Services**: 75%+

### Executar Testes Específicos
```bash
# Por módulo
python manage.py test presencas

# Por arquivo
python manage.py test presencas.tests.test_models

# Por classe
python manage.py test presencas.tests.test_models.PresencaDetalhadaTestCase

# Por método
python manage.py test presencas.tests.test_models.PresencaDetalhadaTestCase.test_calculo_percentual
```

## Debugging

### Django Debug Toolbar
- **URL**: `/__debug__/` (apenas em DEBUG=True)
- **Funcionalidades**: SQL queries, cache hits, templates

### Logs Importantes
```python
import logging
logger = logging.getLogger(__name__)

# Usar em código
logger.debug("Debug info")
logger.info("Informação")
logger.warning("Aviso")
logger.error("Erro")
logger.critical("Crítico")
```

### Breakpoints
```python
# Python 3.7+
breakpoint()

# Ou tradicional
import pdb; pdb.set_trace()
```

## Troubleshooting Comum

### Erro: "No module named 'django'"
```bash
# Verificar se ambiente virtual está ativo
which python  # Linux/Mac
where python  # Windows

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstalar dependências se necessário
pip install -r requirements.txt
```

### Erro de Migração
```bash
# Reset completo (CUIDADO! Perde dados)
rm db.sqlite3
rm -rf */migrations/__pycache__
python manage.py makemigrations
python manage.py migrate

# Ou reverter migração específica
python manage.py migrate presencas 0001
```

### Performance Lenta
```bash
# Habilitar debug de SQL
# settings.py
LOGGING['loggers']['django.db.backends'] = {
    'level': 'DEBUG',
    'handlers': ['console'],
}

# Usar Django Debug Toolbar
pip install django-debug-toolbar
```

## Links Úteis

### Documentação
- [Manual do Usuário](docs/MANUAL_USUARIO.md)
- [Arquitetura](docs/ARQUITETURA_PRESENCAS.md)
- [API Documentation](docs/API_DOCUMENTATION.md)
- [Guia Desenvolvedor](docs/GUIA_DESENVOLVEDOR.md)

### Ferramentas
- **Admin Django**: `/admin/`
- **API Docs**: `/api/docs/` (se configurado)
- **Debug Toolbar**: `/__debug__/`

### Repositório
- **GitHub**: https://github.com/lcsilv3/omaum
- **Issues**: https://github.com/lcsilv3/omaum/issues
- **Wiki**: https://github.com/lcsilv3/omaum/wiki

## Convenções Git

### Branches
- `main`: Produção estável
- `develop`: Desenvolvimento ativo
- `feature/nome-feature`: Novas funcionalidades
- `hotfix/nome-bug`: Correções urgentes

### Commits
```bash
feat: adicionar nova funcionalidade
fix: corrigir bug específico
docs: atualizar documentação
style: formatação de código
refactor: refatoração sem mudança de comportamento
test: adicionar ou corrigir testes
chore: tarefas de manutenção
```

## Contatos

- **Email Suporte**: suporte@omaum.edu.br
- **Email Dev**: dev@omaum.edu.br
- **GitHub Issues**: Para bugs e features
- **Slack**: #dev-omaum (se aplicável)

---

*Última atualização: Janeiro 2024*
*Versão do sistema: 2.0.0*
