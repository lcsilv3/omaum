# Sistema OMAUM 🎓

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-4.2+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)


Sistema de gestão acadêmica completo desenvolvido em Django, especializado no controle de presenças e frequência de alunos em atividades acadêmicas e ritualísticas.


## Aviso Importante

Para rodar o monitoramento automático de formatação Python:

**Abra o menu de tarefas (Ctrl+Shift+B ou F1 > "Executar Tarefa") e selecione "Monitoramento automático Ruff".**

O script ficará rodando em segundo plano, monitorando alterações nos arquivos Python do seu projeto.

### 📈 Relatórios e Análises
- **Painel de Estatísticas**: Dashboard interativo com gráficos em tempo real
- **Exportação Avançada**: Excel profissional, PDF completo, CSV estruturado
- **Agendamento Automático**: Relatórios periódicos enviados por email

- **Relatórios Consolidados**: Visão geral por período, turma ou curso


### 🔗 API REST Completa
- **Endpoints Documentados**: Swagger/ReDoc integrado

- **Autenticação Segura**: Token-based authentication

- **Rate Limiting**: Controle de acesso e performance
- **Versionamento**: APIs versionadas para compatibilidade


### 👥 Gestão Acadêmica

- **Alunos**: Cadastro completo com validações
- **Turmas**: Gestão de períodos letivos e matriculas
- **Atividades**: Controle de atividades acadêmicas e ritualísticas

- **Cursos**: Estrutura hierárquica de cursos oferecidos


## 🚀 Quick Start


```bash

# 1. Clonar o repositório
git clone https://github.com/lcsilv3/omaum.git
cd omaum

# 2. Configurar ambiente virtual

python -m venv venv

source venv/bin/activate  # Linux/Mac

# ou

venv\Scripts\activate     # Windows

# 3. Instalar dependências

pip install -r requirements.txt


# 4. Configurar banco de dados

python manage.py migrate


# 5. Criar superusuário

python manage.py createsuperuser


# 6. Executar servidor
python manage.py runserver
```

