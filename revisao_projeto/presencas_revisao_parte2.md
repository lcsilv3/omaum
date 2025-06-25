'''
# Revisão da Funcionalidade: presencas

## Arquivos forms.py:


### Arquivo: presencas\templates\presencas\academicas\formulario_presencas_multiplas_academica_passo1.html

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



### Arquivo: presencas\templates\presencas\academicas\formulario_presencas_multiplas_academica_passo2.html

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



### Arquivo: presencas\templates\presencas\academicas\historico_presencas_academica.html

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



### Arquivo: presencas\templates\presencas\academicas\importar_presencas_academica.html

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



### Arquivo: presencas\templates\presencas\academicas\listar_observacoes_presenca_academica.html

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



### Arquivo: presencas\templates\presencas\academicas\listar_presencas_academicas.html

html
{% extends 'base.html' %}

{% block title %}Presenças Acadêmicas{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <!-- Cabeçalho com botões -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Presenças Acadêmicas</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <!-- Botão do novo fluxo passo a passo -->
            <a href="{% url 'presencas:registrar_presenca_dados_basicos' %}" class="btn btn-success me-2">
                <i class="fas fa-plus"></i> Registrar Nova Presença (Fluxo Passo a Passo)
            </a>
            <a href="{% url 'presencas:exportar_presencas_academicas' %}" class="btn btn-success me-2">
                <i class="fas fa-file-export"></i> Exportar CSV
            </a>
            <a href="{% url 'presencas:importar_presencas_academicas' %}" class="btn btn-info">
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
            <form id="filtro-presencas" method="get" class="row g-3 mb-4">
                <div class="col-md-3">
                    <label for="id_curso" class="form-label">Curso</label>
                    <select id="id_curso" name="curso" class="form-select">
                        <option value="">Todos</option>
                        {% for curso in cursos %}
                            <option value="{{ curso.id }}" {% if request.GET.curso == curso.id|stringformat:"s" %}selected{% endif %}>{{ curso.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="id_turma" class="form-label">Turma</label>
                    <select id="id_turma" name="turma" class="form-select">
                        <option value="">Todas</option>
                        {% for turma in turmas %}
                            <option value="{{ turma.id }}" {% if request.GET.turma == turma.id|stringformat:"s" %}selected{% endif %}>{{ turma.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="id_atividade" class="form-label">Atividade</label>
                    <select id="id_atividade" name="atividade" class="form-select">
                        <option value="">Todas</option>
                        {% for atividade in atividades %}
                            <option value="{{ atividade.id }}" {% if request.GET.atividade == atividade.id|stringformat:"s" %}selected{% endif %}>{{ atividade.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="id_aluno" class="form-label">Aluno</label>
                    <select id="id_aluno" name="aluno" class="form-select">
                        <option value="">Todos</option>
                        {% for aluno in alunos %}
                            <option value="{{ aluno.id }}" {% if request.GET.aluno == aluno.id|stringformat:"s" %}selected{% endif %}>{{ aluno.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="id_data_inicio" class="form-label">Data início</label>
                    <input type="date" id="id_data_inicio" name="data_inicio" class="form-control" value="{{ request.GET.data_inicio }}">
                </div>
                <div class="col-md-3">
                    <label for="id_data_fim" class="form-label">Data fim</label>
                    <input type="date" id="id_data_fim" name="data_fim" class="form-control" value="{{ request.GET.data_fim }}">
                </div>
                <div class="col-md-3 align-self-end">
                    <button type="submit" class="btn btn-primary w-100">Filtrar</button>
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
                                    <a href="{% url 'presencas:detalhar_presenca_academica' presenca.id %}" class="btn btn-sm btn-info" title="Ver detalhes da presença">
                                        <i class="fas fa-eye"></i> Detalhes
                                    </a>
                                    <a href="{% url 'presencas:editar_presenca_academica' presenca.id %}" class="btn btn-sm btn-warning" title="Editar presença">
                                        <i class="fas fa-edit"></i> Editar
                                    </a>
                                    <a href="{% url 'presencas:excluir_presenca_academica' presenca.id %}" class="btn btn-sm btn-danger" title="Excluir presença">
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
{% endblock content %}

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

        const cursoSelect = document.getElementById('id_curso');
        const turmaSelect = document.getElementById('id_turma');
        const atividadeSelect = document.getElementById('id_atividade');

        cursoSelect.addEventListener('change', function() {
            const cursoId = this.value;
            turmaSelect.innerHTML = '<option value="">Carregando...</option>';
            fetch(`/presencas/registrar-presenca/turmas-por-curso/?curso_id=${cursoId}`)
                .then(response => response.json())
                .then(data => {
                    turmaSelect.innerHTML = '<option value="">Todas</option>';
                    data.forEach(turma => {
                        const opt = document.createElement('option');
                        opt.value = turma.id;
                        opt.textContent = turma.nome;
                        turmaSelect.appendChild(opt);
                    });
                    atividadeSelect.innerHTML = '<option value="">Todas</option>';
                });
        });

        turmaSelect.addEventListener('change', function() {
            const turmaId = this.value;
            atividadeSelect.innerHTML = '<option value="">Carregando...</option>';
            fetch(`/presencas/registrar-presenca/atividades-por-turma/?turma_id=${turmaId}`)
                .then(response => response.json())
                .then(data => {
                    atividadeSelect.innerHTML = '<option value="">Todas</option>';
                    data.forEach(atividade => {
                        const opt = document.createElement('option');
                        opt.value = atividade.id;
                        opt.textContent = atividade.nome;
                        atividadeSelect.appendChild(opt);
                    });
                });
        });
    });
</script>
{% endblock %}




### Arquivo: presencas\templates\presencas\academicas\registrar_presenca_academica.html

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
                    <a href="{% url 'presencas:listar_presencas_academicas' %}" class="btn btn-secondary">
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




### Arquivo: presencas\templates\presencas\academicas\registrar_presenca_em_massa_academica.html

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



### Arquivo: presencas\templates\presencas\academicas\registrar_presencas_multiplas_academica.html

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



### Arquivo: presencas\templates\presencas\academicas\relatorio_presencas_academica.html

html
{% extends 'base.html' %}

{% block title %}Relatório de Presenças{% endblock %}

{% block extra_css %}
<style>
    .stat-card {
        transition: transform 0.3s;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
    }
    
    .chart-container {
        position: relative;
        height: 300px;
        margin-bottom: 20px;
    }
</style>
{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Relatório de Presenças</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-primary me-2">
                <i class="fas fa-list"></i> Lista de Presenças
            </a>
            <button onclick="window.print()" class="btn btn-success">
                <i class="fas fa-print"></i> Imprimir Relatório
            </button>
        </div>
    </div>
    
    <!-- Filtros -->
    <div class="card mb-4 no-print">
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
                
                <div class="col-md-3">
                    <label for="data_inicio" class="form-label">Data Início</label>
                    <input type="date" class="form-control" id="data_inicio" name="data_inicio" value="{{ filtros.data_inicio }}">
                </div>
                
                <div class="col-md-3">
                    <label for="data_fim" class="form-label">Data Fim</label>
                    <input type="date" class="form-control" id="data_fim" name="data_fim" value="{{ filtros.data_fim }}">
                </div>
                
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                    <a href="{% url 'presencas:relatorio_presencas' %}" class="btn btn-secondary">
                        <i class="fas fa-undo"></i> Limpar Filtros
                    </a>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Estatísticas Gerais -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card stat-card bg-primary text-white h-100">
                <div class="card-body text-center">
                    <h5 class="card-title">Total de Registros</h5>
                    <p class="display-4">{{ total }}</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card stat-card bg-success text-white h-100">
                <div class="card-body text-center">
                    <h5 class="card-title">Presenças</h5>
                    <p class="display-4">{{ presentes }}</p>
                    <p>{{ taxa_presenca|floatformat:1 }}%</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card stat-card bg-danger text-white h-100">
                <div class="card-body text-center">
                    <h5 class="card-title">Ausências</h5>
                    <p class="display-4">{{ ausentes }}</p>
                    <p>{{ 100|subtract:taxa_presenca|floatformat:1 }}%</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card stat-card bg-info text-white h-100">
                <div class="card-body text-center">
                    <h5 class="card-title">Média de Presença</h5>
                    <p class="display-4">{{ taxa_presenca|floatformat:1 }}%</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Gráficos -->
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Presença por Aluno (Top 10)</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="alunosChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Presença por Turma</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="turmasChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-12">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Evolução de Presença por Data</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="datasChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Tabelas de Estatísticas -->
    <div class="row">
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Estatísticas por Aluno</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped table-hover">
                            <thead>
                                <tr>
                                    <th>Aluno</th>
                                    <th>Presenças</th>
                                    <th>Ausências</th>
                                    <th>Total</th>
                                    <th>Percentual</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for aluno in alunos_stats %}
                                <tr>
                                    <td>{{ aluno.aluno__nome }}</td>
                                    <td>{{ aluno.presentes }}</td>
                                    <td>{{ aluno.ausentes }}</td>
                                    <td>{{ aluno.total }}</td>
                                    <td>
                                        <div class="progress" style="height: 20px;">
                                            <div class="progress-bar {% if aluno.percentual < 75 %}bg-danger{% elif aluno.percentual < 85 %}bg-warning{% else %}bg-success{% endif %}" 
                                                 role="progressbar" style="width: {{ aluno.percentual }}%;" 
                                                 aria-valuenow="{{ aluno.percentual }}" aria-valuemin="0" aria-valuemax="100">
                                                {{ aluno.percentual|floatformat:1 }}%
                                            </div>
                                        </div>
                                    </td>
                                </tr>
                                {% empty %}
                                <tr>
                                    <td colspan="5" class="text-center">Nenhum dado disponível</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Estatísticas por Turma</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped table-hover">
                            <thead>
                                <tr>
                                    <th>Turma</th>
                                    <th>Presenças</th>
                                    <th>Ausências</th>
                                    <th>Total</th>
                                    <th>Percentual</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for turma in turmas_stats %}
                                <tr>
                                    <td>{{ turma.atividade__turmas__nome }}</td>
                                    <td>{{ turma.presentes }}</td>
                                    <td>{{ turma.ausentes }}</td>
                                    <td>{{ turma.total }}</td>
                                    <td>
                                        <div class="progress" style="height: 20px;">
                                            <div class="progress-bar {% if turma.percentual < 75 %}bg-danger{% elif turma.percentual < 85 %}bg-warning{% else %}bg-success{% endif %}" 
                                                 role="progressbar" style="width: {{ turma.percentual }}%;" 
                                                 aria-valuenow="{{ turma.percentual }}" aria-valuemin="0" aria-valuemax="100">
                                                {{ turma.percentual|floatformat:1 }}%
                                            </div>
                                        </div>
                                    </td>
                                </tr>
                                {% empty %}
                                <tr>
                                    <td colspan="5" class="text-center">Nenhum dado disponível</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-12">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Estatísticas por Data</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped table-hover">
                            <thead>
                                <tr>
                                    <th>Data</th>
                                    <th>Presenças</th>
                                    <th>Ausências</th>
                                    <th>Total</th>
                                    <th>Percentual</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for data in datas_stats %}
                                <tr>
                                    <td>{{ data.data|date:"d/m/Y" }}</td>
                                    <td>{{ data.presentes }}</td>
                                    <td>{{ data.ausentes }}</td>
                                    <td>{{ data.total }}</td>
                                    <td>
                                        <div class="progress" style="height: 20px;">
                                            <div class="progress-bar {% if data.percentual < 75 %}bg-danger{% elif data.percentual < 85 %}bg-warning{% else %}bg-success{% endif %}" 
                                                 role="progressbar" style="width: {{ data.percentual }}%;" 
                                                 aria-valuenow="{{ data.percentual }}" aria-valuemin="0" aria-valuemax="100">
                                                {{ data.percentual|floatformat:1 }}%
                                            </div>
                                        </div>
                                    </td>
                                </tr>
                                {% empty %}
                                <tr>
                                    <td colspan="5" class="text-center">Nenhum dado disponível</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
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
        // Gráfico de presença por aluno
        var ctxAlunos = document.getElementById('alunosChart').getContext('2d');
        new Chart(ctxAlunos, {
            type: 'bar',
            data: {
                labels: {{ alunos_labels|safe }},
                datasets: [{
                    label: 'Percentual de Presença',
                    data: {{ alunos_presenca|safe }},
                    backgroundColor: function(context) {
                        const value = context.dataset.data[context.dataIndex];
                        return value < 75 ? 'rgba(220, 53, 69, 0.7)' : 
                               value < 85 ? 'rgba(255, 193, 7, 0.7)' : 
                               'rgba(40, 167, 69, 0.7)';
                    },
                    borderColor: function(context) {
                        const value = context.dataset.data[context.dataIndex];
                        return value < 75 ? 'rgba(220, 53, 69, 1)' : 
                               value < 85 ? 'rgba(255, 193, 7, 1)' : 
                               'rgba(40, 167, 69, 1)';
                    },
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
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
                    legend: {
                        display: false
                    }
                }
            }
        });
        
        // Gráfico de presença por turma
        var ctxTurmas = document.getElementById('turmasChart').getContext('2d');
        new Chart(ctxTurmas, {
            type: 'bar',
            data: {
                labels: {{ turmas_labels|safe }},
                datasets: [{
                    label: 'Percentual de Presença',
                    data: {{ turmas_presenca|safe }},
                    backgroundColor: function(context) {
                        const value = context.dataset.data[context.dataIndex];
                        return value < 75 ? 'rgba(220, 53, 69, 0.7)' : 
                               value < 85 ? 'rgba(255, 193, 7, 0.7)' : 
                               'rgba(40, 167, 69, 0.7)';
                    },
                    borderColor: function(context) {
                        const value = context.dataset.data[context.dataIndex];
                        return value < 75 ? 'rgba(220, 53, 69, 1)' : 
                               value < 85 ? 'rgba(255, 193, 7, 1)' : 
                               'rgba(40, 167, 69, 1)';
                    },
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
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
                    legend: {
                        display: false
                    }
                }
            }
        });
        
        // Gráfico de evolução de presença por data
        var ctxDatas = document.getElementById('datasChart').getContext('2d');
        new Chart(ctxDatas, {
            type: 'line',
            data: {
                labels: {{ datas_labels|safe }},
                datasets: [{
                    label: 'Percentual de Presença',
                    data: {{ datas_presenca|safe }},
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    tension: 0.1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
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

<style type="text/css" media="print">
    .no-print, .no-print * {
        display: none !important;
    }
    
    .container-fluid {
        width: 100%;
        padding: 0;
    }
    
    .card {
        border: 1px solid #ddd;
        margin-bottom: 20px;
        break-inside: avoid;
    }
    
    .card-header {
        background-color: #f8f9fa !important;
        color: #000 !important;
        border-bottom: 1px solid #ddd;
    }
    
    .chart-container {
        height: 250px;
    }
    
    @page {
        size: landscape;
        margin: 1cm;
    }
</style>
{% endblock %}



### Arquivo: presencas\templates\presencas\registrar_presenca_alunos.html

html
<!-- filepath: presencas/templates/presencas/registrar_presenca_alunos.html -->
{% extends 'base.html' %}
{% block content %}
<div class="container mt-4">
    <h2>Registrar Presença - Marque os Alunos Presentes</h2>
    <form id="form-alunos-presenca" method="post" autocomplete="off">
        {% csrf_token %}
        <div class="mb-3">
            {{ form.alunos_presentes }}
        </div>
        <button type="submit" class="btn btn-primary">Confirmar e Avançar</button>
    </form>
    <div id="form-errors" class="alert alert-danger mt-3 d-none"></div>
    <div id="ajax-error" class="alert alert-danger mt-3 d-none"></div>
</div>
{% endblock %}

{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-alunos-presenca');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        fetch("{% url 'presencas:registrar_presenca_alunos_ajax' %}", {
            method: "POST",
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url;
            } else if (data.errors) {
                let errorDiv = document.getElementById('form-errors');
                errorDiv.innerHTML = '';
                for (const [field, errors] of Object.entries(data.errors)) {
                    errorDiv.innerHTML += `<strong>${field}:</strong> ${errors.join('<br>')}<br>`;
                }
                errorDiv.classList.remove('d-none');
            } else if (data.erro) {
                let ajaxError = document.getElementById('ajax-error');
                ajaxError.textContent = data.erro;
                ajaxError.classList.remove('d-none');
            }
        });
    });
});
</script>
{% endblock %}



### Arquivo: presencas\templates\presencas\registrar_presenca_confirmar.html

html
<!-- filepath: presencas/templates/presencas/registrar_presenca_confirmar.html -->
{% extends 'base.html' %}
{% block content %}
<div class="container mt-4">
    <h2>Confirmar Registro de Presença</h2>
    <div class="mb-3">
        <strong>Turma:</strong> {{ turma }}<br>
        <strong>Ano:</strong> {{ ano }}<br>
        <strong>Mês:</strong> {{ mes }}<br>
        <strong>Atividade:</strong> {{ atividade }}<br>
        <strong>Alunos Presentes:</strong>
        <ul>
            {% for aluno in alunos_presentes %}
                <li>{{ aluno }}</li>
            {% empty %}
                <li>Nenhum aluno selecionado.</li>
            {% endfor %}
        </ul>
    </div>
    <form id="form-confirmar-presenca" method="post">
        {% csrf_token %}
        <button type="submit" class="btn btn-success">Confirmar e Salvar</button>
    </form>
    <div id="form-errors" class="alert alert-danger mt-3 d-none"></div>
</div>
{% endblock %}

{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-confirmar-presenca');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        fetch("{% url 'presencas:registrar_presenca_confirmar_ajax' %}", {
            method: "POST",
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                let errorDiv = document.getElementById('form-errors');
                errorDiv.innerHTML = 'Erro ao salvar presença.';
                errorDiv.classList.remove('d-none');
            }
        });
    });
});
</script>
{% endblock %}



### Arquivo: presencas\templates\presencas\registrar_presenca_dados_basicos.html

html
<!-- filepath: presencas/templates/presencas/registrar_presenca_dados_basicos.html -->
{% extends 'base.html' %}
{% load i18n %}
{% load static %}
{% block content %}
<div class="container mt-4">
    <h2>{% trans "Registrar Presença - Dados Básicos" %}</h2>
    <form id="form-dados-basicos" method="post" autocomplete="off" action="{% url 'presencas:registrar_presenca_dados_basicos_ajax' %}">
        {% csrf_token %}
        <div class="mb-3">
            <label for="id_curso" class="form-label">{% trans "Curso" %}</label>
            {{ form.curso }}
        </div>
        <div class="mb-3">
            <label for="id_turma" class="form-label">{% trans "Turma" %}</label>
            {{ form.turma }}
            <span id="loading-turmas" class="ms-2 text-primary d-none">{% trans "Carregando turmas..." %}</span>
        </div>
        <div class="mb-3">
            <label class="form-label">{% trans "Selecione o Ano/Mês" %}</label>
            <div id="calendario-mes-ano" class="d-flex align-items-center">
                <button type="button" id="btn-prev" class="btn btn-outline-secondary btn-sm me-2" aria-label="{% trans 'Retroceder mês' %}">&lt;</button>
                <span id="mes-ano-atual" style="min-width:120px; text-align:center;"></span>
                <button type="button" id="btn-next" class="btn btn-outline-secondary btn-sm ms-2" aria-label="{% trans 'Avançar mês' %}">&gt;</button>
                <span id="loading-calendario" class="ms-2 text-primary d-none">{% trans "Carregando calendário..." %}</span>
            </div>
            <input type="hidden" id="id_ano" name="ano" value="{{ form.initial.ano|default:ano_corrente }}">
            <input type="hidden" id="id_mes" name="mes" value="{{ form.initial.mes|default:mes_corrente }}">
        </div>
        <button type="submit" class="btn btn-primary">{% trans "Confirmar e Avançar" %}</button>
    </form>
    <div id="form-errors" class="alert alert-danger mt-3 d-none"></div>
    <!-- Bloco para exibir mensagens de erro do AJAX -->
    <div id="mensagem-erro-ajax" class="alert alert-danger d-none"></div>
    <div id="mensagem-sucesso-ajax" class="alert alert-success d-none"></div>
    <!-- Comentário: O bloco acima exibe erros de requisições AJAX, como falha ao carregar turmas ou calendário. -->
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/presencas/registrar_presenca_dados_basicos.js' %}"></script>
{% endblock %}



### Arquivo: presencas\templates\presencas\registrar_presenca_dias_atividades.html

html
{% extends "base.html" %}
{% load static %}
{% load presenca_extras %}

{% block content %}
<h2>Designação dos Dias das Atividades</h2>

<style>
    .atividades-container {
        display: flex;
        overflow-x: auto;
        gap: 24px;
        padding-bottom: 16px;
    }
    .atividade-quadro {
        min-width: 260px;
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 16px;
        background: #fafafa;
        flex-shrink: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .minicalendario {
        display: flex;
        flex-direction: column;
        gap: 4px;
        margin-bottom: 8px;
        justify-content: flex-start;
        width: 100%;
    }
    .minicalendario .dia-linha {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 2px;
    }
    .minicalendario label {
        width: 32px;
        text-align: center;
        cursor: pointer;
        margin-bottom: 0;
    }
    .minicalendario input[type="text"] {
        flex: 1;
        min-width: 0;
        max-width: 140px;
        font-size: 0.95em;
    }
    .matriz-confirmada {
        margin-top: 12px;
        border-top: 1px solid #ddd;
        padding-top: 8px;
        font-size: 0.95em;
    }
    .obs-curta {
        display: inline;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 180px;
        vertical-align: bottom;
    }
</style>

<form id="form-presenca" method="post">
    {% csrf_token %}
    <div id="mensagem-ajax" class="alert d-none" role="alert"></div>
    <div id="mensagem-erro-ajax" class="alert alert-danger d-none"></div>
    <div class="atividades-container">
        {% for atividade in atividades %}
        <div class="atividade-quadro" id="quadro-{{ atividade.id }}">
            <strong>
                {{ atividade.nome }} ({{ atividade.qtd_ativ_mes }})
            </strong>
            <div>
                <small>Mês: {{ mes }}/{{ ano }}</small>
            </div>
            <div class="minicalendario">
                {% for dia in dias_do_mes %}
                <div class="dia-linha">
                    <label>
                        <input type="checkbox"
                            class="dia-checkbox"
                            name="presenca_{{ atividade.id }}"
                            value="{{ dia }}"
                            data-atividade="{{ atividade.id }}"
                            data-dia="{{ dia }}"
                            {% if dia in presencas|get_item:atividade.id %}checked{% endif %}>
                        {{ dia }}
                    </label>
                    <input type="text"
                        name="obs_{{ atividade.id }}_{{ dia }}"
                        maxlength="200"
                        class="form-control obs-dia"
                        placeholder="Obs. deste dia"
                        value="{% if presencas_obs and presencas_obs|get_item:atividade.id and presencas_obs|get_item:atividade.id|get_item:dia %}{{ presencas_obs|get_item:atividade.id|get_item:dia }}{% endif %}">
                </div>
                {% endfor %}
            </div>
            <button type="button"
                class="btn btn-success btn-confirmar"
                data-atividade="{{ atividade.id }}"
                data-qtd="{{ atividade.qtd_ativ_mes }}">
                Confirmar
            </button>
            <div class="matriz-confirmada" id="matriz-{{ atividade.id }}" style="display:none;">
                <!-- Lista dos dias e observações confirmadas aparecerá aqui -->
            </div>
        </div>
        {% endfor %}
    </div>
    <button type="submit" class="btn btn-primary">Salvar e avançar</button>
</form>

<script src="{% static 'js/presencas/registrar_presenca_dias_atividades.js' %}"></script>
{% endblock %}



### Arquivo: presencas\templates\presencas\registrar_presenca_totais_atividades.html

html
<!-- filepath: presencas/templates/presencas/registrar_presenca_totais_atividades.html -->
{% extends 'base.html' %}
{% block content %}
<div class="container mt-4">
    <h2>Registrar Presença - Totais de Atividades</h2>
    <p>Informe a quantidade de dias em que cada atividade ocorreu neste mês. Caso alguma atividade não tenha sido realizada, informe zero. As atividades não informadas não poderão sofrer alterações na seção seguinte.</p>
    {% if totais_registrados %}
        <div class="alert alert-info">
            <strong>Totais já registrados neste mês:</strong>
            <ul>
                {% for total in totais_registrados %}
                    <li>{{ total.atividade.nome }}: {{ total.qtd_ativ_mes }} dia(s)</li>
                {% endfor %}
            </ul>
        </div>
    {% endif %}
    {% if curso and turma and ano and mes %}
    <div class="alert alert-info d-flex justify-content-between align-items-center">
        <div>
            <strong>Seleção atual:</strong>
            Curso: {{ curso.nome }} |
            Turma: {{ turma.nome }} |
            Ano: {{ ano }} |
            Mês: {{ mes }}
        </div>
        <a href="{% url 'presencas:registrar_presenca_dados_basicos' %}" class="btn btn-outline-primary btn-sm">
            <i class="fas fa-arrow-left"></i> Alterar seleção
        </a>
    </div>
    {% endif %}
    <div id="form-errors" class="alert alert-danger d-none"></div>
    <div id="mensagem-erro-ajax" class="alert alert-danger d-none"></div>
    <form id="form-totais-atividades" method="post" autocomplete="off">
        {% csrf_token %}
        {% if form.non_field_errors %}
            <div class="alert alert-danger">
                {{ form.non_field_errors }}
            </div>
        {% endif %}
        <div class="row">
            <div class="col-md-8 offset-md-2">
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th>Atividade</th>
                            <th>Qtd. Dias</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for field in form %}
                            <tr>
                                <td>{{ field.label }}</td>
                                <td>
                                    {{ field }}
                                    {% if field.errors %}
                                        <div class="text-danger small">{{ field.errors|join:", " }}</div>
                                    {% endif %}
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <button type="submit" class="btn btn-primary">Confirmar e Avançar</button>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-totais-atividades');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        // Limpa mensagens anteriores
        document.getElementById('form-errors').classList.add('d-none');
        document.getElementById('mensagem-erro-ajax').classList.add('d-none');
        const formData = new FormData(form);
        fetch("{% url 'presencas:registrar_presenca_totais_atividades_ajax' %}", {
            method: "POST",
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url;
            } else if (data.errors) {
                let errorDiv = document.getElementById('form-errors');
                errorDiv.innerHTML = '';
                for (const [field, errors] of Object.entries(data.errors)) {
                    errorDiv.innerHTML += `<strong>${field}:</strong> ${errors.join('<br>')}<br>`;
                }
                errorDiv.classList.remove('d-none');
            } else if (data.erro || (data.errors && data.errors.atividade)) {
                let ajaxError = document.getElementById('mensagem-erro-ajax');
                ajaxError.textContent = data.erro || (data.errors && data.errors.atividade ? data.errors.atividade[0] : '');
                ajaxError.classList.remove('d-none');
            }
        });
    });
});
</script>
{% endblock %}



### Arquivo: presencas\templates\presencas\ritualisticas\detalhar_presenca_ritualistica.html

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



### Arquivo: presencas\templates\presencas\ritualisticas\editar_presenca_ritualistica.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Presença</h1>
    
    <div class="card mb-4">
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                {% for field in form %}
                <div class="mb-3">
                    <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                    {{ field }}
                    {% if field.errors %}
                    <div class="text-danger">
                        {% for error in field.errors %}
                        <small>{{ error }}</small>
                        {% endfor %}
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
                
                <div class="mt-4">
                    <button type="submit" class="btn btn-primary">Salvar Alterações</button>
                    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}



'''