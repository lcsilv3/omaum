'''
# Revisão da Funcionalidade: presencas

## Arquivos forms.py:


### Arquivo: presencas\templates\presencas\ritualisticas\excluir_presenca_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}Excluir Presença{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card border-danger">
                <div class="card-header bg-danger text-white">
                    <h4 class="mb-0">Confirmar Exclusão</h4>
                </div>
                <div class="card-body">
                    <div class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        Você está prestes a excluir o seguinte registro de presença:
                    </div>
                    
                    <div class="card mb-3">
                        <div class="card-body">
                            <p><strong>Aluno:</strong> {{ presenca.aluno.nome }}</p>
                            <p><strong>Atividade:</strong> {{ presenca.atividade.titulo }}</p>
                            <p><strong>Data:</strong> {{ presenca.data|date:"d/m/Y" }}</p>
                            <p><strong>Situação:</strong> 
                                {% if presenca.situacao == 'PRESENTE' %}
                                <span class="badge bg-success">Presente</span>
                                {% elif presenca.situacao == 'AUSENTE' %}
                                <span class="badge bg-danger">Ausente</span>
                                {% elif presenca.situacao == 'JUSTIFICADO' %}
                                <span class="badge bg-warning">Justificado</span>
                                {% endif %}
                            </p>
                            {% if presenca.justificativa %}
                            <p><strong>Justificativa:</strong> {{ presenca.justificativa }}</p>
                            {% endif %}
                        </div>
                    </div>
                    
                    <p class="text-danger">Esta ação não pode ser desfeita. Deseja continuar?</p>
                    
                    <form method="post">
                        {% csrf_token %}
                        <div class="d-flex justify-content-between">
                            <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
                                <i class="fas fa-times"></i> Cancelar
                            </a>
                            <button type="submit" class="btn btn-danger">
                                <i class="fas fa-trash"></i> Confirmar Exclusão
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: presencas\templates\presencas\ritualisticas\exportar_presencas_ritualisticas.html

html
{% extends 'base.html' %}

{% block title %}Exportar Presenças Ritualísticas{% endblock %}

{% block content %}
<div class="container mt-4">
    <h2>Exportação de Presenças Ritualísticas</h2>
    <p>Funcionalidade de exportação de presenças ritualísticas. Implemente aqui a lógica de exportação (CSV, Excel, etc).</p>
    <a href="{% url 'presencas:listar_presencas_ritualisticas' %}" class="btn btn-secondary mt-3">Voltar</a>
</div>
{% endblock %}



### Arquivo: presencas\templates\presencas\ritualisticas\filtro_presencas_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}Filtrar Presenças{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Filtrar Presenças</h1>
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
    
    <div class="card">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Filtros de Pesquisa</h5>
        </div>
        <div class="card-body">
            <form method="get" action="{% url 'presencas:listar_presencas' %}">
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label for="aluno" class="form-label">Aluno</label>
                        <select class="form-select" id="aluno" name="aluno">
                            <option value="">Todos os alunos</option>
                            {% for aluno in alunos %}
                            <option value="{{ aluno.cpf }}">{{ aluno.nome }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="col-md-6">
                        <label for="turma" class="form-label">Turma</label>
                        <select class="form-select" id="turma" name="turma">
                            <option value="">Todas as turmas</option>
                            {% for turma in turmas %}
                            <option value="{{ turma.id }}">{{ turma.nome }}</option>
                            {% endfor %}
                        </select>
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label for="atividade" class="form-label">Atividade</label>
                        <select class="form-select" id="atividade" name="atividade">
                            <option value="">Todas as atividades</option>
                            {% for atividade in atividades %}
                            <option value="{{ atividade.id }}">{{ atividade.nome }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="col-md-3">
                        <label for="data_inicio" class="form-label">Data Início</label>
                        <input type="date" class="form-control" id="data_inicio" name="data_inicio">
                    </div>
                    
                    <div class="col-md-3">
                        <label for="data_fim" class="form-label">Data Fim</label>
                        <input type="date" class="form-control" id="data_fim" name="data_fim">
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label for="status" class="form-label">Status</label>
                        <select class="form-select" id="status" name="status">
                            <option value="">Todos</option>
                            <option value="presente">Presente</option>
                            <option value="ausente">Ausente</option>
                        </select>
                    </div>
                    
                    <div class="col-md-6">
                        <label for="ordenar" class="form-label">Ordenar por</label>
                        <select class="form-select" id="ordenar" name="ordenar">
                            <option value="data">Data (mais recente primeiro)</option>
                            <option value="data_asc">Data (mais antiga primeiro)</option>
                            <option value="aluno">Nome do Aluno</option>
                            <option value="atividade">Nome da Atividade</option>
                        </select>
                    </div>
                </div>
                
                <div class="d-flex justify-content-between">
                    <button type="reset" class="btn btn-secondary">
                        <i class="fas fa-undo"></i> Limpar Filtros
                    </button>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-search"></i> Pesquisar
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
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
            
            $('#atividade').select2({
                theme: 'bootstrap-5',
                placeholder: 'Selecione uma atividade',
                allowClear: true
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
                            atividadeSelect.innerHTML = '<option value="">Todas as atividades</option>';
                            
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
{% endblock %}



### Arquivo: presencas\templates\presencas\ritualisticas\formulario_presenca_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">{{ titulo }}</h4>
                </div>
                <div class="card-body">
                    <form method="post" novalidate>
                        {% csrf_token %}
                        
                        {% if form.non_field_errors %}
                        <div class="alert alert-danger">
                            {% for error in form.non_field_errors %}
                            <p>{{ error }}</p>
                            {% endfor %}
                        </div>
                        {% endif %}
                        
                        <div class="mb-3">
                            <label for="{{ form.aluno.id_for_label }}" class="form-label">{{ form.aluno.label }}</label>
                            {{ form.aluno }}
                            {% if form.aluno.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.aluno.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.aluno.help_text %}
                            <div class="form-text">{{ form.aluno.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.atividade.id_for_label }}" class="form-label">{{ form.atividade.label }}</label>
                            {{ form.atividade }}
                            {% if form.atividade.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.atividade.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.atividade.help_text %}
                            <div class="form-text">{{ form.atividade.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.data.id_for_label }}" class="form-label">{{ form.data.label }}</label>
                            {{ form.data }}
                            {% if form.data.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.data.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.data.help_text %}
                            <div class="form-text">{{ form.data.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.situacao.id_for_label }}" class="form-label">{{ form.situacao.label }}</label>
                            {{ form.situacao }}
                            {% if form.situacao.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.situacao.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.situacao.help_text %}
                            <div class="form-text">{{ form.situacao.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3" id="justificativa-container">
                            <label for="{{ form.justificativa.id_for_label }}" class="form-label">{{ form.justificativa.label }}</label>
                            {{ form.justificativa }}
                            {% if form.justificativa.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.justificativa.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.justificativa.help_text %}
                            <div class="form-text">{{ form.justificativa.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="d-flex justify-content-between mt-4">
                            <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
                                <i class="fas fa-arrow-left"></i> Voltar
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Salvar
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Inicializar Select2 para melhorar a experiência de seleção
        $('.select2').select2({
            theme: 'bootstrap-5',
            width: '100%'
        });
        
        // Mostrar/ocultar campo de justificativa com base na situação
        const situacaoSelect = document.getElementById('id_situacao');
        const justificativaContainer = document.getElementById('justificativa-container');
        
        function toggleJustificativa() {
            if (situacaoSelect.value === 'JUSTIFICADO') {
                justificativaContainer.style.display = 'block';
                document.getElementById('id_justificativa').setAttribute('required', 'required');
            } else {
                justificativaContainer.style.display = 'none';
                document.getElementById('id_justificativa').removeAttribute('required');
            }
        }
        
        // Executar na inicialização
        toggleJustificativa();
        
        // Adicionar evento de mudança
        situacaoSelect.addEventListener('change', toggleJustificativa);
    });
</script>
{% endblock %}



### Arquivo: presencas\templates\presencas\ritualisticas\formulario_presencas_multiplas_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}Registro de Presenças{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Registro de Presenças</h1>
        <div>
            <a href="{% url 'presencas:registrar_presencas_multiplas' %}" class="btn btn-secondary me-2">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-outline-secondary">
                <i class="fas fa-list"></i> Lista de Presenças
            </a>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Informações do Registro</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-4">
                    <p><strong>Data:</strong> {{ data|date:"d/m/Y" }}</p>
                </div>
                <div class="col-md-8">
                    <p><strong>Turmas:</strong> 
                        {% for turma in turmas %}
                            <span class="badge bg-info">{{ turma.nome }}</span>
                        {% endfor %}
                    </p>
                </div>
            </div>
            <div class="row">
                <div class="col-12">
                    <p><strong>Atividades:</strong> 
                        {% for atividade in atividades %}
                            <span class="badge bg-success">{{ atividade.titulo }}</span>
                        {% endfor %}
                    </p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Lista de Alunos</h5>
                <div>
                    <button type="button" class="btn btn-success btn-sm me-2" id="btn-marcar-todos-presentes">
                        <i class="fas fa-check"></i> Marcar Todos Presentes
                    </button>
                    <button type="button" class="btn btn-danger btn-sm" id="btn-marcar-todos-ausentes">
                        <i class="fas fa-times"></i> Marcar Todos Ausentes
                    </button>
                </div>
            </div>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover" id="tabela-alunos">
                    <thead class="table-light">
                        <tr>
                            <th style="width: 40%">Aluno</th>
                            <th style="width: 20%">Atividade</th>
                            <th style="width: 20%">Situação</th>
                            <th style="width: 20%">Justificativa</th>
                        </tr>
                    </thead>
                    <tbody id="tbody-alunos">
                        <tr>
                            <td colspan="4" class="text-center py-4">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Carregando...</span>
                                </div>
                                <p class="mt-2">Carregando alunos...</p>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer">
            <div class="d-flex justify-content-between">
                <a href="{% url 'presencas:registrar_presencas_multiplas' %}" class="btn btn-secondary">Cancelar</a>
                <button type="button" class="btn btn-primary" id="btn-salvar-presencas">
                    <i class="fas fa-save"></i> Salvar Presenças
                </button>
            </div>
        </div>
    </div>
</div>

<!-- Template para linha de aluno -->
<template id="template-linha-aluno">
    <tr data-aluno-id="">
        <td>
            <div class="d-flex align-items-center">
                <div class="avatar-placeholder rounded-circle me-2 d-flex align-items-center justify-content-center" 
                     style="width: 40px; height: 40px; background-color: #6c757d; color: white;">
                </div>
                <div>
                    <div class="aluno-nome fw-bold"></div>
                    <small class="text-muted aluno-cpf"></small>
                </div>
            </div>
        </td>
        <td class="atividade-titulo"></td>
        <td>
            <select class="form-select form-select-sm situacao-select">
                <option value="PRESENTE">Presente</option>
                <option value="AUSENTE">Ausente</option>
                <option value="JUSTIFICADO">Justificado</option>
            </select>
        </td>
        <td>
            <input type="text" class="form-control form-control-sm justificativa-input" placeholder="Opcional" disabled>
        </td>
    </tr>
</template>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const data = '{{ data|date:"Y-m-d" }}';
        const turmasIds = [{% for turma in turmas %}'{{ turma.id }}'{% if not forloop.last %},{% endif %}{% endfor %}];
        const atividadesIds = [{% for atividade in atividades %}'{{ atividade.id }}'{% if not forloop.last %},{% endif %}{% endfor %}];
        
        const tbodyAlunos = document.getElementById('tbody-alunos');
        const templateLinhaAluno = document.getElementById('template-linha-aluno');
        const btnMarcarTodosPresentes = document.getElementById('btn-marcar-todos-presentes');
        const btnMarcarTodosAusentes = document.getElementById('btn-marcar-todos-ausentes');
        const btnSalvarPresencas = document.getElementById('btn-salvar-presencas');
        
        // Carregar alunos
        carregarAlunos();
        
        // Configurar eventos
        btnMarcarTodosPresentes.addEventListener('click', marcarTodosPresentes);
        btnMarcarTodosAusentes.addEventListener('click', marcarTodosAusentes);
        btnSalvarPresencas.addEventListener('click', salvarPresencas);
        
        // Função para carregar alunos
        function carregarAlunos() {
            fetch('{% url "presencas:api_obter_alunos_por_turmas" %}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({
                    turmas_ids: turmasIds
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    mostrarErro(data.error);
                    return;
                }
                
                // Limpar tabela
                tbodyAlunos.innerHTML = '';
                
                // Verificar se há alunos
                if (data.alunos.length === 0) {
                    tbodyAlunos.innerHTML = `
                        <tr>
                            <td colspan="4" class="text-center py-4">
                                <p class="text-muted mb-0">Nenhum aluno encontrado nas turmas selecionadas.</p>
                            </td>
                        </tr>
                    `;
                    return;
                }
                
                // Adicionar alunos à tabela
                data.alunos.forEach(aluno => {
                    atividadesIds.forEach(atividadeId => {
                        const atividade = data.atividades.find(a => a.id == atividadeId);
                        if (!atividade) return;
                        
                        adicionarLinhaAluno(aluno, atividade);
                    });
                });
                
                // Configurar eventos para os selects de situação
                document.querySelectorAll('.situacao-select').forEach(select => {
                    select.addEventListener('change', function() {
                        const justificativaInput = this.closest('tr').querySelector('.justificativa-input');
                        justificativaInput.disabled = this.value !== 'JUSTIFICADO';
                        
                        if (this.value !== 'JUSTIFICADO') {
                            justificativaInput.value = '';
                        }
                    });
                });
            })
            .catch(error => {
                console.error('Erro ao carregar alunos:', error);
                mostrarErro('Erro ao carregar alunos. Por favor, tente novamente.');
            });
        }
        
        // Função para adicionar linha de aluno
        function adicionarLinhaAluno(aluno, atividade) {
            const clone = document.importNode(templateLinhaAluno.content, true);
            const tr = clone.querySelector('tr');
            
            tr.dataset.alunoId = aluno.cpf;
            tr.dataset.atividadeId = atividade.id;
            
            // Configurar avatar
            const avatarPlaceholder = tr.querySelector('.avatar-placeholder');
            if (aluno.foto) {
                avatarPlaceholder.innerHTML = `<img src="${aluno.foto}" alt="Foto de ${aluno.nome}" class="rounded-circle" width="40" height="40" style="object-fit: cover;">`;
                avatarPlaceholder.className = 'me-2';
            } else {
                avatarPlaceholder.textContent = aluno.nome.charAt(0).toUpperCase();
            }
            
            // Configurar dados do aluno
            tr.querySelector('.aluno-nome').textContent = aluno.nome;
            tr.querySelector('.aluno-cpf').textContent = aluno.cpf;
            tr.querySelector('.atividade-titulo').textContent = atividade.titulo;
            
            tbodyAlunos.appendChild(tr);
        }
        
        // Função para marcar todos como presentes
        function marcarTodosPresentes() {
            document.querySelectorAll('.situacao-select').forEach(select => {
                select.value = 'PRESENTE';
                
                // Desabilitar campo de justificativa
                const justificativaInput = select.closest('tr').querySelector('.justificativa-input');
                justificativaInput.disabled = true;
                justificativaInput.value = '';
            });
        }
        
        // Função para marcar todos como ausentes
        function marcarTodosAusentes() {
            document.querySelectorAll('.situacao-select').forEach(select => {
                select.value = 'AUSENTE';
                
                // Desabilitar campo de justificativa
                const justificativaInput = select.closest('tr').querySelector('.justificativa-input');
                justificativaInput.disabled = true;
                justificativaInput.value = '';
            });
        }
        
        // Função para salvar presenças
        function salvarPresencas() {
            // Desabilitar botão para evitar múltiplos envios
            btnSalvarPresencas.disabled = true;
            btnSalvarPresencas.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Salvando...';
            
            // Coletar dados
            const presencas = [];
            
            document.querySelectorAll('#tbody-alunos tr[data-aluno-id]').forEach(tr => {
                const alunoId = tr.dataset.alunoId;
                const atividadeId = tr.dataset.atividadeId;
                const situacao = tr.querySelector('.situacao-select').value;
                const justificativa = tr.querySelector('.justificativa-input').value;
                
                presencas.push({
                    aluno_id: alunoId,
                    atividade_id: atividadeId,
                    data: data,
                    situacao: situacao,
                    justificativa: justificativa
                });
            });
            
            // Enviar dados
            fetch('{% url "presencas:api_salvar_presencas_multiplas" %}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({
                    presencas: presencas
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    mostrarErro(data.error);
                    return;
                }
                
                // Redirecionar para a lista de presenças
                window.location.href = '{% url "presencas:listar_presencas" %}';
            })
            .catch(error => {
                console.error('Erro ao salvar presenças:', error);
                mostrarErro('Erro ao salvar presenças. Por favor, tente novamente.');
            })
            .finally(() => {
                // Reabilitar botão
                btnSalvarPresencas.disabled = false;
                btnSalvarPresencas.innerHTML = '<i class="fas fa-save"></i> Salvar Presenças';
            });
        }
        
        // Função para mostrar erro
        function mostrarErro(mensagem) {
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-danger alert-dismissible fade show';
            alertDiv.innerHTML = `
                ${mensagem}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
            `;
            
            document.querySelector('.container-fluid').insertBefore(alertDiv, document.querySelector('.card'));
        }
        
        // Função para obter token CSRF
        function getCsrfToken() {
            return document.querySelector('input[name="csrfmiddlewaretoken"]')?.value || '';
        }
    });
</script>
{% endblock %}



### Arquivo: presencas\templates\presencas\ritualisticas\formulario_presencas_multiplas_ritualistica_passo1.html

html
{% extends 'base.html' %}

{% block title %}Registro de Presenças Múltiplas{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header bg-success text-white">
                    <h4 class="mb-0">Registro de Presenças Múltiplas - Passo 1</h4>
                </div>
                <div class="card-body">
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle me-2"></i>
                        Selecione a data, as turmas e as atividades para registrar presenças em massa.
                    </div>
                    
                    <form method="post" id="form-passo1" novalidate>
                        {% csrf_token %}
                        
                        {% if form.non_field_errors %}
                        <div class="alert alert-danger">
                            {% for error in form.non_field_errors %}
                            <p>{{ error }}</p>
                            {% endfor %}
                        </div>
                        {% endif %}
                        
                        <div class="mb-3">
                            <label for="{{ form.data.id_for_label }}" class="form-label">{{ form.data.label }}</label>
                            {{ form.data }}
                            {% if form.data.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.data.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.data.help_text %}
                            <div class="form-text">{{ form.data.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.turmas.id_for_label }}" class="form-label">{{ form.turmas.label }}</label>
                            {{ form.turmas }}
                            {% if form.turmas.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.turmas.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.turmas.help_text %}
                            <div class="form-text">{{ form.turmas.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.atividades.id_for_label }}" class="form-label">{{ form.atividades.label }}</label>
                            {{ form.atividades }}
                            {% if form.atividades.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.atividades.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.atividades.help_text %}
                            <div class="form-text">{{ form.atividades.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="d-flex justify-content-between mt-4">
                            <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
                                <i class="fas fa-arrow-left"></i> Voltar
                            </a>
                            <button type="submit" class="btn btn-success">
                                <i class="fas fa-arrow-right"></i> Próximo Passo
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Inicializar Select2 para melhorar a experiência de seleção
        $('.select2').select2({
            theme: 'bootstrap-5',
            width: '100%'
        });
        
        // Atualizar atividades quando a data mudar
        const dataInput = document.getElementById('id_data');
        const atividadesSelect = document.getElementById('id_atividades');
        
        dataInput.addEventListener('change', function() {
            const data = this.value;
            
            if (!data) return;
            
            // Fazer requisição AJAX para obter atividades da data
            fetch(`/presencas/api/obter-atividades-por-data/?data=${data}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error(data.error);
                        return;
                    }
                    
                    // Limpar opções atuais
                    atividadesSelect.innerHTML = '';
                    
                    // Adicionar novas opções
                    data.atividades.forEach(atividade => {
                        const option = document.createElement('option');
                        option.value = atividade.id;
                        option.textContent = atividade.titulo;
                        atividadesSelect.appendChild(option);
                    });
                    
                    // Atualizar Select2
                    $(atividadesSelect).trigger('change');
                })
                .catch(error => {
                    console.error('Erro ao carregar atividades:', error);
                });
        });
    });
</script>
{% endblock %}



### Arquivo: presencas\templates\presencas\ritualisticas\formulario_presencas_multiplas_ritualistica_passo2.html

html
{% extends 'base.html' %}

{% block title %}Registro de Presenças Múltiplas - Passo 2{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="card">
        <div class="card-header bg-success text-white">
            <div class="d-flex justify-content-between align-items-center">
                <h4 class="mb-0">Registro de Presenças Múltiplas - Passo 2</h4>
                <div>
                    <span class="badge bg-light text-dark">Data: {{ data_formatada }}</span>
                </div>
            </div>
        </div>
        <div class="card-body">
            <div class="alert alert-info">
                <i class="fas fa-info-circle me-2"></i>
                Marque a situação de presença para cada aluno nas atividades selecionadas.
            </div>
            
            <div class="mb-3">
                <h5>Turmas selecionadas:</h5>
                <div class="d-flex flex-wrap gap-2">
                    {% for turma in turmas %}
                    <span class="badge bg-primary">{{ turma.nome }}</span>
                    {% endfor %}
                </div>
            </div>
            
            <div class="mb-3">
                <h5>Atividades selecionadas:</h5>
                <div class="d-flex flex-wrap gap-2">
                    {% for atividade in atividades %}
                    <span class="badge bg-info">{{ atividade.titulo }}</span>
                    {% endfor %}
                </div>
            </div>
            
            <form id="form-presencas-multiplas">
                {% csrf_token %}
                <input type="hidden" name="data" value="{{ data }}">
                
                <div class="table-responsive">
                    <table class="table table-striped table-bordered">
                        <thead class="table-dark">
                            <tr>
                                <th style="width: 30%">Aluno</th>
                                {% for atividade in atividades %}
                                <th>{{ atividade.titulo }}</th>
                                {% endfor %}
                            </tr>
                        </thead>
                        <tbody>
                            {% for aluno in alunos %}
                            <tr>
                                <td>
                                    <div class="d-flex align-items-center">
                                        {% if aluno.foto %}
                                        <img src="{{ aluno.foto.url }}" alt="{{ aluno.nome }}" 
                                             class="rounded-circle me-2" width="40" height="40">
                                        {% else %}
                                        <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-2"
                                             style="width: 40px; height: 40px; color: white;">
                                            {{ aluno.nome|first|upper }}
                                        </div>
                                        {% endif %}
                                        <div>
                                            <div>{{ aluno.nome }}</div>
                                            <small class="text-muted">{{ aluno.cpf }}</small>
                                        </div>
                                    </div>
                                </td>
                                
                                {% for atividade in atividades %}
                                <td>
                                    {% with key=aluno.cpf|add:'_'|add:atividade.id|stringformat:'s' %}
                                    {% with presenca=presencas_dict|get_item:key %}
                                    <div class="btn-group" role="group">
                                        <input type="radio" class="btn-check" name="presenca_{{ aluno.cpf }}_{{ atividade.id }}" 
                                               id="presente_{{ aluno.cpf }}_{{ atividade.id }}" value="PRESENTE"
                                               {% if presenca and presenca.situacao == 'PRESENTE' %}checked{% elif not presenca %}checked{% endif %}>
                                        <label class="btn btn-outline-success



### Arquivo: presencas\templates\presencas\ritualisticas\historico_presencas_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}Histórico de Presenças - {{ aluno.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Histórico de Presenças</h1>
        <div>
            <a href="{% url 'alunos:detalhar_aluno' aluno.cpf %}" class="btn btn-secondary me-2">
                <i class="fas fa-user"></i> Perfil do Aluno
            </a>
            <a href="{% url 'presencas:exportar_historico' aluno.cpf %}" class="btn btn-success">
                <i class="fas fa-file-csv"></i> Exportar CSV
            </a>
        </div>
    </div>
    
    <!-- Informações do aluno -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Informações do Aluno</h5>
        </div>
        <div class="card-body">
            <div class="d-flex align-items-center">
                {% if aluno.foto %}
                <img src="{{ aluno.foto.url }}" alt="{{ aluno.nome }}" 
                     class="rounded-circle me-3" width="60" height="60" style="object-fit: cover;">
                {% else %}
                <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-3"
                     style="width: 60px; height: 60px; color: white; font-size: 1.5rem;">
                    {{ aluno.nome|first|upper }}
                </div>
                {% endif %}
                <div>
                    <h5 class="mb-1">{{ aluno.nome }}</h5>
                    <p class="mb-0">{{ aluno.email }}</p>
                    <p class="mb-0">CPF: {{ aluno.cpf }}</p>
                </div>
            </div>
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
                    <label for="atividade" class="form-label">Atividade</label>
                    <select class="form-select" id="atividade" name="atividade">
                        <option value="">Todas as atividades</option>
                        {% for atividade in atividades %}
                        <option value="{{ atividade.id }}" {% if filtros.atividade == atividade.id|stringformat:"s" %}selected{% endif %}>
                            {{ atividade.nome }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="col-md-4">
                    <label for="data_inicio" class="form-label">Data Início</label>
                    <input type="date" class="form-control" id="data_inicio" name="data_inicio" value="{{ filtros.data_inicio }}">
                </div>
                
                <div class="col-md-4">
                    <label for="data_fim" class="form-label">Data Fim</label>
                    <input type="date" class="form-control" id="data_fim" name="data_fim" value="{{ filtros.data_fim }}">
                </div>
                
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                    <a href="{% url 'presencas:historico_presencas' aluno.cpf %}" class="btn btn-secondary">
                        <i class="fas fa-undo"></i> Limpar Filtros
                    </a>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Estatísticas -->
    <div class="card mb-4">
        <div class="card-header bg-success text-white">
            <h5 class="mb-0">Estatísticas</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-4">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Total de Presenças</h5>
                            <p class="card-text display-4">{{ total_presencas }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Total de Faltas</h5>
                            <p class="card-text display-4">{{ total_faltas }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Percentual de Presença</h5>
                            <p class="card-text display-4">{{ percentual_presenca|floatformat:1 }}%</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Lista de presenças -->
    <div class="card">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Registros de Presença</h5>
        </div>
        <div class="card-body">
            {% if presencas %}
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Data</th>
                            <th>Atividade</th>
                            <th>Turma</th>
                            <th>Status</th>
                            <th>Justificativa</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for presenca in presencas %}
                        <tr>
                            <td>{{ presenca.data|date:"d/m/Y" }}</td>
                            <td>{{ presenca.atividade.nome }}</td>
                            <td>{{ presenca.atividade.turma.nome }}</td>
                            <td>
                                {% if presenca.presente %}
                                <span class="badge bg-success">Presente</span>
                                {% else %}
                                <span class="badge bg-danger">Ausente</span>
                                {% endif %}
                            </td>
                            <td>{{ presenca.justificativa|default:"-"|truncatechars:50 }}</td>
                            <td>
                                <div class="table-actions">
                                    <a href="{% url 'presencas:detalhar_presenca' presenca.id %}" class="btn btn-sm btn-info" title="Ver detalhes da presença">
                                        <i class="fas fa-eye"></i>
                                    </a>
                                    <a href="{% url 'presencas:editar_presenca' presenca.id %}" class="btn btn-sm btn-warning" title="Editar presença">
                                        <i class="fas fa-edit"></i>
                                    </a>
                                </div>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="alert alert-info">
                <i class="fas fa-info-circle me-2"></i>
                Não há registros de presença para este aluno com os filtros selecionados.
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: presencas\templates\presencas\ritualisticas\importar_presencas_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}Importar Presenças{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Importar Presenças</h1>
    
    <div class="card">
        <div class="card-body">
            <p class="mb-3">Faça upload de um arquivo CSV contendo os dados de presenças.</p>
            
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                <div class="mb-3">
                    <label for="csv_file" class="form-label">Arquivo CSV</label>
                    <input type="file" name="csv_file" id="csv_file" class="form-control" accept=".csv" required>
                    <div class="form-text">O arquivo deve ter cabeçalhos: Aluno (CPF), Turma, Data, Presente, Justificativa</div>
                </div>
                
                <div class="d-flex">
                    <button type="submit" class="btn btn-primary me-2">Importar</button>
                    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
    
    <div class="mt-3">
        <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-link">Voltar para a lista de presenças</a>
    </div>
</div>
{% endblock %}



### Arquivo: presencas\templates\presencas\ritualisticas\importar_presencas_ritualisticas.html

html
{% extends 'base.html' %}

{% block title %}Importar Presenças Ritualísticas{% endblock %}

{% block content %}
<div class="container mt-4">
    <h2>Importação de Presenças Ritualísticas</h2>
    <p>Funcionalidade de importação de presenças ritualísticas. Implemente aqui a lógica de importação (CSV, Excel, etc).</p>
    <a href="{% url 'presencas:listar_presencas_ritualisticas' %}" class="btn btn-secondary mt-3">Voltar</a>
</div>
{% endblock %}



### Arquivo: presencas\templates\presencas\ritualisticas\listar_observacoes_presenca_ritualistica.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Detalhes da Presença</h1>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Informações do Registro</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Aluno:</strong> {{ presenca.aluno.nome }}</p>
                    <p><strong>Turma:</strong> {{ presenca.turma.nome }}</p>
                    <p><strong>Data:</strong> {{ presenca.data|date:"d/m/Y" }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Status:</strong> {% if presenca.presente %}Presente{% else %}Ausente{% endif %}</p>
                    <p><strong>Registrado por:</strong> {{ presenca.registrado_por.username }}</p>
                    <p><strong>Data de Registro:</strong> {{ presenca.data_registro|date:"d/m/Y H:i" }}</p>
                </div>
            </div>

            {% if presenca.justificativa %}
            <div class="mt-3">
                <h6>Justificativa:</h6>
                <div class="p-3 bg-light rounded">
                    {{ presenca.justificativa }}
                </div>
            </div>
            {% endif %}
        </div>
        <div class="card-footer">
            <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
                <i class="fas fa-list"></i> Voltar para a lista
            </a>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: presencas\templates\presencas\ritualisticas\listar_presencas_ritualisticas.html

html
{% extends 'base.html' %}

{% block title %}Listar Presenças Ritualísticas{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <!-- Padronizar cabeçalho com botões -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Presenças Ritualísticas</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'presencas:registrar_presenca_ritualistica' %}" class="btn btn-primary me-2">
                <i class="fas fa-plus"></i> Registrar Presença
            </a>
            <a href="{% url 'presencas:exportar_presencas_ritualisticas' %}" class="btn btn-success me-2">
                <i class="fas fa-file-export"></i> Exportar CSV
            </a>
            <a href="{% url 'presencas:importar_presencas_ritualisticas' %}" class="btn btn-info">
                <i class="fas fa-file-import"></i> Importar CSV
            </a>
        </div>
    </div>
    
    <!-- Filtros avançados -->
    <div class="card mb-4">
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
                
                <div class="col-md-2">
                    <label for="data_inicio" class="form-label">Data Início</label>
                    <input type="date" class="form-control" id="data_inicio" name="data_inicio" value="{{ filtros.data_inicio }}">
                </div>
                
                <div class="col-md-2">
                    <label for="data_fim" class="form-label">Data Fim</label>
                    <input type="date" class="form-control" id="data_fim" name="data_fim" value="{{ filtros.data_fim }}">
                </div>
                
                <div class="col-md-2">
                    <label for="presente" class="form-label">Status</label>
                    <select name="presente" id="presente" class="form-select">
                        <option value="">Todos</option>
                        <option value="true" {% if filtros.presente == 'true' %}selected{% endif %}>Presente</option>
                        <option value="false" {% if filtros.presente == 'false' %}selected{% endif %}>Ausente</option>
                    </select>
                </div>
                
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                    <a href="{% url 'presencas:listar_presencas_ritualisticas' %}" class="btn btn-secondary">
                        <i class="fas fa-undo"></i> Limpar Filtros
                    </a>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Tabela de presenças -->
    <div class="card">
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Aluno</th>
                            <th>Atividade</th>
                            <th>Turma</th>
                            <th>Data</th>
                            <th>Status</th>
                            <th>Justificativa</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for presenca in presencas %}
                        <tr>
                            <td>
                                <div class="d-flex align-items-center">
                                    {% if presenca.aluno.foto %}
                                    <img src="{{ presenca.aluno.foto.url }}" alt="{{ presenca.aluno.nome }}" 
                                         class="rounded-circle me-2" width="40" height="40" style="object-fit: cover;">
                                    {% else %}
                                    <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-2"
                                         style="width: 40px; height: 40px; color: white;">
                                        {{ presenca.aluno.nome|first|upper }}
                                    </div>
                                    {% endif %}
                                    <div>
                                        <div>{{ presenca.aluno.nome }}</div>
                                        <small class="text-muted">{{ presenca.aluno.cpf }}</small>
                                    </div>
                                </div>
                            </td>
                            <td>{{ presenca.atividade.nome }}</td>
                            <td>{{ presenca.atividade.turma.nome }}</td>
                            <td>{{ presenca.data|date:"d/m/Y" }}</td>
                            <td>
                                {% if presenca.presente %}
                                <span class="badge bg-success">Presente</span>
                                {% else %}
                                <span class="badge bg-danger">Ausente</span>
                                {% endif %}
                            </td>
                            <td>{{ presenca.justificativa|truncatechars:30|default:"-" }}</td>
                            <td>
                                <div class="table-actions">
                                    <a href="{% url 'presencas:detalhar_presenca_ritualistica' presenca.id %}" class="btn btn-sm btn-info" title="Ver detalhes da presença">
                                        <i class="fas fa-eye"></i> Detalhes
                                    </a>
                                    <a href="{% url 'presencas:editar_presenca_ritualistica' presenca.id %}" class="btn btn-sm btn-warning" title="Editar presença">
                                        <i class="fas fa-edit"></i> Editar
                                    </a>
                                    <a href="{% url 'presencas:excluir_presenca_ritualistica' presenca.id %}" class="btn btn-sm btn-danger" title="Excluir presença">
                                        <i class="fas fa-trash"></i> Excluir
                                    </a>
                                </div>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="7" class="text-center py-3">
                                <p class="mb-0">Nenhum registro de presença encontrado com os filtros selecionados.</p>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer d-flex justify-content-between align-items-center">
            <div>
                <p class="mb-0">Exibindo {{ presencas|length }} de {{ page_obj.paginator.count }} registros</p>
            </div>
            
            {% if page_obj.has_other_pages %}
            <nav aria-label="Paginação">
                <ul class="pagination mb-0">
                    {% if page_obj.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% for key, value in filtros.items %}&{{ key }}={{ value }}{% endfor %}" aria-label="Anterior">
                            <span aria-hidden="true">«</span>
                        </a>
                    </li>
                    {% else %}
                    <li class="page-item disabled">
                        <span class="page-link" aria-hidden="true">«</span>
                    </li>
                    {% endif %}
                    
                    {% for i in page_obj.paginator.page_range %}
                        {% if page_obj.number == i %}
                        <li class="page-item active"><span class="page-link">{{ i }}</span></li>
                        {% else %}
                        <li class="page-item">
                            <a class="page-link" href="?page={{ i }}{% for key, value in filtros.items %}&{{ key }}={{ value }}{% endfor %}">{{ i }}</a>
                        </li>
                        {% endif %}
                    {% endfor %}
                    
                    {% if page_obj.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.next_page_number }}{% for key, value in filtros.items %}&{{ key }}={{ value }}{% endfor %}" aria-label="Próxima">
                            <span aria-hidden="true">»</span>
                        </a>
                    </li>
                    {% else %}
                    <li class="page-item disabled">
                        <span class="page-link" aria-hidden="true">»</span>
                    </li>
                    {% endif %}
                </ul>
            </nav>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
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
{% endblock %}




### Arquivo: presencas\templates\presencas\ritualisticas\registrar_presenca_em_massa_ritualistica.html

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



### Arquivo: presencas\templates\presencas\ritualisticas\registrar_presenca_ritualistica.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Registrar Presença</h1>

    <div class="card mb-4">
        <div class="card-body">
            <form method="post">
                {% csrf_token %}

                {% for field in form %}
                <div class="mb-3">
                    <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                    {{ field }}
                    {% if field.errors %}
                        <div class="invalid-feedback">
                            {{ field.errors }}
                        </div>
                    {% endif %}
                </div>
                {% endfor %}
                <!-- Padronizar botões no formulário -->
                <div class="d-flex justify-content-between mt-4">
                    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
                        <i class="fas fa-times"></i> Cancelar
                    </a>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-save"></i> Registrar Presenças
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: presencas\templates\presencas\ritualisticas\registrar_presencas_multiplas_ritualistica.html

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


'''