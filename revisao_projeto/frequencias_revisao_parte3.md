'''
# Revisão da Funcionalidade: frequencias

## Arquivos forms.py:


### Arquivo: frequencias\templates\frequencias\listar_carencias.html

html
{% extends 'base.html' %}

{% block title %}Carências de Frequência{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Carências de Frequência</h1>
        <div>
            <a href="{% url 'dashboard' %}" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'frequencias:relatorio_carencias' %}" class="btn btn-info">
                <i class="fas fa-chart-bar"></i> Relatório
            </a>
        </div>
    </div>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-3">
                    <label for="aluno" class="form-label">Aluno</label>
                    <input type="text" class="form-control" id="aluno" name="aluno" value="{{ filtros.aluno|default:'' }}" placeholder="Nome ou CPF">
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
                
                <div class="col-md-2">
                    <label for="status" class="form-label">Status</label>
                    <select class="form-select" id="status" name="status">
                        <option value="">Todos</option>
                        <option value="PENDENTE" {% if filtros.status == 'PENDENTE' %}selected{% endif %}>Pendente</option>
                        <option value="EM_ACOMPANHAMENTO" {% if filtros.status == 'EM_ACOMPANHAMENTO' %}selected{% endif %}>Em Acompanhamento</option>
                        <option value="RESOLVIDO" {% if filtros.status == 'RESOLVIDO' %}selected{% endif %}>Resolvido</option>
                    </select>
                </div>
                
                <div class="col-md-2">
                    <label for="periodo" class="form-label">Período</label>
                    <select class="form-select" id="periodo" name="periodo">
                        <option value="">Todos</option>
                        {% for periodo in periodos %}
                        <option value="{{ periodo.id }}" {% if filtros.periodo == periodo.id|stringformat:"s" %}selected{% endif %}>
                            {{ periodo.mes }}/{{ periodo.ano }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="col-md-2 d-flex align-items-end">
                    <button type="submit" class="btn btn-primary w-100">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Estatísticas rápidas -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card bg-danger text-white">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="card-title mb-0">Pendentes</h6>
                            <h2 class="mt-2 mb-0">{{ stats.pendentes }}</h2>
                        </div>
                        <i class="fas fa-exclamation-circle fa-3x opacity-50"></i>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card bg-warning text-dark">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="card-title mb-0">Em Acompanhamento</h6>
                            <h2 class="mt-2 mb-0">{{ stats.em_acompanhamento }}</h2>
                        </div>
                        <i class="fas fa-clock fa-3x opacity-50"></i>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card bg-success text-white">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="card-title mb-0">Resolvidas</h6>
                            <h2 class="mt-2 mb-0">{{ stats.resolvidas }}</h2>
                        </div>
                        <i class="fas fa-check-circle fa-3x opacity-50"></i>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card bg-primary text-white">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="card-title mb-0">Total</h6>
                            <h2 class="mt-2 mb-0">{{ stats.total }}</h2>
                        </div>
                        <i class="fas fa-list fa-3x opacity-50"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Lista de carências -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Carências Identificadas</h5>
        </div>
        <div class="card-body p-0">
            <div class="table-responsive">
                <table class="table table-hover mb-0">
                    <thead class="table-light">
                        <tr>
                            <th>Aluno</th>
                            <th>Curso</th>
                            <th>Turma</th>
                            <th>Período</th>
                            <th>% Presença</th>
                            <th>Status</th>
                            <th>Notificação</th>
                            <th>Data</th>
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
                                         class="rounded-circle me-2" width="40" height="40" style="object-fit: cover;">
                                    {% else %}
                                    <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-2"
                                         style="width: 40px; height: 40px; color: white; font-size: 1rem;">
                                        {{ carencia.aluno.nome|first|upper }}
                                    </div>
                                    {% endif %}
                                    <div>
                                        <div>{{ carencia.aluno.nome }}</div>
                                        <small class="text-muted">{{ carencia.aluno.cpf }}</small>
                                    </div>
                                </div>
                            </td>
                            <td>{{ carencia.frequencia_mensal.turma.curso.nome }}</td>
                            <td>{{ carencia.frequencia_mensal.turma.nome }}</td>
                            <td>{{ carencia.frequencia_mensal.get_mes_display }}/{{ carencia.frequencia_mensal.ano }}</td>
                            <td>
                                <div class="d-flex align-items-center">
                                    <div class="progress flex-grow-1 me-2" style="height: 8px;">
                                        <div class="progress-bar bg-danger" role="progressbar" 
                                             style="width: {{ carencia.percentual_presenca }}%;" 
                                             aria-valuenow="{{ carencia.percentual_presenca }}" 
                                             aria-valuemin="0" aria-valuemax="100">
                                        </div>
                                    </div>
                                    <span>{{ carencia.percentual_presenca|floatformat:1 }}%</span>
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
                            <td>
                                {% if carencia.notificacao %}
                                    {% if carencia.notificacao.status == 'PENDENTE' %}
                                    <span class="badge bg-secondary">Pendente</span>
                                    {% elif carencia.notificacao.status == 'ENVIADA' %}
                                    <span class="badge bg-info">Enviada</span>
                                    {% elif carencia.notificacao.status == 'LIDA' %}
                                    <span class="badge bg-primary">Lida</span>
                                    {% elif carencia.notificacao.status == 'RESPONDIDA' %}
                                    <span class="badge bg-success">Respondida</span>
                                    {% endif %}
                                {% else %}
                                <span class="badge bg-light text-dark">Não criada</span>
                                {% endif %}
                            </td>
                            <td>{{ carencia.data_identificacao|date:"d/m/Y" }}</td>
                            <td>
                                <div class="btn-group">
                                    <a href="{% url 'frequencias:detalhar_carencia' carencia.id %}" class="btn btn-sm btn-info">
                                        <i class="fas fa-eye"></i>
                                    </a>
                                    
                                    {% if carencia.status == 'PENDENTE' %}
                                    <a href="{% url 'frequencias:iniciar_acompanhamento' carencia.id %}" class="btn btn-sm btn-warning" title="Iniciar Acompanhamento">
                                        <i class="fas fa-clock"></i>
                                    </a>
                                    {% endif %}
                                    
                                    {% if carencia.status != 'RESOLVIDO' %}
                                    <a href="{% url 'frequencias:resolver_carencia' carencia.id %}" class="btn btn-sm btn-success" title="Resolver Carência">
                                        <i class="fas fa-check"></i>
                                    </a>
                                    
                                    {% if not carencia.notificacao %}
                                    <a href="{% url 'frequencias:criar_notificacao' carencia.id %}" class="btn btn-sm btn-primary" title="Criar Notificação">
                                        <i class="fas fa-envelope"></i>
                                    </a>
                                    {% endif %}
                                    {% endif %}
                                </div>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="9" class="text-center py-4">
                                <div class="alert alert-info mb-0">
                                    <i class="fas fa-info-circle"></i> Nenhuma carência encontrada com os filtros selecionados.
                                </div>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <p class="mb-0 text-muted">Exibindo {{ carencias|length }} de {{ paginator.count }} carências</p>
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
                            <span class="page-link">«</span>
                        </li>
                        {% endif %}
                        
                        {% for i in paginator.page_range %}
                            {% if page_obj.number == i %}
                            <li class="page-item active">
                                <span class="page-link">{{ i }}</span>
                            </li>
                            {% else %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ i }}{% for key, value in filtros.items %}&{{ key }}={{ value }}{% endfor %}">{{ i }}</a>
                            </li>
                            {% endif %}
                        {% endfor %}
                        
                        {% if page_obj.has_next %}
                        <li class="page-item">
                            <a class="page-link" href="?page={{ page_obj.next_page_number }}{% for key, value in filtros.items %}&{{ key }}={{ value }}{% endfor %}" aria-label="Próximo">
                                <span aria-hidden="true">»</span>
                            </a>
                        </li>
                        {% else %}
                        <li class="page-item disabled">
                            <span class="page-link">»</span>
                        </li>
                        {% endif %}
                    </ul>
                </nav>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\listar_frequencias.html

html
{% extends 'base.html' %}

{% block title %}Lista de Frequências Mensais{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <!-- Padronizar cabeçalho com botões -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Lista de Frequências Mensais</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'frequencias:criar_frequencia_mensal' %}" class="btn btn-primary me-2">
                <i class="fas fa-plus"></i> Nova Frequência
            </a>
            <a href="{% url 'frequencias:exportar_frequencias' %}" class="btn btn-success me-2">
                <i class="fas fa-file-export"></i> Exportar CSV
            </a>
            <a href="{% url 'frequencias:importar_frequencias' %}" class="btn btn-info me-2">
                <i class="fas fa-file-import"></i> Importar CSV
            </a>
            <a href="{% url 'frequencias:dashboard' %}" class="btn btn-success">
                <i class="fas fa-chart-bar"></i> Dashboard
            </a>
        </div>
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
                <div class="col-12 mt-3">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                    <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">
                        <i class="fas fa-broom"></i> Limpar Filtros
                    </a>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Tabela de frequências -->
    <div class="card">
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Turma</th>
                            <th>Mês/Ano</th>
                            <th>Percentual Mínimo</th>
                            <th>Alunos em Carência</th>
                            <th>Última Atualização</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for frequencia in frequencias %}
                        <tr>
                            <td>
                                <div class="d-flex align-items-center">
                                    <span class="badge bg-primary me-2">{{ frequencia.turma.codigo }}</span>
                                    <span>{{ frequencia.turma.nome }}</span>
                                </div>
                            </td>
                            <td>{{ frequencia.get_mes_display }}/{{ frequencia.ano }}</td>
                            <td>{{ frequencia.percentual_minimo }}%</td>
                            <td>
                                <span class="badge bg-{% if frequencia.carencias.count > 0 %}danger{% else %}success{% endif %}">
                                    {{ frequencia.carencias.count }}
                                </span>
                            </td>
                            <td>{{ frequencia.updated_at|date:"d/m/Y H:i" }}</td>
                            <td>
                                <div class="btn-group">
                                    <a href="{% url 'frequencias:detalhar_frequencia_mensal' frequencia.id %}" class="btn btn-sm btn-info" title="Ver detalhes da frequência">
                                        <i class="fas fa-eye"></i> Detalhes
                                    </a>
                                    <a href="{% url 'frequencias:editar_frequencia_mensal' frequencia.id %}" class="btn btn-sm btn-warning" title="Editar frequência">
                                        <i class="fas fa-edit"></i> Editar
                                    </a>
                                    <a href="{% url 'frequencias:excluir_frequencia_mensal' frequencia.id %}" class="btn btn-sm btn-danger" title="Excluir frequência">
                                        <i class="fas fa-trash"></i> Excluir
                                    </a>
                                    <a href="{% url 'frequencias:recalcular_carencias' frequencia.id %}" class="btn btn-sm btn-primary" title="Recalcular carências">
                                        <i class="fas fa-sync"></i> Recalcular
                                    </a>
                                </div>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="6" class="text-center py-4">
                                <div class="alert alert-info mb-0">
                                    Nenhuma frequência mensal encontrada com os filtros selecionados.
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
                <span>Total: {{ page_obj.paginator.count }} frequências mensais</span>
                <span>Página {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}</span>
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
    });
</script>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\listar_notificacoes_carencia.html

html
<!-- Padronizar cabeçalho com botões -->
<div class="d-flex justify-content-between align-items-center mb-3">
    <h1>Notificações de Carência</h1>
    <div>
        <a href="javascript:history.back()" class="btn btn-secondary me-2">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
        <a href="{% url 'frequencias:dashboard' %}" class="btn btn-success">
            <i class="fas fa-chart-bar"></i> Dashboard
        </a>
    </div>
</div>

<!-- Padronizar botões de ação na tabela -->
<td>
    <div class="table-actions">
        <a href="{% url 'frequencias:detalhar_notificacao' notificacao.id %}" class="btn btn-sm btn-info" title="Ver detalhes da notificação">
            <i class="fas fa-eye"></i> Detalhes
        </a>
        {% if notificacao.status == 'PENDENTE' %}
        <a href="{% url 'frequencias:editar_notificacao' notificacao.id %}" class="btn btn-sm btn-warning" title="Editar notificação">
            <i class="fas fa-edit"></i> Editar
        </a>
        <a href="{% url 'frequencias:enviar_notificacao' notificacao.id %}" class="btn btn-sm btn-primary" title="Enviar notificação">
            <i class="fas fa-paper-plane"></i> Enviar
        </a>
        {% elif notificacao.status == 'ENVIADA' or notificacao.status == 'LIDA' %}
        <a href="{% url 'frequencias:reenviar_notificacao' notificacao.id %}" class="btn btn-sm btn-primary" title="Reenviar notificação">
            <i class="fas fa-sync"></i> Reenviar
        </a>
        {% endif %}
        {% if notificacao.status == 'RESPONDIDA' %}
        <a href="{% url 'frequencias:responder_aluno' notificacao.id %}" class="btn btn-sm btn-success" title="Responder ao aluno">
            <i class="fas fa-reply"></i> Responder
        </a>
        {% endif %}
    </div>
</td>



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


'''