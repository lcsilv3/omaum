'''
# Revisão da Funcionalidade: pagamentos

## Arquivos forms.py:


### Arquivo: pagamentos\templates\pagamentos\dashboard.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Dashboard de Pagamentos{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Dashboard de Pagamentos</h1>
        <div>
            <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-primary">
                <i class="fas fa-list"></i> Listar Pagamentos
            </a>
            <a href="{% url 'pagamentos:criar_pagamento' %}" class="btn btn-success">
                <i class="fas fa-plus"></i> Novo Pagamento
            </a>
        </div>
    </div>

    <!-- Cards de estatísticas -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card bg-primary text-white">
                <div class="card-body">
                    <h5 class="card-title">Total de Alunos</h5>
                    <h2 class="display-4">{{ total_alunos }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-success text-white">
                <div class="card-body">
                    <h5 class="card-title">Pagamentos Pagos</h5>
                    <h2 class="display-4">{{ pagamentos_pagos }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-warning text-dark">
                <div class="card-body">
                    <h5 class="card-title">Pagamentos Pendentes</h5>
                    <h2 class="display-4">{{ pagamentos_pendentes }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-danger text-white">
                <div class="card-body">
                    <h5 class="card-title">Pagamentos Atrasados</h5>
                    <h2 class="display-4">{{ pagamentos_atrasados }}</h2>
                </div>
            </div>
        </div>
    </div>

    <!-- Cards de valores -->
    <div class="row mb-4">
        <div class="col-md-4">
            <div class="card border-success">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">Total Pago</h5>
                </div>
                <div class="card-body">
                    <h3 class="text-success">R$ {{ total_pago|floatformat:2 }}</h3>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card border-warning">
                <div class="card-header bg-warning text-dark">
                    <h5 class="mb-0">Total Pendente</h5>
                </div>
                <div class="card-body">
                    <h3 class="text-warning">R$ {{ total_pendente|floatformat:2 }}</h3>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card border-danger">
                <div class="card-header bg-danger text-white">
                    <h5 class="mb-0">Total Atrasado</h5>
                </div>
                <div class="card-body">
                    <h3 class="text-danger">R$ {{ total_atrasado|floatformat:2 }}</h3>
                </div>
            </div>
        </div>
    </div>

    <!-- Links para dashboards específicos -->
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Dashboards Específicos</h5>
                </div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <a href="{% url 'pagamentos:dashboard_pagamentos' %}" class="btn btn-outline-primary">
                            <i class="fas fa-chart-line"></i> Dashboard de Pagamentos
                        </a>
                        <a href="{% url 'pagamentos:dashboard_financeiro' %}" class="btn btn-outline-success">
                            <i class="fas fa-money-bill-wave"></i> Dashboard Financeiro
                        </a>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">Relatórios</h5>
                </div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <a href="{% url 'pagamentos:exportar_pagamentos_pdf' %}" class="btn btn-outline-danger">
                            <i class="fas fa-file-pdf"></i> Exportar Pagamentos (PDF)
                        </a>
                        <a href="{% url 'pagamentos:relatorio_financeiro' %}" class="btn btn-outline-info">
                            <i class="fas fa-chart-pie"></i> Relatório Financeiro
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <!-- Pagamentos recentes -->
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">Pagamentos Recentes</h5>
                </div>
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-striped mb-0">
                            <thead>
                                <tr>
                                    <th>Aluno</th>
                                    <th>Valor</th>
                                    <th>Data</th>
                                    <th>Ações</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for pagamento in pagamentos_recentes %}
                                <tr>
                                    <td>{{ pagamento.aluno.nome }}</td>
                                    <td>R$ {{ pagamento.valor_pago|default:pagamento.valor|floatformat:2 }}</td>
                                    <td>{{ pagamento.data_pagamento|date:"d/m/Y" }}</td>
                                    <td>
                                        <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i>
                                        </a>
                                    </td>
                                </tr>
                                {% empty %}
                                <tr>
                                    <td colspan="4" class="text-center">Nenhum pagamento recente encontrado.</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="card-footer">
                    <a href="{% url 'pagamentos:listar_pagamentos' %}?status=PAGO" class="btn btn-sm btn-outline-success">Ver todos os pagamentos</a>
                </div>
            </div>
        </div>

        <!-- Pagamentos próximos -->
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header bg-warning text-dark">
                    <h5 class="mb-0">Pagamentos Próximos (7 dias)</h5>
                </div>
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-striped mb-0">
                            <thead>
                                <tr>
                                    <th>Aluno</th>
                                    <th>Valor</th>
                                    <th>Vencimento</th>
                                    <th>Ações</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for pagamento in pagamentos_proximos %}
                                <tr>
                                    <td>{{ pagamento.aluno.nome }}</td>
                                    <td>R$ {{ pagamento.valor|floatformat:2 }}</td>
                                    <td>{{ pagamento.data_vencimento|date:"d/m/Y" }}</td>
                                    <td>
                                        <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i>
                                        </a>
                                    </td>
                                </tr>
                                {% empty %}
                                <tr>
                                    <td colspan="4" class="text-center">Nenhum pagamento próximo encontrado.</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="card-footer">
                    <a href="{% url 'pagamentos:listar_pagamentos' %}?status=PENDENTE" class="btn btn-sm btn-outline-warning">Ver todos os pagamentos pendentes</a>
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
        // Gráfico de pagamentos por mês
        const ctxMes = document.getElementById('pagamentosPorMes').getContext('2d');
        new Chart(ctxMes, {
            type: 'bar',
            data: {
                labels: [{% for item in pagamentos_por_mes %}'{{ item.mes }}',{% endfor %}],
                datasets: [{
                    label: 'Valor Total',
                    data: [{% for item in pagamentos_por_mes %}{{ item.total }},{% endfor %}],
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgb(54, 162, 235)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return 'R$ ' + value.toFixed(2);
                            }
                        }
                    }
                }
            }
        });
        
        // Gráfico de pagamentos por status
        const ctxStatus = document.getElementById('pagamentosPorStatus').getContext('2d');
        new Chart(ctxStatus, {
            type: 'pie',
            data: {
                labels: ['Pago', 'Pendente', 'Cancelado'],
                datasets: [{
                    data: [{{ total_pago }}, {{ total_pendente }}, {{ total_cancelado }}],
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(255, 205, 86, 0.6)',
                        'rgba(201, 203, 207, 0.6)'
                    ],
                    borderColor: [
                        'rgb(75, 192, 192)',
                        'rgb(255, 205, 86)',
                        'rgb(201, 203, 207)'
                    ],
                    borderWidth: 1
                }]
            }
        });
    });
</script>
{% endblock %}



### Arquivo: pagamentos\templates\pagamentos\dashboard_financeiro.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Dashboard Financeiro{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.css">
{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Cabeçalho com botões de ação -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Dashboard Financeiro</h1>
        <div>
            <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary me-2">
                <i class="fas fa-list"></i> Lista de Pagamentos
            </a>
            <a href="{% url 'pagamentos:criar_pagamento' %}" class="btn btn-success">
                <i class="fas fa-plus"></i> Novo Pagamento
            </a>
        </div>
    </div>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-4">
                    <label for="ano" class="form-label">Ano</label>
                    <select class="form-select" id="ano" name="ano">
                        {% for ano_opcao in anos_disponiveis %}
                        <option value="{{ ano_opcao }}" {% if ano_opcao == ano_selecionado %}selected{% endif %}>{{ ano_opcao }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-4">
                    <label for="curso" class="form-label">Curso</label>
                    <select class="form-select" id="curso" name="curso">
                        <option value="">Todos os cursos</option>
                        {% for curso in cursos %}
                        <option value="{{ curso.id }}" {% if curso.id|stringformat:"s" == filtros.curso %}selected{% endif %}>{{ curso.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-4">
                    <label for="tipo" class="form-label">Tipo de Pagamento</label>
                    <select class="form-select" id="tipo" name="tipo">
                        <option value="">Todos os tipos</option>
                        <option value="MENSALIDADE" {% if filtros.tipo == 'MENSALIDADE' %}selected{% endif %}>Mensalidade</option>
                        <option value="MATRICULA" {% if filtros.tipo == 'MATRICULA' %}selected{% endif %}>Matrícula</option>
                        <option value="MATERIAL" {% if filtros.tipo == 'MATERIAL' %}selected{% endif %}>Material</option>
                        <option value="OUTRO" {% if filtros.tipo == 'OUTRO' %}selected{% endif %}>Outro</option>
                    </select>
                </div>
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                    <a href="{% url 'pagamentos:dashboard' %}" class="btn btn-secondary">
                        <i class="fas fa-undo"></i> Limpar Filtros
                    </a>
                    <a href="{% url 'pagamentos:exportar_relatorio_pdf' %}{{ request.GET.urlencode }}" class="btn btn-danger float-end">
                        <i class="fas fa-file-pdf"></i> Exportar Relatório
                    </a>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Resumo financeiro -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card bg-success text-white h-100">
                <div class="card-body">
                    <h5 class="card-title">Receita Total</h5>
                    <h2>R$ {{ resumo.receita_total|floatformat:2 }}</h2>
                    <p class="mb-0">{{ resumo.total_pagos }} pagamentos</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-warning text-dark h-100">
                <div class="card-body">
                    <h5 class="card-title">Pendente</h5>
                    <h2>R$ {{ resumo.valor_pendente|floatformat:2 }}</h2>
                    <p class="mb-0">{{ resumo.total_pendentes }} pagamentos</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-danger text-white h-100">
                <div class="card-body">
                    <h5 class="card-title">Atrasado</h5>
                    <h2>R$ {{ resumo.valor_atrasado|floatformat:2 }}</h2>
                    <p class="mb-0">{{ resumo.total_atrasados }} pagamentos</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-info text-white h-100">
                <div class="card-body">
                    <h5 class="card-title">Previsão Mensal</h5>
                    <h2>R$ {{ resumo.previsao_mensal|floatformat:2 }}</h2>
                    <p class="mb-0">Média dos últimos 3 meses</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Gráficos financeiros -->
    <div class="row">
        <!-- Gráfico de receita mensal -->
        <div class="col-md-8">
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Receita Mensal ({{ ano_selecionado }})</h5>
                </div>
                <div class="card-body">
                    <canvas id="graficoReceitaMensal" height="300"></canvas>
                </div>
            </div>
        </div>
        
        <!-- Gráfico de distribuição por status -->
        <div class="col-md-4">
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Distribuição por Status</h5>
                </div>
                <div class="card-body">
                    <canvas id="graficoDistribuicaoStatus" height="300"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row">
        <!-- Gráfico de distribuição por tipo -->
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Distribuição por Tipo</h5>
                </div>
                <div class="card-body">
                    <canvas id="graficoDistribuicaoTipo" height="300"></canvas>
                </div>
            </div>
        </div>
        
        <!-- Gráfico de distribuição por curso -->
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Distribuição por Curso</h5>
                </div>
                <div class="card-body">
                    <canvas id="graficoDistribuicaoCurso" height="300"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Pagamentos recentes -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Pagamentos Recentes</h5>
        </div>
        <div class="card-body">
            {% if pagamentos_recentes %}
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Data</th>
                            <th>Aluno</th>
                            <th>Descrição</th>
                            <th>Valor</th>
                            <th>Status</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for pagamento in pagamentos_recentes %}
                        <tr>
                            <td>{{ pagamento.data_vencimento|date:"d/m/Y" }}</td>
                            <td>{{ pagamento.aluno.nome }}</td>
                            <td>{{ pagamento.descricao|truncatechars:30 }}</td>
                            <td>R$ {{ pagamento.valor|floatformat:2 }}</td>
                            <td>
                                <span class="badge 
                                    {% if pagamento.status == 'PAGO' %}bg-success
                                    {% elif pagamento.status == 'PENDENTE' %}bg-warning
                                    {% elif pagamento.status == 'ATRASADO' %}bg-danger
                                    {% else %}bg-secondary{% endif %}">
                                    {{ pagamento.get_status_display }}
                                </span>
                            </td>
                            <td>
                                <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-sm btn-info">
                                    <i class="fas fa-eye"></i>
                                </a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            <div class="text-end mt-3">
                <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-outline-primary">
                    Ver todos os pagamentos
                </a>
            </div>
            {% else %}
            <div class="alert alert-info">
                <i class="fas fa-info-circle"></i> Não há pagamentos recentes para exibir.
            </div>
            {% endif %}
        </div>
    </div>
    
    <!-- Pagamentos atrasados -->
    <div class="card mb-4">
        <div class="card-header bg-danger text-white">
            <h5 class="mb-0">Pagamentos Atrasados</h5>
        </div>
        <div class="card-body">
            {% if pagamentos_atrasados %}
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Vencimento</th>
                            <th>Aluno</th>
                            <th>Descrição</th>
                            <th>Valor</th>
                            <th>Dias Atrasados</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for pagamento in pagamentos_atrasados %}
                        <tr>
                            <td>{{ pagamento.data_vencimento|date:"d/m/Y" }}</td>
                            <td>{{ pagamento.aluno.nome }}</td>
                            <td>{{ pagamento.descricao|truncatechars:30 }}</td>
                            <td>R$ {{ pagamento.valor|floatformat:2 }}</td>
                            <td>{{ pagamento.dias_atrasados }}</td>
                            <td>
                                <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-sm btn-info">
                                    <i class="fas fa-eye"></i>
                                </a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="alert alert-info">
                <i class="fas fa-info-circle"></i> Não há pagamentos atrasados para exibir.
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.js"></script>
<script>
    // Gráfico de receita mensal
    const ctxReceita = document.getElementById('graficoReceitaMensal').getContext('2d');
    const graficoReceitaMensal = new Chart(ctxReceita, {
        type: 'bar',
        data: {
            labels: {{ meses|safe }},
            datasets: [{
                label: 'Receita Mensal (R$)',
                data: {{ valores_mensais|safe }},
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
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
                    text: 'Receita Mensal do Ano de {{ ano_selecionado }}'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return 'R$ ' + value.toFixed(2);
                        }
                    }
                }
            }
        }
    });

    // Gráfico de distribuição por status
    const ctxStatus = document.getElementById('graficoDistribuicaoStatus').getContext('2d');
    const graficoDistribuicaoStatus = new Chart(ctxStatus, {
        type: 'pie',
        data: {
            labels: ['Pago', 'Pendente', 'Atrasado'],
            datasets: [{
                data: [{{ resumo.total_pagos }}, {{ resumo.total_pendentes }}, {{ resumo.total_atrasados }}],
                backgroundColor: [
                    'rgba(40, 167, 69, 0.7)',
                    'rgba(255, 193, 7, 0.7)',
                    'rgba(220, 53, 69, 0.7)'
                ],
                borderColor: [
                    'rgba(40, 167, 69, 1)',
                    'rgba(255, 193, 7, 1)',
                    'rgba(220, 53, 69, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: 'Distribuição de Pagamentos por Status'
                }
            }
        }
    });

    // Gráfico de distribuição por tipo
    const ctxTipo = document.getElementById('graficoDistribuicaoTipo').getContext('2d');
    const graficoDistribuicaoTipo = new Chart(ctxTipo, {
        type: 'pie',
        data: {
            labels: ['Mensalidade', 'Matrícula', 'Material', 'Outro'],
            datasets: [{
                data: [{{ resumo.mensalidades }}, {{ resumo.matriculas }}, {{ resumo.materiais }}, {{ resumo.outros }}],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: 'Distribuição de Pagamentos por Tipo'
                }
            }
        }
    });

    // Gráfico de distribuição por curso
    const ctxCurso = document.getElementById('graficoDistribuicaoCurso').getContext('2d');
    const graficoDistribuicaoCurso = new Chart(ctxCurso, {
        type: 'pie',
        data: {
            labels: {{ cursos_nomes|safe }},
            datasets: [{
                data: {{ cursos_valores|safe }},
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(153, 102, 255, 0.7)',
                    'rgba(255, 159, 64, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: 'Distribuição de Pagamentos por Curso'
                }
            }
        }
    });
</script>
{% endblock %}




### Arquivo: pagamentos\templates\pagamentos\dashboard_pagamentos.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Dashboard de Pagamentos{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.css">
{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Dashboard de Pagamentos</h1>
        <div>
            <a href="{% url 'pagamentos:dashboard' %}" class="btn btn-secondary me-2">
                <i class="fas fa-tachometer-alt"></i> Dashboard Principal
            </a>
            <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-primary">
                <i class="fas fa-list"></i> Listar Pagamentos
            </a>
        </div>
    </div>

    <!-- Estatísticas do mês atual -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Estatísticas do Mês ({{ mes_atual }})</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-4">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Pagamentos Pagos</h5>
                            <p class="card-text display-4 text-success">{{ pagos_mes }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Pagamentos Pendentes</h5>
                            <p class="card-text display-4 text-warning">{{ pendentes_mes }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Pagamentos Atrasados</h5>
                            <p class="card-text display-4 text-danger">{{ atrasados_mes }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row mt-3">
                <div class="col-md-4">
                    <div class="card border-success">
                        <div class="card-header bg-success text-white">
                            <h5 class="mb-0">Valor Pago</h5>
                        </div>
                        <div class="card-body">
                            <h3 class="text-success">R$ {{ valor_pago_mes|floatformat:2 }}</h3>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card border-warning">
                        <div class="card-header bg-warning text-dark">
                            <h5 class="mb-0">Valor Pendente</h5>
                        </div>
                        <div class="card-body">
                            <h3 class="text-warning">R$ {{ valor_pendente_mes|floatformat:2 }}</h3>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card border-danger">
                        <div class="card-header bg-danger text-white">
                            <h5 class="mb-0">Valor Atrasado</h5>
                        </div>
                        <div class="card-body">
                            <h3 class="text-danger">R$ {{ valor_atrasado_mes|floatformat:2 }}</h3>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Resumo estatístico -->
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="card bg-primary text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Total de Pagamentos</h5>
                    <p class="card-text display-6">{{ total_pagamentos }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card bg-success text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Valor Total</h5>
                    <p class="card-text display-6">R$ {{ valor_total|floatformat:2 }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Pagamentos por status -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Pagamentos por Status</h5>
        </div>
        <div class="card-body">
            {% if pagamentos_por_status %}
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Status</th>
                                <th>Quantidade</th>
                                <th>Valor Total</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for item in pagamentos_por_status %}
                                <tr>
                                    <td>
                                        <span class="badge {% if item.status == 'pago' %}bg-success{% elif item.status == 'pendente' %}bg-warning{% else %}bg-danger{% endif %}">
                                            {% if item.status == 'pago' %}Pago{% elif item.status == 'pendente' %}Pendente{% else %}Cancelado{% endif %}
                                        </span>
                                    </td>
                                    <td>{{ item.total }}</td>
                                    <td>R$ {{ item.valor_total|floatformat:2 }}</td>
                                    <td>
                                        <a href="{% url 'pagamentos:listar_pagamentos' %}?status={{ item.status }}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i> Ver Pagamentos
                                        </a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> Nenhum pagamento encontrado.
                </div>
            {% endif %}
        </div>
    </div>
    
    <!-- Pagamentos por mês -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Pagamentos por Mês (Últimos 6 meses)</h5>
        </div>
        <div class="card-body">
            {% if pagamentos_por_mes %}
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Mês</th>
                                <th>Quantidade</th>
                                <th>Valor Total</th>
                                <th>Média por Pagamento</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for item in pagamentos_por_mes %}
                                <tr>
                                    <td>{{ item.mes }}</td>
                                    <td>{{ item.total }}</td>
                                    <td>R$ {{ item.valor_total|floatformat:2 }}</td>
                                    <td>
                                        {% if item.total > 0 %}
                                            R$ {{ item.valor_total|floatformat:2|default:0|divisibleby:item.total }}
                                        {% else %}
                                            R$ 0,00
                                        {% endif %}
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> Nenhum pagamento encontrado nos últimos 6 meses.
                </div>
            {% endif %}
        </div>
    </div>

    <!-- Pagamentos por aluno -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Top 5 Alunos por Valor Total</h5>
        </div>
        <div class="card-body">
            {% if pagamentos_por_aluno %}
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Aluno</th>
                                <th>Quantidade de Pagamentos</th>
                                <th>Valor Total</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for item in pagamentos_por_aluno %}
                                <tr>
                                    <td>{{ item.aluno__nome }}</td>
                                    <td>{{ item.total }}</td>
                                    <td>R$ {{ item.valor_total|floatformat:2 }}</td>
                                    <td>
                                        <a href="{% url 'pagamentos:listar_pagamentos' %}?aluno={{ item.aluno__cpf }}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i> Ver Pagamentos
                                        </a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> Nenhum pagamento encontrado.
                </div>
            {% endif %}
        </div>
    </div>

    <!-- Gráficos -->
    <div class="row">
        <!-- Gráfico de pagamentos por dia -->
        <div class="col-md-8">
            <div class="card mb-4">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">Pagamentos por Dia ({{ mes_atual }})</h5>
                </div>
                <div class="card-body">
                    <canvas id="grafico-pagamentos-dia" height="300"></canvas>
                </div>
            </div>
        </div>

        <!-- Gráfico de métodos de pagamento -->
        <div class="col-md-4">
            <div class="card mb-4">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">Métodos de Pagamento</h5>
                </div>
                <div class="card-body">
                    <canvas id="grafico-metodos-pagamento" height="300"></canvas>
                </div>
            </div>
        </div>
    </div>

    <!-- Pagamentos atrasados por faixa -->
    <div class="card mb-4">
        <div class="card-header bg-danger text-white">
            <h5 class="mb-0">Pagamentos Atrasados por Faixa</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-4">
                    <div class="card text-center">
                        <div class="card-body">
                            <h5 class="card-title">Até 15 dias</h5>
                            <p class="card-text display-4 text-warning">{{ atrasados_ate_15 }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center">
                        <div class="card-body">
                            <h5 class="card-title">15 a 30 dias</h5>
                            <p class="card-text display-4 text-danger">{{ atrasados_15_30 }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center">
                        <div class="card-body">
                            <h5 class="card-title">Mais de 30 dias</h5>
                            <p class="card-text display-4 text-danger">{{ atrasados_mais_30 }}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="mt-3 text-center">
                <a href="{% url 'pagamentos:listar_pagamentos' %}?status=ATRASADO" class="btn btn-outline-danger">
                    <i class="fas fa-exclamation-triangle"></i> Ver Todos os Pagamentos Atrasados
                </a>
            </div>
        </div>
    </div>

    <div class="mt-4">
        <a href="javascript:history.back()" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.js"></script>
<script>
    // Gráfico de pagamentos por dia
    const ctxDia = document.getElementById('grafico-pagamentos-dia').getContext('2d');
    const graficoPagamentosDia = new Chart(ctxDia, {
        type: 'line',
        data: {
            labels: {{ dias|safe }},
            datasets: [{
                label: 'Valor Pago (R$)',
                data: {{ valores_por_dia|safe }},
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 2,
                tension: 0.1
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
                    text: 'Pagamentos Recebidos por Dia'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return 'R$ ' + value.toFixed(2);
                        }
                    }
                }
            }
        }
    });

    // Gráfico de métodos de pagamento
    const ctxMetodos = document.getElementById('grafico-metodos-pagamento').getContext('2d');
    const graficoMetodosPagamento = new Chart(ctxMetodos, {
        type: 'doughnut',
        data: {
            labels: {{ metodos|safe }},
            datasets: [{
                data: {{ contagens|safe }},
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(153, 102, 255, 0.7)',
                    'rgba(255, 159, 64, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: 'Métodos de Pagamento'
                }
            }
        }
    });
</script>
{% endblock %}



### Arquivo: pagamentos\templates\pagamentos\detalhar_pagamento.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Detalhes do Pagamento{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Detalhes do Pagamento</h1>
        <div>
            <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'pagamentos:editar_pagamento' pagamento.id %}" class="btn btn-warning">
                <i class="fas fa-edit"></i> Editar
            </a>
            <a href="{% url 'pagamentos:excluir_pagamento' pagamento.id %}" class="btn btn-danger">
                <i class="fas fa-trash"></i> Excluir
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
        <div class="card-header">
            <h5 class="mb-0">Informações do Pagamento</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <h6>Aluno</h6>
                    <p>
                        <a href="{% url 'alunos:detalhar_aluno' pagamento.aluno.cpf %}">
                            {{ pagamento.aluno.nome }}
                        </a>
                    </p>
                    
                    <h6>Valor</h6>
                    <p>R$ {{ pagamento.valor|floatformat:2 }}</p>
                    
                    <h6>Data de Vencimento</h6>
                    <p>{{ pagamento.data_vencimento|date:"d/m/Y" }}</p>
                    
                    <h6>Descrição</h6>
                    <p>{{ pagamento.descricao }}</p>
                    
                    <h6>Tipo</h6>
                    <p>{{ pagamento.get_tipo_display }}</p>
                </div>
                <div class="col-md-6">
                    <h6>Status</h6>
                    <p>
                        {% if pagamento.status == 'PAGO' %}
                            <span class="badge bg-success">{{ pagamento.get_status_display }}</span>
                        {% elif pagamento.status == 'PENDENTE' %}
                            <span class="badge bg-warning">{{ pagamento.get_status_display }}</span>
                        {% elif pagamento.status == 'ATRASADO' %}
                            <span class="badge bg-danger">{{ pagamento.get_status_display }}</span>
                        {% else %}
                            <span class="badge bg-secondary">{{ pagamento.get_status_display }}</span>
                        {% endif %}
                    </p>
                    
                    {% if pagamento.status == 'PAGO' %}
                        <h6>Data de Pagamento</h6>
                        <p>{{ pagamento.data_pagamento|date:"d/m/Y" }}</p>
                        
                        <h6>Valor Pago</h6>
                        <p>R$ {{ pagamento.valor_pago|floatformat:2 }}</p>
                        
                        <h6>Método de Pagamento</h6>
                        <p>{{ pagamento.get_metodo_pagamento_display }}</p>
                        
                        {% if pagamento.comprovante %}
                            <h6>Comprovante</h6>
                            <p>
                                <a href="{{ pagamento.comprovante.url }}" target="_blank" class="btn btn-sm btn-info">
                                    <i class="fas fa-file-download"></i> Visualizar Comprovante
                                </a>
                            </p>
                        {% endif %}
                    {% else %}
                        <div class="alert alert-info">
                            <h6 class="mb-2">Ações Disponíveis</h6>
                            <a href="{% url 'pagamentos:registrar_pagamento' pagamento.id %}" class="btn btn-success">
                                <i class="fas fa-check-circle"></i> Registrar Pagamento
                            </a>
                        </div>
                    {% endif %}
                </div>
            </div>
            
            {% if pagamento.observacoes %}
                <div class="mt-3">
                    <h6>Observações</h6>
                    <div class="p-3 bg-light rounded">
                        {{ pagamento.observacoes|linebreaks }}
                    </div>
                </div>
            {% endif %}
            
            {% if pagamento.matricula %}
                <div class="mt-3">
                    <h6>Matrícula Associada</h6>
                    <div class="p-3 bg-light rounded">
                        <p><strong>Curso:</strong> {{ pagamento.matricula.turma.curso.nome }}</p>
                        <p><strong>Turma:</strong> {{ pagamento.matricula.turma.nome }}</p>
                        {% if pagamento.numero_parcela %}
                            <p><strong>Parcela:</strong> {{ pagamento.numero_parcela }} de {{ pagamento.total_parcelas }}</p>
                        {% endif %}
                    </div>
                </div>
            {% endif %}
        </div>
        <div class="card-footer text-muted">
            <small>Criado em: {{ pagamento.created_at|date:"d/m/Y H:i" }}</small>
            <br>
            <small>Última atualização: {{ pagamento.updated_at|date:"d/m/Y H:i" }}</small>
        </div>
    </div>
    
    {% if pagamentos_relacionados %}
        <div class="card mb-4">
            <div class="card-header">
                <h5 class="mb-0">Pagamentos Relacionados</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Descrição</th>
                                <th>Valor</th>
                                <th>Vencimento</th>
                                <th>Status</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for pag in pagamentos_relacionados %}
                                <tr>
                                    <td>
                                        {{ pag.descricao }}
                                        {% if pag.numero_parcela %}
                                            <br><small>Parcela {{ pag.numero_parcela }}/{{ pag.total_parcelas }}</small>
                                        {% endif %}
                                    </td>
                                    <td>R$ {{ pag.valor|floatformat:2 }}</td>
                                    <td>{{ pag.data_vencimento|date:"d/m/Y" }}</td>
                                    <td>
                                        {% if pag.status == 'PAGO' %}
                                            <span class="badge bg-success">Pago</span>
                                            {% if pag.data_pagamento %}
                                                <br><small>em {{ pag.data_pagamento|date:"d/m/Y" }}</small>
                                            {% endif %}
                                        {% elif pag.status == 'PENDENTE' %}
                                            <span class="badge bg-warning text-dark">Pendente</span>
                                        {% elif pag.status == 'ATRASADO' %}
                                            <span class="badge bg-danger">Atrasado</span>
                                        {% elif pag.status == 'CANCELADO' %}
                                            <span class="badge bg-secondary">Cancelado</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        <a href="{% url 'pagamentos:detalhar_pagamento' pag.id %}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i>
                                        </a>
                                        {% if pag.status == 'PENDENTE' or pag.status == 'ATRASADO' %}
                                            <a href="{% url 'pagamentos:registrar_pagamento' pag.id %}" class="btn btn-sm btn-success">
                                                <i class="fas fa-check"></i>
                                            </a>
                                        {% endif %}
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    {% endif %}
    
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">Histórico de Alterações</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Data</th>
                            <th>Usuário</th>
                            <th>Ação</th>
                            <th>Detalhes</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for log in historico %}
                            <tr>
                                <td>{{ log.timestamp|date:"d/m/Y H:i" }}</td>
                                <td>{{ log.usuario.username }}</td>
                                <td>{{ log.get_acao_display }}</td>
                                <td>{{ log.detalhes }}</td>
                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="4" class="text-center">Nenhum registro de alteração encontrado.</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: pagamentos\templates\pagamentos\editar_pagamento.html

html
{% extends 'base.html' %}

{% block title %}Editar Pagamento{% endblock %}

{% block content %}
<style>
@keyframes piscarBorda {
    0%   { box-shadow: 0 0 0 0 red; }
    50%  { box-shadow: 0 0 8px 2px red; }
    100% { box-shadow: 0 0 0 0 red; }
}
.piscar-erro {
    animation: piscarBorda 0.8s linear 2;
}
</style>
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Editar Pagamento</h1>
        <div>
            <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar
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
    
    <div class="row">
        <div class="col-md-8">
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Dados do Pagamento</h5>
                </div>
                <div class="card-body">
                    <form method="post" enctype="multipart/form-data" id="pagamento-form" novalidate>
                        {% csrf_token %}
                        {% if form.non_field_errors %}
                            <div class="alert alert-danger">
                                {% for error in form.non_field_errors %}
                                    <div>{{ error }}</div>
                                {% endfor %}
                            </div>
                        {% endif %}

                        <div class="mb-3">
                            <label class="form-label">Aluno</label>
                            <div class="input-group">
                                <div class="alert alert-info d-flex align-items-center w-100 mb-0">
                                    {% if pagamento.aluno.foto %}
                                        <img src="{{ pagamento.aluno.foto.url }}" alt="Foto de {{ pagamento.aluno.nome }}" 
                                             class="rounded-circle me-3" width="40" height="40" style="object-fit: cover;">
                                    {% else %}
                                        <div class="rounded-circle bg-secondary d-flex align-items-center justify-content-center me-3" 
                                             style="width: 40px; height: 40px; color: white;">
                                            {{ pagamento.aluno.nome|first|upper }}
                                        </div>
                                    {% endif %}
                                    <div>
                                        <strong>{{ pagamento.aluno.nome }}</strong>
                                        <br>
                                        <small>CPF: {{ pagamento.aluno.cpf }}</small>
                                    </div>
                                    <a href="{% url 'alunos:detalhar_aluno' pagamento.aluno.cpf %}" class="btn btn-sm btn-outline-primary ms-auto">
                                        <i class="fas fa-user"></i> Ver Perfil
                                    </a>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="id_valor" class="form-label">Valor (R$) <span class="text-danger">*</span></label>
                                    <input type="number" name="valor" step="0.01" required id="id_valor"
                                           class="form-control{% if form.valor.errors %} is-invalid piscar-erro{% endif %}"
                                           value="{{ form.valor.value|default_if_none:'' }}" placeholder="Ex: 100.00">
                                    {% for error in form.valor.errors %}
                                        <div class="invalid-feedback">{{ error }}</div>
                                    {% endfor %}
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="id_data_vencimento" class="form-label">Data de Vencimento <span class="text-danger">*</span></label>
                                    <input type="date" name="data_vencimento" required id="id_data_vencimento"
                                           class="form-control{% if form.data_vencimento.errors %} is-invalid piscar-erro{% endif %}"
                                           value="{{ form.data_vencimento.value|date:'Y-m-d' }}">
                                    {% for error in form.data_vencimento.errors %}
                                        <div class="invalid-feedback">{{ error }}</div>
                                    {% endfor %}
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label for="id_observacoes" class="form-label">Observações</label>
                            <textarea name="observacoes" cols="40" rows="3" id="id_observacoes"
                                      class="form-control{% if form.observacoes.errors %} is-invalid piscar-erro{% endif %}"
                                      placeholder="Observações adicionais...">{{ form.observacoes.value|default_if_none:'' }}</textarea>
                            {% for error in form.observacoes.errors %}
                                <div class="invalid-feedback">{{ error }}</div>
                            {% endfor %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="id_status" class="form-label">Status <span class="text-danger">*</span></label>
                            <select name="status" id="id_status"
                                    class="form-select{% if form.status.errors %} is-invalid piscar-erro{% endif %}" required>
                                <option value="PENDENTE" {% if form.status.value == 'PENDENTE' %}selected{% endif %}>Pendente</option>
                                <option value="PAGO" {% if form.status.value == 'PAGO' %}selected{% endif %}>Pago</option>
                                <option value="ATRASADO" {% if form.status.value == 'ATRASADO' %}selected{% endif %}>Atrasado</option>
                                <option value="CANCELADO" {% if form.status.value == 'CANCELADO' %}selected{% endif %}>Cancelado</option>
                            </select>
                            {% for error in form.status.errors %}
                                <div class="invalid-feedback">{{ error }}</div>
                            {% endfor %}
                        </div>
                        
                        <div class="mb-3 metodo-pagamento-container" style="display: none;">
                            <label for="id_metodo_pagamento" class="form-label">Método de Pagamento</label>
                            <select name="metodo_pagamento" id="id_metodo_pagamento"
                                    class="form-select{% if form.metodo_pagamento.errors %} is-invalid piscar-erro{% endif %}">
                                <option value="">Selecione um método</option>
                                <option value="DINHEIRO" {% if form.metodo_pagamento.value == 'DINHEIRO' %}selected{% endif %}>Dinheiro</option>
                                <option value="CARTAO_CREDITO" {% if form.metodo_pagamento.value == 'CARTAO_CREDITO' %}selected{% endif %}>Cartão de Crédito</option>
                                <option value="CARTAO_DEBITO" {% if form.metodo_pagamento.value == 'CARTAO_DEBITO' %}selected{% endif %}>Cartão de Débito</option>
                                <option value="BOLETO" {% if form.metodo_pagamento.value == 'BOLETO' %}selected{% endif %}>Boleto Bancário</option>
                                <option value="TRANSFERENCIA" {% if form.metodo_pagamento.value == 'TRANSFERENCIA' %}selected{% endif %}>Transferência</option>
                                <option value="PIX" {% if form.metodo_pagamento.value == 'PIX' %}selected{% endif %}>PIX</option>
                                <option value="OUTRO" {% if form.metodo_pagamento.value == 'OUTRO' %}selected{% endif %}>Outro</option>
                            </select>
                            {% for error in form.metodo_pagamento.errors %}
                                <div class="invalid-feedback">{{ error }}</div>
                            {% endfor %}
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3 data-pagamento-container" style="display: none;">
                                    <label for="id_data_pagamento" class="form-label">Data de Pagamento</label>
                                    <input type="date" name="data_pagamento" id="id_data_pagamento"
                                           class="form-control{% if form.data_pagamento.errors %} is-invalid piscar-erro{% endif %}"
                                           value="{{ form.data_pagamento.value|date:'Y-m-d' }}">
                                    {% for error in form.data_pagamento.errors %}
                                        <div class="invalid-feedback">{{ error }}</div>
                                    {% endfor %}
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3 valor-pago-container" style="display: none;">
                                    <label for="id_valor_pago" class="form-label">Valor Pago (R$)</label>
                                    <input type="number" name="valor_pago" id="id_valor_pago"
                                           class="form-control{% if form.valor_pago.errors %} is-invalid piscar-erro{% endif %}"
                                           step="0.01" min="0" value="{{ form.valor_pago.value|default_if_none:'' }}">
                                    {% for error in form.valor_pago.errors %}
                                        <div class="invalid-feedback">{{ error }}</div>
                                    {% endfor %}
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label for="id_comprovante" class="form-label">Comprovante de Pagamento</label>
                            <input type="file" name="comprovante" id="id_comprovante"
                                   class="form-control{% if form.comprovante.errors %} is-invalid piscar-erro{% endif %}">
                            <div class="form-text">Formatos aceitos: PDF, JPG, PNG. Tamanho máximo: 5MB</div>
                            {% for error in form.comprovante.errors %}
                                <div class="invalid-feedback">{{ error }}</div>
                            {% endfor %}
                        </div>
                        
                        <div class="d-flex justify-content-between">
                            <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-secondary">
                                <i class="fas fa-times"></i> Cancelar
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Salvar Alterações
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
                    <p>Você está editando um pagamento existente.</p>
                    <p>Se alterar o status para "Pago", informe também a data de pagamento e o método utilizado.</p>
                    
                    <div class="alert alert-warning mt-3">
                        <i class="fas fa-exclamation-triangle"></i> Não é possível alterar o aluno associado ao pagamento.
                    </div>
                </div>
            </div>
            
            {% if pagamento.matricula %}
            <div class="card mb-4">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">Dados da Matrícula</h5>
                </div>
                <div class="card-body">
                    <p><strong>Curso:</strong> {{ pagamento.matricula.turma.curso.nome }}</p>
                    <p><strong>Turma:</strong> {{ pagamento.matricula.turma.nome }}</p>
                    {% if pagamento.numero_parcela %}
                        <p><strong>Parcela:</strong> {{ pagamento.numero_parcela }}/{{ pagamento.total_parcelas }}</p>
                    {% endif %}
                    
                    <a href="{% url 'matriculas:detalhar_matricula' pagamento.matricula.id %}" class="btn btn-sm btn-outline-success">
                        <i class="fas fa-graduation-cap"></i> Ver Matrícula
                    </a>
                </div>
            </div>
            {% endif %}
            
            <div class="card mb-4">
                <div class="card-header bg-secondary text-white">
                    <h5 class="mb-0">Histórico</h5>
                </div>
                <div class="card-body">
                    <p><strong>Criado em:</strong> {{ pagamento.created_at|date:"d/m/Y H:i" }}</p>
                    <p><strong>Última atualização:</strong> {{ pagamento.updated_at|date:"d/m/Y H:i" }}</p>
                    
                    {% if pagamento.status == 'PAGO' %}
                        <div class="alert alert-success">
                            <i class="fas fa-check-circle"></i> Este pagamento foi registrado como pago em {{ pagamento.data_pagamento|date:"d/m/Y" }}.
                        </div>
                    {% elif pagamento.status == 'ATRASADO' %}
                        <div class="alert alert-danger">
                            <i class="fas fa-exclamation-circle"></i> Este pagamento está atrasado há {{ pagamento.dias_atraso }} dias.
                        </div>
                    {% elif pagamento.status == 'CANCELADO' %}
                        <div class="alert alert-secondary">
                            <i class="fas fa-ban"></i> Este pagamento foi cancelado.
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const statusSelect = document.getElementById('id_status');
        const dataPagamentoContainer = document.querySelector('.data-pagamento-container');
        const valorPagoContainer = document.querySelector('.valor-pago-container');
        const metodoPagamentoContainer = document.querySelector('.metodo-pagamento-container');
        
        // Função para mostrar/ocultar campos dependendo do status
        function toggleFields() {
            if (statusSelect.value === 'PAGO') {
                dataPagamentoContainer.style.display = 'block';
                valorPagoContainer.style.display = 'block';
                metodoPagamentoContainer.style.display = 'block';
                document.getElementById('id_data_pagamento').required = true;
                document.getElementById('id_valor_pago').required = true;
                
                // Se não houver data de pagamento, definir para hoje
                const dataPagamentoInput = document.getElementById('id_data_pagamento');
                if (!dataPagamentoInput.value) {
                    const hoje = new Date();
                    const ano = hoje.getFullYear();
                    const mes = String(hoje.getMonth() + 1).padStart(2, '0');
                    const dia = String(hoje.getDate()).padStart(2, '0');
                    dataPagamentoInput.value = `${ano}-${mes}-${dia}`;
                }
                
                // Se não houver valor pago, usar o valor original
                const valorPagoInput = document.getElementById('id_valor_pago');
                if (!valorPagoInput.value) {
                    valorPagoInput.value = document.getElementById('id_valor').value;
                }
            } else {
                dataPagamentoContainer.style.display = 'none';
                valorPagoContainer.style.display = 'none';
                metodoPagamentoContainer.style.display = 'none';
                document.getElementById('id_data_pagamento').required = false;
                document.getElementById('id_valor_pago').required = false;
            }
        }
        
        // Executar ao carregar a página
        toggleFields();
        
        // Adicionar evento de mudança
        statusSelect.addEventListener('change', toggleFields);
    });
</script>
{% endblock %}



### Arquivo: pagamentos\templates\pagamentos\excluir_pagamento.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Excluir Pagamento{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-7">
            <div class="card border-danger">
                <div class="card-header bg-danger text-white">
                    <h5 class="mb-0">Confirmar Exclusão de Pagamento</h5>
                </div>
                <div class="card-body">
                    <p>
                        Tem certeza que deseja <strong>excluir</strong> o pagamento do aluno
                        <strong>{{ pagamento.aluno.nome }}</strong>
                        no valor de <strong>R$ {{ pagamento.valor|floatformat:2 }}</strong>
                        com vencimento em <strong>{{ pagamento.data_vencimento|date:"d/m/Y" }}</strong>?
                    </p>
                    <p class="text-danger mb-0"><small>Esta ação não poderá ser desfeita.</small></p>
                </div>
                <div class="card-footer d-flex justify-content-between">
                    <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">
                        <i class="fas fa-arrow-left"></i> Cancelar
                    </a>
                    <form method="post" style="display: inline;">
                        {% csrf_token %}
                        <button type="submit" class="btn btn-danger">
                            <i class="fas fa-trash"></i> Excluir Pagamento
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: pagamentos\templates\pagamentos\exportar_pagamentos.html

html
        # Adicionar cabeçalhos
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.value = header
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
        
        # Adicionar dados
        for row_num, pagamento in enumerate(pagamentos, 2):
            ws.cell(row=row_num, column=1).value = pagamento.id
            ws.cell(row=row_num, column=2).value = pagamento.aluno.nome if pagamento.aluno else "N/A"
            ws.cell(row=row_num, column=3).value = pagamento.valor
            ws.cell(row=row_num, column=3).number_format = '#,##0.00'
            ws.cell(row=row_num, column=4).value = pagamento.data.strftime("%d/%m/%Y") if pagamento.data else "N/A"
            ws.cell(row=row_num, column=5).value = pagamento.get_metodo_pagamento_display() if hasattr(pagamento, 'get_metodo_pagamento_display') else pagamento.metodo_pagamento
            ws.cell(row=row_num, column=6).value = pagamento.get_status_display() if hasattr(pagamento, 'get_status_display') else pagamento.status
            ws.cell(row=row_num, column=7).value = pagamento.descricao
        
        # Ajustar largura das colunas
        for col_num in range(1, len(headers) + 1):
            col_letter = get_column_letter(col_num)
            # Definir uma largura mínima
            ws.column_dimensions[col_letter].width = 15
            
            # Ajustar para o conteúdo mais largo (até um limite razoável)
            max_length = 0
            for row_num in range(1, len(pagamentos) + 2):  # +2 para incluir o cabeçalho
                cell = ws.cell(row=row_num, column=col_num)
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            adjusted_width = min(max_length + 2, 50)  # Limitar a 50 caracteres
            ws.column_dimensions[col_letter].width = adjusted_width
        
        # Salvar o arquivo em um buffer
        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        
        # Configurar a resposta HTTP
        response = HttpResponse(
            buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="pagamentos.xlsx"'
        
        return response
    except Exception as e:
        logger.error(f"Erro ao exportar pagamentos para Excel: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao exportar pagamentos para Excel: {str(e)}")
        return redirect("pagamentos:listar_pagamentos")

@login_required
def exportar_pagamentos_pdf(request):
    """Exporta os dados dos pagamentos para um arquivo PDF."""
    try:
        from django.http import HttpResponse
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        import io
        from datetime import datetime
        
        Pagamento = get_pagamento_model()
        
        # Buscar todos os pagamentos
        pagamentos = Pagamento.objects.all().order_by('-data')
        
        # Criar um buffer para o PDF
        buffer = io.BytesIO()
        
        # Configurar o documento PDF
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(letter),
            title="Relatório de Pagamentos",
            author="Sistema OMAUM"
        )
        
        # Estilos para o PDF
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        
        # Elementos do PDF
        elements = []
        
        # Título
        elements.append(Paragraph("Relatório de Pagamentos", title_style))
        elements.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Dados para a tabela
        data = [["ID", "Aluno", "Valor (R$)", "Data", "Método", "Status", "Descrição"]]
        
        for pagamento in pagamentos:
            data.append([
                str(pagamento.id),
                pagamento.aluno.nome if pagamento.aluno else "N/A",
                f"{pagamento.valor:.2f}",
                pagamento.data.strftime("%d/%m/%Y") if pagamento.data else "N/A",
                pagamento.get_metodo_pagamento_display() if hasattr(pagamento, 'get_metodo_pagamento_display') else pagamento.metodo_pagamento,
                pagamento.get_status_display() if hasattr(pagamento, 'get_status_display') else pagamento.status,
                pagamento.descricao[:50] + "..." if pagamento.descricao and len(pagamento.descricao) > 50 else pagamento.descricao or "N/A"
            ])
        
        # Criar a tabela
        table = Table(data, repeatRows=1)
        
        # Estilo da tabela
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(table)
        
        # Construir o PDF
        doc.build(elements)
        
        # Preparar a resposta
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="pagamentos.pdf"'
        
        return response
    except Exception as e:
        logger.error(f"Erro ao exportar pagamentos para PDF: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao exportar pagamentos para PDF: {str(e)}")
        return redirect("pagamentos:listar_pagamentos")




### Arquivo: pagamentos\templates\pagamentos\formulario_pagamento.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}
    {% if pagamento %}Editar Pagamento{% else %}Novo Pagamento{% endif %}
{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Cabeçalho com botões de ação -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>{% if pagamento %}Editar Pagamento{% else %}Novo Pagamento{% endif %}</h1>
        <div>
            <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">
                <i class="fas fa-list"></i> Lista de Pagamentos
            </a>
        </div>
    </div>
    
    <!-- Formulário -->
    <div class="card">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Informações do Pagamento</h5>
        </div>
        <div class="card-body">
            <form method="post" enctype="multipart/form-data" novalidate>
                {% csrf_token %}
                
                {% if form.non_field_errors %}
                <div class="alert alert-danger">
                    {% for error in form.non_field_errors %}
                    <p class="mb-0">{{ error }}</p>
                    {% endfor %}
                </div>
                {% endif %}
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label for="{{ form.aluno.id_for_label }}" class="form-label">Aluno*</label>
                        {{ form.aluno }}
                        {% if form.aluno.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in form.aluno.errors %}
                            {{ error }}
                            {% endfor %}
                        </div>
                        {% endif %}
                        <div class="form-text">Selecione o aluno para este pagamento</div>
                    </div>
                    
                    <div class="col-md-6">
                        <label for="{{ form.tipo.id_for_label }}" class="form-label">Tipo de Pagamento*</label>
                        {{ form.tipo }}
                        {% if form.tipo.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in form.tipo.errors %}
                            {{ error }}
                            {% endfor %}
                        </div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label for="{{ form.descricao.id_for_label }}" class="form-label">Descrição*</label>
                        {{ form.descricao }}
                        {% if form.descricao.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in form.descricao.errors %}
                            {{ error }}
                            {% endfor %}
                        </div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-6">
                        <label for="{{ form.valor.id_for_label }}" class="form-label">Valor (R$)*</label>
                        {{ form.valor }}
                        {% if form.valor.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in form.valor.errors %}
                            {{ error }}
                            {% endfor %}
                        </div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label for="{{ form.data_vencimento.id_for_label }}" class="form-label">Data de Vencimento*</label>
                        {{ form.data_vencimento }}
                        {% if form.data_vencimento.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in form.data_vencimento.errors %}
                            {{ error }}
                            {% endfor %}
                        </div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-6">
                        <label for="{{ form.status.id_for_label }}" class="form-label">Status*</label>
                        {{ form.status }}
                        {% if form.status.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in form.status.errors %}
                            {{ error }}
                            {% endfor %}
                        </div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="row mb-3" id="pagamento-info" style="display: {% if form.instance.status == 'PAGO' %}block{% else %}none{% endif %};">
                    <div class="col-md-6">
                        <label for="{{ form.data_pagamento.id_for_label }}" class="form-label">Data de Pagamento</label>
                        {{ form.data_pagamento }}
                        {% if form.data_pagamento.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in form.data_pagamento.errors %}
                            {{ error }}
                            {% endfor %}
                        </div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-6">
                        <label for="{{ form.metodo_pagamento.id_for_label }}" class="form-label">Método de Pagamento</label>
                        {{ form.metodo_pagamento }}
                        {% if form.metodo_pagamento.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in form.metodo_pagamento.errors %}
                            {{ error }}
                            {% endfor %}
                        </div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label for="{{ form.curso.id_for_label }}" class="form-label">Curso</label>
                        {{ form.curso }}
                        {% if form.curso.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in form.curso.errors %}
                            {{ error }}
                            {% endfor %}
                        </div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-6">
                        <label for="{{ form.turma.id_for_label }}" class="form-label">Turma</label>
                        {{ form.turma }}
                        {% if form.turma.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in form.turma.errors %}
                            {{ error }}
                            {% endfor %}
                        </div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="mb-3">
                    <label for="{{ form.observacoes.id_for_label }}" class="form-label">Observações</label>
                    {{ form.observacoes }}
                    {% if form.observacoes.errors %}
                    <div class="invalid-feedback d-block">
                        {% for error in form.observacoes.errors %}
                        {{ error }}
                        {% endfor %}
                    </div>
                    {% endif %}
                </div>
                
                <div class="mb-3">
                    <label for="{{ form.comprovante.id_for_label }}" class="form-label">Comprovante de Pagamento</label>
                    {% if pagamento.comprovante %}
                    <div class="mb-2">
                        <a href="{{ pagamento.comprovante.url }}" target="_blank" class="btn btn-sm btn-info">
                            <i class="fas fa-file-alt"></i> Ver comprovante atual
                        </a>
                    </div>
                    {% endif %}
                    {{ form.comprovante }}
                    {% if form.comprovante.errors %}
                    <div class="invalid-feedback d-block">
                        {% for error in form.comprovante.errors %}
                        {{ error }}
                        {% endfor %}
                    </div>
                    {% endif %}
                    <div class="form-text">Formatos aceitos: PDF, JPG, PNG. Tamanho máximo: 5MB</div>
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">Cancelar</a>
                    <button type="submit" class="btn btn-primary">
                        {% if pagamento %}Atualizar{% else %}Cadastrar{% endif %} Pagamento
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
    // Mostrar/ocultar campos de pagamento conforme o status
    const statusSelect = document.getElementById('{{ form.status.id_for_label }}');
    const pagamentoInfo = document.getElementById('pagamento-info');
    
    function togglePagamentoInfo() {
        if (statusSelect.value === 'PAGO') {
            pagamentoInfo.style.display = 'flex';
        } else {
            pagamentoInfo.style.display = 'none';
        }
    }
    
    // Chama ao carregar a página para garantir o estado correto
    togglePagamentoInfo();
    statusSelect.addEventListener('change', togglePagamentoInfo);
    
    // Inicializar campos de select2
    $(document).ready(function() {
        $('#{{ form.aluno.id_for_label }}').select2({
            theme: 'bootstrap-5',
            placeholder: 'Selecione um aluno',
            allowClear: true
        });
        
        $('#{{ form.curso.id_for_label }}').select2({
            theme: 'bootstrap-5',
            placeholder: 'Selecione um curso',
            allowClear: true
        });
        
        $('#{{ form.turma.id_for_label }}').select2({
            theme: 'bootstrap-5',
            placeholder: 'Selecione uma turma',
            allowClear: true
        });
        
        // Filtrar turmas com base no curso selecionado
        function carregarTurmas(cursoId, turmaSelecionada) {
            var turmaSelect = $('#{{ form.turma.id_for_label }}');
            turmaSelect.empty().append('<option value="">---------</option>');
            if (cursoId) {
                $.ajax({
                    url: '{% url "pagamentos:turmas_por_curso" %}',
                    data: {
                        'curso_id': cursoId
                    },
                    dataType: 'json',
                    success: function(data) {
                        $.each(data, function(i, turma) {
                            var option = $('<option></option>')
                                .attr('value', turma.id)
                                .text(turma.nome);
                            if (turmaSelecionada && turma.id == turmaSelecionada) {
                                option.attr('selected', 'selected');
                            }
                            turmaSelect.append(option);
                        });
                    }
                });
            }
        }

        $('#{{ form.curso.id_for_label }}').on('change', function() {
            var cursoId = $(this).val();
            carregarTurmas(cursoId, null);
        });

        // Ao carregar a página, se já houver curso selecionado, carregar as turmas
        var cursoInicial = $('#{{ form.curso.id_for_label }}').val();
        var turmaInicial = $('#{{ form.turma.id_for_label }}').val();
        if (cursoInicial) {
            carregarTurmas(cursoInicial, turmaInicial);
        }
    });
});
</script>
{% endblock %}




### Arquivo: pagamentos\templates\pagamentos\importar_pagamentos.html

html
{% extends 'base.html' %}

{% block title %}Importar Pagamentos CSV{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Importar Pagamentos via CSV</h1>
    <form method="post" enctype="multipart/form-data" class="mt-3">
        {% csrf_token %}
        <div class="mb-3">
            <label for="arquivo_csv" class="form-label">Arquivo CSV</label>
            <input type="file" class="form-control" id="arquivo_csv" name="arquivo_csv" accept=".csv" required>
        </div>
        <button type="submit" class="btn btn-primary">Importar</button>
        <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">Cancelar</a>
    </form>
    <div class="mt-3">
        <p>O arquivo CSV deve conter as colunas: <strong>cpf, valor, data_vencimento, status, observacoes</strong></p>
    </div>
</div>
{% endblock %}


'''