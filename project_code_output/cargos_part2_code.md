# Código da Funcionalidade: cargos - Parte 2/3
*Gerado automaticamente*



## cargos\templates\cargos\atribuir_cargo.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Atribuir Cargo</h1>
  
  <form method="post">
    {% csrf_token %}
    {% include 'includes/form_errors.html' %}
    
    {% for field in form %}
      {% include 'includes/form_field.html' %}
    {% endfor %}
    
    <button type="submit" class="btn btn-primary">Atribuir</button>
    <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}





## cargos\templates\cargos\confirmar_exclusao.html

html
{% extends 'base.html' %}

{% block title %}Confirmar Exclusão{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">Confirmar Exclusão</h1>
    
    <div class="card">
        <div class="card-body">
            <p class="lead">Tem certeza que deseja excluir o cargo administrativo "{{ cargo.nome }}"?</p>
            <p class="text-danger">Esta ação não pode ser desfeita.</p>
            
            <form method="post">
                {% csrf_token %}
                <button type="submit" class="btn btn-danger">Sim, excluir</button>
                <a href="{% url 'cargos:listar_cargos_administrativos' %}" class="btn btn-secondary">Cancelar</a>
            </form>
        </div>
    </div>
</div>
{% endblock %}





## cargos\templates\cargos\criar_cargo.html

html
{% extends 'base.html' %}

{% block title %}Criar Novo Cargo Administrativo{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Criar Novo Cargo Administrativo</h1>
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        {% for field in form %}
            {% include 'includes/form_field.html' %}
        {% endfor %}
        
        <button type="submit" class="btn btn-primary">Criar Cargo</button>
        <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}





## cargos\templates\cargos\detalhar_cargo.html

html
{% extends 'core/base.html' %}

{% block title %}Detalhes do Cargo Administrativo{% endblock %}

{% block content %}
<div class="container mt-4">
  <h1>Detalhes do Cargo Administrativo</h1>
  
  <div class="card">
    <div class="card-header">
      <h2>{{ cargo.nome }}</h2>
    </div>
    <div class="card-body">
      <p><strong>Código:</strong> {{ cargo.codigo_cargo }}</p>
      <p><strong>Descrição:</strong> {{ cargo.descricao|default:"Não informada" }}</p>
    </div>
    <div class="card-footer">
      <a href="{% url 'cargos:editar_cargo' cargo.id %}" class="btn btn-warning">Editar</a>
      <a href="{% url 'cargos:excluir_cargo' cargo.id %}" class="btn btn-danger">Excluir</a>
      <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Voltar</a>
    </div>
  </div>
</div>
{% endblock %}





## cargos\templates\cargos\detalhes_cargo.html

html
{% extends 'base.html' %}

{% block title %}Detalhes do Cargo Administrativo{% endblock %}

{% block content %}
<div class="container mt-4">
  <h1>Detalhes do Cargo Administrativo</h1>
  
  <div class="card">
    <div class="card-header">
      <h2>{{ cargo.nome }}</h2>
    </div>
    <div class="card-body">
      <p><strong>Código:</strong> {{ cargo.codigo_cargo }}</p>
      <p><strong>Descrição:</strong> {{ cargo.descricao|default:"Não informada" }}</p>
    </div>
    <div class="card-footer">
      <a href="{% url 'cargos:editar_cargo' cargo.id %}" class="btn btn-warning">Editar</a>
      <a href="{% url 'cargos:excluir_cargo' cargo.id %}" class="btn btn-danger">Excluir</a>
      <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Voltar</a>
    </div>
  </div>
</div>
{% endblock %}





## cargos\templates\cargos\detalhe_cargo.html

html
{% extends 'base.html' %}

{% block title %}Detalhes do Cargo{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">Detalhes do Cargo Administrativo</h1>
    
    <div class="card">
        <div class="card-body">
            <h2>{{ cargo.nome }}</h2>
            <p><strong>Código:</strong> {{ cargo.codigo_cargo }}</p>
            <p><strong>Descrição:</strong> {{ cargo.descricao }}</p>
            
            <div class="mt-3">
                <a href="{% url 'cargos:editar_cargo' cargo.codigo_cargo %}" class="btn btn-warning">Editar</a>
                <a href="{% url 'cargos:excluir_cargo' cargo.codigo_cargo %}" class="btn btn-danger">Excluir</a>
                <a href="{% url 'cargos:listar_cargos_administrativos' %}" class="btn btn-secondary">Voltar para a Lista</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}





## cargos\templates\cargos\editar_cargo.html

html
{% extends 'base.html' %}

{% block title %}Editar Cargo Administrativo{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Cargo Administrativo</h1>
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        {% for field in form %}
            {% include 'includes/form_field.html' %}
        {% endfor %}
        
        <button type="submit" class="btn btn-primary">Atualizar Cargo</button>
        <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}





## cargos\templates\cargos\excluir_cargo.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Cargo</h1>
  
    <div class="alert alert-danger">
      <p>Tem certeza que deseja excluir o cargo "{{ cargo.nome }}"?</p>
      {% if atribuicoes %}
        <p><strong>Atenção:</strong> Este cargo possui {{ atribuicoes.count }} atribuições. Excluir o cargo removerá todas as atribuições associadas.</p>
      {% endif %}
    </div>
  
    <form method="post">
      {% csrf_token %}
      <button type="submit" class="btn btn-danger">Sim, excluir</button>
      <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}





## cargos\templates\cargos\formulario_cargo.html

html
{% extends 'base.html' %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">{{ titulo }}</h1>
    
    <form method="post">
        {% csrf_token %}
        
        <div class="card">
            <div class="card-body">
                {% for field in form %}
                <div class="mb-3">
                    <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                    {{ field }}
                    {% if field.errors %}
                    <div class="text-danger">
                        {{ field.errors }}
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="mt-3">
            <button type="submit" class="btn btn-primary">Salvar</button>
            <a href="{% url 'cargos:listar_cargos_administrativos' %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}





## cargos\templates\cargos\form_cargo.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>{% if cargo.id %}Editar{% else %}Novo{% endif %} Cargo</h1>
  
  <form method="post">
    {% csrf_token %}
    {% include 'includes/form_errors.html' %}
    
    {% for field in form %}
      {% include 'includes/form_field.html' %}
    {% endfor %}
    
    <button type="submit" class="btn btn-primary">Salvar</button>
    <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}



