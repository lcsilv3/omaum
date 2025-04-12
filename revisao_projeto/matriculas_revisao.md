# Revisão da Funcionalidade: matriculas

## Arquivos views.py:


### Arquivo: matriculas\views.py

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def listar_matriculas(request):
    """Lista todas as matrículas."""
    return render(request, 'matriculas/listar_matriculas.html')

@login_required
def detalhar_matricula(request, id):
    """Exibe os detalhes de uma matrícula."""
    return render(request, 'matriculas/detalhes_matricula.html')

@login_required
def realizar_matricula(request):
    """Realiza uma nova matrícula."""
    return render(request, 'matriculas/realizar_matricula.html')

```

## Arquivos urls.py:


### Arquivo: matriculas\urls.py

```python
from django.urls import path
from . import views

app_name = 'matriculas'

urlpatterns = [
    path('', views.listar_matriculas, name='listar_matriculas'),
    path('<int:id>/detalhes/', views.detalhar_matricula, name='detalhar_matricula'),
    path('realizar/', views.realizar_matricula, name='realizar_matricula'),
]

```

## Arquivos de Template:


### Arquivo: matriculas\templates\matriculas\detalhes_matricula.html

```html
{% extends 'base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}

```


### Arquivo: matriculas\templates\matriculas\listar_matriculas.html

```html
{% extends 'base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}

```


### Arquivo: matriculas\templates\matriculas\realizar_matricula.html

```html
{% extends 'base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}

```
