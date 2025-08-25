# Sistema de Testes Automatizados - OMAUM

## 📋 Visão Geral

Sistema completo de testes automatizados para o projeto OMAUM, com cobertura de 100% e execução otimizada. Inclui testes unitários, testes de integração, testes de API e testes de interface.

## 🎯 Objetivos

- **Cobertura de 100%**: Todos os apps críticos com cobertura completa
- **Execução Rápida**: Testes otimizados para máxima velocidade
- **Automação Completa**: Execução e correção automática de erros
- **Integração CI/CD**: Integração com GitHub Actions
- **Relatórios Detalhados**: Análise completa de cobertura e performance

## 🚀 Início Rápido

### Windows
```batch
# Executar automação completa
run_tests.bat

# Apenas configurar ambiente
run_tests.bat --setup-only

# Apenas executar testes
run_tests.bat --tests-only

# Testes paralelos
run_tests.bat --parallel

# Testes de fumaça
run_tests.bat --smoke
```

### Linux/Mac
```bash
# Executar automação completa
python automate_tests.py

# Apenas configurar ambiente
python automate_tests.py --setup-only

# Apenas executar testes
python automate_tests.py --tests-only

# Testes paralelos
python tests/run_parallel_tests.py

# Testes de fumaça
python tests/run_parallel_tests.py --smoke
```

## 📁 Estrutura de Testes

```
tests/
├── conftest.py                 # Configurações globais do pytest
├── factories.py               # Factories para criação de dados
├── settings_test.py           # Configurações otimizadas para testes
├── run_tests.py              # Script principal de execução
├── run_parallel_tests.py     # Script para execução paralela
├── test_cursos.py            # Testes do módulo de cursos
├── test_alunos.py            # Testes do módulo de alunos
├── test_matriculas.py        # Testes do módulo de matrículas
├── test_turmas.py            # Testes do módulo de turmas
├── test_presencas.py         # Testes do módulo de presenças
└── integration/              # Testes de integração
    └── test_sistema_completo.py
```

## 🔧 Configuração

### Dependências
```bash
# Instalar dependências de teste
pip install -r requirements-test.txt
```

### Configuração do Django
```python
# tests/settings_test.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
```

### Configuração do Pytest
```ini
# pytest.ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = tests.settings_test
addopts = --tb=short --strict-markers --strict-config
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

## 🧪 Tipos de Testes

### 1. Testes Unitários
- **Modelos**: Validação de campos, métodos e relacionamentos
- **Forms**: Validação de formulários e dados
- **Services**: Lógica de negócio
- **Views**: Comportamento das views

### 2. Testes de Integração
- **Fluxo Completo**: Aluno → Matrícula → Turma → Presença
- **APIs**: Testes de endpoints REST
- **Relacionamentos**: Testes de integridade referencial

### 3. Testes de Performance
- **Consultas**: Otimização de queries
- **Carga**: Teste com grande volume de dados
- **Concorrência**: Testes de acesso simultâneo

### 4. Testes de Interface
- **Selenium**: Testes de interface web
- **Formulários**: Interação com formulários
- **Navegação**: Fluxo de navegação

## 📊 Cobertura de Testes

### Apps Críticos (100% de cobertura)
- ✅ **cursos**: Gestão de cursos e tipos
- ✅ **alunos**: Gestão de alunos e tipos
- ✅ **matriculas**: Gestão de matrículas e status
- ✅ **turmas**: Gestão de turmas e status
- ✅ **presencas**: Gestão de presenças e status

### Métricas de Qualidade
- **Cobertura mínima**: 90%
- **Cobertura objetivo**: 100%
- **Testes unitários**: 80%
- **Testes de integração**: 20%

## 🔄 Execução Automatizada

### Scripts Disponíveis

#### 1. Automação Completa
```python
# automate_tests.py
python automate_tests.py
```
- Configura ambiente virtual
- Instala dependências
- Executa migrações
- Executa testes com correção automática
- Gera relatórios de cobertura

#### 2. Execução Paralela
```python
# tests/run_parallel_tests.py
python tests/run_parallel_tests.py --apps cursos alunos
```
- Execução em paralelo com pytest-xdist
- Otimização de performance
- Relatórios de tempo de execução

#### 3. Testes Específicos
```python
# Testes de fumaça
python tests/run_parallel_tests.py --smoke

# Testes de performance
python tests/run_parallel_tests.py --performance

