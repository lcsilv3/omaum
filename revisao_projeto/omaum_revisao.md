# Revisão da Funcionalidade: omaum

## Arquivos urls.py:


### Arquivo: omaum\urls.py

```python
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings  # Adicione esta linha

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "", include("core.urls")
    ),  # Inclui as URLs do core, incluindo a p√°gina inicial
    path("alunos/", include("alunos.urls")),
    path("atividades/", include("atividades.urls")),
    path("cargos/", include("cargos.urls")),
    path("cursos/", include("cursos.urls")),
    path("frequencias/", include("frequencias.urls")),
    path("iniciacoes/", include("iniciacoes.urls")),
    path("presencas/", include("presencas.urls")),
    path("punicoes/", include("punicoes.urls")),
    path("relatorios/", include("relatorios.urls", namespace="relatorios")),
    path("turmas/", include("turmas.urls")),
]

from django.contrib.auth import views as auth_views

urlpatterns += [
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(next_page="/"),
        name="logout",
    ),
]

# Adicione este bloco no final do arquivo
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

```

## Arquivos de Template:


### Arquivo: omaum\templates\403.html

```html
{% extends "base.html" %}

{% block title %}403 Acesso Proibido{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body text-center">
                    <h1 class="display-1">403</h1>
                    <h2 class="mb-4">Acesso Proibido</h2>
                    <p class="lead">Desculpe, você não tem permissão para acessar esta página.</p>
                    <a href="{% url 'core:home' %}" class="btn btn-primary mt-3">Voltar para a Página Inicial</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```


### Arquivo: omaum\templates\404.html

```html
{% extends "base.html" %}

{% block title %}404 Página Não Encontrada{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body text-center">
                    <h1 class="display-1">404</h1>
                    <h2 class="mb-4">Página Não Encontrada</h2>
                    <p class="lead">Desculpe, a página que você está procurando não existe.</p>
                    <a href="{% url 'core:home' %}" class="btn btn-primary mt-3">Voltar para a Página Inicial</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```


### Arquivo: omaum\templates\500.html

```html
{% extends "base.html" %}

{% block title %}500 Erro Interno do Servidor{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body text-center">
                    <h1 class="display-1">500</h1>
                    <h2 class="mb-4">Erro Interno do Servidor</h2>
                    <p class="lead">Desculpe, ocorreu um erro interno no servidor. Nossa equipe técnica foi notificada e está trabalhando para resolver o problema.</p>
                    <a href="{% url 'core:home' %}" class="btn btn-primary mt-3">Tentar Novamente</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```


### Arquivo: omaum\templates\atualizar_configuracao.html

```html
{% extends "base.html" %}

{% block title %}Atualizar Configurações do Sistema{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Atualizar Configurações do Sistema</h1>
    
    <div class="card mt-4">
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="nome_sistema" class="form-label">Nome do Sistema</label>
                    <input type="text" class="form-control" id="nome_sistema" name="nome_sistema" value="{{ config.nome_sistema }}" required>
                </div>
                
                <div class="mb-3">
                    <label for="versao" class="form-label">Versão</label>
                    <input type="text" class="form-control" id="versao" name="versao" value="{{ config.versao }}" required>
                </div>
                
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="manutencao_ativa" name="manutencao_ativa" {% if config.manutencao_ativa %}checked{% endif %}>
                    <label class="form-check-label" for="manutencao_ativa">Sistema em Manutenção</label>
                </div>
                
                <div class="mb-3">
                    <label for="mensagem_manutencao" class="form-label">Mensagem de Manutenção</label>
                    <textarea class="form-control" id="mensagem_manutencao" name="mensagem_manutencao" rows="3">{{ config.mensagem_manutencao }}</textarea>
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'core:painel_controle' %}" class="btn btn-secondary">Cancelar</a>
                    <button type="submit" class="btn btn-primary">Salvar Alterações</button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}

```


### Arquivo: omaum\templates\base.html

