# Revisão da Funcionalidade: templates

## Arquivos de Template:


### Arquivo: templates\atividades\academicas\listar_atividades_academicas.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Atividades Acadêmicas - OMAUM{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Barra superior com título e botão -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Atividades Acadêmicas</h1>
        <a href="{% url 'atividades:criar_atividade_academica' %}" class="btn btn-primary me-2">
            <i class="fas fa-plus"></i> Nova Atividade
        </a>
    </div>
    <div class="card mb-4">
        <!-- Filtro no card-header -->
        <div class="card-header">
            <form method="get" id="filtro-atividades" class="row g-3">
                <div class="col-md-4">
                    <label for="id_q" class="form-label">Buscar</label>
                    <input type="text" name="q" id="id_q" class="form-control" 
                           placeholder="Buscar por nome ou descrição..." value="{{ query|default:'' }}">
                </div>
                <div class="col-md-4">
                    <label for="id_curso" class="form-label">Curso</label>
                    <select name="curso" id="id_curso" class="form-select" onchange="this.form.submit()">
                        <option value="">Todos os cursos</option>
                        {% for curso in cursos %}
                            <option value="{{ curso.id }}" {% if curso_selecionado == curso.id|stringformat:"s" %}selected{% endif %}>
                                {{ curso.nome }}
                            </option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-4">
                    <label for="id_turmas" class="form-label">Turmas</label>
                    <select name="turma" id="id_turmas" class="form-select">
                        <option value="">Todas as turmas</option>
                        {% for turma in turmas %}
                            <option value="{{ turma.id }}" {% if turma_selecionada == turma.id|stringformat:"s" %}selected{% endif %}>
                                {{ turma.nome }}
                            </option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-12 mt-3">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-search"></i> Filtrar
                    </button>
                </div>
            </form>
        </div>
        <!-- Tabela de atividades no card-body -->
        <div class="card-body table-responsive">
            {% include "atividades/academicas/partials/atividades_tabela.html" %}
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/atividades_filtros.js' %}"></script>
{% endblock %}



### Arquivo: templates\atividades\academicas\partials\atividades_tabela.html

html
<table class="table table-striped align-middle">
      <thead>
          <tr>
              <th>Nome</th>
              <th>Curso</th>
              <th>Turmas</th>
              <th>Tipo</th>
              <th>Status</th>
              <th>Data Início</th>
              <th>Ações</th>
          </tr>
      </thead>
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
              {% for turma in atividade.turmas.all %}
                <span class="badge bg-secondary">{{ turma.nome }}</span>
              {% empty %}
                <span class="text-muted">Nenhuma</span>
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
</table>



### Arquivo: templates\atividades\dashboard_atividades.html