Acesse: **[http://localhost:8000](http://localhost:8000)**

## Import seguro de códigos (curto)

Antes de rodar imports que alteram dados, crie um backup do banco de produção. Exemplo (PowerShell):

```powershell
# criar pasta de backups local
mkdir .\backups -Force

# gerar dump no container Postgres (formato custom)
docker --% exec -i omaum-db-prod bash -lc "pg_dump -U omaum_app -d omaum_prod -F c -f /tmp/omaum_prod_$(date +%Y%m%d%H%M%S).dump"

# copiar dump para o host
docker cp omaum-db-prod:/tmp/omaum_prod_<TIMESTAMP>.dump .\backups\
```

Executar o import (script idempotente que cria tipos quando solicitado):

```powershell
docker compose -f docker\docker-compose.prod.yml exec -w /app omaum-web bash -lc "export PYTHONPATH=/app; export DJANGO_SETTINGS_MODULE=omaum.settings.production; python scripts/popular_codigos_por_tipo.py --create-types"
```

Restaurar a partir do dump (se necessário):

```powershell
# copiar o dump de volta para o container
docker cp .\backups\omaum_prod_<TIMESTAMP>.dump omaum-db-prod:/tmp/

# restaurar (substitui dados atuais)
docker --% exec -i omaum-db-prod bash -lc "pg_restore -U omaum_app -d omaum_prod /tmp/omaum_prod_<TIMESTAMP>.dump"
```

Observação: `scripts/popular_codigos_por_tipo.py` foi refatorado para ser mais tolerante a cabeçalhos e possui a flag `--create-types`.

## ▶️ Inicialização com Docker e atalho

Para iniciar o ambiente completo (Docker + aplicação + navegador) utilize o script PowerShell dedicado:

```powershell
cd C:\projetos\omaum
pwsh -ExecutionPolicy Bypass -File scripts/run_omaum.ps1
```

- O script garante que o Docker Desktop esteja ativo, sobe os serviços `omaum-web` e `omaum-nginx` via `docker-compose` e pergunta qual navegador deve abrir `http://omaum.local/`.
- Caso o PowerShell solicite permissão, execute uma única vez como administrador: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

### Criar atalho na área de trabalho

```powershell
pwsh -ExecutionPolicy Bypass -File scripts/create_desktop_shortcut.ps1
```

- Será gerado o atalho **"OMAUM - Iniciar"** na área de trabalho apontando para `scripts/run_omaum.ps1`.
- Use os parâmetros `-ShortcutName` ou `-AppUrl` para customizar o nome do atalho ou o endereço aberto após o boot dos serviços.

### Executar scripts localmente (wrapper)

Você pode usar um wrapper que configura automaticamente o PYTHONPATH para a raiz do repositório e executa o script com o Python do `venv` (se existir) ou com o `py`/`python` do sistema:

```powershell
python scripts/run_local.py scripts/popular_codigos_por_tipo.py
```

O wrapper tentará localizar `venv\Scripts\python.exe`, depois `py -3` e por fim `python` no PATH. Se não encontrar um interpretador, instale o Python 3.8+ e/ou crie o `venv` com `python -m venv venv`.

## 🛠️ Tecnologias Utilizadas

### Backend
- **Django 4.2+**: Framework web robusto
- **Django REST Framework**: API REST moderna
- **PostgreSQL**: Banco de dados principal (produção)

- **SQLite**: Desenvolvimento local

## Aviso Importante

Para rodar o monitoramento automático de formatação Python:


**Abra o menu de tarefas (Ctrl+Shift+B ou F1 > "Executar Tarefa") e selecione "Monitoramento automático Ruff".**



O script ficará rodando em segundo plano, monitorando alterações nos arquivos Python do seu projeto.



- **Celery**: Processamento assíncrono (futuro)



- **Bootstrap 5**: Framework CSS responsivo

- **jQuery**: Interações dinâmicas

- **Chart.js**: Gráficos interativos
- **Select2**: Componentes avançados


### Infraestrutura

- **Docker**: Containerização
- **Nginx**: Proxy reverso
- **Gunicorn**: Servidor WSGI

- **GitHub Actions**: CI/CD


## 📁 Estrutura do Projeto


```

omaum/
├── 📁 docs/                    # Documentação completa
│   ├── ARQUITETURA_PRESENCAS.md

│   ├── MANUAL_USUARIO.md

│   ├── GUIA_INSTALACAO.md
│   ├── API_DOCUMENTATION.md
│   └── GUIA_DESENVOLVEDOR.md
├── 📁 presencas/              # ⭐ Sistema de Presenças (principal)
│   ├── models.py              # Modelos de dados

│   ├── views/                 # Views organizadas por função

│   ├── api/                   # API REST endpoints

│   ├── services/              # Lógica de negócio

│   └── templates/             # Templates HTML
├── 📁 alunos/                 # Gestão de estudantes
├── 📁 turmas/                 # Gestão de turmas

├── 📁 atividades/             # Controle de atividades

├── 📁 cursos/                 # Administração de cursos
├── 📁 core/                   # Utilitários comuns

└── 📁 static/                 # Arquivos estáticos

```


### Módulos Principais


- **🎯 presencas**: Sistema completo de controle de frequência ⭐
- **👥 alunos**: Gerenciamento de estudantes e perfis
- **🏫 turmas**: Organização de turmas e períodos letivos
- **📚 atividades**: Controle de atividades acadêmicas e ritualísticas
- **🎓 cursos**: Estrutura hierárquica de cursos
- **⚙️ core**: Utilitários, middlewares e configurações comuns

## 📖 Documentação

### Documentação Disponível

- **📋 [Manual do Usuário](docs/MANUAL_USUARIO.md)**: Guia completo para professores e coordenadores

- **🏗️ [Arquitetura do Sistema](docs/ARQUITETURA_PRESENCAS.md)**: Visão técnica detalhada

- **⚙️ [Guia de Instalação](docs/GUIA_INSTALACAO.md)**: Instruções completas de setup
- **🔌 [Documentação da API](docs/API_DOCUMENTATION.md)**: Endpoints REST documentados
- **👨‍💻 [Guia do Desenvolvedor](docs/GUIA_DESENVOLVEDOR.md)**: Padrões e convenções
- **📝 [Changelog](docs/CHANGELOG.md)**: Histórico de versões e mudanças
- **📊 [Status da Refatoração do Histórico](docs/historico_refatoracao_status.md)**: acompanhamento das etapas e QA contínuo



## 🧪 Desenvolvimento



### Executar Testes



```bash

# Checklist rápido do histórico
python scripts/run_historico_qa.py

# Todos os testes
python manage.py test
# Testes específicos do módulo de presenças
python manage.py test presencas

# Com coverage
coverage run --source='.' manage.py test
coverage report
```

### Linting e Formatação

```bash
# Executar linters
python scripts/lint.py

# Formatação automática
black .
isort .
```

### Configuração do Editor (VS Code)

Extensões recomendadas:
- Python (Microsoft)
- Pylint
- Black Formatter
- Django

## 🌟 Principais Features do Sistema de Presenças

### ✅ Implementado (v2.0)

- ✅ **Registro Multi-etapas**: Processo guiado completo
- ✅ **Registro Rápido**: Interface AJAX otimizada
- ✅ **Painel Estatísticas**: Gráficos interativos em tempo real
- ✅ **Exportação Avançada**: Excel, PDF, CSV profissionais
- ✅ **API REST**: Endpoints completos documentados
- ✅ **Configurações Flexíveis**: Por turma/atividade
- ✅ **Agendamento Automático**: Relatórios por email
- ✅ **Validações Robustas**: Multi-camadas de validação
- ✅ **Cache Inteligente**: Performance otimizada
- ✅ **Auditoria Completa**: Logs detalhados

### 🚧 Roadmap Futuro

- 🔄 **Notificações Push**: Alertas em tempo real
- 📱 **App Mobile**: Aplicativo nativo
- 🤖 **IA Predictiva**: Predição de faltas
- 🔗 **Integrações**: Sistemas acadêmicos externos
- ⚡ **Microserviços**: Arquitetura escalável

## 🤝 Como Contribuir

1. **Fork** o repositório
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add: AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

### Convenções de Commit

```bash
feat: nova funcionalidade
fix: correção de bug
docs: atualização de documentação
style: formatação de código
refactor: refatoração
test: adição de testes
```

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

### Canais de Suporte

- **📧 Email**: suporte@omaum.edu.br
- **🐛 Issues**: [GitHub Issues](https://github.com/lcsilv3/omaum/issues)
- **💬 Discussões**: [GitHub Discussions](https://github.com/lcsilv3/omaum/discussions)
- **📖 Wiki**: [Documentação Completa](https://github.com/lcsilv3/omaum/wiki)

### Reportar Bugs

Para reportar bugs, use o template de issue no GitHub incluindo:
- Versão do sistema
- Passos para reproduzir
- Comportamento esperado vs atual
- Screenshots (se aplicável)
- Logs de erro

---

<div align="center">

**Desenvolvido com ❤️ para a comunidade acadêmica**

[⭐ Star no GitHub](https://github.com/lcsilv3/omaum) | [📖 Documentação](docs/) | [🐛 Reportar Bug](https://github.com/lcsilv3/omaum/issues)

</div>