'''
# Revisão da Funcionalidade: frequencias

## Arquivos forms.py:


### Arquivo: frequencias\templates\frequencias\dashboard.html

html
{% extends 'base.html' %}

{% block title %}Dashboard de Frequências{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Dashboard de Frequências</h1>
        <div>
            <a href="{% url 'frequencias:relatorio_carencias' %}" class="btn btn-primary">
                <i class="fas fa-file-alt"></i> Relatório de Carências
            </a>
            <a href="{% url 'frequencias:notificacoes_carencia' %}" class="btn btn-info">
                <i class="fas fa-envelope"></i> Notificações
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
                <div class="col-md-3">
                    <label for="periodo" class="form-label">Período</label>
                    <select class="form-select" id="periodo" name="periodo">
                        <option value="">Todos os períodos</option>
                        {% for ano in anos %}
                            <optgroup label="{{ ano }}">
                                {% for mes in meses %}
                                <option value="{{ ano }}-{{ mes.0 }}" 
                                        {% if filtros.periodo == ano|stringformat:"s"|add:"-"|add:mes.0 %}selected{% endif %}>
                                    {{ mes.1 }}/{{ ano }}
                                </option>
                                {% endfor %}
                            </optgroup>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="col-md-3">
                    <label for="curso" class="form-label">Curso</label>
                    <select class="form-select" id="curso" name="curso">
                        <option value="">Todos os cursos</option>
                        {% for curso in cursos %}
                        <option value="{{ curso.codigo_curso }}" {% if curso.codigo_curso|stringformat:"s" == filtros.curso %}selected{% endif %}>
                            {{ curso.nome }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="col-md-3">
                    <label for="turma" class="form-label">Turma</label>
                    <select class="form-select" id="turma" name="turma">
                        <option value="">Todas as turmas</option>
                        {% for turma in turmas %}
                        <option value="{{ turma.id }}" {% if turma.id|stringformat:"s" == filtros.turma %}selected{% endif %}>
                            {{ turma.nome }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                    <a href="{% url 'frequencias:dashboard' %}" class="btn btn-secondary">
                        <i class="fas fa-undo"></i> Limpar Filtros
                    </a>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Cards de estatísticas -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card text-white bg-primary h-100">
                <div class="card-body">
                    <h5 class="card-title">Média de Frequência</h5>
                    <p class="card-text display-4">{{ estatisticas.media_frequencia|floatformat:1 }}%</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <small>Média geral de frequência</small>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card text-white bg-success h-100">
                <div class="card-body">
                    <h5 class="card-title">Alunos Regulares</h5>
                    <p class="card-text display-4">{{ estatisticas.alunos_regulares }}</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <small>Alunos com frequência ≥ 75%</small>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card text-white bg-danger h-100">
                <div class="card-body">
                    <h5 class="card-title">Alunos em Carência</h5>
                    <p class="card-text display-4">{{ estatisticas.alunos_carencia }}</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <small>Alunos com frequência < 75%</small>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card text-white bg-info h-100">
                <div class="card-body">
                    <h5 class="card-title">Total de Alunos</h5>
                    <p class="card-text display-4">{{ estatisticas.total_alunos }}</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <small>Alunos ativos no período</small>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Gráficos -->
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Frequência por Curso</h5>
                </div>
                <div class="card-body">
                    <canvas id="graficoFrequenciaCursos" height="300"></canvas>
                </div>
            </div>
        </div>
        
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Evolução da Frequência</h5>
                </div>
                <div class="card-body">
                    <canvas id="graficoEvolucaoFrequencia" height="300"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Tabela de turmas com menor frequência -->
    <div class="card mb-4">
        <div class="card-header bg-warning text-dark">
            <h5 class="mb-0">Turmas com Menor Frequência</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Turma</th>
                            <th>Curso</th>
                            <th>Período</th>
                            <th>Média de Frequência</th>
                            <th>Alunos em Carência</th>
                            <th>Total de Alunos</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for turma in turmas_menor_frequencia %}
                        <tr>
                            <td>{{ turma.nome }}</td>
                            <td>{{ turma.curso.nome }}</td>
                            <td>{{ turma.periodo_mes }}/{{ turma.periodo_ano }}</td>
                            <td>
                                <div class="progress" style="height: 20px;">
                                    <div class="progress-bar {% if turma.media_frequencia < 75 %}bg-danger{% elif turma.media_frequencia < 85 %}bg-warning{% else %}bg-success{% endif %}" 
                                         role="progressbar" style="width: {{ turma.media_frequencia }}%;" 
                                         aria-valuenow="{{ turma.media_frequencia }}" aria-valuemin="0" aria-valuemax="100">
                                        {{ turma.media_frequencia|floatformat:1 }}%
                                    </div>
                                </div>
                            </td>
                            <td>{{ turma.alunos_carencia }} / {{ turma.total_alunos }}</td>
                            <td>{{ turma.total_alunos }}</td>
                            <td>
                                <a href="{% url 'frequencias:listar_frequencias' %}?turma={{ turma.id }}" class="btn btn-sm btn-primary">
                                    <i class="fas fa-list"></i> Ver Frequências
                                </a>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="7" class="text-center py-3">
                                <p class="mb-0">Nenhuma turma encontrada com os filtros selecionados.</p>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <!-- Alunos com menor frequência -->
    <div class="card mb-4">
        <div class="card-header bg-danger text-white">
            <h5 class="mb-0">Alunos com Menor Frequência</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Aluno</th>
                            <th>Turma</th>
                            <th>Curso</th>
                            <th>Período</th>
                            <th>Frequência</th>
                            <th>Status</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for aluno in alunos_menor_frequencia %}
                        <tr>
                            <td>
                                <div class="d-flex align-items-center">
                                    {% if aluno.foto %}
                                    <img src="{{ aluno.foto.url }}" alt="{{ aluno.nome }}" 
                                         class="rounded-circle me-2" width="40" height="40" style="object-fit: cover;">
                                    {% else %}
                                    <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-2"
                                         style="width: 40px; height: 40px; color: white;">
                                        {{ aluno.nome|first|upper }}
                                    </div>
                                    {% endif %}
                                    <div>
                                        <div>{{ aluno.nome }}</div>
                                        <small class="text-muted">{{ aluno.email }}</small>
                                    </div>
                                </div>
                            </td>
                            <td>{{ aluno.turma }}</td>
                            <td>{{ aluno.curso }}</td>
                            <td>{{ aluno.periodo_mes }}/{{ aluno.periodo_ano }}</td>
                            <td>
                                <div class="progress" style="height: 20px;">
                                    <div class="progress-bar bg-danger" role="progressbar" 
                                         style="width: {{ aluno.percentual_presenca }}%;" 
                                         aria-valuenow="{{ aluno.percentual_presenca }}" aria-valuemin="0" aria-valuemax="100">
                                        {{ aluno.percentual_presenca }}%
                                    </div>
                                </div>
                            </td>
                            <td>
                                {% if aluno.status_carencia == 'PENDENTE' %}
                                <span class="badge bg-danger">Pendente</span>
                                {% elif aluno.status_carencia == 'EM_ACOMPANHAMENTO' %}
                                <span class="badge bg-warning text-dark">Em Acompanhamento</span>
                                {% elif aluno.status_carencia == 'RESOLVIDO' %}
                                <span class="badge bg-success">Resolvido</span>
                                {% endif %}
                            </td>
                            <td>
                                <div class="btn-group">
                                    <a href="{% url 'alunos:detalhar_aluno' aluno.cpf %}" class="btn btn-sm btn-info">
                                        <i class="fas fa-user"></i>
                                    </a>
                                    {% if aluno.carencia_id %}
                                    <a href="{% url 'frequencias:detalhar_carencia' aluno.carencia_id %}" class="btn btn-sm btn-warning">
                                        <i class="fas fa-exclamation-triangle"></i>
                                    </a>
                                    {% if aluno.status_carencia != 'RESOLVIDO' %}
                                    <a href="{% url 'frequencias:resolver_carencia' aluno.carencia_id %}" class="btn btn-sm btn-success">
                                        <i class="fas fa-check"></i>
                                    </a>
                                    {% endif %}
                                    {% endif %}
                                </div>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="7" class="text-center py-3">
                                <p class="mb-0">Nenhum aluno em carência encontrado com os filtros selecionados.</p>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Gráfico de frequência por curso
        const ctxCursos = document.getElementById('graficoFrequenciaCursos').getContext('2d');
        new Chart(ctxCursos, {
            type: 'bar',
            data: {
                labels: {{ cursos_labels|safe }},
                datasets: [{
                    label: 'Média de Frequência (%)',
                    data: {{ frequencia_por_curso|safe }},
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)',
                        'rgba(255, 159, 64, 0.7)',
                        'rgba(199, 199, 199, 0.7)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(199, 199, 199, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
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
        
        // Gráfico de evolução da frequência
        const ctxEvolucao = document.getElementById('graficoEvolucaoFrequencia').getContext('2d');
        new Chart(ctxEvolucao, {
            type: 'line',
            data: {
                labels: {{ periodos_labels|safe }},
                datasets: [{
                    label: 'Média de Frequência (%)',
                    data: {{ evolucao_frequencia|safe }},
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    tension: 0.1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
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
        
        // Atualizar turmas quando o curso for alterado
        const cursoSelect = document.getElementById('curso');
        const turmaSelect = document.getElementById('turma');
        
        cursoSelect.addEventListener('change', function() {
            const cursoId = this.value;
            
            // Limpar o select de turmas
            turmaSelect.innerHTML = '<option value="">Todas as turmas</option>';
            
            if (cursoId) {
                // Fazer uma requisição AJAX para buscar as turmas do curso
                fetch(`/frequencias/api/turmas-por-curso/${cursoId}/`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.turmas) {
                            data.turmas.forEach(turma => {
                                const option = document.createElement('option');
                                option.value = turma.id;
                                option.textContent = turma.nome;
                                turmaSelect.appendChild(option);
                            });
                        }
                    })
                    .catch(error => console.error('Erro ao buscar turmas:', error));
            }
        });
    });
</script>
{% endblock %}
{% endblock %}



### Arquivo: frequencias\templates\frequencias\detalhar_carencia.html

html
{% extends 'base.html' %}

{% block title %}Detalhes da Carência{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Padronizar botões de ação -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Detalhes da Carência</h1>
        <div>
            <a href="{% url 'frequencias:listar_carencias' %}" class="btn btn-secondary me-2">
                <i class="fas fa-list"></i> Lista de Carências
            </a>
            <a href="javascript:history.back()" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
        </div>
    </div>
    
    <!-- Status da carência -->
    <div class="alert 
        {% if carencia.status == 'PENDENTE' %}alert-danger
        {% elif carencia.status == 'EM_ACOMPANHAMENTO' %}alert-warning
        {% elif carencia.status == 'RESOLVIDO' %}alert-success
        {% endif %}">
        <div class="d-flex justify-content-between align-items-center">
            <div>
                <h5 class="alert-heading mb-1">
                    {% if carencia.status == 'PENDENTE' %}
                    <i class="fas fa-exclamation-circle"></i> Carência Pendente
                    {% elif carencia.status == 'EM_ACOMPANHAMENTO' %}
                    <i class="fas fa-clock"></i> Carência em Acompanhamento
                    {% elif carencia.status == 'RESOLVIDO' %}
                    <i class="fas fa-check-circle"></i> Carência Resolvida
                    {% endif %}
                </h5>
                <p class="mb-0">
                    {% if carencia.status == 'PENDENTE' %}
                    Esta carência foi identificada em {{ carencia.data_identificacao|date:"d/m/Y" }} e ainda não foi tratada.
                    {% elif carencia.status == 'EM_ACOMPANHAMENTO' %}
                    Esta carência está sendo acompanhada desde {{ carencia.data_acompanhamento|date:"d/m/Y" }}.
                    {% elif carencia.status == 'RESOLVIDO' %}
                    Esta carência foi resolvida em {{ carencia.data_resolucao|date:"d/m/Y" }}.
                    {% endif %}
                </p>
            </div>
            <div>
                {% if carencia.status == 'PENDENTE' %}
                <a href="{% url 'frequencias:iniciar_acompanhamento' carencia.id %}" class="btn btn-warning">
                    <i class="fas fa-clock"></i> Iniciar Acompanhamento
                </a>
                {% elif carencia.status == 'EM_ACOMPANHAMENTO' %}
                <a href="{% url 'frequencias:resolver_carencia' carencia.id %}" class="btn btn-success">
                    <i class="fas fa-check"></i> Resolver Carência
                </a>
                {% endif %}
            </div>
        </div>
    </div>
    
    <!-- Informações do aluno -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Informações do Aluno</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <div class="d-flex align-items-center">
                        {% if carencia.aluno.foto %}
                        <img src="{{ carencia.aluno.foto.url }}" alt="{{ carencia.aluno.nome }}" 
                             class="rounded-circle me-3" width="60" height="60" style="object-fit: cover;">
                        {% else %}
                        <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-3"
                             style="width: 60px; height: 60px; color: white; font-size: 1.5rem;">
                            {{ carencia.aluno.nome|first|upper }}
                        </div>
                        {% endif %}
                        <div>
                            <h5 class="mb-1">{{ carencia.aluno.nome }}</h5>
                            <p class="mb-0">{{ carencia.aluno.email }}</p>
                            <p class="mb-0">CPF: {{ carencia.aluno.cpf }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 text-md-end">
                    <a href="{% url 'alunos:detalhar_aluno' carencia.aluno.cpf %}" class="btn btn-outline-primary">
                        <i class="fas fa-user"></i> Ver Perfil Completo
                    </a>
                    <a href="{% url 'frequencias:historico_frequencia' carencia.aluno.cpf %}" class="btn btn-outline-info">
                        <i class="fas fa-history"></i> Histórico de Frequência
                    </a>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Informações da frequência -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Informações da Frequência</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Curso:</strong> {{ carencia.frequencia_mensal.turma.curso.nome }}</p>
                    <p><strong>Turma:</strong> {{ carencia.frequencia_mensal.turma.nome }}</p>
                    <p><strong>Período:</strong> {{ carencia.frequencia_mensal.get_mes_display }}/{{ carencia.frequencia_mensal.ano }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Total de Aulas:</strong> {{ carencia.frequencia_mensal.total_aulas }}</p>
                    <p><strong>Presenças:</strong> {{ carencia.frequencia_mensal.presencas }}</p>
                    <p><strong>Faltas:</strong> {{ carencia.frequencia_mensal.faltas }}</p>
                </div>
            </div>
            
            <div class="mt-3">
                <h6>Percentual de Presença:</h6>
                <div class="progress" style="height: 25px;">
                    <div class="progress-bar bg-danger" role="progressbar" 
                         style="width: {{ carencia.percentual_presenca }}%;" 
                         aria-valuenow="{{ carencia.percentual_presenca }}" aria-valuemin="0" aria-valuemax="100">
                        {{ carencia.percentual_presenca|floatformat:1 }}%
                    </div>
                </div>
                <div class="d-flex justify-content-between mt-1">
                    <small class="text-muted">0%</small>
                    <small class="text-danger">Mínimo: 75%</small>
                    <small class="text-muted">100%</small>
                </div>
            </div>
            
            <div class="mt-3 text-end">
                <a href="{% url 'frequencias:detalhar_frequencia_mensal' carencia.frequencia_mensal.id %}" class="btn btn-outline-info">
                    <i class="fas fa-calendar-alt"></i> Ver Detalhes da Frequência Mensal
                </a>
            </div>
        </div>
    </div>
    
    <!-- Notificações -->
    <div class="card mb-4">
        <div class="card-header bg-warning text-dark">
            <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Notificações</h5>
                {% if not carencia.notificacao and carencia.status != 'RESOLVIDO' %}
                <a href="{% url 'frequencias:criar_notificacao' carencia.id %}" class="btn btn-sm btn-primary">
                    <i class="fas fa-plus"></i> Criar Notificação
                </a>
                {% endif %}
            </div>
        </div>
        <div class="card-body">
            {% if carencia.notificacao %}
            <div class="card mb-3">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h6 class="mb-0">{{ carencia.notificacao.assunto }}</h6>
                        <span class="badge 
                            {% if carencia.notificacao.status == 'PENDENTE' %}bg-secondary
                            {% elif carencia.notificacao.status == 'ENVIADA' %}bg-info
                            {% elif carencia.notificacao.status == 'LIDA' %}bg-primary
                            {% elif carencia.notificacao.status == 'RESPONDIDA' %}bg-success
                            {% endif %}">
                            {{ carencia.notificacao.get_status_display }}
                        </span>
                    </div>
                    <p class="mb-2">{{ carencia.notificacao.mensagem|truncatechars:150 }}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                            Criada em: {{ carencia.notificacao.data_criacao|date:"d/m/Y H:i" }}
                            {% if carencia.notificacao.data_envio %}
                            | Enviada em: {{ carencia.notificacao.data_envio|date:"d/m/Y H:i" }}
                            {% endif %}
                        </small>
                        <a href="{% url 'frequencias:detalhar_notificacao' carencia.notificacao.id %}" class="btn btn-sm btn-outline-primary">
                            Ver Detalhes
                        </a>
                    </div>
                </div>
            </div>
            {% else %}
            <div class="alert alert-info mb-0">
                <i class="fas fa-info-circle"></i> Nenhuma notificação foi criada para esta carência.
                {% if carencia.status != 'RESOLVIDO' %}
                <a href="{% url 'frequencias:criar_notificacao' carencia.id %}" class="btn btn-sm btn-primary ms-2">
                    Criar Notificação
                </a>
                {% endif %}
            </div>
            {% endif %}
        </div>
    </div>
    
    <!-- Resolução (se resolvida) -->
    {% if carencia.status == 'RESOLVIDO' %}
    <div class="card mb-4 border-success">
        <div class="card-header bg-success text-white">
            <h5 class="mb-0">Resolução da Carência</h5>
        </div>
        <div class="card-body">
            <div class="mb-3">
                <h6>Motivo da Resolução:</h6>
                <p class="mb-0">{{ carencia.get_motivo_resolucao_display }}</p>
            </div>
            
            <div class="mb-3">
                <h6>Observações:</h6>
                <div class="p-3 bg-light rounded border">
                    {{ carencia.observacoes_resolucao|linebreaks }}
                </div>
            </div>
            
            {% if carencia.documentos_resolucao.all %}
            <div>
                <h6>Documentos:</h6>
                <ul class="list-group">
                    {% for documento in carencia.documentos_resolucao.all %}
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <span>{{ documento.nome }}</span>
                        <a href="{{ documento.arquivo.url }}" class="btn btn-sm btn-outline-primary" download>
                            <i class="fas fa-download"></i> Download
                        </a>
                    </li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}
            
            <div class="mt-3">
                <p class="text-muted mb-0">
                    <small>Resolvida por: {{ carencia.resolvido_por.get_full_name|default:carencia.resolvido_por.username }} em {{ carencia.data_resolucao|date:"d/m/Y H:i" }}</small>
                </p>
            </div>
        </div>
    </div>
    {% endif %}
    
    <!-- Padronizar botões de ações na seção de ações -->
    <div class="card mb-4">
        <div class="card-header bg-secondary text-white">
            <h5 class="mb-0">Ações</h5>
        </div>
        <div class="card-body">
            <div class="d-flex flex-wrap gap-2">
                {% if carencia.status == 'PENDENTE' %}
                <a href="{% url 'frequencias:iniciar_acompanhamento' carencia.id %}" class="btn btn-warning">
                    <i class="fas fa-clock"></i> Iniciar Acompanhamento
                </a>
                {% endif %}
                
                {% if carencia.status != 'RESOLVIDO' %}
                <a href="{% url 'frequencias:resolver_carencia' carencia.id %}" class="btn btn-success">
                    <i class="fas fa-check"></i> Resolver Carência
                </a>
                {% endif %}
                
                {% if not carencia.notificacao and carencia.status != 'RESOLVIDO' %}
                <a href="{% url 'frequencias:criar_notificacao' carencia.id %}" class="btn btn-primary">
                    <i class="fas fa-envelope"></i> Criar Notificação
                </a>
                {% endif %}
                
                <a href="{% url 'frequencias:historico_frequencia' carencia.aluno.cpf %}" class="btn btn-info">
                    <i class="fas fa-history"></i> Ver Histórico de Frequência
                </a>
                
                <a href="{% url 'alunos:detalhar_aluno' carencia.aluno.cpf %}" class="btn btn-primary">
                    <i class="fas fa-user"></i> Ver Perfil do Aluno
                </a>
            </div>
        </div>
    </div>
    
    <!-- Histórico de ações -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Histórico de Ações</h5>
        </div>
        <div class="card-body p-0">
            <ul class="list-group list-group-flush">
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-exclamation-circle text-danger"></i> 
                            <strong>Carência identificada</strong>
                            {% if carencia.identificado_por %}
                            por {{ carencia.identificado_por.get_full_name|default:carencia.identificado_por.username }}
                            {% endif %}
                        </div>
                        <div>{{ carencia.data_identificacao|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                
                {% if carencia.data_acompanhamento %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-clock text-warning"></i> 
                            <strong>Acompanhamento iniciado</strong>
                            {% if carencia.acompanhado_por %}
                            por {{ carencia.acompanhado_por.get_full_name|default:carencia.acompanhado_por.username }}
                            {% endif %}
                        </div>
                        <div>{{ carencia.data_acompanhamento|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                {% endif %}
                
                {% if carencia.notificacao %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-envelope text-primary"></i> 
                            <strong>Notificação criada</strong>
                            {% if carencia.notificacao.criado_por %}
                            por {{ carencia.notificacao.criado_por.get_full_name|default:carencia.notificacao.criado_por.username }}
                            {% endif %}
                        </div>
                        <div>{{ carencia.notificacao.data_criacao|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                
                {% if carencia.notificacao.data_envio %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-paper-plane text-info"></i> 
                            <strong>Notificação enviada</strong>
                            {% if carencia.notificacao.enviado_por %}
                            por {{ carencia.notificacao.enviado_por.get_full_name|default:carencia.notificacao.enviado_por.username }}
                            {% endif %}
                        </div>
                        <div>{{ carencia.notificacao.data_envio|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                {% endif %}
                
                {% if carencia.notificacao.data_leitura %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-envelope-open text-primary"></i> 
                            <strong>Notificação lida</strong> pelo aluno
                        </div>
                        <div>{{ carencia.notificacao.data_leitura|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                {% endif %}
                
                {% if carencia.notificacao.data_resposta %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-reply text-success"></i> 
                            <strong>Notificação respondida</strong> pelo aluno
                        </div>
                        <div>{{ carencia.notificacao.data_resposta|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                {% endif %}
                {% endif %}
                
                {% if carencia.data_resolucao %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-check-circle text-success"></i> 
                            <strong>Carência resolvida</strong>
                            {% if carencia.resolvido_por %}
                            por {{ carencia.resolvido_por.get_full_name|default:carencia.resolvido_por.username }}
                            {% endif %}
                        </div>
                        <div>{{ carencia.data_resolucao|date:"d/m/Y H:i" }}</div>
                    </div>
                    {% if carencia.observacoes_resolucao %}
                    <div class="mt-1 text-muted">
                        <small>{{ carencia.observacoes_resolucao|truncatewords:20 }}</small>
                    </div>
                    {% endif %}
                </li>
                {% endif %}
                
                {% for log in carencia.logs.all %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas {{ log.get_icone }} {{ log.get_cor }}"></i> 
                            <strong>{{ log.acao }}</strong>
                            {% if log.usuario %}
                            por {{ log.usuario.get_full_name|default:log.usuario.username }}
                            {% endif %}
                        </div>
                        <div>{{ log.data|date:"d/m/Y H:i" }}</div>
                    </div>
                    {% if log.detalhes %}
                    <div class="mt-1 text-muted">
                        <small>{{ log.detalhes }}</small>
                    </div>
                    {% endif %}
                </li>
                {% endfor %}
            </ul>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\detalhar_frequencia.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Detalhes da Frequência</h1>
    
  {% if messages %}
      {% for message in messages %}
          <div class="alert alert-{{ message.tags }}">
              {{ message }}
          </div>
      {% endfor %}
  {% endif %}
    
  <div class="card">
      <div class="card-header">
          <h5 class="mb-0">Informações da Frequência</h5>
      </div>
      <div class="card-body">
          <div class="row mb-3">
              <div class="col-md-6">
                  <p><strong>Aluno:</strong> {{ frequencia.aluno.nome }}</p>
                  <p><strong>Turma:</strong> {{ frequencia.turma.id }}</p>
                  <p><strong>Data:</strong> {{ frequencia.data }}</p>
              </div>
              <div class="col-md-6">
                  <p>
                      <strong>Status:</strong> 
                      {% if frequencia.presente %}
                          <span class="badge bg-success">Presente</span>
                      {% else %}
                          <span class="badge bg-danger">Ausente</span>
                      {% endif %}
                  </p>
                  <p><strong>Registrado por:</strong> {{ frequencia.registrado_por|default:"Não informado" }}</p>
                  <p><strong>Data de registro:</strong> {{ frequencia.data_registro }}</p>
              </div>
          </div>
            
          {% if not frequencia.presente %}
          <div class="mb-3">
              <h6>Justificativa:</h6>
              <div class="p-3 bg-light rounded">
                  {% if frequencia.justificativa %}
                      {{ frequencia.justificativa|linebreaks }}
                  {% else %}
                      <em>Nenhuma justificativa fornecida.</em>
                  {% endif %}
              </div>
          </div>
          {% endif %}
            
          <div class="d-grid gap-2 d-md-flex justify-content-md-end">
              <a href="{% url 'frequencias:editar_frequencia' frequencia.id %}" class="btn btn-warning">Editar</a>
              <a href="{% url 'frequencias:excluir_frequencia' frequencia.id %}" class="btn btn-danger">Excluir</a>
              <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">Voltar</a>
          </div>
      </div>
  </div>
</div>
{% endblock %}




### Arquivo: frequencias\templates\frequencias\detalhar_frequencia_mensal.html

html
{% extends 'base.html' %}

{% block title %}Detalhes da Frequência Mensal{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Padronizar botões de ação -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Detalhes da Frequência Mensal</h1>
        <div class="btn-group">
            <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'frequencias:editar_frequencia_mensal' frequencia.id %}" class="btn btn-warning">
                <i class="fas fa-edit"></i> Editar
            </a>
            <a href="{% url 'frequencias:excluir_frequencia_mensal' frequencia.id %}" class="btn btn-danger">
                <i class="fas fa-trash"></i> Excluir
            </a>
            <a href="{% url 'frequencias:recalcular_carencias' frequencia.id %}" class="btn btn-primary">
                <i class="fas fa-sync"></i> Recalcular Carências
            </a>
            <a href="{% url 'frequencias:exportar_frequencia_csv' frequencia.id %}" class="btn btn-success">
                <i class="fas fa-file-csv"></i> Exportar CSV
            </a>
        </div>
    </div>
    
    <!-- Informações da frequência -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Informações Gerais</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Turma:</strong> {{ frequencia.turma.nome }}</p>
                    <p><strong>Curso:</strong> {{ frequencia.turma.curso.nome }}</p>
                    <p><strong>Período:</strong> {{ frequencia.get_mes_display }}/{{ frequencia.ano }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Percentual Mínimo:</strong> {{ frequencia.percentual_minimo }}%</p>
                    <p><strong>Criado em:</strong> {{ frequencia.created_at|date:"d/m/Y H:i" }}</p>
                    <p><strong>Última atualização:</strong> {{ frequencia.updated_at|date:"d/m/Y H:i" }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Estatísticas -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Estatísticas</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-4">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Total de Alunos</h5>
                            <p class="card-text display-4">{{ total_alunos }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Alunos em Carência</h5>
                            <p class="card-text display-4">{{ carencias|length }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Percentual de Carência</h5>
                            <p class="card-text display-4">
                                {% if total_alunos > 0 %}
                                {{ carencias|length|multiply:100|divide:total_alunos|floatformat:1 }}%
                                {% else %}
                                0%
                                {% endif %}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="mt-4">
                <canvas id="grafico-frequencia"></canvas>
            </div>
        </div>
    </div>
    
    <!-- Alunos em carência -->
    <div class="card">
        <div class="card-header bg-danger text-white">
            <h5 class="mb-0">Alunos em Carência</h5>
        </div>
        <div class="card-body">
            {% if carencias %}
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Aluno</th>
                            <th>Percentual de Presença</th>
                            <th>Status</th>
                            <th>Observações</th>
                            <th>Ações</th>
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
                            <td>
                                <div class="progress" style="height: 20px;">
                                    <div class="progress-bar {% if carencia.percentual_presenca < frequencia.percentual_minimo %}bg-danger{% else %}bg-success{% endif %}" role="progressbar" 
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
                            <td>{{ carencia.observacoes|default:"Sem observações"|truncatechars:50 }}</td>
                            <td>
                                <div class="btn-group">
                                    <a href="{% url 'frequencias:editar_carencia' carencia.id %}" 
                                       class="btn btn-sm btn-warning" title="Editar">
                                        <i class="fas fa-edit"></i>
                                    </a>
                                    <a href="{% url 'frequencias:detalhar_carencia' carencia.id %}" 
                                       class="btn btn-sm btn-info" title="Detalhes">
                                        <i class="fas fa-eye"></i>
                                    </a>
                                    <a href="{% url 'alunos:detalhar_aluno' carencia.aluno.cpf %}" 
                                       class="btn btn-sm btn-primary" title="Ver aluno">
                                        <i class="fas fa-user"></i>
                                    </a>
                                </div>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="alert alert-success">
                <i class="fas fa-check-circle me-2"></i>
                Não há alunos em carência para esta frequência mensal.
            </div>
            {% endif %}
        </div>
        <div class="card-footer">
            <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">
                <i class="fas fa-list"></i> Voltar para a lista
            </a>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Gráfico de frequência
        const ctxFrequencia = document.getElementById('grafico-frequencia').getContext('2d');
        new Chart(ctxFrequencia, {
            type: 'bar',
            data: {
                labels: {{ alunos_labels|safe }},
                datasets: [{
                    label: 'Percentual de Presença',
                    data: {{ percentuais_presenca|safe }},
                    backgroundColor: function(context) {
                        const value = context.dataset.data[context.dataIndex];
                        return value < {{ frequencia.percentual_minimo }} ? 
                            'rgba(220, 53, 69, 0.7)' : 'rgba(40, 167, 69, 0.7)';
                    },
                    borderColor: function(context) {
                        const value = context.dataset.data[context.dataIndex];
                        return value < {{ frequencia.percentual_minimo }} ? 
                            'rgba(220, 53, 69, 1)' : 'rgba(40, 167, 69, 1)';
                    },
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
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
    });
</script>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\detalhar_notificacao.html

html
{% extends 'base.html' %}

{% block title %}Detalhes da Notificação{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Detalhes da Notificação</h1>
        <div>
            {% if notificacao.carencia %}
            <a href="{% url 'frequencias:detalhar_carencia' notificacao.carencia.id %}" class="btn btn-secondary me-2">
                <i class="fas fa-exclamation-triangle"></i> Ver Carência
            </a>
            {% endif %}
            <a href="javascript:history.back()" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
        </div>
    </div>
    
    <!-- Status da notificação -->
    <div class="alert 
        {% if notificacao.status == 'PENDENTE' %}alert-secondary
        {% elif notificacao.status == 'ENVIADA' %}alert-info
        {% elif notificacao.status == 'LIDA' %}alert-primary
        {% elif notificacao.status == 'RESPONDIDA' %}alert-success
        {% endif %}">
        <div class="d-flex justify-content-between align-items-center">
            <div>
                <h5 class="alert-heading mb-1">
                    {% if notificacao.status == 'PENDENTE' %}
                    <i class="fas fa-clock"></i> Notificação Pendente
                    {% elif notificacao.status == 'ENVIADA' %}
                    <i class="fas fa-paper-plane"></i> Notificação Enviada
                    {% elif notificacao.status == 'LIDA' %}
                    <i class="fas fa-envelope-open"></i> Notificação Lida
                    {% elif notificacao.status == 'RESPONDIDA' %}
                    <i class="fas fa-reply"></i> Notificação Respondida
                    {% endif %}
                </h5>
                <p class="mb-0">
                    {% if notificacao.status == 'PENDENTE' %}
                    Esta notificação ainda não foi enviada ao aluno.
                    {% elif notificacao.status == 'ENVIADA' %}
                    Esta notificação foi enviada em {{ notificacao.data_envio|date:"d/m/Y H:i" }}.
                    {% elif notificacao.status == 'LIDA' %}
                    Esta notificação foi lida pelo aluno em {{ notificacao.data_leitura|date:"d/m/Y H:i" }}.
                    {% elif notificacao.status == 'RESPONDIDA' %}
                    Esta notificação foi respondida pelo aluno em {{ notificacao.data_resposta|date:"d/m/Y H:i" }}.
                    {% endif %}
                </p>
            </div>
            <div>
                {% if notificacao.status == 'PENDENTE' %}
                <a href="{% url 'frequencias:enviar_notificacao' notificacao.id %}" class="btn btn-primary">
                    <i class="fas fa-paper-plane"></i> Enviar Agora
                </a>
                {% elif notificacao.status == 'ENVIADA' or notificacao.status == 'LIDA' %}
                <a href="{% url 'frequencias:reenviar_notificacao' notificacao.id %}" class="btn btn-outline-primary">
                    <i class="fas fa-sync"></i> Reenviar
                </a>
                {% endif %}
            </div>
        </div>
    </div>
    
    <!-- Informações do destinatário -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Destinatário</h5>
        </div>
        <div class="card-body">
            <div class="d-flex align-items-center">
                {% if notificacao.aluno.foto %}
                <img src="{{ notificacao.aluno.foto.url }}" alt="{{ notificacao.aluno.nome }}" 
                     class="rounded-circle me-3" width="60" height="60" style="object-fit: cover;">
                {% else %}
                <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-3"
                     style="width: 60px; height: 60px; color: white; font-size: 1.5rem;">
                    {{ notificacao.aluno.nome|first|upper }}
                </div>
                {% endif %}
                <div>
                    <h5 class="mb-1">{{ notificacao.aluno.nome }}</h5>
                    <p class="mb-0">{{ notificacao.aluno.email }}</p>
                    {% if notificacao.aluno.celular_primeiro_contato %}
                    <p class="mb-0">{{ notificacao.aluno.celular_primeiro_contato }}</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    
    <!-- Conteúdo da notificação -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Conteúdo da Notificação</h5>
        </div>
        <div class="card-body">
            <div class="mb-3">
                <h6>Assunto:</h6>
                <p class="mb-0">{{ notificacao.assunto }}</p>
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
            
            <div class="mt-3">
                <p class="text-muted mb-0">
                    <small>Criada por: {{ notificacao.criado_por.get_full_name|default:notificacao.criado_por.username }} em {{ notificacao.data_criacao|date:"d/m/Y H:i" }}</small>
                </p>
            </div>
        </div>
    </div>
    
    <!-- Resposta do aluno (se houver) -->
    {% if notificacao.resposta %}
    <div class="card mb-4 border-success">
        <div class="card-header bg-success text-white">
            <h5 class="mb-0">Resposta do Aluno</h5>
        </div>
        <div class="card-body">
            <div class="mb-3">
                <h6>Assunto:</h6>
                <p class="mb-0">{{ notificacao.resposta.assunto }}</p>
            </div>
            
            <div class="mb-3">
                <h6>Mensagem:</h6>
                <div class="p-3 bg-light rounded border">
                    {{ notificacao.resposta.mensagem|linebreaks }}
                </div>
            </div>
            
            {% if notificacao.resposta.anexos.all %}
            <div>
                <h6>Anexos:</h6>
                <ul class="list-group">
                    {% for anexo in notificacao.resposta.anexos.all %}
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
            
            <div class="mt-3">
                <p class="text-muted mb-0">
                    <small>Respondido em: {{ notificacao.data_resposta|date:"d/m/Y H:i" }}</small>
                </p>
            </div>
            
            {% if notificacao.resposta.solicitar_compensacao %}
            <div class="alert alert-warning mt-3">
                <i class="fas fa-exclamation-circle"></i> O aluno solicitou opções de compensação de faltas.
            </div>
            {% endif %}
        </div>
    </div>
    {% endif %}
    
    <!-- Ações -->
    <div class="card mb-4">
        <div class="card-header bg-secondary text-white">
            <h5 class="mb-0">Ações</h5>
        </div>
        <div class="card-body">
            <div class="d-flex flex-wrap gap-2">
                {% if notificacao.status == 'PENDENTE' %}
                <a href="{% url 'frequencias:editar_notificacao' notificacao.id %}" class="btn btn-warning">
                    <i class="fas fa-edit"></i> Editar Notificação
                </a>
                <a href="{% url 'frequencias:enviar_notificacao' notificacao.id %}" class="btn btn-primary">
                    <i class="fas fa-paper-plane"></i> Enviar Notificação
                </a>
                {% elif notificacao.status == 'ENVIADA' or notificacao.status == 'LIDA' %}
                <a href="{% url 'frequencias:reenviar_notificacao' notificacao.id %}" class="btn btn-primary">
                    <i class="fas fa-sync"></i> Reenviar Notificação
                </a>
                {% endif %}
                
                {% if notificacao.status == 'RESPONDIDA' %}
                <a href="{% url 'frequencias:responder_aluno' notificacao.id %}" class="btn btn-success">
                    <i class="fas fa-reply"></i> Responder ao Aluno
                </a>
                {% endif %}
                
                {% if notificacao.carencia and notificacao.carencia.status != 'RESOLVIDO' %}
                <a href="{% url 'frequencias:resolver_carencia' notificacao.carencia.id %}" class="btn btn-success">
                    <i class="fas fa-check"></i> Resolver Carência
                </a>
                {% endif %}
                
                <a href="{% url 'frequencias:historico_frequencia' notificacao.aluno.cpf %}" class="btn btn-info">
                    <i class="fas fa-history"></i> Ver Histórico de Frequência
                </a>
                
                <a href="{% url 'alunos:detalhar_aluno' notificacao.aluno.cpf %}" class="btn btn-primary">
                    <i class="fas fa-user"></i> Ver Perfil do Aluno
                </a>
            </div>
        </div>
    </div>
    
    <!-- Histórico de ações -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Histórico de Ações</h5>
        </div>
        <div class="card-body p-0">
            <ul class="list-group list-group-flush">
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-plus-circle text-success"></i> 
                            <strong>Notificação criada</strong> por {{ notificacao.criado_por.get_full_name|default:notificacao.criado_por.username }}
                        </div>
                        <div>{{ notificacao.data_criacao|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                
                {% if notificacao.data_envio %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-paper-plane text-primary"></i> 
                            <strong>Notificação enviada</strong>
                            {% if notificacao.enviado_por %}
                            por {{ notificacao.enviado_por.get_full_name|default:notificacao.enviado_por.username }}
                            {% endif %}
                        </div>
                        <div>{{ notificacao.data_envio|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                {% endif %}
                
                {% if notificacao.data_leitura %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-envelope-open text-info"></i> 
                            <strong>Notificação lida</strong> pelo aluno
                        </div>
                        <div>{{ notificacao.data_leitura|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                {% endif %}
                
                {% if notificacao.data_resposta %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-reply text-success"></i> 
                            <strong>Notificação respondida</strong> pelo aluno
                        </div>
                        <div>{{ notificacao.data_resposta|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                {% endif %}
                
                {% for log in notificacao.logs.all %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas {{ log.get_icone }} {{ log.get_cor }}"></i> 
                            <strong>{{ log.acao }}</strong>
                            {% if log.usuario %}
                            por {{ log.usuario.get_full_name|default:log.usuario.username }}
                            {% endif %}
                        </div>
                        <div>{{ log.data|date:"d/m/Y H:i" }}</div>
                    </div>
                    {% if log.detalhes %}
                    <div class="mt-1 text-muted">
                        <small>{{ log.detalhes }}</small>
                    </div>
                    {% endif %}
                </li>
                {% endfor %}
            </ul>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\editar_carencia.html

html
{% extends 'base.html' %}

{% block title %}Editar Carência{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header bg-warning text-dark">
                    <h4 class="mb-0">Editar Carência</h4>
                </div>
                <div class="card-body">
                    <div class="mb-4">
                        <div class="d-flex align-items-center">
                            {% if carencia.aluno.foto %}
                            <img src="{{ carencia.aluno.foto.url }}" alt="{{ carencia.aluno.nome }}" 
                                 class="rounded-circle me-3" width="60" height="60">
                            {% else %}
                            <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-3"
                                 style="width: 60px; height: 60px; color: white; font-size: 24px;">
                                {{ carencia.aluno.nome|first|upper }}
                            </div>
                            {% endif %}
                            <div>
                                <h5 class="mb-1">{{ carencia.aluno.nome }}</h5>
                                <p class="mb-0 text-muted">{{ carencia.aluno.cpf }}</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card mb-4">
                        <div class="card-body">
                            <p><strong>Frequência Mensal:</strong> {{ carencia.frequencia_mensal.turma.nome }} - {{ carencia.frequencia_mensal.get_mes_display }}/{{ carencia.frequencia_mensal.ano }}</p>
                            <p><strong>Percentual de Presença:</strong> {{ carencia.percentual_presenca }}%</p>
                            <p><strong>Percentual Mínimo Exigido:</strong> {{ carencia.frequencia_mensal.percentual_minimo }}%</p>
                            <p><strong>Déficit:</strong> {{ carencia.frequencia_mensal.percentual_minimo|subtract:carencia.percentual_presenca|floatformat:1 }}%</p>
                        </div>
                    </div>
                    
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
                            <label for="{{ form.observacoes.id_for_label }}" class="form-label">{{ form.observacoes.label }}</label>
                            {{ form.observacoes }}
                            {% if form.observacoes.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.observacoes.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.observacoes.help_text %}
                            <div class="form-text">{{ form.observacoes.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.status.id_for_label }}" class="form-label">{{ form.status.label }}</label>
                            {{ form.status }}
                            {% if form.status.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.status.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.status.help_text %}
                            <div class="form-text">{{ form.status.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3" id="data_resolucao_container" style="display: none;">
                            <label for="{{ form.data_resolucao.id_for_label }}" class="form-label">{{ form.data_resolucao.label }}</label>
                            {{ form.data_resolucao }}
                            {% if form.data_resolucao.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.data_resolucao.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.data_resolucao.help_text %}
                            <div class="form-text">{{ form.data_resolucao.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="d-flex justify-content-between mt-4">
                            <a href="{% url 'frequencias:detalhar_frequencia_mensal' carencia.frequencia_mensal.id %}" class="btn btn-secondary">
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
        // Mostrar/ocultar campo de data de resolução com base no status
        const statusSelect = document.getElementById('id_status');
        const dataResolucaoContainer = document.getElementById('data_resolucao_container');
        
        function toggleDataResolucao() {
            if (statusSelect.value === 'RESOLVIDO') {
                dataResolucaoContainer.style.display = 'block';
                document.getElementById('id_data_resolucao').setAttribute('required', 'required');
            } else {
                dataResolucaoContainer.style.display = 'none';
                document.getElementById('id_data_resolucao').removeAttribute('required');
            }
        }
        
        // Executar na inicialização
        toggleDataResolucao();
        
        // Adicionar evento de mudança
        statusSelect.addEventListener('change', toggleDataResolucao);
    });
</script>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\editar_frequencia.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Registro de FrequÃªncia</h1>
  
    <form method="post">
      {% csrf_token %}
      {% include 'includes/form_errors.html' %}
    
      {% for field in form %}
        {% include 'includes/form_field.html' %}
      {% endfor %}
    
      <button type="submit" class="btn btn-primary">Atualizar</button>
      <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




### Arquivo: frequencias\templates\frequencias\editar_notificacao.html

html
{% extends 'base.html' %}

{% block title %}Editar Notificação{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Editar Notificação</h1>
        <a href="{% url 'frequencias:detalhar_notificacao' notificacao.id %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    {% if notificacao.status != 'PENDENTE' %}
    <div class="alert alert-warning">
        <i class="fas fa-exclamation-triangle"></i> Esta notificação já foi enviada e não pode ser editada.
    </div>
    {% else %}
    
    <!-- Informações da carência -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Informações da Carência</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Aluno:</strong> {{ notificacao.carencia.aluno.nome }}</p>
                    <p><strong>CPF:</strong> {{ notificacao.carencia.aluno.cpf }}</p>
                    <p><strong>Email:</strong> {{ notificacao.carencia.aluno.email }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Turma:</strong> {{ notificacao.carencia.frequencia_mensal.turma.nome }}</p>
                    <p><strong>Curso:</strong> {{ notificacao.carencia.frequencia_mensal.turma.curso.nome }}</p>
                    <p><strong>Período:</strong> {{ notificacao.carencia.frequencia_mensal.get_mes_display }}/{{ notificacao.carencia.frequencia_mensal.ano }}</p>
                </div>
            </div>
            
            <div class="mt-3">
                <h6>Percentual de Presença:</h6>
                <div class="progress" style="height: 25px;">
                    <div class="progress-bar bg-danger" role="progressbar" 
                         style="width: {{ notificacao.carencia.percentual_presenca }}%;" 
                         aria-valuenow="{{ notificacao.carencia.percentual_presenca }}" 
                         aria-valuemin="0" aria-valuemax="100">
                        {{ notificacao.carencia.percentual_presenca }}%
                    </div>
                </div>
                <small class="text-muted">Mínimo exigido: 75%</small>
            </div>
        </div>
    </div>
    
    <!-- Formulário de edição -->
    <div class="card mb-4">
        <div class="card-header bg-warning text-dark">
            <h5 class="mb-0">Editar Notificação</h5>
        </div>
        <div class="card-body">
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="assunto" class="form-label">Assunto</label>
                    <input type="text" class="form-control" id="assunto" name="assunto" 
                           value="{{ notificacao.assunto }}" required>
                </div>
                
                <div class="mb-3">
                    <label for="mensagem" class="form-label">Mensagem</label>
                    <textarea class="form-control" id="mensagem" name="mensagem" rows="10" required>{{ notificacao.mensagem }}</textarea>
                </div>
                
                <div class="mb-3">
                    <label for="anexos" class="form-label">Anexos (opcional)</label>
                    <input type="file" class="form-control" id="anexos" name="anexos" multiple>
                </div>
                
                {% if notificacao.anexos.all %}
                <div class="mb-3">
                    <label class="form-label">Anexos Atuais</label>
                    <ul class="list-group">
                        {% for anexo in notificacao.anexos.all %}
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                            <span>{{ anexo.nome }}</span>
                            <div>
                                <a href="{{ anexo.arquivo.url }}" class="btn btn-sm btn-outline-primary me-2" download>
                                    <i class="fas fa-download"></i> Download
                                </a>
                                <div class="form-check form-check-inline">
                                    <input class="form-check-input" type="checkbox" id="remover_anexo_{{ anexo.id }}" 
                                           name="remover_anexos" value="{{ anexo.id }}">
                                    <label class="form-check-label" for="remover_anexo_{{ anexo.id }}">Remover</label>
                                </div>
                            </div>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
                {% endif %}
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'frequencias:detalhar_notificacao' notificacao.id %}" class="btn btn-secondary">
                        Cancelar
                    </a>
                    <div>
                        <button type="submit" class="btn btn-warning me-2" name="action" value="salvar">
                            <i class="fas fa-save"></i> Salvar Alterações
                        </button>
                        <button type="submit" class="btn btn-primary" name="action" value="salvar_enviar">
                            <i class="fas fa-paper-plane"></i> Salvar e Enviar
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Modelos de mensagem -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Modelos de Mensagem</h5>
        </div>
        <div class="card-body">
            <div class="accordion" id="accordionModelos">
                <div class="accordion-item">
                    <h2 class="accordion-header" id="headingOne">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" 
                                data-bs-target="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
                            Modelo 1: Notificação Padrão
                        </button>
                    </h2>
                    <div id="collapseOne" class="accordion-collapse collapse" aria-labelledby="headingOne" data-bs-parent="#accordionModelos">
                        <div class="accordion-body">
                            <div class="d-flex justify-content-between mb-2">
                                <strong>Assunto: Notificação de Carência de Frequência</strong>
                                <button class="btn btn-sm btn-outline-primary usar-modelo" data-modelo="1">
                                    <i class="fas fa-copy"></i> Usar este modelo
                                </button>
                            </div>
                            <pre class="bg-light p-3 rounded">Prezado(a) {{ notificacao.carencia.aluno.nome }},

Esperamos que esteja bem. Estamos entrando em contato para informar que foi identificada uma carência de frequência em suas aulas do curso {{ notificacao.carencia.frequencia_mensal.turma.curso.nome }}, na turma {{ notificacao.carencia.frequencia_mensal.turma.nome }}, durante o período de {{ notificacao.carencia.frequencia_mensal.get_mes_display }}/{{ notificacao.carencia.frequencia_mensal.ano }}.

Seu percentual de presença no período foi de {{ notificacao.carencia.percentual_presenca }}%, abaixo do mínimo exigido de 75%.

Gostaríamos de lembrá-lo(a) que a frequência regular é fundamental para o bom aproveitamento do curso e constitui um dos requisitos para aprovação.

Solicitamos que entre em contato conosco para justificar as ausências e discutir possíveis alternativas para compensação das aulas perdidas.

Estamos à disposição para quaisquer esclarecimentos.

Atenciosamente,
Equipe Pedagógica</pre>
                        </div>
                    </div>
                </div>
                
                <div class="accordion-item">
                    <h2 class="accordion-header" id="headingTwo">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" 
                                data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                            Modelo 2: Notificação com Urgência
                        </button>
                    </h2>
                    <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo" data-bs-parent="#accordionModelos">
                        <div class="accordion-body">
                            <div class="d-flex justify-content-between mb-2">
                                <strong>Assunto: URGENTE - Notificação de Carência de Frequência</strong>
                                <button class="btn btn-sm btn-outline-primary usar-modelo" data-modelo="2">
                                    <i class="fas fa-copy"></i> Usar este modelo
                                </button>
                            </div>
                            <pre class="bg-light p-3 rounded">Prezado(a) {{ notificacao.carencia.aluno.nome }},

NOTIFICAÇÃO URGENTE

Identificamos uma situação crítica em relação à sua frequência no curso {{ notificacao.carencia.frequencia_mensal.turma.curso.nome }}, turma {{ notificacao.carencia.frequencia_mensal.turma.nome }}.

Seu percentual de presença no período de {{ notificacao.carencia.frequencia_mensal.get_mes_display }}/{{ notificacao.carencia.frequencia_mensal.ano }} foi de apenas {{ notificacao.carencia.percentual_presenca }}%, muito abaixo do mínimo exigido de 75%.

Esta situação coloca em risco sua aprovação no curso e, caso não seja regularizada com urgência, poderá resultar em reprovação por frequência insuficiente.

Solicitamos seu comparecimento à secretaria no prazo máximo de 3 dias úteis para apresentar justificativas e discutir medidas de recuperação.

Caso já possua justificativas para as ausências (atestados médicos ou outros documentos), favor responder a este e-mail com os documentos anexados.

Atenciosamente,
Coordenação Pedagógica</pre>
                        </div>
                    </div>
                </div>
                
                <div class="accordion-item">
                    <h2 class="accordion-header" id="headingThree">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" 
                                data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                            Modelo 3: Notificação com Opções de Recuperação
                        </button>
                    </h2>
                    <div id="collapseThree" class="accordion-collapse collapse" aria-labelledby="headingThree" data-bs-parent="#accordionModelos">
                        <div class="accordion-body">
                            <div class="d-flex justify-content-between mb-2">
                                <strong>Assunto: Notificação de Carência e Opções de Recuperação</strong>
                                <button class="btn btn-sm btn-outline-primary usar-modelo" data-modelo="3">
                                    <i class="fas fa-copy"></i> Usar este modelo
                                </button>
                            </div>
                            <pre class="bg-light p-3 rounded">Prezado(a) {{ notificacao.carencia.aluno.nome }},

Esperamos que esteja bem. Estamos entrando em contato para informar que foi identificada uma carência de frequência em suas aulas do curso {{ notificacao.carencia.frequencia_mensal.turma.curso.nome }}, na turma {{ notificacao.carencia.frequencia_mensal.turma.nome }}, durante o período de {{ notificacao.carencia.frequencia_mensal.get_mes_display }}/{{ notificacao.carencia.frequencia_mensal.ano }}.

Seu percentual de presença no período foi de {{ notificacao.carencia.percentual_presenca }}%, abaixo do mínimo exigido de 75%.

Para regularizar sua situação, oferecemos as seguintes opções de recuperação:

1. Participação em aulas de reposição nos dias XX/XX e XX/XX, das XX:XX às XX:XX.
2. Realização de trabalho complementar sobre os temas abordados nas aulas perdidas.
3. Participação em atividades extras programadas para os dias XX/XX.

Solicitamos que entre em contato conosco até o dia XX/XX para informar qual opção deseja seguir.

Lembramos que a regularização da frequência é fundamental para a continuidade no curso e para o aproveitamento adequado do conteúdo.

Estamos à disposição para quaisquer esclarecimentos.

Atenciosamente,
Equipe Pedagógica</pre>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    {% endif %}
</div>

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Manipuladores para os botões de modelo
        const botoesModelo = document.querySelectorAll('.usar-modelo');
        const campoAssunto = document.getElementById('assunto');
        const campoMensagem = document.getElementById('mensagem');
        
        // Modelos de assunto
        const assuntosModelo = {
            "1": "Notificação de Carência de Frequência",
            "2": "URGENTE - Notificação de Carência de Frequência",
            "3": "Notificação de Carência e Opções de Recuperação"
        };
        
        // Função para obter o texto do modelo
        function obterTextoModelo(modeloId) {
            const acordeao = document.querySelector(`#collapse${modeloId} pre`);
            return acordeao ? acordeao.textContent.trim() : '';
        }
        
        // Adicionar evento de clique aos botões de modelo
        botoesModelo.forEach(botao => {
            botao.addEventListener('click', function() {
                const modeloId = this.getAttribute('data-modelo');
                
                // Confirmar antes de substituir o conteúdo atual
                if (campoMensagem.value.trim() !== '') {
                    if (!confirm('Isso substituirá o conteúdo atual da mensagem. Deseja continuar?')) {
                        return;
                    }
                }
                
                // Preencher os campos com o modelo selecionado
                campoAssunto.value = assuntosModelo[modeloId] || '';
                campoMensagem.value = obterTextoModelo(modeloId);
                
                // Fechar o acordeão
                const accordion = bootstrap.Collapse.getInstance(document.querySelector(`#collapse${modeloId}`));
                if (accordion) {
                    accordion.hide();
                }
                
                // Rolar até o formulário
                document.querySelector('.card-header.bg-warning').scrollIntoView({ behavior: 'smooth' });
            });
        });
    });
</script>
{% endblock %}
{% endblock %}



### Arquivo: frequencias\templates\frequencias\enviar_notificacao.html

html
{% extends 'base.html' %}

{% block title %}Enviar Notificação{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Enviar Notificação</h1>
        <a href="{% url 'frequencias:detalhar_notificacao' notificacao.id %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    {% if notificacao.status != 'PENDENTE' %}
    <div class="alert alert-warning">
        <i class="fas fa-exclamation-triangle"></i> Esta notificação já foi enviada em {{ notificacao.data_envio|date:"d/m/Y H:i" }}.
    </div>
    {% else %}
    
    <!-- Informações do destinatário -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Informações do Destinatário</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <div class="d-flex align-items-center mb-3">
                        {% if notificacao.carencia.aluno.foto %}
                        <img src="{{ notificacao.carencia.aluno.foto.url }}" alt="{{ notificacao.carencia.aluno.nome }}" 
                             class="rounded-circle me-3" width="60" height="60" style="object-fit: cover;">
                        {% else %}
                        <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-3"
                             style="width: 60px; height: 60px; color: white; font-size: 1.5rem;">
                            {{ notificacao.carencia.aluno.nome|first|upper }}
                        </div>
                        {% endif %}
                        <div>
                            <h5 class="mb-1">{{ notificacao.carencia.aluno.nome }}</h5>
                            <p class="text-muted mb-0">{{ notificacao.carencia.aluno.email }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <p><strong>Turma:</strong> {{ notificacao.carencia.frequencia_mensal.turma.nome }}</p>
                    <p><strong>Curso:</strong> {{ notificacao.carencia.frequencia_mensal.turma.curso.nome }}</p>
                    <p><strong>Período:</strong> {{ notificacao.carencia.frequencia_mensal.get_mes_display }}/{{ notificacao.carencia.frequencia_mensal.ano }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Prévia da notificação -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Prévia da Notificação</h5>
        </div>
        <div class="card-body">
            <div class="mb-3">
                <h6>Assunto:</h6>
                <p>{{ notificacao.assunto }}</p>
            </div>
            
            <div>
                <h6>Mensagem:</h6>
                <div class="p-3 bg-light rounded border">
                    {{ notificacao.mensagem|linebreaks }}
                </div>
            </div>
            
            {% if notificacao.anexos.all %}
            <div class="mt-3">
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
            
            <div class="mt-3">
                <a href="{% url 'frequencias:editar_notificacao' notificacao.id %}" class="btn btn-warning">
                    <i class="fas fa-edit"></i> Editar Notificação
                </a>
            </div>
        </div>
    </div>
    
    <!-- Formulário de envio -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Enviar Notificação</h5>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="enviar_copia" name="enviar_copia">
                    <label class="form-check-label" for="enviar_copia">
                        Enviar cópia para mim
                    </label>
                </div>
                
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="marcar_acompanhamento" name="marcar_acompanhamento" checked>
                    <label class="form-check-label" for="marcar_acompanhamento">
                        Marcar carência como "Em Acompanhamento"
                    </label>
                </div>
                
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> A notificação será enviada para o email <strong>{{ notificacao.carencia.aluno.email }}</strong>. 
                    Certifique-se de que o endereço está correto.
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'frequencias:detalhar_notificacao' notificacao.id %}" class="btn btn-secondary">
                        Cancelar
                    </a>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-paper-plane"></i> Enviar Notificação
                    </button>
                </div>
            </form>
        </div>
    </div>
    
    {% endif %}
</div>
{% endblock %}


'''