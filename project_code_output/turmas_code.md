# Código da Funcionalidade: turmas
*Gerado automaticamente*



## turmas\admin.py

python
from django.contrib import admin
from .models import Turma, Matricula

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'curso', 'data_inicio', 'data_fim', 'status', 'capacidade']
    list_filter = ['status', 'curso']
    search_fields = ['nome', 'curso__nome']
    date_hierarchy = 'data_inicio'

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'turma', 'data_matricula', 'status']
    list_filter = ['status', 'turma']
    search_fields = ['aluno__nome', 'turma__nome']
    date_hierarchy = 'data_matricula'




## turmas\apps.py

python
from django.apps import AppConfig


class TurmasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'turmas'




## turmas\forms.py

python
from django import forms
from .models import Turma, Matricula
from cursos.models import Curso
from alunos.models import Aluno
from django.core.exceptions import ValidationError

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'curso', 'data_inicio', 'data_fim', 'capacidade', 'status', 'descricao']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise ValidationError("O nome da turma deve ter pelo menos 3 caracteres.")
        return nome

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        if data_inicio and data_fim and data_inicio >= data_fim:
            raise ValidationError("A data de início deve ser anterior à data de fim.")
        return cleaned_data

class AlunoSelecionadoForm(forms.Form):
    aluno = forms.ModelChoiceField(
        queryset=Aluno.objects.all(),
        label="Selecione pelo menos um aluno",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        curso = kwargs.pop('curso', None)
        super().__init__(*args, **kwargs)
        
        if curso:
            # Filtra alunos pelo curso selecionado
            self.fields['aluno'].queryset = Aluno.objects.filter(curso=curso)

class TurmaComAlunoForm(forms.Form):
    """Formulário combinado para criar uma turma com pelo menos um aluno"""
    # Campos da turma
    nome = forms.CharField(max_length=100, label="Nome da Turma")
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(), 
        label="Curso",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_curso'})
    )
    data_inicio = forms.DateField(
        label="Data de Início",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    data_fim = forms.DateField(
        label="Data de Fim",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    capacidade = forms.IntegerField(
        label="Capacidade de Alunos",
        initial=30,
        min_value=1
    )
    status = forms.ChoiceField(
        choices=Turma.OPCOES_STATUS,
        initial='A',
        label="Status"
    )
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label="Descrição"
    )
    
    # Campo para selecionar pelo menos um aluno
    alunos = forms.ModelMultipleChoiceField(
        queryset=Aluno.objects.all(),
        label="Selecione pelo menos um aluno",
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        help_text="Mantenha pressionado Ctrl (ou Command no Mac) para selecionar múltiplos alunos."
    )
    
    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        alunos = cleaned_data.get('alunos')
        curso = cleaned_data.get('curso')
        
        if data_inicio and data_fim and data_inicio >= data_fim:
            raise ValidationError("A data de início deve ser anterior à data de fim.")
        
        if not alunos or len(alunos) < 1:
            raise ValidationError("É necessário selecionar pelo menos um aluno para criar uma turma.")
        
        # Verifica se todos os alunos pertencem ao curso selecionado
        if alunos and curso:
            for aluno in alunos:
                if aluno.curso != curso:
                    raise ValidationError(f"O aluno {aluno.nome} não pertence ao curso {curso.nome}.")
        
        return cleaned_data

class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields = ['aluno', 'status']
        
    def __init__(self, *args, **kwargs):
        turma = kwargs.pop('turma', None)
        super().__init__(*args, **kwargs)
        
        if turma:
            # Filtra alunos pelo curso da turma
            self.fields['aluno'].queryset = self.fields['aluno'].queryset.filter(curso=turma.curso)



## turmas\models.py

python
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Turma(models.Model):
    OPCOES_STATUS = [
        ('A', 'Ativa'),
        ('I', 'Inativa'),
        ('C', 'Concluída'),
    ]
    
    nome = models.CharField('Nome', max_length=100)
    curso = models.ForeignKey('cursos.Curso', on_delete=models.CASCADE, verbose_name='Curso')
    data_inicio = models.DateField('Data de Início')
    data_fim = models.DateField('Data de Fim')
    status = models.CharField('Status', max_length=1, choices=OPCOES_STATUS, default='A')
    capacidade = models.PositiveIntegerField('Capacidade de Alunos', default=30)
    descricao = models.TextField('Descrição', blank=True)
    
    def __str__(self):
        return f"{self.nome} - {self.curso}"
    
    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
    
    def clean(self):
        if self.data_fim and self.data_inicio and self.data_fim < self.data_inicio:
            raise ValidationError({'data_fim': 'A data de término deve ser posterior à data de início.'})
        
        # Atualiza status automaticamente com base nas datas
        hoje = timezone.now().date()
        if self.status == 'A' and self.data_fim < hoje:
            self.status = 'C'  # Marca como concluída se a data final já passou
    
    @property
    def alunos_matriculados(self):
        return self.matriculas.count()
    
    @property
    def vagas_disponiveis(self):
        return self.capacidade - self.alunos_matriculados
    
    def tem_alunos(self):
        """Verifica se a turma tem pelo menos um aluno matriculado"""
        return self.alunos_matriculados > 0
    
    def save(self, *args, **kwargs):
        # Se for uma turma nova, permitimos salvar sem alunos inicialmente
        if not self.pk:
            super().save(*args, **kwargs)
        else:
            # Para turmas existentes, verificamos se há pelo menos um aluno
            if not self.tem_alunos():
                raise ValidationError("Uma turma deve ter pelo menos um aluno matriculado.")
            super().save(*args, **kwargs)


class Matricula(models.Model):
    OPCOES_STATUS = [
        ('A', 'Ativa'),
        ('C', 'Cancelada'),
        ('F', 'Finalizada'),
    ]
    
    aluno = models.ForeignKey('alunos.Aluno', on_delete=models.CASCADE, 
                             related_name='matriculas', verbose_name='Aluno')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, 
                             related_name='matriculas', verbose_name='Turma')
    data_matricula = models.DateField('Data da Matrícula', auto_now_add=True)
    status = models.CharField('Status', max_length=1, choices=OPCOES_STATUS, default='A')
    
    class Meta:
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        unique_together = ['aluno', 'turma']
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.turma.nome}"
    
    def clean(self):
        # Check if class is active
        if self.turma.status != 'A':
            raise ValidationError({'turma': _('Não é possível matricular em uma turma inativa ou concluída.')})
        
        # Check if there are available spots
        if not self.pk and self.turma.vagas_disponiveis <= 0:  # Only for new enrollments
            raise ValidationError({'turma': _('Não há vagas disponíveis nesta turma.')})
        
        # Check if student's course matches the class's course
        if self.aluno.curso != self.turma.curso:
            raise ValidationError({'aluno': _('O aluno deve pertencer ao mesmo curso da turma.')})



