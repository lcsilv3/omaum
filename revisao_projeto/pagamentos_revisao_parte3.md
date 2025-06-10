'''
# Revisão da Funcionalidade: pagamentos

## Arquivos forms.py:


### Arquivo: pagamentos\templates\pagamentos\painel_financeiro.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Painel Financeiro{% endblock %}

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
                    <a href="{% url 'pagamentos:painel_geral' %}" class="btn btn-secondary">
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




### Arquivo: pagamentos\templates\pagamentos\painel_geral.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Painel Geral de Pagamentos{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Painel de Pagamentos</h1>
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
                    <h2 class="display-4">{{ pagamentos_atrasados_count }}</h2>
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
                    <h5 class="mb-0">Painéis Específicos</h5>
                </div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <a href="{% url 'pagamentos:painel_mensal' %}" class="btn btn-outline-primary">
                            <i class="fas fa-chart-line"></i> Painel de Pagamentos
                        </a>
                        <a href="{% url 'pagamentos:painel_financeiro' %}" class="btn btn-outline-success">
                            <i class="fas fa-money-bill-wave"></i> Painel Financeiro
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




### Arquivo: pagamentos\templates\pagamentos\painel_mensal.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Painel Mensal{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.css">
{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Dashboard de Pagamentos</h1>
        <div>
            <a href="{% url 'pagamentos:painel_geral' %}" class="btn btn-secondary me-2">
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




### Arquivo: pagamentos\templates\pagamentos\pdf\pagamentos_pdf.html

html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Relatório de Pagamentos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            font-size: 12px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .header {
            margin-bottom: 20px;
            text-align: center;
        }
        .info {
            margin-bottom: 20px;
            border: 1px solid #ddd;
            padding: 10px;
            background-color: #f9f9f9;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .footer {
            margin-top: 20px;
            text-align: center;
            font-size: 10px;
            color: #666;
        }
        .totals {
            margin-top: 20px;
            text-align: right;
        }
        .status-pago {
            color: green;
            font-weight: bold;
        }
        .status-pendente {
            color: orange;
            font-weight: bold;
        }
        .status-cancelado {
            color: gray;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Relatório de Pagamentos</h1>
        <p>Data de geração: {{ data_geracao|date:"d/m/Y H:i" }}</p>
    </div>
    
    <div class="info">
        <h3>Filtros Aplicados</h3>
        <p>Status: {{ filtros.status|default:"Todos" }}</p>
        <p>Período: {% if filtros.data_inicio or filtros.data_fim %}
            {% if filtros.data_inicio %}De: {{ filtros.data_inicio|date:"d/m/Y" }}{% endif %}
            {% if filtros.data_fim %}Até: {{ filtros.data_fim|date:"d/m/Y" }}{% endif %}
            {% else %}Todos{% endif %}
        </p>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>Aluno</th>
                <th>Valor</th>
                <th>Vencimento</th>
                <th>Status</th>
                <th>Data Pagamento</th>
            </tr>
        </thead>
        <tbody>
            {% for pagamento in pagamentos %}
                <tr>
                    <td>{{ pagamento.aluno.nome }}</td>
                    <td>R$ {{ pagamento.valor|floatformat:2 }}</td>
                    <td>{{ pagamento.data_vencimento|date:"d/m/Y" }}</td>
                    <td class="status-{{ pagamento.status }}">{{ pagamento.get_status_display }}</td>
                    <td>{{ pagamento.data_pagamento|date:"d/m/Y"|default:"-" }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <div class="totals">
        <p><strong>Total Pago:</strong> R$ {{ total_pago|floatformat:2 }}</p>
        <p><strong>Total Pendente:</strong> R$ {{ total_pendente|floatformat:2 }}</p>
        <p><strong>Total Geral:</strong> R$ {{ total_geral|floatformat:2 }}</p>
    </div>
    
    <div class="footer">
        <p>Relatório gerado pelo sistema OMAUM - Página 1 de 1</p>
    </div>
</body>
</html>



### Arquivo: pagamentos\templates\pagamentos\registrar_pagamento.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Registrar Pagamento{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Registrar Pagamento</h1>
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
                    <div class="alert alert-info d-flex align-items-center mb-4">
                        {% if pagamento.aluno.foto %}
                            <img src="{{ pagamento.aluno.foto.url }}" alt="Foto de {{ pagamento.aluno.nome }}" 
                                 class="rounded-circle me-3" width="50" height="50" style="object-fit: cover;">
                        {% else %}
                            <div class="rounded-circle bg-secondary d-flex align-items-center justify-content-center me-3" 
                                 style="width: 50px; height: 50px; color: white;">
                                {{ pagamento.aluno.nome|first|upper }}
                            </div>
                        {% endif %}
                        <div>
                            <strong>Aluno:</strong> {{ pagamento.aluno.nome }}
                            <br>
                            <small>CPF: {{ pagamento.aluno.cpf }}</small>
                        </div>
                    </div>
                    
                    <form method="post">
                        {% csrf_token %}
                        
                        <div class="row mb-3">
                            <div class="col-md-6">
                                <label class="form-label">Valor</label>
                                <div class="input-group">
                                    <span class="input-group-text">R$</span>
                                    <input type="text" class="form-control" value="{{ pagamento.valor|floatformat:2 }}" readonly>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label">Data de Vencimento</label>
                                <input type="text" class="form-control" value="{{ pagamento.data_vencimento|date:'d/m/Y' }}" readonly>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Descrição</label>
                            <input type="text" class="form-control" value="{% if pagamento.matricula %}{{ pagamento.matricula.turma.curso.nome }} - {{ pagamento.matricula.turma.nome }}{% else %}Pagamento Avulso{% endif %}" readonly>
                        </div>
                        
                        <div class="row mb-3">
                            <div class="col-md-6">
                                <label for="data_pagamento" class="form-label">Data de Pagamento</label>
                                <input type="date" name="data_pagamento" id="data_pagamento" class="form-control" value="{{ data_hoje }}" required>
                            </div>
                            <div class="col-md-6">
                                <label for="metodo_pagamento" class="form-label">Método de Pagamento</label>
                                <select name="metodo_pagamento" id="metodo_pagamento" class="form-select" required>
                                    <option value="">Selecione um método</option>
                                    <option value="DINHEIRO">Dinheiro</option>
                                    <option value="CARTAO_CREDITO">Cartão de Crédito</option>
                                    <option value="CARTAO_DEBITO">Cartão de Débito</option>
                                    <option value="BOLETO">Boleto Bancário</option>
                                    <option value="TRANSFERENCIA">Transferência</option>
                                    <option value="PIX">PIX</option>
                                    <option value="OUTRO">Outro</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label for="observacoes" class="form-label">Observações</label>
                            <textarea name="observacoes" id="observacoes" class="form-control" rows="3">{{ pagamento.observacoes }}</textarea>
                        </div>
                        
                        <div class="d-flex justify-content-between">
                            <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-secondary">
                                <i class="fas fa-times"></i> Cancelar
                            </a>
                            <button type="submit" class="btn btn-success">
                                <i class="fas fa-check"></i> Confirmar Pagamento
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
                    <p>Você está registrando o pagamento para <strong>{{ pagamento.aluno.nome }}</strong>.</p>
                    <p>Valor a ser pago: <strong>R$ {{ pagamento.valor|floatformat:2 }}</strong></p>
                    <p>Vencimento: <strong>{{ pagamento.data_vencimento|date:'d/m/Y' }}</strong></p>
                    
                    {% if pagamento.status == 'ATRASADO' %}
                        <div class="alert alert-danger">
                            <i class="fas fa-exclamation-triangle"></i> Este pagamento está <strong>atrasado</strong>.
                        </div>
                    {% endif %}
                    
                    <hr>
                    <p class="mb-0"><small>Ao confirmar o pagamento, o status será alterado para "Pago" e não poderá ser revertido facilmente.</small></p>
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
                        <p><strong>Parcela:</strong> {{ pagamento.numero_parcela }} de {{ pagamento.total_parcelas }}</p>
                    {% endif %}
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Definir data de pagamento padrão como hoje
        const dataPagamentoInput = document.getElementById('data_pagamento');
        if (!dataPagamentoInput.value) {
            const hoje = new Date();
            const ano = hoje.getFullYear();
            const mes = String(hoje.getMonth() + 1).padStart(2, '0');
            const dia = String(hoje.getDate()).padStart(2, '0');
            dataPagamentoInput.value = `${ano}-${mes}-${dia}`;
        }
        
        // Validar formulário antes de enviar
        document.querySelector('form').addEventListener('submit', function(e) {
            const dataPagamento = document.getElementById('data_pagamento').value;
            const metodoPagamento = document.getElementById('metodo_pagamento').value;
            
            if (!dataPagamento) {
                e.preventDefault();
                alert('Por favor, informe a data de pagamento.');
                return false;
            }
            
            if (!metodoPagamento) {
                e.preventDefault();
                alert('Por favor, selecione o método de pagamento.');
                return false;
            }
            
            return true;
        });
    });
</script>
{% endblock %}




### Arquivo: pagamentos\templates\pagamentos\registrar_pagamento_rapido.html

html
{% extends 'base.html' %}

{% block title %}Registrar Pagamento para {{ aluno.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Registrar Pagamento</h1>
        <div>
            <a href="{% url 'pagamentos:pagamentos_aluno' aluno.cpf %}" class="btn btn-secondary">
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
                    <div class="alert alert-info d-flex align-items-center mb-4">
                        {% if aluno.foto %}
                            <img src="{{ aluno.foto.url }}" alt="Foto de {{ aluno.nome }}" 
                                 class="rounded-circle me-3" width="50" height="50" style="object-fit: cover;">
                        {% else %}
                            <div class="rounded-circle bg-secondary d-flex align-items-center justify-content-center me-3" 
                                 style="width: 50px; height: 50px; color: white;">
                                {{ aluno.nome|first|upper }}
                            </div>
                        {% endif %}
                        <div>
                            <strong>Aluno:</strong> {{ aluno.nome }}
                            <br>
                            <small>CPF: {{ aluno.cpf }}</small>
                        </div>
                    </div>
                    
                    <form method="post">
                        {% csrf_token %}
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="valor" class="form-label">Valor (R$)</label>
                                    <input type="number" name="valor" id="valor" class="form-control" step="0.01" min="0" required>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="data_vencimento" class="form-label">Data de Vencimento</label>
                                    <input type="date" name="data_vencimento" id="data_vencimento" class="form-control" value="{{ data_hoje }}" required>
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label for="observacoes" class="form-label">Observações</label>
                            <textarea name="observacoes" id="observacoes" class="form-control" rows="3"></textarea>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="status" class="form-label">Status</label>
                                    <select name="status" id="status" class="form-select" required>
                                        <option value="PENDENTE">Pendente</option>
                                        <option value="PAGO">Pago</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3 metodo-pagamento-container" style="display: none;">
                                    <label for="metodo_pagamento" class="form-label">Método de Pagamento</label>
                                    <select name="metodo_pagamento" id="metodo_pagamento" class="form-select">
                                        <option value="">Selecione um método</option>
                                        <option value="DINHEIRO">Dinheiro</option>
                                        <option value="CARTAO_CREDITO">Cartão de Crédito</option>
                                        <option value="CARTAO_DEBITO">Cartão de Débito</option>
                                        <option value="BOLETO">Boleto Bancário</option>
                                        <option value="TRANSFERENCIA">Transferência</option>
                                        <option value="PIX">PIX</option>
                                        <option value="OUTRO">Outro</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="d-flex justify-content-between">
                            <a href="{% url 'pagamentos:pagamentos_aluno' aluno.cpf %}" class="btn btn-secondary">
                                <i class="fas fa-times"></i> Cancelar
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Registrar Pagamento
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
                    <p>Você está registrando um novo pagamento para <strong>{{ aluno.nome }}</strong>.</p>
                    <p>Preencha todos os campos obrigatórios para continuar.</p>
                    <p>Se o status for "Pago", o sistema registrará a data de pagamento como hoje.</p>
                </div>
            </div>
            
            {% if matriculas %}
            <div class="card mb-4">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">Matrículas Ativas</h5>
                </div>
                <div class="card-body">
                    <ul class="list-group">
                        {% for matricula in matriculas %}
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <div>
                                    <strong>{{ matricula.turma.curso.nome }}</strong>
                                    <div>{{ matricula.turma.nome }}</div>
                                </div>
                            </li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const statusSelect = document.getElementById('status');
        const metodoPagamentoContainer = document.querySelector('.metodo-pagamento-container');
        
        // Função para mostrar/ocultar campos dependendo do status
        function toggleFields() {
            if (statusSelect.value === 'PAGO') {
                metodoPagamentoContainer.style.display = 'block';
                document.getElementById('metodo_pagamento').required = true;
            } else {
                metodoPagamentoContainer.style.display = 'none';
                document.getElementById('metodo_pagamento').required = false;
            }
        }
        
        // Executar ao carregar a página
        toggleFields();
        
        // Adicionar evento de mudança
        statusSelect.addEventListener('change', toggleFields);
    });
</script>
{% endblock %}
                            </div>




### Arquivo: pagamentos\templates\pagamentos\relatorio_financeiro.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Relatório Financeiro{% endblock %}

{% block extra_css %}
<style>
    .card-dashboard {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .card-dashboard:hover {
        transform: translateY(-5px);
    }
    
    .chart-container {
        position: relative;
        height: 300px;
        margin-bottom: 20px;
    }
    
    .status-indicator {
        width: 15px;
        height: 15px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
    }
    
    .status-pago {
        background-color: #28a745;
    }
    
    .status-pendente {
        background-color: #ffc107;
    }
    
    .status-atrasado {
        background-color: #dc3545;
    }
    
    .status-cancelado {
        background-color: #6c757d;
    }
    
    .table-financeiro th {
        background-color: #f8f9fa;
    }
</style>
{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Relatório Financeiro</h1>
        <div>
            <a href="{% url 'pagamentos:exportar_relatorio_pdf' %}?ano={{ ano_atual }}" class="btn btn-danger" target="_blank">
                <i class="fas fa-file-pdf"></i> Exportar PDF
            </a>
            <a href="{% url 'pagamentos:exportar_relatorio_excel' %}?ano={{ ano_atual }}" class="btn btn-success">
                <i class="fas fa-file-excel"></i> Exportar Excel
            </a>
        </div>
    </div>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-4">
                    <label for="ano" class="form-label">Ano</label>
                    <select class="form-select" id="ano" name="ano" onchange="this.form.submit()">
                        {% for ano in anos_disponiveis %}
                            <option value="{{ ano }}" {% if ano == ano_atual %}selected{% endif %}>{{ ano }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-4">
                    <label for="mes" class="form-label">Mês (opcional)</label>
                    <select class="form-select" id="mes" name="mes" onchange="this.form.submit()">
                        <option value="">Todos os meses</option>
                        {% for i in "123456789101112"|make_list %}
                            {% with mes_num=forloop.counter %}
                                <option value="{{ mes_num }}" {% if mes_num == mes_atual %}selected{% endif %}>
                                    {{ mes_num|stringformat:"02d" }} - {% now "F"|date:"F"|cut:mes_num %}
                                </option>
                            {% endwith %}
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-4">
                    <label for="status" class="form-label">Status (opcional)</label>
                    <select class="form-select" id="status" name="status" onchange="this.form.submit()">
                        <option value="">Todos os status</option>
                        <option value="PAGO" {% if filtros.status == 'PAGO' %}selected{% endif %}>Pago</option>
                        <option value="PENDENTE" {% if filtros.status == 'PENDENTE' %}selected{% endif %}>Pendente</option>
                        <option value="ATRASADO" {% if filtros.status == 'ATRASADO' %}selected{% endif %}>Atrasado</option>
                        <option value="CANCELADO" {% if filtros.status == 'CANCELADO' %}selected{% endif %}>Cancelado</option>
                    </select>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Resumo -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card card-dashboard bg-primary text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Total Geral</h5>
                    <p class="card-text display-6">R$ {{ total_geral|floatformat:2 }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card card-dashboard bg-success text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Total Pago</h5>
                    <p class="card-text display-6">R$ {{ total_pago|floatformat:2 }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card card-dashboard bg-warning text-dark">
                <div class="card-body text-center">
                    <h5 class="card-title">Total Pendente</h5>
                    <p class="card-text display-6">R$ {{ total_pendente|floatformat:2 }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card card-dashboard bg-danger text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Total Atrasado</h5>
                    <p class="card-text display-6">R$ {{ total_atrasado|floatformat:2 }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Gráficos -->
    <div class="row mb-4">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">Evolução Mensal</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="graficoMensal"></canvas>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">Distribuição por Status</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="graficoPizza"></canvas>
                    </div>
                    <div class="mt-3">
                        <div class="d-flex justify-content-between mb-2">
                            <div>
                                <span class="status-indicator status-pago"></span> Pago
                            </div>
                            <strong>{{ total_pago|floatformat:2 }} ({{ porcentagem_pago|floatformat:1 }}%)</strong>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                            <div>
                                <span class="status-indicator status-pendente"></span> Pendente
                            </div>
                            <strong>{{ total_pendente|floatformat:2 }} ({{ porcentagem_pendente|floatformat:1 }}%)</strong>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                            <div>
                                <span class="status-indicator status-atrasado"></span> Atrasado
                            </div>
                            <strong>{{ total_atrasado|floatformat:2 }} ({{ porcentagem_atrasado|floatformat:1 }}%)</strong>
                        </div>
                        <div class="d-flex justify-content-between">
                            <div>
                                <span class="status-indicator status-cancelado"></span> Cancelado
                            </div>
                            <strong>{{ total_cancelado|floatformat:2 }} ({{ porcentagem_cancelado|floatformat:1 }}%)</strong>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Tabela de dados mensais -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Dados Mensais - {{ ano_atual }}</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover table-financeiro">
                    <thead>
                        <tr>
                            <th>Mês</th>
                            <th class="text-success">Pago</th>
                            <th class="text-warning">Pendente</th>
                            <th class="text-danger">Atrasado</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for dado in dados_mensais %}
                            <tr>
                                <td>{{ dado.nome_mes }}</td>
                                <td class="text-success">R$ {{ dado.pago|floatformat:2 }}</td>
                                <td class="text-warning">R$ {{ dado.pendente|floatformat:2 }}</td>
                                <td class="text-danger">R$ {{ dado.atrasado|floatformat:2 }}</td>
                                <td><strong>R$ {{ dado.total|floatformat:2 }}</strong></td>
                            </tr>
                        {% endfor %}
                    </tbody>
                    <tfoot>
                        <tr class="table-active">
                            <th>Total</th>
                            <th class="text-success">R$ {{ total_pago|floatformat:2 }}</th>
                            <th class="text-warning">R$ {{ total_pendente|floatformat:2 }}</th>
                            <th class="text-danger">R$ {{ total_atrasado|floatformat:2 }}</th>
                            <th>R$ {{ total_geral|floatformat:2 }}</th>
                        </tr>
                    </tfoot>
                </table>
            </div>
        </div>
    </div>
    
    <div class="text-muted text-center mb-4">
        <small>Relatório gerado em {{ data_geracao|date:"d/m/Y H:i" }}</small>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Dados para o gráfico mensal
        const meses = [{% for dado in dados_mensais %}'{{ dado.nome_mes }}',{% endfor %}];



'''