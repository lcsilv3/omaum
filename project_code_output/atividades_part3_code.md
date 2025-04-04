# Código da Funcionalidade: atividades - Parte 3/3
*Gerado automaticamente*



## atividades\templates\atividades\editar_atividade_academica.html

html
{% extends 'core/base.html' %}

{% block title %}Editar Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Editar Atividade Acadêmica</h1>
        <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-secondary">Voltar para detalhes</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.responsavel %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Data e Local</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_inicio %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_fim %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Classificação</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.tipo_atividade %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.status %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Atualizar Atividade</button>
        </div>
    </form>
</div>
{% endblock %}





## atividades\templates\atividades\editar_atividade_ritualistica.html

html
{% extends 'core/base.html' %}

{% block title %}Editar Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Editar Atividade Ritualística</h1>
        <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-secondary">Voltar para detalhes</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Data e Horário</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.data %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_inicio %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_fim %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Turma e Participantes</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.todos_alunos %}
                        <small class="form-text text-muted">Marque esta opção para incluir automaticamente todos os alunos da turma.</small>
                    </div>
                </div>
                
                <div class="row mt-3" id="participantes-container">
                    <div class="col-md-12">
                        <label for="{{ form.participantes.id_for_label }}">{{ form.participantes.label }}</label>
                        <div class="border p-3 rounded">
                            {{ form.participantes }}
                        </div>
                        {% if form.participantes.errors %}
                            <div class="text-danger">
                                {{ form.participantes.errors }}
                            </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Atualizar Atividade</button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const todosAlunosCheckbox = document.getElementById('{{ form.todos_alunos.id_for_label }}');
        const participantesContainer = document.getElementById('participantes-container');
        
        function toggleParticipantes() {
            if (todosAlunosCheckbox.checked) {
                participantesContainer.style.display = 'none';
            } else {
                participantesContainer.style.display = 'block';
            }
        }
        
        // Inicializar
        toggleParticipantes();
        
        // Adicionar listener para mudanças
        todosAlunosCheckbox.addEventListener('change', toggleParticipantes);
    });
</script>
{% endblock %}





## atividades\templates\atividades\excluir_atividade_academica.html

html
{% extends 'core/base.html' %}

{% block title %}Excluir Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Atividade Acadêmica</h1>
    
    <div class="alert alert-danger">
        <p>Tem certeza que deseja excluir a atividade acadêmica "{{ atividade.nome }}"?</p>
        <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ atividade.nome }}</p>
            <p><strong>Responsável:</strong> {{ atividade.responsavel|default:"Não informado" }}</p>
            <p><strong>Data de Início:</strong> {{ atividade.data_inicio|date:"d/m/Y H:i" }}</p>
            <p><strong>Data de Término:</strong> {{ atividade.data_fim|date:"d/m/Y H:i"|default:"Não definida" }}</p>
            <p><strong>Local:</strong> {{ atividade.local|default:"Não informado" }}</p>
            <p><strong>Tipo:</strong> {{ atividade.get_tipo_atividade_display }}</p>
            <p><strong>Status:</strong> {{ atividade.get_status_display }}</p>
            <p><strong>Turma:</strong> {{ atividade.turma }}</p>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <div class="d-flex">
            <button type="submit" class="btn btn-danger me-2">Sim, excluir</button>
            <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}





## atividades\templates\atividades\excluir_atividade_ritualistica.html

html
{% extends 'core/base.html' %}

