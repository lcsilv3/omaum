# Código da Funcionalidade: frequencias - Parte 2/2
*Gerado automaticamente*



## frequencias\templates\frequencias\editar_frequencia.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Registro de Frequência</h1>
  
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





## frequencias\templates\frequencias\estatisticas_frequencia.html

html
{% extends 'core/base.html' %}

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
                            <option value="{{ turma.id }}" {% if turma_id == turma.id|stringformat:"s" %}selected{% endif %}>{{ turma.codigo_turma }}</option>
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





## frequencias\templates\frequencias\excluir_frequencia.html

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





## frequencias\templates\frequencias\listar_frequencias.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Frequências</h1>
  
    <div class="d-flex justify-content-between mb-3">
      <a href="{% url 'frequencias:registrar_frequencia' %}" class="btn btn-primary">Registrar Frequência</a>
      <a href="{% url 'frequencias:relatorio_frequencias' %}" class="btn btn-info">Gerar Relatório</a>
    </div>
  
    <div class="card mb-4">
      <div class="card-header">
        <h5>Filtros</h5>
      </div>
      <div class="card-body">
        <form method="get" class="row g-3">
          <div class="col-md-4">
            <label for="aluno" class="form-label">Aluno</label>
            <select name="aluno" id="aluno" class="form-select">
              <option value="">Todos</option>
              {% for aluno in alunos %}
                <option value="{{ aluno.id }}" {% if request.GET.aluno == aluno.id|stringformat:"i" %}selected{% endif %}>
                  {{ aluno.nome }}
                </option>
              {% endfor %}
            </select>
          </div>
          <div class="col-md-4">
            <label for="atividade" class="form-label">Atividade</label>
            <select name="atividade" id="atividade" class="form-select">
              <option value="">Todas</option>
              {% for atividade in atividades %}
                <option value="{{ atividade.id }}" {% if request.GET.atividade == atividade.id|stringformat:"i" %}selected{% endif %}>
                  {{ atividade.nome }}
                </option>
              {% endfor %}
            </select>
          </div>
          <div class="col-md-4">
            <label for="data" class="form-label">Data</label>
            <input type="date" name="data" id="data" class="form-control" value="{{ request.GET.data }}">
          </div>
          <div class="col-12 mt-3">
            <button type="submit" class="btn btn-primary">Filtrar</button>
            <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">Limpar Filtros</a>
          </div>
        </form>
      </div>
    </div>
  
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Aluno</th>
          <th>Atividade</th>
          <th>Data</th>
          <th>Presente</th>
          <th>Justificativa</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        {% for frequencia in frequencias %}
        <tr>
          <td>{{ frequencia.aluno.nome }}</td>
          <td>{{ frequencia.atividade.nome }}</td>
          <td>{{ frequencia.data|date:"d/m/Y" }}</td>
          <td>
            {% if frequencia.presente %}
              <span class="badge bg-success">Sim</span>
            {% else %}
              <span class="badge bg-danger">Não</span>
            {% endif %}
          </td>
          <td>{{ frequencia.justificativa|truncatechars:30|default:"-" }}</td>
          <td>
            <a href="{% url 'frequencias:detalhar_frequencia' frequencia.id %}" class="btn btn-sm btn-info">Detalhes</a>
            <a href="{% url 'frequencias:editar_frequencia' frequencia.id %}" class="btn btn-sm btn-warning">Editar</a>
            <a href="{% url 'frequencias:excluir_frequencia' frequencia.id %}" class="btn btn-sm btn-danger">Excluir</a>
          </td>
        </tr>
        {% empty %}
        <tr>
          <td colspan="6">Nenhum registro de frequência encontrado.</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  
    {% if frequencias.has_other_pages %}
    <nav aria-label="Paginação">
      <ul class="pagination justify-content-center">
        {% if frequencias.has_previous %}
          <li class="page-item">
            <a class="page-link" href="?page=1{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.atividade %}&atividade={{ request.GET.atividade }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}" aria-label="Primeira">
              <span aria-hidden="true">««</span>
            </a>
          </li>
          <li class="page-item">
            <a class="page-link" href="?page={{ frequencias.previous_page_number }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.atividade %}&atividade={{ request.GET.atividade }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}" aria-label="Anterior">
              <span aria-hidden="true">«</span>
            </a>
          </li>
        {% else %}
          <li class="page-item disabled">
            <a class="page-link" href="#" aria-label="Primeira">
              <span aria-hidden="true">««</span>
            </a>
          </li>
          <li class="page-item disabled">
            <a class="page-link" href="#" aria-label="Anterior">
              <span aria-hidden="true">«</span>
            </a>
          </li>
        {% endif %}
      
        {% for i in frequencias.paginator.page_range %}
          {% if frequencias.number == i %}
            <li class="page-item active"><a class="page-link" href="#">{{ i }}</a></li>
          {% elif i > frequencias.number|add:'-3' and i < frequencias.number|add:'3' %}
            <li class="page-item">
              <a class="page-link" href="?page={{ i }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.atividade %}&atividade={{ request.GET.atividade }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}">{{ i }}</a>
            </li>
          {% endif %}
        {% endfor %}
      
        {% if frequencias.has_next %}
          <li class="page-item">
            <a class="page-link" href="?page={{ frequencias.next_page_number }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.atividade %}&atividade={{ request.GET.atividade }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}" aria-label="Próxima">
              <span aria-hidden="true">»</span>
            </a>
          </li>
          <li class="page-item">
            <a class="page-link" href="?page={{ frequencias.paginator.num_pages }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.atividade %}&atividade={{ request.GET.atividade }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}" aria-label="Última">
              <span aria-hidden="true">»»</span>
            </a>
          </li>
        {% else %}
          <li class="page-item disabled">
            <a class="page-link" href="#" aria-label="Próxima">
              <span aria-hidden="true">»</span>
            </a>
          </li>
          <li class="page-item disabled">
            <a class="page-link" href="#" aria-label="Última">
              <span aria-hidden="true">»»</span>
            </a>
          </li>
        {% endif %}
      </ul>
    </nav>
    {% endif %}
  
    <div class="mt-3">
      <a href="{% url 'frequencias:exportar_frequencias' %}" class="btn btn-success">Exportar para Excel</a>
    </div>