```html
{% load static %}
{% comment %}
Este é o template base para o projeto OMAUM.
Localização: omaum/templates/base.html

Uso:
Este template serve como base para todas as outras páginas do projeto.
Ele contém a estrutura HTML comum, incluindo cabeçalho, rodapé, e blocos
que podem ser sobrescritos pelos templates filhos.

Para usar este template em outras páginas, comece o template filho com:
{% extends "base.html" %}

E então defina os blocos necessários, como título e conteúdo:
{% block title %}Título da Página{% endblock %}
{% block content %}
    <!-- Conteúdo específico da página aqui -->
{% endblock %}
{% endcomment %}<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Sistema OMAUM{% endblock %}</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <!-- CSS Personalizado -->
    <link rel="stylesheet" href="{% static 'css/extra_styles.css' %}">
    <link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />
</head>
<body>
    <!-- Cabeçalho -->
    <header class="bg-dark text-white p-3">
        <div class="container">
            <nav class="navbar navbar-expand-lg navbar-dark">
                <a class="navbar-brand" href="{% url 'core:pagina_inicial' %}">OMAUM</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" title="Menu de navegação">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        {% if user.is_authenticated %}
                            <li class="nav-item"><a class="nav-link" href="{% url 'alunos:listar_alunos' %}">Alunos</a></li>
                            <li class="nav-item"><a class="nav-link" href="{% url 'cursos:listar_cursos' %}">Cursos</a></li>
                            <li class="nav-item"><a class="nav-link" href="{% url 'atividades:listar_atividades_academicas' %}">Atividades Acadêmicas</a></li>
                            <li class="nav-item"><a class="nav-link" href="{% url 'atividades:listar_atividades_ritualisticas' %}">Atividades Ritualísticas</a></li>
                            <li class="nav-item"><a class="nav-link" href="{% url 'turmas:listar_turmas' %}">Turmas</a></li>
                            <li class="nav-item"><a class="nav-link" href="{% url 'iniciacoes:listar_iniciacoes' %}">Iniciações</a></li>
                            <li class="nav-item"><a class="nav-link" href="{% url 'cargos:listar_cargos' %}">Cargos</a></li>
                            <li class="nav-item"><a class="nav-link" href="{% url 'frequencias:listar_frequencias' %}">Frequências</a></li>
                            <li class="nav-item"><a class="nav-link" href="{% url 'presencas:listar_presencas' %}">Presenças</a></li>
                            <li class="nav-item"><a class="nav-link" href="{% url 'punicoes:listar_punicoes' %}">Punições</a></li>
                            {% if user.is_staff %}
                                <li class="nav-item"><a class="nav-link" href="{% url 'core:painel_controle' %}">Painel de Controle</a></li>
                            {% endif %}
                        {% endif %}
                    </ul>
                    <div class="navbar-nav">
                        {% if user.is_authenticated %}
                            <span class="nav-item nav-link">Olá, {{ user.username }}</span>
                            <a class="nav-link" href="{% url 'core:sair' %}">Sair</a>
                        {% else %}
                            <a class="nav-link" href="{% url 'core:entrar' %}">Entrar</a>
                        {% endif %}
                    </div>
                </div>
            </nav>
        </div>
    </header>

    <!-- Mensagens -->
    <div class="container mt-3">
        {% if messages %}
        <div class="messages">
            {% for message in messages %}
            <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>

    <!-- Conteúdo Principal -->
    <main class="container py-4">
        {% block content %}{% endblock %}
    </main>

    <!-- Rodapé -->
    <footer class="bg-dark text-white p-3 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <p>© 2025 OMAUM - Todos os direitos reservados</p>
                </div>
                <div class="col-md-6 text-md-end">
                    <p>Versão 1.0</p>
                </div>
            </div>
        </div>
    </footer>

    <!-- JavaScript Bootstrap -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
    <!-- JavaScript Personalizado -->
    {% block extra_js %}{% endblock %}
    <!-- CSRF Refresh Script -->
    <script src="{% static 'js/csrf_refresh.js' %}"></script>
</body>
</html>
```


