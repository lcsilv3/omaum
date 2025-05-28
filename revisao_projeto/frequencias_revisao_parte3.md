'''
# Revisão da Funcionalidade: frequencias

## Arquivos forms.py:


### Arquivo: frequencias\templates\frequencias\estatisticas_frequencia.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Estatísticas de Frequência</h1>
   
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
   
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-3">
                    <label for="aluno" class="form-label">Aluno</label>
                    <select name="aluno" id="aluno" class="form-select">
                        <option value="">Todos</option>
                        {% for aluno in alunos %}
                            <option value="{{ aluno.id }}" {% if aluno_id == aluno.id|stringformat:"s" %}selected{% endif %}>{{ aluno.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="turma" class="form-label">Turma</label>
                    <select name="turma" id="turma" class="form-select">
                        <option value="">Todas</option>
                        {% for turma in turmas %}
                            <option value="{{ turma.id }}" {% if turma_id == turma.id|stringformat:"s" %}selected{% endif %}>{{ turma.id }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="data_inicio" class="form-label">Data Início</label>
                    <input type="date" class="form-control" id="data_inicio" name="data_inicio" value="{{ data_inicio }}">
                </div>
                <div class="col-md-3">
                    <label for="data_fim" class="form-label">Data Fim</label>
                    <input type="date" class="form-control" id="data_fim" name="data_fim" value="{{ data_fim }}">
                </div>
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">Filtrar</button>
                    <a href="{% url 'estatisticas_frequencia' %}" class="btn btn-secondary">Limpar Filtros</a>
                </div>
            </form>
        </div>
    </div>
   
    <!-- Resumo Estatístico -->
    <div class="row">
        <div class="col-md-4">
            <div class="card text-white bg-primary mb-4">
                <div class="card-header">Total de Registros</div>
                <div class="card-body">
                    <h5 class="card-title">{{ total }}</h5>
                    <p class="card-text">registros de frequência</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card text-white bg-success mb-4">
                <div class="card-header">Presenças</div>
                <div class="card-body">
                    <h5 class="card-title">{{ presentes }}</h5>
                    <p class="card-text">alunos presentes ({{ taxa_presenca|floatformat:2 }}%)</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card text-white bg-danger mb-4">
                <div class="card-header">Ausências</div>
                <div class="card-body">
                    <h5 class="card-title">{{ ausentes }}</h5>
                    <p class="card-text">alunos ausentes ({{ 100|sub:taxa_presenca|floatformat:2 }}%)</p>
                </div>
            </div>
        </div>
    </div>
   
    <!-- Gráfico (pode ser implementado com Chart.js) -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Gráfico de Frequência</h5>
        </div>
        <div class="card-body">
            <canvas id="graficoFrequencia" width="400" height="200"></canvas>
        </div>
    </div>
   
    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
        <a href="{% url 'listar_frequencias' %}" class="btn btn-secondary">Voltar para Lista</a>
    </div>
</div>

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        var ctx = document.getElementById('graficoFrequencia').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Presentes', 'Ausentes'],
                datasets: [{
                    label: 'Frequência',
                    data: [{{ presentes }}, {{ ausentes }}],
                    backgroundColor: [
                        'rgba(40, 167, 69, 0.8)',
                        'rgba(220, 53, 69, 0.8)'
                    ],
                    borderColor: [
                        'rgba(40, 167, 69, 1)',
                        'rgba(220, 53, 69, 1)'
                    ],
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
                        text: 'Distribuição de Frequência'
                    }
                }
            }
        });
    });
</script>
{% endblock %}
{% endblock %}




### Arquivo: frequencias\templates\frequencias\excluir_frequencia.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Registro de Frequência</h1>
  
    <div class="alert alert-danger">
      <p>Tem certeza que deseja excluir o registro de frequência de <strong>{{ frequencia.aluno.nome }}</strong> na atividade <strong>{{ frequencia.atividade.nome }}</strong> do dia <strong>{{ frequencia.data|date:"d/m/Y" }}</strong>?</p>
    </div>
  
    <form method="post">
      {% csrf_token %}
      <button type="submit" class="btn btn-danger">Sim, excluir</button>
      <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




### Arquivo: frequencias\templates\frequencias\excluir_frequencia_mensal.html

html
{% extends 'base.html' %}

{% block title %}Excluir Frequência Mensal{% endblock %}

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
                        Você está prestes a excluir a seguinte frequência mensal:
                    </div>
                    
                    <div class="card mb-3">
                        <div class="card-body">
                            <p><strong>Turma:</strong> {{ frequencia.turma.nome }}</p>
                            <p><strong>Período:</strong> {{ frequencia.get_mes_display }}/{{ frequencia.ano }}</p>
                            <p><strong>Percentual Mínimo:</strong> {{ frequencia.percentual_minimo }}%</p>
                            <p><strong>Alunos em Carência:</strong> {{ frequencia.carencias.count }}</p>
                        </div>
                    </div>
                    
                    <p class="text-danger">Esta ação não pode ser desfeita e também excluirá todas as carências associadas. Deseja continuar?</p>
                    
                    <form method="post">
                        {% csrf_token %}
                        <div class="d-flex justify-content-between">
                            <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">
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



### Arquivo: frequencias\templates\frequencias\filtro_painel_frequencias.html

html
{% extends 'base.html' %}

{% block title %}Painel de Frequências - Filtros{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Painel de Frequências</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Selecione a Turma e o Período</h5>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="row mb-3">
                    <div class="col-md-12">
                        <label for="{{ form.turma.id_for_label }}" class="form-label">{{ form.turma.label }}</label>
                        {{ form.turma }}
                        {% if form.turma.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.turma.errors }}
                            </div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-md-3">
                        <label for="{{ form.mes_inicio.id_for_label }}" class="form-label">{{ form.mes_inicio.label }}</label>
                        {{ form.mes_inicio }}
                        {% if form.mes_inicio.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.mes_inicio.errors }}
                            </div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-3">
                        <label for="{{ form.ano_inicio.id_for_label }}" class="form-label">{{ form.ano_inicio.label }}</label>
                        {{ form.ano_inicio }}
                        {% if form.ano_inicio.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.ano_inicio.errors }}
                            </div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-3">
                        <label for="{{ form.mes_fim.id_for_label }}" class="form-label">{{ form.mes_fim.label }}</label>
                        {{ form.mes_fim }}
                        {% if form.mes_fim.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.mes_fim.errors }}
                            </div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-3">
                        <label for="{{ form.ano_fim.id_for_label }}" class="form-label">{{ form.ano_fim.label }}</label>
                        {{ form.ano_fim }}
                        {% if form.ano_fim.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.ano_fim.errors }}
                            </div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="text-end">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-search"></i> Gerar Relatório
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
        // Validar que a data final é posterior à data inicial
        const form = document.querySelector('form');
        form.addEventListener('submit', function(e) {
            const mesInicio = parseInt(document.getElementById('id_mes_inicio').value);
            const anoInicio = parseInt(document.getElementById('id_ano_inicio').value);
            const mesFim = parseInt(document.getElementById('id_mes_fim').value);
            const anoFim = parseInt(document.getElementById('id_ano_fim').value);
            
            const dataInicio = new Date(anoInicio, mesInicio - 1, 1);
            const dataFim = new Date(anoFim, mesFim - 1, 1);
            
            if (dataFim < dataInicio) {
                e.preventDefault();
                alert('A data final deve ser posterior à data inicial.');
            }
        });
    });
</script>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\formulario_frequencia_mensal.html

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
                            <label for="{{ form.turma.id_for_label }}" class="form-label">{{ form.turma.label }}</label>
                            {{ form.turma }}
                            {% if form.turma.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.turma.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.turma.help_text %}
                            <div class="form-text">{{ form.turma.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="{{ form.mes.id_for_label }}" class="form-label">{{ form.mes.label }}</label>
                                    {{ form.mes }}
                                    {% if form.mes.errors %}
                                    <div class="invalid-feedback d-block">
                                        {% for error in form.mes.errors %}
                                        {{ error }}
                                        {% endfor %}
                                    </div>
                                    {% endif %}
                                    {% if form.mes.help_text %}
                                    <div class="form-text">{{ form.mes.help_text }}</div>
                                    {% endif %}
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="{{ form.ano.id_for_label }}" class="form-label">{{ form.ano.label }}</label>
                                    {{ form.ano }}
                                    {% if form.ano.errors %}
                                    <div class="invalid-feedback d-block">
                                        {% for error in form.ano.errors %}
                                        {{ error }}
                                        {% endfor %}
                                    </div>
                                    {% endif %}
                                    {% if form.ano.help_text %}
                                    <div class="form-text">{{ form.ano.help_text }}</div>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.percentual_minimo.id_for_label }}" class="form-label">
                                {{ form.percentual_minimo.label }}
                            </label>
                            <div class="input-group">
                                {{ form.percentual_minimo }}
                                <span class="input-group-text">%</span>
                            </div>
                            {% if form.percentual_minimo.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.percentual_minimo.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.percentual_minimo.help_text %}
                            <div class="form-text">{{ form.percentual_minimo.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="d-flex justify-content-between mt-4">
                            <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">
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
    });
</script>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\gerar_frequencia_mensal.html

html
{% extends 'base.html' %}

{% block title %}Gerar Frequência Mensal{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Gerar Frequência Mensal</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Selecione a Turma e o Período</h5>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="row mb-3">
                    <div class="col-md-12">
                        <label for="{{ form.turma.id_for_label }}" class="form-label">{{ form.turma.label }}</label>
                        {{ form.turma }}
                        {% if form.turma.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.turma.errors }}
                            </div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-md-4">
                        <label for="{{ form.mes.id_for_label }}" class="form-label">{{ form.mes.label }}</label>
                        {{ form.mes }}
                        {% if form.mes.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.mes.errors }}
                            </div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-4">
                        <label for="{{ form.ano.id_for_label }}" class="form-label">{{ form.ano.label }}</label>
                        {{ form.ano }}
                        {% if form.ano.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.ano.errors }}
                            </div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-4">
                        <label for="{{ form.percentual_minimo.id_for_label }}" class="form-label">{{ form.percentual_minimo.label }}</label>
                        {{ form.percentual_minimo }}
                        {% if form.percentual_minimo.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.percentual_minimo.errors }}
                            </div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> Esta operação irá gerar ou atualizar o registro de frequência mensal para a turma e período selecionados. Todas as presenças registradas no período serão consideradas no cálculo.
                </div>
                
                <div class="text-end">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-calculator"></i> Gerar Frequência
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\gerenciar_carencias.html

html
{% extends 'base.html' %}

{% block title %}Gerenciar Carências{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Gerenciar Carências</h1>
        <div>
            <a href="{% url 'frequencias:detalhar_frequencia_mensal' frequencia.id %}" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
        </div>
    </div>
    
    <!-- Informações da frequência -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Informações da Frequência</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-4">
                    <p><strong>Turma:</strong> {{ frequencia.turma.nome }}</p>
                </div>
                <div class="col-md-4">
                    <p><strong>Mês/Ano:</strong> {{ frequencia.get_mes_display }}/{{ frequencia.ano }}</p>
                </div>
                <div class="col-md-4">
                    <p><strong>Percentual Mínimo:</strong> {{ frequencia.percentual_minimo }}%</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Lista de alunos com carência -->
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">Alunos com Carência</h5>
        </div>
        <div class="card-body">
            {% if carencias %}
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead class="table-light">
                            <tr>
                                <th>Aluno</th>
                                <th class="text-center">Presenças</th>
                                <th class="text-center">Percentual</th>
                                <th class="text-center">Carências</th>
                                <th class="text-center">Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for carencia in carencias %}
                                <tr>
                                    <td>
                                        <div class="d-flex align-items-center">
                                            {% if carencia.aluno.foto %}
                                                <img src="{{ carencia.aluno.foto.url }}" alt="Foto de {{ carencia.aluno.nome }}" 
                                                    class="rounded-circle me-2" width="40" height="40" style="object-fit: cover;">
                                            {% else %}
                                                <div class="rounded-circle bg-secondary d-flex align-items-center justify-content-center me-2" 
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
                                    <td class="text-center">
                                        {{ carencia.total_presencas }}/{{ carencia.total_atividades }}
                                    </td>
                                    <td class="text-center">
                                        {{ carencia.percentual_presenca|floatformat:1 }}%
                                    </td>
                                    <td class="text-center">
                                        <span class="badge bg-danger">{{ carencia.numero_carencias }}</span>
                                    </td>
                                    <td class="text-center">
                                        <form method="post" action="{% url 'frequencias:atualizar_carencia' carencia.id %}" class="d-inline">
                                            {% csrf_token %}
                                            <input type="hidden" name="liberado" value="true">
                                            <button type="submit" class="btn btn-success btn-sm">
                                                <i class="fas fa-check"></i> Liberar
                                            </button>
                                        </form>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="alert alert-success">
                    <i class="fas fa-check-circle me-2"></i> Não há alunos com carência nesta frequência.
                </div>
            {% endif %}
        </div>
        <div class="card-footer">
            <a href="{% url 'frequencias:detalhar_frequencia_mensal' frequencia.id %}" class="btn btn-secondary">
                Voltar
            </a>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\historico_frequencia.html

html
{% extends 'base.html' %}

{% block title %}Histórico de Frequência - {{ aluno.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Padronizar botões de ação -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Histórico de Frequência</h1>
        <div>
            <a href="{% url 'alunos:detalhar_aluno' aluno.cpf %}" class="btn btn-secondary me-2">
                <i class="fas fa-user"></i> Perfil do Aluno
            </a>
            <a href="{% url 'frequencias:exportar_historico' aluno.cpf %}" class="btn btn-success">
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
                
                <div class="col-md-4">
                    <label for="turma" class="form-label">Turma</label>
                    <select class="form-select" id="turma" name="turma">
                        <option value="">Todas as turmas</option>
                        {% for turma in turmas %}
                        <option value="{{ turma.id }}" {% if filtros.turma == turma.id|stringformat:"s" %}selected{% endif %}>
                            {{ turma.nome }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="col-md-4">
                    <label for="periodo" class="form-label">Período</label>
                    <select class="form-select" id="periodo" name="periodo">
                        <option value="">Todos os períodos</option>
                        {% for ano in anos %}
                            <optgroup label="{{ ano }}">
                                {% for mes in meses %}
                                <option value="{{ ano }}-{{ mes.0 }}" 
                                        {% if filtros.periodo == ano|stringformat:"s"|add:"-"|add:mes.0|stringformat:"s" %}selected{% endif %}>
                                    {{ mes.1 }}/{{ ano }}
                                </option>
                                {% endfor %}
                            </optgroup>
                        {% endfor %}
                    </select>
                </div>
                
                <!-- Padronizar botões de filtro -->
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                    <a href="{% url 'frequencias:historico_frequencia' aluno.cpf %}" class="btn btn-secondary">
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
                <div class="col-md-6">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Média Geral de Frequência</h5>
                            <p class="card-text display-4">{{ media_geral|floatformat:1 }}%</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Total de Carências</h5>
                            <p class="card-text display-4">{{ carencias.count }}</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="mt-4">
                <canvas id="grafico-evolucao"></canvas>
            </div>
        </div>
    </div>
    
    <!-- Registros de frequência -->
    <div class="card">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Registros de Frequência</h5>
        </div>
        <div class="card-body">
            {% if registros %}
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Período</th>
                            <th>Curso</th>
                            <th>Turma</th>
                            <th>Percentual de Presença</th>
                            <th>Status</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for registro in registros %}
                        <tr>
                            <td>{{ registro.frequencia_mensal.get_mes_display }}/{{ registro.frequencia_mensal.ano }}</td>
                            <td>{{ registro.frequencia_mensal.turma.curso.nome }}</td>
                            <td>{{ registro.frequencia_mensal.turma.nome }}</td>
                            <td>
                                <div class="progress" style="height: 20px;">
                                    <div class="progress-bar {% if registro.percentual_presenca < 75 %}bg-danger{% else %}bg-success{% endif %}" role="progressbar" 
                                         style="width: {{ registro.percentual_presenca }}%;" 
                                         aria-valuenow="{{ registro.percentual_presenca }}" 
                                         aria-valuemin="0" aria-valuemax="100">
                                        {{ registro.percentual_presenca }}%
                                    </div>
                                </div>
                            </td>
                            <td>
                                {% if registro.percentual_presenca < 75 %}
                                    {% if registro.liberado %}
                                        <span class="badge bg-success">Liberado</span>
                                    {% else %}
                                        {% if registro.status == 'PENDENTE' %}
                                            <span class="badge bg-danger">Carência Pendente</span>
                                        {% elif registro.status == 'EM_ACOMPANHAMENTO' %}
                                            <span class="badge bg-warning text-dark">Em Acompanhamento</span>
                                        {% elif registro.status == 'RESOLVIDO' %}
                                            <span class="badge bg-success">Resolvido</span>
                                        {% else %}
                                            <span class="badge bg-danger">Carência</span>
                                        {% endif %}
                                    {% endif %}
                                {% else %}
                                    <span class="badge bg-success">Regular</span>
                                {% endif %}
                            </td>
                            <td>
                                <div class="btn-group">
                                    <a href="{% url 'frequencias:detalhar_frequencia_mensal' registro.frequencia_mensal.id %}" 
                                       class="btn btn-sm btn-info" title="Ver frequência mensal">
                                        <i class="fas fa-calendar-alt"></i>
                                    </a>
                                    {% if registro.percentual_presenca < 75 and not registro.liberado %}
                                        <a href="{% url 'frequencias:detalhar_carencia' registro.id %}" 
                                           class="btn btn-sm btn-warning" title="Ver carência">
                                            <i class="fas fa-exclamation-triangle"></i>
                                        </a>
                                    {% endif %}
                                    <a href="{% url 'turmas:detalhar_turma' registro.frequencia_mensal.turma.id %}" 
                                       class="btn btn-sm btn-primary" title="Ver turma">
                                        <i class="fas fa-users"></i>
                                    </a>
                                </div>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="9" class="text-center py-3">
                                <p class="mb-0">Nenhum registro de frequência encontrado com os filtros selecionados.</p>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer d-flex justify-content-between align-items-center">
            <div>
                <p class="mb-0">Exibindo {{ registros|length }} de {{ total_registros }} registros</p>
            </div>
            
            {% if registros.has_other_pages %}
            <nav aria-label="Paginação" class="mt-4">
                <ul class="pagination justify-content-center">
                    {% if registros.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ registros.previous_page_number }}{% if filtros.curso %}&curso={{ filtros.curso }}{% endif %}{% if filtros.turma %}&turma={{ filtros.turma }}{% endif %}{% if filtros.periodo %}&periodo={{ filtros.periodo }}{% endif %}">Anterior</a>
                    </li>
                    {% else %}
                    <li class="page-item disabled">
                        <span class="page-link">Anterior</span>
                    </li>
                    {% endif %}
                    
                    {% for num in registros.paginator.page_range %}
                    {% if registros.number == num %}
                    <li class="page-item active">
                        <span class="page-link">{{ num }}</span>
                    </li>
                    {% else %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ num }}{% if filtros.curso %}&curso={{ filtros.curso }}{% endif %}{% if filtros.turma %}&turma={{ filtros.turma }}{% endif %}{% if filtros.periodo %}&periodo={{ filtros.periodo }}{% endif %}">{{ num }}</a>
                    </li>
                    {% endif %}
                    {% endfor %}
                    
                    {% if registros.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ registros.next_page_number }}{% if filtros.curso %}&curso={{ filtros.curso }}{% endif %}{% if filtros.turma %}&turma={{ filtros.turma }}{% endif %}{% if filtros.periodo %}&periodo={{ filtros.periodo }}{% endif %}">Próxima</a>
                    </li>
                    {% else %}
                    <li class="page-item disabled">
                        <span class="page-link">Próxima</span>
                    </li>
                    {% endif %}
                </ul>
            </nav>
            {% endif %}
            
            {% else %}
            <div class="alert alert-info">
                <i class="fas fa-info-circle me-2"></i>
                Não há registros de frequência para este aluno com os filtros selecionados.
            </div>
            {% endif %}
        </div>
    </div>
    
    <!-- Carências -->
    <div class="card mb-4">
        <div class="card-header bg-danger text-white">
            <h5 class="mb-0">Histórico de Carências</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Curso</th>
                            <th>Turma</th>
                            <th>Período</th>
                            <th>% Presença</th>
                            <th>Data Identificação</th>
                            <th>Status</th>
                            <th>Notificação</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for carencia in carencias %}
                        <tr>
                            <td>{{ carencia.frequencia_mensal.turma.curso.nome }}</td>
                            <td>{{ carencia.frequencia_mensal.turma.nome }}</td>
                            <td>{{ carencia.frequencia_mensal.get_mes_display }}/{{ carencia.frequencia_mensal.ano }}</td>
                            <td>
                                <div class="progress" style="height: 20px;">
                                    <div class="progress-bar bg-danger" role="progressbar" 
                                         style="width: {{ carencia.percentual_presenca }}%;" 
                                         aria-valuenow="{{ carencia.percentual_presenca }}" aria-valuemin="0" aria-valuemax="100">
                                        {{ carencia.percentual_presenca|floatformat:1 }}%
                                    </div>
                                </div>
                            </td>
                            <td>{{ carencia.data_identificacao|date:"d/m/Y" }}</td>
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
                                    <span class="badge bg-secondary">Não Enviada</span>
                                    {% elif carencia.notificacao.status == 'ENVIADA' %}
                                    <span class="badge bg-info">Enviada</span>
                                    {% elif carencia.notificacao.status == 'LIDA' %}
                                    <span class="badge bg-primary">Lida</span>
                                    {% elif carencia.notificacao.status == 'RESPONDIDA' %}
                                    <span class="badge bg-success">Respondida</span>
                                    {% endif %}
                                {% else %}
                                <span class="badge bg-secondary">Não Criada</span>
                                {% endif %}
                            </td>
                            <td>
                                <div class="btn-group">
                                    <a href="{% url 'frequencias:detalhar_carencia' carencia.id %}" class="btn btn-sm btn-info">
                                        <i class="fas fa-eye"></i>
                                    </a>
                                    {% if carencia.notificacao %}
                                    <a href="{% url 'frequencias:detalhar_notificacao' carencia.notificacao.id %}" class="btn btn-sm btn-primary">
                                        <i class="fas fa-envelope"></i>
                                    </a>
                                    {% endif %}
                                </div>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="8" class="text-center py-3">
                                <p class="mb-0">Nenhuma carência encontrada com os filtros selecionados.</p>
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
        // Gráfico de evolução de frequência
        const ctxEvolucao = document.getElementById('grafico-evolucao').getContext('2d');
        new Chart(ctxEvolucao, {
            type: 'line',
            data: {
                labels: {{ periodos_labels|safe }},
                datasets: [{
                    label: 'Percentual de Presença',
                    data: {{ percentuais_presenca|safe }},
                    backgroundColor: 'rgba(40, 167, 69, 0.2)',
                    borderColor: 'rgba(40, 167, 69, 1)',
                    borderWidth: 2,
                    tension: 0.1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.raw.toFixed(1) + '%';
                            }
                        }
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



### Arquivo: frequencias\templates\frequencias\importar_frequencias.html

html
{% extends 'base.html' %}

{% block title %}Importar Frequências{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Importar Frequências Mensais</h1>
    
    <div class="card">
        <div class="card-body">
            <p class="mb-3">Faça upload de um arquivo CSV contendo os dados das frequências mensais.</p>
            
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                <div class="mb-3">
                    <label for="csv_file" class="form-label">Arquivo CSV</label>
                    <input type="file" name="csv_file" id="csv_file" class="form-control" accept=".csv" required>
                    <div class="form-text">O arquivo deve ter cabeçalhos: Turma, Mês, Ano, Percentual Mínimo</div>
                </div>
                
                <div class="d-flex">
                    <button type="submit" class="btn btn-primary me-2">Importar</button>
                    <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
    
    <div class="mt-3">
        <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-link">Voltar para a lista de frequências</a>
    </div>
</div>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\iniciar_acompanhamento.html

html
{% extends 'base.html' %}

{% block title %}Iniciar Acompanhamento de Carência{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Iniciar Acompanhamento de Carência</h1>
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
                    <p><strong>Curso:</strong> {{ carencia.frequencia_mensal.turma.curso.nome }}</p>
                    <p><strong>Turma:</strong> {{ carencia.frequencia_mensal.turma.nome }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Período:</strong> {{ carencia.frequencia_mensal.get_mes_display }}/{{ carencia.frequencia_mensal.ano }}</p>
                    <p><strong>Percentual de Presença:</strong> {{ carencia.percentual_presenca }}%</p>
                    <p><strong>Status Atual:</strong> {{ carencia.get_status_display }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Formulário de acompanhamento -->
    <div class="card mb-4">
        <div class="card-header bg-warning text-dark">
            <h5 class="mb-0">Iniciar Acompanhamento</h5>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="observacoes" class="form-label">Observações</label>
                    <textarea class="form-control" id="observacoes" name="observacoes" rows="5" required></textarea>
                    <div class="form-text">Descreva as ações que serão tomadas para acompanhar esta carência.</div>
                </div>
                
                <div class="mb-3">
                    <label for="prazo_resolucao" class="form-label">Prazo Estimado para Resolução</label>
                    <input type="date" class="form-control" id="prazo_resolucao" name="prazo_resolucao" 
                           min="{{ data_atual|date:'Y-m-d' }}" required>
                    <div class="form-text">Defina um prazo para a resolução desta carência.</div>
                </div>
                
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="criar_notificacao" name="criar_notificacao" checked>
                    <label class="form-check-label" for="criar_notificacao">
                        Criar notificação para o aluno
                    </label>
                </div>
                
                <div id="notificacao_fields" class="border p-3 rounded mb-3">
                    <h6>Dados da Notificação</h6>
                    
                    <div class="mb-3">
                        <label for="assunto" class="form-label">Assunto</label>
                        <input type="text" class="form-control" id="assunto" name="assunto" 
                               value="Notificação de Carência - {{ carencia.frequencia_mensal.turma.curso.nome }}">
                    </div>
                    
                    <div class="mb-3">
                        <label for="mensagem" class="form-label">Mensagem</label>
                        <textarea class="form-control" id="mensagem" name="mensagem" rows="5">Prezado(a) {{ carencia.aluno.nome }},

Identificamos que sua frequência no curso {{ carencia.frequencia_mensal.turma.curso.nome }}, turma {{ carencia.frequencia_mensal.turma.nome }}, no período de {{ carencia.frequencia_mensal.get_mes_display }}/{{ carencia.frequencia_mensal.ano }} está abaixo do mínimo necessário (75%).

Seu percentual atual de presença é de {{ carencia.percentual_presenca }}%.

Por favor, entre em contato com a secretaria para regularizar sua situação.

Atenciosamente,
Equipe OMAUM</textarea>
                    </div>
                    
                    <div class="mb-3 form-check">
                        <input type="checkbox" class="form-check-input" id="enviar_agora" name="enviar_agora" checked>
                        <label class="form-check-label" for="enviar_agora">
                            Enviar notificação imediatamente
                        </label>
                    </div>
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'frequencias:detalhar_carencia' carencia.id %}" class="btn btn-secondary">
                        Cancelar
                    </a>
                    <button type="submit" class="btn btn-warning">
                        <i class="fas fa-clock"></i> Iniciar Acompanhamento
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        const criarNotificacaoCheckbox = document.getElementById('criar_notificacao');
        const notificacaoFields = document.getElementById('notificacao_fields');
        
        criarNotificacaoCheckbox.addEventListener('change', function() {
            notificacaoFields.style.display = this.checked ? 'block' : 'none';
        });
        
        // Definir prazo padrão para 7 dias a partir de hoje
        const prazoInput = document.getElementById('prazo_resolucao');
        if (prazoInput) {
            const hoje = new Date();
            const prazo = new Date(hoje);
            prazo.setDate(hoje.getDate() + 7);
            
            const ano = prazo.getFullYear();
            const mes = String(prazo.getMonth() + 1).padStart(2, '0');
            const dia = String(prazo.getDate()).padStart(2, '0');
            
            prazoInput.value = `${ano}-${mes}-${dia}`;
        }
    });
</script>
{% endblock %}



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


'''