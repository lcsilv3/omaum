'''
# Revisão da Funcionalidade: pagamentos

## Arquivos forms.py:


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
            <a href="{% url 'pagamentos:painel_geral' %}" class="btn btn-outline-secondary" data-bs-toggle="tooltip" title="Voltar ao Painel de Controle">
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



'''