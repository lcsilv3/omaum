'''
# Revisão da Funcionalidade: atividades

## Arquivos forms.py:


### Arquivo: atividades\templates\atividades\academicas\criar_atividade_academica.html

html
{% extends 'base.html' %}
{% load static %}
{% block title %}Criar Nova Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Nova Atividade Acadêmica</h1>
        <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    <div class="row">
        <div class="col-md-8">
            <form method="post" enctype="multipart/form-data" novalidate>
                {% csrf_token %}
                <!-- Seção 1: Informações Básicas -->
                <div class="card mb-4">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">Informações Básicas</h5>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <label for="id_nome" class="form-label">
                                Nome da Atividade <span class="text-danger">*</span>
                            </label>
                            {{ form.nome }}
                            {% for error in form.nome.errors %}
                                <div class="text-danger">{{ error }}</div>
                            {% endfor %}
                        </div>
                        <div class="mb-3">
                            <label for="id_descricao" class="form-label">Descrição</label>
                            {{ form.descricao }}
                            {% for error in form.descricao.errors %}
                                <div class="text-danger">{{ error }}</div>
                            {% endfor %}
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="id_tipo_atividade" class="form-label">
                                    Tipo de Atividade <span class="text-danger">*</span>
                                </label>
                                {{ form.tipo_atividade }}
                                {% for error in form.tipo_atividade.errors %}
                                    <div class="text-danger">{{ error }}</div>
                                {% endfor %}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="id_status" class="form-label">
                                    Status <span class="text-danger">*</span>
                                </label>
                                {{ form.status }}
                                {% for error in form.status.errors %}
                                    <div class="text-danger">{{ error }}</div>
                                {% endfor %}
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Seção 2: Datas e Horários -->
                <div class="card mb-4">
                    <div class="card-header bg-secondary text-white">
                        <h5 class="mb-0">Datas e Horários</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="id_data_inicio" class="form-label">
                                    Data de Início <span class="text-danger">*</span>
                                </label>
                                {{ form.data_inicio }}
                                {% for error in form.data_inicio.errors %}
                                    <div class="text-danger">{{ error }}</div>
                                {% endfor %}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="id_data_fim" class="form-label">Data de Término</label>
                                {{ form.data_fim }}
                                {% for error in form.data_fim.errors %}
                                    <div class="text-danger">{{ error }}</div>
                                {% endfor %}
                                <small class="form-text text-muted">Opcional. Se não informada, será considerada a mesma data de início.</small>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="id_hora_inicio" class="form-label">
                                    Hora de Início <span class="text-danger">*</span>
                                </label>
                                {{ form.hora_inicio }}
                                {% for error in form.hora_inicio.errors %}
                                    <div class="text-danger">{{ error }}</div>
                                {% endfor %}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="id_hora_fim" class="form-label">Hora de Término</label>
                                {{ form.hora_fim }}
                                {% for error in form.hora_fim.errors %}
                                    <div class="text-danger">{{ error }}</div>
                                {% endfor %}
                                <small class="form-text text-muted">Opcional. Se não informada, será considerada 1 hora após o início.</small>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Seção 3: Vínculos -->
                <div class="card mb-4">
                    <div class="card-header bg-info text-white">
                        <h5 class="mb-0">Vínculos</h5>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <label for="id_local" class="form-label">Local</label>
                            {{ form.local }}
                            {% for error in form.local.errors %}
                                <div class="text-danger">{{ error }}</div>
                            {% endfor %}
                        </div>
                        <div class="mb-3">
                            <label for="id_responsavel" class="form-label">Responsável</label>
                            {{ form.responsavel }}
                            {% for error in form.responsavel.errors %}
                                <div class="text-danger">{{ error }}</div>
                            {% endfor %}
                        </div>
                        <div class="mb-3 position-relative">
                            <label for="id_curso" class="form-label">Curso</label>
                            {{ form.curso }}
                            {% for error in form.curso.errors %}
                                <div class="text-danger">{{ error }}</div>
                            {% endfor %}
                        </div>
                        <div class="mb-3">
                            <label for="id_turmas" class="form-label">Turmas</label>
                            <div class="d-flex align-items-center mb-2">
                                <input type="checkbox" id="select-all-turmas" class="form-check-input me-2">
                                <label for="select-all-turmas" class="form-check-label">Selecionar todas as turmas</label>
                            </div>
                            {{ form.turmas }}
                            <div id="no-turmas-msg" class="text-muted mt-2"></div>
                            {% for error in form.turmas.errors %}
                                <div class="text-danger">{{ error }}</div>
                            {% endfor %}
                            <small class="form-text text-muted">Selecione uma ou mais(CTRL) turmas para esta atividade.</small>
                        </div>
                        <div class="mb-3 form-check">
                            {{ form.convocacao }}
                            <label class="form-check-label" for="id_convocacao">Convocação</label>
                            {% for error in form.convocacao.errors %}
                                <div class="text-danger">{{ error }}</div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
                <div class="d-flex justify-content-between mb-4">
                    <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">
                        <i class="fas fa-times"></i> Cancelar
                    </a>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-save"></i> Criar Atividade
                    </button>
                </div>
            </form>
        </div>
        <div class="col-md-4">
            <div class="card mb-4">
                <div class="card-header bg-light">
                    <h5 class="mb-0">Dicas</h5>
                </div>
                <div class="card-body">
                    <ul>
                        <li>Preencha todos os campos obrigatórios <span class="text-danger">*</span>.</li>
                        <li>Use datas e horários corretos para evitar conflitos.</li>
                        <li>Associe a atividade a uma ou mais turmas.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/atividades_ajax.js' %}"></script>
<script>
    window.initTurmasAjax();

    function highlightRequiredFields(form) {
        // IDs dos campos obrigatórios
        const obrigatorios = [
            'id_nome',
            'id_tipo_atividade',
            'id_data_inicio',
            'id_hora_inicio',
            'id_status'
        ];
        let algumErro = false;
        obrigatorios.forEach(function(id) {
            const field = document.getElementById(id);
            if (field) {
                // Remove highlight anterior
                field.classList.remove('is-required-error');
                // Checa se está vazio
                if (!field.value || (field.type === "select-one" && !field.value)) {
                    field.classList.add('is-required-error');
                    algumErro = true;
                }
            }
        });
        return !algumErro;
    }

    document.addEventListener('DOMContentLoaded', function() {
        const form = document.querySelector('form');
        if (form) {
            form.addEventListener('submit', function(e) {
                if (!highlightRequiredFields(form)) {
                    e.preventDefault();
                    // Foca no primeiro campo com erro
                    const erro = form.querySelector('.is-required-error');
                    if (erro) erro.focus();
                }
            });
        }
    });
</script>
{% endblock %}



### Arquivo: atividades\templates\atividades\academicas\detalhar_atividade_academica.html

html
{% extends 'base.html' %}
{% load static %}
{% block title %}Detalhes da Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card">
        <div class="card-header">
            <h2>{{ atividade.nome }}</h2>
        </div>
        <div class="card-body">
            <dl class="row">
                <dt class="col-sm-3">Curso:</dt>
                <dd class="col-sm-9">{{ atividade.curso }}</dd>
                <dt class="col-sm-3">Turmas:</dt>
                <dd class="col-sm-9">
                    {% for turma in atividade.turmas.all %}
                        <span class="badge bg-info">{{ turma.nome }}</span>
                    {% empty %}
                        <span class="text-muted">-</span>
                    {% endfor %}
                </dd>
                <dt class="col-sm-3">Convocação:</dt>
                <dd class="col-sm-9">
                    {% if atividade.convocacao %}
                        <span class="badge bg-success">Sim</span>
                    {% else %}
                        <span class="badge bg-secondary">Não</span>
                    {% endif %}
                </dd>
                <!-- Adicione outros campos relevantes aqui -->
            </dl>
            <div class="mt-4">
                <a href="{% url 'atividades:editar_atividade_academica' atividade.id %}" class="btn btn-primary">Editar</a>
                <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">Voltar para a lista</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\academicas\editar_atividade_academica.html

html
{% extends 'base.html' %}
{% load static %}
{% block title %}Editar Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Editar Atividade Acadêmica</h1>
        <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar para detalhes
        </a>
    </div>
    <div class="row">
        <div class="col-md-8">
            <form method="post" enctype="multipart/form-data" novalidate>
                {% csrf_token %}
                <!-- Seção 1: Informações Básicas -->
                <div class="card mb-4">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">Informações Básicas</h5>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <label for="id_nome" class="form-label">
                                Nome da Atividade <span class="text-danger">*</span>
                            </label>
                            {{ form.nome }}
                            {% for error in form.nome.errors %}
                                <div class="text-danger">{{ error }}</div>
                            {% endfor %}
                        </div>
                        <div class="mb-3">
                            <label for="id_descricao" class="form-label">Descrição</label>
                            {{ form.descricao }}
                            {% for error in form.descricao.errors %}
                                <div class="text-danger">{{ error }}</div>
                            {% endfor %}
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="id_tipo_atividade" class="form-label">
                                    Tipo de Atividade <span class="text-danger">*</span>
                                </label>
                                {{ form.tipo_atividade }}
                                {% for error in form.tipo_atividade.errors %}
                                    <div class="text-danger">{{ error }}</div>
                                {% endfor %}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="id_status" class="form-label">
                                    Status <span class="text-danger">*</span>
                                </label>
                                {{ form.status }}
                                {% for error in form.status.errors %}
                                    <div class="text-danger">{{ error }}</div>
                                {% endfor %}
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Seção 2: Datas e Horários -->
                <div class="card mb-4">
                    <div class="card-header bg-secondary text-white">
                        <h5 class="mb-0">Datas e Horários</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="id_data_inicio" class="form-label">
                                    Data de Início <span class="text-danger">*</span>
                                </label>
                                {{ form.data_inicio }}
                                {% for error in form.data_inicio.errors %}
                                    <div class="text-danger">{{ error }}</div>
                                {% endfor %}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="id_data_fim" class="form-label">Data de Término</label>
                                {{ form.data_fim }}
                                {% for error in form.data_fim.errors %}
                                    <div class="text-danger">{{ error }}</div>
                                {% endfor %}
                                <small class="form-text text-muted">Opcional. Se não informada, será considerada a mesma data de início.</small>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="id_hora_inicio" class="form-label">
                                    Hora de Início <span class="text-danger">*</span>
                                </label>
                                {{ form.hora_inicio }}
                                {% for error in form.hora_inicio.errors %}
                                    <div class="text-danger">{{ error }}</div>
                                {% endfor %}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="id_hora_fim" class="form-label">Hora de Término</label>
                                {{ form.hora_fim }}
                                {% for error in form.hora_fim.errors %}
                                    <div class="text-danger">{{ error }}</div>
                                {% endfor %}
                                <small class="form-text text-muted">Opcional. Se não informada, será considerada 1 hora após o início.</small>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Seção 3: Vínculos -->
                <div class="card mb-4">
                    <div class="card-header bg-info text-white">
                        <h5 class="mb-0">Vínculos</h5>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <label for="id_local" class="form-label">Local</label>
                            {{ form.local }}
                            {% for error in form.local.errors %}
                                <div class="text-danger">{{ error }}</div>
                            {% endfor %}
                        </div>
                        <div class="mb-3">
                            <label for="id_responsavel" class="form-label">Responsável</label>
                            {{ form.responsavel }}
                            {% for error in form.responsavel.errors %}
                                <div class="text-danger">{{ error }}</div>
                            {% endfor %}
                        </div>
                        <div class="mb-3 position-relative">
                            <label for="id_curso" class="form-label">Curso</label>
                            {{ form.curso }}
                            {% for error in form.curso.errors %}
                                <div class="text-danger">{{ error }}</div>
                            {% endfor %}
                        </div>
                        <div class="mb-3">
                            <label for="id_turmas" class="form-label">Turmas</label>
                            <div class="d-flex align-items-center mb-2">
                                <input type="checkbox" id="select-all-turmas" class="form-check-input me-2">
                                <label for="select-all-turmas" class="form-check-label">Selecionar todas as turmas</label>
                            </div>
                            {{ form.turmas }}
                            <div id="no-turmas-msg" class="text-muted mt-2"></div>
                            {% for error in form.turmas.errors %}
                                <div class="text-danger">{{ error }}</div>
                            {% endfor %}
                            <small class="form-text text-muted">Selecione uma ou mais(CTRL) turmas para esta atividade.</small>
                        </div>
                        <div class="mb-3 form-check">
                            {{ form.convocacao }}
                            <label class="form-check-label" for="id_convocacao">Convocação</label>
                            {% for error in form.convocacao.errors %}
                                <div class="text-danger">{{ error }}</div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
                <div class="d-flex justify-content-between mb-4">
                    <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-secondary">
                        <i class="fas fa-times"></i> Cancelar
                    </a>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-save"></i> Salvar Alterações
                    </button>
                </div>
            </form>
        </div>
        <div class="col-md-4">
            <div class="card mb-4">
                <div class="card-header bg-light">
                    <h5 class="mb-0">Dicas</h5>
                </div>
                <div class="card-body">
                    <ul>
                        <li>Preencha todos os campos obrigatórios <span class="text-danger">*</span>.</li>
                        <li>Use datas e horários corretos para evitar conflitos.</li>
                        <li>Associe a atividade a uma ou mais turmas.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/atividades_ajax.js' %}"></script>
<script>
    window.initTurmasAjax();

    function highlightRequiredFields(form) {
        // IDs dos campos obrigatórios
        const obrigatorios = [
            'id_nome',
            'id_tipo_atividade',
            'id_data_inicio',
            'id_hora_inicio',
            'id_status'
        ];
        let algumErro = false;
        obrigatorios.forEach(function(id) {
            const field = document.getElementById(id);
            if (field) {
                // Remove highlight anterior
                field.classList.remove('is-required-error');
                // Checa se está vazio
                if (!field.value || (field.type === "select-one" && !field.value)) {
                    field.classList.add('is-required-error');
                    algumErro = true;
                }
            }
        });
        return !algumErro;
    }

    document.addEventListener('DOMContentLoaded', function() {
        const form = document.querySelector('form');
        if (form) {
            form.addEventListener('submit', function(e) {
                if (!highlightRequiredFields(form)) {
                    e.preventDefault();
                    // Foca no primeiro campo com erro
                    const erro = form.querySelector('.is-required-error');
                    if (erro) erro.focus();
                }
            });
        }
    });
</script>
{% endblock %}




### Arquivo: atividades\templates\atividades\academicas\excluir_atividade_academica.html

html
{% extends 'base.html' %}
{% load static %}
{% block title %}Excluir Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Atividade Acadêmica</h1>
    <div class="alert alert-danger">
        <p>Tem certeza que deseja excluir a atividade <strong>{{ atividade.nome }}</strong>?</p>
        <p><strong>Curso:</strong> {{ atividade.curso }}</p>
        <p><strong>Turmas:</strong>
            {% for turma in atividade.turmas.all %}
                {{ turma.nome }}{% if not forloop.last %}, {% endif %}
            {% endfor %}
        </p>
    </div>
    <form method="post">
        {% csrf_token %}
        <button type="submit" class="btn btn-danger">Confirmar Exclusão</button>
        <a href="{% url 'atividades:detalhar_atividade_academica' atividade.pk %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




### Arquivo: atividades\templates\atividades\academicas\form_atividade_academica.html

html
<form method="post" enctype="multipart/form-data" novalidate>
    {% csrf_token %}
    <div class="mb-3">
        <label for="id_nome" class="form-label">Nome da Atividade</label>
        {{ form.nome }}
        {% for error in form.nome.errors %}
            <div class="text-danger">{{ error }}</div>
        {% endfor %}
    </div>
    <div class="mb-3">
        <label for="id_descricao" class="form-label">Descrição</label>
        {{ form.descricao }}
        {% for error in form.descricao.errors %}
            <div class="text-danger">{{ error }}</div>
        {% endfor %}
    </div>
    <div class="mb-3">
        <label for="id_tipo_atividade" class="form-label">Tipo de Atividade</label>
        {{ form.tipo_atividade }}
        {% for error in form.tipo_atividade.errors %}
            <div class="text-danger">{{ error }}</div>
        {% endfor %}
    </div>
    <div class="mb-3">
        <label for="id_status" class="form-label">Status</label>
        {{ form.status }}
        {% for error in form.status.errors %}
            <div class="text-danger">{{ error }}</div>
        {% endfor %}
    </div>
    <div class="mb-3">
        <label for="id_data_inicio" class="form-label">Data de Início</label>
        {{ form.data_inicio }}
        {% for error in form.data_inicio.errors %}
            <div class="text-danger">{{ error }}</div>
        {% endfor %}
    </div>
    <div class="mb-3">
        <label for="id_data_fim" class="form-label">Data de Término</label>
        {{ form.data_fim }}
        {% for error in form.data_fim.errors %}
            <div class="text-danger">{{ error }}</div>
        {% endfor %}
        <small class="form-text text-muted">Opcional. Se não informada, será considerada a mesma data de início.</small>
    </div>
    <div class="mb-3">
        <label for="id_hora_inicio" class="form-label">Hora de Início</label>
        {{ form.hora_inicio }}
        {% for error in form.hora_inicio.errors %}
            <div class="text-danger">{{ error }}</div>
        {% endfor %}
    </div>
    <div class="mb-3">
        <label for="id_hora_fim" class="form-label">Hora de Término</label>
        {{ form.hora_fim }}
        {% for error in form.hora_fim.errors %}
            <div class="text-danger">{{ error }}</div>
        {% endfor %}
        <small class="form-text text-muted">Opcional. Se não informada, será considerada 1 hora após o início.</small>
    </div>
    <div class="mb-3">
        <label for="id_local" class="form-label">Local</label>
        {{ form.local }}
        {% for error in form.local.errors %}
            <div class="text-danger">{{ error }}</div>
        {% endfor %}
    </div>
    <div class="mb-3">
        <label for="id_responsavel" class="form-label">Responsável</label>
        {{ form.responsavel }}
        {% for error in form.responsavel.errors %}
            <div class="text-danger">{{ error }}</div>
        {% endfor %}
    </div>
    <div class="mb-3">
        <label for="id_curso" class="form-label">Curso</label>
        {{ form.curso }}
        {% for error in form.curso.errors %}
            <div class="text-danger">{{ error }}</div>
        {% endfor %}
    </div>
    <div class="mb-3">
        <label for="id_turmas" class="form-label">Turmas</label>
        <div class="d-flex align-items-center mb-2">
            <input type="checkbox" id="select-all-turmas" class="form-check-input me-2">
            <label for="select-all-turmas" class="form-check-label">Selecionar todas as turmas</label>
        </div>
        {{ form.turmas }}
        {% for error in form.turmas.errors %}
            <div class="text-danger">{{ error }}</div>
        {% endfor %}
        <small class="form-text text-muted">Selecione uma ou mais(CTRL) turmas para esta atividade.</small>
    </div>
    <div class="mb-3 form-check">
        {{ form.convocacao }}
        <label class="form-check-label" for="id_convocacao">Convocação</label>
        {% for error in form.convocacao.errors %}
            <div class="text-danger">{{ error }}</div>
        {% endfor %}
    </div>
    <div class="d-flex justify-content-between mb-4">
        <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">
            <i class="fas fa-times"></i> Cancelar
        </a>
        <button type="submit" class="btn btn-primary">
            <i class="fas fa-save"></i> Criar Atividade
        </button>
    </div>
</form>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const cursoSelect = document.getElementById('id_curso');
    const turmasSelect = document.getElementById('id_turmas');
    const selectAllTurmas = document.getElementById('select-all-turmas');
    let noTurmasMsg = document.getElementById('no-turmas-msg');
    if (!noTurmasMsg) {
        noTurmasMsg = document.createElement('div');
        noTurmasMsg.id = 'no-turmas-msg';
        noTurmasMsg.className = 'text-muted mt-2';
        turmasSelect.parentNode.appendChild(noTurmasMsg);
    }

    function atualizarTurmas(cursoId, turmasSelecionadas=[]) {
        if (!cursoId) {
            turmasSelect.innerHTML = '';
            noTurmasMsg.textContent = '';
            return;
        }
        fetch(`/atividades/ajax/turmas-por-curso/?curso=${cursoId}`)
            .then(response => response.json())
            .then(data => {
                turmasSelect.innerHTML = '';
                if (data.turmas.length === 0) {
                    noTurmasMsg.textContent = 'Não há turmas para este curso.';
                } else {
                    noTurmasMsg.textContent = '';
                    data.turmas.forEach(function(turma) {
                        const option = document.createElement('option');
                        option.value = turma.id;
                        option.textContent = turma.nome;
                        if (turmasSelecionadas.includes(String(turma.id))) {
                            option.selected = true;
                        }
                        turmasSelect.appendChild(option);
                    });
                }
            });
    }

    if (cursoSelect) {
        cursoSelect.addEventListener('change', function() {
            atualizarTurmas(this.value);
        });
    }

    if (cursoSelect && turmasSelect) {
        const turmasSelecionadas = Array.from(turmasSelect.selectedOptions).map(opt => opt.value);
        if (cursoSelect.value) {
            atualizarTurmas(cursoSelect.value, turmasSelecionadas);
        } else {
            turmasSelect.innerHTML = '';
            noTurmasMsg.textContent = '';
        }
    }

    if (selectAllTurmas && turmasSelect) {
        selectAllTurmas.addEventListener('change', function() {
            for (let option of turmasSelect.options) {
                option.selected = this.checked;
            }
        });
        turmasSelect.addEventListener('change', function() {
            selectAllTurmas.checked = Array.from(turmasSelect.options).every(opt => opt.selected);
        });
    }
});
</script>

{% comment %}
Returns:
    dict: Dicionário com todos os modelos necessários
Raises:
    ImportError: Se algum módulo não puder ser importado
    AttributeError: Se algum modelo não for encontrado no módulo
"""
try:
    atividades_module = import_module("atividades.models")
    cursos_module = import_module("cursos.models")
    turmas_module = import_module("turmas.models")
    alunos_module = import_module("alunos.models")

    return {
        'AtividadeAcademica': getattr(atividades_module, "AtividadeAcademica"),
        'AtividadeRitualistica': getattr(atividades_module, "AtividadeRitualistica"),
        'Curso': getattr(cursos_module, "Curso"),
        'Turma': getattr(turmas_module, "Turma"),
        'Aluno': getattr(alunos_module, "Aluno"),
    }
except (ImportError, AttributeError) as e:
    logger.error("Erro ao obter modelos: %s", e)
    raise
{% endcomment %}



### Arquivo: atividades\templates\atividades\academicas\importar_atividades_academicas.html

html
<!-- filepath: c:\projetos\omaum\atividades\templates\atividades\importar_atividades_academicas.html -->
{% extends 'base.html' %}
{% block title %}Importar Atividades Acadêmicas{% endblock %}
{% block content %}
<div class="container mt-4">
    <h2>Importar Atividades Acadêmicas (CSV)</h2>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <div class="mb-3">
            <label for="csv_file" class="form-label">Arquivo CSV</label>
            <input type="file" name="csv_file" id="csv_file" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-success">Importar</button>
        <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\academicas\listar_atividades_academicas.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Lista de Atividades Acadêmicas{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Atividades Acadêmicas</h1>
        <div class="d-flex gap-2">
            <!-- 1. Voltar ao Painel de Controle -->
            <a href="{% url 'atividades:dashboard_atividades' %}" class="btn btn-outline-secondary" data-bs-toggle="tooltip" title="Voltar ao Painel de Controle">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <!-- 2. Nova Atividade -->
            <a href="{% url 'atividades:criar_atividade_academica' %}" class="btn btn-success" data-bs-toggle="tooltip" title="Criar nova atividade">
                <i class="fas fa-plus"></i> Nova Atividade
            </a>
            <!-- 3. Relatórios -->
            <a href="{% url 'atividades:relatorio_atividades' %}" class="btn btn-outline-primary" data-bs-toggle="tooltip" title="Relatórios">
                <i class="fas fa-file-alt"></i> Relatórios
            </a>
            <!-- 4. Importar CSV -->
            <a href="{% url 'atividades:importar_atividades_academicas' %}" class="btn btn-outline-success" data-bs-toggle="tooltip" title="Importar atividades via CSV">
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
        <div class="col-md-3">
            <label for="id_q" class="form-label">Busca</label>
            <input type="text" name="q" id="id_q" class="form-control" placeholder="Buscar por nome ou descrição" value="{{ query }}">
        </div>
        <div class="col-md-3">
            <label for="id_curso" class="form-label">Curso</label>
            <select name="curso" id="id_curso" class="form-select">
                <option value="">Todos os cursos</option>
                {% for curso in cursos %}
                    <option value="{{ curso.codigo_curso }}"
                        {% if curso.codigo_curso|stringformat:"s" == curso_selecionado|stringformat:"s" %}selected{% endif %}>
                        {{ curso.codigo_curso }} - {{ curso.nome }}
                    </option>
                {% endfor %}
            </select>
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
        <div class="col-md-3 d-grid gap-2 d-md-flex justify-content-md-end align-items-end">
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

    <!-- Tabela de atividades -->
    <div class="table-responsive">
        <table class="table align-middle table-hover">
            <thead class="table-light">
                <tr>
                    <th>Nome</th>
                    <th>Curso</th>
                    <th>Turmas</th>
                    <th>Tipo</th>
                    <th>Status</th>
                    <th>Data Início</th>
                    <th>Convocação</th>
                    <th class="text-start">Ações</th>
                </tr>
            </thead>
            <tbody>
                {% for atividade in atividades %}
                <tr>
                    <td>{{ atividade.nome }}</td>
                    <td>{{ atividade.curso }}</td>
                    <td>
                        {% for turma in atividade.turmas.all %}
                            <span class="badge bg-info">{{ turma.nome }}</span>
                        {% empty %}
                            <span class="text-muted">-</span>
                        {% endfor %}
                    </td>
                    <td>{{ atividade.get_tipo_atividade_display }}</td>
                    <td>
                        {% if atividade.status == 'CONFIRMADA' %}
                            <span class="badge bg-success">Confirmada</span>
                        {% elif atividade.status == 'PENDENTE' %}
                            <span class="badge bg-warning text-dark">Pendente</span>
                        {% else %}
                            <span class="badge bg-secondary">{{ atividade.get_status_display }}</span>
                        {% endif %}
                    </td>
                    <td>{{ atividade.data_inicio|date:"d/m/Y" }}</td>
                    <td>
                        {% if atividade.convocacao %}
        <span class="badge bg-success">Sim</span>
    {% else %}
        <span class="badge bg-secondary">Não</span>
    {% endif %}
                    </td>
                    <td class="text-start">
                        <div class="btn-group btn-group-sm" role="group">
                            <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-info" title="Detalhar atividade" data-bs-toggle="tooltip">
                                <i class="fas fa-eye"></i>
                            </a>
                            <a href="{% url 'atividades:editar_atividade_academica' atividade.id %}" class="btn btn-warning" title="Editar atividade" data-bs-toggle="tooltip">
                                <i class="fas fa-edit"></i>
                            </a>
                            <a href="{% url 'atividades:excluir_atividade_academica' atividade.id %}" class="btn btn-danger" title="Excluir atividade" data-bs-toggle="tooltip">
                                <i class="fas fa-trash"></i>
                            </a>
                            <a href="{% url 'atividades:copiar_atividade_academica' atividade.id %}" class="btn btn-secondary" title="Copiar atividade" data-bs-toggle="tooltip">
                                <i class="fas fa-copy"></i>
                            </a>
                        </div>
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="8" class="text-center">Nenhuma atividade encontrada.</td>
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
                    <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% if query %}&q={{ query }}{% endif %}{% if curso_selecionado %}&curso={{ curso_selecionado }}{% endif %}{% if turma_selecionada %}&turma={{ turma_selecionada }}{% endif %}">&laquo;</a>
                </li>
            {% else %}
                <li class="page-item disabled"><span class="page-link">&laquo;</span></li>
            {% endif %}
            {% for num in page_obj.paginator.page_range %}
                {% if page_obj.number == num %}
                    <li class="page-item active"><span class="page-link">{{ num }}</span></li>
                {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                    <li class="page-item"><a class="page-link" href="?page={{ num }}{% if query %}&q={{ query }}{% endif %}{% if curso_selecionado %}&curso={{ curso_selecionado }}{% endif %}{% if turma_selecionada %}&turma={{ turma_selecionada }}{% endif %}">{{ num }}</a></li>
                {% endif %}
            {% endfor %}
            {% if page_obj.has_next %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ page_obj.next_page_number }}{% if query %}&q={{ query }}{% endif %}{% if curso_selecionado %}&curso={{ curso_selecionado }}{% endif %}{% if turma_selecionada %}&turma={{ turma_selecionada }}{% endif %}">&raquo;</a>
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
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
</div>
{% endblock %}




### Arquivo: atividades\templates\atividades\academicas\partials\atividades_tabela.html

html
<tbody>
{% for atividade in atividades %}
    <tr>
        <td>{{ atividade.nome }}</td>
        <td>
            {% if atividade.curso %}
                {{ atividade.curso.nome }}
            {% else %}
                <span class="text-muted">-</span>
            {% endif %}
        </td>
        <td>
            {% if atividade.turmas.exists %}
                {% for turma in atividade.turmas.all %}
                    <span class="badge bg-secondary">{{ turma.nome }}</span>
                {% endfor %}
            {% else %}
                <span class="text-muted">Nenhuma</span>
            {% endif %}
        </td>
        <td>
            {{ atividade.get_tipo_atividade_display|default:atividade.get_tipo_display }}
        </td>
        <td>
            {{ atividade.get_status_display|default:atividade.status }}
        </td>
        <td>
            {{ atividade.data_inicio|date:"d/m/Y" }}
        </td>
        <td>
            <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-sm btn-info" title="Detalhes">Detalhes</a>
            <a href="{% url 'atividades:editar_atividade_academica' atividade.id %}" class="btn btn-sm btn-warning" title="Editar">Editar</a>
            <a href="{% url 'atividades:excluir_atividade_academica' atividade.id %}" class="btn btn-sm btn-danger" title="Excluir">Excluir</a>
        </td>
    </tr>
{% empty %}
    <tr>
        <td colspan="7" class="text-center">Nenhuma atividade encontrada.</td>
    </tr>
{% endfor %}
</tbody>




### Arquivo: atividades\templates\atividades\academicas\partials\atividades_tabela_body.html

html
{% if atividades %}
    {% for atividade in atividades %}
        <tr>
            <td>{{ atividade.nome }}</td>
            <td>
                {% if atividade.curso %}
                    {{ atividade.curso.nome }}
                {% else %}
                    <span class="text-muted">-</span>
                {% endif %}
            </td>
            <td>
                {% for turma in atividade.turmas.all %}
                    <span class="badge bg-info">{{ turma.nome }}</span>
                {% empty %}
                    <span class="text-muted">-</span>
                {% endfor %}
            </td>
            <td>
                {{ atividade.get_tipo_atividade_display|default:atividade.tipo_atividade }}
            </td>
            <td>
                {{ atividade.get_status_display|default:atividade.status }}
            </td>
            <td>
                {{ atividade.data_inicio|date:"d/m/Y" }}
            </td>
            <td>
                <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-info btn-sm">Detalhes</a>
                <a href="{% url 'atividades:editar_atividade_academica' atividade.id %}" class="btn btn-warning btn-sm">Editar</a>
                <a href="{% url 'atividades:excluir_atividade_academica' atividade.id %}" class="btn btn-danger btn-sm">Excluir</a>
            </td>
        </tr>
    {% endfor %}
{% else %}
    <tr>
        <td colspan="7" class="text-center">Nenhuma atividade encontrada.</td>
    </tr>
{% endif %}



### Arquivo: atividades\templates\atividades\academicas\partials\cursos_options.html

html
<option value="">Selecione um curso</option>
{% for curso in cursos %}
    <option value="{{ curso.id }}" {% if curso.id|stringformat:"s" == curso_selecionado|stringformat:"s" %}selected{% endif %}>
        {{ curso.codigo_curso }} - {{ curso.nome }}
    </option>
{% endfor %}



### Arquivo: atividades\templates\atividades\academicas\partials\turmas_options.html

html
<option value="">Selecione uma turma</option>
{% for turma in turmas %}
    <option value="{{ turma.id }}" {% if turma.id|stringformat:"s" == turma_selecionada|stringformat:"s" %}selected{% endif %}>
        {{ turma.nome }}
    </option>
{% endfor %}



### Arquivo: atividades\templates\atividades\academicas\relatorio_atividades_academicas.html

html
{% extends 'base.html' %}
{% load static %}
{% block title %}Relatório de Atividades Acadêmicas{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Relatório de Atividades Acadêmicas</h1>
        <a href="{% url 'listar_atividades_academicas' %}" class="btn btn-secondary">Voltar</a>
    </div>
    <form method="get" class="mb-3">
        <select name="curso" class="form-select w-auto d-inline" onchange="this.form.submit()">
            <option value="">Todos os cursos</option>
            {% for curso in cursos %}
                <option value="{{ curso.codigo_curso }}" {% if curso.codigo_curso|stringformat:"s" == curso_id %}selected{% endif %}>
                    {{ curso.nome }}
                </option>
            {% endfor %}
        </select>
    </form>
    {% for curso, atividades_curso in cursos_dict.items %}
        <h3>{{ curso }}</h3>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Turmas</th>
                    <th>Tipo</th>
                    <th>Status</th>
                    <th>Início</th>
                    <th>Término</th>
                </tr>
            </thead>
            <tbody>
                {% for atividade in atividades_curso %}
                <tr>
                    <td>{{ atividade.nome }}</td>
                    <td>
                        {% for turma in atividade.turmas.all %}
                            {{ turma.nome }}{% if not forloop.last %}, {% endif %}
                        {% endfor %}
                    </td>
                    <td>{{ atividade.get_tipo_atividade_display }}</td>
                    <td>{{ atividade.get_status_display }}</td>
                    <td>{{ atividade.data_inicio|date:"d/m/Y H:i" }}</td>
                    <td>{{ atividade.data_fim|date:"d/m/Y H:i" }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% endfor %}
    <div class="d-flex justify-content-end mt-4">
        <a href="{% url 'listar_atividades_academicas' %}" class="btn btn-secondary">Voltar</a>
    </div>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\calendario_atividades.html

html
{% extends 'base.html' %}
{% load static %}
{% block title %}Calendário de Atividades{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Calendário de Atividades</h1>
    <table class="table table-bordered">
        <thead>
            <tr>
                <th>Data</th>
                <th>Nome</th>
                <th>Curso</th>
                <th>Turmas</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {% for atividade in atividades %}
            <tr>
                <td>{{ atividade.data_inicio|date:"d/m/Y" }}</td>
                <td>{{ atividade.nome }}</td>
                <td>{{ atividade.curso }}</td>
                <td>
                    {% for turma in atividade.turmas.all %}
                        {{ turma.nome }}{% if not forloop.last %}, {% endif %}
                    {% endfor %}
                </td>
                <td>{{ atividade.get_status_display }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\dashboard.html

html
{% extends 'base.html' %}
{% load static %}
{% block title %}Dashboard de Atividades{% endblock %}
{% block content %}
<div class="container mt-4">
    <h1>Dashboard de Atividades</h1>
    <form id="filtro-dashboard-form" method="get" class="row g-3 mb-4">
        <div class="col-md-4">
            <label for="curso" class="form-label">Curso</label>
            <select name="curso" id="filtro-curso" class="form-select">
                <option value="">Todos os cursos</option>
                {% for curso in cursos %}
                    <option value="{{ curso.id }}" {% if curso_selecionado == curso.id|stringformat:"s" %}selected{% endif %}>{{ curso.nome }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="col-md-4">
            <label for="turma" class="form-label">Turma</label>
            <select name="turma" id="filtro-turma" class="form-select">
                <option value="">Todas as turmas</option>
                {% for turma in turmas %}
                    <option value="{{ turma.id }}" {% if turma_selecionada == turma.id|stringformat:"s" %}selected{% endif %}>{{ turma.nome }}</option>
                {% endfor %}
            </select>
        </div>
    </form>
    <div id="dashboard-conteudo">
        {# Aqui ficaria o conteúdo do dashboard, como cards, gráficos, tabelas etc. #}
        {# Corrigir eventuais usos de filtro date: #}
        {% if atividades %}
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Curso</th>
                        <th>Turmas</th>
                        <th>Tipo</th>
                        <th>Status</th>
                        <th>Início</th>
                    </tr>
                </thead>
                <tbody>
                    {% for atividade in atividades %}
                    <tr>
                        <td>{{ atividade.nome }}</td>
                        <td>{{ atividade.curso.nome }}</td>
                        <td>
                            {% for turma in atividade.turmas.all %}
                                <span class="badge bg-info">{{ turma.nome }}</span>
                            {% endfor %}
                        </td>
                        <td>{{ atividade.get_tipo_display }}</td>
                        <td>{{ atividade.get_status_display }}</td>
                        <td>
                            {{ atividade.data_inicio|date:"d/m/Y" }}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% endif %}
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/atividades_filtros.js' %}"></script>
{% endblock %}



### Arquivo: atividades\templates\atividades\dashboard_atividades.html

html
{% extends 'base.html' %}
{% load static %}
{% block title %}Dashboard de Atividades{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Dashboard de Atividades</h1>
    <table class="table table-bordered">
        <thead>
            <tr>
                <th>Nome</th>
                <th>Curso</th>
                <th>Turmas</th>
                <th>Status</th>
                <th>In√≠cio</th>
            </tr>
        </thead>
        <tbody>
            {% for atividade in atividades %}
            <tr>
                <td>{{ atividade.nome }}</td>
                <td>{{ atividade.curso }}</td>
                <td>
                    {% for turma in atividade.turmas.all %}
                        {{ turma.nome }}{% if not forloop.last %}, {% endif %}
                    {% endfor %}
                </td>
                <td>{{ atividade.get_status_display }}</td>
                <td>{{ atividade.data_inicio|date:"d/m/Y H:i" }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\importar_atividades.html

html
{% extends 'base.html' %}
{% load static %}
{% block title %}Importar Atividades{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Importar Atividades</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Upload de Arquivo CSV</h5>
        </div>
        <div class="card-body">
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="tipo_atividade" class="form-label">Tipo de Atividade</label>
                    <select class="form-select" id="tipo_atividade" name="tipo_atividade">
                        <option value="academica">Atividade Acadêmica</option>
                        <option value="ritualistica">Atividade Ritualística</option>
                    </select>
                </div>
                
                <div class="mb-3">
                    <label for="csv_file" class="form-label">Arquivo CSV</label>
                    <input type="file" class="form-control" id="csv_file" name="csv_file" accept=".csv" required>
                    <div class="form-text">
                        O arquivo CSV deve conter os seguintes cabeçalhos:
                        <div id="headers_academica">
                            <strong>Para Atividades Acadêmicas:</strong> Nome, Descricao, Data_Inicio, Data_Fim, Responsavel, Local, Tipo, Status, Turmas
                        </div>
                        <div id="headers_ritualistica" style="display: none;">
                            <strong>Para Atividades Ritualísticas:</strong> Nome, Descricao, Data, Hora_Inicio, Hora_Fim, Local, Turma, Participantes
                        </div>
                    </div>
                </div>
                
                <div class="mb-3">
                    <div class="alert alert-info">
                        <h6>Instruções:</h6>
                        <ul>
                            <li>O arquivo deve estar no formato CSV com cabeçalhos.</li>
                            <li>As datas devem estar no formato DD/MM/AAAA.</li>
                            <li>As horas devem estar no formato HH:MM.</li>
                            <li>Para atividades acadêmicas, o campo "Turmas" deve conter IDs de turmas separados por vírgula.</li>
                            <li>Para atividades ritualísticas, o campo "Participantes" deve conter CPFs de alunos separados por vírgula.</li>
                        </ul>
                    </div>
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="javascript:history.back()" class="btn btn-secondary">Cancelar</a>
                    <button type="submit" class="btn btn-primary">Importar</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Exemplos de arquivos CSV -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Exemplos de Formato</h5>
        </div>
        <div class="card-body">
            <div id="exemplo_academica">
                <h6>Exemplo para Atividades Acadêmicas:</h6>
                <pre class="bg-light p-3 rounded">Nome,Descricao,Data_Inicio,Data_Fim,Responsavel,Local,Tipo,Status,Turmas
Aula de Meditação,Aula introdutória sobre técnicas de meditação,01/10/2023 14:00,01/10/2023 16:00,João Silva,Sala 101,aula,agendada,1,2
Workshop de Mantras,Workshop sobre mantras e sua aplicação,05/10/2023 09:00,05/10/2023 12:00,Maria Oliveira,Auditório,workshop,agendada,3</pre>
            </div>
            
            <div id="exemplo_ritualistica" style="display: none;">
                <h6>Exemplo para Atividades Ritualísticas:</h6>
                <pre class="bg-light p-3 rounded">Nome,Descricao,Data,Hora_Inicio,Hora_Fim,Local,Turma,Participantes
Ritual de Lua Cheia,Ritual mensal de lua cheia,15/10/2023,19:00,21:00,Templo Principal,1,12345678901,23456789012
Meditação Coletiva,Meditação coletiva de alinhamento,20/10/2023,18:00,19:30,Sala de Meditação,2,34567890123,45678901234</pre>
            </div>
        </div>
    </div>
</div>

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const tipoAtividadeSelect = document.getElementById('tipo_atividade');
        const headersAcademica = document.getElementById('headers_academica');
        const headersRitualistica = document.getElementById('headers_ritualistica');
        const exemploAcademica = document.getElementById('exemplo_academica');
        const exemploRitualistica = document.getElementById('exemplo_ritualistica');
        
        tipoAtividadeSelect.addEventListener('change', function() {
            if (this.value === 'academica') {
                headersAcademica.style.display = 'block';
                headersRitualistica.style.display = 'none';
                exemploAcademica.style.display = 'block';
                exemploRitualistica.style.display = 'none';
            } else {
                headersAcademica.style.display = 'none';
                headersRitualistica.style.display = 'block';
                exemploAcademica.style.display = 'none';
                exemploRitualistica.style.display = 'block';
            }
        });
    });
</script>
{% endblock %}
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
<form method="get" class="row g-3">
    <div class="col-md-4">
        <input type="text" name="q" class="form-control" placeholder="Buscar por nome ou descrição..." value="{{ query }}">
    </div>
    <div class="col-md-3">
        <select name="codigo_curso" id="id_codigo_curso" class="form-select" aria-label="Selecionar curso">
            <option value="">Todos os cursos</option>
            {% for curso in cursos %}
                <option value="{{ curso.codigo_curso }}" {% if codigo_curso_selecionado == curso.codigo_curso|stringformat:"s" %}selected{% endif %}>
                    {{ curso.nome }}
                </option>
            {% endfor %}
        </select>
    </div>
    <div class="col-md-3">
        <select name="turma" id="id_turma" class="form-select" aria-label="Selecionar turma">
            <option value="">Todas as turmas</option>
            {% for turma in turmas %}
                <option value="{{ turma.id }}" {% if turma_selecionada == turma.id|stringformat:"s" %}selected{% endif %}>
                    {{ turma.nome }}
                </option>
            {% endfor %}
        </select>
    </div>    <div class="col-md-2">
        <button type="submit" class="btn btn-primary w-100">
            <i class="fas fa-search"></i> Filtrar
        </button>
    </div>
</form>
</select>



### Arquivo: atividades\templates\atividades\registrar_frequencia.html

html
{% extends 'base.html' %}
{% load static %}
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



### Arquivo: atividades\templates\atividades\relatorio_atividades_curso_turma.html

html
{% extends 'base.html' %}
{% load static %}
{% block title %}Relatório de Atividades por Curso e Turma{% endblock %}
{% block content %}
<div class="container mt-4">
    <h1>Relatório de Atividades Acadêmicas</h1>
    <form id="filtro-relatorio-form" method="get" class="row g-3 mb-4">
        <div class="col-md-4">
            <label for="curso" class="form-label">Curso</label>
            <select name="curso" id="filtro-curso" class="form-select">
                <option value="">Todos os cursos</option>
                {% for curso in cursos %}
                    <option value="{{ curso.id }}" {% if curso_selecionado == curso.id|stringformat:"s" %}selected{% endif %}>{{ curso.nome }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="col-md-4">
            <label for="turma" class="form-label">Turma</label>
            <select name="turma" id="filtro-turma" class="form-select">
                <option value="">Todas as turmas</option>
                {% for turma in turmas %}
                    <option value="{{ turma.id }}" {% if turma_selecionada == turma.id|stringformat:"s" %}selected{% endif %}>{{ turma.nome }}</option>
                {% endfor %}
            </select>
        </div>
    </form>
    <div class="card">
        <div class="card-body">
            <div id="relatorio-tabela-container">
            {% if atividades %}
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Curso</th>
                            <th>Turmas</th>
                            <th>Nome da Atividade</th>
                            <th>Data</th>
                            <th>Descrição</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for atividade in atividades %}
                        <tr>
                            <td>{{ atividade.curso.nome }}</td>
                            <td>
                                {% for turma in atividade.turmas.all %}
                                    <span class="badge bg-info">{{ turma.nome }}</span>
                                {% endfor %}
                            </td>
                            <td>{{ atividade.nome }}</td>
                            <td>
                                {# CORREÇÃO DO ERRO DE DATA: usar apenas d/m/Y para DateField #}
                                {{ atividade.data|date:"d/m/Y" }}
                            </td>
                            <td>{{ atividade.descricao }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            {% else %}
                <div class="alert alert-warning">
                    Nenhuma atividade acadêmica encontrada para o filtro selecionado.
                </div>
            {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/atividades_filtros.js' %}"></script>
{% endblock %}



### Arquivo: atividades\templates\atividades\ritualisticas\confirmar_copia_ritualistica.html

html
{% extends 'base.html' %}
{% load static %}
{% block title %}Copiar Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Copiar Atividade Ritualística</h1>
    
    <div class="alert alert-info">
        <p>Você está prestes a criar uma cópia da atividade ritualística <strong>"{{ atividade.nome }}"</strong>.</p>
        <p>A nova atividade terá os mesmos dados e participantes da original.</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade Original</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ atividade.nome }}</p>
            <p><strong>Descrição:</strong> {{ atividade.descricao|default:"Não informada" }}</p>
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
            <button type="submit" class="btn btn-primary me-2">Criar Cópia</button>
            <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\ritualisticas\confirmar_exclusao_ritualistica.html

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
        <input type="hidden" name="return_url" value="{{ return_url }}">
        <div class="d-flex">
            <button type="submit" class="btn btn-danger me-2">Sim, excluir</button>
            <a href="{{ return_url }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\ritualisticas\copiar_atividade_ritualistica.html

html
{% extends 'base.html' %}
{% load static %}
{% block title %}Copiar Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Copiar Atividade Ritualística</h1>
        <a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Atividade Original</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Nome:</strong> {{ atividade_original.nome }}</p>
                    <p><strong>Data:</strong> {{ atividade_original.data|date:"d/m/Y" }}</p>
                    <p><strong>Horário:</strong> {{ atividade_original.hora_inicio }} - {{ atividade_original.hora_fim }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Local:</strong> {{ atividade_original.local }}</p>
                    <p><strong>Turma:</strong> {{ atividade_original.turma.nome }}</p>
                    <p><strong>Participantes:</strong> {{ atividade_original.participantes.count }}</p>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <p><strong>Descrição:</strong></p>
                    <p>{{ atividade_original.descricao|default:"Sem descrição"|linebreaks }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações da Nova Atividade</h5>
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
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
                <div class="form-check mt-3">
                    <input class="form-check-input" type="checkbox" id="copiar_participantes" name="copiar_participantes" checked>
                    <label class="form-check-label" for="copiar_participantes">
                        Copiar lista de participantes da atividade original
                    </label>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="javascript:history.back()" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Criar Cópia</button>
        </div>
    </form>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\ritualisticas\criar_atividade_ritualistica.html

html
{% extends 'base.html' %}
{% load static %}
{% block title %}Criar Nova Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Nova Atividade Ritualística</h1>
        <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">{{ message }}</div>
        {% endfor %}
    {% endif %}

    {% if form.non_field_errors %}
        <div class="alert alert-danger">
            {% for error in form.non_field_errors %}
                <div>{{ error }}</div>
            {% endfor %}
        </div>
    {% endif %}

    <div class="row">
        <div class="col-md-8">
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Dados da Atividade</h5>
                </div>
                <div class="card-body">
                    <form method="post" novalidate>
                        {% csrf_token %}
                        {% include 'includes/form_errors.html' %}
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
                        <div class="row">
                            <div class="col-md-6">
                                {% include 'includes/form_field.html' with field=form.turma %}
                            </div>
                            <div class="col-md-6">
                                {% include 'includes/form_field.html' with field=form.todos_alunos %}
                                <small class="form-text text-muted">Marque para incluir todos os alunos da turma.</small>
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
                        <div class="d-flex justify-content-between mt-4">
                            <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-secondary">
                                <i class="fas fa-times"></i> Cancelar
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Cadastrar Atividade
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



'''