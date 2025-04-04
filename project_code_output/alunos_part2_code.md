# Código da Funcionalidade: alunos - Parte 2/3
*Gerado automaticamente*



## alunos\templates\alunos\criar_aluno.html

html
{% extends 'core/base.html' %}

{% block title %}Criar Novo Aluno{% endblock %}

{% block content %}
<div class="container mt-4">
  <h1>Criar Novo Aluno</h1>
  
  <form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    
    {% for field in form %}
      <div class="form-group">
        <label for="{{ field.id_for_label }}">{{ field.label }}</label>
        {{ field }}
        {% if field.help_text %}
          <small class="form-text text-muted">{{ field.help_text }}</small>
        {% endif %}
        {% for error in field.errors %}
          <div class="alert alert-danger">{{ error }}</div>
        {% endfor %}
      </div>
    {% endfor %}
    
    <button type="submit" class="btn btn-primary">Salvar</button>
    <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}




## alunos\templates\alunos\dashboard.html

html
{% extends 'core/base.html' %}
{% load static %}

{% block content %}
<div class="container mt-4">
    <h1 class="mb-4">Dashboard de Alunos</h1>

    <div class="row">
        <!-- Cartão de Total de Alunos -->
        <div class="col-md-3 mb-4">
            <div class="card text-white bg-primary">
                <div class="card-body">
                    <h5 class="card-title">Total de Alunos</h5>
                    <p class="card-text display-4">{{ total_alunos }}</p>
                </div>
            </div>
        </div>

        <!-- Cartão de Alunos Ativos -->
        <div class="col-md-3 mb-4">
            <div class="card text-white bg-success">
                <div class="card-body">
                    <h5 class="card-title">Alunos Ativos</h5>
                    <p class="card-text display-4">{{ alunos_ativos }}</p>
                </div>
            </div>
        </div>

        <!-- Cartão de Alunos por Curso -->
        <div class="col-md-3 mb-4">
            <div class="card text-white bg-info">
                <div class="card-body">
                    <h5 class="card-title">Cursos</h5>
                    <p class="card-text display-4">{{ total_cursos }}</p>
                </div>
            </div>
        </div>

        <!-- Cartão de Atividades Recentes -->
        <div class="col-md-3 mb-4">
            <div class="card text-white white-warning">
                <div class="card-body">
                    <h5 class="card-title">Atividades Recentes</h5>
                    <p class="card-text display-4">{{ atividades_recentes }}</p>
                </div>
            </div>
        </div>
    </div>

    <div class="row mt-4">
        <!-- Gráfico de Alunos por Curso -->
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Alunos por Curso</h5>
                    <canvas id="alunosPorCursoChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Lista de Alunos Recentes -->
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Alunos Recentemente Adicionados</h5>
                    <ul class="list-group">
                        {% for aluno in alunos_recentes %}
                            <li class="list-group-item">
                                {{ aluno.nome }}
                                <a href="{% url 'alunos:detalhes' aluno.cpf %}" class="btn btn-sm btn-info float-right">Detalhes</a>
                            </li>
                        {% empty %}
                            <li class="list-group-item">Nenhum aluno recente.</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <div class="row mt-4">
        <!-- Ações Rápidas -->
        <div class="col-md-12">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Ações Rápidas</h5>
                    <a href="{% url 'alunos:cadastrar' %}" class="btn btn-primary mr-2">Cadastrar Novo Aluno</a>
                    <a href="{% url 'alunos:listar' %}" class="btn btn-secondary mr-2">Listar Todos os Alunos</a>
                    <a href="{% url 'alunos:exportar' %}" class="btn btn-success mr-2">Exportar Dados</a>
                    <a href="{% url 'alunos:importar' %}" class="btn btn-info">Importar Dados</a>
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
    var ctx = document.getElementById('alunosPorCursoChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: JSON.parse('{{ cursos_labels|safe }}'),
            datasets: [{
                label: 'Número de Alunos',
                data: JSON.parse('{{ alunos_por_curso_data|safe }}'),
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
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





## alunos\templates\alunos\detalhar_aluno.html

html
{% extends 'core/base.html' %}

{% block title %}{% if aluno.id %}Editar{% else %}Novo{% endif %} Aluno{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{% if aluno.id %}Editar{% else %}Novo{% endif %} Aluno</h1>
        <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-secondary">Voltar para a lista</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Dados Pessoais</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.cpf %}
                        {% include 'includes/form_field.html' with field=form.nome %}
                        {% include 'includes/form_field.html' with field=form.data_nascimento %}
                        {% include 'includes/form_field.html' with field=form.hora_nascimento %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.email %}
                        {% include 'includes/form_field.html' with field=form.sexo %}
                        {% include 'includes/form_field.html' with field=form.foto %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Dados Iniciáticos</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.numero_iniciatico %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome_iniciatico %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Nacionalidade e Naturalidade</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nacionalidade %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.naturalidade %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Endereço</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        {% include 'includes/form_field.html' with field=form.rua %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.numero_imovel %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.complemento %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.bairro %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.cep %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-8">
                        {% include 'includes/form_field.html' with field=form.cidade %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.estado %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Contatos de Emergência</h5>
            </div>
            <div class="card-body">
                <h6>Primeiro Contato</h6>
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.nome_primeiro_contato %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.celular_primeiro_contato %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.tipo_relacionamento_primeiro_contato %}
                    </div>
                </div>
                
                <h6 class="mt-3">Segundo Contato</h6>
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.nome_segundo_contato %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.celular_segundo_contato %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.tipo_relacionamento_segundo_contato %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações Médicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.tipo_sanguineo %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.fator_rh %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.convenio_medico %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.hospital %}
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.alergias %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.condicoes_medicas_gerais %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">
                {% if aluno.cpf %}Atualizar{% else %}Cadastrar{% endif %} Aluno
            </button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
    // Script para pré-visualização da imagem quando o usuário seleciona uma foto
    document.addEventListener('DOMContentLoaded', function() {
        const fotoInput = document.getElementById('{{ form.foto.id_for_label }}');
        if (fotoInput) {
            fotoInput.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    const preview = document.createElement('img');
                    preview.className = 'img-fluid mt-2 rounded';
                    preview.style.maxHeight = '200px';
                    
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        preview.src = e.target.result;
                    }
                    
                    reader.readAsDataURL(this.files[0]);
                    
                    // Remove qualquer preview anterior
                    const previewContainer = fotoInput.parentNode;
                    const existingPreview = previewContainer.querySelector('img');
                    if (existingPreview) {
                        previewContainer.removeChild(existingPreview);
                    }
                    
                    // Adiciona o novo preview
                    previewContainer.appendChild(preview);
                }
            });
        }
    });
</script>
{% endblock %}





## alunos\templates\alunos\editar_aluno.html

html
{% extends 'core/base.html' %}

{% block title %}Editar Aluno: {{ aluno.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Aluno: {{ aluno.nome }}</h1>
    
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        
        {% for field in form %}
            <div class="form-group mb-3">
                <label for="{{ field.id_for_label }}">{{ field.label }}</label>
                {{ field }}
                {% if field.help_text %}
                    <small class="form-text text-muted">{{ field.help_text }}</small>
                {% endif %}
                {% for error in field.errors %}
                    <div class="alert alert-danger">{{ error }}</div>
                {% endfor %}
            </div>
        {% endfor %}
        
        <div class="mt-4">
            <button type="submit" class="btn btn-primary">Salvar Alterações</button>
            <a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>
            <a href="{% url 'alunos:detalhar_aluno' aluno.cpf %}" class="btn btn-info">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}




## alunos\templates\alunos\excluir_aluno.html

html
{% extends 'core/base.html' %}

{% block title %}Excluir Aluno: {{ aluno.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
  <h1>Excluir Aluno: {{ aluno.nome }}</h1>
    
  <div class="alert alert-danger">
      <p>Você tem certeza que deseja excluir o aluno "{{ aluno.nome }}"?</p>
      <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
  </div>
    
  <form method="post">
      {% csrf_token %}
      <button type="submit" class="btn btn-danger">Confirmar Exclusão</button>
      <a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>
      <a href="{% url 'alunos:detalhar_aluno' aluno.cpf %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}





## alunos\templates\alunos\formulario_aluno.html

html
{% extends 'core/base.html' %}

{% block title %}{% if aluno.id %}Editar{% else %}Novo{% endif %} Aluno{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{% if aluno.id %}Editar{% else %}Novo{% endif %} Aluno</h1>
        <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-secondary">Voltar para a lista</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Dados Pessoais</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.cpf %}
                        {% include 'includes/form_field.html' with field=form.nome %}
                        {% include 'includes/form_field.html' with field=form.data_nascimento %}
                        {% include 'includes/form_field.html' with field=form.hora_nascimento %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.email %}
                        {% include 'includes/form_field.html' with field=form.sexo %}
                        {% include 'includes/form_field.html' with field=form.foto %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Dados Iniciáticos</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.numero_iniciatico %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome_iniciatico %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Nacionalidade e Naturalidade</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nacionalidade %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.naturalidade %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Endereço</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        {% include 'includes/form_field.html' with field=form.rua %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.numero_imovel %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.complemento %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.bairro %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.cep %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-8">
                        {% include 'includes/form_field.html' with field=form.cidade %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.estado %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Contatos de Emergência</h5>
            </div>
            <div class="card-body">
                <h6>Primeiro Contato</h6>
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.nome_primeiro_contato %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.celular_primeiro_contato %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.tipo_relacionamento_primeiro_contato %}
                    </div>
                </div>
                
                <h6 class="mt-3">Segundo Contato</h6>
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.nome_segundo_contato %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.celular_segundo_contato %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.tipo_relacionamento_segundo_contato %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações Médicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.tipo_sanguineo %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.fator_rh %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.convenio_medico %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.hospital %}
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.alergias %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.condicoes_medicas_gerais %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">
                {% if aluno.id %}Atualizar{% else %}Cadastrar{% endif %} Aluno
            </button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
    // Script para pré-visualização da imagem quando o usuário seleciona uma foto
    document.addEventListener('DOMContentLoaded', function() {
        const fotoInput = document.getElementById('{{ form.foto.id_for_label }}');
        if (fotoInput) {
            fotoInput.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    const preview = document.createElement('img');
                    preview.className = 'img-fluid mt-2 rounded';
                    preview.style.maxHeight = '200px';
                    
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        preview.src = e.target.result;
                    }
                    
                    reader.readAsDataURL(this.files[0]);
                    
                    // Remove qualquer preview anterior
                    const previewContainer = fotoInput.parentNode;
                    const existingPreview = previewContainer.querySelector('img');
                    if (existingPreview) {
                        previewContainer.removeChild(existingPreview);
                    }
                    
                    // Adiciona o novo preview
                    previewContainer.appendChild(preview);
                }
            });
        }
    });
</script>
{% endblock %}





## alunos\templates\alunos\importar_alunos.html

html
{% extends 'core/base.html' %}

{% block title %}Importar Alunos{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Importar Alunos</h1>
    
    <div class="card">
        <div class="card-body">
            <p class="mb-3">Faça upload de um arquivo CSV contendo os dados dos alunos.</p>
            
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                <div class="mb-3">
                    <label for="csv_file" class="form-label">Arquivo CSV</label>
                    <input type="file" name="csv_file" id="csv_file" class="form-control" accept=".csv" required>
                    <div class="form-text">O arquivo deve ter cabeçalhos: CPF, Nome, Email, etc.</div>
                </div>
                
                <div class="d-flex">
                    <button type="submit" class="btn btn-primary me-2">Importar</button>
                    <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
    
    <div class="mt-3">
        <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-link">Voltar para a lista de alunos</a>
    </div>
</div>
{% endblock %}




## alunos\templates\alunos\listar_alunos.html

html
{% extends 'core/base.html' %}

{% block title %}Lista de Alunos{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Cabeçalho com título e botões na mesma linha -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Lista de Alunos</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'alunos:criar_aluno' %}" class="btn btn-primary">Novo Aluno</a>
            <a href="{% url 'alunos:exportar_alunos' %}" class="btn btn-success">Exportar CSV</a>
            <a href="{% url 'alunos:importar_alunos' %}" class="btn btn-info">Importar CSV</a>
            <a href="{% url 'alunos:relatorio_alunos' %}" class="btn btn-warning">Relatório</a>
            <a href="{% url 'alunos:dashboard' %}" class="btn btn-dark">Dashboard</a>
        </div>
    </div>
    
    <!-- Barra de busca e filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <form method="get" class="row g-3">
                <div class="col-md-6">
                    <input type="text" name="q" class="form-control" placeholder="Buscar por nome, CPF ou email..." value="{{ query }}">
                </div>
                <div class="col-md-4">
                    <select name="curso" class="form-select">
                        <option value="">Todos os cursos</option>
                        {% for curso in cursos %}
                            <option value="{{ curso.codigo_curso }}" {% if curso.codigo_curso|stringformat:"s" == curso_selecionado %}selected{% endif %}>{{ curso.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn btn-primary w-100">Filtrar</button>
                </div>
            </form>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>CPF</th>
                            <th>Email</th>
                            <th>Data de Nascimento</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for aluno in alunos %}
                            <tr>
                                <td>{{ aluno.nome }}</td>
                                <td>{{ aluno.cpf }}</td>
                                <td>{{ aluno.email }}</td>
                                <td>{{ aluno.data_nascimento|date:"d/m/Y" }}</td>
                                <td>
                                    {% if aluno.cpf %}
                                        <a href="{% url 'alunos:detalhar_aluno' aluno.cpf %}" class="btn btn-sm btn-info">Detalhes</a>
                                        <a href="{% url 'alunos:editar_aluno' aluno.cpf %}" class="btn btn-sm btn-warning">Editar</a>
                                        <a href="{% url 'alunos:excluir_aluno' aluno.cpf %}" class="btn btn-sm btn-danger">Excluir</a>
                                    {% else %}
                                        <span class="text-muted">CPF não disponível</span>
                                    {% endif %}
                                </td>
                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="5" class="text-center">
                                    <p class="my-3">Nenhum aluno cadastrado.</p>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer">
            <p class="text-muted mb-0">Total: {{ alunos.count|default:"0" }} aluno(s)</p>
            {% if page_obj.has_other_pages %}
                <nav aria-label="Paginação">
                    <ul class="pagination justify-content-center mb-0">
                        {% if page_obj.has_previous %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.previous_page_number }}&q={{ query }}&curso={{ curso_selecionado }}">Anterior</a>
                            </li>
                        {% else %}
                            <li class="page-item disabled">
                                <span class="page-link">Anterior</span>
                            </li>
                        {% endif %}

                        {% for num in page_obj.paginator.page_range %}
                            {% if page_obj.number == num %}
                                <li class="page-item active">
                                    <span class="page-link">{{ num }}</span>
                                </li>
                            {% else %}
                                <li class="page-item">
                                    <a class="page-link" href="?page={{ num }}&q={{ query }}&curso={{ curso_selecionado }}">{{ num }}</a>
                                </li>
                            {% endif %}
                        {% endfor %}

                        {% if page_obj.has_next %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.next_page_number }}&q={{ query }}&curso={{ curso_selecionado }}">Próxima</a>
                            </li>
                        {% else %}
                            <li class="page-item disabled">
                                <span class="page-link">Próxima</span>
                            </li>
                        {% endif %}
                    </ul>
                </nav>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}





## alunos\templates\alunos\registro.html

html
{% extends 'base.html' %}

{% block content %}
<h2>Registro</h2>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Registrar</button>
</form>

<a href="javascript:history.back()" class="back-button">Voltar</a>

<style>
    .back-button {
        margin-top: 20px;
        display: inline-block;
        padding: 10px 20px;
        background-color: #f0f0f0;
        border: 1px solid #ccc;
        text-decoration: none;
        color: #333;
        border-radius: 5px;
    }
</style>
{% endblock %}





## alunos\templates\alunos\relatorio_alunos.html

html
{% extends 'core/base.html' %}

{% block title %}Relatório de Alunos{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Relatório de Alunos</h1>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="card-title">Estatísticas Gerais</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-3">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Total de Alunos</h5>
                            <p class="card-text display-4">{{ total_alunos }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Masculino</h5>
                            <p class="card-text display-4">{{ total_masculino }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Feminino</h5>
                            <p class="card-text display-4">{{ total_feminino }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Outros</h5>
                            <p class="card-text display-4">{{ total_outros }}</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="card mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Idade Média</h5>
                            <p class="card-text display-4">{{ idade_media|floatformat:1 }} anos</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}



