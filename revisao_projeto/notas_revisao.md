# Revisão da Funcionalidade: notas

## Arquivos views.py:


### Arquivo: notas\views.py

python
from django.shortcuts import render, get_object_or_404
from .models import Nota


def listar_notas(request):
    notas = Nota.objects.all()
    return render(request, "notas/listar_notas.html", {"notas": notas})


def detalhar_nota(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id)
    return render(request, "notas/detalhar_nota.html", {"nota": nota})



## Arquivos urls.py:


### Arquivo: notas\urls.py

python
from django.urls import path
from . import views

app_name = "notas"

urlpatterns = [
    path("", views.listar_notas, name="listar_notas"),
    path("<int:nota_id>/", views.detalhar_nota, name="detalhar_nota"),
]



## Arquivos models.py:


### Arquivo: notas\models.py

python
from django.db import models
from alunos.models import Aluno
from cursos.models import Curso


class Nota(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    data = models.DateField()

    def __str__(self):
        return f"Nota de {self.aluno} em {self.curso}: {self.valor}"



## Arquivos de Template:


### Arquivo: notas\templates\notas\listar_notas.html

html
{% extends 'base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}