</div>
{% endblock %}





## frequencias\templates\frequencias\registrar_frequencia.html

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





## frequencias\templates\frequencias\registrar_frequencia_turma.html

html
{% extends 'core/base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Registrar Frequência da Turma: {{ turma.codigo_turma }}</h1>
   
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





## frequencias\templates\frequencias\relatorio_frequencias.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Relatório de Frequências</h1>
  
  <div class="card mb-4">
    <div class="card-header">
      <h5>Filtros do Relatório</h5>
    </div>
    <div class="card-body">
      <form method="get" class="row g-3">
        <div class="col-md-4">
          <label for="aluno" class="form-label">Aluno</label>
          <select name="aluno" id="aluno" class="form-select">
            <option value="">Todos</option>
            {% for aluno in alunos %}
              <option value="{{ aluno.id }}" {% if request.GET.aluno == aluno.id|stringformat:"i" %}selected{% endif %}>
                {{ aluno.nome }}
              </option>
            {% endfor %}
          </select>
        </div>
        <div class="col-md-4">
          <label for="atividade" class="form-label">Atividade</label>
          <select name="atividade" id="atividade" class="form-select">
            <option value="">Todas</option>
            {% for atividade in atividades %}
              <option value="{{ atividade.id }}" {% if request.GET.atividade == atividade.id|stringformat:"i" %}selected{% endif %}>
                {{ atividade.nome }}
              </option>
            {% endfor %}
          </select>
        </div>
        <div class="col-md-4">
          <label for="turma" class="form-label">Turma</label>
          <select name="turma" id="turma" class="form-select">
            <option value="">Todas</option>
            {% for turma in turmas %}
              <option value="{{ turma.id }}" {% if request.GET.turma == turma.id|stringformat:"i" %}selected{% endif %}>
                {{ turma.nome }}
              </option>
            {% endfor %}
          </select>
        </div>
        <div class="col-md-4">
          <label for="data_inicio" class="form-label">Data Início</label>
          <input type="date" name="data_inicio" id="data_inicio" class="form-control" value="{{ request.GET.data_inicio }}">
        </div>
        <div class="col-md-4">
          <label for="data_fim" class="form-label">Data Fim</label>
          <input type="date" name="data_fim" id="data_fim" class="form-control" value="{{ request.GET.data_fim }}">
        </div>
        <div class="col-md-4">
          <label for="status" class="form-label">Status</label>
          <select name="status" id="status" class="form-select">
            <option value="">Todos</option>
            <option value="presente" {% if request.GET.status == 'presente' %}selected{% endif %}>Presente</option>
            <option value="ausente" {% if request.GET.status == 'ausente' %}selected{% endif %}>Ausente</option>
          </select>
        </div>
        <div class="col-12 mt-3">
          <button type="submit" class="btn btn-primary">Gerar Relatório</button>
          <a href="{% url 'frequencias:relatorio_frequencias' %}" class="btn btn-secondary">Limpar Filtros</a>
          {% if frequencias %}
            <a href="{% url 'frequencias:exportar_frequencias' %}?{{ request.GET.urlencode }}" class="btn btn-success">Exportar para Excel</a>
          {% endif %}
        </div>
      </form>
    </div>
  </div>
  
  {% if frequencias %}
    <div class="card">
      <div class="card-header">
        <h5>Resultados do Relatório</h5>
      </div>
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Aluno</th>
                <th>Atividade</th>
                <th>Turma</th>
                <th>Data</th>
                <th>Status</th>
                <th>Justificativa</th>
              </tr>
            </thead>
            <tbody>
              {% for frequencia in frequencias %}
              <tr>
                <td>{{ frequencia.aluno.nome }}</td>
                <td>{{ frequencia.atividade.nome }}</td>
                <td>{{ frequencia.atividade.turma.nome }}</td>
                <td>{{ frequencia.data|date:"d/m/Y" }}</td>
                <td>
                  {% if frequencia.presente %}
                    <span class="badge bg-success">Presente</span>
                  {% else %}
                    <span class="badge bg-danger">Ausente</span>
                  {% endif %}
                </td>
                <td>{{ frequencia.justificativa|default:"-" }}</td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
        
        <div class="mt-4">
          <h5>Resumo</h5>
          <div class="row">
            <div class="col-md-4">
              <div class="card bg-light">
                <div class="card-body">
                  <h6 class="card-title">Total de Registros</h6>
                  <p class="card-text display-6">{{ frequencias|length }}</p>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card bg-success text-white">
                <div class="card-body">
                  <h6 class="card-title">Presenças</h6>
                  <p class="card-text display-6">{{ presencas }}</p>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card bg-danger text-white">
                <div class="card-body">
                  <h6 class="card-title">Ausências</h6>
                  <p class="card-text display-6">{{ ausencias }}</p>
                </div>
              </div>
            </div>
          </div>
          
          {% if taxa_presenca is not None %}
          <div class="mt-3">
            <h6>Taxa de Presença: {{ taxa_presenca }}%</h6>
            <div class="progress">
              <div class="progress-bar bg-success" role="progressbar" style="width: {{ taxa_presenca }}%" aria-valuenow="{{ taxa_presenca }}" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
          </div>
          {% endif %}
        </div>
      </div>
    </div>
  {% elif request.GET %}
    <div class="alert alert-info">
      Nenhum registro de frequência encontrado com os filtros selecionados.
    </div>
  {% endif %}
</div>
{% endblock %}





## frequencias\templatetags\frequencia_extras.py

python
from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    """Subtrai o argumento do valor"""
    return value - arg





## frequencias\templatetags\__init__.py

python
# Arquivo vazio para marcar o diretório como um pacote Python