## turmas\tests.py

python
from django.test import TestCase

# Create your tests here.




## turmas\urls.py

python
from django.urls import path
from . import views

app_name = 'turmas'

urlpatterns = [
    # URLs para Turmas
    path('', views.listar_turmas, name='listar_turmas'),
    path('criar/', views.criar_turma, name='criar_turma'),
    path('<int:id>/', views.detalhar_turma, name='detalhar_turma'),
    path('<int:id>/editar/', views.editar_turma, name='editar_turma'),
    path('<int:id>/excluir/', views.excluir_turma, name='excluir_turma'),
    
    # URLs para Matrículas
    path('<int:turma_id>/matricular/', views.matricular_aluno, name='matricular_aluno'),
    path('<int:turma_id>/alunos/', views.listar_alunos_matriculados, name='listar_alunos_matriculados'),
    path('<int:turma_id>/alunos/<int:aluno_id>/cancelar/', views.cancelar_matricula, name='cancelar_matricula'),
    
    # URLs para Cursos (mantidas para compatibilidade)
    path('cursos/', views.listar_cursos, name='listar_cursos'),
    path('cursos/criar/', views.criar_curso, name='criar_curso'),
    path('cursos/<int:id>/editar/', views.editar_curso, name='editar_curso'),
    path('cursos/<int:id>/excluir/', views.excluir_curso, name='excluir_curso'),
    path('cursos/<int:id>/', views.detalhar_curso, name='detalhar_curso'),
]




## turmas\views.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from .models import Turma, Matricula
from cursos.models import Curso
from .forms import TurmaForm, MatriculaForm

# Views para Turmas
@login_required
def listar_turmas(request):
    query = request.GET.get('q')
    curso_id = request.GET.get('curso')
    status = request.GET.get('status')
    
    turmas = Turma.objects.all().select_related('curso')
    
    if query:
        turmas = turmas.filter(
            Q(nome__icontains=query) | 
            Q(curso__nome__icontains=query)
        )
    
    if curso_id:
        turmas = turmas.filter(curso_id=curso_id)
    
    if status:
        turmas = turmas.filter(status=status)
    
    # Obtém todos os cursos para o filtro dropdown
    cursos = Curso.objects.all()
    
    paginator = Paginator(turmas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'turmas': page_obj,
        'query': query,
        'cursos': cursos,
        'curso_selecionado': curso_id,
        'opcoes_status': Turma.OPCOES_STATUS,
        'status_selecionado': status
    }
    
    return render(request, 'turmas/listar_turmas.html', context)

