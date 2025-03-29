# Código da Funcionalidade: templates
*Gerado automaticamente*



## templates\base.html

html
{% load static %}
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Sistema{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'core:pagina_inicial' %}">OMAUM</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" title="Menu de navegação">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    {% if user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'alunos:listar' %}">Alunos</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'atividades:atividade_academica_list' %}">Atividades Acadêmicas</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'atividades:atividade_ritualistica_list' %}">Atividades Ritualísticas</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'turmas:listar_turmas' %}">Turmas</a>
                          </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/presencas/lista/">Presenças</a>
                        </li>
                        <!-- Add more navigation items for other functionalities -->
                        {% if user.is_staff %}
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'core:painel_controle' %}">Painel de Controle</a>
                            </li>
                        {% endif %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'core:sair' %}">Sair</a>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'core:entrar' %}">Entrar</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>
    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
               
        {% block content %}{% endblock %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
    <!-- Adicione esta linha antes do fechamento do body -->
    <script src="{% static 'js/csrf_refresh.js' %}"></script>
</body>
</html>





## templates\base_old.html

html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Sistema de Gestão de Iniciados da OmAum{% endblock %}</title>
    <!-- Bootstrap CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css" rel="stylesheet">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="/">Sistema de Gestão de Iniciados da OmAum</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'turmas:listar_turmas' %}">Turmas</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'cursos:listar_cursos' %}">Cursos</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'cargos:listar_cargos' %}">Cargos</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'frequencias:listar_frequencias' %}">Frequências</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'iniciacoes:listar_iniciacoes' %}">Iniciações</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'punicoes:listar_punicoes' %}">Punições</a>
                </li>
                <!-- Adicione mais itens de menu conforme necessário -->
            </ul>
        </div>
    </nav>

    <main class="container mt-4">
        {% block content %}{% endblock %}
    </main>

    <footer class="mt-5 py-3 bg-light text-center">
        <div class="container">
            <span class="text-muted">© 2024 Sistema de Gestão de Iniciados da OmAum. Todos os direitos reservados.</span>
        </div>
    </footer>

    <!-- Bootstrap JS, Popper.js, and jQuery -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>





## templates\csrf_test.html

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






## templates\home_old.html

html
{% extends 'base.html' %}

{% block title %} Sistema de Gestão de Iniciados da OmAum {% endblock %}

{% block content %}
<div class="container">
    <div class="jumbotron mt-4">
        <h1 class="display-4">Welcome to OMAUM</h1>
        <p class="lead">Your platform for courses and learning.</p>
        <hr class="my-4">
        <p>Get started by exploring our courses.</p>
        
        <a class="btn btn-primary btn-lg" href="{% url 'cursos:listar_cursos' %}" role="button">View Courses</a>
        
        {% if not user.is_authenticated %}
            <a class="btn btn-outline-secondary btn-lg" href="{% url 'login' %}" role="button">Login</a>
        {% endif %}
    </div>
</div>
{% endblock %}





## templates\core\base_old.html

html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}OMAUM{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    
    <!-- Custom CSS -->
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">OMAUM</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'home' %}">Home</a>
                    </li>
                    {% if user.is_authenticated %}
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="atividadesDropdown" role="button" data-bs-toggle="dropdown">
                            Atividades
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="{% url 'atividades:atividade_academica_list' %}">Acadêmicas</a></li>
                            <li><a class="dropdown-item" href="{% url 'atividades:atividade_ritualistica_list' %}">Ritualísticas</a></li>
                        </ul>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/cursos/">Cursos</a>  <!-- Use um URL absoluto temporariamente -->
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'cargos:listar_cargos' %}">Cargos</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'frequencias:listar_frequencias' %}">Frequências</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'iniciacoes:listar_iniciacoes' %}">Iniciações</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'punicoes:listar_punicoes' %}">Punições</a>
                    </li>
                    {% endif %}
                </ul>
                <ul class="navbar-nav">
                    {% if user.is_authenticated %}
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                            {{ user.username }}
                        </a>
                        <ul class="dropdown-menu dropdown-menu-end">
                            {% if user.is_staff %}
                            <li><a class="dropdown-item" href="{% url 'admin:index' %}">Admin</a></li>
                            {% endif %}
                            <li><a class="dropdown-item" href="{% url 'logout' %}">Sair</a></li>
                        </ul>
                    </li>
                    {% else %}
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'login' %}">Login</a>
                    </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main>
        {% if messages %}
        <div class="container mt-3">
            {% for message in messages %}
            <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
            {% endfor %}
        </div>
        {% endif %}

        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-light text-center text-muted py-4 mt-5">
        <div class="container">
            <p>© {% now "Y" %} OMAUM - Todos os direitos reservados</p>
        </div>
    </footer>

    <!-- Bootstrap JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Custom JavaScript -->
    {% block extra_js %}{% endblock %}
</body>
</html>





## templates\core\home.html

html
{% extends 'base.html' %}

{% block title %}OMAUM - Home{% endblock %}

{% block content %}
<div class="container">
    <div class="jumbotron mt-4">
        <h1 class="display-4">Welcome to OMAUM</h1>
        <p class="lead">Your platform for courses and learning.</p>
        <hr class="my-4">
        <p>Get started by exploring our system.</p>
        
        {% if user.is_authenticated %}
            <a class="btn btn-primary btn-lg" href="{% url 'alunos:listar' %}" role="button">View Students</a>
        {% else %}
            <a class="btn btn-outline-secondary btn-lg" href="{% url 'core:entrar' %}" role="button">Login</a>
        {% endif %}
    </div>
</div>
{% endblock %}





## templates\includes\form_errors.html

html
{% if form.non_field_errors %}
    <div class="alert alert-




## templates\registration\login.html

html
{% extends 'base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
<div class="container mt-5">
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card">
        <div class="card-header">
          <h4 class="mb-0">Login</h4>
        </div>
        <div class="card-body">
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
            </div>

            <div class="mb-3">
              <label for="id_password" class="form-label">Senha</label>
              <input type="password" name="password" id="id_password" class="form-control" required>
            </div>

            <input type="hidden" name="next" value="{{ next }}">

            <div class="d-grid">
              <button type="submit" class="btn btn-primary">Entrar</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}





## templates\registration\registro.html

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