{% block title %}Excluir Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Atividade Ritualística</h1>
    
    <div class="alert alert-danger">
        <p>Tem certeza que deseja excluir a atividade ritualística "{{ atividade.nome }}"?</p>
        <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ atividade.nome }}</p>
            <p><strong>Data:</strong> {{ atividade.data|date:"d/m/Y" }}</p>
            <p><strong>Horário:</strong> {{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</p>
            <p><strong>Local:</strong> {{ atividade.local }}</p>
            <p><strong>Turma:</strong> {{ atividade.turma }}</p>
            <p><strong>Total de Participantes:</strong> {{ atividade.participantes.count }}</p>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <div class="d-flex">
            <button type="submit" class="btn btn-danger me-2">Sim, excluir</button>
            <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}





## atividades\templates\atividades\formulario_atividade_academica.html

html
{% extends 'core/base.html' %}
{% block title %}Criar Nova Atividade Acadêmica{% endblock %}
{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{% if form.instance.pk %}Editar{% else %}Nova{% endif %} Atividade Acadêmica</h1>
        <a href="{{ return_url }}" class="btn btn-secondary me-2">Voltar</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.responsavel %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Data e Local</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_inicio %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_fim %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Classificação</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.tipo_atividade %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.status %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <!-- Use a URL de retorno fornecida pela view -->
            <a href="{{ return_url }}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">
                {% if atividade %}Atualizar{% else %}Criar{% endif %} Atividade
            </button>
        </div>
    </form>
</div>
{% endblock %}





## atividades\templates\atividades\formulario_atividade_ritualistica.html

html
{% extends 'core/base.html' %}

{% block title %}{% if atividade %}Editar{% else %}Nova{% endif %} Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{% if atividade %}Editar{% else %}Nova{% endif %} Atividade Ritualística</h1>
        <a href="{{ return_url }}" class="btn btn-secondary">Voltar para a lista</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Data e Horário</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.data %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_inicio %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_fim %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Turma e Participantes</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.participantes %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{{ return_url }}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">
                {% if atividade %}Atualizar{% else %}Criar{% endif %} Atividade
            </button>
        </div>
    </form>
</div>
{% endblock %}




## atividades\templates\atividades\listar_atividades_academicas.html

html
{% extends 'core/base.html' %}

{% block title %}Lista de Atividades Acadêmicas{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Cabeçalho com título e botões na mesma linha -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Lista de Atividades Acadêmicas</h1>
        <div>
            <!-- Use uma URL específica em vez de javascript:history.back() -->
            <a href="{% url 'home' %}" class="btn btn-secondary me-2">Voltar ao Dashboard</a>
            
            <!-- Botão para criar nova atividade acadêmica com URL de retorno -->
            <a href="{% url 'atividades:criar_atividade_academica' %}?return_url={{ request.path|urlencode }}" class="btn btn-primary">
                Nova Atividade Acadêmica
            </a>
        </div>
    </div>    
    <!-- Barra de busca e filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <form method="get" class="row g-3">
                <div class="col-md-6">
                    <input type="text" name="q" class="form-control" placeholder="Buscar por título, descrição ou responsável..." value="{{ query }}">
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn btn-primary w-100">Filtrar</button>
                </div>
            </form>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Título</th>
                            <th>Responsável</th>
                            <th>Data de Início</th>
                            <th>Status</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for atividade in atividades %}
                            <tr>
                                <td>{{ atividade.nome }}</td>
                                <td>{{ atividade.descrição }}</td>
                                <td>{{ atividade.data_inicio|date:"d/m/Y" }}</td>
                                <td>{{ atividade.get_status_display }}</td>
                                <td>
                                    <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-sm btn-info">Detalhes</a>
                                    <a href="{% url 'atividades:editar_atividade_academica' atividade.id %}" class="btn btn-sm btn-warning">Editar</a>
                                    <a href="{% url 'atividades:excluir_atividade_academica' atividade.id %}" class="btn btn-sm btn-danger">Excluir</a>                                </td>                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="5" class="text-center">
                                    <p class="my-3">Nenhuma atividade acadêmica cadastrada.</p>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer">
            <p class="text-muted mb-0">Total: {{ atividades.count|default:"0" }} atividade(s)</p>
            {% if page_obj.has_other_pages %}
                <nav aria-label="Paginação">
                    <ul class="pagination justify-content-center mb-0">
                        {% if page_obj.has_previous %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.previous_page_number }}&q={{ query }}">Anterior</a>
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
                                    <a class="page-link" href="?page={{ num }}&q={{ query }}">{{ num }}</a>
                                </li>
                            {% endif %}
                        {% endfor %}

                        {% if page_obj.has_next %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.next_page_number }}&q={{ query }}">Próxima</a>
                            </li>
                        {% else %}
                            <li class="page-item disabled">
                                <span class="page-link">Próxima</span>
                            </li>
                        {% endif %}
                    </ul>
                </nav>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}





## atividades\templates\atividades\listar_atividades_ritualisticas.html

html
{% extends 'core/base.html' %}