### Arquivo: omaum\templates\csrf_test.html

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSRF Test</title>
</head>
<body>
    <h1>CSRF Test</h1>
    <form method="post">
        {% csrf_token %}
        <input type="submit" value="Test CSRF">
    </form>
    <script>
        console.log("CSRF cookie:", document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken=')));
    </script>
</body>
</html>


```


### Arquivo: omaum\templates\home.html

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}OMAUM - Página Inicial{% endblock %}

{% block content %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<div class="container mt-4">
    <div class="jumbotron">
        <h1 class="display-4">Sistema de Gestão de Pessoal</h1>
        <p class="lead">Bem-vindo ao sistema de gestão de Pessoal da Ordem Mística de Iniciação Universal ao Mestrado.</p>
    </div>
    
    <!-- Primeira linha: Cursos, Alunos, Turmas -->
    <div class="row mb-4">
        <div class="col-12">
            <h3 class="mb-3 border-bottom pb-2">Gestão Acadêmica</h3>
        </div>
        
        <div class="col-md-4 mb-3">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">Cursos</h5>
                    <p class="card-text">Gerenciamento de cursos oferecidos pela instituição.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'cursos:listar_cursos' %}" class="btn btn-primary">Acessar</a>
                </div>
            </div>
        </div>
        
        <div class="col-md-4 mb-3">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">Alunos</h5>
                    <p class="card-text">Cadastro e gerenciamento de alunos.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-primary">Acessar</a>
                </div>
            </div>
        </div>
        
        <div class="col-md-4 mb-3">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">Turmas</h5>
                    <p class="card-text">Gerenciamento de turmas e períodos letivos.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-primary">Acessar</a>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Segunda linha: Atividades, Presenças, Frequências -->
    <div class="row mb-4">
        <div class="col-12">
            <h3 class="mb-3 border-bottom pb-2">Controle de Participação</h3>
        </div>
        
        <div class="col-md-4 mb-3">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">Atividades</h5>
                    <p class="card-text">Gerenciamento de atividades da instituição.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <div class="btn-group">
                        <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-primary">Atividades Acadêmicas</a>
                        <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-primary">Atividades Ritualísticas</a>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-4 mb-3">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">Presenças</h5>
                    <p class="card-text">Registro e controle de presenças em atividades.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-primary">Acessar</a>
                </div>
            </div>
        </div>
        
        <div class="col-md-4 mb-3">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">Frequências</h5>
                    <p class="card-text">Análise e relatórios de frequência dos alunos.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-primary">Acessar</a>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Terceira linha: Iniciações, Punições, Cargos -->
    <div class="row mb-4">
        <div class="col-12">
            <h3 class="mb-3 border-bottom pb-2">Gestão Institucional</h3>
        </div>
        
        <div class="col-md-4 mb-3">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">Iniciações</h5>
                    <p class="card-text">Gerenciamento de processos iniciatórios.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-primary">Acessar</a>
                </div>
            </div>
        </div>
        
        <div class="col-md-4 mb-3">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">Punições</h5>
                    <p class="card-text">Registro e controle de medidas disciplinares.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'punicoes:listar_punicoes' %}" class="btn btn-primary">Acessar</a>
                </div>
            </div>
        </div>
        
        <div class="col-md-4 mb-3">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">Cargos</h5>
                    <p class="card-text">Gestão de cargos e funções institucionais.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-primary">Acessar</a>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Quarta linha: Relatórios, Painel de Controle -->
    <div class="row mb-4">
        <div class="col-12">
            <h3 class="mb-3 border-bottom pb-2">Análise e Controle</h3>
        </div>
        
        <div class="col-md-6 mb-3">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">Relatórios</h5>
                    <p class="card-text">Geração de relatórios e análises estatísticas.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'relatorios:index' %}" class="btn btn-primary">Acessar</a>
                </div>
            </div>
        </div>
        
        <div class="col-md-6 mb-3">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">Painel de Controle</h5>
                    <p class="card-text">Visão geral e indicadores de desempenho.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'core:painel_controle' %}" class="btn btn-primary">Acessar</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

```


### Arquivo: omaum\templates\home_old.html

```html
{% extends "base.html" %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Bem-vindo ao {{ titulo }}</h1>
    {% if user.is_authenticated %}    
        <div class="row mt-4">
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Alunos</h5>
                        <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-primary">Gerenciar Alunos</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Cursos</h5>
                        <a href="{% url 'cursos:listar_cursos' %}" class="btn btn-primary">Gerenciar Cursos</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Atividades Acadêmicas</h5>
                        <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-primary">Gerenciar Atividades Acadêmicas</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Atividades Ritualísticas</h5>
                        <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-primary">Gerenciar Atividades Ritualísticas</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Turmas</h5>
                        <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-primary">Gerenciar Turmas</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Iniciações</h5>
                        <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-primary">Gerenciar Iniciações</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Cargos</h5>
                        <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-primary">Gerenciar Cargos</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Frequências</h5>
                        <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-primary">Gerenciar Frequências</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Presenças</h5>
                        <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-primary">Gerenciar Presenças</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Relatórios</h5>
                        <a href="{% url 'relatorios:index' %}" class="btn btn-primary">Gerar Relatórios</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Punições</h5>
                        <a href="{% url 'punicoes:listar_punicoes' %}" class="btn btn-primary">Gerenciar Punições</a>
                    </div>
                </div>
            </div>
            {% if user.is_staff %}
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Painel de Controle</h5>
                        <a href="{% url 'core:painel_controle' %}" class="btn btn-primary">Acessar Painel</a>
                    </div>
                </div>
            </div>
            {% endif %}
        </div>
    {% else %}
        <p>Por favor, faça login para acessar as funcionalidades do sistema.</p>
        <a href="{% url 'core:entrar' %}" class="btn btn-primary">Entrar</a>
    {% endif %}
</div>
{% endblock %}
```


### Arquivo: omaum\templates\includes\form_error.html

```html
{% if form.errors %}
    {% if form.non_field_errors %}
        <div class="alert alert-danger">
            <strong>Erro:</strong>
            <ul>
                {% for error in form.non_field_errors %}
                    <li>{{ error }}</li>
                {% endfor %}
            </ul>
        </div>
    {% endif %}

    {% for field in form %}
        {% if field.errors %}
            <div class="alert alert-danger">
                <strong>{{ field.label }}:</strong>
                <ul>
                    {% for error in field.errors %}
                        <li>{{ error }}</li>
                    {% endfor %}
                </ul>
            </div>
        {% endif %}
    {% endfor %}
{% endif %}
```


### Arquivo: omaum\templates\includes\form_errors.html

```html
{% if form.errors %}
    {% if form.non_field_errors %}
        <div class="alert alert-danger">
            <strong>Erro:</strong>
            <ul>
                {% for error in form.non_field_errors %}
                    <li>{{ error }}</li>
                {% endfor %}
            </ul>
        </div>
    {% endif %}

    {% for field in form %}
        {% if field.errors %}
            <div class="alert alert-danger">
                <strong>{{ field.label }}:</strong>
                <ul>
                    {% for error in field.errors %}
                        <li>{{ error }}</li>
                    {% endfor %}
                </ul>
            </div>
        {% endif %}
    {% endfor %}
{% endif %}
```


### Arquivo: omaum\templates\includes\form_field.html

```html
<div class="mb-3">
    <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
    {{ field }}
    {% if field.errors %}
        <div class="invalid-feedback d-block">
            {% for error in field.errors %}
                {{ error }}
            {% endfor %}
        </div>
    {% endif %}
    {% if field.help_text %}
        <small class="form-text text-muted">{{ field.help_text }}</small>
    {% endif %}
</div>

```


### Arquivo: omaum\templates\lista_categorias.html

```html
{% extends "base.html" %}

{% block title %}Categorias{% endblock %}

{% block content %}
    <h1>Categorias</h1>
    
    <div class="row mt-4">
        {% for categoria in categorias %}
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ categoria.nome }}</h5>
                        <p class="card-text">{{ categoria.descricao|truncatewords:20 }}</p>
                        <a href="{% url 'core:detalhe_categoria' categoria.id %}" class="btn btn-primary">Ver detalhes</a>
                    </div>
                </div>
            </div>
        {% empty %}
            <div class="col-12">
                <p>Nenhuma categoria encontrada.</p>
            </div>
        {% endfor %}
    </div>
{% endblock %}

```


### Arquivo: omaum\templates\manutencao.html

```html
{% extends "base.html" %}

{% block title %}Sistema em Manutenção{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-8 text-center">
            <div class="alert alert-warning">
                <h2><i class="fas fa-tools"></i> Sistema em Manutenção</h2>
                <p class="lead mt-3">
                    Estamos realizando melhorias no sistema. Por favor, tente novamente mais tarde.
                </p>
                {% if mensagem %}
                    <div class="mt-4">
                        <p>{{ mensagem }}</p>
                    </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}

```


### Arquivo: omaum\templates\painel_controle.html

```html
{% extends "base.html" %}

{% block title %}Painel de Controle{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Painel de Controle</h1>
    
    <div class="row mt-4">
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">Configurações do Sistema</h5>
                </div>
                <div class="card-body">
                    <p><strong>Nome do Sistema:</strong> {{ config.nome_sistema }}</p>
                    <p><strong>Versão:</strong> {{ config.versao }}</p>
                    <p><strong>Última Atualização:</strong> {{ config.data_atualizacao|date:"d/m/Y H:i" }}</p>
                    <p>
                        <strong>Status:</strong>
                        {% if config.manutencao_ativa %}
                            <span class="badge bg-warning">Em Manutenção</span>
                        {% else %}
                            <span class="badge bg-success">Operacional</span>
                        {% endif %}
                    </p>
                    
                    <a href="{% url 'core:atualizar_configuracao' %}" class="btn btn-primary">
                        Editar Configurações
                    </a>
                </div>
            </div>
        </div>
        
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Logs Recentes</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Tipo</th>
                                    <th>Ação</th>
                                    <th>Usuário</th>
                                    <th>Data</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for log in logs_recentes %}
                                <tr>
                                    <td>
                                        {% if log.tipo == 'INFO' %}
                                            <span class="badge bg-info">INFO</span>
                                        {% elif log.tipo == 'AVISO' %}
                                            <span class="badge bg-warning">AVISO</span>
                                        {% elif log.tipo == 'ERRO' %}
                                            <span class="badge bg-danger">ERRO</span>
                                        {% else %}
                                            <span class="badge bg-secondary">{{ log.tipo }}</span>
                                        {% endif %}
                                    </td>
                                    <td>{{ log.acao }}</td>
                                    <td>{{ log.usuario }}</td>
                                    <td>{{ log.data|date:"d/m/Y H:i" }}</td>
                                </tr>
                                {% empty %}
                                <tr>
                                    <td colspan="4" class="text-center">Nenhum log encontrado</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    
                    <a href="{% url 'admin:core_logatividade_changelist' %}" class="btn btn-primary">
                        Ver Todos os Logs
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

```


### Arquivo: omaum\templates\registration\login.html

```html
{% extends "base.html" %}

{% block title %}Entrar no Sistema{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">Bem-vindo ao OMAUM</h4>
                </div>
                <div class="card-body">
                    <p class="text-center mb-4">Sistema de Gestão de Iniciados da OmAum</p>
                    
                    <form method="post" class="needs-validation" novalidate>
                        {% csrf_token %}
                        
                        {% if form.errors %}
                            <div class="alert alert-danger">
                                Seu nome de usuário e senha não correspondem. Por favor, tente novamente.
                            </div>
                        {% endif %}
                        
                        <div class="mb-3">
                            <label for="id_username" class="form-label">Nome de usuário</label>
                            <input type="text" name="username" id="id_username" class="form-control" required>
                            <div class="invalid-feedback">
                                Por favor, informe seu nome de usuário.
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label for="id_password" class="form-label">Senha</label>
                            <input type="password" name="password" id="id_password" class="form-control" required>
                            <div class="invalid-feedback">
                                Por favor, informe sua senha.
                            </div>
                        </div>
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary">Entrar</button>
                        </div>
                    </form>
                </div>
                <div class="card-footer text-center text-muted">
                    <small>© {% now "Y" %} OMAUM - Todos os direitos reservados</small>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
// Validação do formulário
(function() {
    'use strict';
    window.addEventListener('load', function() {
        var forms = document.getElementsByClassName('needs-validation');
        var validation = Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();
</script>
{% endblock %}

```


### Arquivo: omaum\templates\registration\registro.html

```html
{% extends 'base.html' %}
{% load widget_tweaks %}

{% block title %}Registrar - OMAUM{% endblock %}
{% block content %}
<div class="container mt-5">
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card">
        <div class="card-header">
          <h4 class="mb-0">Registrar</h4>
        </div>
        <div class="card-body">
          <p class="mb-3">Por favor, preencha os campos abaixo para criar uma nova conta.</p>
          <form method="post" class="needs-validation" novalidate>
            {% csrf_token %}

            {% if form.errors %}
              <div class="alert alert-danger">
                Por favor, corrija os erros abaixo.
              </div>
            {% endif %}

            {% for field in form %}
              <div class="mb-3">
                <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                {{ field|add_class:"form-control" }}
                {% if field.errors %}
                  <div class="invalid-feedback d-block">
                    {% for error in field.errors %}
                      {{ error }}
                    {% endfor %}
                  </div>
                {% endif %}
              </div>
            {% endfor %}

            <div class="d-grid">
              <button type="submit" class="btn btn-primary">Registrar</button>
            </div>
          </form>

          <div class="mt-3 text-center">
            <p>Já tem uma conta? <a href="{% url 'login' %}">Faça login aqui</a></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```
