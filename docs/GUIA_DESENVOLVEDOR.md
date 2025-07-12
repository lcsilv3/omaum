# Guia do Desenvolvedor - Sistema OMAUM

## Índice
1. [Estrutura do Projeto](#estrutura-do-projeto)
2. [Padrões de Desenvolvimento](#padrões-de-desenvolvimento)
3. [Configuração do Ambiente](#configuração-do-ambiente)
4. [Como Contribuir](#como-contribuir)
5. [Testes e QA](#testes-e-qa)
6. [Deploy e CI/CD](#deploy-e-cicd)
7. [Debugging](#debugging)
8. [Performance](#performance)

## Estrutura do Projeto

### Visão Geral
```
omaum/
├── docs/                    # Documentação
├── omaum/                   # Configurações do Django
│   ├── settings/            # Settings modulares
│   ├── urls.py             # URLs principais
│   └── wsgi.py             # WSGI config
├── apps/                    # Aplicações Django
│   ├── alunos/             # Gestão de alunos
│   ├── atividades/         # Tipos de atividades
│   ├── cursos/             # Cursos oferecidos
│   ├── presencas/          # Sistema de presenças ⭐
│   ├── turmas/             # Gestão de turmas
│   └── core/               # Utilitários comuns
├── static/                 # Arquivos estáticos
├── media/                  # Arquivos de mídia
├── templates/              # Templates base
├── tests/                  # Testes globais
├── scripts/                # Scripts auxiliares
├── requirements/           # Dependências
└── manage.py              # CLI do Django
```

### Aplicação Presenças (Foco Principal)
```
presencas/
├── models.py              # Modelos de dados
├── views/                 # Views organizadas por funcionalidade
│   ├── __init__.py
│   ├── consolidado.py     # Relatórios consolidados
│   ├── painel.py          # Painel de estatísticas
│   ├── registro_rapido.py # Interface otimizada
│   └── exportacao_simplificada.py
├── views_ext/             # Views multi-etapas
│   ├── registro_presenca.py
│   ├── listagem.py
│   └── multiplas.py
├── api/                   # API REST
│   ├── views.py          # Endpoints da API
│   ├── serializers.py    # Serializers DRF
│   └── urls.py           # URLs da API
├── services/              # Lógica de negócio
│   ├── __init__.py
│   ├── calculadora_estatisticas.py
│   ├── exportacao_service.py
│   └── presenca_service.py
├── templates/             # Templates HTML
├── static/               # CSS/JS específicos
├── tests/                # Testes da aplicação
├── management/           # Comandos customizados
├── migrations/           # Migrações do banco
└── templatetags/         # Template tags customizadas
```

## Padrões de Desenvolvimento

### 1. Arquitetura em Camadas

```python
# Estrutura recomendada para uma feature

# models.py - Camada de Dados
class Presenca(models.Model):
    """Modelo de dados com validações básicas"""
    
# services/presenca_service.py - Camada de Negócio
class PresencaService:
    """Regras de negócio complexas"""
    
    @staticmethod
    def calcular_carencias(presenca_detalhada):
        """Lógica específica de cálculo"""
        
# repositories.py - Camada de Acesso a Dados
class PresencaRepository:
    """Consultas otimizadas"""
    
    @staticmethod
    def buscar_por_periodo(turma, periodo):
        """Query específica e otimizada"""
        
# views.py - Camada de Apresentação
class PresencaView:
    """Orquestração e apresentação"""
    
    def post(self, request):
        # Usar service para lógica de negócio
        service = PresencaService()
        resultado = service.processar_presencas(dados)
```

### 2. Convenções de Nomenclatura

#### Modelos
```python
class PresencaDetalhada(models.Model):  # PascalCase
    """Docstring obrigatória explicando o propósito"""
    
    # Campos descritivos
    percentual_presenca = models.DecimalField(  # snake_case
        max_digits=5,
        decimal_places=2,
        verbose_name="Percentual de Presença",  # Nome amigável
        help_text="Calculado automaticamente"    # Ajuda contextual
    )
```

#### Views
```python
class RegistrarPresencaView(View):              # PascalCase + View
    """View para registro de presenças"""
    
    def get(self, request, turma_id):           # snake_case para métodos
        """Exibe formulário de registro"""
        
    def post(self, request, turma_id):
        """Processa dados do formulário"""

def listar_presencas_academicas(request):      # snake_case para functions
    """Lista presenças de atividades acadêmicas"""
```

#### URLs
```python
urlpatterns = [
    # snake_case com hífens
    path('registrar-presenca/', views.registrar, name='registrar_presenca'),
    path('consolidado/', views.consolidado, name='consolidado_presencas'),
    
    # IDs explícitos
    path('editar/<int:presenca_id>/', views.editar, name='editar_presenca'),
    path('turma/<int:turma_id>/alunos/', views.alunos, name='alunos_turma'),
]
```

### 3. Validação de Dados

#### No Modelo
```python
class PresencaDetalhada(models.Model):
    def clean(self):
        """Validações de negócio"""
        super().clean()
        
        # Validação customizada
        if self.presencas + self.faltas > self.convocacoes:
            raise ValidationError(
                "Presenças + Faltas não podem superar Convocações"
            )
    
    def save(self, *args, **kwargs):
        """Executa validações e cálculos"""
        self.full_clean()  # Executa validações
        
        # Cálculos automáticos
        self.percentual_presenca = self.calcular_percentual()
        self.carencias = self.calcular_carencias()
        
        super().save(*args, **kwargs)
```

#### No Formulário
```python
class PresencaForm(forms.ModelForm):
    class Meta:
        model = Presenca
        fields = ['aluno', 'data', 'presente', 'justificativa']
        
    def clean(self):
        """Validações no formulário"""
        cleaned_data = super().clean()
        
        presente = cleaned_data.get('presente')
        justificativa = cleaned_data.get('justificativa')
        
        if not presente and not justificativa:
            raise forms.ValidationError(
                "Justificativa é obrigatória para ausências"
            )
        
        return cleaned_data
```

### 4. Tratamento de Erros

```python
import logging

logger = logging.getLogger(__name__)

class PresencaService:
    @staticmethod
    def processar_presencas_lote(dados):
        """Processa presenças em lote com tratamento de erro"""
        
        resultados = {
            'processadas': 0,
            'erros': [],
            'sucessos': []
        }
        
        for item in dados:
            try:
                presenca = Presenca.objects.create(**item)
                resultados['sucessos'].append(presenca.id)
                resultados['processadas'] += 1
                
            except ValidationError as e:
                logger.warning(f"Erro de validação: {e}")
                resultados['erros'].append({
                    'item': item,
                    'erro': str(e)
                })
                
            except Exception as e:
                logger.error(f"Erro inesperado: {e}")
                resultados['erros'].append({
                    'item': item,
                    'erro': 'Erro interno do sistema'
                })
        
        return resultados
```

### 5. Documentação de Código

```python
class CalculadoraEstatisticas:
    """
    Serviço para cálculo de estatísticas de presença.
    
    Esta classe centraliza todos os cálculos estatísticos relacionados
    a presenças, oferecendo métodos para diferentes tipos de análise.
    
    Attributes:
        cache_timeout (int): Tempo de cache em segundos (padrão: 300)
        
    Example:
        >>> calc = CalculadoraEstatisticas()
        >>> stats = calc.calcular_por_turma(turma_id=1, periodo='2024-01')
        >>> print(stats['percentual_geral'])
        85.5
    """
    
    def calcular_por_turma(self, turma_id, periodo):
        """
        Calcula estatísticas de presença para uma turma específica.
        
        Args:
            turma_id (int): ID da turma para cálculo
            periodo (str): Período no formato 'YYYY-MM' ou 'YYYY-MM-DD'
            
        Returns:
            dict: Dicionário com estatísticas calculadas:
                - percentual_geral (float): Percentual geral de presença
                - total_alunos (int): Número total de alunos
                - alunos_carencia (int): Alunos com carência
                - por_atividade (list): Estatísticas por atividade
                
        Raises:
            ValueError: Se turma_id não for encontrada
            ValidationError: Se período estiver em formato inválido
            
        Example:
            >>> calc = CalculadoraEstatisticas()
            >>> result = calc.calcular_por_turma(1, '2024-01')
            >>> print(f"Presença geral: {result['percentual_geral']}%")
            Presença geral: 85.5%
        """
        # Implementação...
```

## Configuração do Ambiente

### 1. Ambiente de Desenvolvimento

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Configurar pre-commit hooks
pre-commit install

# Configurar variáveis de ambiente
cp .env.example .env.dev
```

### 2. Configuração do Editor (VS Code)

**`.vscode/settings.json`**:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length=88"],
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

**`.vscode/extensions.json`**:
```json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.pylint",
        "ms-python.flake8",
        "ms-python.black-formatter",
        "bradlc.vscode-tailwindcss",
        "esbenp.prettier-vscode"
    ]
}
```

### 3. Configuração de Linting

**`.pylintrc`**:
```ini
[MASTER]
load-plugins=pylint_django
django-settings-module=omaum.settings

[MESSAGES CONTROL]
disable=missing-docstring,too-few-public-methods

[FORMAT]
max-line-length=88
```

**`pyproject.toml`**:
```toml
[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
```

## Como Contribuir

### 1. Workflow Git

```bash
# 1. Criar branch para feature
git checkout -b feature/nome-da-feature

# 2. Fazer commits atômicos
git add .
git commit -m "feat: adicionar cálculo de carências automático"

# 3. Push e Pull Request
git push origin feature/nome-da-feature
# Criar PR no GitHub/GitLab
```

### 2. Convenção de Commits

Seguimos o padrão [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Tipos principais
feat: nova funcionalidade
fix: correção de bug
docs: documentação
style: formatação, espaços
refactor: refatoração de código
test: adição/modificação de testes
chore: tarefas de manutenção

# Exemplos
feat(presencas): adicionar registro multi-etapas
fix(api): corrigir validação de datas futuras
docs(readme): atualizar instruções de instalação
test(presencas): adicionar testes para cálculo de carências
```

### 3. Pull Request Template

```markdown
## Descrição
Breve descrição das mudanças implementadas.

## Tipo de Mudança
- [ ] Bug fix (correção que resolve um problema)
- [ ] Feature (nova funcionalidade)
- [ ] Breaking change (mudança que quebra compatibilidade)
- [ ] Documentação

## Como Testar
1. Executar `python manage.py test presencas`
2. Navegar para `/presencas/registro-rapido/`
3. Verificar se a funcionalidade X funciona

## Checklist
- [ ] Código segue as convenções do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada
- [ ] Não há breaking changes ou foram documentadas
```

## Testes e QA

### 1. Estrutura de Testes

```python
# tests/test_models.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from presencas.models import PresencaDetalhada
from turmas.models import Turma
from alunos.models import Aluno

class PresencaDetalhadaTestCase(TestCase):
    """Testes para o modelo PresencaDetalhada"""
    
    def setUp(self):
        """Configuração inicial para todos os testes"""
        self.turma = Turma.objects.create(
            nome="Turma Teste",
            codigo="TT001"
        )
        self.aluno = Aluno.objects.create(
            nome="João Teste",
            cpf="123.456.789-00"
        )
    
    def test_calculo_percentual_presenca(self):
        """Testa cálculo correto do percentual de presença"""
        presenca = PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            convocacoes=10,
            presencas=8,
            faltas=2
        )
        
        self.assertEqual(presenca.percentual_presenca, 80.00)
    
    def test_validacao_presencas_faltas_maior_convocacoes(self):
        """Testa validação quando P+F > C"""
        with self.assertRaises(ValidationError):
            presenca = PresencaDetalhada(
                aluno=self.aluno,
                turma=self.turma,
                convocacoes=10,
                presencas=8,
                faltas=5  # 8+5 = 13 > 10
            )
            presenca.clean()
```

### 2. Testes de API

```python
# tests/test_api.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class PresencaAPITestCase(APITestCase):
    """Testes para API de presenças"""
    
    def setUp(self):
        """Configuração inicial"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_listar_presencas_autenticado(self):
        """Testa listagem de presenças com usuário autenticado"""
        response = self.client.get('/presencas/api/presencas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_criar_presenca_dados_validos(self):
        """Testa criação de presença com dados válidos"""
        data = {
            'aluno_id': 1,
            'turma_id': 1,
            'data': '2024-01-15',
            'presente': True
        }
        response = self.client.post('/presencas/api/presencas/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

### 3. Executar Testes

```bash
# Todos os testes
python manage.py test

# Testes específicos
python manage.py test presencas
python manage.py test presencas.tests.test_models
python manage.py test presencas.tests.test_api.PresencaAPITestCase.test_criar_presenca

# Com coverage
coverage run --source='.' manage.py test
coverage report
coverage html

# Testes em paralelo
python manage.py test --parallel 4

# Testes com debug
python manage.py test --debug-mode --verbosity=2
```

### 4. Factories para Testes

```python
# tests/factories.py
import factory
from factory.django import DjangoModelFactory
from presencas.models import PresencaDetalhada
from datetime import date

class PresencaDetalhadaFactory(DjangoModelFactory):
    """Factory para criar objetos PresencaDetalhada para testes"""
    
    class Meta:
        model = PresencaDetalhada
    
    aluno = factory.SubFactory('alunos.tests.factories.AlunoFactory')
    turma = factory.SubFactory('turmas.tests.factories.TurmaFactory')
    atividade = factory.SubFactory('atividades.tests.factories.AtividadeFactory')
    periodo = date(2024, 1, 1)
    convocacoes = 20
    presencas = 18
    faltas = 2
    voluntario_extra = 0
    voluntario_simples = 0

# Uso nos testes
def test_exemplo(self):
    presenca = PresencaDetalhadaFactory(
        convocacoes=10,
        presencas=8
    )
    self.assertEqual(presenca.percentual_presenca, 80.00)
```

## Deploy e CI/CD

### 1. GitHub Actions

**`.github/workflows/ci.yml`**:
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_omaum
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run linting
      run: |
        flake8 .
        pylint presencas/
    
    - name: Run tests
      run: |
        coverage run --source='.' manage.py test
        coverage xml
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_omaum
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to production
      run: |
        # Script de deploy
        echo "Deploying to production..."
```

### 2. Docker

**`Dockerfile`**:
```dockerfile
FROM python:3.11-slim

# Configurar ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Configurar diretório de trabalho
WORKDIR /app

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput

# Expor porta
EXPOSE 8000

# Comando de inicialização
CMD ["gunicorn", "omaum.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**`docker-compose.yml`**:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://postgres:password@db:5432/omaum
    depends_on:
      - db
    volumes:
      - ./media:/app/media
      - ./logs:/app/logs

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: omaum
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./staticfiles:/app/staticfiles
    depends_on:
      - web

volumes:
  postgres_data:
```

## Debugging

### 1. Configuração de Debug

```python
# settings/development.py
DEBUG = True

# Django Debug Toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

INTERNAL_IPS = ['127.0.0.1', '::1']

# Logging detalhado
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'presencas': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

### 2. Debugging em Views

```python
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def debug_view(request):
    """View com debugging detalhado"""
    
    if settings.DEBUG:
        logger.debug(f"Request: {request.method} {request.path}")
        logger.debug(f"User: {request.user}")
        logger.debug(f"GET params: {request.GET}")
        logger.debug(f"POST data: {request.POST}")
    
    # Usar breakpoint() para debug interativo
    if settings.DEBUG and 'debug' in request.GET:
        breakpoint()
    
    # Lógica da view...
```

### 3. Debugging de Queries

```python
from django.db import connection
from django.conf import settings

def view_with_query_debug(request):
    """View que monitora queries SQL"""
    
    if settings.DEBUG:
        # Resetar queries
        connection.queries_log.clear()
    
    # Executar lógica que faz queries
    presencas = Presenca.objects.select_related('aluno', 'turma').all()
    
    if settings.DEBUG:
        logger.debug(f"Queries executadas: {len(connection.queries)}")
        for query in connection.queries:
            logger.debug(f"SQL: {query['sql']}")
            logger.debug(f"Tempo: {query['time']}s")
    
    return render(request, 'template.html', {'presencas': presencas})
```

## Performance

### 1. Otimização de Queries

```python
# ❌ Problema N+1
def listar_presencas_lento(request):
    presencas = Presenca.objects.all()  # 1 query
    for presenca in presencas:
        print(presenca.aluno.nome)      # N queries

# ✅ Solução otimizada
def listar_presencas_rapido(request):
    presencas = Presenca.objects.select_related(
        'aluno', 'turma', 'atividade'
    ).all()  # 1 query apenas
    
    for presenca in presencas:
        print(presenca.aluno.nome)  # Sem queries adicionais

# ✅ Para relacionamentos many-to-many
def listar_com_prefetch(request):
    turmas = Turma.objects.prefetch_related(
        'presencas_detalhadas__aluno'
    ).all()
```

### 2. Cache Estratégico

```python
from django.core.cache import cache
from django.views.decorators.cache import cache_page

# Cache de view
@cache_page(60 * 15)  # 15 minutos
def estatisticas_view(request):
    """View com cache automático"""
    pass

# Cache manual
def calcular_estatisticas_turma(turma_id, periodo):
    """Função com cache manual"""
    
    cache_key = f'stats_turma_{turma_id}_{periodo}'
    result = cache.get(cache_key)
    
    if result is None:
        # Cálculo pesado
        result = fazer_calculo_complexo(turma_id, periodo)
        cache.set(cache_key, result, 60 * 30)  # 30 minutos
    
    return result

# Cache de template
{% load cache %}
{% cache 300 sidebar request.user.username %}
    <!-- Conteúdo cacheado por 5 minutos -->
{% endcache %}
```

### 3. Índices de Banco

```python
class PresencaDetalhada(models.Model):
    # Campos...
    
    class Meta:
        indexes = [
            # Índice composto para consultas comuns
            models.Index(
                fields=['turma', 'periodo', 'atividade'],
                name='presenca_turma_periodo_idx'
            ),
            # Índice para ordenação
            models.Index(
                fields=['-data_registro'],
                name='presenca_data_registro_idx'
            ),
            # Índice parcial (PostgreSQL)
            models.Index(
                fields=['aluno'],
                condition=models.Q(presente=False),
                name='presenca_ausencias_idx'
            ),
        ]
```

### 4. Paginação Eficiente

```python
from django.core.paginator import Paginator

def listar_presencas_paginado(request):
    """Listagem com paginação eficiente"""
    
    presencas = Presenca.objects.select_related(
        'aluno', 'turma'
    ).order_by('-data_registro')
    
    paginator = Paginator(presencas, 25)  # 25 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'lista.html', {
        'page_obj': page_obj,
        'total_count': paginator.count  # Avoid count() in template
    })
```

### 5. Monitoring de Performance

```python
# middleware/performance.py
import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('performance')

class PerformanceMiddleware(MiddlewareMixin):
    """Middleware para monitorar performance"""
    
    def process_request(self, request):
        request.start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            if duration > 1.0:  # Log requests > 1 segundo
                logger.warning(
                    f"Slow request: {request.method} {request.path} "
                    f"took {duration:.2f}s"
                )
        
        return response
```

---

*Para dúvidas específicas sobre desenvolvimento, consulte a documentação adicional ou entre em contato com a equipe de desenvolvimento.*
