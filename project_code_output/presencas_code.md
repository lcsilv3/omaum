# Código da Funcionalidade: presencas
*Gerado automaticamente*



## presencas\admin.py

python
from django.contrib import admin

# Register your models here.




## presencas\apps.py

python
from django.apps import AppConfig


class PresencasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'presencas'




## presencas\forms.py

python
from django import forms
from .models import PresencaAcademica

class PresencaForm(forms.ModelForm):
    class Meta:
        model = PresencaAcademica
        fields = ['aluno', 'turma', 'data', 'presente']



## presencas\models.py

python
from django.db import models
from turmas.models import Turma
from alunos.models import Aluno

class PresencaAcademica(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data = models.DateField()
    presente = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.aluno} - {self.turma} - {self.data}"

    class Meta:
        verbose_name = "Presença Acadêmica"
        verbose_name_plural = "Presenças Acadêmicas"



## presencas\tests.py

python
from django.test import TestCase

# Create your tests here.




## presencas\urls.py

python
from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_presenca, name='registrar_presenca'),
    path('lista/', views.lista_presencas, name='lista_presencas'),
]





## presencas\views.py

python
from django.shortcuts import render, redirect
from .models import PresencaAcademica
from .forms import PresencaForm

def registrar_presenca(request):
    if request.method == 'POST':
        form = PresencaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_presencas')
    else:
        form = PresencaForm()
    return render(request, 'presencas/registrar_presenca.html', {'form': form})

def lista_presencas(request):
    presencas = PresencaAcademica.objects.all()
    return render(request, 'presencas/lista_presencas.html', {'presencas': presencas})




## presencas\tests\test_models.py

python
from django.test import TestCase
from presencas.models import PresencaAcademica
from turmas.models import Turma
from atividades.models import AtividadeAcademica
from alunos.models import Aluno
from datetime import date, time

class PresencaAcademicaModelTest(TestCase):
    def setUp(self):
        self.turma = Turma.objects.create(codigo_turma='TURMA001')
        self.atividade = AtividadeAcademica.objects.create(codigo_atividade='ATV001')
        self.aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            hora_nascimento=time(14, 30),
            email='joao@example.com',
            sexo='M',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='Maria Silva',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Mãe',
            nome_segundo_contato='José Silva',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Pai',
            tipo_sanguineo='A',
            fator_rh='+'
        )

    def test_criar_presenca(self):
        presenca = PresencaAcademica.objects.create(
            codigo_turma=self.turma,
            codigo_atividade=self.atividade,
            cpf_aluno=self.aluno,
            data=date(2023, 10, 1),
            presente=True
        )
        self.assertEqual(presenca.presente, True)
        self.assertEqual(presenca.cpf_aluno, self.aluno)




## presencas\tests\test_views.py

python
from django.test import TestCase, Client
from django.urls import reverse
from presencas.models import PresencaAcademica
from turmas.models import Turma
from atividades.models import AtividadeAcademica
from alunos.models import Aluno
from datetime import date, time

class PresencaViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.turma = Turma.objects.create(codigo_turma='TURMA001')
        self.atividade = AtividadeAcademica.objects.create(codigo_atividade='ATV001')
        self.aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            hora_nascimento=time(14, 30),
            email='joao@example.com',
            sexo='M',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='Maria Silva',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Mãe',
            nome_segundo_contato='José Silva',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Pai',
            tipo_sanguineo='A',
            fator_rh='+'
        )
        self.presenca = PresencaAcademica.objects.create(
            codigo_turma=self.turma,
            codigo_atividade=self.atividade,
            cpf_aluno=self.aluno,
            data=date(2023, 10, 1),
            presente=True
        )

    def test_listar_presencas(self):
        response = self.client.get(reverse('listar_presencas_academicas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'João Silva')


