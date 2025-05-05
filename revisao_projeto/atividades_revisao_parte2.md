'''
# Revisão da Funcionalidade: atividades

## Arquivos forms.py:


### Arquivo: atividades\templates\atividades\formulario_atividade_academica.html

html
{% extends 'base.html' %}
{% block title %}{% if form.instance.pk %}Editar{% else %}Nova{% endif %} Atividade Acadêmica{% endblock %}
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
        
        <!-- Nova seção para Turmas -->
        <div class="card mb-4">
            <div class="card-header">
                <h5>Turmas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.turmas %}
                    </div>
                </div>
                <div class="row mt-2">
                    <div class="col-md-12">
                        <div class="form-check">
                            {{ form.todas_turmas }}
                            <label class="form-check-label" for="{{ form.todas_turmas.id_for_label }}">
                                {{ form.todas_turmas.label }}
                            </label>
                            <small class="form-text text-muted">
                                Marque esta opção para aplicar esta atividade a todas as turmas ativas automaticamente.
                            </small>
                        </div>
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
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.tipo_atividade %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.status %}
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

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const todasTurmasCheckbox = document.getElementById('{{ form.todas_turmas.id_for_label }}');
        const turmasSelect = document.getElementById('{{ form.turmas.id_for_label }}');
        
        function toggleTurmasField() {
            if (todasTurmasCheckbox.checked) {
                turmasSelect.disabled = true;
                // Adicionar uma mensagem informativa
                if (!document.getElementById('turmas-info')) {
                    const infoDiv = document.createElement('div');
                    infoDiv.id = 'turmas-info';
                    infoDiv.className = 'alert alert-info mt-2';
                    infoDiv.textContent = 'Todas as turmas ativas serão incluídas automaticamente.';
                    turmasSelect.parentNode.appendChild(infoDiv);
                }
            } else {
                turmasSelect.disabled = false;
                // Remover a mensagem informativa se existir
                const infoDiv = document.getElementById('turmas-info');
                if (infoDiv) {
                    infoDiv.remove();
                }
            }
        }
        
        // Inicializar
        toggleTurmasField();
        
        // Adicionar listener para mudanças
        todasTurmasCheckbox.addEventListener('change', toggleTurmasField);
        
        // Inicializar Select2 para o campo de turmas
        if (typeof $.fn.select2 === 'function') {
            $(turmasSelect).select2({
                theme: 'bootstrap4',
                placeholder: 'Selecione as turmas',
                allowClear: true,
                width: '100%'
            });
        }
    });
</script>
{% endblock %}




### Arquivo: atividades\templates\atividades\formulario_atividade_ritualistica.html

html
{% extends 'base.html' %}

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



### Arquivo: atividades\templates\atividades\index.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Atividades - OMAUM{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Atividades</h1>
        <a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>
    </div>
    
    <div class="row">
        <div class="col-md-6 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">Atividades Acadêmicas</h5>
                    <p class="card-text">Gerenciamento de atividades relacionadas ao ensino e aprendizagem.</p>
                    <p class="card-text text-muted">Aulas, workshops, palestras, seminários e outras atividades educacionais.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-primary">Gerenciar Atividades Acadêmicas</a>
                </div>
            </div>
        </div>
        
        <div class="col-md-6 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">Atividades Ritualísticas</h5>
                    <p class="card-text">Gerenciamento de atividades relacionadas a rituais e cerimônias.</p>
                    <p class="card-text text-muted">Cerimônias, rituais, meditações coletivas e outras práticas espirituais.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-primary">Gerenciar Atividades Ritualísticas</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: atividades\templates\atividades\listar_atividades.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Atividades - OMAUM{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Atividades</h1>
        <div class="btn-group">
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'atividades:calendario_atividades' %}" class="btn btn-info me-2">
                <i class="fas fa-calendar-alt"></i> Calendário
            </a>
            <a href="{% url 'atividades:dashboard_atividades' %}" class="btn btn-success me-2">
                <i class="fas fa-chart-bar"></i> Dashboard
            </a>
            <a href="{% url 'atividades:relatorio_atividades' %}" class="btn btn-warning">
                <i class="fas fa-file-alt"></i> Relatórios
            </a>
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-6 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">Atividades Acadêmicas</h5>
                    <p class="card-text">Gerenciamento de atividades relacionadas ao ensino e aprendizagem.</p>
                    <p class="card-text text-muted">Aulas, workshops, palestras, seminários e outras atividades educacionais.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-primary">Gerenciar Atividades Acadêmicas</a>
                </div>
            </div>
        </div>
        
        <div class="col-md-6 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">Atividades Ritualísticas</h5>
                    <p class="card-text">Gerenciamento de atividades relacionadas a rituais e cerimônias.</p>
                    <p class="card-text text-muted">Cerimônias, rituais, meditações coletivas e outras práticas espirituais.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-primary">Gerenciar Atividades Ritualísticas</a>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-4 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">Calendário</h5>
                    <p class="card-text">Visualize todas as atividades em um calendário interativo.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'atividades:calendario_atividades' %}" class="btn btn-info">Acessar Calendário</a>
                </div>
            </div>
        </div>
        
        <div class="col-md-4 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">Dashboard</h5>
                    <p class="card-text">Visualize estatísticas e gráficos sobre as atividades.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'atividades:dashboard_atividades' %}" class="btn btn-success">Acessar Dashboard</a>
                </div>
            </div>
        </div>
        
        <div class="col-md-4 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">Relatórios</h5>
                    <p class="card-text">Gere relatórios detalhados sobre as atividades.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'atividades:relatorio_atividades' %}" class="btn btn-warning">Gerar Relatórios</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\listar_atividades_academicas.html

html
{% extends 'base.html' %}

{% block title %}Lista de Atividades Acadêmicas{% endblock %}

{% block content %}
<main id="main-content" class="py-4">
    <div class="container mt-4">
        <!-- Cabeçalho com título e botões na mesma linha -->
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h1>Lista de Atividades Acadêmicas</h1>
            <div class="btn-group">
                <a href="/" class="btn btn-secondary me-2">Página Inicial</a>
                
                <!-- Botão para criar nova atividade acadêmica com URL de retorno -->
                <a href="/atividades/academicas/criar/?return_url=/atividades/academicas/" class="btn btn-primary me-2">
                    <i class="fas fa-plus"></i> Nova Atividade
                </a>
                
                <!-- Botões para as novas funcionalidades -->
                <a href="/atividades/calendario/" class="btn btn-info me-2">
                    <i class="fas fa-calendar-alt"></i> Calendário
                </a>
                
                <a href="/atividades/dashboard/" class="btn btn-success me-2">
                    <i class="fas fa-chart-bar"></i> Dashboard
                </a>
                
                <a href="/atividades/relatorio/" class="btn btn-warning">
                    <i class="fas fa-file-alt"></i> Relatórios
                </a>
            </div>
        </div>
        
        <!-- Barra de busca e filtros -->
        <div class="card mb-4">
            <div class="card-header">
                <form method="get" class="row g-3">
                    <div class="col-md-6">
                        <input type="text" name="q" class="form-control" placeholder="Buscar por título, descrição ou responsável..." value="">
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
                                <th>Turmas</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Plenilúnio</td>
                                <td>Não informado</td>
                                <td>26/10/2026</td>
                                <td>
                                    <span class="badge bg-warning">
                                        Agendada
                                    </span>
                                </td>
                                <td>
                                    Turma A
                                </td>
                                <td>
                                    <a href="/atividades/academicas/detalhar/2/" class="btn btn-sm btn-info" title="Ver detalhes completos da atividade">Detalhes</a>
                                    <a href="/atividades/academicas/editar/2/" class="btn btn-sm btn-warning" title="Editar informações da atividade">Editar</a>
                                    <a href="/atividades/academicas/excluir/2/" class="btn btn-sm btn-danger" title="Excluir esta atividade">Excluir</a>
                                    <a href="/atividades/academicas/2/copiar/" class="btn btn-sm btn-secondary" title="Criar uma cópia desta atividade">Copiar</a>
                                </td>
                            </tr>
                            <tr>
                                <td>Aula</td>
                                <td>Não informado</td>
                                <td>26/10/2024</td>
                                <td>
                                    <span class="badge bg-warning">
                                        Agendada
                                    </span>
                                </td>
                                <td>
                                    Turma A
                                </td>
                                <td>
                                    <a href="/atividades/academicas/detalhar/1/" class="btn btn-sm btn-info" title="Ver detalhes completos da atividade">Detalhes</a>
                                    <a href="/atividades/academicas/editar/1/" class="btn btn-sm btn-warning" title="Editar informações da atividade">Editar</a>
                                    <a href="/atividades/academicas/excluir/1/" class="btn btn-sm btn-danger" title="Excluir esta atividade">Excluir</a>
                                    <a href="/atividades/academicas/1/copiar/" class="btn btn-sm btn-secondary" title="Criar uma cópia desta atividade">Copiar</a>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="card-footer">
                <p class="text-muted mb-0">Total: 2 atividade(s)</p>
            </div>
        </div>
    </div>
</main>
{% endblock %}




### Arquivo: atividades\templates\atividades\listar_atividades_ritualisticas.html

html
{% extends 'base.html' %}

{% block title %}Lista de Atividades Ritualísticas{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Cabeçalho com título e botões na mesma linha -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Lista de Atividades Ritualísticas</h1>
        <div class="btn-group">
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <!-- Botão para criar nova atividade ritualística -->
            <a href="{% url 'atividades:criar_atividade_ritualistica' %}?return_url={{ request.path|urlencode }}" class="btn btn-primary me-2">
                <i class="fas fa-plus"></i> Nova Atividade
            </a>
            
            <!-- Botões para as novas funcionalidades -->
            <a href="{% url 'atividades:calendario_atividades' %}" class="btn btn-info me-2">
                <i class="fas fa-calendar-alt"></i> Calendário
            </a>
            
            <a href="{% url 'atividades:dashboard_atividades' %}" class="btn btn-success me-2">
                <i class="fas fa-chart-bar"></i> Dashboard
            </a>
            
            <a href="{% url 'atividades:relatorio_atividades' %}" class="btn btn-warning">
                <i class="fas fa-file-alt"></i> Relatórios
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
                                    <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-sm btn-info" title="Ver detalhes completos da atividade">Detalhes</a>
                                    <a href="{% url 'atividades:editar_atividade_ritualistica' atividade.id %}" class="btn btn-sm btn-warning" title="Editar informações da atividade">Editar</a>
                                    <a href="{% url 'atividades:excluir_atividade_ritualistica' atividade.id %}" class="btn btn-sm btn-danger" title="Excluir esta atividade">Excluir</a>
                                    <!-- Novo botão para copiar atividade -->
                                    <a href="{% url 'atividades:copiar_atividade_ritualistica' atividade.id %}" class="btn btn-sm btn-secondary" title="Criar uma cópia desta atividade">Copiar</a>
                                </td>
                            </tr>
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




### Arquivo: atividades\templates\atividades\registrar_frequencia.html

html
{% extends 'base.html' %}

{% block title %}Registrar Frequência - {{ atividade.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Registrar Frequência</h1>
        <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-secondary">Voltar</a>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Nome:</strong> {{ atividade.nome }}</p>
                    <p><strong>Tipo:</strong> {{ atividade.get_tipo_atividade_display }}</p>
                    <p><strong>Status:</strong> {{ atividade.get_status_display }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Data de Início:</strong> {{ atividade.data_inicio|date:"d/m/Y" }}</p>
                    <p><strong>Data de Término:</strong> {{ atividade.data_fim|date:"d/m/Y"|default:"Não definida" }}</p>
                    <p><strong>Responsável:</strong> {{ atividade.responsavel|default:"Não informado" }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        
        <div class="card mb-4">
            <div class="card-header">
                <div class="d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">Lista de Presença</h5>
                    <div>
                        <div class="form-group mb-0">
                            <label for="data" class="me-2">Data:</label>
                            <input type="date" id="data" name="data" class="form-control d-inline-block" style="width: auto;" value="{{ data_hoje }}" required>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card-body">
                {% if alunos %}
                    <div class="mb-3">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="marcar-todos" checked>
                            <label class="form-check-label" for="marcar-todos">
                                Marcar/Desmarcar Todos
                            </label>
                        </div>
                    </div>
                    
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th style="width: 50px;">#</th>
                                    <th>Aluno</th>
                                    <th style="width: 120px;">Presente</th>
                                    <th>Justificativa (se ausente)</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for aluno in alunos %}
                                <tr>
                                    <td>{{ forloop.counter }}</td>
                                    <td>
                                        <div class="d-flex align-items-center">
                                            {% if aluno.foto %}
                                                <img src="{{ aluno.foto.url }}" alt="Foto de {{ aluno.nome }}" 
                                                     class="rounded-circle me-2" width="30" height="30" 
                                                     style="object-fit: cover;">
                                            {% else %}
                                                <div class="rounded-circle bg-secondary me-2 d-flex align-items-center justify-content-center" 
                                                     style="width: 30px; height: 30px; color: white;">
                                                    {{ aluno.nome|first|upper }}
                                                </div>
                                            {% endif %}
                                            <div>
                                                <div>{{ aluno.nome }}</div>
                                                <small class="text-muted">{{ aluno.numero_iniciatico|default:"Sem número iniciático" }}</small>
                                            </div>
                                        </div>
                                    </td>
                                    <td>
                                        <div class="form-check">
                                            <input class="form-check-input presenca-checkbox" type="checkbox" name="presentes" value="{{ aluno.cpf }}" id="presente_{{ aluno.cpf }}" checked>
                                            <label class="form-check-label" for="presente_{{ aluno.cpf }}">
                                                Presente
                                            </label>
                                        </div>
                                    </td>
                                    <td>
                                        <textarea class="form-control justificativa-field" name="justificativa_{{ aluno.cpf }}" rows="1" placeholder="Justificativa para ausência" disabled></textarea>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                {% else %}
                    <div class="alert alert-warning">
                        <p>Não há alunos matriculados nas turmas associadas a esta atividade.</p>
                    </div>
                {% endif %}
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-secondary">Cancelar</a>
            {% if alunos %}
                <button type="submit" class="btn btn-primary">Registrar Frequência</button>
            {% endif %}
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Função para alternar o estado de habilitação do campo de justificativa
        function toggleJustificativa(checkbox) {
            const row = checkbox.closest('tr');
            const justificativa = row.querySelector('.justificativa-field');
            
            if (checkbox.checked) {
                justificativa.disabled = true;
                justificativa.value = '';
            } else {
                justificativa.disabled = false;
            }
        }
        
        // Adicionar evento para cada checkbox de presença
        const checkboxes = document.querySelectorAll('.presenca-checkbox');
        checkboxes.forEach(function(checkbox) {
            checkbox.addEventListener('change', function() {
                toggleJustificativa(this);
            });
            
            // Inicializar o estado
            toggleJustificativa(checkbox);
        });
        
        // Marcar/Desmarcar todos
        const marcarTodos = document.getElementById('marcar-todos');
        marcarTodos.addEventListener('change', function() {
            checkboxes.forEach(function(checkbox) {
                checkbox.checked = marcarTodos.checked;
                toggleJustificativa(checkbox);
            });
        });
    });
</script>
{% endblock %}



### Arquivo: atividades\templates\atividades\relatorio_atividades.html

html
{% extends 'base.html' %}

{% block title %}Relatório de Atividades{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Relatório de Atividades</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'atividades:calendario_atividades' %}" class="btn btn-info me-2">
                <i class="fas fa-calendar-alt"></i> Calendário
            </a>
            <a href="{% url 'atividades:dashboard_atividades' %}" class="btn btn-success me-2">
                <i class="fas fa-chart-bar"></i> Dashboard
            </a>
            <div class="btn-group">
                <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-outline-primary">Atividades Acadêmicas</a>
                <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-outline-info">Atividades Ritualísticas</a>
            </div>
        </div>
    </div>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-3">
                    <label for="tipo" class="form-label">Tipo de Atividade</label>
                    <select name="tipo" id="tipo" class="form-select">
                        <option value="todas" {% if tipo == 'todas' %}selected{% endif %}>Todas</option>
                        <option value="academicas" {% if tipo == 'academicas' %}selected{% endif %}>Acadêmicas</option>
                        <option value="ritualisticas" {% if tipo == 'ritualisticas' %}selected{% endif %}>Ritualísticas</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="status" class="form-label">Status</label>
                    <select name="status" id="status" class="form-select">
                        <option value="">Todos</option>
                        <option value="agendada" {% if status == 'agendada' %}selected{% endif %}>Agendada</option>
                        <option value="em_andamento" {% if status == 'em_andamento' %}selected{% endif %}>Em Andamento</option>
                        <option value="concluida" {% if status == 'concluida' %}selected{% endif %}>Concluída</option>
                        <option value="cancelada" {% if status == 'cancelada' %}selected{% endif %}>Cancelada</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="data_inicio" class="form-label">Data Início</label>
                    <input type="date" name="data_inicio" id="data_inicio" class="form-control" value="{{ data_inicio }}">
                </div>
                <div class="col-md-3">
                    <label for="data_fim" class="form-label">Data Fim</label>
                    <input type="date" name="data_fim" id="data_fim" class="form-control" value="{{ data_fim }}">
                </div>
                <div class="col-md-12 d-flex justify-content-end">
                    <button type="submit" class="btn btn-primary me-2">Filtrar</button>
                    <a href="{% url 'atividades:relatorio_atividades' %}" class="btn btn-secondary">Limpar Filtros</a>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Botões de exportação -->
    <div class="mb-4">
        <a href="{% url 'atividades:exportar_atividades' 'pdf' %}?{{ request.GET.urlencode }}" class="btn btn-danger me-2">
            <i class="fas fa-file-pdf"></i> Exportar PDF
        </a>
        <a href="{% url 'atividades:exportar_atividades' 'excel' %}?{{ request.GET.urlencode }}" class="btn btn-success me-2">
            <i class="fas fa-file-excel"></i> Exportar Excel
        </a>
        <a href="{% url 'atividades:exportar_atividades' 'csv' %}?{{ request.GET.urlencode }}" class="btn btn-info">
            <i class="fas fa-file-csv"></i> Exportar CSV
        </a>
    </div>
    
    <!-- Resumo -->
    <div class="row mb-4">
        <div class="col-md-4">
            <div class="card bg-light">
                <div class="card-body text-center">
                    <h5 class="card-title">Total de Atividades</h5>
                    <p class="display-4">{{ total_atividades }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card bg-primary text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Atividades Acadêmicas</h5>
                    <p class="display-4">{{ total_academicas }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card bg-info text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Atividades Ritualísticas</h5>
                    <p class="display-4">{{ total_ritualisticas }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Tabela de resultados -->
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">Resultados</h5>
        </div>
        <div class="card-body">
            <ul class="nav nav-tabs mb-3" id="myTab" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="academicas-tab" data-bs-toggle="tab" data-bs-target="#academicas" type="button" role="tab" aria-controls="academicas" aria-selected="true">
                        Atividades Acadêmicas
                    </button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="ritualisticas-tab" data-bs-toggle="tab" data-bs-target="#ritualisticas" type="button" role="tab" aria-controls="ritualisticas" aria-selected="false">
                        Atividades Ritualísticas
                    </button>
                </li>
            </ul>
            <div class="tab-content" id="myTabContent">
                <!-- Atividades Acadêmicas -->
                <div class="tab-pane fade show active" id="academicas" role="tabpanel" aria-labelledby="academicas-tab">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Nome</th>
                                    <th>Tipo</th>
                                    <th>Data de Início</th>
                                    <th>Status</th>
                                    <th>Responsável</th>
                                    <th>Turmas</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for atividade in atividades_academicas %}
                                <tr>
                                    <td>
                                        <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}">
                                            {{ atividade.nome }}
                                        </a>
                                    </td>
                                    <td>{{ atividade.get_tipo_atividade_display }}</td>
                                    <td>{{ atividade.data_inicio|date:"d/m/Y" }}</td>
                                    <td>
                                        <span class="badge {% if atividade.status == 'agendada' %}bg-warning{% elif atividade.status == 'em_andamento' %}bg-info{% elif atividade.status == 'concluida' %}bg-success{% else %}bg-secondary{% endif %}">
                                            {{ atividade.get_status_display }}
                                        </span>
                                    </td>
                                    <td>{{ atividade.responsavel|default:"Não informado" }}</td>
                                    <td>
                                        {% for turma in atividade.turmas.all %}
                                            <span class="badge bg-primary">{{ turma.nome }}</span>
                                        {% empty %}
                                            <span class="text-muted">Nenhuma turma</span>
                                        {% endfor %}
                                    </td>
                                </tr>
                                {% empty %}
                                <tr>
                                    <td colspan="6" class="text-center">Nenhuma atividade acadêmica encontrada.</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <!-- Atividades Ritualísticas -->
                <div class="tab-pane fade" id="ritualisticas" role="tabpanel" aria-labelledby="ritualisticas-tab">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Nome</th>
                                    <th>Data</th>
                                    <th>Horário</th>
                                    <th>Local</th>
                                    <th>Turma</th>
                                    <th>Participantes</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for atividade in atividades_ritualisticas %}
                                <tr>
                                    <td>
                                        <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}">
                                            {{ atividade.nome }}
                                        </a>
                                    </td>
                                    <td>{{ atividade.data|date:"d/m/Y" }}</td>
                                    <td>{{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</td>
                                    <td>{{ atividade.local }}</td>
                                    <td>{{ atividade.turma.nome }}</td>
                                    <td>{{ atividade.participantes.count }}</td>
                                </tr>
                                {% empty %}
                                <tr>
                                    <td colspan="6" class="text-center">Nenhuma atividade ritualística encontrada.</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\visualizar_frequencia.html

html
{% extends 'base.html' %}

{% block title %}Frequência - {{ atividade.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Frequência: {{ atividade.nome }}</h1>
        <div>
            <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'atividades:registrar_frequencia_atividade' atividade.id %}" class="btn btn-primary">Registrar Nova Frequência</a>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Selecionar Data</h5>
                <div>
                    <form method="get" class="d-flex align-items-center">
                        <label for="data" class="me-2">Data:</label>
                        <select name="data" id="data" class="form-select" style="width: auto;" onchange="this.form.submit()">
                            <option value="">Selecione uma data</option>
                            {% for data in datas_disponiveis %}
                                <option value="{{ data|date:'Y-m-d' }}" {% if data|date:'Y-m-d' == data_selecionada|date:'Y-m-d' %}selected{% endif %}>
                                    {{ data|date:"d/m/Y" }}
                                </option>
                            {% endfor %}
                        </select>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
    {% if data_selecionada %}
        <!-- Estatísticas -->
        <div class="row mb-4">
            <div class="col-md-4">
                <div class="card text-white bg-primary">
                    <div class="card-body text-center">
                        <h5 class="card-title">Total de Alunos</h5>
                        <p class="display-4">{{ total_registros }}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card text-white bg-success">
                    <div class="card-body text-center">
                        <h5 class="card-title">Presentes</h5>
                        <p class="display-4">{{ presentes }}</p>
                        <p>{{ taxa_presenca|floatformat:1 }}%</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card text-white bg-danger">
                    <div class="card-body text-center">
                        <h5 class="card-title">Ausentes</h5>
                        <p class="display-4">{{ ausentes }}</p>
                        <p>{{ 100|subtract:taxa_presenca|floatformat:1 }}%</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Gráfico -->
        <div class="card mb-4">
            <div class="card-header">
                <h5>Gráfico de Frequência</h5>
            </div>
            <div class="card-body">
                <canvas id="frequenciaChart" height="200"></canvas>
            </div>
        </div>
        
        <!-- Lista de Alunos -->
        <div class="card">
            <div class="card-header">
                <h5>Lista de Frequência - {{ data_selecionada|date:"d/m/Y" }}</h5>
            </div>
            <div class="card-body">
                {% if frequencias %}
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th style="width: 50px;">#</th>
                                    <th>Aluno</th>
                                    <th style="width: 120px;">Status</th>
                                    <th>Justificativa</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for frequencia in frequencias %}
                                <tr>
                                    <td>{{ forloop.counter }}</td>
                                    <td>
                                        <div class="d-flex align-items-center">
                                            {% if frequencia.aluno.foto %}
                                                <img src="{{ frequencia.aluno.foto.url }}" alt="Foto de {{ frequencia.aluno.nome }}" 
                                                     class="rounded-circle me-2" width="30" height="30" 
                                                     style="object-fit: cover;">
                                            {% else %}
                                                <div class="rounded-circle bg-secondary me-2 d-flex align-items-center justify-content-center" 
                                                     style="width: 30px; height: 30px; color: white;">
                                                    {{ frequencia.aluno.nome|first|upper }}
                                                </div>
                                            {% endif %}
                                            <div>
                                                <div>{{ frequencia.aluno.nome }}</div>
                                                <small class="text-muted">{{ frequencia.aluno.numero_iniciatico|default:"Sem número iniciático" }}</small>
                                            </div>
                                        </div>
                                    </td>
                                    <td>
                                        {% if frequencia.presente %}
                                            <span class="badge bg-success">Presente</span>
                                        {% else %}
                                            <span class="badge bg-danger">Ausente</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        {% if not frequencia.presente %}
                                            {{ frequencia.justificativa|default:"Sem justificativa" }}
                                        {% else %}
                                            -
                                        {% endif %}
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                {% else %}
                    <div class="alert alert-info">
                        <p>Não há registros de frequência para esta data.</p>
                    </div>
                {% endif %}
            </div>
        </div>
    {% else %}
        <div class="alert alert-info">
            <p>Selecione uma data para visualizar os registros de frequência.</p>
        </div>
    {% endif %}
</div>
{% endblock %}

{% block extra_js %}
{% if data_selecionada %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        var ctx = document.getElementById('frequenciaChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Presentes', 'Ausentes'],
                datasets: [{
                    data: [{{ presentes }}, {{ ausentes }}],
                    backgroundColor: [
                        'rgba(40, 167, 69, 0.8)',
                        'rgba(220, 53, 69, 0.8)'
                    ],
                    borderColor: [
                        'rgba(40, 167, 69, 1)',
                        'rgba(220, 53, 69, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Distribuição de Frequência'
                    }
                }
            }
        });
    });
</script>
{% endif %}
{% endblock %}


'''