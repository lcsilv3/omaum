# Suite de Testes de Integração - Sistema de Presenças

## Visão Geral

Esta suite de testes de integração valida fluxos completos end-to-end do sistema de presenças, cobrindo:

- **User Stories reais**
- **Fluxos de trabalho completos**
- **Performance e carga**
- **Compatibilidade e regressão**
- **Interações JavaScript/Browser**

## Estrutura dos Testes

### 1. test_integration.py
**Testes de integração principal**
- Fluxos completos de registro de presenças
- Visualização consolidada
- Exportação de relatórios
- Painel de estatísticas
- APIs AJAX
- Navegação entre páginas
- Workflows de professor e coordenador
- Testes transacionais

### 2. test_user_stories.py
**Testes baseados em casos de uso reais**
- Professor registrando presenças diárias
- Coordenador fazendo análise semanal/mensal
- Interface Excel-like para usuários avançados
- Regras de negócio e validações
- Compatibilidade com sistema legado
- Cenários de performance com dados reais

### 3. test_performance.py
**Testes de performance e otimização**
- Otimização de queries (N+1, select_related, prefetch_related)
- Testes de carga com grandes volumes
- Benchmarks de tempo de resposta
- Cache e invalidação
- Uso de memória
- Turmas com 100+ alunos
- Histórico de 1+ ano

### 4. test_browser.py
**Testes de interface JavaScript**
- Interações mouse/teclado (Selenium)
- Edição inline tipo Excel
- Navegação com setas
- AJAX em tempo real
- Responsividade
- Acessibilidade
- Feedback visual

### 5. test_compatibility.py
**Testes de compatibilidade e migração**
- Compatibilidade com modelos legados
- Migração de dados antigos
- Testes de regressão
- URLs e routing legados
- Templates e CSS
- Integridade de banco

## Como Executar

### Executar Todos os Testes
```bash
# Executar toda a suite de integração
python manage.py test presencas.tests.test_integration
python manage.py test presencas.tests.test_user_stories
python manage.py test presencas.tests.test_performance
python manage.py test presencas.tests.test_browser
python manage.py test presencas.tests.test_compatibility

# Ou todos de uma vez
python manage.py test presencas.tests --pattern="test_*.py"
```

### Executar Testes Específicos
```bash
# Apenas fluxos de registro
python manage.py test presencas.tests.test_integration.RegistroPresencaFluxoCompletoTest

# Apenas user stories de professor
python manage.py test presencas.tests.test_user_stories.ProfessorDiarioUserStoryTest

# Apenas testes de performance
python manage.py test presencas.tests.test_performance.QueryOptimizationTest
```

### Executar com Cobertura
```bash
# Instalar coverage se necessário
pip install coverage

# Executar com cobertura
coverage run --source='presencas' manage.py test presencas.tests
coverage report
coverage html
```

## Requisitos

### Dependências Base
- Django TestCase/TransactionTestCase
- Python unittest.mock
- Django Client para requisições HTTP

### Dependências Opcionais
- **Selenium** (para testes de browser)
- **Coverage** (para relatórios de cobertura)
- **Chrome/ChromeDriver** (para Selenium)

### Instalação de Dependências Opcionais
```bash
# Para testes de browser
pip install selenium
# Download ChromeDriver: https://chromedriver.chromium.org/

# Para cobertura
pip install coverage

# Para relatórios avançados
pip install django-coverage-plugin
```

## Configuração

### Settings para Testes
```python
# settings/test.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Desabilitar migrations desnecessárias para velocidade
MIGRATION_MODULES = {
    'presencas': None,
    'alunos': None,
    'turmas': None,
    'atividades': None,
}
```

### Variáveis de Ambiente
```bash
# Para testes Selenium
export SELENIUM_HEADLESS=true
export CHROME_DRIVER_PATH=/path/to/chromedriver

# Para testes de performance
export RUN_SLOW_TESTS=true
export TEST_DATABASE_NAME=test_performance_db
```

## Cenários de Dados

### Dados Base (todos os testes)
- 1 usuário professor
- 1 usuário coordenador
- 2 turmas (Iniciação, Avançada)
- 4 tipos de atividades (Ritual, Aula, Prática, Evento)
- 5-8 alunos por turma

### Dados de Performance
- Turmas com 100+ alunos
- Histórico de 365 dias
- 10.000+ registros de presença

### Dados de User Stories
- Padrões realistas de frequência
- Alunos com diferentes perfis (exemplar, problemático, melhorando, piorando)
- Cenários de justificativas variadas

## Relatórios

### Métricas de Sucesso
- **Cobertura**: > 90% do código de presenças
- **Performance**: Páginas < 3s, APIs < 500ms
- **Compatibilidade**: 100% funcionalidades legadas
- **User Stories**: Todos os fluxos principais

### Relatórios Gerados
```bash
# Relatório de cobertura HTML
coverage html
# Abre htmlcov/index.html

# Relatório de performance
python -m pytest presencas/tests/test_performance.py --benchmark-only

# Log de queries (DEBUG=True)
python manage.py test presencas.tests.test_performance --debug-mode
```

## Integração Contínua

### GitHub Actions / CI
```yaml
name: Testes de Integração
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install coverage selenium
    
    - name: Setup Chrome
      uses: browser-actions/setup-chrome@latest
    
    - name: Run integration tests
      run: |
        coverage run manage.py test presencas.tests
        coverage report --fail-under=85
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

## Troubleshooting

### Problemas Comuns

1. **Selenium não encontra ChromeDriver**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install chromium-chromedriver
   
   # macOS
   brew install chromedriver
   
   # Windows - download manual
   ```

2. **Testes de performance lentos**
   ```bash
   # Usar banco em memória
   export TEST_DATABASE_ENGINE=sqlite3
   export TEST_DATABASE_NAME=:memory:
   
   # Desabilitar logging
   export DJANGO_LOG_LEVEL=ERROR
   ```

3. **Falhas em testes AJAX**
   ```python
   # Verificar se view tem decorator @csrf_exempt ou
   # cliente tem CSRF token correto
   from django.test import Client
   client = Client(enforce_csrf_checks=False)
   ```

### Debug

```python
# Adicionar debug em testes
import pdb; pdb.set_trace()

# Ver queries executadas
from django.db import connection
print(connection.queries)

# Timing detalhado
import time
start = time.time()
# ... código do teste
print(f"Tempo: {time.time() - start}s")
```

## Manutenção

### Atualizações Regulares
- Revisar cenários quando funcionalidades mudam
- Atualizar dados de teste com padrões reais
- Validar performance com volume crescente
- Manter compatibilidade com versões Django

### Monitoramento
- Executar suite completa semanalmente
- Monitorar tempo de execução dos testes
- Validar cobertura não diminui
- Verificar compatibilidade com browsers

---

**Nota**: Esta suite foi desenvolvida para validar o sistema completo de presenças em cenários reais de uso. Para dúvidas ou melhorias, consulte a documentação do projeto principal.
