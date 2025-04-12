# Revisão da Funcionalidade: notas

## Arquivos views.py:


### Arquivo: notas\views.py

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def listar_notas(request):
    """Lista todas as notas."""
    return render(request, 'notas/listar_notas.html')

```

## Arquivos urls.py:


### Arquivo: notas\urls.py

```python
from django.urls import path
from . import views

app_name = 'notas'

urlpatterns = [
    path('', views.listar_notas, name='listar_notas'),
]

```

## Arquivos de Template:


### Arquivo: notas\templates\notas\listar_notas.html

```html
{% extends 'base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}

```