{% block title %}Lista de Atividades Ritualísticas{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Cabeçalho com título e botões na mesma linha -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Lista de Atividades Ritualísticas</h1>
        <div>
            <a href="{% url 'home' %}" class="btn btn-secondary me-2">Voltar ao Dashboard</a>
            <!-- Botão para criar nova atividade ritualística -->
            <a href="{% url 'atividades:criar_atividade_ritualistica' %}?return_url={{ request.path|urlencode }}" class="btn btn-primary">
                Nova Atividade Ritualística
            </a>
        </div>
    </div>    
    <!-- Barra de busca e filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <form method="get" class="row g-3">
                <div class="col-md-6">
                    <input type="text" name="q" class="form-control" placeholder="Buscar por nome, descrição ou local..." value="{{ query }}">
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn btn-primary w-100">Filtrar</button>
                </div>
            </form>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>Data</th>
                            <th>Horário</th>
                            <th>Local</th>
                            <th>Turma</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for atividade in atividades %}
                            <tr>
                                <td>{{ atividade.nome }}</td>
                                <td>{{ atividade.data|date:"d/m/Y" }}</td>
                                <td>{{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</td>
                                <td>{{ atividade.local }}</td>
                                <td>{{ atividade.turma }}</td>
                                <td>
                                    <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-sm btn-info">Detalhes</a>
                                    <a href="{% url 'atividades:editar_atividade_ritualistica' atividade.id %}" class="btn btn-sm btn-warning">Editar</a>
                                    <a href="{% url 'atividades:excluir_atividade_ritualistica' atividade.id %}" class="btn btn-sm btn-danger">Excluir</a>                                </td>                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="6" class="text-center">
                                    <p class="my-3">Nenhuma atividade ritualística cadastrada.</p>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer">
            <p class="text-muted mb-0">Total: {{ atividades.count|default:"0" }} atividade(s)</p>
            {% if page_obj.has_other_pages %}
                <nav aria-label="Paginação">
                    <ul class="pagination justify-content-center mb-0">
                        {% if page_obj.has_previous %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.previous_page_number }}&q={{ query }}">Anterior</a>
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
                                    <a class="page-link" href="?page={{ num }}&q={{ query }}">{{ num }}</a>
                                </li>
                            {% endif %}
                        {% endfor %}

                        {% if page_obj.has_next %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.next_page_number }}&q={{ query }}">Próxima</a>
                            </li>
                        {% else %}
                            <li class="page-item disabled">
                                <span class="page-link">Próxima</span>
                            </li>
                        {% endif %}
                    </ul>
                </nav>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}





## atividades\tests\test_models.py

python
from django.test import TestCase
from atividades.models import AtividadeAcademica, AtividadeRitualistica
from turmas.models import Turma
from cursos.models import Curso
from alunos.models import Aluno
from datetime import date, timedelta
from django.utils import timezone

class AtividadeAcademicaModelTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            nome='Curso de Teste',
            descricao='Descrição do curso de teste'
        )
        self.turma = Turma.objects.create(
            nome='Turma de Teste',
            curso=self.curso,
            data_inicio=date(2023, 1, 1),
            data_fim=date(2023, 12, 31)
        )
        
    def test_criar_atividade(self):
        data_inicio = timezone.now()
        data_fim = data_inicio + timedelta(days=7)
        
        atividade = AtividadeAcademica.objects.create(
            nome='Aula de Matemática',
            descricao='Aula introdutória sobre álgebra.',
            data_inicio=data_inicio,
            data_fim=data_fim,
            turma=self.turma
        )
        
        self.assertEqual(atividade.nome, 'Aula de Matemática')
        self.assertEqual(atividade.descricao, 'Aula introdutória sobre álgebra.')
        self.assertEqual(atividade.data_inicio, data_inicio)
        self.assertEqual(atividade.data_fim, data_fim)
        self.assertEqual(atividade.turma, self.turma)
        self.assertEqual(str(atividade), 'Aula de Matemática')

class AtividadeRitualisticaModelTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            nome='Curso de Teste',
            descricao='Descrição do curso de teste'
        )
        self.turma = Turma.objects.create(
            nome='Turma de Teste',
            curso=self.curso,
            data_inicio=date(2023, 1, 1),
            data_fim=date(2023, 12, 31)
        )
        self.aluno1 = Aluno.objects.create(
            nome='Aluno 1',
            email='aluno1@teste.com'
        )
        self.aluno1.turmas.add(self.turma)
        self.aluno2 = Aluno.objects.create(
            nome='Aluno 2',
            email='aluno2@teste.com'
        )
        self.aluno2.turmas.add(self.turma)
        
    def test_criar_atividade_ritualistica(self):
        data_inicio = timezone.now()
        data_fim = data_inicio + timedelta(days=7)
        
        atividade = AtividadeRitualistica.objects.create(
            nome='Ritual de Iniciação',
            descricao='Ritual para novos membros',
            data_inicio=data_inicio,
            data_fim=data_fim,
            turma=self.turma
        )
        atividade.alunos.add(self.aluno1, self.aluno2)
        
        self.assertEqual(atividade.nome, 'Ritual de Iniciação')
        self.assertEqual(atividade.descricao, 'Ritual para novos membros')
        self.assertEqual(atividade.data_inicio, data_inicio)
        self.assertEqual(atividade.data_fim, data_fim)
        self.assertEqual(atividade.turma, self.turma)
        self.assertEqual(atividade.alunos.count(), 2)
        self.assertTrue(self.aluno1 in atividade.alunos.all())
        self.assertTrue(self.aluno2 in atividade.alunos.all())
        self.assertEqual(str(atividade), 'Ritual de Iniciação')





