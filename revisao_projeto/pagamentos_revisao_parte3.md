'''
# Revisão da Funcionalidade: pagamentos

## Arquivos forms.py:


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



### Arquivo: pagamentos\templates\pdf\pagamentos_pdf.html

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


'''