@login_required
def criar_turma(request):
    if request.method == 'POST':
        form = TurmaComAlunoForm(request.POST)
        if form.is_valid():
            # Cria a turma
            turma = Turma(
                nome=form.cleaned_data['nome'],
                curso=form.cleaned_data['curso'],
                data_inicio=form.cleaned_data['data_inicio'],
                data_fim=form.cleaned_data['data_fim'],
                capacidade=form.cleaned_data['capacidade'],
                status=form.cleaned_data['status'],
                descricao=form.cleaned_data['descricao']
            )
            turma.save()
            
            # Cria as matrículas para os alunos selecionados
            alunos = form.cleaned_data['alunos']
            for aluno in alunos:
                Matricula.objects.create(
                    aluno=aluno,
                    turma=turma,
                    status='A'  # Ativa
                )
            
            messages.success(request, 'Turma criada com sucesso com os alunos selecionados!')
            return redirect('turmas:listar_turmas')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = TurmaComAlunoForm()
    
    return render(request, 'turmas/criar_turma.html', {'form': form})

@login_required
def detalhar_turma(request, id):
    turma = get_object_or_404(Turma, id=id)
    matriculas = Matricula.objects.filter(turma=turma).select_related('aluno')
    
    context = {
        'turma': turma,
        'matriculas': matriculas,
        'total_matriculas': matriculas.count(),
        'vagas_disponiveis': turma.capacidade - matriculas.count()
    }
    
    return render(request, 'turmas/detalhar_turma.html', context)

@login_required
def editar_turma(request, id):
    turma = get_object_or_404(Turma, id=id)
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turma atualizada com sucesso!')
            return redirect('turmas:listar_turmas')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = TurmaForm(instance=turma)
    return render(request, 'turmas/editar_turma.html', {'form': form, 'turma': turma})

@login_required
def excluir_turma(request, id):
    turma = get_object_or_404(Turma, id=id)
    
    # Verifica se há matrículas associadas à turma
    matriculas = Matricula.objects.filter(turma=turma)
    
    if request.method == 'POST':
        if matriculas.exists():
            messages.error(request, 'Não é possível excluir uma turma com alunos matriculados.')
            return redirect('turmas:detalhar_turma', id=turma.id)
        
        turma.delete()
        messages.success(request, 'Turma excluída com sucesso!')
        return redirect('turmas:listar_turmas')
    
    return render(request, 'turmas/excluir_turma.html', {
        'turma': turma,
        'tem_matriculas': matriculas.exists()
    })

# Views para Matrículas
@login_required
def matricular_aluno(request, turma_id):
    """Matricula um aluno na turma"""
    turma = get_object_or_404(Turma, pk=turma_id)
    
    # Verificar se há vagas disponíveis
    if turma.vagas_disponiveis <= 0:
        adicionar_mensagem(request, 'erro', 'Não há vagas disponíveis nesta turma.')
        return redirect('turmas:detalhes_turma', turma_id=turma.id)
    
    if request.method == 'POST':
        form = AlunoTurmaForm(request.POST, turma=turma)
        if form.is_valid():
            aluno = form.cleaned_data['aluno']
            
            # Verificar se o aluno já está matriculado
            if turma.alunos.filter(id=aluno.id).exists():
                adicionar_mensagem(request, 'erro', f'O aluno {aluno.nome} já está matriculado nesta turma.')
            else:
                turma.alunos.add(aluno)
                registrar_log(request, f'Aluno {aluno.nome} matriculado na turma {turma.nome}')
                adicionar_mensagem(request, 'sucesso', f'Aluno {aluno.nome} matriculado com sucesso!')
            
            return redirect('turmas:detalhes_turma', turma_id=turma.id)
    else:
        form = AlunoTurmaForm(turma=turma)
    
    return render(request, 'turmas/matricular_aluno.html', {
        'form': form,
        'turma': turma,
        'titulo': f'Matricular Aluno na Turma: {turma.nome}'
    })