html
{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Dashboard de Atividades</h1>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <form method="get" id="filtro-form" class="row g-3">
                <div class="col-md-3">
                    <label for="id_curso" class="form-label">Curso</label>
                    <select name="curso" id="id_curso" class="form-select">
                        <option value="">Todos os cursos</option>
                        {% for curso in cursos %}
                            <option value="{{ curso.codigo_curso }}" {% if filtros.curso_id|stringformat:"s" == curso.codigo_curso|stringformat:"s" %}selected{% endif %}>
                                {{ curso.nome }}
                            </option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="id_turma" class="form-label">Turma</label>
                    <select name="turma" id="id_turma" class="form-select">
                        <option value="">Todas as turmas</option>
                        {% for turma in turmas %}
                            <option value="{{ turma.id }}" {% if filtros.turma_id|stringformat:"s" == turma.id|stringformat:"s" %}selected{% endif %}>
                                {{ turma.nome }}
                            </option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="id_periodo" class="form-label">Período</label>
                    <select name="periodo" id="id_periodo" class="form-select">
                        <option value="semana" {% if filtros.periodo == 'semana' %}selected{% endif %}>Semana atual</option>
                        <option value="mes" {% if filtros.periodo == 'mes' %}selected{% endif %}>Mês atual</option>
                        <option value="trimestre" {% if filtros.periodo == 'trimestre' %}selected{% endif %}>Trimestre atual</option>
                        <option value="ano" {% if filtros.periodo == 'ano' %}selected{% endif %}>Ano atual</option>
                    </select>
                </div>
                <div class="col-12 col-md-2 mt-2">
                    <button type="submit" class="btn btn-primary w-100">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                </div>
            </form>
        </div>
        
        <div id="conteudo-container">
            <!-- O conteúdo do dashboard será carregado aqui -->
            <div class="text-center py-4">
                <div class="spinner-border" role="status">
                    <span class="visually-hidden">Carregando...</span>
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
        const filtroForm = document.getElementById('filtro-form');
        const cursoSelect = document.getElementById('id_curso');
        const turmaSelect = document.getElementById('id_turma');
        const periodoSelect = document.getElementById('id_periodo');
        
        // Gráficos
        let graficoStatus = null;
        let graficoTipo = null;
        
            // Função para atualizar as turmas com base no curso selecionado
            function atualizarTurmas(cursoId) {
                // Limpa o select de turmas
                turmaSelect.innerHTML = '<option value="">Todas as turmas</option>';
            
                // Mostra indicador de carregamento
                turmaSelect.disabled = true;
            
                // URL para a requisição AJAX
                const url = cursoId 
                    ? `{% url 'atividades:ajax_turmas_por_curso_dashboard' %}?curso_id=${cursoId}`
                    : `{% url 'atividades:ajax_turmas_por_curso_dashboard' %}`;
            
                // Faz a requisição AJAX
                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        // Adiciona as opções de turma
                        data.turmas.forEach(turma => {
                            const option = document.createElement('option');
                            option.value = turma.id;
                            option.textContent = turma.nome;
                            turmaSelect.appendChild(option);
                        });
                        turmaSelect.disabled = false;
                    })
                    .catch(error => {
                        console.error('Erro ao carregar turmas:', error);
                        turmaSelect.disabled = false;
                    });
            }
        
            // Função para aplicar os filtros via AJAX
            function aplicarFiltros() {
                if (!filtroForm) return;
            
                const formData = new FormData(filtroForm);
                const queryString = new URLSearchParams(formData).toString();
                const url = `${window.location.pathname}?${queryString}`;
            
                // Atualiza a URL sem recarregar a página
                window.history.pushState({}, '', url);
            
                // Mostra indicador de carregamento
                const conteudoContainer = document.getElementById('conteudo-container');
                if (conteudoContainer) {
                    conteudoContainer.innerHTML = '<div class="text-center py-4"><div class="spinner-border" role="status"><span class="visually-hidden">Carregando...</span></div></div>';
                }
            
                // Faz a requisição AJAX
                fetch(`{% url 'atividades:ajax_dashboard_conteudo' %}?${queryString}`, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    // Atualiza o conteúdo
                    if (conteudoContainer) {
                        conteudoContainer.innerHTML = data.html;
                    }
                
                    // Atualiza os gráficos
                    if (data.graficos) {
                        atualizarGraficos(data.graficos);
                    }
                })
                .catch(error => {
                    console.error('Erro ao filtrar dados:', error);
                    if (conteudoContainer) {
                        conteudoContainer.innerHTML = '<div class="alert alert-danger">Erro ao carregar dados. Por favor, tente novamente.</div>';
                    }
                });
            }
        
            // Função para atualizar os gráficos
            function atualizarGraficos(dados) {
                // Atualiza o gráfico de status
                if (dados.status) {
                    const ctxStatus = document.getElementById('grafico-status');
                    if (ctxStatus) {
                        if (graficoStatus) {
                            graficoStatus.destroy();
                        }
                    
                        graficoStatus = new Chart(ctxStatus, {
                            type: 'pie',
                            data: {
                                labels: dados.status.labels,
                                datasets: [{
                                    data: dados.status.dados,
                                    backgroundColor: [
                                        '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b'
                                    ]
                                }]
                            },
                            options: {
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {
                                    legend: {
                                        position: 'bottom'
                                    }
                                }
                            }
                        });
                    }
                }
            
                // Atualiza o gráfico de tipo
                if (dados.tipo) {
                    const ctxTipo = document.getElementById('grafico-tipo');
                    if (ctxTipo) {
                        if (graficoTipo) {
                            graficoTipo.destroy();
                        }
                    
                        graficoTipo = new Chart(ctxTipo, {
                            type: 'bar',
                            data: {
                                labels: dados.tipo.labels,
                                datasets: [{
                                    label: 'Quantidade',
                                    data: dados.tipo.dados,
                                    backgroundColor: '#4e73df'
                                }]
                            },
                            options: {
                                responsive: true,
                                maintainAspectRatio: false,
                                scales: {
                                    y: {
                                        beginAtZero: true,
                                        ticks: {
                                            precision: 0
                                        }
                                    }
                                }
                            }
                        });
                    }
                }
            }
        
            // Event listeners
            if (cursoSelect) {
                cursoSelect.addEventListener('change', function() {
                    atualizarTurmas(this.value);
                    aplicarFiltros();
                });
            }
        
            if (turmaSelect) {
                turmaSelect.addEventListener('change', aplicarFiltros);
            }
        
            if (periodoSelect) {
                periodoSelect.addEventListener('change', aplicarFiltros);
            }
        
            if (filtroForm) {
                filtroForm.addEventListener('submit', function(e) {
                    e.preventDefault();
                    aplicarFiltros();
                });
            }
        
            // Carrega os dados iniciais
            aplicarFiltros();            turmaSelect.innerHTML



