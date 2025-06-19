'''
# Revisão da Funcionalidade: atividades

## Arquivos forms.py:


### Arquivo: atividades\templates\atividades\ritualisticas\detalhar_atividade_ritualistica.html

html
{% extends 'base.html' %}
{% load static %}
{% block title %}Detalhes da Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{{ atividade.nome }}</h1>
        <div>
            <a href="{{ return_url }}" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-secondary me-2">Lista de Atividades</a>
            <a href="{% url 'atividades:editar_atividade_ritualistica' atividade.id %}?return_url={{ request.path|urlencode }}" class="btn btn-warning me-2">Editar</a>
            <!-- Novo botão para copiar atividade -->
            <a href="{% url 'atividades:copiar_atividade_ritualistica' atividade.id %}" class="btn btn-secondary me-2">Copiar</a>
            <a href="{% url 'atividades:confirmar_exclusao_ritualistica' atividade.id %}?return_url={{ request.path|urlencode }}" class="btn btn-danger">Excluir</a>
        </div>
    </div>    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="row">
        <div class="col-md-8">
            <div class="card mb-4">
                <div class="card-header">
                    <h5>Informações Básicas</h5>
                </div>
                <div class="card-body">
                    <p><strong>Descrição:</strong> {{ atividade.descricao|default:"Não informada" }}</p>
                    <p><strong>Data:</strong> {{ atividade.data|date:"d/m/Y" }}</p>
                    <p><strong>Horário:</strong> {{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</p>
                    <p><strong>Local:</strong> {{ atividade.local }}</p>
                    <p><strong>Turma:</strong> {{ atividade.turma }}</p>
                    <p><strong>Convocação:</strong>
    {% if atividade.convocacao %}
        <span class="badge bg-success">Sim</span>
    {% else %}
        <span class="badge bg-secondary">Não</span>
    {% endif %}
</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="card mb-4">
                <div class="card-header">
                    <h5>Estatísticas</h5>
                </div>
                <div class="card-body">
                    <p><strong>Total de Participantes:</strong> {{ total_participantes }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Participantes</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>Número Iniciático</th>
                            <th>Email</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for aluno in atividade.participantes.all %}
                            <tr>
                                <td>{{ aluno.nome }}</td>
                                <td>{{ aluno.numero_iniciatico|default:"N/A" }}</td>
                                <td>{{ aluno.email }}</td>
                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="3" class="text-center">
                                    <p class="my-3">Nenhum participante cadastrado para esta atividade.</p>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: atividades\templates\atividades\ritualisticas\editar_atividade_ritualistica.html

html
{% extends 'base.html' %}
{% load static %}
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
                        <label for="id_nome" class="form-label">
                            {{ form.nome.label }} <span class="text-danger">*</span>
                        </label>
                        {{ form.nome }}
                        {% for error in form.nome.errors %}
                            <div class="text-danger">{{ error }}</div>
                        {% endfor %}
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
                        <label for="id_data" class="form-label">
                            {{ form.data.label }} <span class="text-danger">*</span>
                        </label>
                        {{ form.data }}
                        {% for error in form.data.errors %}
                            <div class="text-danger">{{ error }}</div>
                        {% endfor %}
                    </div>
                    <div class="col-md-4">
                        <label for="id_hora_inicio" class="form-label">
                            {{ form.hora_inicio.label }} <span class="text-danger">*</span>
                        </label>
                        {{ form.hora_inicio }}
                        {% for error in form.hora_inicio.errors %}
                            <div class="text-danger">{{ error }}</div>
                        {% endfor %}
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
        
        <div class="row mt-3">
            <div class="col-md-6">
                <label for="id_status" class="form-label">
                    {{ form.status.label }} <span class="text-danger">*</span>
                </label>
                {{ form.status }}
                {% for error in form.status.errors %}
                    <div class="text-danger">{{ error }}</div>
                {% endfor %}
            </div>
        </div>
        
        <div class="mb-3 form-check">
            {{ form.convocacao }}
            <label class="form-check-label" for="id_convocacao">Convocação</label>
            {% for error in form.convocacao.errors %}
                <div class="text-danger">{{ error }}</div>
            {% endfor %}
        </div>
        
        <div class="d-flex justify-content-between mb-5 mt-4">
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
            if (todosAlunosCheckbox && participantesContainer) {
                participantesContainer.style.display = todosAlunosCheckbox.checked ? 'none' : 'block';
            }
        }
        if (todosAlunosCheckbox) {
            toggleParticipantes();
            todosAlunosCheckbox.addEventListener('change', toggleParticipantes);
        }

        // Highlight campos obrigatórios
        function highlightRequiredFields(form) {
            const obrigatorios = [
                'id_nome',
                'id_data',
                'id_hora_inicio',
                'id_status'
            ];
            let algumErro = false;
            obrigatorios.forEach(function(id) {
                const field = document.getElementById(id);
                if (field) {
                    field.classList.remove('is-required-error');
                    if (!field.value || (field.type === "select-one" && !field.value)) {
                        field.classList.add('is-required-error');
                        algumErro = true;
                    }
                }
            });
            return !algumErro;
        }

        const form = document.querySelector('form');
        if (form) {
            form.addEventListener('submit', function(e) {
                if (!highlightRequiredFields(form)) {
                    e.preventDefault();
                    const erro = form.querySelector('.is-required-error');
                    if (erro) erro.focus();
                }
            });
        }
    });
</script>
{% endblock %}




### Arquivo: atividades\templates\atividades\ritualisticas\excluir_atividade_ritualistica.html

html
{% extends 'base.html' %}
{% load static %}
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




### Arquivo: atividades\templates\atividades\ritualisticas\form_atividade_ritualistica.html

html
{% extends 'base.html' %}
{% load static %}
{% block title %}Criar Nova Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Nova Atividade Ritualística</h1>
        <a href="/atividades/ritualisticas/" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    <div class="row">
        <div class="col-md-8">
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Dados da Atividade</h5>
                </div>
                <div class="card-body">
                    <form method="post" enctype="multipart/form-data" novalidate>
                        {% csrf_token %}
                        <div class="mb-3">
                            <label for="id_nome" class="form-label">Nome da Atividade</label>
                            <input type="text" name="nome" class="form-control" maxlength="100" required id="id_nome" value="{{ form.nome.value|default_if_none:'' }}">
                        </div>
                        <div class="mb-3">
                            <label for="id_descricao" class="form-label">Descrição</label>
                            <textarea name="descricao" cols="40" rows="3" class="form-control" id="id_descricao">{{ form.descricao.value|default_if_none:'' }}</textarea>
                        </div>
                        <div class="row">
                            <div class="col-md-4 mb-3">
                                <label for="id_data" class="form-label">Data</label>
                                <input type="date" name="data" class="form-control" required id="id_data" value="{{ form.data.value|default_if_none:'' }}">
                            </div>
                            <div class="col-md-4 mb-3">
                                <label for="id_hora_inicio" class="form-label">Hora de Início</label>
                                <input type="time" name="hora_inicio" class="form-control" required id="id_hora_inicio" value="{{ form.hora_inicio.value|default_if_none:'' }}">
                            </div>
                            <div class="col-md-4 mb-3">
                                <label for="id_hora_fim" class="form-label">Hora de Término</label>
                                <input type="time" name="hora_fim" class="form-control" id="id_hora_fim" value="{{ form.hora_fim.value|default_if_none:'' }}">
                                <small class="form-text text-muted">Opcional. Se não informada, será considerada 1 hora após o início.</small>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="id_local" class="form-label">Local</label>
                            <input type="text" name="local" class="form-control" maxlength="100" id="id_local" value="{{ form.local.value|default_if_none:'' }}">
                        </div>
                        <div class="mb-3">
                            <label for="id_responsavel" class="form-label">Responsável</label>
                            <input type="text" name="responsavel" class="form-control" maxlength="100" id="id_responsavel" value="{{ form.responsavel.value|default_if_none:'' }}">
                        </div>
                        <div class="mb-3">
                            <label for="id_turma" class="form-label">Turma</label>
                            <select name="turma" class="form-control" id="id_turma">
                                {% for turma in form.turma.field.choices %}
                                    <option value="{{ turma.0 }}" {% if form.turma.value == turma.0 %}selected{% endif %}>{{ turma.1 }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="mb-3">
                            <div class="form-check">
                                <input type="checkbox" name="todos_alunos" class="form-check-input" id="id_todos_alunos" {% if form.todos_alunos.value %}checked{% endif %}>
                                <label class="form-check-label" for="id_todos_alunos">Incluir todos os alunos da turma</label>
                            </div>
                        </div>
                        <div class="mb-3" id="participantes-container">
                            <label for="id_participantes" class="form-label">Participantes</label>
                            <select name="participantes" class="form-control" id="id_participantes" multiple>
                                {% for participante in form.participantes.field.choices %}
                                    <option value="{{ participante.0 }}" {% if participante.0 in form.participantes.value %}selected{% endif %}>{{ participante.1 }}</option>
                                {% endfor %}
                            </select>
                            <small class="form-text text-muted">Selecione os participantes manualmente ou marque "Incluir todos os alunos".</small>
                        </div>
                        <div class="mb-3 form-check">
                            {{ form.convocacao }}
                            <label class="form-check-label" for="id_convocacao">Convocação</label>
                            {% for error in form.convocacao.errors %}
                                <div class="text-danger">{{ error }}</div>
                            {% endfor %}
                        </div>
                        <div class="d-flex justify-content-between">
                            <a href="/atividades/ritualisticas/" class="btn btn-secondary">
                                <i class="fas fa-times"></i> Cancelar
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Criar Atividade
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card mb-4">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">Informações</h5>
                </div>
                <div class="card-body">
                    <p>Preencha os dados para cadastrar uma nova atividade ritualística.</p>
                    <ul>
                        <li>Campos obrigatórios estão marcados com <span class="text-danger">*</span>.</li>
                        <li>Você pode adicionar participantes manualmente ou incluir todos da turma.</li>
                        <li>Se não informar hora de término, será considerada 1 hora após o início.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const todosAlunosCheckbox = document.getElementById('id_todos_alunos');
        const participantesContainer = document.getElementById('participantes-container');
        function toggleParticipantes() {
            if (todosAlunosCheckbox && participantesContainer) {
                participantesContainer.style.display = todosAlunosCheckbox.checked ? 'none' : 'block';
            }
        }
        if (todosAlunosCheckbox) {
            toggleParticipantes();
            todosAlunosCheckbox.addEventListener('change', toggleParticipantes);
        }
    });
</script>
{% endblock %}



### Arquivo: atividades\templates\atividades\ritualisticas\formulario_atividade_ritualistica.html

html
{% extends 'base.html' %}
{% load static %}
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



### Arquivo: atividades\templates\atividades\ritualisticas\importar_atividades_ritualisticas.html

html
<!-- filepath: c:\projetos\omaum\atividades\templates\atividades\importar_atividades_academicas.html -->
{% extends 'base.html' %}
{% block title %}Importar Atividades Ritualísticas{% endblock %}
{% block content %}
<div class="container mt-4">
    <h2>Importar Atividades Ritualísticas (CSV)</h2>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <div class="mb-3">
            <label for="csv_file" class="form-label">Arquivo CSV</label>
            <input type="file" name="csv_file" id="csv_file" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-success">Importar</button>
        <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\ritualisticas\listar_atividades_ritualisticas.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Lista de Atividades Ritualísticas{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Atividades Ritualísticas</h1>
        <div class="d-flex gap-2">
            <!-- 1. Voltar ao Painel de Controle -->
            <a href="{% url 'atividades:dashboard_atividades' %}" class="btn btn-outline-secondary" data-bs-toggle="tooltip" title="Voltar ao Painel de Controle">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <!-- 2. Nova Atividade -->
            <a href="{% url 'atividades:criar_atividade_ritualistica' %}" class="btn btn-success" data-bs-toggle="tooltip" title="Criar nova atividade ritualística">
                <i class="fas fa-plus"></i> Nova Atividade
            </a>
            <!-- 3. Relatórios -->
            <a href="{% url 'atividades:relatorio_atividades_ritualisticas' %}" class="btn btn-outline-primary" data-bs-toggle="tooltip" title="Relatórios">
                <i class="fas fa-file-alt"></i> Relatórios
            </a>
            <!-- 4. Importar CSV -->
            <a href="{% url 'atividades:importar_atividades_ritualisticas' %}" class="btn btn-outline-success" data-bs-toggle="tooltip" title="Importar atividades via CSV">
                <i class="fas fa-file-import"></i> Importar CSV
            </a>
            <!-- 5. Exportar -->
            <div class="btn-group">
                <button type="button" class="btn btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false" title="Exportar atividades" data-bs-toggle="tooltip">
                    <i class="fas fa-file-export"></i> Exportar
                </button>
                <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="?exportar=csv">Exportar CSV</a></li>
                    <li><a class="dropdown-item" href="?exportar=excel">Exportar Excel</a></li>
                    <li><a class="dropdown-item" href="?exportar=pdf" target="_blank">Exportar PDF</a></li>
                </ul>
            </div>
        </div>
    </div>

    <!-- Filtros -->
    <form method="get" class="row g-3 mb-4">
        <div class="col-md-4">
            <label for="id_q" class="form-label">Busca</label>
            <input type="text" name="q" id="id_q" class="form-control" placeholder="Buscar por nome, descrição ou local" value="{{ query }}">
        </div>
        <div class="col-md-3">
            <label for="id_turma" class="form-label">Turma</label>
            <select name="turma" id="id_turma" class="form-select">
                <option value="">Todas as turmas</option>
                {% for turma in turmas %}
                    <option value="{{ turma.id }}" {% if turma.id|stringformat:"s" == turma_selecionada|stringformat:"s" %}selected{% endif %}>
                        {{ turma.nome }}
                    </option>
                {% endfor %}
            </select>
        </div>
        <div class="col-md-5 d-grid gap-2 d-md-flex justify-content-md-end align-items-end">
            <button type="submit" class="btn btn-primary">
                <i class="fas fa-search"></i> Filtrar
            </button>
        </div>
    </form>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">{{ message }}</div>
        {% endfor %}
    {% endif %}

    <!-- Tabela de atividades ritualísticas -->
    <div class="table-responsive">
        <table class="table align-middle table-hover">
            <thead class="table-light">
                <tr>
                    <th>Nome</th>
                    <th>Data</th>
                    <th>Horário</th>
                    <th>Local</th>
                    <th>Turma</th>
                    <th>Convocação</th>
                    <th class="text-start">Ações</th>
                </tr>
            </thead>
            <tbody>
                {% for atividade in atividades %}
                <tr>
                    <td>{{ atividade.nome }}</td>
                    <td>{{ atividade.data|date:"d/m/Y" }}</td>
                    <td>{{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</td>
                    <td>{{ atividade.local }}</td>
                    <td>
                        {% if atividade.turma %}
                            <span class="badge bg-info">{{ atividade.turma }}</span>
                        {% else %}
                            <span class="text-muted">-</span>
                        {% endif %}
                    </td>
                    <td>
                        {% if atividade.convocacao %}
                            <span class="badge bg-success">Sim</span>
                        {% else %}
                            <span class="badge bg-secondary">Não</span>
                        {% endif %}
                    </td>
                    <td class="text-start">
                        <div class="btn-group btn-group-sm" role="group">
                            <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-info" title="Detalhar atividade" data-bs-toggle="tooltip">
                                <i class="fas fa-eye"></i>
                            </a>
                            <a href="{% url 'atividades:editar_atividade_ritualistica' atividade.id %}" class="btn btn-warning" title="Editar atividade" data-bs-toggle="tooltip">
                                <i class="fas fa-edit"></i>
                            </a>
                            <a href="{% url 'atividades:excluir_atividade_ritualistica' atividade.id %}" class="btn btn-danger" title="Excluir atividade" data-bs-toggle="tooltip">
                                <i class="fas fa-trash"></i>
                            </a>
                            <a href="{% url 'atividades:copiar_atividade_ritualistica' atividade.id %}" class="btn btn-secondary" title="Copiar atividade" data-bs-toggle="tooltip">
                                <i class="fas fa-copy"></i>
                            </a>
                        </div>
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="7" class="text-center">Nenhuma atividade ritualística encontrada.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <!-- Paginação -->
    {% if page_obj.has_other_pages %}
    <nav aria-label="Paginação">
        <ul class="pagination justify-content-center">
            {% if page_obj.has_previous %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% if query %}&q={{ query }}{% endif %}{% if turma_selecionada %}&turma={{ turma_selecionada }}{% endif %}">&laquo;</a>
                </li>
            {% else %}
                <li class="page-item disabled"><span class="page-link">&laquo;</span></li>
            {% endif %}
            {% for num in page_obj.paginator.page_range %}
                {% if page_obj.number == num %}
                    <li class="page-item active"><span class="page-link">{{ num }}</span></li>
                {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                    <li class="page-item"><a class="page-link" href="?page={{ num }}{% if query %}&q={{ query }}{% endif %}{% if turma_selecionada %}&turma={{ turma_selecionada }}{% endif %}">{{ num }}</a></li>
                {% endif %}
            {% endfor %}
            {% if page_obj.has_next %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ page_obj.next_page_number }}{% if query %}&q={{ query }}{% endif %}{% if turma_selecionada %}&turma={{ turma_selecionada }}{% endif %}">&raquo;</a>
                </li>
            {% else %}
                <li class="page-item disabled"><span class="page-link">&raquo;</span></li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}

    <!-- Botão Voltar ao final da listagem -->
    <div class="mt-3">
        <a href="{% url 'atividades:dashboard_atividades' %}" class="btn btn-outline-secondary">
            <i class="fas fa-arrow-left"></i> Menu inicial
        </a>
    </div>
</div>
{% endblock %}




### Arquivo: atividades\templates\atividades\ritualisticas\relatorio_atividades_ritualisticas.html

html
{% extends 'base.html' %}
{% load static %}
{% block title %}Relatório de Atividades Ritualísticas{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Relatório de Atividades Ritualísticas</h1>
    <form method="get" class="row g-3 mb-4">
        <div class="col-md-4">
            <label for="turma" class="form-label">Turma</label>
            <select name="turma" id="turma" class="form-select">
                <option value="">Todas as turmas</option>
                {% for turma in turmas %}
                    <option value="{{ turma.id }}" {% if turma_selecionada == turma.id|stringformat:"s" %}selected{% endif %}>{{ turma.nome }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="col-md-4">
            <label for="data" class="form-label">Data</label>
            <input type="date" name="data" id="data" class="form-control" value="{{ data_selecionada }}">
        </div>
        <div class="col-md-4 d-flex align-items-end">
            <button type="submit" class="btn btn-primary me-2">
                <i class="fas fa-search"></i> Filtrar
            </button>
            <a href="{% url 'atividades:relatorio_atividades_ritualisticas' %}" class="btn btn-outline-secondary">
                Limpar
            </a>
        </div>
    </form>
    <div class="card">
        <div class="card-body">
            {% if atividades %}
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>Data</th>
                            <th>Horário</th>
                            <th>Local</th>
                            <th>Turma</th>
                            <th>Convocação</th> <!-- NOVA COLUNA -->
                            <th>Descrição</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for atividade in atividades %}
                        <tr>
                            <td>{{ atividade.nome }}</td>
                            <td>{{ atividade.data|date:"d/m/Y" }}</td>
                            <td>
                                {% if atividade.hora_inicio and atividade.hora_fim %}
                                    {{ atividade.hora_inicio }} - {{ atividade.hora_fim }}
                                {% else %}
                                    <span class="text-muted">-</span>
                                {% endif %}
                            </td>
                            <td>{{ atividade.local }}</td>
                            <td>
                                {% if atividade.turma %}
                                    <span class="badge bg-info">{{ atividade.turma }}</span>
                                {% else %}
                                    <span class="text-muted">-</span>
                                {% endif %}
                            </td>
                            <td>
                                {% if atividade.convocacao %}
                                    <span class="badge bg-success">Sim</span>
                                {% else %}
                                    <span class="badge bg-secondary">Não</span>
                                {% endif %}
                            </td>
                            <td>{{ atividade.descricao|default:"-" }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            {% else %}
                <div class="alert alert-warning">
                    Nenhuma atividade ritualística encontrada para o filtro selecionado.
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\visualizar_frequencia.html

html
{% extends 'base.html' %}
{% load static %}
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