# Guia de Instalação - Sistema OMAUM

## Pré-requisitos do Sistema

### Requisitos Mínimos
- **Python**: 3.8+ (recomendado 3.11+)
- **Sistema Operacional**: Windows 10+, Ubuntu 18.04+, macOS 10.15+
- **Memória RAM**: 4GB (recomendado 8GB+)
- **Espaço em Disco**: 2GB livres
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)

### Software Necessário
```bash
# Verificar versão do Python
python --version  # ou python3 --version no Linux/Mac

# Git para clonar o repositório
git --version

# pip para gerenciar pacotes Python
pip --version
```

## Instalação

### 1. Clonar o Repositório

```bash
# Clonar do GitHub
git clone https://github.com/lcsilv3/omaum.git

# Navegar para o diretório
cd omaum
```

### 2. Criar Ambiente Virtual

#### Windows
```cmd
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate

# Verificar ativação (deve mostrar (venv) no prompt)
```

#### Linux/macOS
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Verificar ativação (deve mostrar (venv) no prompt)
```

### 3. Instalar Dependências

```bash
# Atualizar pip
pip install --upgrade pip

# Instalar dependências de produção
pip install -r requirements.txt

# Para desenvolvimento (opcional)
pip install -r requirements-dev.txt
```

### 4. Configuração Inicial

#### Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# Copiar template
cp .env.example .env  # Linux/Mac
copy .env.example .env  # Windows
```

Edite o arquivo `.env`:

```env
# Configurações básicas
SECRET_KEY=sua-chave-secreta-super-segura-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,::1

# Banco de dados (SQLite para desenvolvimento)
DATABASE_URL=sqlite:///db.sqlite3

# Para PostgreSQL em produção
# DATABASE_URL=postgresql://usuario:senha@localhost:5432/omaum

# Email (opcional para desenvolvimento)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app

# Configurações de arquivos estáticos
STATIC_URL=/static/
MEDIA_URL=/media/

# Timezone
TIME_ZONE=America/Sao_Paulo
LANGUAGE_CODE=pt-br
```

#### Gerar SECRET_KEY (Obrigatório)

```python
# Execute no terminal Python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copie a saída e cole no arquivo `.env` como valor de `SECRET_KEY`.

### 5. Configurar Banco de Dados

#### Desenvolvimento (SQLite)
```bash
# Executar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
```

#### Produção (PostgreSQL)
```bash
# Instalar driver PostgreSQL
pip install psycopg2-binary

# Configurar DATABASE_URL no .env
# DATABASE_URL=postgresql://usuario:senha@localhost:5432/omaum

# Executar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
```

### 6. Executar Aplicação

```bash
# Desenvolvimento
python manage.py runserver

# Produção (usar gunicorn)
pip install gunicorn
gunicorn omaum.wsgi:application --bind 0.0.0.0:8000
```

Acesse: `http://localhost:8000`

## Configuração Inicial do Sistema

### 1. Acessar Admin Django

1. Acesse `http://localhost:8000/admin/`
2. Faça login com o superusuário criado
3. Configurar dados básicos

### 2. Configurar Dados Mestres

#### Cursos
```python
# Via Admin Django ou shell
python manage.py shell

from cursos.models import Curso
Curso.objects.create(
    nome="Curso Básico",
    codigo="CB001",
    descricao="Curso introdutório",
    duracao_meses=12
)
```

#### Atividades
```python
from atividades.models import Atividade
Atividade.objects.create(
    nome="Aula Teórica",
    tipo="academica",
    obrigatoria=True,
    descricao="Aulas teóricas regulares"
)
```

#### Turmas
```python
from turmas.models import Turma
from datetime import date

Turma.objects.create(
    nome="Turma 2024-1",
    codigo="T2024001",
    data_inicio=date(2024, 3, 1),
    data_fim=date(2024, 12, 15),
    perc_carencia=75.0  # 75% mínimo de presença
)
```

### 3. Configurar Presenças

#### Configurações por Turma/Atividade
```python
from presencas.models import ConfiguracaoPresenca
from turmas.models import Turma
from atividades.models import Atividade

turma = Turma.objects.get(codigo="T2024001")
atividade = Atividade.objects.get(nome="Aula Teórica")

ConfiguracaoPresenca.objects.create(
    turma=turma,
    atividade=atividade,
    limite_carencia_0_25=0,    # 0-25%: 0 carências permitidas
    limite_carencia_26_50=1,   # 26-50%: 1 carência permitida
    limite_carencia_51_75=2,   # 51-75%: 2 carências permitidas
    limite_carencia_76_100=3,  # 76-100%: 3 carências permitidas
    obrigatoria=True,
    peso_calculo=1.0
)
```