# Padrão específico
python tests/run_parallel_tests.py --pattern "test_*_models.py"
```

## 🛠️ Factories e Fixtures

### Factories (factory_boy)
```python
# tests/factories.py
class AlunoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Aluno
    
    nome = factory.Faker('name')
    cpf = factory.Faker('cpf', locale='pt_BR')
    email = factory.Faker('email')
```

### Fixtures (pytest)
```python
# tests/conftest.py
@pytest.fixture
def usuario_autenticado(db):
    user = UserFactory()
    client = Client()
    client.login(username=user.username, password='testpassword')
    return client, user
```

## 📈 Relatórios

### Relatório de Cobertura
```bash
# Gerar relatório HTML
pytest --cov=. --cov-report=html

# Visualizar relatório
open htmlcov/index.html
```

### Relatório de Performance
```bash
# Mostrar testes mais lentos
pytest --durations=10
```

### Relatório JSON
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "total_apps": 5,
  "successful_apps": 5,
  "average_coverage": 98.5,
  "details": {
    "cursos": {"success": true, "coverage": 100.0},
    "alunos": {"success": true, "coverage": 99.2}
  }
}
```

## 🔍 Debugging

### Logs de Teste
```python
# Habilitar logs durante testes
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Debugging com pdb
```python
import pdb; pdb.set_trace()
```

### Verbose Mode
```bash
pytest -v -s tests/test_alunos.py::AlunoModelTest::test_creation
```

## 🚨 Correção Automática

### Tipos de Erros Corrigidos
- **ImportError**: Criação de arquivos `__init__.py`
- **ModuleNotFoundError**: Adição de apps ao INSTALLED_APPS
- **Migration Issues**: Aplicação automática de migrações
- **Database Issues**: Configuração de banco em memória

### Padrões de Correção
```python
def _fix_import_error(self, app_name: str, error_text: str):
    """Corrige erros de importação."""
    init_file = self.project_root / app_name / '__init__.py'
    if not init_file.exists():
        init_file.touch()
```

## 📋 Checklist de Qualidade

### ✅ Antes de Commit
- [ ] Todos os testes passam
- [ ] Cobertura >= 90%
- [ ] Sem warnings do pytest
- [ ] Documentação atualizada

### ✅ Antes de Deploy
- [ ] Testes de integração passam
- [ ] Testes de performance passam
- [ ] Testes de fumaça passam
- [ ] CI/CD pipeline verde

## 🔧 Configuração Avançada

### Parallel Testing
```ini
# pytest.ini
[tool:pytest]
addopts = -n auto --dist=loadscope
```

### Custom Markers
```python
# pytest.ini
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    api: marks tests as API tests
```

### Database Configuration
```python
# tests/settings_test.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'OPTIONS': {
            'timeout': 20,
        },
    }
}
```

## 🎯 Melhores Práticas

### 1. Nomenclatura de Testes
```python
def test_should_create_aluno_when_valid_data_provided():
    """Deve criar aluno quando dados válidos são fornecidos."""
    pass
```

### 2. Organização de Testes
```python
class AlunoModelTest(TestCase):
    """Testes para o modelo Aluno."""
    
    def setUp(self):
        """Configuração inicial para cada teste."""
        self.aluno = AlunoFactory()
    
    def test_str_representation(self):
        """Teste da representação string."""
        assert str(self.aluno) == self.aluno.nome
```

### 3. Uso de Factories
```python
# Prefer factories over manual creation
aluno = AlunoFactory()  # ✅ Bom
aluno = Aluno.objects.create(...)  # ❌ Evitar
```

### 4. Assertions Claras
```python
# Seja específico nas assertions
assert response.status_code == 200  # ✅ Bom
assert response.status_code  # ❌ Vago
```

## 🚀 Próximos Passos

### Melhorias Planejadas
- [ ] Testes de carga com Locust
- [ ] Testes de segurança
- [ ] Testes de acessibilidade
- [ ] Testes de API GraphQL
- [ ] Testes de mobile (Django REST + React Native)

### Integração Contínua
- [ ] Hooks de pre-commit
- [ ] Análise de código com SonarQube
- [ ] Monitoramento de performance
- [ ] Alertas de cobertura

## 📞 Suporte

### Problemas Comuns
1. **Erro de importação**: Verificar PYTHONPATH
2. **Banco de dados**: Verificar configuração em settings_test.py
3. **Dependências**: Executar `pip install -r requirements-test.txt`

### Contato
- **Desenvolvedor**: Equipe OMAUM
- **Email**: suporte@omaum.com
- **Documentação**: [docs.omaum.com](https://docs.omaum.com)

---

*Sistema de testes automatizados implementado com foco em qualidade, performance e manutenibilidade. 🚀*