### Arquivo: templates\atividades\partials\dashboard_conteudo.html

html
<div class="card-body">
    <div class="alert alert-info">
        <i class="fas fa-info-circle"></i> Dados do período: <strong>{{ periodo.nome }}</strong> ({{ periodo.inicio|date:"d/m/Y" }} a {{ periodo.fim|date:"d/m/Y" }})
    </div>
    
    <div class="row">
        <!-- Card com total de atividades -->
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-primary shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                                Total de Atividades</div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">{{ total_atividades }}</div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-calendar fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Cards com estatísticas por status -->
        {% for status in atividades_por_status %}
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-info shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                                {{ status.status_display }}</div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">{{ status.total }}</div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-clipboard-list fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    
    <div class="row">
        <!-- Gráfico de status -->
        <div class="col-xl-6 col-lg-6">
            <div class="card shadow mb-4">
                <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                    <h6 class="m-0 font-weight-bold text-primary">Atividades por Status</h6>
                </div>
                <div class="card-body">
                    <div class="chart-pie pt-4 pb-2" style="height: 300px;">
                        <canvas id="grafico-status"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Gráfico de tipo -->
        <div class="col-xl-6 col-lg-6">
            <div class="card shadow mb-4">
                <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                    <h6 class="m-0 font-weight-bold text-primary">Atividades por Tipo</h6>
                </div>
                <div class="card-body">
                    <div class="chart-bar pt-4 pb-2" style="height: 300px;">
                        <canvas id="grafico-tipo"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Próximas atividades -->
    <div class="card shadow mb-4">
        <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-primary">Próximas Atividades</h6>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-bordered" width="100%" cellspacing="0">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>Curso</th>
                            <th>Turmas</th>
                            <th>Tipo</th>
                            <th>Data</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for atividade in proximas_atividades %}
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
                                {% if atividade.turmas.all %}
                                    {% for turma in atividade.turmas.all %}
                                        <span class="badge bg-secondary">{{ turma.nome }}</span>
                                    {% endfor %}
                                {% else %}
                                    <span class="text-muted">Nenhuma</span>
                                {% endif %}
                            </td>
                            <td>{{ atividade.get_tipo_atividade_display }}</td>
                            <td>{{ atividade.data_inicio|date:"d/m/Y" }} {{ atividade.hora_inicio|time:"H:i" }}</td>
                            <td>{{ atividade.get_status_display }}</td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="6" class="text-center">Nenhuma atividade futura encontrada.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>