## Configuração de Produção

### 1. Configurações de Segurança

```python
# settings/production.py
import os

DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com', 'www.seu-dominio.com']

# Configurações HTTPS
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = 'same-origin'

# Sessions
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 2. Arquivos Estáticos

```bash
# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Configurar servidor web (nginx/apache) para servir estáticos
```

### 3. Banco de Dados PostgreSQL

```bash
# Instalar PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Criar banco e usuário
sudo -u postgres psql
CREATE DATABASE omaum;
CREATE USER omaum_user WITH PASSWORD 'senha_segura';
GRANT ALL PRIVILEGES ON DATABASE omaum TO omaum_user;
\q
```

### 4. Supervisor (Gerenciamento de Processo)

```ini
# /etc/supervisor/conf.d/omaum.conf
[program:omaum]
command=/path/to/venv/bin/gunicorn omaum.wsgi:application --bind 127.0.0.1:8000
directory=/path/to/omaum
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/omaum/gunicorn.log
```

### 5. Nginx (Proxy Reverso)

```nginx
# /etc/nginx/sites-available/omaum
server {
    listen 80;
    server_name seu-dominio.com;
    
    location /static/ {
        alias /path/to/omaum/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/omaum/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Migrations e Dados Iniciais

### 1. Executar Migrações

```bash
# Verificar migrações pendentes
python manage.py showmigrations

# Executar migrações
python manage.py migrate

# Criar migração personalizada (se necessário)
python manage.py makemigrations
```

### 2. Carregar Dados Iniciais

```bash
# Carregar fixtures (se disponíveis)
python manage.py loaddata fixtures/initial_data.json

# Ou executar script personalizado
python manage.py shell < scripts/dados_iniciais.py
```

### 3. Backup de Dados

```bash
# Backup completo
python manage.py dumpdata > backup_completo.json

# Backup específico
python manage.py dumpdata presencas > backup_presencas.json

# Restaurar backup
python manage.py loaddata backup_completo.json
```

## Testes e Verificação

### 1. Executar Testes

```bash
# Todos os testes
python manage.py test

# Testes específicos
python manage.py test presencas
python manage.py test presencas.tests.test_models

# Com coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### 2. Verificar Configuração

```bash
# Verificar configuração Django
python manage.py check

# Verificar deployment
python manage.py check --deploy

# Verificar banco de dados
python manage.py dbshell
```

### 3. Logs e Monitoramento

```python
# settings.py - Configuração de logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'presencas': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

## Solução de Problemas

### Problemas Comuns

#### Erro de Importação
```bash
# Verificar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/omaum"

# Ou adicionar ao manage.py
import sys
sys.path.append('/path/to/omaum')
```

#### Erro de Permissão de Arquivos
```bash
# Linux/Mac - Ajustar permissões
chmod -R 755 /path/to/omaum
chown -R www-data:www-data /path/to/omaum
```

#### Erro de Banco de Dados
```bash
# Reset completo do banco (CUIDADO!)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

#### Erro de Dependências
```bash
# Reinstalar dependências
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Debug de Problemas

```python
# Habilitar debug detalhado
DEBUG = True
DEBUG_TOOLBAR = True  # Se usando django-debug-toolbar

# Log SQL queries
LOGGING['loggers']['django.db.backends'] = {
    'level': 'DEBUG',
    'handlers': ['console'],
}
```

## Atualizações

### Processo de Atualização

```bash
# 1. Backup
python manage.py dumpdata > backup_pre_update.json

# 2. Atualizar código
git pull origin main

# 3. Atualizar dependências
pip install -r requirements.txt --upgrade

# 4. Executar migrações
python manage.py migrate

# 5. Coletar estáticos
python manage.py collectstatic --noinput

# 6. Reiniciar serviços
sudo systemctl restart supervisor
sudo systemctl restart nginx
```

### Rollback em Caso de Problemas

```bash
# Reverter migração
python manage.py migrate presencas 0001

# Restaurar backup
python manage.py flush
python manage.py loaddata backup_pre_update.json

# Reverter código
git checkout HEAD~1
```

## Suporte

### Documentação Adicional
- [Manual do Usuário](MANUAL_USUARIO.md)
- [Documentação da API](API_DOCUMENTATION.md)
- [Guia do Desenvolvedor](GUIA_DESENVOLVEDOR.md)

### Contato
- **Email**: suporte@omaum.edu.br
- **GitHub Issues**: https://github.com/lcsilv3/omaum/issues
- **Documentação Online**: https://docs.omaum.edu.br

### Comunidade
- **Fórum**: https://forum.omaum.edu.br
- **Slack**: https://omaum.slack.com
- **Wiki**: https://wiki.omaum.edu.br
