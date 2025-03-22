# Código da Funcionalidade: cargos
*Gerado automaticamente*



## cargos\admin.py

python
from django.contrib import admin

# Register your models here.




## cargos\apps.py

python
from django.apps import AppConfig


class CargosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cargos'




## cargos\models.py

python
from django.db import models

class CargoAdministrativo(models.Model):
    """
    Represents an administrative cargo in the system. The administrative cargo has a unique code, a name, and an optional description.
    """
    codigo_cargo = models.CharField(max_length=10, unique=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome




## cargos\urls.py

python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_cargos_administrativos, name='listar_cargos_administrativos'),
    path('<str:codigo_cargo>/', views.detalhe_cargo, name='detalhe_cargo'),
]



## cargos\views.py

python
from django.shortcuts import render, get_object_or_404
from .models import CargoAdministrativo

def listar_cargos_administrativos(request):
    cargos = CargoAdministrativo.objects.all()
    return render(request, 'cargos/listar_cargos.html', {'cargos': cargos})

def detalhe_cargo(request, codigo_cargo):
    cargo = get_object_or_404(CargoAdministrativo, codigo_cargo=codigo_cargo)
    return render(request, 'cargos/detalhe_cargo.html', {'cargo': cargo})




## cargos\templates\cargos\detalhe_cargo.html

html
{% extends 'base.html' %}

{% block content %}
<div class="cargo-detail">
    <h1>{{ cargo.nome }}</h1>
    <p>Código: {{ cargo.codigo_cargo }}</p>
    <p>Descrição: {{ cargo.descricao }}</p>
</div>
{% endblock %}




## cargos\templates\cargos\listar_cargos.html

html
{% extends 'base.html' %}

{% block content %}
<h1>Lista de Cargos Administrativos</h1>
<div class="cargos-list">
    {% for cargo in cargos %}
    <div class="cargo-item">
        <h2>{{ cargo.nome }}</h2>
        <p>Código: {{ cargo.codigo_cargo }}</p>
        <p>{{ cargo.descricao }}</p>
    </div>
    {% endfor %}
</div>
{% endblock %}



## cargos\tests\test_models.py

python
from django.test import TestCase
from cargos.models import CargoAdministrativo

class CargoAdministrativoTest(TestCase):
    def test_criar_cargo(self):
        cargo = CargoAdministrativo.objects.create(
            codigo_cargo='CARGO001',
            nome='Coordenador',
            descricao='Responsável pela coordenação do curso.'
        )
        self.assertEqual(cargo.nome, 'Coordenador')
        self.assertEqual(cargo.codigo_cargo, 'CARGO001')




## cargos\tests\test_views.py

python
from django.test import TestCase, Client
from django.urls import reverse
from cargos.models import CargoAdministrativo

class CargoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cargo = CargoAdministrativo.objects.create(
            codigo_cargo='CARGO001',
            nome='Coordenador',
            descricao='Responsável pela coordenação do curso.'
        )

    def test_listar_cargos(self):
        response = self.client.get(reverse('listar_cargos_administrativos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Coordenador')

    def test_detalhe_cargo(self):
        response = self.client.get(reverse('detalhe_cargo', args=[self.cargo.codigo_cargo]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Coordenador')