@login_required
def cancelar_matricula(request, turma_id, aluno_id):
    """Cancela a matrícula de um aluno na turma"""
    turma = get_object_or_404(Turma, pk=turma_id)
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    
    if request.method == 'POST':
        if turma.alunos.filter(id=aluno.id).exists():
            turma.alunos.remove(aluno)
            registrar_log(request, f'Matrícula do aluno {aluno.nome} na turma {turma.nome} foi cancelada')
            adicionar_mensagem(request, 'sucesso', f'Matrícula do aluno {aluno.nome} cancelada com sucesso!')
        else:
            adicionar_mensagem(request, 'erro', f'O aluno {aluno.nome} não está matriculado nesta turma.')
        
        return redirect('turmas:detalhes_turma', turma_id=turma.id)
    
    return render(request, 'turmas/confirmar_cancelamento_matricula.html', {
        'turma': turma,
        'aluno': aluno,
        'titulo': 'Confirmar Cancelamento de Matrícula'
    })

@login_required
def listar_alunos_matriculados(request, turma_id):
    """Lista todos os alunos matriculados em uma turma"""
    turma = get_object_or_404(Turma, pk=turma_id)
    alunos = turma.alunos.all()
    
    return render(request, 'turmas/listar_alunos_matriculados.html', {
        'turma': turma,
        'alunos': alunos,
        'titulo': f'Alunos Matriculados na Turma: {turma.nome}'
    })

# Views para Cursos (mantidas para compatibilidade)
def listar_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'turmas/listar_cursos.html', {'cursos': cursos})

def criar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso criado com sucesso!')
            return redirect('turmas:listar_cursos')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CursoForm()
    return render(request, 'turmas/criar_curso.html', {'form': form})

def detalhar_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    return render(request, 'turmas/detalhar_curso.html', {'curso': curso})

def editar_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso atualizado com sucesso!')
            return redirect('turmas:listar_cursos')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CursoForm(instance=curso)
    return render(request, 'turmas/editar_curso.html', {'form': form, 'curso': curso})

def excluir_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    if request.method == 'POST':
        curso.delete()
        messages.success(request, 'Curso excluído com sucesso!')
        return redirect('turmas:listar_cursos')
    return render(request, 'turmas/excluir_curso.html', {'curso': curso})



## turmas\migrations\0001_initial.py

python
# Generated by Django 5.1.7 on 2025-03-16 21:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alunos', '__first__'),
        ('cursos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inicio', models.DateField()),
                ('data_fim', models.DateField()),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True)),
                ('alunos', models.ManyToManyField(blank=True, to='alunos.aluno')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso')),
            ],
        ),
    ]




## turmas\migrations\0002_curso_alter_turma_options_remove_turma_alunos_and_more.py

python
# Generated by Django 5.1.7 on 2025-03-16 23:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turmas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('codigo_curso', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Código do Curso')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('descricao', models.TextField(verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Curso',
                'verbose_name_plural': 'Cursos',
            },
        ),
        migrations.AlterModelOptions(
            name='turma',
            options={'verbose_name': 'Turma', 'verbose_name_plural': 'Turmas'},
        ),
        migrations.RemoveField(
            model_name='turma',
            name='alunos',
        ),
        migrations.RemoveField(
            model_name='turma',
            name='descricao',
        ),
        migrations.AlterField(
            model_name='turma',
            name='data_fim',
            field=models.DateField(verbose_name='Data de Fim'),
        ),
        migrations.AlterField(
            model_name='turma',
            name='data_inicio',
            field=models.DateField(verbose_name='Data de Início'),
        ),
        migrations.AlterField(
            model_name='turma',
            name='nome',
            field=models.CharField(max_length=100, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='turma',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='turmas.curso', verbose_name='Curso'),
        ),
    ]




## turmas\migrations\0003_alter_turma_curso_alter_turma_data_fim_and_more.py

python
# Generated by Django 5.1.7 on 2025-03-17 03:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0003_curso_descricao_curso_duracao'),
        ('turmas', '0002_curso_alter_turma_options_remove_turma_alunos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turma',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso'),
        ),
        migrations.AlterField(
            model_name='turma',
            name='data_fim',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='turma',
            name='data_inicio',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='turma',
            name='nome',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Curso',
        ),
    ]




## turmas\templates\turmas\cancelar_matricula.html

html
{% extends 'base.html' %}

