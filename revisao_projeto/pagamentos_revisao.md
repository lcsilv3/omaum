# Revisão da Funcionalidade: pagamentos

## Arquivos views.py:


### Arquivo: pagamentos\views.py

python
from django.shortcuts import render, get_object_or_404
from .models import Pagamento


def listar_pagamentos(request):
    pagamentos = Pagamento.objects.all()
    return render(
        request,
        "pagamentos/listar_pagamentos.html",
        {"pagamentos": pagamentos},
    )


def detalhar_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    return render(
        request, "pagamentos/detalhar_pagamento.html", {"pagamento": pagamento}
    )



## Arquivos urls.py:


### Arquivo: pagamentos\urls.py

python
from django.urls import path
from . import views

app_name = "pagamentos"

urlpatterns = [
    path("", views.listar_pagamentos, name="listar_pagamentos"),
    path(
        "<int:pagamento_id>/",
        views.detalhar_pagamento,
        name="detalhar_pagamento",
    ),
]



## Arquivos models.py:


### Arquivo: pagamentos\models.py

python
from django.db import models
from alunos.models import Aluno


class Pagamento(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("pendente", "Pendente"),
            ("pago", "Pago"),
            ("cancelado", "Cancelado"),
        ],
    )

    def __str__(self):
        return f"Pagamento de {self.aluno} - {self.valor} em {self.data_pagamento}"



## Arquivos de Template:


### Arquivo: pagamentos\templates\pagamentos\listar_pagamentos.html

html
{% extends 'base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}