### Arquivo: templates\atividades\partials\filtro_curso_turma.html

html
<div class="row g-3">
    <div class="col-md-4">
        <label for="id_q" class="form-label">Buscar</label>
        <input type="text" name="q" id="id_q" class="form-control" 
               placeholder="Buscar por nome ou descrição..." value="{{ q|default:'' }}">
    </div>
    <div class="col-md-4">
        <label for="id_curso" class="form-label">Curso</label>
        <select name="curso" id="id_curso" class="form-select">
            <option value="">Todos os cursos</option>
            {% for curso in cursos %}
                <option value="{{ curso.codigo_curso }}" {% if filtros.curso_id|stringformat:"s" == curso.codigo_curso|stringformat:"s" %}selected{% endif %}>
                    {{ curso.nome }}
                </option>
            {% endfor %}
        </select>
    </div>
    <div class="col-md-4">
        <label for="id_turma" class="form-label">Turmas</label>
        <select name="turma" id="id_turma" class="form-select">
            <option value="">Todas as turmas</option>
            {% for turma in turmas %}
                <option value="{{ turma.id }}" {% if filtros.turma_id|stringformat:"s" == turma.id|stringformat:"s" %}selected{% endif %}>
                    {{ turma.nome }}
                </option>
            {% endfor %}
        </select>
    </div>
    <div class="col-12 col-md-2 mt-2">
        <button type="submit" class="btn btn-primary w-100">
            <i class="fas fa-search"></i> Filtrar
        </button>
    </div>
</div>



### Arquivo: templates\atividades\partials\js_filtro_curso_turma.html

html
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const filtroForm = document.getElementById('filtro-form');
        const cursoSelect = document.getElementById('id_curso');
        const turmaSelect = document.getElementById('id_turma');
        const searchInput = document.getElementById('id_q');
        
        // Função para atualizar as turmas com base no curso selecionado
        function atualizarTurmas(cursoId) {
            // Limpa o select de turmas
            turmaSelect.innerHTML = '<option value="">Todas as turmas</option>';
            
            // Mostra indicador de carregamento
            turmaSelect.disabled = true;
            
            // URL para a requisição AJAX
            const url = cursoId 
                ? `{% url 'atividades:ajax_turmas_por_curso' %}?curso_id=${cursoId}`
                : `{% url 'atividades:ajax_turmas_por_curso' %}`;
            
            // Faz a requisição AJAX
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    // Adiciona as opções de turma
                    data.turmas.forEach(turma => {
                        const option = document.createElement('option');
                        option.value = turma.id;
                        option.textContent = turma.nome;
                        turmaSelect.appendChild(option);
                    });
                    turmaSelect.disabled = false;
                })
                .catch(error => {
                    console.error('Erro ao carregar turmas:', error);
                    turmaSelect.disabled = false;
                });
        }
        
        // Função para aplicar os filtros via AJAX
        function aplicarFiltros() {
            if (!filtroForm) return;
            
            const formData = new FormData(filtroForm);
            const queryString = new URLSearchParams(formData).toString();
            const url = `${window.location.pathname}?${queryString}`;
            
            // Atualiza a URL sem recarregar a página
            window.history.pushState({}, '', url);
            
            // Mostra indicador de carregamento
            const conteudoContainer = document.getElementById('conteudo-container');
            if (conteudoContainer) {
                conteudoContainer.innerHTML = '<div class="text-center py-4"><div class="spinner-border" role="status"><span class="visually-hidden">Carregando...</span></div></div>';
            }
            
            // Faz a requisição AJAX
            fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                // Atualiza o conteúdo
                if (conteudoContainer) {
                    conteudoContainer.innerHTML = data.html;
                }
                
                // Atualiza gráficos se existirem
                if (data.graficos && typeof atualizarGraficos === 'function') {
                    atualizarGraficos(data.graficos);
                }
            })
            .catch(error => {
                console.error('Erro ao filtrar dados:', error);
                if (conteudoContainer) {
                    conteudoContainer.innerHTML = '<div class="alert alert-danger">Erro ao carregar dados. Por favor, tente novamente.</div>';
                }
            });
        }
        
        // Event listeners
        if (cursoSelect) {
            cursoSelect.addEventListener('change', function() {
                atualizarTurmas(this.value);
                aplicarFiltros();
            });
        }
        
        if (turmaSelect) {
            turmaSelect.addEventListener('change', aplicarFiltros);
        }
        
        if (searchInput) {
            // Implementa debounce para o campo de busca
            let timeoutId;
            searchInput.addEventListener('input', function() {
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => {
                    aplicarFiltros();
                }, 500); // Aguarda 500ms após o usuário parar de digitar
            });
        }
        
        if (filtroForm) {
            filtroForm.addEventListener('submit', function(e) {
                e.preventDefault();
                aplicarFiltros();
            });
        }
    });
