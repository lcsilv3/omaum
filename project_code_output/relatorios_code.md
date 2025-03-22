# Código da Funcionalidade: relatorios
*Gerado automaticamente*



## relatorios\admin.py

python
from django.contrib import admin

# Register your models here.




## relatorios\apps.py

python
from django.apps import AppConfig


class RelatoriosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relatorios'




## relatorios\models.py

python
from django.db import models

# Create your models here.




## relatorios\tests.py

python
from django.test import TestCase

# Create your tests here.




## relatorios\urls.py

python
from django.urls import path
from . import views

urlpatterns = [
    path('alunos/', views.relatorio_alunos, name='relatorio_alunos'),
    path('alunos/pdf/', views.relatorio_alunos_pdf, name='relatorio_alunos_pdf'),
]




## relatorios\views.py

python
from django.shortcuts import render
from django.http import HttpResponse
from alunos.models import Aluno  # Update the import to use the correct app
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

def relatorio_alunos(request):
    alunos = Aluno.objects.all()
    context = {
        'alunos': alunos,
    }
    return render(request, 'relatorios/relatorio_alunos.html', context)

def relatorio_alunos_pdf(request):
    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=letter)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 750, "Relatório de Alunos")

    alunos = Aluno.objects.all()
    y = 700
    for aluno in alunos:
        p.drawString(100, y, f"{aluno.nome} - {aluno.cpf}")
        y -= 20

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')




## relatorios\templates\relatorios\gerar_relatorio.html

html
{% extends 'core/base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}




## relatorios\templates\relatorios\relatorio_alunos.html

html
{% extends 'base.html' %}

{% block content %}
<h1>Relatório de Alunos</h1>
<a href="{% url 'relatorio_alunos_pdf' %}" class="btn btn-primary">Download PDF</a>
<table class="table table-striped">
    <thead>
        <tr>
            <th>Nome</th>
            <th>CPF</th>
            <th>Email</th>
            <!-- Adicione mais colunas conforme necessário -->
        </tr>
    </thead>
    <tbody>
        {% for aluno in alunos %}
        <tr>
            <td>{{ aluno.nome }}</td>
            <td>{{ aluno.cpf }}</td>
            <td>{{ aluno.email }}</td>
            <!-- Adicione mais campos conforme necessário -->
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}




## relatorios\tests\test_views.py

python
from django.test import TestCase, Client
from django.urls import reverse
from alunos.models import Aluno
from datetime import date, time

class RelatorioViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='Maria Oliveira',
            data_nascimento=date(1985, 5, 15),
            hora_nascimento=time(14, 30),
            email='maria@example.com',
            sexo='F',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='João Oliveira',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Pai',
            nome_segundo_contato='Ana Oliveira',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Mãe',
            tipo_sanguineo='A',
            fator_rh='+'
        )

    def test_relatorio_alunos(self):
        response = self.client.get(reverse('relatorio_alunos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Oliveira')

    def test_relatorio_alunos_pdf(self):
        response = self.client.get(reverse('relatorio_alunos_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

