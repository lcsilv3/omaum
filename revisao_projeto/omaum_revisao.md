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
from core import views as core_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('alunos/', include('alunos.urls', namespace='alunos')),
    path('cursos/', include('cursos.urls', namespace='cursos')),
    path('turmas/', include('turmas.urls', namespace='turmas')),
    path('matriculas/', include('matriculas.urls', namespace='matriculas')),
    path('frequencias/', include('frequencias.urls', namespace='frequencias')),
    path('atividades/', include('atividades.urls', namespace='atividades')),
    path('presencas/', include('presencas.urls', namespace='presencas')),
    path('iniciacoes/', include('iniciacoes.urls', namespace='iniciacoes')),
    path('cargos/', include('cargos.urls', namespace='cargos')),
    path('punicoes/', include('punicoes.urls', namespace='punicoes')),
    path('relatorios/', include('relatorios.urls', namespace='relatorios')),
    path('notas/', include('notas.urls', namespace='notas')),
    path('pagamentos/', include('pagamentos.urls', namespace='pagamentos')),
    # URLs de autenticação do Django
    path('accounts/', include('django.contrib.auth.urls')),
    # Adicionar rota para 'entrar/'
    path('entrar/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # Adicionar rota para 'register'
    path('register/', core_views.registro_usuario, name='register'),
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




### Arquivo: omaum\templates\base copy.html

html
<!DOCTYPE html>
{% load static %}
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <!-- Atualização do título conforme recomendado -->
    <title>{% block title %}SGI - Sistema de Gestão Integrada da OmAum{% endblock %}</title>
    
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
                <!-- Atualização do texto da marca para refletir o novo nome -->
                <a class="navbar-brand" href="{% url 'core:pagina_inicial' %}">
                    <img src="{% static 'img/logo.png' %}" alt="OMAUM Logo" height="40">
                    SGI - Om-Aum                </a>
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
                                <a class="nav-link {% if request.resolver_match.app_name == 'presencas' %}active{% endif %}"
                                   href="{% url 'presencas:listar_presencas' %}">
                                    <i class="fas fa-clipboard-check"></i> Presenças
                                </a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link {% if request.resolver_match.app_name == 'frequencias' %}active{% endif %}"
                                   href="{% url 'frequencias:listar_frequencias' %}">
                                    <i class="fas fa-check-square"></i> Frequências
                                </a>
                            </li>
                            <!-- Adicionando itens de menu que estavam no outro template -->
                            <li class="nav-item">
                                <a class="nav-link {% if request.resolver_match.app_name == 'iniciacoes' %}active{% endif %}"
                                   href="{% url 'iniciacoes:listar_iniciacoes' %}">
                                    <i class="fas fa-graduation-cap"></i> Iniciações
                                </a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link {% if request.resolver_match.app_name == 'cargos' %}active{% endif %}"
                                   href="{% url 'cargos:listar_cargos' %}">
                                    <i class="fas fa-id-badge"></i> Cargos
                                </a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link {% if request.resolver_match.app_name == 'notas' %}active{% endif %}"
                                   href="{% url 'notas:listar_notas' %}">
                                    <i class="fas fa-star"></i> Notas
                                </a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link {% if request.resolver_match.app_name == 'pagamentos' %}active{% endif %}"
                                   href="{% url 'pagamentos:listar_pagamentos' %}">
                                    <i class="fas fa-money-bill-wave"></i> Pagamentos
                                </a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link {% if request.resolver_match.app_name == 'punicoes' %}active{% endif %}"
                                   href="{% url 'punicoes:listar_punicoes' %}">
                                    <i class="fas fa-gavel"></i> Punições
                                </a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link {% if request.resolver_match.app_name == 'relatorios' %}active{% endif %}"
                                   href="{% url 'relatorios:listar_relatorios' %}">
                                    <i class="fas fa-chart-bar"></i> Relatórios
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
            <!-- Atualização do texto do rodapé para refletir o novo nome -->
            <span class="text-muted">© {% now "Y" %} SGI - Sistema de Gestão Integrada da OmAum</span>
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




### Arquivo: omaum\templates\base.html

html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}SGI - OmAum{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    {% block extra_css %}{% endblock %}
    <style>
        body {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        main {
            flex: 1;
        }
        .navbar-brand img {
            width: 50px; /* Aumentando o tamanho do ícone */
            height: auto;
        }
        .navbar-brand {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        .brand-text {
            font-size: 0.8rem;
            margin-top: 2px;
        }
        .footer {
            background-color: #f8f9fa;
            padding: 1rem 0;
            margin-top: auto;
        }
        
        /* Adicione estas regras para os links dourados na navbar */
        .navbar-dark .navbar-nav .nav-link {
            color: gold !important; /* Cor dourada para todos os links */
        }
        .navbar-dark .navbar-nav .nav-link:hover {
            color: #FFD700 !important; /* Dourado mais brilhante no hover */
            text-decoration: underline;
        }
        .navbar-dark .navbar-brand {
            color: gold !important; /* Cor dourada para o logo/texto da marca */
        }
        .navbar-dark .navbar-toggler-icon {
            background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba(255, 215, 0, 1)' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e") !important;
        }
    </style>
</head>
<body>
    <header>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand" href="/">
                    <img src="/static/img/logo.png" alt="Logo OmAum">
                    <span class="brand-text">SGI - Om-Aum</span>
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        {% if user.is_authenticated %}
                            <!-- Gestão Acadêmica -->
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="#" id="academicoDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                    Gestão Acadêmica
                                </a>
                                <ul class="dropdown-menu" aria-labelledby="academicoDropdown">
                                    <li><a class="dropdown-item" href="{% url 'cursos:listar_cursos' %}">Cursos</a></li>
                                    <li><a class="dropdown-item" href="{% url 'alunos:listar_alunos' %}">Alunos</a></li>
                                    <li><a class="dropdown-item" href="{% url 'turmas:listar_turmas' %}">Turmas</a></li>
                                </ul>
                            </li>
                            
                            <!-- Frequência e Presença -->
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="#" id="frequenciaDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                    Frequência e Presença
                                </a>
                                <ul class="dropdown-menu" aria-labelledby="frequenciaDropdown">
                                    <li><a class="dropdown-item" href="{% url 'atividades:listar_atividades_academicas' %}">Atividades Acadêmicas</a></li>
                                    <li><a class="dropdown-item" href="{% url 'atividades:listar_atividades_ritualisticas' %}">Atividades Ritualísticas</a></li>
                                    <li><a class="dropdown-item" href="{% url 'presencas:listar_presencas' %}">Presenças</a></li>
                                    <li><a class="dropdown-item" href="{% url 'frequencias:listar_frequencias' %}">Frequências</a></li>
                                </ul>
                            </li>
                            
                            <!-- Processos Iniciáticos -->
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="#" id="iniciaticosDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                    Processos Iniciáticos
                                </a>
                                <ul class="dropdown-menu" aria-labelledby="iniciaticosDropdown">
                                    <li><a class="dropdown-item" href="{% url 'iniciacoes:listar_iniciacoes' %}">Iniciações</a></li>
                                    <li><a class="dropdown-item" href="{% url 'punicoes:listar_punicoes' %}">Punições</a></li>
                                    <li><a class="dropdown-item" href="{% url 'cargos:listar_cargos' %}">Cargos Administrativos</a></li>
                                </ul>
                            </li>
                            
                            <!-- Avaliação e Financeiro -->
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="#" id="avaliacaoDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                    Avaliação e Financeiro
                                </a>
                                <ul class="dropdown-menu" aria-labelledby="avaliacaoDropdown">
                                    <li><a class="dropdown-item" href="{% url 'notas:listar_notas' %}">Notas</a></li>
                                    <li><a class="dropdown-item" href="{% url 'pagamentos:listar_pagamentos' %}">Pagamentos</a></li>
                                    <li><a class="dropdown-item" href="{% url 'pagamentos:pagamentos_por_turma' %}">Pagamentos por Turma</a></li>
                                    <li><a class="dropdown-item" href="{% url 'pagamentos:relatorio_financeiro' %}">Relatório Financeiro</a></li>
                                </ul>
                            </li>
                            
                            <!-- Relatórios e Análises -->
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="#" id="relatoriosDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                    Relatórios e Análises
                                </a>
                                <ul class="dropdown-menu" aria-labelledby="relatoriosDropdown">
                                    <li><a class="dropdown-item" href="{% url 'relatorios:listar_relatorios' %}">Relatórios</a></li>
                                </ul>
                            </li>
                        {% endif %}
                    </ul>
                    <ul class="navbar-nav">
                        {% if user.is_authenticated %}
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="#" id="notificacoesDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                    <i class="fas fa-bell"></i>
                                    {% if pagamentos_atrasados_count > 0 %}
                                        <span class="badge bg-danger">{{ pagamentos_atrasados_count }}</span>
                                    {% endif %}
                                </a>
                                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="notificacoesDropdown">
                                    <li><h6 class="dropdown-header">Notificações</h6></li>
                                    {% if pagamentos_atrasados %}
                                        {% for pagamento in pagamentos_atrasados|slice:":5" %}
                                            <li>
                                                <a class="dropdown-item text-danger" href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}">
                                                    <i class="fas fa-exclamation-circle"></i>
                                                    Pagamento atrasado: {{ pagamento.aluno.nome }} - R$ {{ pagamento.valor|floatformat:2 }}
                                                    <small class="d-block text-muted">Vencido há {{ pagamento.dias_atraso }} dias</small>
                                                </a>
                                            </li>
                                        {% endfor %}
                                        {% if pagamentos_atrasados_count > 5 %}
                                            <li><hr class="dropdown-divider"></li>
                                            <li>
                                                <a class="dropdown-item text-center" href="{% url 'pagamentos:relatorio_financeiro' %}?filtro=atrasados">
                                                    Ver todos os {{ pagamentos_atrasados_count }} pagamentos atrasados
                                                </a>
                                            </li>
                                        {% endif %}
                                    {% else %}
                                        <li><a class="dropdown-item text-muted">Não há notificações</a></li>
                                    {% endif %}
                                </ul>
                            </li>
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                    <i class="fas fa-user"></i> {{ user.username }}
                                </a>
                                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                                    <!-- Removendo o link para o perfil que não existe -->
                                    <li><a class="dropdown-item" href="{% url 'admin:index' %}">Administração</a></li>
                                    <!-- Removendo o link para alterar senha que pode não existir -->
                                    <li><hr class="dropdown-divider"></li>
                                    
                                    <li>
                                        
                                        <form method="post" action="{% url 'logout' %}" style="display: inline;">
                                            {% csrf_token %}
                                            <button type="submit" class="dropdown-item" style="background: none; border: none; width: 100%; text-align: left;">Sair</button>
                                        </form>
                                    </li>
                                </ul>
                            </li>
                        {% else %}
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'login' %}">Entrar</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'register' %}">Registrar</a>
                            </li>
                        {% endif %}
                    </ul>
                </div>
            </div>
        </nav>
    </header>
    <main class="py-4">
        <div class="container">
            {% block content %}{% endblock %}
        </div>
    </main>
    <footer class="footer">
        <div class="container text-center">
            <p class="mb-0">&copy; {% now "Y" %} SGI - OmAum. Todos os direitos reservados.</p>
        </div>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
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
{% extends "base.html" %}
{% load static %}

{% block title %}SGI - Sistema de Gestão Integrada da OmAum{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="jumbotron bg-light p-4 rounded">
        <h1 class="display-4">Bem-vindo ao SGI - OmAum</h1>
        <p class="lead">Sistema de Gestão Integrada da OmAum - Gerenciamento completo de alunos, cursos, turmas e atividades.</p>
        <hr class="my-4">
        <p>Selecione um dos módulos abaixo para começar.</p>
        <div class="alert alert-info text-center">
            <i class="fas fa-arrow-down"></i> Role a página para ver todos os módulos disponíveis <i class="fas fa-arrow-down"></i>
        </div>
    </div>

    {% if user.is_authenticated %}
        <!-- Seção: Gestão Acadêmica -->
        <div class="mt-4 mb-3">
            <h3 class="border-bottom pb-2">Gestão Acadêmica</h3>
            <div class="row">
                <!-- Módulo de Cursos -->
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">
                                <i class="fas fa-book text-success"></i> Cursos
                            </h5>
                            <p class="card-text">Cadastro e gerenciamento de cursos oferecidos pela instituição.</p>
                            <a href="{% url 'cursos:listar_cursos' %}" class="btn btn-success">
                                <i class="fas fa-book-open"></i> Acessar Cursos
                            </a>
                        </div>
                    </div>
                </div>
                <!-- Módulo de Alunos -->
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">
                                <i class="fas fa-user-graduate text-primary"></i> Alunos
                            </h5>
                            <p class="card-text">Gerenciamento completo de alunos, incluindo cadastro, edição e consulta.</p>
                            <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-primary">
                                <i class="fas fa-users"></i> Acessar Alunos
                            </a>
                        </div>
                    </div>
                </div>
                <!-- Módulo de Turmas -->
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">
                                <i class="fas fa-users text-info"></i> Turmas
                            </h5>
                            <p class="card-text">Gerenciamento de turmas, incluindo horários, instrutores e alunos.</p>
                            <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-info">
                                <i class="fas fa-chalkboard-teacher"></i> Acessar Turmas
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="text-center mt-2 mb-4">
                <span class="badge bg-secondary">Role para ver mais módulos <i class="fas fa-arrow-down"></i></span>
            </div>
        </div>

        <!-- Seção: Frequência e Presença -->
        <div class="mt-4 mb-3">
            <h3 class="border-bottom pb-2">Frequência e Presença</h3>
            <div class="row">
                <!-- Módulo de Atividades (mudando de vermelho para rosa) -->
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">
                                <i class="fas fa-calendar-alt text-pink"></i> Atividades
                            </h5>
                            <p class="card-text">Gerenciamento de atividades acadêmicas e ritualísticas.</p>
                            <div class="d-flex flex-column">
                                <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-pink mb-2">
                                    <i class="fas fa-school"></i> Atividades Acadêmicas
                                </a>
                                <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-outline-pink">
                                    <i class="fas fa-pray"></i> Atividades Ritualísticas
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Módulo de Presenças -->
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">
                                <i class="fas fa-clipboard-check text-secondary"></i> Presenças
                            </h5>
                            <p class="card-text">Controle de presenças em atividades e aulas.</p>
                            <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
                                <i class="fas fa-clipboard-check"></i> Acessar Presenças
                            </a>
                        </div>
                    </div>
                </div>
                <!-- Módulo de Frequências -->
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">
                                <i class="fas fa-check-square text-primary"></i> Frequências
                            </h5>
                            <p class="card-text">Registro e consulta de frequências dos alunos.</p>
                            <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-primary">
                                <i class="fas fa-check-square"></i> Acessar Frequências
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="text-center mt-2 mb-4">
                <span class="badge bg-secondary">Continue rolando <i class="fas fa-arrow-down"></i></span>
            </div>
        </div>

        <!-- Seção: Processos Iniciáticos -->
        <div class="mt-4 mb-3">
            <h3 class="border-bottom pb-2">Processos Iniciáticos</h3>
            <div class="row">
                <!-- Módulo de Iniciações -->
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">
                                <i class="fas fa-graduation-cap text-success"></i> Iniciações
                            </h5>
                            <p class="card-text">Gerenciamento de iniciações e processos iniciáticos.</p>
                            <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-success">
                                <i class="fas fa-graduation-cap"></i> Acessar Iniciações
                            </a>
                        </div>
                    </div>
                </div>
                <!-- Módulo de Punições (mudando de vermelho para roxo claro) -->
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">
                                <i class="fas fa-gavel text-purple"></i> Punições
                            </h5>
                            <p class="card-text">Registro e gerenciamento de punições disciplinares.</p>
                            <a href="{% url 'punicoes:listar_punicoes' %}" class="btn btn-purple">
                                <i class="fas fa-gavel"></i> Acessar Punições
                            </a>
                        </div>
                    </div>
                </div>
                <!-- Módulo de Cargos Administrativos -->
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">
                                <i class="fas fa-id-badge text-info"></i> Cargos Administrativos
                            </h5>
                            <p class="card-text">Gerenciamento de cargos e funções administrativas.</p>
                            <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-info">
                                <i class="fas fa-id-badge"></i> Acessar Cargos
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="text-center mt-2 mb-4">
                <span class="badge bg-secondary">Mais módulos abaixo <i class="fas fa-arrow-down"></i></span>
            </div>
        </div>

        <!-- Seção: Avaliação e Financeiro -->
        <div class="mt-4 mb-3">
            <h3 class="border-bottom pb-2">Avaliação e Financeiro</h3>
            <div class="row">
                <!-- Módulo de Notas -->
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">
                                <i class="fas fa-star text-warning"></i> Notas
                            </h5>
                            <p class="card-text">Gerenciamento de notas dos alunos nos cursos.</p>
                            <a href="{% url 'notas:listar_notas' %}" class="btn btn-warning">
                                <i class="fas fa-star"></i> Acessar Notas
                            </a>
                        </div>
                    </div>
                </div>
                <!-- Módulo de Pagamentos -->
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">
                                <i class="fas fa-money-bill-wave text-success"></i> Pagamentos
                            </h5>
                            <p class="card-text">Gerenciamento de pagamentos dos alunos.</p>
                            <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-success">
                                <i class="fas fa-money-bill-wave"></i> Acessar Pagamentos
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Seção: Relatórios e Análises -->
        <div class="mt-4 mb-3">
            <h3 class="border-bottom pb-2">Relatórios e Análises</h3>
            <div class="row">
                <!-- Módulo de Relatórios -->
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">
                                <i class="fas fa-chart-bar text-secondary"></i> Relatórios
                            </h5>
                            <p class="card-text">Geração de relatórios e estatísticas do sistema.</p>
                            <a href="{% url 'relatorios:listar_relatorios' %}" class="btn btn-secondary">
                                <i class="fas fa-chart-bar"></i> Acessar Relatórios
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Botão para voltar ao topo -->
        <div class="text-center my-4">
            <a href="#" class="btn btn-outline-primary" onclick="window.scrollTo({top: 0, behavior: 'smooth'}); return false;">
                <i class="fas fa-arrow-up"></i> Voltar ao topo
            </a>
        </div>
    {% else %}
        <div class="col-12 text-center mt-4">
            <div class="alert alert-info">
                <h4>Bem-vindo ao Sistema de Gestão Integrada da OmAum</h4>
                <p>Por favor, faça login para acessar o sistema.</p>
                <a href="{% url 'login' %}" class="btn btn-primary">
                    <i class="fas fa-sign-in-alt"></i> Entrar
                </a>
            </div>
        </div>
    {% endif %}
</div>

<style>
    /* Cores personalizadas mais suaves para substituir o vermelho */
    .text-pink {
        color: #e83e8c !important;
    }
    .btn-pink {
        background-color: #e83e8c !important;
        border-color: #e83e8c !important;
        color: white !important;
    }
    .btn-outline-pink {
        color: #e83e8c !important;
        border-color: #e83e8c !important;
    }
    .btn-outline-pink:hover {
        background-color: #e83e8c !important;
        color: white !important;
    }
    
    .text-purple {
        color: #6f42c1 !important;
    }
    .btn-purple {
        background-color: #6f42c1 !important;
        border-color: #6f42c1 !important;
        color: white !important;
    }
</style>
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



### Arquivo: omaum\templates\includes\action_buttons.html

html
{% comment %}
Componente para botões de ação padronizados
Uso: {% include 'includes/action_buttons.html' with type="list|detail|form" %}
{% endcomment %}

{% if type == "list" %}
<div class="actions-container">
    <a href="javascript:history.back()" class="btn btn-secondary">
        <i class="fas fa-arrow-left"></i> Voltar
    </a>
    <a href="{{ create_url }}" class="btn btn-primary">
        <i class="fas fa-plus"></i> Novo {{ entity_name }}
    </a>
</div>
{% elif type == "detail" %}
<div class="actions-container">
    <a href="{{ list_url }}" class="btn btn-secondary">
        <i class="fas fa-arrow-left"></i> Voltar
    </a>
    <div class="actions-container-end">
        <a href="{{ edit_url }}" class="btn btn-warning">
            <i class="fas fa-edit"></i> Editar
        </a>
        {% if delete_url %}
        <a href="{{ delete_url }}" class="btn btn-danger">
            <i class="fas fa-trash"></i> Excluir
        </a>
        {% endif %}
    </div>
</div>
{% elif type == "form" %}
<div class="actions-container">
    <a href="{{ cancel_url|default:'javascript:history.back()' }}" class="btn btn-secondary">
        <i class="fas fa-times"></i> Cancelar
    </a>
    <button type="submit" class="btn btn-primary">
        <i class="fas fa-save"></i> {{ submit_text|default:'Salvar' }}
    </button>
</div>
{% endif %}



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



### Arquivo: omaum\templates\sidebar.html

html
<!-- Adicionar esta seção ao menu lateral ou menu principal -->
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" id="pagamentosDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
        <i class="fas fa-money-bill-wave"></i> Pagamentos
    </a>
    <ul class="dropdown-menu" aria-labelledby="pagamentosDropdown">
        <li>
            <a class="dropdown-item" href="{% url 'pagamentos:listar_pagamentos' %}">
                <i class="fas fa-list"></i> Listar Todos
            </a>
        </li>
        <li>
            <a class="dropdown-item" href="{% url 'pagamentos:criar_pagamento' %}">
                <i class="fas fa-plus"></i> Novo Pagamento
            </a>
        </li>
        <li>
            <a class="dropdown-item" href="{% url 'pagamentos:pagamentos_por_turma' %}">
                <i class="fas fa-users"></i> Por Turma
            </a>
        </li>
        <li>
            <a class="dropdown-item" href="{% url 'pagamentos:relatorio_financeiro' %}">
                <i class="fas fa-chart-line"></i> Relatório Financeiro
            </a>
        </li>
        <li>
            <a class="dropdown-item" href="{% url 'pagamentos:exportar_pagamentos_pdf' %}">
                <i class="fas fa-file-pdf"></i> Exportar PDF
            </a>
        </li>
    </ul>
</li>