</script>



### Arquivo: templates\atividades\ritualisticas\listar_atividades_ritualisticas.html

html
{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <!-- Barra superior com título e botão -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Atividades Ritualísticas</h1>
        <a href="{% url 'atividades:criar_atividade_ritualistica' %}" class="btn btn-primary me-2">
            <i class="fas fa-plus"></i> Nova Atividade
        </a>
    </div>
    <div class="card mb-4">
        <!-- Filtro no card-header -->
        <div class="card-header">
            <form method="get" id="filtro-form" class="row g-3">
                <div class="col-md-6">
                    <label for="id_q" class="form-label">Buscar</label>
                    <input type="text" name="q" id="id_q" class="form-control" 
                           placeholder="Buscar por nome ou descrição..." value="{{ q|default:'' }}">
                </div>
                <div class="col-12 col-md-2 mt-2">
                    <button type="submit" class="btn btn-primary w-100">
                        <i class="fas fa-search"></i> Filtrar
                    </button>
                </div>
            </form>
        </div>
        <!-- Tabela de atividades no card-body -->
        <div class="card-body table-responsive">
            <div id="conteudo-container">
                {% include "atividades/ritualisticas/partials/atividades_tabela.html" %}
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const filtroForm = document.getElementById('filtro-form');
        const searchInput = document.getElementById('id_q');
        
        // Função para aplicar os filtros via AJAX
        function aplicarFiltros() {
            if (!filtroForm) return;
            
            const formData = new FormData(filtroForm);
            const queryString = new URLSearchParams(formData).toString();
            const url = `${window.location.pathname}?${queryString}`;
            
            // Atualiza a URL sem recarregar a página
            window.history.pushState({}, '', url);
            
            // Mostra indicador de carregamento
            const conteudoContainer = document.getElementById('conteudo-container');
            if (conteudoContainer) {
                conteudoContainer.innerHTML = '<div class="text-center py-4"><div class="spinner-border" role="status"><span class="visually-hidden">Carregando...</span></div></div>';
            }
            
            // Faz a requisição AJAX
            fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                // Atualiza o conteúdo
                if (conteudoContainer) {
                    conteudoContainer.innerHTML = data.html;
                }
            })
            .catch(error => {
                console.error('Erro ao filtrar dados:', error);
                if (conteudoContainer) {
                    conteudoContainer.innerHTML = '<div class="alert alert-danger">Erro ao carregar dados. Por favor, tente novamente.</div>';
                }
            });
        }
        
        if (searchInput) {
            // Implementa debounce para o campo de busca
            let timeoutId;
            searchInput.addEventListener('input', function() {
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => {
                    aplicarFiltros();
                }, 500); // Aguarda 500ms após o usuário parar de digitar
            });
        }
        
        if (filtroForm) {
            filtroForm.addEventListener('submit', function(e) {
                e.preventDefault();
                aplicarFiltros();
            });
        }
    });
</script>
{% endblock %}

