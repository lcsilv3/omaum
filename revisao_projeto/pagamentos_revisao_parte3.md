'''
# Revisão da Funcionalidade: pagamentos

## Arquivos forms.py:


### Arquivo: pagamentos\templates\pagamentos\listar_pagamentos.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Lista de Pagamentos{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Pagamentos</h1>
        <div class="d-flex gap-2">
            <a href="{% url 'pagamentos:dashboard' %}" class="btn btn-outline-secondary" data-bs-toggle="tooltip" title="Voltar ao Painel de Controle">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'pagamentos:criar_pagamento' %}" class="btn btn-success" data-bs-toggle="tooltip" title="Criar novo pagamento">
                <i class="fas fa-plus"></i> Criar Pagamento
            </a>
            <a href="{% url 'pagamentos:importar_pagamentos_csv' %}" class="btn btn-outline-primary me-2" data-bs-toggle="tooltip" title="Importar pagamentos via CSV">
                <i class="fas fa-file-import"></i> Importar CSV
            </a>
            <div class="btn-group">
                <button type="button" class="btn btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false" title="Exportar pagamentos" data-bs-toggle="tooltip">
                    <i class="fas fa-file-export"></i> Exportar
                </button>
                <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="?exportar=csv{{ request.GET.q|default_if_none:''|yesno:'&q=' }}">Exportar CSV</a></li>
                    <li><a class="dropdown-item" href="?exportar=excel{{ request.GET.q|default_if_none:''|yesno:'&q=' }}">Exportar Excel</a></li>
                    <li><a class="dropdown-item" href="?exportar=pdf{{ request.GET.q|default_if_none:''|yesno:'&q=' }}" target="_blank">Exportar PDF</a></li>
                </ul>
            </div>
        </div>
    </div>

    <!-- Filtros -->
    <form method="get" class="row g-3 mb-4">
        <div class="col-md-3">
            <label for="id_q" class="form-label">Busca</label>
            <input type="text" name="q" id="id_q" class="form-control" placeholder="Buscar por nome, CPF ou observação" value="{{ query }}">
        </div>
        <div class="col-md-2">
            <label for="id_status" class="form-label">Status</label>
            <select name="status" id="id_status" class="form-select">
                <option value="">Todos os Status</option>
                <option value="PAGO" {% if status == 'PAGO' %}selected{% endif %}>Pago</option>
                <option value="PENDENTE" {% if status == 'PENDENTE' %}selected{% endif %}>Pendente</option>
                <option value="ATRASADO" {% if status == 'ATRASADO' %}selected{% endif %}>Atrasado</option>
                <option value="CANCELADO" {% if status == 'CANCELADO' %}selected{% endif %}>Cancelado</option>
            </select>
        </div>
        <div class="col-md-2">
            <label for="id_data_inicio" class="form-label">Data início</label>
            <input type="date" name="data_inicio" id="id_data_inicio" class="form-control" value="{{ data_inicio }}">
        </div>
        <div class="col-md-2">
            <label for="id_data_fim" class="form-label">Data fim</label>
            <input type="date" name="data_fim" id="id_data_fim" class="form-control" value="{{ data_fim }}">
        </div>
        <div class="col-md-3 d-grid gap-2 d-md-flex justify-content-md-end align-items-end">
            <button type="submit" class="btn btn-primary">
                <i class="fas fa-search"></i> Filtrar
            </button>
            <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-outline-secondary">
                Limpar
            </a>
        </div>
    </form>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}

    <!-- Tabela de pagamentos -->
    <div class="table-responsive">
        <table class="table align-middle table-hover">
            <thead class="table-light">
                <tr>
                    <th>Aluno</th>
                    <th>CPF</th>
                    <th>Valor (R$)</th>
                    <th>Vencimento</th>
                    <th>Status</th>
                    <th>Data Pagamento</th>
                    <th>Método</th>
                    <th>Observações</th>
                    <th class="text-start">Ações</th> <!-- Alinha à esquerda -->
                </tr>
            </thead>
            <tbody>
                {% for pagamento in pagamentos %}
                <tr{% if pagamento.status == 'ATRASADO' %} class="table-danger"{% endif %}>
                    <td>
                        <a href="{% url 'pagamentos:pagamentos_aluno' pagamento.aluno.cpf %}" title="Ver pagamentos do aluno" data-bs-toggle="tooltip">
                            {{ pagamento.aluno.nome }}
                        </a>
                    </td>
                    <td>{{ pagamento.aluno.cpf }}</td>
                    <td>{{ pagamento.valor|floatformat:2 }}</td>
                    <td>{{ pagamento.data_vencimento|date:"d/m/Y" }}</td>
                    <td>
                        {% if pagamento.status == 'PAGO' %}
                            <span class="badge bg-success">Pago</span>
                        {% elif pagamento.status == 'PENDENTE' %}
                            <span class="badge bg-warning text-dark">Pendente</span>
                        {% elif pagamento.status == 'ATRASADO' %}
                            <span class="badge bg-danger">Atrasado</span>
                        {% else %}
                            <span class="badge bg-secondary">{{ pagamento.status }}</span>
                        {% endif %}
                    </td>
                    <td>
                        {% if pagamento.data_pagamento %}
                            {{ pagamento.data_pagamento|date:"d/m/Y" }}
                        {% else %}
                            -
                        {% endif %}
                    </td>
                    <td>
                        {% if pagamento.metodo_pagamento %}
                            {{ pagamento.get_metodo_pagamento_display }}
                        {% else %}
                            -
                        {% endif %}
                    </td>
                    <td>{{ pagamento.observacoes|default:"-" }}</td>
                    <td class="text-start">
                        <div class="btn-group btn-group-sm" role="group">
                            <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-info" title="Detalhar pagamento" data-bs-toggle="tooltip">
                                <i class="fas fa-eye"></i>
                            </a>
                            <a href="{% url 'pagamentos:editar_pagamento' pagamento.id %}" class="btn btn-warning" title="Editar pagamento" data-bs-toggle="tooltip">
                                <i class="fas fa-edit"></i>
                            </a>
                            <button type="button" class="btn btn-danger btn-excluir" title="Excluir pagamento" data-bs-toggle="tooltip"
                                data-pagamento-id="{{ pagamento.id }}">
                                <i class="fas fa-trash"></i>
                            </button>
                            {% if pagamento.status != 'PAGO' %}
                                <a href="{% url 'pagamentos:registrar_pagamento_rapido' pagamento.aluno.cpf %}" class="btn btn-success" title="Pagamento Rápido" data-bs-toggle="tooltip">
                                    <i class="fas fa-bolt"></i>
                                </a>
                            {% endif %}
                        </div>
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="9" class="text-center">Nenhum pagamento encontrado.</td>
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
                    <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% if query %}&q={{ query }}{% endif %}{% if status %}&status={{ status }}{% endif %}{% if data_inicio %}&data_inicio={{ data_inicio }}{% endif %}{% if data_fim %}&data_fim={{ data_fim }}{% endif %}">&laquo;</a>
                </li>
            {% else %}
                <li class="page-item disabled"><span class="page-link">&laquo;</span></li>
            {% endif %}
            {% for num in page_obj.paginator.page_range %}
                {% if page_obj.number == num %}
                    <li class="page-item active"><span class="page-link">{{ num }}</span></li>
                {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                    <li class="page-item"><a class="page-link" href="?page={{ num }}{% if query %}&q={{ query }}{% endif %}{% if status %}&status={{ status }}{% endif %}{% if data_inicio %}&data_inicio={{ data_inicio }}{% endif %}{% if data_fim %}&data_fim={{ data_fim }}{% endif %}">{{ num }}</a></li>
                {% endif %}
            {% endfor %}
            {% if page_obj.has_next %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ page_obj.next_page_number }}{% if query %}&q={{ query }}{% endif %}{% if status %}&status={{ status }}{% endif %}{% if data_inicio %}&data_inicio={{ data_inicio }}{% endif %}{% if data_fim %}&data_fim={{ data_fim }}{% endif %}">&raquo;</a>
                </li>
            {% else %}
                <li class="page-item disabled"><span class="page-link">&raquo;</span></li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}

    <!-- Totais -->
    <div class="row mt-4 mb-4 g-3">
        <div class="col-12 col-sm-6 col-md-3">
            <div class="card border-success shadow-sm h-100">
                <div class="card-header bg-success text-white text-center">Pago</div>
                <div class="card-body text-center">
                    <h5 class="card-title mb-0">R$ {{ total_pago|floatformat:2 }}</h5>
                </div>
            </div>
        </div>
        <div class="col-12 col-sm-6 col-md-3">
            <div class="card border-warning shadow-sm h-100">
                <div class="card-header bg-warning text-dark text-center">Pendente</div>
                <div class="card-body text-center">
                    <h5 class="card-title mb-0">R$ {{ total_pendente|floatformat:2 }}</h5>
                </div>
            </div>
        </div>
        <div class="col-12 col-sm-6 col-md-3">
            <div class="card border-danger shadow-sm h-100">
                <div class="card-header bg-danger text-white text-center">Atrasado</div>
                <div class="card-body text-center">
                    <h5 class="card-title mb-0">R$ {{ total_atrasado|floatformat:2 }}</h5>
                </div>
            </div>
        </div>
        <div class="col-12 col-sm-6 col-md-3">
            <div class="card border-secondary shadow-sm h-100">
                <div class="card-header bg-secondary text-white text-center">Cancelado</div>
                <div class="card-body text-center">
                    <h5 class="card-title mb-0">R$ {{ total_cancelados|floatformat:2 }}</h5>
                </div>
            </div>
        </div>
    </div>
    <div class="row mb-4">
        <div class="col-md-12">
            <div class="alert alert-info text-end shadow-sm">
                <strong>Total Geral:</strong> R$ {{ total_geral|floatformat:2 }}
            </div>
        </div>
    </div>
</div>

<!-- Modal de confirmação de exclusão -->
<div class="modal fade" id="modalExcluirPagamento" tabindex="-1" aria-labelledby="modalExcluirPagamentoLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header bg-danger text-white">
        <h5 class="modal-title" id="modalExcluirPagamentoLabel">Confirmar Exclusão</h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Fechar"></button>
      </div>
      <div class="modal-body">
        Tem certeza que deseja excluir este pagamento? Esta ação não poderá ser desfeita.
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
        <a href="#" class="btn btn-danger" id="btnConfirmarExclusao">Excluir</a>
      </div>
    </div>
  </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    // Ativar tooltips Bootstrap 5
    document.addEventListener('DOMContentLoaded', function () {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.forEach(function (tooltipTriggerEl) {
            new bootstrap.Tooltip(tooltipTriggerEl);
        });

        // Modal de confirmação de exclusão
        var modalExcluir = document.getElementById('modalExcluirPagamento');
        var btnConfirmar = document.getElementById('btnConfirmarExclusao');
        document.querySelectorAll('.btn-excluir').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var pagamentoId = this.getAttribute('data-pagamento-id');
                btnConfirmar.href = "{% url 'pagamentos:excluir_pagamento' 0 %}".replace('/0/', '/' + pagamentoId + '/');
                var modal = new bootstrap.Modal(modalExcluir);
                modal.show();
            });
        });
    });
</script>
{% endblock %}



### Arquivo: pagamentos\templates\pagamentos\pagamento_rapido.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Pagamento Rápido{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Cabeçalho com botões de ação -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Pagamento Rápido</h1>
        <div>
            <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">
                <i class="fas fa-list"></i> Lista de Pagamentos
            </a>
        </div>
    </div>
    
    <!-- Formulário -->
    <div class="card">
        <div class="card-header bg-success text-white">
            <h5 class="mb-0">Registrar Pagamento</h5>
        </div>
        <div class="card-body">
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                
                {% if messages %}
                    {% for message in messages %}
                        <div class="alert alert-{{ message.tags }}">
                            {{ message }}
                        </div>
                    {% endfor %}
                {% endif %}
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label for="aluno" class="form-label">Aluno</label>
                        <select class="form-select" id="aluno" name="aluno" required>
                            <option value="">Selecione um aluno</option>
                            {% for aluno in alunos %}
                                <option value="{{ aluno.cpf }}" {% if form.aluno.value == aluno.cpf %}selected{% endif %}>
                                    {{ aluno.nome }} ({{ aluno.cpf }})
                                </option>
                            {% endfor %}
                        </select>
                        {% if form.aluno.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.aluno.errors %}
                                    {{ error }}
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-6">
                        <label for="tipo" class="form-label">Tipo de Pagamento</label>
                        <select class="form-select" id="tipo" name="tipo" required>
                            <option value="">Selecione o tipo</option>
                            <option value="MENSALIDADE" {% if form.tipo.value == 'MENSALIDADE' %}selected{% endif %}>Mensalidade</option>
                            <option value="MATRICULA" {% if form.tipo.value == 'MATRICULA' %}selected{% endif %}>Matrícula</option>
                            <option value="MATERIAL" {% if form.tipo.value == 'MATERIAL' %}selected{% endif %}>Material</option>
                            <option value="OUTRO" {% if form.tipo.value == 'OUTRO' %}selected{% endif %}>Outro</option>
                        </select>
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
                        <label for="valor" class="form-label">Valor (R$)</label>
                        <input type="number" step="0.01" class="form-control" id="valor" name="valor" required value="{{ form.valor.value|default:'' }}">
                        {% if form.valor.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.valor.errors %}
                                    {{ error }}
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-6">
                        <label for="metodo_pagamento" class="form-label">Método de Pagamento</label>
                        <select class="form-select" id="metodo_pagamento" name="metodo_pagamento" required>
                            <option value="">Selecione o método</option>
                            <option value="PIX" {% if form.metodo_pagamento.value == 'PIX' %}selected{% endif %}>PIX</option>
                            <option value="CARTAO_CREDITO" {% if form.metodo_pagamento.value == 'CARTAO_CREDITO' %}selected{% endif %}>Cartão de Crédito</option>
                            <option value="CARTAO_DEBITO" {% if form.metodo_pagamento.value == 'CARTAO_DEBITO' %}selected{% endif %}>Cartão de Débito</option>
                            <option value="DINHEIRO" {% if form.metodo_pagamento.value == 'DINHEIRO' %}selected{% endif %}>Dinheiro</option>
                            <option value="BOLETO" {% if form.metodo_pagamento.value == 'BOLETO' %}selected{% endif %}>Boleto</option>
                            <option value="TRANSFERENCIA" {% if form.metodo_pagamento.value == 'TRANSFERENCIA' %}selected{% endif %}>Transferência</option>
                            <option value="OUTRO" {% if form.metodo_pagamento.value == 'OUTRO' %}selected{% endif %}>Outro</option>
                        </select>
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
                    <div class="col-md-12">
                        <label for="descricao" class="form-label">Descrição</label>
                        <input type="text" class="form-control" id="descricao" name="descricao" required value="{{ form.descricao.value|default:'' }}">
                        {% if form.descricao.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.descricao.errors %}
                                    {{ error }}
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label for="comprovante" class="form-label">Comprovante (opcional)</label>
                        <input type="file" class="form-control" id="comprovante" name="comprovante">
                        {% if form.comprovante.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.comprovante.errors %}
                                    {{ error }}
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-6">
                        <label for="observacoes" class="form-label">Observações (opcional)</label>
                        <textarea class="form-control" id="observacoes" name="observacoes" rows="3">{{ form.observacoes.value|default:'' }}</textarea>
                        {% if form.observacoes.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.observacoes.errors %}
                                    {{ error }}
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                    <button type="submit" class="btn btn-success">
                        <i class="fas fa-money-bill-wave"></i> Registrar Pagamento
                    </button>
                    <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">
                        <i class="fas fa-times"></i> Cancelar
                    </a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Inicializar o select2 para o campo de aluno
        $('#aluno').select2({
            placeholder: 'Selecione um aluno',
            allowClear: true,
            width: '100%'
        });
        
        // Atualizar a descrição automaticamente quando o tipo mudar
        $('#tipo').change(function() {
            var tipo = $(this).val();
            var descricao = '';
            
            if (tipo === 'MENSALIDADE') {
                var dataAtual = new Date();
                var mes = dataAtual.toLocaleString('pt-BR', { month: 'long' });
                var ano = dataAtual.getFullYear();
                descricao = 'Mensalidade - ' + mes + '/' + ano;
            } else if (tipo === 'MATRICULA') {
                descricao = 'Taxa de Matrícula';
            } else if (tipo === 'MATERIAL') {
                descricao = 'Material Didático';
            }
            
            if (descricao) {
                $('#descricao').val(descricao);
            }
        });
        
        // Formatar o campo de valor para mostrar como moeda
        $('#valor').on('input', function() {
            var value = $(this).val();
            if (value) {
                value = parseFloat(value).toFixed(2);
                if (!isNaN(value)) {
                    $(this).val(value);
                }
            }
        });
    });
</script>
{% endblock %}



### Arquivo: pagamentos\templates\pagamentos\pagamentos_aluno.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Pagamentos de {{ aluno.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Pagamentos de {{ aluno.nome }}</h1>
        <div>
            <a href="{% url 'alunos:detalhar_aluno' aluno.cpf %}" class="btn btn-secondary me-2">
                <i class="fas fa-arrow-left"></i> Voltar para o Perfil
            </a>
            <a href="{% url 'pagamentos:registrar_pagamento_rapido' aluno.cpf %}" class="btn btn-primary">
                <i class="fas fa-plus"></i> Novo Pagamento
            </a>
        </div>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card bg-primary text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Total</h5>
                    <p class="card-text display-6">R$ {{ total_pago|add:total_pendente|add:total_atrasado|add:total_cancelado|floatformat:2 }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-success text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Pago</h5>
                    <p class="card-text display-6">R$ {{ total_pago|floatformat:2 }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-warning text-dark">
                <div class="card-body text-center">
                    <h5 class="card-title">Pendente</h5>
                    <p class="card-text display-6">R$ {{ total_pendente|floatformat:2 }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-danger text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Atrasado</h5>
                    <p class="card-text display-6">R$ {{ total_atrasado|floatformat:2 }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-8">
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Lista de Pagamentos</h5>
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
                                {% for pagamento in pagamentos %}
                                    <tr>
                                        <td>
                                            {% if pagamento.matricula %}
                                                {{ pagamento.matricula.turma.curso.nome }} - {{ pagamento.matricula.turma.nome }}
                                                {% if pagamento.numero_parcela %}
                                                    <br><small>Parcela {{ pagamento.numero_parcela }}/{{ pagamento.total_parcelas }}</small>
                                                {% endif %}
                                            {% else %}
                                                Pagamento Avulso
                                            {% endif %}
                                            {% if pagamento.observacoes %}
                                                <br><small class="text-muted">{{ pagamento.observacoes }}</small>
                                            {% endif %}
                                        </td>
                                        <td>R$ {{ pagamento.valor|floatformat:2 }}</td>
                                        <td>{{ pagamento.data_vencimento|date:"d/m/Y" }}</td>
                                        <td>
                                            {% if pagamento.status == 'PAGO' %}
                                                <span class="badge bg-success">Pago</span>
                                                {% if pagamento.data_pagamento %}
                                                    <br><small>em {{ pagamento.data_pagamento|date:"d/m/Y" }}</small>
                                                {% endif %}
                                            {% elif pagamento.status == 'PENDENTE' %}
                                                <span class="badge bg-warning text-dark">Pendente</span>
                                            {% elif pagamento.status == 'ATRASADO' %}
                                                <span class="badge bg-danger">Atrasado</span>
                                            {% elif pagamento.status == 'CANCELADO' %}
                                                <span class="badge bg-secondary">Cancelado</span>
                                            {% endif %}
                                        </td>
                                        <td>
                                            <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-sm btn-info">
                                                <i class="fas fa-eye"></i>
                                            </a>
                                            {% if pagamento.status == 'PENDENTE' or pagamento.status == 'ATRASADO' %}
                                                <a href="{% url 'pagamentos:registrar_pagamento' pagamento.id %}" class="btn btn-sm btn-success">
                                                    <i class="fas fa-check"></i>
                                                </a>
                                            {% endif %}
                                        </td>
                                    </tr>
                                {% empty %}
                                    <tr>
                                        <td colspan="5" class="text-center">
                                            <p class="my-3">Nenhum pagamento registrado para este aluno.</p>
                                        </td>
                                    </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="card mb-4">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">Dados do Aluno</h5>
                </div>
                <div class="card-body">
                    <div class="d-flex align-items-center mb-3">
                        {% if aluno.foto %}
                            <img src="{{ aluno.foto.url }}" alt="Foto de {{ aluno.nome }}" 
                                 class="rounded-circle me-3" width="60" height="60" style="object-fit: cover;">
                        {% else %}
                            <div class="rounded-circle bg-secondary d-flex align-items-center justify-content-center me-3" 
                                 style="width: 60px; height: 60px; color: white;">
                                {{ aluno.nome|first|upper }}
                            </div>
                        {% endif %}
                        <div>
                            <h5 class="mb-0">{{ aluno.nome }}</h5>
                            <p class="text-muted mb-0">CPF: {{ aluno.cpf }}</p>
                        </div>
                    </div>
                    
                    <p><strong>Email:</strong> {{ aluno.email|default:"Não informado" }}</p>
                    {% if aluno.numero_iniciatico %}
                        <p><strong>Nº Iniciático:</strong> {{ aluno.numero_iniciatico }}</p>
                    {% endif %}
                </div>
            </div>
            
            {% if matriculas %}
            <div class="card mb-4">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">Matrículas</h5>
                </div>
                <div class="card-body">
                    <ul class="list-group">
                        {% for matricula in matriculas %}
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <div>
                                    <strong>{{ matricula.turma.curso.nome }}</strong>
                                    <div>{{ matricula.turma.nome }}</div>
                                </div>
                                <span class="badge bg-{{ matricula.status_color }}">{{ matricula.get_status_display }}</span>
                            </li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
            {% endif %}
            
            <div class="card">
                <div class="card-header bg-warning text-dark">
                    <h5 class="mb-0">Histórico de Pagamentos</h5>
                </div>
                <div class="card-body">
                    <canvas id="graficoHistorico" height="200"></canvas>
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
        // Dados para o gráfico de histórico
        const ctx = document.getElementById('graficoHistorico').getContext('2d');
        
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Pago', 'Pendente', 'Atrasado', 'Cancelado'],
                datasets: [{
                    label: 'Valor (R$)',
                    data: [
                        {{ total_pago|floatformat:2 }}, 
                        {{ total_pendente|floatformat:2 }}, 
                        {{ total_atrasado|floatformat:2 }}, 
                        {{ total_cancelado|floatformat:2 }}
                    ],
                    backgroundColor: [
                        'rgba(40, 167, 69, 0.7)',  // Verde para pago
                        'rgba(255, 193, 7, 0.7)',  // Amarelo para pendente
                        'rgba(220, 53, 69, 0.7)',  // Vermelho para atrasado
                        'rgba(108, 117, 125, 0.7)' // Cinza para cancelado
                    ],
                    borderColor: [
                        'rgb(40, 167, 69)',
                        'rgb(255, 193, 7)',
                        'rgb(220, 53, 69)',
                        'rgb(108, 117, 125)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'R$ ' + context.raw.toFixed(2);
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return 'R$ ' + value;
                            }
                        }
                    }
                }
            }
        });
    });
</script>
{% endblock %}



### Arquivo: pagamentos\templates\pagamentos\pagamentos_por_turma.html

html
{% extends 'base.html' %}

{% block title %}Pagamentos por Turma{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Pagamentos por Turma</h1>
        <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    {% for item in turmas_com_pagamentos %}
        <div class="card mb-4">
            <div class="card-header bg-primary text-white">
                <div class="d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">{{ item.turma.nome }} - {{ item.turma.curso.nome }}</h5>
                    <span class="badge bg-light text-dark">{{ item.alunos_count }} alunos</span>
                </div>
            </div>
            <div class="card-body">
                <div class="row mb-3">
                    <div class="col-md-4">
                        <div class="card text-white bg-success">
                            <div class="card-body text-center">
                                <h6 class="card-title">Total Pago</h6>
                                <p class="card-text h4">R$ {{ item.total_pago|floatformat:2 }}</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card text-white bg-warning">
                            <div class="card-body text-center">
                                <h6 class="card-title">Total Pendente</h6>
                                <p class="card-text h4">R$ {{ item.total_pendente|floatformat:2 }}</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card text-white bg-info">
                            <div class="card-body text-center">
                                <h6 class="card-title">Total</h6>
                                <p class="card-text h4">R$ {{ item.total|floatformat:2 }}</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Aluno</th>
                                <th>Valor</th>
                                <th>Vencimento</th>
                                <th>Status</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for pagamento in item.pagamentos %}
                                <tr>
                                    <td>{{ pagamento.aluno.nome }}</td>
                                    <td>R$ {{ pagamento.valor|floatformat:2 }}</td>
                                    <td>{{ pagamento.data_vencimento|date:"d/m/Y" }}</td>
                                    <td>
                                        {% if pagamento.status == 'PAGO' %}
                                            <span class="badge bg-success">{{ pagamento.get_status_display }}</span>
                                        {% elif pagamento.status == 'PENDENTE' %}
                                            <span class="badge bg-warning">{{ pagamento.get_status_display }}</span>
                                        {% elif pagamento.status == 'ATRASADO' %}
                                            <span class="badge bg-danger">{{ pagamento.get_status_display }}</span>
                                        {% else %}
                                            <span class="badge bg-secondary">{{ pagamento.get_status_display }}</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-sm btn-info">Detalhes</a>
                                        <a href="{% url 'pagamentos:editar_pagamento' pagamento.id %}" class="btn btn-sm btn-warning">Editar</a>
                                    </td>
                                </tr>
                            {% empty %}
                                <tr>
                                    <td colspan="5" class="text-center">Nenhum pagamento encontrado para esta turma.</td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    {% empty %}
        <div class="alert alert-info">
            <p>Nenhuma turma ativa encontrada.</p>
        </div>
    {% endfor %}
</div>
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