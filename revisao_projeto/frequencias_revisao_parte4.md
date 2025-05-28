'''
# Revisão da Funcionalidade: frequencias

## Arquivos forms.py:


### Arquivo: frequencias\templates\frequencias\notificacoes_carencia.html

html
{% extends 'base.html' %}

{% block title %}Notificações de Carência{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Notificações de Carência</h1>
        <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-3">
                    <label for="turma" class="form-label">Turma</label>
                    <select name="turma" id="turma" class="form-select select2">
                        <option value="">Todas as turmas</option>
                        {% for turma in turmas %}
                        <option value="{{ turma.id }}" {% if request.GET.turma == turma.id|stringformat:"s" %}selected{% endif %}>
                            {{ turma.nome }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="status" class="form-label">Status</label>
                    <select name="status" id="status" class="form-select">
                        <option value="">Todos os status</option>
                        <option value="PENDENTE" {% if request.GET.status == "PENDENTE" %}selected{% endif %}>Pendente</option>
                        <option value="ENVIADA" {% if request.GET.status == "ENVIADA" %}selected{% endif %}>Enviada</option>
                        <option value="LIDA" {% if request.GET.status == "LIDA" %}selected{% endif %}>Lida</option>
                        <option value="RESPONDIDA" {% if request.GET.status == "RESPONDIDA" %}selected{% endif %}>Respondida</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="periodo" class="form-label">Período</label>
                    <select name="periodo" id="periodo" class="form-select">
                        <option value="">Todos os períodos</option>
                        <option value="7" {% if request.GET.periodo == "7" %}selected{% endif %}>Últimos 7 dias</option>
                        <option value="30" {% if request.GET.periodo == "30" %}selected{% endif %}>Últimos 30 dias</option>
                        <option value="90" {% if request.GET.periodo == "90" %}selected{% endif %}>Últimos 90 dias</option>
                    </select>
                </div>
                <div class="col-12 mt-3">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                    <a href="{% url 'frequencias:notificacoes_carencia' %}" class="btn btn-secondary">
                        <i class="fas fa-broom"></i> Limpar Filtros
                    </a>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Estatísticas -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card bg-primary text-white">
                <div class="card-body">
                    <h5 class="card-title">Total de Notificações</h5>
                    <p class="card-text display-4">{{ total_notificacoes }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-warning text-dark">
                <div class="card-body">
                    <h5 class="card-title">Pendentes</h5>
                    <p class="card-text display-4">{{ notificacoes_pendentes }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-info text-white">
                <div class="card-body">
                    <h5 class="card-title">Enviadas</h5>
                    <p class="card-text display-4">{{ notificacoes_enviadas }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-success text-white">
                <div class="card-body">
                    <h5 class="card-title">Respondidas</h5>
                    <p class="card-text display-4">{{ notificacoes_respondidas }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Lista de notificações -->
    <div class="card">
        <div class="card-header bg-light d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Lista de Notificações</h5>
            <div>
                <button id="btn-enviar-selecionadas" class="btn btn-primary btn-sm" disabled>
                    <i class="fas fa-paper-plane"></i> Enviar Selecionadas
                </button>
                <button id="btn-marcar-todas" class="btn btn-secondary btn-sm">
                    <i class="fas fa-check-square"></i> Marcar Todas
                </button>
                <button id="btn-desmarcar-todas" class="btn btn-outline-secondary btn-sm">
                    <i class="fas fa-square"></i> Desmarcar Todas
                </button>
            </div>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" id="selecionar-todas">
                                </div>
                            </th>
                            <th>Aluno</th>
                            <th>Turma</th>
                            <th>Período</th>
                            <th>Percentual</th>
                            <th>Status</th>
                            <th>Data de Envio</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for notificacao in notificacoes %}
                        <tr>
                            <td>
                                <div class="form-check">
                                    <input class="form-check-input notificacao-checkbox" type="checkbox" 
                                           value="{{ notificacao.id }}" 
                                           {% if notificacao.status != 'PENDENTE' %}disabled{% endif %}>
                                </div>
                            </td>
                            <td>
                                <div class="d-flex align-items-center">
                                    {% if notificacao.carencia.aluno.foto %}
                                    <img src="{{ notificacao.carencia.aluno.foto.url }}" alt="{{ notificacao.carencia.aluno.nome }}" 
                                         class="rounded-circle me-2" width="40" height="40">
                                    {% else %}
                                    <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-2"
                                         style="width: 40px; height: 40px; color: white;">
                                        {{ notificacao.carencia.aluno.nome|first|upper }}
                                    </div>
                                    {% endif %}
                                    <div>
                                        <div>{{ notificacao.carencia.aluno.nome }}</div>
                                        <small class="text-muted">{{ notificacao.carencia.aluno.cpf }}</small>
                                    </div>
                                </div>
                            </td>
                            <td>{{ notificacao.carencia.frequencia_mensal.turma.nome }}</td>
                            <td>{{ notificacao.carencia.frequencia_mensal.get_mes_display }}/{{ notificacao.carencia.frequencia_mensal.ano }}</td>
                            <td>
                                <div class="progress" style="height: 20px;">
                                    <div class="progress-bar bg-danger" role="progressbar" 
                                         style="width: {{ notificacao.carencia.percentual_presenca }}%;" 
                                         aria-valuenow="{{ notificacao.carencia.percentual_presenca }}" 
                                         aria-valuemin="0" aria-valuemax="100">
                                        {{ notificacao.carencia.percentual_presenca }}%
                                    </div>
                                </div>
                            </td>
                            <td>
                                {% if notificacao.status == 'PENDENTE' %}
                                <span class="badge bg-warning text-dark">Pendente</span>
                                {% elif notificacao.status == 'ENVIADA' %}
                                <span class="badge bg-info">Enviada</span>
                                {% elif notificacao.status == 'LIDA' %}
                                <span class="badge bg-primary">Lida</span>
                                {% elif notificacao.status == 'RESPONDIDA' %}
                                <span class="badge bg-success">Respondida</span>
                                {% endif %}
                            </td>
                            <td>{{ notificacao.data_envio|date:"d/m/Y H:i"|default:"-" }}</td>
                            <td>
                                <div class="btn-group">
                                    <a href="{% url 'frequencias:detalhar_notificacao' notificacao.id %}" 
                                       class="btn btn-sm btn-info" title="Ver detalhes">
                                        <i class="fas fa-eye"></i>
                                    </a>
                                    {% if notificacao.status == 'PENDENTE' %}
                                    <a href="{% url 'frequencias:enviar_notificacao' notificacao.id %}" 
                                       class="btn btn-sm btn-primary" title="Enviar notificação">
                                        <i class="fas fa-paper-plane"></i>
                                    </a>
                                    {% endif %}
                                    {% if notificacao.status == 'RESPONDIDA' %}
                                    <a href="{% url 'frequencias:visualizar_resposta' notificacao.id %}" 
                                       class="btn btn-sm btn-success" title="Ver resposta">
                                        <i class="fas fa-reply"></i>
                                    </a>
                                    {% endif %}
                                </div>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="8" class="text-center py-4">
                                <div class="alert alert-info mb-0">
                                    Nenhuma notificação encontrada com os filtros selecionados.
                                </div>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            
            <!-- Paginação -->
            {% if page_obj.has_other_pages %}
            <nav aria-label="Paginação" class="mt-4">
                <ul class="pagination justify-content-center">
                    {% if page_obj.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page=1{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                            <i class="fas fa-angle-double-left"></i>
                        </a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                            <i class="fas fa-angle-left"></i>
                        </a>
                    </li>
                    {% else %}
                    <li class="page-item disabled">
                        <span class="page-link"><i class="fas fa-angle-double-left"></i></span>
                    </li>
                    <li class="page-item disabled">
                        <span class="page-link"><i class="fas fa-angle-left"></i></span>
                    </li>
                    {% endif %}
                    
                    {% for num in page_obj.paginator.page_range %}
                        {% if page_obj.number == num %}
                        <li class="page-item active">
                            <span class="page-link">{{ num }}</span>
                        </li>
                        {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                        <li class="page-item">
                            <a class="page-link" href="?page={{ num }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                                {{ num }}
                            </a>
                        </li>
                        {% endif %}
                    {% endfor %}
                    
                    {% if page_obj.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.next_page_number }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                            <i class="fas fa-angle-right"></i>
                        </a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                            <i class="fas fa-angle-double-right"></i>
                        </a>
                    </li>
                    {% else %}
                    <li class="page-item disabled">
                        <span class="page-link"><i class="fas fa-angle-right"></i></span>
                    </li>
                    <li class="page-item disabled">
                        <span class="page-link"><i class="fas fa-angle-double-right"></i></span>
                    </li>
                    {% endif %}
                </ul>
            </nav>
            {% endif %}
        </div>
        <div class="card-footer">
            <div class="d-flex justify-content-between align-items-center">
                <span>Total: {{ page_obj.paginator.count }} notificações</span>
                <span>Página {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}</span>
            </div>
        </div>
    </div>
</div>

<!-- Modal de confirmação para envio em massa -->
<div class="modal fade" id="modalEnvioMassa" tabindex="-1" aria-labelledby="modalEnvioMassaLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="modalEnvioMassaLabel">Confirmar Envio de Notificações</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
            </div>
            <div class="modal-body">
                <p>Você está prestes a enviar <span id="qtd-notificacoes-selecionadas">0</span> notificações de carência.</p>
                <p>Esta ação enviará e-mails para os alunos selecionados. Deseja continuar?</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="button" class="btn btn-primary" id="btn-confirmar-envio">Confirmar Envio</button>
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
        
        // Gerenciar seleção de notificações
        const checkboxes = document.querySelectorAll('.notificacao-checkbox');
        const selecionarTodas = document.getElementById('selecionar-todas');
        const btnEnviarSelecionadas = document.getElementById('btn-enviar-selecionadas');
        const btnMarcarTodas = document.getElementById('btn-marcar-todas');
        const btnDesmarcarTodas = document.getElementById('btn-desmarcar-todas');
        const qtdNotificacoesSelecionadas = document.getElementById('qtd-notificacoes-selecionadas');
        
        // Modal de confirmação
        const modalEnvioMassa = new bootstrap.Modal(document.getElementById('modalEnvioMassa'));
        const btnConfirmarEnvio = document.getElementById('btn-confirmar-envio');
        
        // Função para atualizar o estado do botão de envio
        function atualizarBotaoEnvio() {
            const selecionadas = document.querySelectorAll('.notificacao-checkbox:checked');
            btnEnviarSelecionadas.disabled = selecionadas.length === 0;
            qtdNotificacoesSelecionadas.textContent = selecionadas.length;
        }
        
        // Evento para o checkbox "selecionar todas"
        selecionarTodas.addEventListener('change', function() {
            checkboxes.forEach(checkbox => {
                if (!checkbox.disabled) {
                    checkbox.checked = this.checked;
                }
            });
            atualizarBotaoEnvio();
        });
        
        // Evento para os checkboxes individuais
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                atualizarBotaoEnvio();
                
                // Verificar se todos estão selecionados
                const todosCheckboxes = document.querySelectorAll('.notificacao-checkbox:not(:disabled)');
                const todosSelecionados = document.querySelectorAll('.notificacao-checkbox:not(:disabled):checked');
                selecionarTodas.checked = todosCheckboxes.length === todosSelecionados.length;
            });
        });
        
        // Botão para marcar todas
        btnMarcarTodas.addEventListener('click', function() {
            checkboxes.forEach(checkbox => {
                if (!checkbox.disabled) {
                    checkbox.checked = true;
                }
            });
            selecionarTodas.checked = true;
            atualizarBotaoEnvio();
        });
        
        // Botão para desmarcar todas
        btnDesmarcarTodas.addEventListener('click', function() {
            checkboxes.forEach(checkbox => {
                checkbox.checked = false;
            });
            selecionarTodas.checked = false;
            atualizarBotaoEnvio();
        });
        
        // Botão para enviar selecionadas
        btnEnviarSelecionadas.addEventListener('click', function() {
            modalEnvioMassa.show();
        });
        
        // Botão para confirmar envio
        btnConfirmarEnvio.addEventListener('click', function() {
            // Obter IDs das notificações selecionadas
            const selecionadas = Array.from(document.querySelectorAll('.notificacao-checkbox:checked')).map(cb => cb.value);
            
            // Enviar requisição AJAX para o backend
            fetch('{% url "frequencias:enviar_notificacoes_massa" %}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: JSON.stringify({
                    notificacoes: selecionadas
                })
            })
            .then(response => response.json())
            .then(data => {
                modalEnvioMassa.hide();
                
                if (data.success) {
                    // Mostrar mensagem de sucesso
                    const alertDiv = document.createElement('div');
                    alertDiv.className = 'alert alert-success alert-dismissible fade show';
                    alertDiv.innerHTML = `
                        <strong>Sucesso!</strong> ${data.message}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
                    `;
                    document.querySelector('.container').prepend(alertDiv);
                    
                    // Recarregar a página após 2 segundos
                    setTimeout(() => {
                        window.location.reload();
                    }, 2000);
                } else {
                    // Mostrar mensagem de erro
                    const alertDiv = document.createElement('div');
                    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
                    alertDiv.innerHTML = `
                        <strong>Erro!</strong> ${data.message}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
                    `;
                    document.querySelector('.container').prepend(alertDiv);
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                modalEnvioMassa.hide();
                
                // Mostrar mensagem de erro
                const alertDiv = document.createElement('div');
                alertDiv.className = 'alert alert-danger alert-dismissible fade show';
                alertDiv.innerHTML = `
                    <strong>Erro!</strong> Ocorreu um erro ao processar sua solicitação.
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
                `;
                document.querySelector('.container').prepend(alertDiv);
            });
        });
        
        // Inicializar o estado do botão
        atualizarBotaoEnvio();
    });
</script>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\painel_frequencias.html

html
{% extends 'base.html' %}

{% block title %}Painel de Frequências{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Painel de Frequências</h1>
        <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-3">
                    <label for="turma" class="form-label">Turma</label>
                    <select name="turma" id="turma" class="form-select select2">
                        <option value="">Todas as turmas</option>
                        {% for turma in turmas %}
                        <option value="{{ turma.id }}" {% if request.GET.turma == turma.id|stringformat:"s" %}selected{% endif %}>
                            {{ turma.nome }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="ano" class="form-label">Ano</label>
                    <select name="ano" id="ano" class="form-select">
                        <option value="">Todos os anos</option>
                        {% for ano in anos %}
                        <option value="{{ ano }}" {% if request.GET.ano == ano|stringformat:"s" %}selected{% endif %}>
                            {{ ano }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-12 mt-3">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                    <a href="{% url 'frequencias:painel_frequencias' %}" class="btn btn-secondary">
                        <i class="fas fa-broom"></i> Limpar Filtros
                    </a>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Resumo em cards -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card bg-primary text-white">
                <div class="card-body">
                    <h5 class="card-title">Total de Frequências</h5>
                    <p class="card-text display-4">{{ total_frequencias }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-success text-white">
                <div class="card-body">
                    <h5 class="card-title">Média de Presença</h5>
                    <p class="card-text display-4">{{ media_presenca|floatformat:1 }}%</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-danger text-white">
                <div class="card-body">
                    <h5 class="card-title">Total de Carências</h5>
                    <p class="card-text display-4">{{ total_carencias }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-warning text-dark">
                <div class="card-body">
                    <h5 class="card-title">Carências Resolvidas</h5>
                    <p class="card-text display-4">{{ carencias_resolvidas }}</p>
                    <p class="card-text">
                        {% if total_carencias > 0 %}
                        {{ carencias_resolvidas|multiply:100|divide:total_carencias|floatformat:1 }}%
                        {% else %}
                        0%
                        {% endif %}
                    </p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Gráficos -->
    <div class="row">
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header bg-light">
                    <h5 class="mb-0">Frequência Mensal</h5>
                </div>
                <div class="card-body">
                    <canvas id="grafico-mensal"></canvas>
                </div>
            </div>
        </div>
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header bg-light">
                    <h5 class="mb-0">Carências por Turma</h5>
                </div>
                <div class="card-body">
                    <canvas id="grafico-carencias-turma"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-12 mb-4">
            <div class="card">
                <div class="card-header bg-light">
                    <h5 class="mb-0">Evolução de Carências</h5>
                </div>
                <div class="card-body">
                    <canvas id="grafico-evolucao-carencias"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Tabela de turmas com mais carências -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Turmas com Mais Carências</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Turma</th>
                            <th>Curso</th>
                            <th>Total de Carências</th>
                            <th>Carências Resolvidas</th>
                            <th>Percentual Resolvido</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for turma in turmas_mais_carencias %}
                        <tr>
                            <td>{{ turma.nome }}</td>
                            <td>{{ turma.curso.nome }}</td>
                            <td>{{ turma.total_carencias }}</td>
                            <td>{{ turma.carencias_resolvidas }}</td>
                            <td>
                                <div class="progress" style="height: 20px;">
                                    <div class="progress-bar bg-success" role="progressbar" 
                                         style="width: {{ turma.percentual_resolvido }}%;" 
                                         aria-valuenow="{{ turma.percentual_resolvido }}" 
                                         aria-valuemin="0" aria-valuemax="100">
                                        {{ turma.percentual_resolvido }}%
                                    </div>
                                </div>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="5" class="text-center py-4">
                                <div class="alert alert-info mb-0">
                                    Nenhuma turma com carências encontrada.
                                </div>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Inicializar Select2 para melhorar a experiência de seleção
        $('.select2').select2({
            theme: 'bootstrap-5',
            width: '100%'
        });
        
        // Gráfico mensal (linha)
        const ctxMensal = document.getElementById('grafico-mensal').getContext('2d');
        new Chart(ctxMensal, {
            type: 'line',
            data: {
                labels: {{ meses|safe }},
                datasets: [
                    {
                        label: 'Média de Presença',
                        data: {{ media_presenca_por_mes|safe }},
                        borderColor: 'rgba(40, 167, 69, 1)',
                        backgroundColor: 'rgba(40, 167, 69, 0.1)',
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
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
                }
            }
        });
        
        // Gráfico de carências por turma (barra)
        const ctxCarenciasTurma = document.getElementById('grafico-carencias-turma').getContext('2d');
        new Chart(ctxCarenciasTurma, {
            type: 'bar',
            data: {
                labels: {{ turmas_labels|safe }},
                datasets: [
                    {
                        label: 'Carências',
                        data: {{ carencias_por_turma|safe }},
                        backgroundColor: 'rgba(220, 53, 69, 0.7)',
                        borderColor: 'rgba(220, 53, 69, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Resolvidas',
                        data: {{ carencias_resolvidas_por_turma|safe }},
                        backgroundColor: 'rgba(40, 167, 69, 0.7)',
                        borderColor: 'rgba(40, 167, 69, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        
        // Gráfico de evolução de carências (linha)
        const ctxEvolucaoCarencias = document.getElementById('grafico-evolucao-carencias').getContext('2d');
        new Chart(ctxEvolucaoCarencias, {
            type: 'line',
            data: {
                labels: {{ meses_completos|safe }},
                datasets: [
                    {
                        label: 'Novas Carências',
                        data: {{ novas_carencias_por_mes|safe }},
                        borderColor: 'rgba(220, 53, 69, 1)',
                        backgroundColor: 'rgba(220, 53, 69, 0.1)',
                        fill: true
                    },
                    {
                        label: 'Carências Resolvidas',
                        data: {{ carencias_resolvidas_por_mes|safe }},
                        borderColor: 'rgba(40, 167, 69, 1)',
                        backgroundColor: 'rgba(40, 167, 69, 0.1)',
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });
</script>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\registrar_frequencia.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Registrar Frequência</h1>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card">
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                {% include 'includes/form_errors.html' %}
                
                {% for field in form %}
                    {% include 'includes/form_field.html' %}
                {% endfor %}
                
                <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                    <button type="submit" class="btn btn-primary">Registrar Frequência</button>
                    <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: frequencias\templates\frequencias\registrar_frequencia_turma.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Registrar Frequência da Turma: {{ turma.id }}</h1>
   
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
   
    <div class="card">
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
               
                <div class="mb-3">
                    <label for="data" class="form-label">Data</label>
                    <input type="date" class="form-control" id="data" name="data" required>
                </div>
               
                <table class="table">
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
                                    <input class="form-check-input" type="checkbox" name="presentes" value="{{ aluno.id }}" id="presente_{{ aluno.id }}" checked>
                                    <label class="form-check-label" for="presente_{{ aluno.id }}">
                                        Presente
                                    </label>
                                </div>
                            </td>
                            <td>
                                <textarea class="form-control" name="justificativa_{{ aluno.id }}" rows="2" placeholder="Justificativa para ausência"></textarea>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="3" class="text-center">Nenhum aluno encontrado nesta turma.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
               
                <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                    <button type="submit" class="btn btn-primary">Registrar Frequências</button>
                    <a href="{% url 'listar_frequencias' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: frequencias\templates\frequencias\relatorio_carencias.html

html
{% extends 'base.html' %}

{% block title %}Relatório de Carências{% endblock %}

{% block extra_css %}
<style>
    .chart-container {
        position: relative;
        height: 300px;
        width: 100%;
    }
</style>
{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Relatório de Carências</h1>
        <div>
            <a href="{% url 'frequencias:listar_carencias' %}" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar para Lista
            </a>
            <button class="btn btn-primary" onclick="window.print()">
                <i class="fas fa-print"></i> Imprimir Relatório
            </button>
        </div>
    </div>
    
    <!-- Filtros -->
    <div class="card mb-4 d-print-none">
        <div class="card-header">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-3">
                    <label for="periodo_inicio" class="form-label">Período Início</label>
                    <input type="month" class="form-control" id="periodo_inicio" name="periodo_inicio" 
                           value="{{ filtros.periodo_inicio|default:'' }}">
                </div>
                
                <div class="col-md-3">
                    <label for="periodo_fim" class="form-label">Período Fim</label>
                    <input type="month" class="form-control" id="periodo_fim" name="periodo_fim" 
                           value="{{ filtros.periodo_fim|default:'' }}">
                </div>
                
                <div class="col-md-3">
                    <label for="curso" class="form-label">Curso</label>
                    <select class="form-select" id="curso" name="curso">
                        <option value="">Todos os cursos</option>
                        {% for curso in cursos %}
                        <option value="{{ curso.codigo_curso }}" {% if filtros.curso == curso.codigo_curso|stringformat:"s" %}selected{% endif %}>
                            {{ curso.nome }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="col-md-3 d-flex align-items-end">
                    <button type="submit" class="btn btn-primary w-100">
                        <i class="fas fa-filter"></i> Gerar Relatório
                    </button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Resumo -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Resumo</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-3 mb-3">
                    <div class="card h-100">
                        <div class="card-body text-center">
                            <h6 class="card-title">Total de Carências</h6>
                            <h2 class="display-4">{{ stats.total }}</h2>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-3 mb-3">
                    <div class="card h-100 border-danger">
                        <div class="card-body text-center">
                            <h6 class="card-title text-danger">Pendentes</h6>
                            <h2 class="display-4">{{ stats.pendentes }}</h2>
                            <p class="mb-0">{{ stats.percentual_pendentes|floatformat:1 }}%</p>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-3 mb-3">
                    <div class="card h-100 border-warning">
                        <div class="card-body text-center">
                            <h6 class="card-title text-warning">Em Acompanhamento</h6>
                            <h2 class="display-4">{{ stats.em_acompanhamento }}</h2>
                            <p class="mb-0">{{ stats.percentual_em_acompanhamento|floatformat:1 }}%</p>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-3 mb-3">
                    <div class="card h-100 border-success">
                        <div class="card-body text-center">
                            <h6 class="card-title text-success">Resolvidas</h6>
                            <h2 class="display-4">{{ stats.resolvidas }}</h2>
                            <p class="mb-0">{{ stats.percentual_resolvidas|floatformat:1 }}%</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Gráficos -->
    <div class="row mb-4">
        <div class="col-md-6 mb-3">
            <div class="card h-100">
                <div class="card-header">
                    <h5 class="mb-0">Carências por Status</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="statusChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-6 mb-3">
            <div class="card h-100">
                <div class="card-header">
                    <h5 class="mb-0">Carências por Curso</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="cursoChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-6 mb-3">
            <div class="card h-100">
                <div class="card-header">
                    <h5 class="mb-0">Carências por Mês</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="mesChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-6 mb-3">
            <div class="card h-100">
                <div class="card-header">
                    <h5 class="mb-0">Tempo Médio de Resolução</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="tempoResolucaoChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Tabela de Carências por Curso -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Carências por Curso</h5>
        </div>
        <div class="card-body p-0">
            <div class="table-responsive">
                <table class="table table-striped mb-0">
                    <thead>
                        <tr>
                            <th>Curso</th>
                            <th class="text-center">Pendentes</th>
                            <th class="text-center">Em Acompanhamento</th>
                            <th class="text-center">Resolvidas</th>
                            <th class="text-center">Total</th>
                            <th class="text-center">% Resolução</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for curso in carencias_por_curso %}
                        <tr>
                            <td>{{ curso.nome }}</td>
                            <td class="text-center">{{ curso.pendentes }}</td>
                            <td class="text-center">{{ curso.em_acompanhamento }}</td>
                            <td class="text-center">{{ curso.resolvidas }}</td>
                            <td class="text-center">{{ curso.total }}</td>
                            <td class="text-center">
                                <div class="d-flex align-items-center justify-content-center">
                                    <div class="progress flex-grow-1 me-2" style="height: 8px; max-width: 100px;">
                                        <div class="progress-bar bg-success" role="progressbar" 
                                             style="width: {{ curso.percentual_resolucao }}%;" 
                                             aria-valuenow="{{ curso.percentual_resolucao }}" 
                                             aria-valuemin="0" aria-valuemax="100">
                                        </div>
                                    </div>
                                    <span>{{ curso.percentual_resolucao|floatformat:1 }}%</span>
                                </div>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="6" class="text-center py-3">Nenhum dado disponível</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <!-- Tabela de Carências por Mês -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Carências por Mês</h5>
        </div>
        <div class="card-body p-0">
            <div class="table-responsive">
                <table class="table table-striped mb-0">
                    <thead>
                        <tr>
                            <th>Mês/Ano</th>
                            <th class="text-center">Pendentes</th>
                            <th class="text-center">Em Acompanhamento</th>
                            <th class="text-center">Resolvidas</th>
                            <th class="text-center">Total</th>
                            <th class="text-center">% Resolução</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for mes in carencias_por_mes %}
                        <tr>
                            <td>{{ mes.nome }}</td>
                            <td class="text-center">{{ mes.pendentes }}</td>
                            <td class="text-center">{{ mes.em_acompanhamento }}</td>
                            <td class="text-center">{{ mes.resolvidas }}</td>
                            <td class="text-center">{{ mes.total }}</td>
                            <td class="text-center">
                                <div class="d-flex align-items-center justify-content-center">
                                    <div class="progress flex-grow-1 me-2" style="height: 8px; max-width: 100px;">
                                        <div class="progress-bar bg-success" role="progressbar" 
                                             style="width: {{ mes.percentual_resolucao }}%;" 
                                             aria-valuenow="{{ mes.percentual_resolucao }}" 
                                             aria-valuemin="0" aria-valuemax="100">
                                        </div>
                                    </div>
                                    <span>{{ mes.percentual_resolucao|floatformat:1 }}%</span>
                                </div>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="6" class="text-center py-3">Nenhum dado disponível</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <!-- Rodapé do relatório -->
    <div class="card mb-4">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <p class="mb-0 text-muted">Relatório gerado em: {{ data_geracao|date:"d/m/Y H:i" }}</p>
                </div>
                <div>
                    <p class="mb-0 text-muted">Período: 
                        {% if filtros.periodo_inicio %}{{ filtros.periodo_inicio_formatado }}{% else %}Início{% endif %} 
                        até 
                        {% if filtros.periodo_fim %}{{ filtros.periodo_fim_formatado }}{% else %}Atual{% endif %}
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Dados para os gráficos
        const statusData = {
            labels: ['Pendentes', 'Em Acompanhamento', 'Resolvidas'],
            datasets: [{
                data: [{{ stats.pendentes }}, {{ stats.em_acompanhamento }}, {{ stats.resolvidas }}],
                backgroundColor: ['#dc3545', '#ffc107', '#28a745'],
                borderWidth: 1
            }]
        };
        
        const cursoData = {
            labels: [{% for curso in carencias_por_curso %}'{{ curso.nome }}'{% if not forloop.last %}, {% endif %}{% endfor %}],
            datasets: [{
                label: 'Total de Carências',
                data: [{% for curso in carencias_por_curso %}{{ curso.total }}{% if not forloop.last %}, {% endif %}{% endfor %}],
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        };
        
        const mesData = {
            labels: [{% for mes in carencias_por_mes %}'{{ mes.nome }}'{% if not forloop.last %}, {% endif %}{% endfor %}],
            datasets: [{
                label: 'Total de Carências',
                data: [{% for mes in carencias_por_mes %}{{ mes.total }}{% if not forloop.last %}, {% endif %}{% endfor %}],
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        };
        
        const tempoResolucaoData = {
            labels: [{% for curso in tempo_resolucao %}'{{ curso.nome }}'{% if not forloop.last %}, {% endif %}{% endfor %}],
            datasets: [{
                label: 'Dias para Resolução (média)',
                data: [{% for curso in tempo_resolucao %}{{ curso.media_dias|floatformat:1 }}{% if not forloop.last %}, {% endif %}{% endfor %}],
                backgroundColor: 'rgba(153, 102, 255, 0.5)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }]
        };
        
        // Configuração dos gráficos
        const statusChart = new Chart(document.getElementById('statusChart'), {
            type: 'pie',
            data: statusData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                    }
                }
            }
        });
        
        const cursoChart = new Chart(document.getElementById('cursoChart'), {
            type: 'bar',
            data: cursoData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        
        const mesChart = new Chart(document.getElementById('mesChart'), {
            type: 'line',
            data: mesData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        
        const tempoResolucaoChart = new Chart(document.getElementById('tempoResolucaoChart'), {
            type: 'bar',
            data: tempoResolucaoData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Dias (média)'
                        }
                    }
                }
            }
        });
    });
</script>
{% endblock %}
{% endblock %}



### Arquivo: frequencias\templates\frequencias\relatorio_frequencias.html

html
{% extends 'base.html' %}

{% block title %}Relatório de Frequências{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
  <div class="d-flex justify-content-between align-items-center mb-3">
      <h1>Relatório de Frequências</h1>
      <div class="btn-group">
          <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">
              <i class="fas fa-arrow-left"></i> Voltar
          </a>
          <button id="btn-imprimir" class="btn btn-primary">
              <i class="fas fa-print"></i> Imprimir
          </button>
          <button id="btn-exportar-pdf" class="btn btn-danger">
              <i class="fas fa-file-pdf"></i> Exportar PDF
          </button>
          <button id="btn-exportar-excel" class="btn btn-success">
              <i class="fas fa-file-excel"></i> Exportar Excel
          </button>
      </div>
  </div>
    
  <!-- Filtros -->
  <div class="card mb-4 no-print">
      <div class="card-header bg-light">
          <h5 class="mb-0">Filtros</h5>
      </div>
      <div class="card-body">
          <form method="get" class="row g-3">
              <div class="col-md-3">
                  <label for="turma" class="form-label">Turma</label>
                  <select name="turma" id="turma" class="form-select select2">
                      <option value="">Todas as turmas</option>
                      {% for turma in turmas %}
                      <option value="{{ turma.id }}" {% if request.GET.turma == turma.id|stringformat:"s" %}selected{% endif %}>
                          {{ turma.nome }}
                      </option>
                      {% endfor %}
                  </select>
              </div>
              <div class="col-md-2">
                  <label for="mes" class="form-label">Mês</label>
                  <select name="mes" id="mes" class="form-select">
                      <option value="">Todos os meses</option>
                      {% for mes_valor, mes_nome in meses_choices %}
                      <option value="{{ mes_valor }}" {% if request.GET.mes == mes_valor %}selected{% endif %}>
                          {{ mes_nome }}
                      </option>
                      {% endfor %}
                  </select>
              </div>
              <div class="col-md-2">
                  <label for="ano" class="form-label">Ano</label>
                  <select name="ano" id="ano" class="form-select">
                      <option value="">Todos os anos</option>
                      {% for ano in anos %}
                      <option value="{{ ano }}" {% if request.GET.ano == ano|stringformat:"s" %}selected{% endif %}>
                          {{ ano }}
                      </option>
                      {% endfor %}
                  </select>
              </div>
              <div class="col-md-3">
                  <label for="status" class="form-label">Status da Carência</label>
                  <select name="status" id="status" class="form-select">
                      <option value="">Todos os status</option>
                      <option value="PENDENTE" {% if request.GET.status == "PENDENTE" %}selected{% endif %}>Pendente</option>
                      <option value="EM_ACOMPANHAMENTO" {% if request.GET.status == "EM_ACOMPANHAMENTO" %}selected{% endif %}>Em Acompanhamento</option>
                      <option value="RESOLVIDO" {% if request.GET.status == "RESOLVIDO" %}selected{% endif %}>Resolvido</option>
                  </select>
              </div>
              <div class="col-12 mt-3">
                  <button type="submit" class="btn btn-primary">
                      <i class="fas fa-filter"></i> Filtrar
                  </button>
                  <a href="{% url 'frequencias:relatorio_frequencias' %}" class="btn btn-secondary">
                      <i class="fas fa-broom"></i> Limpar Filtros
                  </a>
              </div>
          </form>
      </div>
  </div>
    
  <!-- Cabeçalho do relatório -->
  <div class="card mb-4">
      <div class="card-body">
          <div class="d-flex justify-content-between align-items-center">
              <div>
                  <h2 class="mb-1">Relatório de Frequências</h2>
                  <p class="text-muted mb-0">Gerado em: {{ data_geracao|date:"d/m/Y H:i" }}</p>
              </div>
              <div class="text-end">
                  <h5>Filtros aplicados:</h5>
                  <p class="mb-0">
                      Turma: {{ turma_selecionada|default:"Todas" }} |
                      Período: {{ mes_selecionado|default:"Todos os meses" }}/{{ ano_selecionado|default:"Todos os anos" }} |
                      Status: {{ status_selecionado|default:"Todos" }}
                  </p>
              </div>
          </div>
      </div>
  </div>
    
  <!-- Resumo estatístico -->
  <div class="card mb-4">
      <div class="card-header bg-light">
          <h5 class="mb-0">Resumo Estatístico</h5>
      </div>
      <div class="card-body">
          <div class="row">
              <div class="col-md-3">
                  <div class="card text-center mb-3">
                      <div class="card-body">
                          <h5 class="card-title">Total de Frequências</h5>
                          <p class="card-text display-4">{{ total_frequencias }}</p>
                      </div>
                  </div>
              </div>
              <div class="col-md-3">
                  <div class="card text-center mb-3">
                      <div class="card-body">
                          <h5 class="card-title">Total de Carências</h5>
                          <p class="card-text display-4">{{ total_carencias }}</p>
                      </div>
                  </div>
              </div>
              <div class="col-md-3">
                  <div class="card text-center mb-3">
                      <div class="card-body">
                          <h5 class="card-title">Carências Pendentes</h5>
                          <p class="card-text display-4">{{ carencias_pendentes }}</p>
                      </div>
                  </div>
              </div>
              <div class="col-md-3">
                  <div class="card text-center mb-3">
                      <div class="card-body">
                          <h5 class="card-title">Carências Resolvidas</h5>
                          <p class="card-text display-4">{{ carencias_resolvidas }}</p>
                      </div>
                  </div>
              </div>
          </div>
      </div>
  </div>
    
  <!-- Tabela de carências -->
  <div class="card mb-4">
      <div class="card-header bg-light">
          <h5 class="mb-0">Lista de Carências</h5>
      </div>
      <div class="card-body">
          <div class="table-responsive">
              <table class="table table-striped table-hover">
                  <thead class="table-dark">
                      <tr>
                          <th>Aluno</th>
                          <th>Turma</th>
                          <th>Período</th>
                          <th>Percentual</th>
                          <th>Status</th>
                          <th>Data de Resolução</th>
                          <th>Observações</th>
                      </tr>
                  </thead>
                  <tbody>
                      {% for carencia in carencias %}
                      <tr>
                          <td>
                              <div class="d-flex align-items-center">
                                  {% if carencia.aluno.foto %}
                                  <img src="{{ carencia.aluno.foto.url }}" alt="{{ carencia.aluno.nome }}" 
                                       class="rounded-circle me-2" width="40" height="40">
                                  {% else %}
                                  <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-2"
                                       style="width: 40px; height: 40px; color: white;">
                                      {{ carencia.aluno.nome|first|upper }}
                                  </div>
                                  {% endif %}
                                  <div>
                                      <div>{{ carencia.aluno.nome }}</div>
                                      <small class="text-muted">{{ carencia.aluno.cpf }}</small>
                                  </div>
                              </div>
                          </td>
                          <td>{{ carencia.frequencia_mensal.turma.nome }}</td>
                          <td>{{ carencia.frequencia_mensal.get_mes_display }}/{{ carencia.frequencia_mensal.ano }}</td>
                          <td>
                              <div class="progress" style="height: 20px;">
                                  <div class="progress-bar bg-danger" role="progressbar" 
                                       style="width: {{ carencia.percentual_presenca }}%;" 
                                       aria-valuenow="{{ carencia.percentual_presenca }}" 
                                       aria-valuemin="0" aria-valuemax="100">
                                      {{ carencia.percentual_presenca }}%
                                  </div>
                              </div>
                          </td>
                          <td>
                              {% if carencia.status == 'PENDENTE' %}
                              <span class="badge bg-danger">Pendente</span>
                              {% elif carencia.status == 'EM_ACOMPANHAMENTO' %}
                              <span class="badge bg-warning text-dark">Em Acompanhamento</span>
                              {% elif carencia.status == 'RESOLVIDO' %}
                              <span class="badge bg-success">Resolvido</span>
                              {% endif %}
                          </td>
                          <td>{{ carencia.data_resolucao|date:"d/m/Y"|default:"-" }}</td>
                          <td>{{ carencia.observacoes|default:"-" }}</td>
                      </tr>
                      {% empty %}
                      <tr>
                          <td colspan="7" class="text-center py-4">
                              <div class="alert alert-info mb-0">
                                  Nenhuma carência encontrada com os filtros selecionados.
                              </div>
                          </td>
                      </tr>
                      {% endfor %}
                  </tbody>
              </table>
          </div>
            
          <!-- Paginação -->
          {% if page_obj.has_other_pages %}
          <nav aria-label="Paginação" class="mt-4 no-print">
              <ul class="pagination justify-content-center">
                  {% if page_obj.has_previous %}
                  <li class="page-item">
                      <a class="page-link" href="?page=1{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                          <i class="fas fa-angle-double-left"></i>
                      </a>
                  </li>
                  <li class="page-item">
                      <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                          <i class="fas fa-angle-left"></i>
                      </a>
                  </li>
                  {% else %}
                  <li class="page-item disabled">
                      <span class="page-link"><i class="fas fa-angle-double-left"></i></span>
                  </li>
                  <li class="page-item disabled">
                      <span class="page-link"><i class="fas fa-angle-left"></i></span>
                  </li>
                  {% endif %}
                    
                  {% for num in page_obj.paginator.page_range %}
                      {% if page_obj.number == num %}
                      <li class="page-item active">
                          <span class="page-link">{{ num }}</span>
                      </li>
                      {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                      <li class="page-item">
                          <a class="page-link" href="?page={{ num }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                              {{ num }}
                          </a>
                      </li>
                      {% endif %}
                  {% endfor %}
                    
                  {% if page_obj.has_next %}
                  <li class="page-item">
                      <a class="page-link" href="?page={{ page_obj.next_page_number }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                          <i class="fas fa-angle-right"></i>
                      </a>
                  </li>
                  <li class="page-item">
                      <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                          <i class="fas fa-angle-double-right"></i>
                      </a>
                  </li>
                  {% else %}
                  <li class="page-item disabled">
                      <span class="page-link"><i class="fas fa-angle-right"></i></span>
                  </li>
                  <li class="page-item disabled">
                      <span class="page-link"><i class="fas fa-angle-double-right"></i></span>
                  </li>
                  {% endif %}
              </ul>
          </nav>
          {% endif %}
      </div>
      <div class="card-footer">
          <div class="d-flex justify-content-between align-items-center">
              <span>Total: {{ page_obj.paginator.count }} carências</span>
              <span class="no-print">Página {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}</span>
          </div>
      </div>
  </div>
    
  <!-- Gráfico de carências por turma -->
  <div class="card mb-4">
      <div class="card-header bg-light">
          <h5 class="mb-0">Carências por Turma</h5>
      </div>
      <div class="card-body">
          <canvas id="grafico-carencias-turma" height="300"></canvas>
      </div>
  </div>
    
  <!-- Gráfico de evolução mensal -->
  <div class="card mb-4">
      <div class="card-header bg-light">
          <h5 class="mb-0">Evolução Mensal de Carências</h5>
      </div>
      <div class="card-body">
          <canvas id="grafico-evolucao-mensal" height="300"></canvas>
      </div>
  </div>
    
  <!-- Rodapé do relatório -->
  <div class="card mb-4">
      <div class="card-body">
          <div class="d-flex justify-content-between align-items-center">
              <div>
                  <p class="mb-0">Relatório gerado em: {{ data_geracao|date:"d/m/Y H:i" }}</p>
              </div>
              <div>
                  <p class="mb-0">Sistema de Gestão Acadêmica - OMAUM</p>
              </div>
          </div>
      </div>
  </div>
</div>

<!-- Estilos para impressão -->
<style>
    @media print {
        .no-print {
            display: none !important;
        }
        
        .container-fluid {
            width: 100%;
            padding: 0;
            margin: 0;
        }
        
        .card {
            border: none !important;
            margin-bottom: 20px !important;
        }
        
        .card-header {
            background-color: #f8f9fa !important;
            color: #000 !important;
            border-bottom: 1px solid #dee2e6 !important;
        }
        
        .table {
            width: 100% !important;
            border-collapse: collapse !important;
        }
        
        .table th, .table td {
            border: 1px solid #dee2e6 !important;
            padding: 8px !important;
        }
        
        .table thead th {
            background-color: #f8f9fa !important;
            color: #000 !important;
            border-bottom: 2px solid #dee2e6 !important;
        }
        
        .badge {
            border: 1px solid #000 !important;
            padding: 3px 6px !important;
        }
        
        .badge-danger {
            background-color: #fff !important;
            color: #000 !important;
            border: 1px solid #dc3545 !important;
        }
        
        .badge-warning {
            background-color: #fff !important;
            color: #000 !important;
            border: 1px solid #ffc107 !important;
        }
        
        .badge-success {
            background-color: #fff !important;
            color: #000 !important;
            border: 1px solid #28a745 !important;
        }
        
        .progress {
            border: 1px solid #dee2e6 !important;
            background-color: #f8f9fa !important;
        }
        
        .progress-bar {
            background-color: #6c757d !important;
            color: #fff !important;
        }
    }
</style>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Inicializar Select2 para melhorar a experiência de seleção
        $('.select2').select2({
            theme: 'bootstrap-5',
            width: '100%'
        });
        
        // Gráfico de carências por turma
        const ctxCarenciasTurma = document.getElementById('grafico-carencias-turma').getContext('2d');
        new Chart(ctxCarenciasTurma, {
            type: 'bar',
            data: {
                labels: {{ turmas_labels|safe }},
                datasets: [
                    {
                        label: 'Pendentes',
                        data: {{ carencias_pendentes_por_turma|safe }},
                        backgroundColor: 'rgba(220, 53, 69, 0.7)',
                        borderColor: 'rgba(220, 53, 69, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Em Acompanhamento',
                        data: {{ carencias_em_acompanhamento_por_turma|safe }},
                        backgroundColor: 'rgba(255, 193, 7, 0.7)',
                        borderColor: 'rgba(255, 193, 7, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Resolvidas',
                        data: {{ carencias_resolvidas_por_turma|safe }},
                        backgroundColor: 'rgba(40, 167, 69, 0.7)',
                        borderColor: 'rgba(40, 167, 69, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        stacked: true
                    },
                    x: {
                        stacked: true
                    }
                }
            }
        });
        
        // Gráfico de evolução mensal
        const ctxEvolucaoMensal = document.getElementById('grafico-evolucao-mensal').getContext('2d');
        new Chart(ctxEvolucaoMensal, {
            type: 'line',
            data: {
                labels: {{ meses_completos|safe }},
                datasets: [
                    {
                        label: 'Novas Carências',
                        data: {{ novas_carencias_por_mes|safe }},
                        borderColor: 'rgba(220, 53, 69, 1)',
                        backgroundColor: 'rgba(220, 53, 69, 0.1)',
                        fill: true,
                        tension: 0.3
                    },
                    {
                        label: 'Carências Resolvidas',
                        data: {{ carencias_resolvidas_por_mes|safe }},
                        borderColor: 'rgba(40, 167, 69, 1)',
                        backgroundColor: 'rgba(40, 167, 69, 0.1)',
                        fill: true,
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        
        // Botão de impressão
        document.getElementById('btn-imprimir').addEventListener('click', function() {
            window.print();
        });
        
        // Botão de exportar para PDF
        document.getElementById('btn-exportar-pdf').addEventListener('click', function() {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF('p', 'mm', 'a4');
            
            // Título do documento
            doc.setFontSize(18);
            doc.text('Relatório de Frequências', 105, 15, { align: 'center' });
            
            // Data de geração
            doc.setFontSize(10);
            doc.text('Gerado em: {{ data_geracao|date:"d/m/Y H:i" }}', 105, 22, { align: 'center' });
            
            // Filtros aplicados
            doc.setFontSize(12);
            doc.text('Filtros: {{ turma_selecionada|default:"Todas as turmas" }} | {{ mes_selecionado|default:"Todos os meses" }}/{{ ano_selecionado|default:"Todos os anos" }} | {{ status_selecionado|default:"Todos os status" }}', 105, 30, { align: 'center' });
            
            // Resumo estatístico
            doc.setFontSize(14);
            doc.text('Resumo Estatístico', 14, 40);
            
            doc.setFontSize(12);
            doc.text('Total de Frequências: {{ total_frequencias }}', 14, 50);
            doc.text('Total de Carências: {{ total_carencias }}', 14, 58);
            doc.text('Carências Pendentes: {{ carencias_pendentes }}', 14, 66);
            doc.text('Carências Resolvidas: {{ carencias_resolvidas }}', 14, 74);
            
            // Capturar gráficos
            html2canvas(document.getElementById('grafico-carencias-turma')).then(function(canvas) {
                const imgData = canvas.toDataURL('image/png');
                doc.addPage();
                doc.text('Carências por Turma', 105, 15, { align: 'center' });
                doc.addImage(imgData, 'PNG', 10, 30, 190, 100);
                
                html2canvas(document.getElementById('grafico-evolucao-mensal')).then(function(canvas) {
                    const imgData = canvas.toDataURL('image/png');
                    doc.addPage();
                    doc.text('Evolução Mensal de Carências', 105, 15, { align: 'center' });
                    doc.addImage(imgData, 'PNG', 10, 30, 190, 100);
                    
                    // Salvar o PDF
                    doc.save('relatorio-frequencias.pdf');
                });
            });
        });
        
        // Botão de exportar para Excel
        document.getElementById('btn-exportar-excel').addEventListener('click', function() {
            // Preparar dados para o Excel
            const dados = [
                ['Relatório de Frequências - {{ data_geracao|date:"d/m/Y H:i" }}'],
                ['Filtros: {{ turma_selecionada|default:"Todas as turmas" }} | {{ mes_selecionado|default:"Todos os meses" }}/{{ ano_selecionado|default:"Todos os anos" }} | {{ status_selecionado|default:"Todos os status" }}'],
                [''],
                ['Resumo Estatístico'],
                ['Total de Frequências', '{{ total_frequencias }}'],
                ['Total de Carências', '{{ total_carencias }}'],
                ['Carências Pendentes', '{{ carencias_pendentes }}'],
                ['Carências Resolvidas', '{{ carencias_resolvidas }}'],
                [''],
                ['Lista de Carências'],
                ['Aluno', 'CPF', 'Turma', 'Período', 'Percentual', 'Status', 'Data de Resolução', 'Observações']
            ];
            
            // Adicionar dados das carências
            {% for carencia in todas_carencias %}
            dados.push([
                '{{ carencia.aluno.nome }}',
                '{{ carencia.aluno.cpf }}',
                '{{ carencia.frequencia_mensal.turma.nome }}',
                '{{ carencia.frequencia_mensal.get_mes_display }}/{{ carencia.frequencia_mensal.ano }}',
                '{{ carencia.percentual_presenca }}%',
                '{% if carencia.status == "PENDENTE" %}Pendente{% elif carencia.status == "EM_ACOMPANHAMENTO" %}Em Acompanhamento{% else %}Resolvido{% endif %}',
                '{{ carencia.data_resolucao|date:"d/m/Y"|default:"-" }}',
                '{{ carencia.observacoes|default:"-" }}'
            ]);
            {% endfor %}
            
            // Criar planilha
            const ws = XLSX.utils.aoa_to_sheet(dados);
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, "Relatório de Frequências");
            
            // Ajustar largura das colunas
            const wscols = [
                {wch: 30}, // Aluno
                {wch: 15}, // CPF
                {wch: 25}, // Turma
                {wch: 15}, // Período
                {wch: 12}, // Percentual
                {wch: 20}, // Status
                {wch: 15}, // Data de Resolução
                {wch: 40}  // Observações
            ];
            ws['!cols'] = wscols;
            
            // Salvar arquivo
            XLSX.writeFile(wb, "relatorio-frequencias.xlsx");
        });
    });
</script>
{% endblock %}




### Arquivo: frequencias\templates\frequencias\resolver_carencia.html

html
{% extends 'base.html' %}

{% block title %}Resolver Carência{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Resolver Carência</h1>
        <a href="{% url 'frequencias:detalhar_carencia' carencia.id %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    <!-- Informações da carência -->
    <div class="card mb-4">
        <div class="card-header bg-danger text-white">
            <h5 class="mb-0">Informações da Carência</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Aluno:</strong> {{ carencia.aluno.nome }}</p>
                    <p><strong>CPF:</strong> {{ carencia.aluno.cpf }}</p>
                    <p><strong>Turma:</strong> {{ carencia.frequencia_mensal.turma.nome }}</p>
                    <p><strong>Curso:</strong> {{ carencia.frequencia_mensal.turma.curso.nome }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Período:</strong> {{ carencia.frequencia_mensal.get_mes_display }}/{{ carencia.frequencia_mensal.ano }}</p>
                    <p><strong>Percentual de Presença:</strong> {{ carencia.percentual_presenca|floatformat:1 }}%</p>
                    <p><strong>Percentual Mínimo:</strong> {{ carencia.frequencia_mensal.percentual_minimo }}%</p>
                    <p><strong>Status Atual:</strong> {{ carencia.get_status_display }}</p>
                </div>
            </div>
            
            <div class="mt-3">
                <h6>Percentual de Presença:</h6>
                <div class="progress" style="height: 25px;">
                    <div class="progress-bar bg-danger" role="progressbar" 
                         style="width: {{ carencia.percentual_presenca }}%;" 
                         aria-valuenow="{{ carencia.percentual_presenca }}" 
                         aria-valuemin="0" aria-valuemax="100">
                        {{ carencia.percentual_presenca|floatformat:1 }}%
                    </div>
                </div>
                <div class="d-flex justify-content-between mt-1">
                    <small class="text-muted">0%</small>
                    <small class="text-danger">Mínimo: {{ carencia.frequencia_mensal.percentual_minimo }}%</small>
                    <small class="text-muted">100%</small>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Formulário de resolução -->
    <div class="card mb-4">
        <div class="card-header bg-success text-white">
            <h5 class="mb-0">Resolver Carência</h5>
        </div>
        <div class="card-body">
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="motivo_resolucao" class="form-label">Motivo da Resolução</label>
                    <select class="form-select" id="motivo_resolucao" name="motivo_resolucao" required>
                        <option value="">Selecione um motivo</option>
                        <option value="COMPENSACAO">Compensação de Faltas</option>
                        <option value="JUSTIFICATIVA">Justificativa Aceita</option>
                        <option value="DISPENSA">Dispensa Médica</option>
                        <option value="ERRO_REGISTRO">Erro no Registro de Presença</option>
                        <option value="OUTRO">Outro Motivo</option>
                    </select>
                </div>
                
                <div class="mb-3">
                    <label for="observacoes" class="form-label">Observações</label>
                    <textarea class="form-control" id="observacoes" name="observacoes" rows="5" required></textarea>
                    <div class="form-text">Descreva detalhadamente o motivo da resolução desta carência.</div>
                </div>
                
                <div class="mb-3">
                    <label for="documentos" class="form-label">Documentos Comprobatórios (opcional)</label>
                    <input type="file" class="form-control" id="documentos" name="documentos" multiple>
                    <div class="form-text">Anexe documentos que comprovem a justificativa (atestados, declarações, etc).</div>
                </div>
                
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="notificar_aluno" name="notificar_aluno" checked>
                    <label class="form-check-label" for="notificar_aluno">
                        Notificar aluno sobre a resolução
                    </label>
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'frequencias:detalhar_carencia' carencia.id %}" class="btn btn-secondary">
                        Cancelar
                    </a>
                    <button type="submit" class="btn btn-success">
                        <i class="fas fa-check"></i> Resolver Carência
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\responder_notificacao.html

html
{% extends 'base.html' %}

{% block title %}Responder Notificação{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Responder Notificação</h1>
        <a href="{% url 'frequencias:detalhar_notificacao' notificacao.id %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    <!-- Informações da notificação original -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Notificação Original</h5>
        </div>
        <div class="card-body">
            <div class="mb-3">
                <h6>Assunto:</h6>
                <p>{{ notificacao.assunto }}</p>
            </div>
            
            <div class="mb-3">
                <h6>Mensagem:</h6>
                <div class="p-3 bg-light rounded border">
                    {{ notificacao.mensagem|linebreaks }}
                </div>
            </div>
            
            {% if notificacao.anexos.all %}
            <div>
                <h6>Anexos:</h6>
                <ul class="list-group">
                    {% for anexo in notificacao.anexos.all %}
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <span>{{ anexo.nome }}</span>
                        <a href="{{ anexo.arquivo.url }}" class="btn btn-sm btn-outline-primary" download>
                            <i class="fas fa-download"></i> Download
                        </a>
                    </li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}
        </div>
    </div>
    
    <!-- Formulário de resposta -->
    <div class="card mb-4">
        <div class="card-header bg-success text-white">
            <h5 class="mb-0">Sua Resposta</h5>
        </div>
        <div class="card-body">
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="assunto" class="form-label">Assunto</label>
                    <input type="text" class="form-control" id="assunto" name="assunto" 
                           value="RE: {{ notificacao.assunto }}" required>
                </div>
                
                <div class="mb-3">
                    <label for="mensagem" class="form-label">Mensagem</label>
                    <textarea class="form-control" id="mensagem" name="mensagem" rows="10" required></textarea>
                    <div class="form-text">Explique a situação e forneça justificativas para as faltas, se possível.</div>
                </div>
                
                <div class="mb-3">
                    <label for="anexos" class="form-label">Anexos (opcional)</label>
                    <input type="file" class="form-control" id="anexos" name="anexos" multiple>
                    <div class="form-text">Você pode anexar atestados médicos, declarações ou outros documentos que justifiquem suas ausências.</div>
                </div>
                
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="solicitar_compensacao" name="solicitar_compensacao">
                    <label class="form-check-label" for="solicitar_compensacao">
                        Solicitar opções de compensação de faltas
                    </label>
                    <div class="form-text">Marque esta opção se deseja solicitar atividades para compensar as faltas.</div>
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'frequencias:detalhar_notificacao' notificacao.id %}" class="btn btn-secondary">
                        Cancelar
                    </a>
                    <button type="submit" class="btn btn-success">
                        <i class="fas fa-paper-plane"></i> Enviar Resposta
                    </button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Dicas para justificativas -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Dicas para Justificativas</h5>
        </div>
        <div class="card-body">
            <ul class="mb-0">
                <li>Seja claro e objetivo ao explicar os motivos das faltas.</li>
                <li>Anexe documentos comprobatórios sempre que possível (atestados médicos, declarações, etc.).</li>
                <li>Se as faltas foram por motivos de saúde, mencione o período e o tratamento realizado.</li>
                <li>Caso tenha problemas de transporte ou trabalho, explique a situação detalhadamente.</li>
                <li>Demonstre seu interesse em recuperar o conteúdo perdido e melhorar sua frequência.</li>
                <li>Se necessário, solicite uma reunião presencial para discutir sua situação.</li>
            </ul>
        </div>
    </div>
</div>
{% endblock %}


'''