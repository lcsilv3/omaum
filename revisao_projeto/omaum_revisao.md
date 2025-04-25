# Revisão da Funcionalidade: omaum

## Arquivos urls.py:


### Arquivo: omaum\urls.py

python
"""
Configuração de URLs do projeto OMAUM.

A lista `urlpatterns` roteia URLs para views. Para mais informações, consulte:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("alunos/", include("alunos.urls", namespace="alunos")),
    path("atividades/", include("atividades.urls", namespace="atividades")),
    path("cargos/", include("cargos.urls", namespace="cargos")),
    path("cursos/", include("cursos.urls", namespace="cursos")),
    path("frequencias/", include("frequencias.urls", namespace="frequencias")),
    path("iniciacoes/", include("iniciacoes.urls", namespace="iniciacoes")),
    path("matriculas/", include("matriculas.urls", namespace="matriculas")),
    path("notas/", include("notas.urls", namespace="notas")),
    path("pagamentos/", include("pagamentos.urls", namespace="pagamentos")),
    path("presencas/", include("presencas.urls", namespace="presencas")),
    path("punicoes/", include("punicoes.urls", namespace="punicoes")),
    path("relatorios/", include("relatorios.urls", namespace="relatorios")),
    path("turmas/", include("turmas.urls", namespace="turmas")),
    # URLs de autenticação do Django
    path('accounts/', include('django.contrib.auth.urls')),
]

# Configurações para ambiente de desenvolvimento
if settings.DEBUG:
    # Adicionar URLs do Django Debug Toolbar
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
    # Servir arquivos de mídia em desenvolvimento
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



## Arquivos de Template:


### Arquivo: omaum\templates\403.html

html
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



### Arquivo: omaum\templates\404.html

html
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



### Arquivo: omaum\templates\500.html

html
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



### Arquivo: omaum\templates\atualizar_configuracao.html

html
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




### Arquivo: omaum\templates\base.html

html
<!DOCTYPE html>
{% load static %}
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>{% block title %}OMAUM - Sistema de Gestão de Iniciados{% endblock %}</title>
    
    <!-- Favicon -->
    <link rel="shortcut icon" href="{% static 'img/favicon.ico' %}" type="image/x-icon">
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- FontAwesome 5 -->
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.15.4/css/all.css">
    
    <!-- Select2 CSS com tema Bootstrap 4 -->
    <link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@ttskch/select2-bootstrap4-theme@1.5.2/dist/select2-bootstrap4.min.css">
    
    <!-- CSS Global do Projeto -->
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
    
    <!-- CSS de componentes globais -->
    <link rel="stylesheet" href="{% static 'css/components/dias-semana.css' %}">
    
    <!-- CSS específico da página -->
    {% block extra_css %}{% endblock %}
    
    <!-- jQuery (obrigatório para Bootstrap JS, Select2 e jQuery Mask) -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    
    <!-- Pré-carregamento de scripts essenciais -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" defer></script>
    <script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.full.min.js" defer></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js" defer></script>
    
    <!-- Scripts adicionais da página no head -->
    {% block extra_head %}{% endblock %}
</head>
<body>
    <!-- Cabeçalho/Barra de Navegação -->
    <header>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand" href="{% url 'core:pagina_inicial' %}">
                    <img src="{% static 'img/logo.png' %}" alt="OMAUM Logo" height="40">
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" 
                        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <a class="nav-link {% if request.resolver_match.app_name == 'core' and request.resolver_match.url_name == 'pagina_inicial' %}active{% endif %}" 
                               href="{% url 'core:pagina_inicial' %}">
                                <i class="fas fa-home"></i> Início
                            </a>
                        </li>
                        
                        {% if user.is_authenticated %}
                            <li class="nav-item">
                                <a class="nav-link {% if request.resolver_match.app_name == 'alunos' %}active{% endif %}" 
                                   href="{% url 'alunos:listar_alunos' %}">
                                    <i class="fas fa-user-graduate"></i> Alunos
                                </a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link {% if request.resolver_match.app_name == 'cursos' %}active{% endif %}" 
                                   href="{% url 'cursos:listar_cursos' %}">
                                    <i class="fas fa-book"></i> Cursos
                                </a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link {% if request.resolver_match.app_name == 'turmas' %}active{% endif %}" 
                                   href="{% url 'turmas:listar_turmas' %}">
                                    <i class="fas fa-users"></i> Turmas
                                </a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link {% if request.resolver_match.app_name == 'matriculas' %}active{% endif %}" 
                                   href="{% url 'matriculas:listar_matriculas' %}">
                                    <i class="fas fa-clipboard-list"></i> Matrículas
                                </a>
                            </li>
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownAtividades" role="button"
                                   data-bs-toggle="dropdown" aria-expanded="false">
                                   <i class="fas fa-calendar-alt"></i> Atividades
                                </a>
                                <ul class="dropdown-menu" aria-labelledby="navbarDropdownAtividades">
                                    <li>
                                        <a class="dropdown-item" href="{% url 'atividades:listar_atividades_academicas' %}">
                                            <i class="fas fa-school"></i> Acadêmicas
                                        </a>
                                    </li>
                                    <li>
                                        <a class="dropdown-item" href="{% url 'atividades:listar_atividades_ritualisticas' %}">
                                            <i class="fas fa-pray"></i> Ritualísticas
                                        </a>
                                    </li>
                                </ul>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link {% if request.resolver_match.app_name == 'frequencias' %}active{% endif %}" 
                                   href="{% url 'frequencias:listar_frequencias' %}">
                                    <i class="fas fa-check-square"></i> Frequências
                                </a>
                            </li>
                        {% endif %}
                    </ul>
                    
                    <ul class="navbar-nav">
                        {% if user.is_authenticated %}
                            {% if user.is_staff %}
                                <li class="nav-item">
                                    <a class="nav-link" href="{% url 'core:painel_controle' %}">
                                        <i class="fas fa-cog"></i> Painel de Controle
                                    </a>
                                </li>
                            {% endif %}
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button"
                                   data-bs-toggle="dropdown" aria-expanded="false">
                                   <i class="fas fa-user-circle"></i> {{ user.username }}
                                </a>
                                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                                    <li><a class="dropdown-item" href="#">Meu Perfil</a></li>
                                    <li><hr class="dropdown-divider"></li>
                                    <li>
                                        <form method="post" action="{% url 'core:sair' %}" class="d-inline">
                                            {% csrf_token %}
                                            <button type="submit" class="dropdown-item">
                                                <i class="fas fa-sign-out-alt"></i> Sair
                                            </button>
                                        </form>
                                    </li>
                                </ul>
                            </li>
                        {% else %}
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'core:entrar' %}">
                                    <i class="fas fa-sign-in-alt"></i> Entrar
                                </a>
                            </li>
                        {% endif %}
                    </ul>
                </div>
            </div>
        </nav>
    </header>
    
    <!-- Mensagens do sistema (flash messages) -->
    <div class="message-container">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
                </div>
            {% endfor %}
        {% endif %}
    </div>
    
    <!-- Conteúdo principal -->
    <main id="main-content" class="py-4">
        {% block content %}{% endblock %}
    </main>
    
    <!-- Rodapé -->
    <footer class="footer mt-auto py-3 bg-light">
        <div class="container text-center">
            <span class="text-muted">© {% now "Y" %} OMAUM - Sistema de Gestão de Iniciados</span>
        </div>
    </footer>
    
    <!-- Scripts de componentes globais -->
    <script src="{% static 'js/modules/dias-semana.js' %}"></script>
    
    <!-- Scripts específicos da página -->
    {% block extra_js %}{% endblock %}
    
    <!-- Script global do sistema -->
    <script>
        // Inicialização global do site
        document.addEventListener('DOMContentLoaded', function() {
            // Inicializar tooltips do Bootstrap
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
            
            // Inicializar popovers do Bootstrap
            var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
            var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
                return new bootstrap.Popover(popoverTriggerEl);
            });
            
            // Verificação CSRF para AJAX
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            
            // Configuração global do AJAX para incluir o token CSRF
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    }
                }
            });
            
            // Verificação periódica do token CSRF para sessões longas
            setInterval(function() {
                $.get("{% url 'core:csrf_check' %}");
            }, 3600000); // A cada hora
            
            // Aplicar máscaras globais
            if (typeof $.fn.mask === 'function') {
                $('.cpf-mask').mask('000.000.000-00');
                $('.cep-mask').mask('00000-000');
                $('.phone-mask').mask('(00) 0000-00009');
                $('.phone-mask').blur(function(event) {
                    if($(this).val().length == 15){
                        $('.phone-mask').mask('(00) 00000-0009');
                    } else {
                        $('.phone-mask').mask('(00) 0000-00009');
                    }
                });
                $('.date-mask').mask('00/00/0000');
                $('.time-mask').mask('00:00 às 00:00');
            }
            
            // Inicialização global do Select2
            if (typeof $.fn.select2 === 'function') {
                $('.select2').select2({
                    theme: 'bootstrap4',
                    width: '100%'
                });
            }
        });
    </script>
    <script src="{% static 'js/inicializar_select2.js' %}"></script>
</body>
</html>




### Arquivo: omaum\templates\csrf_test.html

html
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





### Arquivo: omaum\templates\home.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}OMAUM - Página Inicial{% endblock %}

{% block content %}
<link rel="stylesheet" href="{% static 'css/styles.css' %}">
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
                    <a href="{% url 'relatorios:listar_relatorios' %}" class="btn btn-primary">Acessar</a>
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




### Arquivo: omaum\templates\home_old.html

html
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



### Arquivo: omaum\templates\includes\form_error.html

html
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



### Arquivo: omaum\templates\includes\form_errors.html

html
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



### Arquivo: omaum\templates\includes\form_field.html

html
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




### Arquivo: omaum\templates\lista_categorias.html

html
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




### Arquivo: omaum\templates\listar_alunos.html

html
{% extends 'base.html' %}

{% block title %}Lista de Alunos{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Cabeçalho com título e botões na mesma linha -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Lista de Alunos</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'alunos:criar_aluno' %}" class="btn btn-primary">Novo Aluno</a>
            <a href="{% url 'alunos:exportar_alunos' %}" class="btn btn-success">Exportar CSV</a>
            <a href="{% url 'alunos:importar_alunos' %}" class="btn btn-info">Importar CSV</a>
            <a href="{% url 'alunos:relatorio_alunos' %}" class="btn btn-warning">Relatório</a>
            <a href="{% url 'alunos:dashboard' %}" class="btn btn-dark">Dashboard</a>
        </div>
    </div>
    
    <!-- Barra de busca e filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <form method="get" class="row g-3">
                <div class="col-md-6">
                    <input type="text" name="q" class="form-control" placeholder="Buscar por nome, CPF ou email..." value="{{ query }}">
                </div>
                <div class="col-md-4">
                    <select name="curso" class="form-select" title="Selecione um curso" aria-label="Selecione um curso">
                        <option value="">Todos os cursos</option>
                        {% for curso in cursos %}
                            <option value="{{ curso.codigo_curso }}" {% if curso.codigo_curso|stringformat:"s" == curso_selecionado %}selected{% endif %}>{{ curso.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn btn-primary w-100">Filtrar</button>
                </div>
            </form>
        </div>
        <div class="card-body">
            {% if error_message %}
            <div class="alert alert-danger">
                {{ error_message }}
            </div>
            {% endif %}
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>CPF</th>
                            <th>Nº Iniciático</th>
                            <th>Email</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for aluno in alunos %}
                            <tr>
                                <td>
                                    <div class="d-flex align-items-center">
                                        {% if aluno.foto %}
                                            <img src="{{ aluno.foto.url }}" alt="Foto de {{ aluno.nome }}" 
                                                 class="rounded-circle me-2" width="40" height="40" 
                                                 style="object-fit: cover;">
                                        {% else %}
                                            <div class="rounded-circle bg-secondary me-2 d-flex align-items-center justify-content-center" 
                                                 style="width: 40px; height: 40px; color: white;">
                                                {{ aluno.nome|first|upper }}
                                            </div>
                                        {% endif %}
                                        {{ aluno.nome }}
                                    </div>
                                </td>
                                <td>{{ aluno.cpf }}</td>
                                <td>{{ aluno.numero_iniciatico|default:"N/A" }}</td>
                                <td>{{ aluno.email }}</td>
                                <td>
                                    {% if aluno.cpf %}
                                        <a href="{% url 'alunos:detalhar_aluno' aluno.cpf %}" class="btn btn-sm btn-info">Detalhes</a>
                                        <a href="{% url 'alunos:editar_aluno' aluno.cpf %}" class="btn btn-sm btn-warning">Editar</a>
                                        <a href="{% url 'alunos:excluir_aluno' aluno.cpf %}" class="btn btn-sm btn-danger">Excluir</a>
                                    {% else %}
                                        <span class="text-muted">CPF não disponível</span>
                                    {% endif %}
                                </td>
                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="5" class="text-center">
                                    <p class="my-3">Nenhum aluno cadastrado.</p>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer">
            <p class="text-muted mb-0">Total: {{ alunos.count|default:"0" }} aluno(s)</p>
            {% if page_obj.has_other_pages %}
                <nav aria-label="Paginação">
                    <ul class="pagination justify-content-center mb-0">
                        {% if page_obj.has_previous %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.previous_page_number }}&q={{ query }}&curso={{ curso_selecionado }}">Anterior</a>
                            </li>
                        {% else %}
                            <li class="page-item disabled">
                                <span class="page-link">Anterior</span>
                            </li>
                        {% endif %}

                        {% for num in page_obj.paginator.page_range %}
                            {% if page_obj.number == num %}
                                <li class="page-item active">
                                    <span class="page-link">{{ num }}</span>
                                </li>
                            {% else %}
                                <li class="page-item">
                                    <a class="page-link" href="?page={{ num }}&q={{ query }}&curso={{ curso_selecionado }}">{{ num }}</a>
                                </li>
                            {% endif %}
                        {% endfor %}

                        {% if page_obj.has_next %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.next_page_number }}&q={{ query }}&curso={{ curso_selecionado }}">Próxima</a>
                            </li>
                        {% else %}
                            <li class="page-item disabled">
                                <span class="page-link">Próxima</span>
                            </li>
                        {% endif %}
                    </ul>
                </nav>
            {% endif %}
        </div>    </div>
</div>
{% endblock %}




### Arquivo: omaum\templates\manutencao.html

html
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




### Arquivo: omaum\templates\painel_controle.html

html
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




### Arquivo: omaum\templates\registration\login.html

html
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




### Arquivo: omaum\templates\registration\registro.html

html
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

