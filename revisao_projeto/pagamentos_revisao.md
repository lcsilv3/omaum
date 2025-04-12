# Revisão da Funcionalidade: pagamentos

## Arquivos views.py:


### Arquivo: pagamentos\views.py

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def listar_pagamentos(request):
    """Lista todos os pagamentos."""
    return render(request, 'pagamentos/listar_pagamentos.html')

```

## Arquivos urls.py:


### Arquivo: pagamentos\urls.py

```python
from django.urls import path
from . import views

app_name = 'pagamentos'

urlpatterns = [
    path('', views.listar_pagamentos, name='listar_pagamentos'),
]

```

## Arquivos de Template:


### Arquivo: pagamentos\templates\pagamentos\listar_pagamentos.html

```html
{% extends 'base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}

```