{% block title %}Cancelar Matrícula{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Cancelar Matrícula</h1>
    
    {% if ultima_matricula %}
        <div class="alert alert-danger">
            <p>Não é possível cancelar esta matrícula porque é a única matrícula ativa na turma.</p>
            <p>Uma turma deve ter pelo menos um aluno matriculado.</p>
        </div>
        <a href="{% url 'turmas:detalhar_turma' matricula.turma.id %}" class="btn btn-primary">Voltar para Detalhes da Turma</a>
    {% else %}
        <div class="alert alert-warning">
            <p>Você tem certeza que deseja cancelar a matrícula de "{{ matricula.aluno.nome }}" na turma "{{ matricula.turma.nome }}"?</p>
        </div>
        
        <form method="post">
            {% csrf_token %}
            <button type="submit" class="btn btn-danger">Confirmar Cancelamento</button>
            <a href="{% url 'turmas:detalhar_turma' matricula.turma.id %}" class="btn btn-secondary">Cancelar</a>
        </form>
    {% endif %}
</div>
{% endblock %}




## turmas\templates\turmas\confirmar_cancelamento_matricula.html

html
{% extends 'core/base.html' %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card">
        <div class="card-header bg-danger text-white">
            <h4>Confirmar Cancelamento de Matrícula</h4>
        </div>
        <div class="card-body">
            <p class="lead">Você tem certeza que deseja cancelar a matrícula do aluno <strong>{{ aluno.nome }}</strong> na turma <strong>{{ turma.nome }}</strong>?</p>
            <p>Esta ação não poderá ser desfeita.</p>
            
            <div class="mt-4">
                <form method="post">
                    {% csrf_token %}
                    <div class="d-flex justify-content-between">
                        <a href="{% url 'turmas:listar_alunos_matriculados' turma.id %}" class="btn btn-secondary">Cancelar</a>
                        <button type="submit" class="btn btn-danger">Confirmar Cancelamento</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    
    <a href="javascript:history.back()" class="btn btn-secondary mt-3">Voltar</a>
</div>
{% endblock %}




## turmas\templates\turmas\criar_turma.html

html
{% extends 'base.html' %}

{% block title %}Criar Turma{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Criar Nova Turma</h1>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="alert alert-info">
        <p><strong>Atenção:</strong> Para criar uma turma, é necessário adicionar pelo menos um aluno.</p>
    </div>
    
    <form method="post">
        {% csrf_token %}
        
        {% if form.non_field_errors %}
            <div class="alert alert-danger">
                {% for error in form.non_field_errors %}
                    {{ error }}
                {% endfor %}
            </div>
        {% endif %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h3>Informações da Turma</h3>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <div class="form-group mb-3">
                            <label for="{{ form.nome.id_for_label }}">{{ form.nome.label }}</label>
                            {{ form.nome }}
                            {% if form.nome.errors %}
                                <div class="alert alert-danger mt-1">
                                    {% for error in form.nome.errors %}
                                        {{ error }}
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group mb-3">
                            <label for="{{ form.curso.id_for_label }}">{{ form.curso.label }}</label>
                            {{ form.curso }}
                            {% if form.curso.errors %}
                                <div class="alert alert-danger mt-1">
                                    {% for error in form.curso.errors %}
                                        {{ error }}
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="form-group mb-3">
                            <label for="{{ form.data_inicio.id_for_label }}">{{ form.data_inicio.label }}</label>
                            {{ form.data_inicio }}
                            {% if form.data_inicio.errors %}
                                <div class="alert alert-danger mt-1">
                                    {% for error in form.data_inicio.errors %}
                                        {{ error }}
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group mb-3">
                            <label for="{{ form.data_fim.id_for_label }}">{{ form.data_fim.label }}</label>
                            {{ form.data_fim }}
                            {% if form.data_fim.errors %}
                                <div class="alert alert-danger mt-1">
                                    {% for error in form.data_fim.errors %}
                                        {{ error }}
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-4">
                        <div class="form-group mb-3">
                            <label for="{{ form.capacidade.id_for_label }}">{{ form.capacidade.label }}</label>
                            {{ form.capacidade }}
                            {% if form.capacidade.errors %}
                                <div class="alert alert-danger mt-1">
                                    {% for error in form.capacidade.errors %}
                                        {{ error }}
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-md-8">
                        <div class="form-group mb-3">
                            <label for="{{ form.status.id_for_label }}">{{ form.status.label }}</label>
                            {{ form.status }}
                            {% if form.status.errors %}
                                <div class="alert alert-danger mt-1">
                                    {% for error in form.status.errors %}
                                        {{ error }}
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
                
                <div class="form-group mb-3">
                    <label for="{{ form.descricao.id_for_label }}">{{ form.descricao.label }}</label>
                    {{ form.descricao }}
                    {% if form.descricao.errors %}
                        <div class="alert alert-danger mt-1">
                            {% for error in form.descricao.errors %}
                                {{ error }}
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h3>Alunos</h3>
            </div>
            <div class="card-body">
                <div class="form-group mb-3">
                    <label for="{{ form.alunos.id_for_label }}">{{ form.alunos.label }}</label>
                    {{ form.alunos }}
                    {% if form.alunos.help_text %}
                        <small class="form-text text-muted">{{ form.alunos.help_text }}</small>
                    {% endif %}
                    {% if form.alunos.errors %}
                        <div class="alert alert-danger mt-1">
                            {% for error in form.alunos.errors %}
                                {{ error }}
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <button type="submit" class="btn btn-primary">Salvar Turma</button>
        <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




## turmas\templates\turmas\detalhar_turma.html

html
{% extends 'base.html' %}

{% block title %}Detalhes da Turma{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Detalhes da Turma</h1>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card mb-4">
        <div class="card-header">
            <h2>{{ turma.nome }}</h2>
        </div>
        <div class="card-body">
            <p><strong>Curso:</strong> {{ turma.curso }}</p>
            <p><strong>Data de Início:</strong> {{ turma.data_inicio|date:"d/m/Y" }}</p>
            <p><strong>Data de Fim:</strong> {{ turma.data_fim|date:"d/m/Y" }}</p>
            <p><strong>Status:</strong> {{ turma.get_status_display }}</p>
            <p><strong>Capacidade:</strong> {{ turma.capacidade }} alunos</p>
            <p><strong>Alunos Matriculados:</strong> {{ total_matriculas }}</p>
            <p><strong>Vagas Disponíveis:</strong> {{ vagas_disponiveis }}</p>
            {% if turma.descricao %}
                <p><strong>Descrição:</strong> {{ turma.descricao }}</p>
            {% endif %}
        </div>
    </div>
    
    <h2>Alunos Matriculados</h2>
    
    {% if vagas_disponiveis > 0 %}
        <a href="{% url 'turmas:matricular_aluno' turma.id %}" class="btn btn-primary mb-3">
            <i class="fas fa-user-plus"></i> Matricular Aluno
        </a>
    {% else %}
        <div class="alert alert-warning mb-3">
            Não há vagas disponíveis nesta turma.
        </div>
    {% endif %}
    
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Nome</th>
                <th>Matrícula</th>
                <th>Data da Matrícula</th>
                <th>Status</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody>
            {% for matricula in matriculas %}
            <tr>
                <td>{{ matricula.aluno.nome }}</td>
                <td>{{ matricula.aluno.matricula }}</td>
                <td>{{ matricula.data_matricula|date:"d/m/Y" }}</td>
                <td>{{ matricula.get_status_display }}</td>
                <td>
                    {% if matricula.status == 'A' %}
                        <a href="{% url 'turmas:cancelar_matricula' matricula.id %}" class="btn btn-sm btn-danger">Cancelar Matrícula</a>
                    {% endif %}
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="5" class="text-center">Nenhum aluno matriculado nesta turma.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <div class="mt-3">
        <a href="{% url 'turmas:editar_turma' turma.id %}" class="btn btn-warning">Editar Turma</a>
        <a href="{% url 'turmas:excluir_turma' turma.id %}" class="btn btn-danger">Excluir Turma</a>
        <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Voltar para Lista</a>
    </div>
</div>
{% endblock %}




## turmas\templates\turmas\detalhes_turma.html

html
{% extends 'base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}




## turmas\templates\turmas\editar_turma.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Turma</h1>
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        {% for field in form %}
            {% include 'includes/form_field.html' %}
        {% endfor %}
        <button type="submit" class="btn btn-primary">Atualizar Turma</button>
        <a href="{% url 'listar_turmas' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}



## turmas\templates\turmas\excluir_turma.html

html
{% extends 'base.html' %}

{% block title %}Excluir Turma{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Turma</h1>
    
    {% if tem_matriculas %}
        <div class="alert alert-danger">
            <p>Não é possível excluir esta turma porque ela possui alunos matriculados.</p>
            <p>Para excluir a turma, primeiro cancele todas as matrículas.</p>
        </div>
        <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-primary">Voltar para Detalhes da Turma</a>
    {% else %}
        <div class="alert alert-warning">
            <p>Você tem certeza que deseja excluir a turma "{{ turma.nome }}"?</p>
            <p>Esta ação não pode ser desfeita.</p>
        </div>
        
        <form method="post">
            {% csrf_token %}
            <button type="submit" class="btn btn-danger">Confirmar Exclusão</button>
            <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Cancelar</a>
        </form>
    {% endif %}
</div>
{% endblock %}




## turmas\templates\turmas\listar_alunos_matriculados.html

html
{% extends 'core/base.html' %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>{{ titulo }}</h1>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Informações da Turma</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome da Turma:</strong> {{ turma.nome }}</p>
            <p><strong>Curso:</strong> {{ turma.curso.nome }}</p>
            <p><strong>Período:</strong> {{ turma.data_inicio|date:"d/m/Y" }} a {{ turma.data_fim|date:"d/m/Y" }}</p>
            <p><strong>Total de Alunos:</strong> {{ turma.total_alunos }} de {{ turma.vagas }}</p>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Alunos Matriculados</h5>
            <a href="{% url 'turmas:matricular_aluno' turma.id %}" class="btn btn-primary btn-sm">
                <i class="fas fa-plus"></i> Matricular Aluno
            </a>
        </div>
        <div class="card-body">
            {% if alunos %}
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Nome</th>
                                <th>Matrícula</th>
                                <th>Curso</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for aluno in alunos %}
                                <tr>
                                    <td>{{ aluno.nome }}</td>
                                    <td>{{ aluno.matricula }}</td>
                                    <td>{{ aluno.curso.nome }}</td>
                                    <td>
                                        <a href="{% url 'alunos:detalhes_aluno' aluno.id %}" class="btn btn-info btn-sm">
                                            <i class="fas fa-eye"></i>
                                        </a>
                                        <a href="{% url 'turmas:cancelar_matricula' turma.id aluno.id %}" class="btn btn-danger btn-sm">
                                            <i class="fas fa-times"></i> Cancelar Matrícula
                                        </a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <p>Nenhum aluno matriculado nesta turma.</p>
            {% endif %}
        </div>
    </div>
    
    <a href="{% url 'turmas:detalhes_turma' turma.id %}" class="btn btn-secondary mt-3">Voltar para Detalhes da Turma</a>
</div>
{% endblock %}




## turmas\templates\turmas\listar_turmas.html

html
{% extends 'base.html' %}

{% block title %}Lista de Turmas{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Lista de Turmas</h1>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="row mb-3">
        <div class="col-md-8">
            <form method="get" class="form-inline">
                <div class="input-group">
                    <input type="text" name="q" class="form-control" placeholder="Buscar por nome ou curso" value="{{ request.GET.q }}">
                    <div class="input-group-append">
                        <button class="btn btn-outline-secondary" type="submit">Buscar</button>
                    </div>
                </div>
            </form>
        </div>
        <div class="col-md-4">
            <a href="{% url 'turmas:criar_turma' %}" class="btn btn-primary mb-3">
                <i class="fas fa-plus"></i> Nova Turma
            </a>
        </div>
    </div>
    
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Nome</th>
                <th>Curso</th>
                <th>Data de Início</th>
                <th>Data de Fim</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody>
            {% for turma in turmas %}
            <tr>
                <td>{{ turma.nome }}</td>
                <td>{{ turma.curso }}</td>
                <td>{{ turma.data_inicio|date:"d/m/Y" }}</td>
                <td>{{ turma.data_fim|date:"d/m/Y" }}</td>
                <td>
                    <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-sm btn-info">Detalhes</a>
                    <a href="{% url 'turmas:editar_turma' turma.id %}" class="btn btn-sm btn-warning">Editar</a>
                    <a href="{% url 'turmas:excluir_turma' turma.id %}" class="btn btn-sm btn-danger">Excluir</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="5" class="text-center">Nenhuma turma encontrada.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}




## turmas\templates\turmas\matricular_aluno.html

html
{% extends 'core/base.html' %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>{{ titulo }}</h1>
    
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">Informações da Turma</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome da Turma:</strong> {{ turma.nome }}</p>
            <p><strong>Curso:</strong> {{ turma.curso.nome }}</p>
            <p><strong>Período:</strong> {{ turma.data_inicio|date:"d/m/Y" }} a {{ turma.data_fim|date:"d/m/Y" }}</p>
            <p><strong>Vagas Disponíveis:</strong> {{ turma.vagas_disponiveis }} de {{ turma.vagas }}</p>
        </div>
    </div>
    
    <div class="card mt-4">
        <div class="card-header">
            <h5 class="mb-0">Selecionar Aluno</h5>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="{{ form.aluno.id_for_label }}" class="form-label">Aluno</label>
                    {{ form.aluno }}
                    {% if form.aluno.errors %}
                        <div class="text-danger">{{ form.aluno.errors }}</div>
                    {% endif %}
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'turmas:detalhes_turma' turma.id %}" class="btn btn-secondary">Cancelar</a>
                    <button type="submit" class="btn btn-primary">Matricular</button>
                </div>
            </form>
        </div>
    </div>
    
    <a href="javascript:history.back()" class="btn btn-secondary mt-3">Voltar</a>
</div>
{% endblock %}




## turmas\templates\turmas\turma_form.html

html
{% extends 'base.html' %}

{% block content %}
  <h1>Criar Turma</h1>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Criar</button>
  </form>
{% endblock %}



## turmas\tests\test_models.py

python
from django.test import TestCase
from turmas.models import Turma
from cursos.models import Curso
from datetime import date

class TurmaModelTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            nome='Curso de Teste',
            descricao='Descrição do curso de teste'
        )

    def test_criar_turma(self):
        turma = Turma.objects.create(
            nome='Turma de Teste',
            curso=self.curso,
            data_inicio=date(2023, 10, 1),
            data_fim=date(2023, 12, 31)
        )

        self.assertEqual(turma.nome, 'Turma de Teste')
        self.assertEqual(turma.curso, self.curso)
        self.assertEqual(str(turma), 'Turma de Teste - Curso de Teste')

class CargoAdministrativoTest(TestCase):
    def test_criar_cargo(self):
        cargo = CargoAdministrativo.objects.create(
            codigo_cargo='CARGO001',
            nome='Coordenador',
            descricao='Responsável pela coordenação do curso.'
        )
        self.assertEqual(cargo.nome, 'Coordenador')
        self.assertEqual(cargo.codigo_cargo, 'CARGO001')



## turmas\tests\test_views.py

python
from django.test import TestCase, Client
from django.urls import reverse
from turmas.models import Turma
from cursos.models import Curso
from datetime import date

class TurmaViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.curso = Curso.objects.create(
            nome='Curso de Teste',
            descricao='Descrição do curso de teste'
        )
        self.turma = Turma.objects.create(
            nome='Turma de Teste',
            curso=self.curso,
            data_inicio=date(2023, 10, 1),
            data_fim=date(2023, 12, 31)
        )

    def test_listar_turmas(self):
        response = self.client.get(reverse('turmas:turma_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Turma de Teste')
        self.assertContains(response, 'Curso de Teste')

    def test_criar_turma(self):
        response = self.client.post(reverse('turmas:turma_create'), {
            'nome': 'Nova Turma',
            'curso': self.curso.id,
            'data_inicio': '2024-01-01',
            'data_fim': '2024-03-31'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Turma.objects.filter(nome='Nova Turma').exists())

    def test_atualizar_turma(self):
        response = self.client.post(reverse('turmas:turma_update', args=[self.turma.id]), {
            'nome': 'Turma Atualizada',
            'curso': self.curso.id,
            'data_inicio': '2023-11-01',
            'data_fim': '2024-01-31'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.turma.refresh_from_db()
        self.assertEqual(self.turma.nome, 'Turma Atualizada')

    def test_deletar_turma(self):
        response = self.client.post(reverse('turmas:turma_delete', args=[self.turma.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Turma.objects.filter(id=self.turma.id).exists())

class CursoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.curso = Curso.objects.create(
            nome='Curso de Teste',
            descricao='Descrição do curso de teste'
        )

    def test_listar_cursos(self):
        response = self.client.get(reverse('turmas:curso_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Curso de Teste')

    def test_criar_curso(self):
        response = self.client.post(reverse('turmas:curso_create'), {
            'nome': 'Novo Curso',
            'descricao': 'Descrição do novo curso'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Curso.objects.filter(nome='Novo Curso').exists())

    def test_atualizar_curso(self):
        response = self.client.post(reverse('turmas:curso_update', args=[self.curso.id]), {
            'nome': 'Curso Atualizado',
            'descricao': 'Descrição atualizada'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.curso.refresh_from_db()
        self.assertEqual(self.curso.nome, 'Curso Atualizado')

    def test_deletar_curso(self):
        response = self.client.post(reverse('turmas:curso_delete', args=[self.curso.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Curso.objects.filter(id=self.curso.id).exists())


