'''
# Revisão da Funcionalidade: turmas

## Arquivos forms.py:


### Arquivo: turmas\templates\turmas\detalhar_turma.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Detalhes da Turma: {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Adicionar exibição do campo alerta_mensagem -->
    {% if turma.alerta_mensagem %}
    <div class="alert alert-warning">
        <i class="fas fa-exclamation-triangle"></i> {{ turma.alerta_mensagem }}
    </div>
    {% endif %}

    <!-- Padronizar botões de ação -->
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Detalhes da Turma</h1>
        <div>
            <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary me-2">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'turmas:editar_turma' turma.id %}" class="btn btn-warning me-2">
                <i class="fas fa-edit"></i> Editar
            </a>
            <a href="{% url 'turmas:excluir_turma' turma.id %}" class="btn btn-danger">
                <i class="fas fa-trash"></i> Excluir
            </a>
        </div>
    </div>
    
    {% if tem_pendencia_instrutoria %}
    <div class="alert alert-danger text-center mb-4 blink">
        <h5 class="mb-0"><strong>Pendência na Instrutoria</strong></h5>
    </div>
    {% endif %}
    
    <!-- Card de informações da turma com layout em colunas -->
    <div class="card mb-4 border-primary">
        <div class="card-header bg-primary text-white">
            <h5 class="card-title mb-0">Informações da Turma</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <!-- Coluna 1 -->
                <div class="col-md-4">
                    <div class="mb-3">
                        <h6 class="text-muted">Curso</h6>
                        <p class="fs-5">{{ turma.curso }}</p>
                    </div>
                    <div class="mb-3">
                        <h6 class="text-muted">Status</h6>
                        <p>
                            {% if turma.status == 'A' %}
                                <span class="badge bg-success">{{ turma.get_status_display }}</span>
                            {% elif turma.status == 'I' %}
                                <span class="badge bg-warning">{{ turma.get_status_display }}</span>
                            {% else %}
                                <span class="badge bg-secondary">{{ turma.get_status_display }}</span>
                            {% endif %}
                        </p>
                    </div>
                </div>
                
                <!-- Coluna 2 -->
                <div class="col-md-4">
                    <div class="mb-3">
                        <h6 class="text-muted">Data de Início</h6>
                        <p>{{ turma.data_inicio|date:"d/m/Y" }}</p>
                    </div>
                    <div class="mb-3">
                        <h6 class="text-muted">Data de Término</h6>
                        <p>{{ turma.data_fim|date:"d/m/Y"|default:"Não definida" }}</p>
                    </div>
                    <div class="mb-3">
                        <h6 class="text-muted">Local</h6>
                        <p>{{ turma.local|default:"Não informado" }}</p>
                    </div>
                </div>
                
                <!-- Coluna 3 - Estatísticas -->
                <div class="col-md-4">
                    <div class="card bg-light">
                        <div class="card-body text-center">
                            <h6 class="text-muted">Ocupação</h6>
                            <div class="d-flex justify-content-around mb-2">
                                <div>
                                    <h3 class="mb-0">{{ alunos_matriculados_count }}</h3>
                                    <small class="text-muted">Matriculados</small>
                                </div>
                                <div>
                                    <h3 class="mb-0">{{ turma.vagas }}</h3>
                                    <small class="text-muted">Total</small>
                                </div>
                                <div>
                                    <h3 class="mb-0">{{ vagas_disponiveis }}</h3>
                                    <small class="text-muted">Disponíveis</small>
                                </div>
                            </div>
                            
                            <!-- Barra de progresso -->
                            <div class="progress" style="height: 10px;">
                                <div class="progress-bar bg-primary" role="progressbar"
                                     style="width: {% widthratio alunos_matriculados_count turma.vagas 100 %}%;"
                                     aria-valuenow="{{ alunos_matriculados_count }}"
                                     aria-valuemin="0"
                                     aria-valuemax="{{ turma.vagas }}">
                                </div>
                            </div>
                            <small class="text-muted">{% widthratio alunos_matriculados_count turma.vagas 100 %}% ocupado</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Linha para Dias da Semana e Horário -->
            <div class="row mt-3">
                <div class="col-md-6">
                    <h6 class="text-muted">Dias da Semana</h6>
                    <p>{{ turma.dias_semana|default:"Não informado" }}</p>
                </div>
                <div class="col-md-6">
                    <h6 class="text-muted">Horário</h6>
                    <p>{{ turma.horario|default:"Não informado" }}</p>
                </div>
            </div>
            
            <!-- Descrição em linha separada -->
            {% if turma.descricao %}
            <div class="row mt-3">
                <div class="col-12">
                    <h6 class="text-muted">Descrição</h6>
                    <p>{{ turma.descricao }}</p>
                </div>
            </div>
            {% endif %}
        </div>
    </div>
    
    <!-- Card de instrutores -->
    <div class="card mb-4 border-success">
        <div class="card-header bg-success text-white">
            <h5 class="card-title mb-0">Instrutoria</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <!-- Instrutor Principal -->
                <div class="col-md-4">
                    <div class="card h-100">
                        <div class="card-header bg-light">
                            <h6 class="mb-0">Instrutor Principal</h6>
                        </div>
                        <div class="card-body text-center">
                            {% if turma.instrutor %}
                                <div class="mb-3">
                                    {% if turma.instrutor.foto %}
                                        <img src="{{ turma.instrutor.foto.url }}" alt="Foto de {{ turma.instrutor.nome }}"
                                             class="rounded-circle" style="width: 100px; height: 100px; object-fit: cover;">
                                    {% else %}
                                        <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center mx-auto"
                                             style="width: 100px; height: 100px; font-size: 36px;">
                                            {{ turma.instrutor.nome|first|upper }}
                                        </div>
                                    {% endif %}
                                </div>
                                <h5>{{ turma.instrutor.nome }}</h5>
                                <p class="text-muted">{{ turma.instrutor.numero_iniciatico|default:"" }}</p>
                                <a href="{% url 'alunos:detalhar_aluno' turma.instrutor.cpf %}" class="btn btn-sm btn-primary">
                                    Ver Perfil
                                </a>
                            {% else %}
                                <div class="text-muted py-4">
                                    <i class="fas fa-user-slash fa-3x mb-3"></i>
                                    <p>Nenhum instrutor designado</p>
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
                
                <!-- Instrutor Auxiliar -->
                <div class="col-md-4">
                    <div class="card h-100">
                        <div class="card-header bg-light">
                            <h6 class="mb-0">Instrutor Auxiliar</h6>
                        </div>
                        <div class="card-body text-center">
                            {% if turma.instrutor_auxiliar %}
                                <div class="mb-3">
                                    {% if turma.instrutor_auxiliar.foto %}
                                        <img src="{{ turma.instrutor_auxiliar.foto.url }}" alt="Foto de {{ turma.instrutor_auxiliar.nome }}"
                                             class="rounded-circle" style="width: 100px; height: 100px; object-fit: cover;">
                                    {% else %}
                                        <div class="rounded-circle bg-info text-white d-flex align-items-center justify-content-center mx-auto"
                                             style="width: 100px; height: 100px; font-size: 36px;">
                                            {{ turma.instrutor_auxiliar.nome|first|upper }}
                                        </div>
                                    {% endif %}
                                </div>
                                <h5>{{ turma.instrutor_auxiliar.nome }}</h5>
                                <p class="text-muted">{{ turma.instrutor_auxiliar.numero_iniciatico|default:"" }}</p>
                                <a href="{% url 'alunos:detalhar_aluno' turma.instrutor_auxiliar.cpf %}" class="btn btn-sm btn-info">
                                    Ver Perfil
                                </a>
                            {% else %}
                                <div class="text-muted py-4">
                                    <i class="fas fa-user-slash fa-3x mb-3"></i>
                                    <p>Nenhum instrutor designado</p>
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
                
                <!-- Auxiliar de Instrução -->
                <div class="col-md-4">
                    <div class="card h-100">
                        <div class="card-header bg-light">
                            <h6 class="mb-0">Auxiliar de Instrução</h6>
                        </div>
                        <div class="card-body text-center">
                            {% if turma.auxiliar_instrucao %}
                                <div class="mb-3">
                                    {% if turma.auxiliar_instrucao.foto %}
                                        <img src="{{ turma.auxiliar_instrucao.foto.url }}" alt="Foto de {{ turma.auxiliar_instrucao.nome }}"
                                             class="rounded-circle" style="width: 100px; height: 100px; object-fit: cover;">
                                    {% else %}
                                        <div class="rounded-circle bg-success text-white d-flex align-items-center justify-content-center mx-auto"
                                             style="width: 100px; height: 100px; font-size: 36px;">
                                            {{ turma.auxiliar_instrucao.nome|first|upper }}
                                        </div>
                                    {% endif %}
                                </div>
                                <h5>{{ turma.auxiliar_instrucao.nome }}</h5>
                                <p class="text-muted">{{ turma.auxiliar_instrucao.numero_iniciatico|default:"" }}</p>
                                <a href="{% url 'alunos:detalhar_aluno' turma.auxiliar_instrucao.cpf %}" class="btn btn-sm btn-success">
                                    Ver Perfil
                                </a>
                            {% else %}
                                <div class="text-muted py-4">
                                    <i class="fas fa-user-slash fa-3x mb-3"></i>
                                    <p>Nenhum auxiliar designado</p>
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Card de alunos matriculados -->
    <div class="card mb-4 border-primary">
        <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Alunos Matriculados</h5>
            <a href="{% url 'turmas:matricular_aluno' turma.id %}" class="btn btn-light">
                <i class="fas fa-user-plus"></i> Matricular Aluno
            </a>
        </div>
        <div class="card-body">
            {% if matriculas %}
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead class="table-light">
                            <tr>
                                <th>Nome</th>
                                <th>CPF</th>
                                <th>Nº Iniciático</th>
                                <th class="text-end">Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for matricula in matriculas %}
                            <tr>
                                <td>
                                    <div class="d-flex align-items-center">
                                        <div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center me-2"
                                             style="width: 32px; height: 32px; font-size: 14px;">
                                            {{ matricula.aluno.nome|first|upper }}
                                        </div>
                                        {{ matricula.aluno.nome }}
                                    </div>
                                </td>
                                <td>{{ matricula.aluno.cpf }}</td>
                                <td>{{ matricula.aluno.numero_iniciatico|default:"N/A" }}</td>
                                <td class="text-end">
                                    <a href="{% url 'alunos:detalhar_aluno' matricula.aluno.cpf %}" class="btn btn-sm btn-info">
                                        <i class="fas fa-eye"></i> Ver
                                    </a>
                                    <a href="{% url 'matriculas:cancelar_matricula_por_turma_aluno' turma.id matricula.aluno.cpf %}"
                                       class="btn btn-sm btn-danger"
                                       onclick="return confirm('Tem certeza que deseja cancelar esta matrícula?');">
                                        <i class="fas fa-times"></i> Cancelar
                                    </a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i> Nenhum aluno matriculado nesta turma.
                </div>
                <a href="{% url 'turmas:matricular_aluno' turma.id %}" class="btn btn-primary">
                    <i class="fas fa-user-plus"></i> Matricular Primeiro Aluno
                </a>
            {% endif %}
        </div>
        {% if matriculas %}
        <div class="card-footer">
            <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary me-2">
                <i class="fas fa-list"></i> Voltar para a lista
            </a>
            <a href="{% url 'turmas:editar_turma' turma.id %}" class="btn btn-warning me-2">
                <i class="fas fa-edit"></i> Editar
            </a>
            <a href="{% url 'turmas:excluir_turma' turma.id %}" class="btn btn-danger">
                <i class="fas fa-trash"></i> Excluir
            </a>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}

{% block extra_css %}
<style>
    .bg-gradient-primary {
        background: linear-gradient(to right, #0d6efd, #0a58ca);
    }
    .bg-primary.bg-opacity-10 {
        background-color: rgba(13, 110, 253, 0.1) !important;
    }
    .bg-success.bg-opacity-10 {
        background-color: rgba(25, 135, 84, 0.1) !important;
    }
    .bg-info.bg-opacity-10 {
        background-color: rgba(13, 202, 240, 0.1) !important;
    }
    .rounded-circle {
        border-radius: 50% !important;
    }
    .progress {
        overflow: hidden;
        background-color: #e9ecef;
    }
    .card {
        transition: all 0.3s ease;
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 .5rem 1rem rgba(0,0,0,.15) !important;
    }
    .blink {
        animation: blinker 1s linear infinite;
    }
    @keyframes blinker {
        50% { opacity: 0.5; }
    }
</style>
{% endblock %}

{% block extra_js %}
<script>
    // Adicione aqui qualquer JavaScript específico para esta página
</script>
{% endblock %}




### Arquivo: turmas\templates\turmas\editar_turma.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Editar Turma{% endblock %}

{% block extra_css %}
<style>
    /* Ocultar os selects originais */
    #id_instrutor, #id_instrutor_auxiliar, #id_auxiliar_instrucao {
        display: none;
    }
    
    /* Estilo para os resultados da busca */
    .list-group-item-action {
        cursor: pointer;
    }
    
    /* Estilo para o contêiner de instrutor selecionado */
    .selected-instrutor {
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
</style>
{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Editar Turma: {{ turma.nome }}</h1>
        <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Voltar para a lista</a>
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
        
        <!-- Seção de Informações Básicas -->
        <div class="card mb-4">
            <div class="card-header bg-primary text-white">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.curso %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.vagas %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.status %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.dias_semana %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.data_inicio %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.data_fim %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.horario %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Seção de Instrutores -->
        <div class="card mb-4">
            <div class="card-header bg-success text-white">
                <h5>Instrutores</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <!-- Instrutor Principal -->
                    <div class="col-md-4 mb-3">
                        <label for="search-instrutor" class="form-label">Instrutor Principal</label>
                        <input type="text" id="search-instrutor" class="form-control" placeholder="Digite parte do CPF, nome ou número iniciático..." autocomplete="off">
                        <div id="search-results-instrutor" class="list-group mt-2" style="display: none"></div>
                        <div id="selected-instrutor-container" class="p-3 border rounded mt-2 d-none">
                            <div id="selected-instrutor-info">
                                Nenhum instrutor selecionado
                            </div>
                        </div>
                        <div id="instrutor-error" class="alert alert-warning mt-2 d-none"></div>
                        <!-- Campo original oculto via CSS -->
                        {{ form.instrutor }}
                    </div>
                    
                    <!-- Instrutor Auxiliar -->
                    <div class="col-md-4 mb-3">
                        <label for="search-instrutor-auxiliar" class="form-label">Instrutor Auxiliar</label>
                        <input type="text" id="search-instrutor-auxiliar" class="form-control" placeholder="Digite parte do CPF, nome ou número iniciático..." autocomplete="off">
                        <div id="search-results-instrutor-auxiliar" class="list-group mt-2" style="display: none;"></div>
                        <div id="selected-instrutor-auxiliar-container" class="p-3 border rounded mt-2 d-none">
                            <div id="selected-instrutor-auxiliar-info">
                                Nenhum instrutor auxiliar selecionado
                            </div>
                        </div>
                        <div id="instrutor-auxiliar-error" class="alert alert-warning mt-2 d-none"></div>
                        <!-- Campo original oculto via CSS -->
                        {{ form.instrutor_auxiliar }}
                    </div>
                    
                    <!-- Auxiliar de Instrução -->
                    <div class="col-md-4 mb-3">
                        <label for="search-auxiliar-instrucao" class="form-label">Auxiliar de Instrução</label>
                        <input type="text" id="search-auxiliar-instrucao" class="form-control" placeholder="Digite parte do CPF, nome ou número iniciático..." autocomplete="off">
                        <div id="search-results-auxiliar-instrucao" class="list-group mt-2" style="display: none;"></div>
                        <div id="selected-auxiliar-instrucao-container" class="p-3 border rounded mt-2 d-none">
                            <div id="selected-auxiliar-instrucao-info">
                                Nenhum auxiliar de instrução selecionado
                            </div>
                        </div>
                        <div id="auxiliar-instrucao-error" class="alert alert-warning mt-2 d-none"></div>
                        <!-- Campo original oculto via CSS -->
                        {{ form.auxiliar_instrucao }}
                    </div>
                </div>
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> Você pode selecionar qualquer aluno como instrutor.
                    O sistema verificará a elegibilidade e mostrará um aviso caso o aluno não atenda aos requisitos.
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Atualizar Turma</button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/instrutor_search.js' %}"></script>
{% endblock %}




### Arquivo: turmas\templates\turmas\excluir_turma.html

html
{% extends 'base.html' %}

{% block title %}Excluir Turma: {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Turma: {{ turma.nome }}</h1>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    <div class="alert alert-danger">
        <p>Você tem certeza que deseja excluir esta turma?</p>
        <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
    </div>

    <!-- Padronizar botões de confirmação -->
    <form method="post">
        {% csrf_token %}
        <div class="d-flex justify-content-between">
            <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">
                <i class="fas fa-times"></i> Cancelar
            </a>
            <button type="submit" class="btn btn-danger">
                <i class="fas fa-trash"></i> Confirmar Exclusão
            </button>
        </div>
    </form>
</div>
{% endblock %}





### Arquivo: turmas\templates\turmas\formulario_instrutoria.html

html
<div class="card mb-4">
    <div class="card-header bg-success text-white">
        <h5 class="mb-0">Instrutoria</h5>
    </div>
    <div class="card-body">
        <div class="row">
            <!-- Instrutor Principal -->
            <div class="col-md-4 mb-3">
                <label for="search-instrutor" class="form-label">Instrutor Principal</label>
                <input type="text" id="search-instrutor" class="form-control" 
                       placeholder="Digite parte do CPF, nome ou número iniciático..." 
                       autocomplete="off"
                       value="{{ turma.instrutor.nome|default:'' }}">
                <div id="search-results-instrutor" class="list-group mt-2" style="display: none;"></div>
                <div id="selected-instrutor-container" class="p-3 border rounded mt-2 {% if not turma.instrutor %}d-none{% endif %}">
                    <div id="selected-instrutor-info">
                        {% if turma.instrutor %}
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <strong>{{ turma.instrutor.nome }}</strong><br>
                                    CPF: {{ turma.instrutor.cpf }}<br>
                                    {% if turma.instrutor.numero_iniciatico %}
                                        Número Iniciático: {{ turma.instrutor.numero_iniciatico }}
                                    {% endif %}
                                </div>
                                <button type="button" class="btn btn-sm btn-outline-danger" id="remove-id_instrutor">
                                    <i class="fas fa-times"></i> Remover
                                </button>
                            </div>
                        {% else %}
                            Nenhum instrutor selecionado
                        {% endif %}
                    </div>
                </div>
                <div class="alert alert-danger mt-2 d-none"></div>
                <select name="instrutor" class="form-control d-none" id="id_instrutor">
                    <option value="">---------</option>
                    {% if turma.instrutor %}
                        <option value="{{ turma.instrutor.cpf }}" selected>{{ turma.instrutor.nome }}</option>
                    {% endif %}
                </select>
            </div>
            
            <!-- Instrutor Auxiliar -->
            <div class="col-md-4 mb-3">
                <label for="search-instrutor-auxiliar" class="form-label">Instrutor Auxiliar</label>
                <input type="text" id="search-instrutor-auxiliar" class="form-control" 
                       placeholder="Digite parte do CPF, nome ou número iniciático..." 
                       autocomplete="off"
                       value="{{ turma.instrutor_auxiliar.nome|default:'' }}">
                <div id="search-results-instrutor-auxiliar" class="list-group mt-2" style="display: none;"></div>
                <div id="selected-instrutor-auxiliar-container" class="p-3 border rounded mt-2 {% if not turma.instrutor_auxiliar %}d-none{% endif %}">
                    <div id="selected-instrutor-auxiliar-info">
                        {% if turma.instrutor_auxiliar %}
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <strong>{{ turma.instrutor_auxiliar.nome }}</strong><br>
                                    CPF: {{ turma.instrutor_auxiliar.cpf }}<br>
                                    {% if turma.instrutor_auxiliar.numero_iniciatico %}
                                        Número Iniciático: {{ turma.instrutor_auxiliar.numero_iniciatico }}
                                    {% endif %}
                                </div>
                                <button type="button" class="btn btn-sm btn-outline-danger" id="remove-id_instrutor_auxiliar">
                                    <i class="fas fa-times"></i> Remover
                                </button>
                            </div>
                        {% else %}
                            Nenhum instrutor auxiliar selecionado
                        {% endif %}
                    </div>
                </div>
                <div class="alert alert-danger mt-2 d-none"></div>
                <select name="instrutor_auxiliar" class="form-control d-none" id="id_instrutor_auxiliar">
                    <option value="">---------</option>
                    {% if turma.instrutor_auxiliar %}
                        <option value="{{ turma.instrutor_auxiliar.cpf }}" selected>{{ turma.instrutor_auxiliar.nome }}</option>
                    {% endif %}
                </select>
            </div>
            
            <!-- Auxiliar de Instrução -->
            <div class="col-md-4 mb-3">
                <label for="search-auxiliar-instrucao" class="form-label">Auxiliar de Instrução</label>
                <input type="text" id="search-auxiliar-instrucao" class="form-control" 
                       placeholder="Digite parte do CPF, nome ou número iniciático..." 
                       autocomplete="off"
                       value="{{ turma.auxiliar_instrucao.nome|default:'' }}">
                <div id="search-results-auxiliar-instrucao" class="list-group mt-2" style="display: none;"></div>
                <div id="selected-auxiliar-instrucao-container" class="p-3 border rounded mt-2 {% if not turma.auxiliar_instrucao %}d-none{% endif %}">
                    <div id="selected-auxiliar-instrucao-info">
                        {% if turma.auxiliar_instrucao %}
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <strong>{{ turma.auxiliar_instrucao.nome }}</strong><br>
                                    CPF: {{ turma.auxiliar_instrucao.cpf }}<br>
                                    {% if turma.auxiliar_instrucao.numero_iniciatico %}
                                        Número Iniciático: {{ turma.auxiliar_instrucao.numero_iniciatico }}
                                    {% endif %}
                                </div>
                                <button type="button" class="btn btn-sm btn-outline-danger" id="remove-id_auxiliar_instrucao">
                                    <i class="fas fa-times"></i> Remover
                                </button>
                            </div>
                        {% else %}
                            Nenhum auxiliar de instrução selecionado
                        {% endif %}
                    </div>
                </div>
                <div class="alert alert-danger mt-2 d-none"></div>
                <select name="auxiliar_instrucao" class="form-control d-none" id="id_auxiliar_instrucao">
                    <option value="">---------</option>
                    {% if turma.auxiliar_instrucao %}
                        <option value="{{ turma.auxiliar_instrucao.cpf }}" selected>{{ turma.auxiliar_instrucao.nome }}</option>
                    {% endif %}
                </select>
            </div>
        </div>
    </div>
</div>



### Arquivo: turmas\templates\turmas\formulario_turma.html

html
<!-- Padronizar botões no formulário -->
<div class="d-flex justify-content-between mb-5">
    <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">
        <i class="fas fa-times"></i> Cancelar
    </a>
    <button type="submit" class="btn btn-primary">
        <i class="fas fa-save"></i> {% if turma.id %}Atualizar{% else %}Criar{% endif %} Turma
    </button>
</div>



### Arquivo: turmas\templates\turmas\importar_turmas.html

html
{% extends 'base.html' %}

{% block title %}Importar Turmas{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Importar Turmas</h1>
    
    <div class="card">
        <div class="card-body">
            <p class="mb-3">Faça upload de um arquivo CSV contendo os dados das turmas.</p>
            
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                <div class="mb-3">
                    <label for="csv_file" class="form-label">Arquivo CSV</label>
                    <input type="file" name="csv_file" id="csv_file" class="form-control" accept=".csv" required>
                    <div class="form-text">O arquivo deve ter cabeçalhos: Nome, Curso, Vagas, Status, etc.</div>
                </div>
                
                <div class="d-flex">
                    <button type="submit" class="btn btn-primary me-2">Importar</button>
                    <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
    
    <div class="mt-3">
        <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-link">Voltar para a lista de turmas</a>
    </div>
</div>
{% endblock %}



### Arquivo: turmas\templates\turmas\listar_alunos_matriculados.html

html
{% extends 'base.html' %}

{% block title %}Alunos Matriculados - {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Alunos Matriculados - {{ turma.nome }}</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary me-2">Detalhes da Turma</a>
            <a href="{% url 'turmas:matricular_aluno' turma.id %}" class="btn btn-primary">Adicionar Aluno</a>        </div>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card">
        <div class="card-header bg-light">
            <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Total de Alunos: {{ total_alunos }}</h5>
                <div>
                    <form method="get" class="d-flex">
                        <input type="text" name="q" class="form-control me-2" placeholder="Buscar aluno..." value="{{ query }}">
                        <button type="submit" class="btn btn-outline-primary">Buscar</button>
                    </form>
                </div>
            </div>
        </div>
        <div class="card-body">
            {% if alunos %}
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead class="table-light">
                            <tr>
                                <th>Nome</th>
                                <th>CPF</th>
                                <th>Email</th>
                                <th>Data de Matrícula</th>
                                <th>Status</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for matricula in matriculas %}
                                <tr>
                                    <td>
                                        <div class="d-flex align-items-center">
                                            {% if matricula.aluno.foto %}
                                                <img src="{{ matricula.aluno.foto.url }}" alt="Foto de {{ matricula.aluno.nome }}" 
                                                     class="rounded-circle me-2" width="40" height="40" 
                                                     style="object-fit: cover;">
                                            {% else %}
                                                <div class="rounded-circle bg-secondary me-2 d-flex align-items-center justify-content-center" 
                                                     style="width: 40px; height: 40px; color: white;">
                                                    {{ matricula.aluno.nome|first|upper }}
                                                </div>
                                            {% endif %}
                                            {{ matricula.aluno.nome }}
                                        </div>
                                    </td>
                                    <td>{{ matricula.aluno.cpf }}</td>
                                    <td>{{ matricula.aluno.email }}</td>
                                    <td>{{ matricula.data_matricula|date:"d/m/Y" }}</td>
                                    <td>
                                        {% if matricula.status == 'A' %}
                                            <span class="badge bg-success">Ativa</span>
                                        {% elif matricula.status == 'C' %}
                                            <span class="badge bg-danger">Cancelada</span>
                                        {% elif matricula.status == 'F' %}
                                            <span class="badge bg-info">Finalizada</span>
                                        {% else %}
                                            <span class="badge bg-secondary">{{ matricula.get_status_display }}</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        <a href="{% url 'alunos:detalhar_aluno' matricula.aluno.cpf %}" class="btn btn-sm btn-info">Detalhes</a>
                                        <a href="{% url 'turmas:remover_aluno_turma' turma.id matricula.aluno.cpf %}" class="btn btn-sm btn-danger">Remover</a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                
                {% if page_obj.has_other_pages %}
                    <nav aria-label="Paginação">
                        <ul class="pagination justify-content-center mt-3">
                            {% if page_obj.has_previous %}
                                <li class="page-item">
                                    <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% if query %}&q={{ query }}{% endif %}">Anterior</a>
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
                                        <a class="page-link" href="?page={{ num }}{% if query %}&q={{ query }}{% endif %}">{{ num }}</a>
                                    </li>
                                {% endif %}
                            {% endfor %}

                            {% if page_obj.has_next %}
                                <li class="page-item">
                                    <a class="page-link" href="?page={{ page_obj.next_page_number }}{% if query %}&q={{ query }}{% endif %}">Próxima</a>
                                </li>
                            {% else %}
                                <li class="page-item disabled">
                                    <span class="page-link">Próxima</span>
                                </li>
                            {% endif %}
                        </ul>
                    </nav>
                {% endif %}
            {% else %}
                <div class="alert alert-info text-center">
                    <p class="mb-0">Nenhum aluno matriculado nesta turma.</p>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: turmas\templates\turmas\listar_turmas.html

html
{% extends 'base.html' %}

{% block title %}Lista de Turmas{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Padronizar cabeçalho com botões -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Lista de Turmas</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'turmas:criar_turma' %}" class="btn btn-primary me-2">
                <i class="fas fa-plus"></i> Nova Turma
            </a>
            <a href="{% url 'turmas:exportar_turmas' %}" class="btn btn-success me-2">
                <i class="fas fa-file-export"></i> Exportar CSV
            </a>
            <a href="{% url 'turmas:importar_turmas' %}" class="btn btn-info">
                <i class="fas fa-file-import"></i> Importar CSV
            </a>
        </div>
    </div>
    
    <!-- Barra de busca e filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <form method="get" class="row g-3">
                <div class="col-md-6">
                    <input type="text" name="q" class="form-control" placeholder="Buscar por nome..." value="{{ query }}">
                </div>
                <div class="col-md-4">
                    <select name="curso" class="form-select">
                        <option value="">Todos os cursos</option>
                        {% for curso in cursos %}
                            <option value="{{ curso.codigo_curso }}" {% if curso.codigo_curso|stringformat:"s" == curso_selecionado %}selected{% endif %}>{{ curso.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn btn-primary w-100">
                        <i class="fas fa-search"></i> Filtrar
                    </button>
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
                            <th>Curso</th>
                            <th>Nome da Turma</th>
                            <th>Instrutor</th>
                            <th>Status</th>
                            <th>Data Início</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for turma in turmas %}
                            <tr>
                                <td>{{ turma.curso.nome }}</td>
                                <td>{{ turma.nome }}</td>
                                <td>{{ turma.instrutor.nome|default:"Não definido" }}</td>
                                <td>
                                    <span class="badge {% if turma.status == 'A' %}bg-success{% elif turma.status == 'P' %}bg-info{% elif turma.status == 'C' %}bg-secondary{% else %}bg-danger{% endif %}">
                                        {{ turma.get_status_display }}
                                    </span>
                                </td>
                                <td>{{ turma.data_inicio|date:"d/m/Y"|default:"-" }}</td>
                                <td>
                                    <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-sm btn-info" title="Ver detalhes completos da turma">Detalhes</a>
                                    <a href="{% url 'turmas:editar_turma' turma.id %}" class="btn btn-sm btn-warning" title="Editar informações da turma">Editar</a>
                                    <a href="{% url 'turmas:excluir_turma' turma.id %}" class="btn btn-sm btn-danger" title="Excluir esta turma">Excluir</a>
                                </td>
                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="6" class="text-center">
                                    <p class="my-3">Nenhuma turma cadastrada.</p>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer">
            <p class="text-muted mb-0">Total: {{ total_turmas|default:"0" }} turma(s)</p>
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
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: turmas\templates\turmas\matricular_aluno.html

html
{% extends 'base.html' %}

{% block title %}Matricular Aluno na Turma{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Matricular Aluno na Turma: {{ turma.nome }}</h1>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Turma</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ turma.nome }}</p>
            <p><strong>Curso:</strong> {{ turma.curso.nome }}</p>
            <p><strong>Vagas Disponíveis:</strong> {{ turma.vagas_disponiveis }}</p>
        </div>
    </div>
    
    <form method="post" id="matricula-form">
        {% csrf_token %}
        <div class="mb-3">
            <label for="aluno-search" class="form-label">Buscar Aluno</label>
            <div class="input-group">
                <input type="text" class="form-control" id="aluno-search" placeholder="Digite o nome, CPF ou número iniciático do aluno...">
                <button class="btn btn-outline-secondary" type="button" id="limpar-aluno">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div id="aluno-results" class="list-group mt-2 d-none"></div>
            <div id="aluno-selected" class="mt-2 d-none">
                <div class="card">
                    <div class="card-body d-flex align-items-center">
                        <div id="aluno-avatar" class="me-3">
                            <!-- Avatar do aluno será inserido aqui -->
                        </div>
                        <div>
                            <h5 id="aluno-nome" class="mb-1"></h5>
                            <p id="aluno-info" class="mb-0 text-muted"></p>
                        </div>
                    </div>
                </div>
            </div>
            <input type="hidden" name="aluno" id="aluno-id" required>
        </div>
        
        <div class="d-flex justify-content-between">
            <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Matricular Aluno</button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const alunoSearch = document.getElementById('aluno-search');
        const alunoResults = document.getElementById('aluno-results');
        const alunoSelected = document.getElementById('aluno-selected');
        const alunoId = document.getElementById('aluno-id');
        const alunoNome = document.getElementById('aluno-nome');
        const alunoInfo = document.getElementById('aluno-info');
        const alunoAvatar = document.getElementById('aluno-avatar');
        const limparAluno = document.getElementById('limpar-aluno');
        const form = document.getElementById('matricula-form');
        
        let searchTimeout;
        
        // Função para buscar alunos
        function buscarAlunos(query) {
            if (query.length < 2) {
                alunoResults.classList.add('d-none');
                return;
            }
            
            fetch(`/alunos/search/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    alunoResults.innerHTML = '';
                    
                    if (data.length === 0) {
                        const noResult = document.createElement('div');
                        noResult.className = 'list-group-item';
                        noResult.textContent = 'Nenhum aluno encontrado';
                        alunoResults.appendChild(noResult);
                    } else {
                        data.forEach(aluno => {
                            const item = document.createElement('a');
                            item.href = '#';
                            item.className = 'list-group-item list-group-item-action';
                            item.dataset.id = aluno.cpf;
                            item.dataset.nome = aluno.nome;
                            item.dataset.numero = aluno.numero_iniciatico;
                            item.dataset.foto = aluno.foto || '';
                            
                            // Criar conteúdo do item
                            let avatarHtml = '';
                            if (aluno.foto) {
                                avatarHtml = `<img src="${aluno.foto}" alt="${aluno.nome}" class="rounded-circle me-2" width="32" height="32">`;
                            } else {
                                avatarHtml = `<div class="rounded-circle bg-secondary text-white d-inline-flex align-items-center justify-content-center me-2" style="width: 32px; height: 32px;">${aluno.nome.charAt(0)}</div>`;
                            }
                            
                            item.innerHTML = `
                                ${avatarHtml}
                                <div>
                                    <div class="fw-bold">${aluno.nome}</div>
                                    <small class="text-muted">CPF: ${aluno.cpf} | Nº Iniciático: ${aluno.numero_iniciatico || 'N/A'}</small>
                                </div>
                            `;
                            
                            item.addEventListener('click', function(e) {
                                e.preventDefault();
                                selecionarAluno(this.dataset);
                            });
                            
                            alunoResults.appendChild(item);
                        });
                    }
                    
                    alunoResults.classList.remove('d-none');
                })
                .catch(error => {
                    console.error('Erro ao buscar alunos:', error);
                });
        }
        
        // Função para selecionar um aluno
        function selecionarAluno(dados) {
            alunoId.value = dados.id;
            alunoNome.textContent = dados.nome;
            alunoInfo.textContent = `CPF: ${dados.id} | Nº Iniciático: ${dados.numero || 'N/A'}`;
            
            // Configurar avatar
            if (dados.foto) {
                alunoAvatar.innerHTML = `<img src="${dados.foto}" alt="${dados.nome}" class="rounded-circle" width="48" height="48">`;
            } else {
                alunoAvatar.innerHTML = `<div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center" style="width: 48px; height: 48px; font-size: 20px;">${dados.nome.charAt(0)}</div>`;
            }
            
            // Mostrar seleção e esconder resultados
            alunoSelected.classList.remove('d-none');
            alunoResults.classList.add('d-none');
            alunoSearch.value = '';
        }
        
        // Função para limpar seleção
        function limparSelecao() {
            alunoId.value = '';
            alunoSelected.classList.add('d-none');
            alunoSearch.value = '';
            alunoResults.classList.add('d-none');
        }
        
        // Event listeners
        alunoSearch.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                buscarAlunos(this.value);
            }, 300);
        });
        
        limparAluno.addEventListener('click', limparSelecao);
        
        // Fechar resultados ao clicar fora
        document.addEventListener('click', function(e) {
            if (!alunoSearch.contains(e.target) && !alunoResults.contains(e.target)) {
                alunoResults.classList.add('d-none');
            }
        });
        
        // Validar formulário antes de enviar
        form.addEventListener('submit', function(e) {
            if (!alunoId.value) {
                e.preventDefault();
                alert('Por favor, selecione um aluno para matricular.');
            }
        });
    });
</script>
{% endblock %}




### Arquivo: turmas\templates\turmas\registrar_frequencia_turma.html

html
{% extends 'base.html' %}

{% block title %}Registrar Frequência - {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Registrar Frequência</h1>
        <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Voltar para Turma</a>
    </div>
    
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">{{ turma.nome }} - {{ turma.curso.nome }}</h5>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="data_atividade" class="form-label">Data da Atividade</label>
                    <input type="date" class="form-control" id="data_atividade" name="data_atividade" required>
                </div>
                
                <div class="mb-3">
                    <label for="atividade" class="form-label">Atividade</label>
                    <select class="form-select" id="atividade" name="atividade" required>
                        <option value="">Selecione uma atividade</option>
                        {% for atividade in atividades %}
                            <option value="{{ atividade.id }}">{{ atividade.nome }} - {{ atividade.data_inicio|date:"d/m/Y" }}</option>
                        {% endfor %}
                    </select>
                </div>
                
                <h5 class="mt-4 mb-3">Lista de Alunos</h5>
                
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Aluno</th>
                                <th>Presente</th>
                                <th>Justificativa (se ausente)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for aluno in alunos %}
                                <tr>
                                    <td>{{ aluno.nome }}</td>
                                    <td>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" name="presentes" value="{{ aluno.cpf }}" id="presente_{{ aluno.cpf }}" checked>
                                            <label class="form-check-label" for="presente_{{ aluno.cpf }}">
                                                Presente
                                            </label>
                                        </div>
                                    </td>
                                    <td>
                                        <textarea class="form-control" name="justificativa_{{ aluno.cpf }}" rows="1" placeholder="Justificativa para ausência"></textarea>
                                    </td>
                                </tr>
                            {% empty %}
                                <tr>
                                    <td colspan="3" class="text-center">Nenhum aluno matriculado nesta turma.</td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                
                <div class="mt-4">
                    <button type="submit" class="btn btn-primary">Registrar Frequência</button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: turmas\templates\turmas\relatorio_frequencia_turma.html

html
{% extends 'base.html' %}

{% block title %}Relatório de Frequência - {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Relatório de Frequência</h1>
        <div>
            <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary me-2">Voltar para Turma</a>
            <button onclick="window.print()" class="btn btn-primary">
                <i class="fas fa-print"></i> Imprimir Relatório
            </button>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">{{ turma.nome }} - {{ turma.curso.nome }}</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Instrutor:</strong> {{ turma.instrutor.nome|default:"Não definido" }}</p>
                    <p><strong>Instrutor Auxiliar:</strong> {{ turma.instrutor_auxiliar.nome|default:"Não definido" }}</p>
                    <p><strong>Auxiliar de Instrução:</strong> {{ turma.auxiliar_instrucao.nome|default:"Não definido" }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Data de Início:</strong> {{ turma.data_inicio|date:"d/m/Y" }}</p>
                    <p><strong>Data de Término:</strong> {{ turma.data_fim|date:"d/m/Y"|default:"Não definida" }}</p>
                    <p><strong>Total de Alunos:</strong> {{ alunos|length }}</p>
                </div>
            </div>
        </div>
    </div>
    
    {% if dados_frequencia %}
        <div class="card mb-4">
            <div class="card-header">
                <h5 class="mb-0">Resumo de Frequência</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Aluno</th>
                                <th>Presenças</th>
                                <th>Total de Atividades</th>
                                <th>Percentual</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for dado in dados_frequencia %}
                                <tr>
                                    <td>{{ dado.aluno.nome }}</td>
                                    <td>{{ dado.total_presencas }}</td>
                                    <td>{{ dado.total_atividades }}</td>
                                    <td>{{ dado.percentual_presenca|floatformat:1 }}%</td>
                                    <td>
                                        {% if dado.percentual_presenca >= 75 %}
                                            <span class="badge bg-success">Aprovado</span>
                                        {% else %}
                                            <span class="badge bg-danger">Reprovado</span>
                                        {% endif %}
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5 class="mb-0">Detalhamento por Atividade</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped table-bordered">
                        <thead>
                            <tr>
                                <th>Aluno</th>
                                {% for data in datas_atividades %}
                                    <th>{{ data|date:"d/m/Y" }}</th>
                                {% endfor %}
                            </tr>
                        </thead>
                        <tbody>
                            {% for dado in dados_frequencia %}
                                <tr>
                                    <td>{{ dado.aluno.nome }}</td>
                                    {% for data in datas_atividades %}
                                        <td class="text-center">
                                            {% for freq in dado.frequencias %}
                                                {% if freq.atividade.data_inicio.date == data %}
                                                    {% if freq.presente %}
                                                        <span class="text-success"><i class="fas fa-check"></i></span>
                                                    {% else %}
                                                        <span class="text-danger"><i class="fas fa-times"></i></span>
                                                    {% endif %}
                                                {% endif %}
                                            {% endfor %}
                                        </td>
                                    {% endfor %}
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    {% else %}
        <div class="alert alert-info">
            <p>Não há dados de frequência disponíveis para esta turma.</p>
        </div>
    {% endif %}
</div>
{% endblock %}



### Arquivo: turmas\templates\turmas\relatorio_turmas.html

html
{% extends 'base.html' %}

{% block title %}Relatório de Turmas{% endblock %}

{% block extra_css %}
<style>
    .card-counter {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        padding: 20px;
        background-color: #fff;
        height: 100%;
        border-radius: 5px;
        transition: .3s linear all;
    }
    
    .card-counter.primary {
        background-color: #007bff;
        color: #FFF;
    }
    
    .card-counter.success {
        background-color: #28a745;
        color: #FFF;
    }
    
    .card-counter.info {
        background-color: #17a2b8;
        color: #FFF;
    }
    
    .card-counter.warning {
        background-color: #ffc107;
        color: #FFF;
    }
    
    .card-counter.danger {
        background-color: #dc3545;
        color: #FFF;
    }
    
    .card-counter i {
        font-size: 4em;
        opacity: 0.3;
    }
    
    .card-counter .count-numbers {
        position: absolute;
        right: 35px;
        top: 20px;
        font-size: 32px;
        display: block;
    }
    
    .card-counter .count-name {
        position: absolute;
        right: 35px;
        top: 65px;
        font-style: italic;
        text-transform: capitalize;
        opacity: 0.7;
        display: block;
    }
    
    .progress-bar-container {
        height: 25px;
        margin-bottom: 10px;
    }
    
    .progress-bar-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
    }
</style>
{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Relatório de Turmas</h1>
        <div>
            <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary me-2">Voltar para Lista</a>
            <button onclick="window.print()" class="btn btn-primary">
                <i class="fas fa-print"></i> Imprimir Relatório
            </button>
        </div>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <h5 class="card-title">Total de Turmas</h5>
                    <p class="card-text display-4">{{ total_turmas }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center bg-success text-white">
                <div class="card-body">
                    <h5 class="card-title">Turmas Ativas</h5>
                    <p class="card-text display-4">{{ turmas_ativas }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center bg-info text-white">
                <div class="card-body">
                    <h5 class="card-title">Turmas Concluídas</h5>
                    <p class="card-text display-4">{{ turmas_concluidas }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center bg-danger text-white">
                <div class="card-body">
                    <h5 class="card-title">Turmas Canceladas</h5>
                    <p class="card-text display-4">{{ turmas_canceladas }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">Turmas por Curso</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Curso</th>
                                    <th>Quantidade</th>
                                    <th>Percentual</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for item in turmas_por_curso %}
                                    <tr>
                                        <td>{{ item.curso.nome }}</td>
                                        <td>{{ item.count }}</td>
                                        <td>{{ item.percentage|floatformat:1 }}%</td>
                                    </tr>
                                {% empty %}
                                    <tr>
                                        <td colspan="3" class="text-center">Nenhum dado disponível</td>
                                    </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">Turmas por Instrutor</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Instrutor</th>
                                    <th>Principal</th>
                                    <th>Auxiliar</th>
                                    <th>Aux. Instrução</th>
                                    <th>Total</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for item in turmas_por_instrutor %}
                                    <tr>
                                        <td>{{ item.instrutor.nome }}</td>
                                        <td>{{ item.count_principal }}</td>
                                        <td>{{ item.count_auxiliar }}</td>
                                        <td>{{ item.count_aux_instrucao }}</td>
                                        <td>{{ item.total }}</td>
                                    </tr>
                                {% empty %}
                                    <tr>
                                        <td colspan="5" class="text-center">Nenhum dado disponível</td>
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

{% block extra_js %}
<script>
    // Filtros personalizados para os cálculos nas barras de progresso
    function div(a, b) {
        return a / b;
    }
    
    function mul(a, b) {
        return a * b;
    }
</script>
{% endblock %}



### Arquivo: turmas\templates\turmas\turma_form.html

html
{% extends 'base.html' %}

{% block content %}
  <h1>Criar Turma</h1>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Criar</button>
  </form>
{% endblock %}


'''