## atividades\tests\test_views.py

python
from django.test import TestCase, Client
from django.urls import reverse
from atividades.models import AtividadeAcademica, AtividadeRitualistica
from turmas.models import Turma
from cursos.models import Curso
from alunos.models import Aluno
from datetime import date, timedelta
from django.utils import timezone

class AtividadeAcademicaViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.curso = Curso.objects.create(
            codigo_curso='CUR01',
            nome='Curso de Teste',
            descricao='Descrição do curso de teste'
        )
        self.turma = Turma.objects.create(
            nome='Turma de Teste',
            curso=self.curso,
            data_inicio=date(2023, 1, 1),
            data_fim=date(2023, 12, 31)
        )
        self.data_inicio = timezone.now()
        self.data_fim = self.data_inicio + timedelta(days=7)
        self.atividade = AtividadeAcademica.objects.create(
            nome='Aula de Matemática',
            descricao='Aula introdutória sobre álgebra.',
            data_inicio=self.data_inicio,
            data_fim=self.data_fim,
            turma=self.turma
        )

    def test_listar_atividades(self):
        response = self.client.get(reverse('atividades:academica_lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aula de Matemática')
        
    def test_filtrar_atividades_por_turma(self):
        # Criar outra turma e atividade
        turma2 = Turma.objects.create(
            nome='Turma 2',
            curso=self.curso,
            data_inicio=date(2023, 1, 1),
            data_fim=date(2023, 12, 31)
        )
        AtividadeAcademica.objects.create(
            nome='Aula de Física',
            descricao='Introdução à física',
            data_inicio=self.data_inicio,
            data_fim=self.data_fim,
            turma=turma2
        )
        
        # Filtrar por turma1
        response = self.client.get(f"{reverse('atividades:academica_lista')}?turma={self.turma.id}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aula de Matemática')
        self.assertNotContains(response, 'Aula de Física')
        
        # Filtrar por turma2
        response = self.client.get(f"{reverse('atividades:academica_lista')}?turma={turma2.id}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aula de Física')
        self.assertNotContains(response, 'Aula de Matemática')

    def test_criar_atividade(self):
        response = self.client.get(reverse('atividades:academica_criar'))
        self.assertEqual(response.status_code, 200)
        
        # Testar POST para criar atividade
        data = {
            'nome': 'Nova Atividade',
            'descricao': 'Descrição da nova atividade',
            'data_inicio': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_fim': (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S'),
            'turma': self.turma.id
        }
        response = self.client.post(reverse('atividades:academica_criar'), data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        
        # Verificar se a atividade foi criada
        self.assertTrue(AtividadeAcademica.objects.filter(nome='Nova Atividade').exists())
    
    def test_editar_atividade(self):
        response = self.client.get(reverse('atividades:academica_editar', args=[self.atividade.id]))
        self.assertEqual(response.status_code, 200)
        
        # Testar POST para editar atividade
        data = {
            'nome': 'Aula de Matemática Atualizada',
            'descricao': 'Descrição atualizada',
            'data_inicio': self.data_inicio.strftime('%Y-%m-%d %H:%M:%S'),
            'data_fim': self.data_fim.strftime('%Y-%m-%d %H:%M:%S'),
            'turma': self.turma.id
        }
        response = self.client.post(reverse('atividades:academica_editar', args=[self.atividade.id]), data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        
        # Verificar se a atividade foi atualizada
        self.atividade.refresh_from_db()
        self.assertEqual(self.atividade.nome, 'Aula de Matemática Atualizada')
        self.assertEqual(self.atividade.descricao, 'Descrição atualizada')
    
    def test_excluir_atividade(self):
        response = self.client.get(reverse('atividades:academica_excluir',



