'''
# Revisão da Funcionalidade: presencas

## Arquivos forms.py:


### Arquivo: presencas\templates\presencas\registrar_presenca_em_massa.html

html
{% extends 'base.html' %}

{% block title %}Registrar Presença em Massa{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Registrar Presença em Massa</h1>
        <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    <div class="card">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Selecione a Turma e a Data</h5>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label for="turma" class="form-label">Turma</label>
                        <select name="turma" id="turma" class="form-select" required>
                            <option value="">Selecione uma turma</option>
                            {% for turma in turmas %}
                                <option value="{{ turma.id }}">{{ turma.nome }} - {{ turma.curso.nome }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="col-md-6">
                        <label for="data" class="form-label">Data</label>
                        <input type="date" name="data" id="data" class="form-control" 
                               value="{{ data_hoje|date:'Y-m-d' }}" required>
                    </div>
                </div>
                
                <div class="mb-3">
                    <label for="atividade" class="form-label">Atividade</label>
                    <select name="atividade" id="atividade" class="form-select" required>
                        <option value="">Selecione uma atividade</option>
                        <!-- As atividades serão carregadas via JavaScript quando uma turma for selecionada -->
                    </select>
                </div>
                
                <div id="lista-alunos" class="mt-4" style="display: none;">
                    <h5>Lista de Alunos</h5>
                    <div class="mb-3 form-check">
                        <input type="checkbox" class="form-check-input" id="marcar-todos" checked>
                        <label class="form-check-label" for="marcar-todos">Marcar/Desmarcar Todos</label>
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
                            <tbody id="tbody-alunos">
                                <!-- Os alunos serão carregados via JavaScript -->
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <div class="d-flex justify-content-between mt-4">
                    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">Cancelar</a>
                    <button type="submit" class="btn btn-primary" id="btn-registrar" disabled>
                        <i class="fas fa-save"></i> Registrar Presenças
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const turmaSelect = document.getElementById('turma');
        const atividadeSelect = document.getElementById('atividade');
        const listaAlunos = document.getElementById('lista-alunos');
        const tbodyAlunos = document.getElementById('tbody-alunos');
        const btnRegistrar = document.getElementById('btn-registrar');
        const marcarTodosCheckbox = document.getElementById('marcar-todos');
        
        // Carregar atividades quando uma turma for selecionada
        turmaSelect.addEventListener('change', function() {
            const turmaId = this.value;
            
            if (!turmaId) {
                atividadeSelect.innerHTML = '<option value="">Selecione uma atividade</option>';
                listaAlunos.style.display = 'none';
                btnRegistrar.disabled = true;
                return;
            }
            
            // Fazer requisição AJAX para buscar atividades da turma
            fetch(`/api/atividades-por-turma/${turmaId}/`)
                .then(response => response.json())
                .then(data => {
                    atividadeSelect.innerHTML = '<option value="">Selecione uma atividade</option>';
                    
                    if (data.atividades && data.atividades.length > 0) {
                        data.atividades.forEach(atividade => {
                            const option = document.createElement('option');
                            option.value = atividade.id;
                            option.textContent = atividade.nome;
                            atividadeSelect.appendChild(option);
                        });
                    } else {
                        const option = document.createElement('option');
                        option.value = "";
                        option.textContent = "Nenhuma atividade encontrada para esta turma";
                        option.disabled = true;
                        atividadeSelect.appendChild(option);
                    }
                })
                .catch(error => console.error('Erro ao buscar atividades:', error));
        });
        
        // Carregar alunos quando uma atividade for selecionada
        atividadeSelect.addEventListener('change', function() {
            const atividadeId = this.value;
            const turmaId = turmaSelect.value;
            
            if (!atividadeId || !turmaId) {
                listaAlunos.style.display = 'none';
                btnRegistrar.disabled = true;
                return;
            }
            
            // Fazer requisição AJAX para buscar alunos da turma
            fetch(`/api/alunos-por-turma/${turmaId}/`)
                .then(response => response.json())
                .then(data => {
                    tbodyAlunos.innerHTML = '';
                    
                    if (data.alunos && data.alunos.length > 0) {
                        data.alunos.forEach((aluno, index) => {
                            const tr = document.createElement('tr');
                            
                            tr.innerHTML = `
                                <td>${index + 1}</td>
                                <td>
                                    <div class="d-flex align-items-center">
                                        ${aluno.foto ? 
                                            `<img src="${aluno.foto}" alt="${aluno.nome}" 
                                                 class="rounded-circle me-2" width="40" height="40" 
                                                 style="object-fit: cover;">` : 
                                            `<div class="rounded-circle bg-secondary me-2 d-flex align-items-center justify-content-center" 
                                                 style="width: 40px; height: 40px; color: white;">
                                                ${aluno.nome.charAt(0).toUpperCase()}
                                            </div>`
                                        }
                                        <div>
                                            <div>${aluno.nome}</div>
                                            <small class="text-muted">${aluno.cpf}</small>
                                        </div>
                                    </div>
                                </td>
                                <td>
                                    <div class="form-check">
                                        <input class="form-check-input presenca-checkbox" type="checkbox" 
                                               name="presentes" value="${aluno.cpf}" id="presente_${aluno.cpf}" checked>
                                        <label class="form-check-label" for="presente_${aluno.cpf}">
                                            Presente
                                        </label>
                                    </div>
                                </td>
                                <td>
                                    <textarea class="form-control justificativa-field" 
                                              name="justificativa_${aluno.cpf}" rows="1" 
                                              placeholder="Justificativa para ausência" disabled></textarea>
                                </td>
                            `;
                            
                            tbodyAlunos.appendChild(tr);
                        });
                        
                        // Adicionar eventos para os checkboxes de presença
                        const checkboxes = document.querySelectorAll('.presenca-checkbox');
                        checkboxes.forEach(function(checkbox) {
                            checkbox.addEventListener('change', function() {
                                const row = this.closest('tr');
                                const justificativa = row.querySelector('.justificativa-field');
                                
                                if (this.checked) {
                                    justificativa.disabled = true;
                                    justificativa.value = '';
                                } else {
                                    justificativa.disabled = false;
                                }
                            });
                        });
                        
                        // Marcar/Desmarcar todos
                        marcarTodosCheckbox.addEventListener('change', function() {
                            checkboxes.forEach(function(checkbox) {
                                checkbox.checked = marcarTodosCheckbox.checked;
                                const row = checkbox.closest('tr');
                                const justificativa = row.querySelector('.justificativa-field');
                                
                                if (checkbox.checked) {
                                    justificativa.disabled = true;
                                    justificativa.value = '';
                                } else {
                                    justificativa.disabled = false;
                                }
                            });
                        });
                        
                        listaAlunos.style.display = 'block';
                        btnRegistrar.disabled = false;
                    } else {
                        tbodyAlunos.innerHTML = `
                            <tr>
                                <td colspan="4" class="text-center py-3">
                                    <p class="mb-0">Nenhum aluno encontrado para esta turma.</p>
                                </td>
                            </tr>
                        `;
                        
                        listaAlunos.style.display = 'block';
                        btnRegistrar.disabled = true;
                    }
                })
                .catch(error => console.error('Erro ao buscar alunos:', error));
        });
    });
</script>
{% endblock %}



### Arquivo: presencas\templates\presencas\registrar_presencas_multiplas.html

html
{% extends 'base.html' %}

{% block title %}Registro de Presença em Massa{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Registro de Presença em Massa</h1>
        <div>
            <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar para Lista
            </a>
        </div>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Selecionar Atividade e Data</h5>
        </div>
        <div class="card-body">
            <form id="selecao-form" method="get">
                <div class="row">
                    <div class="col-md-5">
                        <div class="mb-3">
                            <label for="turma" class="form-label">Turma</label>
                            <select class="form-select" id="turma" name="turma">
                                <option value="">Selecione uma turma</option>
                                {% for turma in turmas %}
                                <option value="{{ turma.id }}" {% if request.GET.turma == turma.id|stringformat:"s" %}selected{% endif %}>
                                    {{ turma.nome }}
                                </option>
                                {% endfor %}
                            </select>
                        </div>
                    </div>
                    <div class="col-md-5">
                        <div class="mb-3">
                            <label for="atividade" class="form-label">Atividade</label>
                            <select class="form-select" id="atividade" name="atividade">
                                <option value="">Selecione uma atividade</option>
                                {% for atividade in atividades %}
                                <option value="{{ atividade.id }}" {% if request.GET.atividade == atividade.id|stringformat:"s" %}selected{% endif %}>
                                    {{ atividade.nome }} ({{ atividade.data_inicio|date:"d/m/Y" }})
                                </option>
                                {% endfor %}
                            </select>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="mb-3">
                            <label for="data" class="form-label">Data</label>
                            <input type="date" class="form-control" id="data" name="data" value="{{ request.GET.data|default:data_hoje }}">
                        </div>
                    </div>
                </div>
                <div class="text-end">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-search"></i> Buscar Alunos
                    </button>
                </div>
            </form>
        </div>
    </div>
    
    {% if alunos %}
    <form method="post" id="presenca-form">
        {% csrf_token %}
        <input type="hidden" name="atividade" value="{{ request.GET.atividade }}">
        <input type="hidden" name="data" value="{{ request.GET.data|default:data_hoje }}">
        
        <div class="card">
            <div class="card-header bg-success text-white">
                <div class="d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">Lista de Presença</h5>
                    <div>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="checkbox" id="marcar-todos" checked>
                            <label class="form-check-label text-white" for="marcar-todos">
                                Marcar/Desmarcar Todos
                            </label>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
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
                                            <img src="{{ aluno.foto }}" alt="Foto de {{ aluno.nome }}" 
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
                                            <small class="text-muted">{{ aluno.cpf }}</small>
                                        </div>
                                    </div>
                                </td>
                                <td>
                                    <div class="form-check">
                                        <input class="form-check-input presenca-checkbox" type="checkbox" name="presentes" value="{{ aluno.cpf }}" id="presente_{{ aluno.cpf }}" {% if aluno.presenca and aluno.presenca.presente %}checked{% else %}checked{% endif %}>
                                        <label class="form-check-label" for="presente_{{ aluno.cpf }}">
                                            Presente
                                        </label>
                                    </div>
                                </td>
                                <td>
                                    <textarea class="form-control justificativa-field" name="justificativa_{{ aluno.cpf }}" rows="1" placeholder="Justificativa para ausência" {% if aluno.presenca and aluno.presenca.presente %}disabled{% else %}disabled{% endif %}>{{ aluno.presenca.justificativa|default:"" }}</textarea>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="card-footer">
                <div class="d-flex justify-content-between">
                    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
                        <i class="fas fa-times"></i> Cancelar
                    </a>
                    <button type="submit" class="btn btn-success">
                        <i class="fas fa-save"></i> Salvar Presenças
                    </button>
                </div>
            </div>
        </div>
    </form>
    {% elif request.GET.atividade %}
    <div class="alert alert-warning">
        <i class="fas fa-exclamation-triangle"></i> Nenhum aluno encontrado para esta atividade.
    </div>
    {% endif %}
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Inicializar Select2 para melhorar a experiência de seleção
        if (typeof $.fn.select2 === 'function') {
            $('#turma').select2({
                theme: 'bootstrap-5',
                placeholder: 'Selecione uma turma',
                allowClear: true
            });
            
            $('#atividade').select2({
                theme: 'bootstrap-5',
                placeholder: 'Selecione uma atividade',
                allowClear: true
            });
        }
        
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
        if (marcarTodos) {
            marcarTodos.addEventListener('change', function() {
                checkboxes.forEach(function(checkbox) {
                    checkbox.checked = marcarTodos.checked;
                    toggleJustificativa(checkbox);
                });
            });
        }
        
        // Filtrar atividades por turma
        const turmaSelect = document.getElementById('turma');
        const atividadeSelect = document.getElementById('atividade');
        
        if (turmaSelect && atividadeSelect) {
            turmaSelect.addEventListener('change', function() {
                const turmaId = this.value;
                
                if (turmaId) {
                    // Fazer requisição AJAX para buscar atividades da turma
                    fetch(`/presencas/api/atividades-por-turma/${turmaId}/`)
                        .then(response => response.json())
                        .then(data => {
                            // Limpar select de atividades
                            atividadeSelect.innerHTML = '<option value="">Selecione uma atividade</option>';
                            
                            // Adicionar novas opções
                            if (data.success && data.atividades && data.atividades.length > 0) {
                                data.atividades.forEach(atividade => {
                                    const option = document.createElement('option');
                                    option.value = atividade.id;
                                    option.textContent = `${atividade.nome} (${atividade.data})`;
                                    atividadeSelect.appendChild(option);
                                });
                            }
                            
                            // Atualizar Select2 se estiver sendo usado
                            if (typeof $.fn.select2 === 'function') {
                                $(atividadeSelect).trigger('change');
                            }
                        })
                        .catch(error => console.error('Erro ao buscar atividades:', error));
                }
            });
        }
    });
</script>
{% endblock %}



### Arquivo: presencas\templates\presencas\relatorio_presencas.html

html
{% extends 'base.html' %}

{% block title %}Relatório de Presenças{% endblock %}

{% block extra_css %}
<style>
    .stat-card {
        transition: transform 0.3s;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
    }
    
    .chart-container {
        position: relative;
        height: 300px;
        margin-bottom: 20px;
    }
</style>
{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Relatório de Presenças</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-primary me-2">
                <i class="fas fa-list"></i> Lista de Presenças
            </a>
            <button onclick="window.print()" class="btn btn-success">
                <i class="fas fa-print"></i> Imprimir Relatório
            </button>
        </div>
    </div>
    
    <!-- Filtros -->
    <div class="card mb-4 no-print">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-3">
                    <label for="aluno" class="form-label">Aluno</label>
                    <select name="aluno" id="aluno" class="form-select">
                        <option value="">Todos os alunos</option>
                        {% for aluno in alunos %}
                        <option value="{{ aluno.cpf }}" {% if filtros.aluno == aluno.cpf %}selected{% endif %}>
                            {{ aluno.nome }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="col-md-3">
                    <label for="turma" class="form-label">Turma</label>
                    <select name="turma" id="turma" class="form-select">
                        <option value="">Todas as turmas</option>
                        {% for turma in turmas %}
                        <option value="{{ turma.id }}" {% if filtros.turma == turma.id|stringformat:"s" %}selected{% endif %}>
                            {{ turma.nome }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="col-md-3">
                    <label for="data_inicio" class="form-label">Data Início</label>
                    <input type="date" class="form-control" id="data_inicio" name="data_inicio" value="{{ filtros.data_inicio }}">
                </div>
                
                <div class="col-md-3">
                    <label for="data_fim" class="form-label">Data Fim</label>
                    <input type="date" class="form-control" id="data_fim" name="data_fim" value="{{ filtros.data_fim }}">
                </div>
                
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                    <a href="{% url 'presencas:relatorio_presencas' %}" class="btn btn-secondary">
                        <i class="fas fa-undo"></i> Limpar Filtros
                    </a>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Estatísticas Gerais -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card stat-card bg-primary text-white h-100">
                <div class="card-body text-center">
                    <h5 class="card-title">Total de Registros</h5>
                    <p class="display-4">{{ total }}</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card stat-card bg-success text-white h-100">
                <div class="card-body text-center">
                    <h5 class="card-title">Presenças</h5>
                    <p class="display-4">{{ presentes }}</p>
                    <p>{{ taxa_presenca|floatformat:1 }}%</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card stat-card bg-danger text-white h-100">
                <div class="card-body text-center">
                    <h5 class="card-title">Ausências</h5>
                    <p class="display-4">{{ ausentes }}</p>
                    <p>{{ 100|subtract:taxa_presenca|floatformat:1 }}%</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card stat-card bg-info text-white h-100">
                <div class="card-body text-center">
                    <h5 class="card-title">Média de Presença</h5>
                    <p class="display-4">{{ taxa_presenca|floatformat:1 }}%</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Gráficos -->
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Presença por Aluno (Top 10)</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="alunosChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Presença por Turma</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="turmasChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-12">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Evolução de Presença por Data</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="datasChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Tabelas de Estatísticas -->
    <div class="row">
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Estatísticas por Aluno</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped table-hover">
                            <thead>
                                <tr>
                                    <th>Aluno</th>
                                    <th>Presenças</th>
                                    <th>Ausências</th>
                                    <th>Total</th>
                                    <th>Percentual</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for aluno in alunos_stats %}
                                <tr>
                                    <td>{{ aluno.aluno__nome }}</td>
                                    <td>{{ aluno.presentes }}</td>
                                    <td>{{ aluno.ausentes }}</td>
                                    <td>{{ aluno.total }}</td>
                                    <td>
                                        <div class="progress" style="height: 20px;">
                                            <div class="progress-bar {% if aluno.percentual < 75 %}bg-danger{% elif aluno.percentual < 85 %}bg-warning{% else %}bg-success{% endif %}" 
                                                 role="progressbar" style="width: {{ aluno.percentual }}%;" 
                                                 aria-valuenow="{{ aluno.percentual }}" aria-valuemin="0" aria-valuemax="100">
                                                {{ aluno.percentual|floatformat:1 }}%
                                            </div>
                                        </div>
                                    </td>
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
        
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Estatísticas por Turma</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped table-hover">
                            <thead>
                                <tr>
                                    <th>Turma</th>
                                    <th>Presenças</th>
                                    <th>Ausências</th>
                                    <th>Total</th>
                                    <th>Percentual</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for turma in turmas_stats %}
                                <tr>
                                    <td>{{ turma.atividade__turmas__nome }}</td>
                                    <td>{{ turma.presentes }}</td>
                                    <td>{{ turma.ausentes }}</td>
                                    <td>{{ turma.total }}</td>
                                    <td>
                                        <div class="progress" style="height: 20px;">
                                            <div class="progress-bar {% if turma.percentual < 75 %}bg-danger{% elif turma.percentual < 85 %}bg-warning{% else %}bg-success{% endif %}" 
                                                 role="progressbar" style="width: {{ turma.percentual }}%;" 
                                                 aria-valuenow="{{ turma.percentual }}" aria-valuemin="0" aria-valuemax="100">
                                                {{ turma.percentual|floatformat:1 }}%
                                            </div>
                                        </div>
                                    </td>
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
    
    <div class="row mb-4">
        <div class="col-md-12">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Estatísticas por Data</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped table-hover">
                            <thead>
                                <tr>
                                    <th>Data</th>
                                    <th>Presenças</th>
                                    <th>Ausências</th>
                                    <th>Total</th>
                                    <th>Percentual</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for data in datas_stats %}
                                <tr>
                                    <td>{{ data.data|date:"d/m/Y" }}</td>
                                    <td>{{ data.presentes }}</td>
                                    <td>{{ data.ausentes }}</td>
                                    <td>{{ data.total }}</td>
                                    <td>
                                        <div class="progress" style="height: 20px;">
                                            <div class="progress-bar {% if data.percentual < 75 %}bg-danger{% elif data.percentual < 85 %}bg-warning{% else %}bg-success{% endif %}" 
                                                 role="progressbar" style="width: {{ data.percentual }}%;" 
                                                 aria-valuenow="{{ data.percentual }}" aria-valuemin="0" aria-valuemax="100">
                                                {{ data.percentual|floatformat:1 }}%
                                            </div>
                                        </div>
                                    </td>
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
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Gráfico de presença por aluno
        var ctxAlunos = document.getElementById('alunosChart').getContext('2d');
        new Chart(ctxAlunos, {
            type: 'bar',
            data: {
                labels: {{ alunos_labels|safe }},
                datasets: [{
                    label: 'Percentual de Presença',
                    data: {{ alunos_presenca|safe }},
                    backgroundColor: function(context) {
                        const value = context.dataset.data[context.dataIndex];
                        return value < 75 ? 'rgba(220, 53, 69, 0.7)' : 
                               value < 85 ? 'rgba(255, 193, 7, 0.7)' : 
                               'rgba(40, 167, 69, 0.7)';
                    },
                    borderColor: function(context) {
                        const value = context.dataset.data[context.dataIndex];
                        return value < 75 ? 'rgba(220, 53, 69, 1)' : 
                               value < 85 ? 'rgba(255, 193, 7, 1)' : 
                               'rgba(40, 167, 69, 1)';
                    },
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
        
        // Gráfico de presença por turma
        var ctxTurmas = document.getElementById('turmasChart').getContext('2d');
        new Chart(ctxTurmas, {
            type: 'bar',
            data: {
                labels: {{ turmas_labels|safe }},
                datasets: [{
                    label: 'Percentual de Presença',
                    data: {{ turmas_presenca|safe }},
                    backgroundColor: function(context) {
                        const value = context.dataset.data[context.dataIndex];
                        return value < 75 ? 'rgba(220, 53, 69, 0.7)' : 
                               value < 85 ? 'rgba(255, 193, 7, 0.7)' : 
                               'rgba(40, 167, 69, 0.7)';
                    },
                    borderColor: function(context) {
                        const value = context.dataset.data[context.dataIndex];
                        return value < 75 ? 'rgba(220, 53, 69, 1)' : 
                               value < 85 ? 'rgba(255, 193, 7, 1)' : 
                               'rgba(40, 167, 69, 1)';
                    },
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
        
        // Gráfico de evolução de presença por data
        var ctxDatas = document.getElementById('datasChart').getContext('2d');
        new Chart(ctxDatas, {
            type: 'line',
            data: {
                labels: {{ datas_labels|safe }},
                datasets: [{
                    label: 'Percentual de Presença',
                    data: {{ datas_presenca|safe }},
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    tension: 0.1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.raw.toFixed(1) + '%';
                            }
                        }
                    }
                }
            }
        });
        
        // Inicializar Select2 para melhorar a experiência de seleção
        if (typeof $.fn.select2 === 'function') {
            $('#aluno').select2({
                theme: 'bootstrap-5',
                placeholder: 'Selecione um aluno',
                allowClear: true
            });
            
            $('#turma').select2({
                theme: 'bootstrap-5',
                placeholder: 'Selecione uma turma',
                allowClear: true
            });
        }
    });
</script>

<style type="text/css" media="print">
    .no-print, .no-print * {
        display: none !important;
    }
    
    .container-fluid {
        width: 100%;
        padding: 0;
    }
    
    .card {
        border: 1px solid #ddd;
        margin-bottom: 20px;
        break-inside: avoid;
    }
    
    .card-header {
        background-color: #f8f9fa !important;
        color: #000 !important;
        border-bottom: 1px solid #ddd;
    }
    
    .chart-container {
        height: 250px;
    }
    
    @page {
        size: landscape;
        margin: 1cm;
    }
</style>
{% endblock %}


'''