'''
# Revisão da Funcionalidade: pagamentos

## Arquivos forms.py:


### Arquivo: pagamentos\forms.py

python
"""
Formulários para o aplicativo de pagamentos.
"""
from django import forms
from django.core.validators import MinValueValidator
from django.utils import timezone
from importlib import import_module

from .models import Pagamento  # <-- Adicione esta linha

def get_aluno_model():
    """Importa o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

class PagamentoForm(forms.ModelForm):
    """Formulário para criação e edição de pagamentos."""
    
    class Meta:
        model = Pagamento
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Aluno = get_aluno_model()
        self.fields['aluno'].queryset = Aluno.objects.filter(situacao='ATIVO')

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        data_pagamento = cleaned_data.get('data_pagamento')
        
        # Se o status for PAGO, a data de pagamento é obrigatória
        if status == 'PAGO' and not data_pagamento:
            self.add_error('data_pagamento', 'A data de pagamento é obrigatória quando o status é Pago.')
        
        # Se o status não for PAGO, a data de pagamento deve ser None
        if status != 'PAGO' and data_pagamento:
            cleaned_data['data_pagamento'] = None
        
        return cleaned_data


class PagamentoRapidoForm(forms.ModelForm):
    """Formulário simplificado para registro rápido de pagamentos."""
    
    aluno_cpf = forms.CharField(
        label="CPF do Aluno",
        max_length=11,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o CPF do aluno'})
    )
    
    class Meta:
        from .models import Pagamento
        model = Pagamento
        fields = [
            'valor',
            'data_vencimento',
            'status',
            'metodo_pagamento',
            'observacoes',
        ]
        widgets = {
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'metodo_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Definir valores padrão
        self.fields['data_vencimento'].initial = timezone.now().date()
        self.fields['status'].initial = 'PENDENTE'
    
    def clean_aluno_cpf(self):
        cpf = self.cleaned_data.get('aluno_cpf')
        if cpf:
            # Remover caracteres não numéricos
            cpf = ''.join(filter(str.isdigit, cpf))
            
            # Verificar se o CPF tem 11 dígitos
            if len(cpf) != 11:
                raise forms.ValidationError("O CPF deve conter 11 dígitos.")
            
            # Verificar se o aluno existe
            Aluno = get_aluno_model()
            try:
                aluno = Aluno.objects.get(cpf=cpf)
                return aluno
            except Aluno.DoesNotExist:
                raise forms.ValidationError("Aluno não encontrado com este CPF.")
        
        return cpf
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.aluno = self.cleaned_data.get('aluno_cpf')
        
        if commit:
            instance.save()
        
        return instance


class FiltroPagamentosForm(forms.Form):
    """
    Formulário para filtrar pagamentos.
    """
    q = forms.CharField(
        required=False,
        label="Buscar",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por aluno, CPF ou observações...'
        })
    )
    
    status = forms.ChoiceField(
        choices=[('', 'Todos')] + list(Pagamento.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    data_inicio = forms.DateField(
        required=False,
        label="Data início",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    data_fim = forms.DateField(
        required=False,
        label="Data fim",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )


## Arquivos views.py:


### Arquivo: pagamentos\views.py

python
import logging
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import models
from django.urls import reverse
from .forms import PagamentoForm, FiltroPagamentosForm, PagamentoRapidoForm
from .models import Pagamento
from .exporters import exportar_pagamentos_csv, exportar_pagamentos_excel, exportar_pagamentos_pdf
from pagamentos.helpers import get_aluno_model  # helpers.py deve conter get_aluno_model

from .views.pagamento_views import (
    listar_pagamentos,
    criar_pagamento,
    editar_pagamento,
    excluir_pagamento,
    detalhar_pagamento,
    pagamentos_aluno,
    registrar_pagamento_rapido,
    importar_pagamentos_csv,
    exportar_pagamentos_csv,
    exportar_pagamentos_excel,
    exportar_pagamentos_pdf,
)

from .views.relatorio_views import (
    relatorio_financeiro,
    exportar_pagamentos_excel,
    exportar_pagamentos_pdf,
    dados_grafico_pagamentos,
    pagamentos_por_turma,
    dados_distribuicao_pagamentos,
)

from .views.dashboard_views import (
    dashboard,
    dashboard_pagamentos,
    dashboard_financeiro,
)


## Arquivos urls.py:


### Arquivo: pagamentos\urls.py

python
from django.urls import path
from . import views

app_name = 'pagamentos'

urlpatterns = [
    path('', views.listar_pagamentos, name='listar_pagamentos'),
    path('novo/', views.criar_pagamento, name='criar_pagamento'),
    path('<int:pagamento_id>/editar/', views.editar_pagamento, name='editar_pagamento'),
    path('<int:pagamento_id>/excluir/', views.excluir_pagamento, name='excluir_pagamento'),
    path('<int:pagamento_id>/', views.detalhar_pagamento, name='detalhar_pagamento'),

    path('aluno/<str:cpf>/', views.pagamentos_aluno, name='pagamentos_aluno'),
    path('registrar-rapido/', views.registrar_pagamento_rapido, name='registrar_pagamento_rapido'),

    path('importar/', views.importar_pagamentos_csv, name='importar_pagamentos_csv'),
    path('exportar/csv/', views.exportar_pagamentos_csv, name='exportar_pagamentos_csv'),
    path('exportar/excel/', views.exportar_pagamentos_excel, name='exportar_pagamentos_excel'),
    path('exportar/pdf/', views.exportar_pagamentos_pdf, name='exportar_pagamentos_pdf'),

    path('relatorio/', views.relatorio_financeiro, name='relatorio_financeiro'),
    path('relatorio/turma/', views.pagamentos_por_turma, name='relatorio_pagamentos_turma'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/pagamentos/', views.dashboard_pagamentos, name='dashboard_pagamentos'),
    path('dashboard/financeiro/', views.dashboard_financeiro, name='dashboard_financeiro'),

    path('api/grafico-pagamentos/', views.dados_grafico_pagamentos, name='dados_grafico_pagamentos'),
    path('api/distribuicao-pagamentos/', views.dados_distribuicao_pagamentos, name='dados_distribuicao_pagamentos'),
]


## Arquivos models.py:


### Arquivo: pagamentos\models.py

python
"""
Modelos para o aplicativo de pagamentos.
"""
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from importlib import import_module


def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


class Pagamento(models.Model):
    """
    Modelo para armazenar informações de pagamentos dos alunos.
    """
    # Opções para o campo status
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('ATRASADO', 'Atrasado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    # Opções para o campo método de pagamento
    METODO_PAGAMENTO_CHOICES = [
        ('DINHEIRO', 'Dinheiro'),
        ('PIX', 'PIX'),
        ('CARTAO_CREDITO', 'Cartão de Crédito'),
        ('CARTAO_DEBITO', 'Cartão de Débito'),
        ('TRANSFERENCIA', 'Transferência Bancária'),
        ('BOLETO', 'Boleto'),
        ('OUTRO', 'Outro'),
    ]
    
    # Relacionamentos
    aluno = models.ForeignKey(
        'alunos.Aluno',
        on_delete=models.CASCADE,
        verbose_name=_('Aluno')
    )
    
    # Campos de pagamento
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Valor')
    )
    
    data_vencimento = models.DateField(
        verbose_name=_('Data de Vencimento')
    )
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDENTE',
        verbose_name=_('Status')
    )
    
    data_pagamento = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Data de Pagamento')
    )
    
    valor_pago = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Valor Pago')
    )
    
    metodo_pagamento = models.CharField(
        max_length=20,
        choices=METODO_PAGAMENTO_CHOICES,
        null=True,
        blank=True,
        verbose_name=_('Método de Pagamento')
    )
    
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Observações')
    )
    
    # Metadados
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Criado em')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Atualizado em')
    )
    
    class Meta:
        verbose_name = _('Pagamento')
        verbose_name_plural = _('Pagamentos')
        ordering = ['-data_vencimento']
    
    def __str__(self):
        return f"Pagamento de {self.aluno.nome} - R$ {self.valor} ({self.get_status_display()})"
    
    def save(self, *args, **kwargs):
        """Sobrescreve o método save para atualizar campos automaticamente."""
        # Se o status for PAGO e não houver data de pagamento, definir como hoje
        if self.status == 'PAGO' and not self.data_pagamento:
            self.data_pagamento = timezone.now().date()
        
        # Se o status for PAGO e não houver valor_pago, usar o valor original
        if self.status == 'PAGO' and not self.valor_pago:
            self.valor_pago = self.valor
        
        # Verificar se o pagamento está atrasado
        hoje = timezone.now().date()
        if self.status == 'PENDENTE' and self.data_vencimento < hoje:
            self.status = 'ATRASADO'
        
        super().save(*args, **kwargs)



## Arquivos de Template:


### Arquivo: pagamentos\templates\pagamentos\criar_pagamento.html

html
{% extends 'base.html' %}

{% block title %}Criar Novo Pagamento{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Criar Novo Pagamento</h1>
        <div>
            <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
        </div>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="row">
        <div class="col-md-8">
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Dados do Pagamento</h5>
                </div>
                <div class="card-body">
                    <form method="post" id="pagamento-form">
                        {% csrf_token %}
                        
                        <input type="hidden" name="aluno_id" id="aluno_id" value="">
                        
                        <div class="mb-3">
                            <label for="aluno_busca" class="form-label">Buscar Aluno</label>
                            <div class="input-group">
                                <input type="text" id="aluno_busca" class="form-control" placeholder="Digite nome, CPF ou número iniciático..." autocomplete="off">
                                <button type="button" class="btn btn-outline-secondary" id="btn-buscar-aluno">
                                    <i class="fas fa-search"></i> Buscar
                                </button>
                            </div>
                            <div id="aluno-selecionado" class="mt-2" style="display: none;">
                                <div class="alert alert-info d-flex align-items-center">
                                    <div id="aluno-foto" class="me-3" style="width: 50px; height: 50px; border-radius: 50%; background-color: #ccc; display: flex; align-items: center; justify-content: center; overflow: hidden;">
                                        <span id="aluno-inicial"></span>
                                    </div>
                                    <div>
                                        <strong>Aluno selecionado:</strong> <span id="aluno-nome"></span>
                                        <br>
                                        <small id="aluno-cpf"></small>
                                    </div>
                                    <button type="button" class="btn-close ms-auto" id="btn-limpar-aluno" aria-label="Limpar seleção"></button>
                                </div>
                            </div>
                        </div>
                        
                        <div id="resultados-busca" class="mb-3" style="display: none;">
                            <div class="card">
                                <div class="card-header bg-light">
                                    <h6 class="mb-0">Resultados da Busca</h6>
                                </div>
                                <div class="card-body p-0">
                                    <div class="list-group list-group-flush" id="lista-alunos">
                                        <!-- Resultados da busca serão inseridos aqui -->
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="valor" class="form-label">Valor (R$)</label>
                                    <input type="number" name="valor" id="valor" class="form-control" step="0.01" min="0" required>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="data_vencimento" class="form-label">Data de Vencimento</label>
                                    <input type="date" name="data_vencimento" id="data_vencimento" class="form-control" required>
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label for="observacoes" class="form-label">Observações</label>
                            <textarea name="observacoes" id="observacoes" class="form-control" rows="3"></textarea>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="status" class="form-label">Status</label>
                                    <select name="status" id="status" class="form-select" required>
                                        <option value="PENDENTE">Pendente</option>
                                        <option value="PAGO">Pago</option>
                                        <option value="ATRASADO">Atrasado</option>
                                        <option value="CANCELADO">Cancelado</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3 metodo-pagamento-container" style="display: none;">
                                    <label for="metodo_pagamento" class="form-label">Método de Pagamento</label>
                                    <select name="metodo_pagamento" id="metodo_pagamento" class="form-select">
                                        <option value="">Selecione um método</option>
                                        <option value="DINHEIRO">Dinheiro</option>
                                        <option value="CARTAO_CREDITO">Cartão de Crédito</option>
                                        <option value="CARTAO_DEBITO">Cartão de Débito</option>
                                        <option value="BOLETO">Boleto Bancário</option>
                                        <option value="TRANSFERENCIA">Transferência</option>
                                        <option value="PIX">PIX</option>
                                        <option value="OUTRO">Outro</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3 data-pagamento-container" style="display: none;">
                            <label for="data_pagamento" class="form-label">Data de Pagamento</label>
                            <input type="date" name="data_pagamento" id="data_pagamento" class="form-control">
                        </div>
                        
                        <div class="d-flex justify-content-between">
                            <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">
                                <i class="fas fa-times"></i> Cancelar
                            </a>
                            <button type="submit" class="btn btn-primary" id="btn-salvar" disabled>
                                <i class="fas fa-save"></i> Salvar Pagamento
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="card mb-4">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">Informações</h5>
                </div>
                <div class="card-body">
                    <p>Preencha todos os campos obrigatórios para registrar um novo pagamento.</p>
                    <p>Primeiro, busque e selecione um aluno. Em seguida, preencha os detalhes do pagamento.</p>
                    <p>Se o status for "Pago", informe também a data de pagamento e o método utilizado.</p>
                    
                    <div class="alert alert-warning mt-3">
                        <i class="fas fa-exclamation-triangle"></i> Após salvar, você poderá editar os detalhes do pagamento, mas não poderá alterar o aluno associado.
                    </div>
                </div>
            </div>
            
            <div class="card mb-4" id="turmas-card" style="display: none;">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">Turmas do Aluno</h5>
                </div>
                <div class="card-body">
                    <div id="lista-turmas">
                        <!-- Turmas do aluno serão inseridas aqui -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const statusSelect = document.getElementById('status');
        const dataPagamentoContainer = document.querySelector('.data-pagamento-container');
        const metodoPagamentoContainer = document.querySelector('.metodo-pagamento-container');
        const alunoBusca = document.getElementById('aluno_busca');
        const btnBuscarAluno = document.getElementById('btn-buscar-aluno');
        const resultadosBusca = document.getElementById('resultados-busca');
        const listaAlunos = document.getElementById('lista-alunos');
        const alunoSelecionado = document.getElementById('aluno-selecionado');
        const alunoNome = document.getElementById('aluno-nome');
        const alunoCpf = document.getElementById('aluno-cpf');
        const alunoFoto = document.getElementById('aluno-foto');
        const alunoInicial = document.getElementById('aluno-inicial');
        const alunoIdInput = document.getElementById('aluno_id');
        const btnLimparAluno = document.getElementById('btn-limpar-aluno');
        const btnSalvar = document.getElementById('btn-salvar');
        const turmasCard = document.getElementById('turmas-card');
        const listaTurmas = document.getElementById('lista-turmas');
        
        // Função para mostrar/ocultar campos dependendo do status
        function toggleFields() {
            if (statusSelect.value === 'PAGO') {
                dataPagamentoContainer.style.display = 'block';
                metodoPagamentoContainer.style.display = 'block';
                document.getElementById('data_pagamento').required = true;
            } else {
                dataPagamentoContainer.style.display = 'none';
                metodoPagamentoContainer.style.display = 'none';
                document.getElementById('data_pagamento').required = false;
            }
        }
        
        // Executar ao carregar a página
        toggleFields();
        
        // Adicionar evento de mudança
        statusSelect.addEventListener('change', toggleFields);
        
        // Definir data de vencimento padrão como hoje
        const dataVencimentoInput = document.getElementById('data_vencimento');
        if (!dataVencimentoInput.value) {
            const hoje = new Date();
            const ano = hoje.getFullYear();
            const mes = String(hoje.getMonth() + 1).padStart(2, '0');
            const dia = String(hoje.getDate()).padStart(2, '0');
            dataVencimentoInput.value = `${ano}-${mes}-${dia}`;
        }
        
        // Buscar alunos
        function buscarAlunos() {
            const termo = alunoBusca.value.trim();
            if (termo.length < 2) return;
            
            listaAlunos.innerHTML = '<div class="list-group-item text-center"><i class="fas fa-spinner fa-spin"></i> Buscando...</div>';
            
            fetch(`/alunos/api/buscar/?termo=${encodeURIComponent(termo)}`)
                .then(response => response.json())
                .then(data => {
                    listaAlunos.innerHTML = '';
                    
                    if (data.success && data.alunos.length > 0) {
                        data.alunos.forEach(aluno => {
                            const item = document.createElement('a');
                            item.href = 'javascript:void(0)';
                            item.className = 'list-group-item list-group-item-action';
                            item.innerHTML = `
                                <div class="d-flex w-100 justify-content-between">
                                    <h6 class="mb-1">${aluno.nome}</h6>
                                    <small>CPF: ${aluno.cpf}</small>
                                </div>
                                <small>${aluno.email || 'Sem e-mail'}</small>
                            `;
                            item.addEventListener('click', () => selecionarAluno(aluno.cpf, aluno.nome, aluno.foto));
                            listaAlunos.appendChild(item);
                        });
                    } else {
                        listaAlunos.innerHTML = '<div class="list-group-item">Nenhum aluno encontrado</div>';
                    }
                    
                    resultadosBusca.style.display = 'block';
                })
                .catch(error => {
                    console.error('Erro ao buscar alunos:', error);
                    listaAlunos.innerHTML = '<div class="list-group-item text-danger">Erro ao buscar alunos</div>';
                    resultadosBusca.style.display = 'block';
                });
        }
        
        // Selecionar um aluno
        function selecionarAluno(cpf, nome, foto) {
            alunoIdInput.value = cpf;
            alunoNome.textContent = nome;
            alunoCpf.textContent = `CPF: ${cpf}`;
            
            if (foto) {
                alunoFoto.innerHTML = `<img src="${foto}" alt="Foto de ${nome}" style="width: 100%; height: 100%; object-fit: cover;">`;
            } else {
                alunoInicial.textContent = nome.charAt(0).toUpperCase();
                alunoFoto.innerHTML = `<span id="aluno-inicial">${nome.charAt(0).toUpperCase()}</span>`;
            }
            
            alunoSelecionado.style.display = 'block';
            resultadosBusca.style.display = 'none';
            alunoBusca.value = '';
            btnSalvar.disabled = false;
            
            // Buscar turmas do aluno
            buscarTurmasDoAluno(cpf);
        }
        
        // Buscar turmas do aluno
        function buscarTurmasDoAluno(cpf) {
            fetch(`/alunos/api/detalhes/${cpf}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.success && data.turmas && data.turmas.length > 0) {
                        listaTurmas.innerHTML = '';
                        
                        const ul = document.createElement('ul');
                        ul.className = 'list-group';
                        
                        data.turmas.forEach(turma => {
                            const li = document.createElement('li');
                            li.className = 'list-group-item d-flex justify-content-between align-items-center';
                            li.innerHTML = `
                                <div>
                                    <strong>${turma.curso}</strong>
                                    <div>${turma.nome}</div>
                                </div>
                            `;
                            ul.appendChild(li);
                        });
                        
                        listaTurmas.appendChild(ul);
                        turmasCard.style.display = 'block';
                    } else {
                        turmasCard.style.display = 'none';
                    }
                })
                .catch(error => {
                    console.error('Erro ao buscar turmas do aluno:', error);
                    turmasCard.style.display = 'none';
                });
        }
        
        // Limpar seleção de aluno
        function limparAluno() {
            alunoIdInput.value = '';
            alunoSelecionado.style.display = 'none';
            btnSalvar.disabled = true;
            turmasCard.style.display = 'none';
        }
        
        // Eventos
        alunoBusca.addEventListener('input', function() {
            if (this.value.trim().length >= 2) {
                buscarAlunos();
            } else {
                resultadosBusca.style.display = 'none';
            }
        });
        
        btnBuscarAluno.addEventListener('click', buscarAlunos);
        
        btnLimparAluno.addEventListener('click', limparAluno);
        
        // Validar formulário antes de enviar
        document.getElementById('pagamento-form').addEventListener('submit', function(e) {
            if (!alunoIdInput.value) {
                e.preventDefault();
                alert('Por favor, selecione um aluno.');
                return false;
            }
            
            if (statusSelect.value === 'PAGO') {
                const dataPagamento = document.getElementById('data_pagamento').value;
                const metodoPagamento = document.getElementById('metodo_pagamento').value;
                
                if (!dataPagamento) {
                    e.preventDefault();
                    alert('Por favor, informe a data de pagamento.');
                    return false;
                }
                
                if (!metodoPagamento) {
                    e.preventDefault();
                    alert('Por favor, selecione o método de pagamento.');
                    return false;
                }
            }
            
            return true;
        });
    });
</script>
{% endblock %}



### Arquivo: pagamentos\templates\pagamentos\dashboard.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Dashboard de Pagamentos{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Dashboard de Pagamentos</h1>
        <div>
            <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-primary">
                <i class="fas fa-list"></i> Listar Pagamentos
            </a>
            <a href="{% url 'pagamentos:criar_pagamento' %}" class="btn btn-success">
                <i class="fas fa-plus"></i> Novo Pagamento
            </a>
        </div>
    </div>

    <!-- Cards de estatísticas -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card bg-primary text-white">
                <div class="card-body">
                    <h5 class="card-title">Total de Alunos</h5>
                    <h2 class="display-4">{{ total_alunos }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-success text-white">
                <div class="card-body">
                    <h5 class="card-title">Pagamentos Pagos</h5>
                    <h2 class="display-4">{{ pagamentos_pagos }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-warning text-dark">
                <div class="card-body">
                    <h5 class="card-title">Pagamentos Pendentes</h5>
                    <h2 class="display-4">{{ pagamentos_pendentes }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-danger text-white">
                <div class="card-body">
                    <h5 class="card-title">Pagamentos Atrasados</h5>
                    <h2 class="display-4">{{ pagamentos_atrasados }}</h2>
                </div>
            </div>
        </div>
    </div>

    <!-- Cards de valores -->
    <div class="row mb-4">
        <div class="col-md-4">
            <div class="card border-success">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">Total Pago</h5>
                </div>
                <div class="card-body">
                    <h3 class="text-success">R$ {{ total_pago|floatformat:2 }}</h3>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card border-warning">
                <div class="card-header bg-warning text-dark">
                    <h5 class="mb-0">Total Pendente</h5>
                </div>
                <div class="card-body">
                    <h3 class="text-warning">R$ {{ total_pendente|floatformat:2 }}</h3>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card border-danger">
                <div class="card-header bg-danger text-white">
                    <h5 class="mb-0">Total Atrasado</h5>
                </div>
                <div class="card-body">
                    <h3 class="text-danger">R$ {{ total_atrasado|floatformat:2 }}</h3>
                </div>
            </div>
        </div>
    </div>

    <!-- Links para dashboards específicos -->
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Dashboards Específicos</h5>
                </div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <a href="{% url 'pagamentos:dashboard_pagamentos' %}" class="btn btn-outline-primary">
                            <i class="fas fa-chart-line"></i> Dashboard de Pagamentos
                        </a>
                        <a href="{% url 'pagamentos:dashboard_financeiro' %}" class="btn btn-outline-success">
                            <i class="fas fa-money-bill-wave"></i> Dashboard Financeiro
                        </a>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">Relatórios</h5>
                </div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <a href="{% url 'pagamentos:exportar_pagamentos_pdf' %}" class="btn btn-outline-danger">
                            <i class="fas fa-file-pdf"></i> Exportar Pagamentos (PDF)
                        </a>
                        <a href="{% url 'pagamentos:relatorio_financeiro' %}" class="btn btn-outline-info">
                            <i class="fas fa-chart-pie"></i> Relatório Financeiro
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <!-- Pagamentos recentes -->
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">Pagamentos Recentes</h5>
                </div>
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-striped mb-0">
                            <thead>
                                <tr>
                                    <th>Aluno</th>
                                    <th>Valor</th>
                                    <th>Data</th>
                                    <th>Ações</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for pagamento in pagamentos_recentes %}
                                <tr>
                                    <td>{{ pagamento.aluno.nome }}</td>
                                    <td>R$ {{ pagamento.valor_pago|default:pagamento.valor|floatformat:2 }}</td>
                                    <td>{{ pagamento.data_pagamento|date:"d/m/Y" }}</td>
                                    <td>
                                        <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i>
                                        </a>
                                    </td>
                                </tr>
                                {% empty %}
                                <tr>
                                    <td colspan="4" class="text-center">Nenhum pagamento recente encontrado.</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="card-footer">
                    <a href="{% url 'pagamentos:listar_pagamentos' %}?status=PAGO" class="btn btn-sm btn-outline-success">Ver todos os pagamentos</a>
                </div>
            </div>
        </div>

        <!-- Pagamentos próximos -->
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header bg-warning text-dark">
                    <h5 class="mb-0">Pagamentos Próximos (7 dias)</h5>
                </div>
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-striped mb-0">
                            <thead>
                                <tr>
                                    <th>Aluno</th>
                                    <th>Valor</th>
                                    <th>Vencimento</th>
                                    <th>Ações</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for pagamento in pagamentos_proximos %}
                                <tr>
                                    <td>{{ pagamento.aluno.nome }}</td>
                                    <td>R$ {{ pagamento.valor|floatformat:2 }}</td>
                                    <td>{{ pagamento.data_vencimento|date:"d/m/Y" }}</td>
                                    <td>
                                        <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i>
                                        </a>
                                    </td>
                                </tr>
                                {% empty %}
                                <tr>
                                    <td colspan="4" class="text-center">Nenhum pagamento próximo encontrado.</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="card-footer">
                    <a href="{% url 'pagamentos:listar_pagamentos' %}?status=PENDENTE" class="btn btn-sm btn-outline-warning">Ver todos os pagamentos pendentes</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Gráfico de pagamentos por mês
        const ctxMes = document.getElementById('pagamentosPorMes').getContext('2d');
        new Chart(ctxMes, {
            type: 'bar',
            data: {
                labels: [{% for item in pagamentos_por_mes %}'{{ item.mes }}',{% endfor %}],
                datasets: [{
                    label: 'Valor Total',
                    data: [{% for item in pagamentos_por_mes %}{{ item.total }},{% endfor %}],
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgb(54, 162, 235)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return 'R$ ' + value.toFixed(2);
                            }
                        }
                    }
                }
            }
        });
        
        // Gráfico de pagamentos por status
        const ctxStatus = document.getElementById('pagamentosPorStatus').getContext('2d');
        new Chart(ctxStatus, {
            type: 'pie',
            data: {
                labels: ['Pago', 'Pendente', 'Cancelado'],
                datasets: [{
                    data: [{{ total_pago }}, {{ total_pendente }}, {{ total_cancelado }}],
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(255, 205, 86, 0.6)',
                        'rgba(201, 203, 207, 0.6)'
                    ],
                    borderColor: [
                        'rgb(75, 192, 192)',
                        'rgb(255, 205, 86)',
                        'rgb(201, 203, 207)'
                    ],
                    borderWidth: 1
                }]
            }
        });
    });
</script>
{% endblock %}



### Arquivo: pagamentos\templates\pagamentos\dashboard_financeiro.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Dashboard Financeiro{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.css">
{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Cabeçalho com botões de ação -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Dashboard Financeiro</h1>
        <div>
            <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary me-2">
                <i class="fas fa-list"></i> Lista de Pagamentos
            </a>
            <a href="{% url 'pagamentos:criar_pagamento' %}" class="btn btn-success">
                <i class="fas fa-plus"></i> Novo Pagamento
            </a>
        </div>
    </div>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-4">
                    <label for="ano" class="form-label">Ano</label>
                    <select class="form-select" id="ano" name="ano">
                        {% for ano_opcao in anos_disponiveis %}
                        <option value="{{ ano_opcao }}" {% if ano_opcao == ano_selecionado %}selected{% endif %}>{{ ano_opcao }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-4">
                    <label for="curso" class="form-label">Curso</label>
                    <select class="form-select" id="curso" name="curso">
                        <option value="">Todos os cursos</option>
                        {% for curso in cursos %}
                        <option value="{{ curso.id }}" {% if curso.id|stringformat:"s" == filtros.curso %}selected{% endif %}>{{ curso.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-4">
                    <label for="tipo" class="form-label">Tipo de Pagamento</label>
                    <select class="form-select" id="tipo" name="tipo">
                        <option value="">Todos os tipos</option>
                        <option value="MENSALIDADE" {% if filtros.tipo == 'MENSALIDADE' %}selected{% endif %}>Mensalidade</option>
                        <option value="MATRICULA" {% if filtros.tipo == 'MATRICULA' %}selected{% endif %}>Matrícula</option>
                        <option value="MATERIAL" {% if filtros.tipo == 'MATERIAL' %}selected{% endif %}>Material</option>
                        <option value="OUTRO" {% if filtros.tipo == 'OUTRO' %}selected{% endif %}>Outro</option>
                    </select>
                </div>
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                    <a href="{% url 'pagamentos:dashboard' %}" class="btn btn-secondary">
                        <i class="fas fa-undo"></i> Limpar Filtros
                    </a>
                    <a href="{% url 'pagamentos:exportar_relatorio_pdf' %}{{ request.GET.urlencode }}" class="btn btn-danger float-end">
                        <i class="fas fa-file-pdf"></i> Exportar Relatório
                    </a>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Resumo financeiro -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card bg-success text-white h-100">
                <div class="card-body">
                    <h5 class="card-title">Receita Total</h5>
                    <h2>R$ {{ resumo.receita_total|floatformat:2 }}</h2>
                    <p class="mb-0">{{ resumo.total_pagos }} pagamentos</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-warning text-dark h-100">
                <div class="card-body">
                    <h5 class="card-title">Pendente</h5>
                    <h2>R$ {{ resumo.valor_pendente|floatformat:2 }}</h2>
                    <p class="mb-0">{{ resumo.total_pendentes }} pagamentos</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-danger text-white h-100">
                <div class="card-body">
                    <h5 class="card-title">Atrasado</h5>
                    <h2>R$ {{ resumo.valor_atrasado|floatformat:2 }}</h2>
                    <p class="mb-0">{{ resumo.total_atrasados }} pagamentos</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-info text-white h-100">
                <div class="card-body">
                    <h5 class="card-title">Previsão Mensal</h5>
                    <h2>R$ {{ resumo.previsao_mensal|floatformat:2 }}</h2>
                    <p class="mb-0">Média dos últimos 3 meses</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Gráficos financeiros -->
    <div class="row">
        <!-- Gráfico de receita mensal -->
        <div class="col-md-8">
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Receita Mensal ({{ ano_selecionado }})</h5>
                </div>
                <div class="card-body">
                    <canvas id="graficoReceitaMensal" height="300"></canvas>
                </div>
            </div>
        </div>
        
        <!-- Gráfico de distribuição por status -->
        <div class="col-md-4">
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Distribuição por Status</h5>
                </div>
                <div class="card-body">
                    <canvas id="graficoDistribuicaoStatus" height="300"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row">
        <!-- Gráfico de distribuição por tipo -->
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Distribuição por Tipo</h5>
                </div>
                <div class="card-body">
                    <canvas id="graficoDistribuicaoTipo" height="300"></canvas>
                </div>
            </div>
        </div>
        
        <!-- Gráfico de distribuição por curso -->
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Distribuição por Curso</h5>
                </div>
                <div class="card-body">
                    <canvas id="graficoDistribuicaoCurso" height="300"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Pagamentos recentes -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Pagamentos Recentes</h5>
        </div>
        <div class="card-body">
            {% if pagamentos_recentes %}
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Data</th>
                            <th>Aluno</th>
                            <th>Descrição</th>
                            <th>Valor</th>
                            <th>Status</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for pagamento in pagamentos_recentes %}
                        <tr>
                            <td>{{ pagamento.data_vencimento|date:"d/m/Y" }}</td>
                            <td>{{ pagamento.aluno.nome }}</td>
                            <td>{{ pagamento.descricao|truncatechars:30 }}</td>
                            <td>R$ {{ pagamento.valor|floatformat:2 }}</td>
                            <td>
                                <span class="badge 
                                    {% if pagamento.status == 'PAGO' %}bg-success
                                    {% elif pagamento.status == 'PENDENTE' %}bg-warning
                                    {% elif pagamento.status == 'ATRASADO' %}bg-danger
                                    {% else %}bg-secondary{% endif %}">
                                    {{ pagamento.get_status_display }}
                                </span>
                            </td>
                            <td>
                                <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-sm btn-info">
                                    <i class="fas fa-eye"></i>
                                </a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            <div class="text-end mt-3">
                <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-outline-primary">
                    Ver todos os pagamentos
                </a>
            </div>
            {% else %}
            <div class="alert alert-info">
                <i class="fas fa-info-circle"></i> Não há pagamentos recentes para exibir.
            </div>
            {% endif %}
        </div>
    </div>
    
    <!-- Pagamentos atrasados -->
    <div class="card mb-4">
        <div class="card-header bg-danger text-white">
            <h5 class="mb-0">Pagamentos Atrasados</h5>
        </div>
        <div class="card-body">
            {% if pagamentos_atrasados %}
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Vencimento</th>
                            <th>Aluno</th>
                            <th>Descrição</th>
                            <th>Valor</th>
                            <th>Dias Atrasados</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for pagamento in pagamentos_atrasados %}
                        <tr>
                            <td>{{ pagamento.data_vencimento|date:"d/m/Y" }}</td>
                            <td>{{ pagamento.aluno.nome }}</td>
                            <td>{{ pagamento.descricao|truncatechars:30 }}</td>
                            <td>R$ {{ pagamento.valor|floatformat:2 }}</td>
                            <td>{{ pagamento.dias_atrasados }}</td>
                            <td>
                                <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-sm btn-info">
                                    <i class="fas fa-eye"></i>
                                </a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="alert alert-info">
                <i class="fas fa-info-circle"></i> Não há pagamentos atrasados para exibir.
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.js"></script>
<script>
    // Gráfico de receita mensal
    const ctxReceita = document.getElementById('graficoReceitaMensal').getContext('2d');
    const graficoReceitaMensal = new Chart(ctxReceita, {
        type: 'bar',
        data: {
            labels: {{ meses|safe }},
            datasets: [{
                label: 'Receita Mensal (R$)',
                data: {{ valores_mensais|safe }},
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Receita Mensal do Ano de {{ ano_selecionado }}'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return 'R$ ' + value.toFixed(2);
                        }
                    }
                }
            }
        }
    });

    // Gráfico de distribuição por status
    const ctxStatus = document.getElementById('graficoDistribuicaoStatus').getContext('2d');
    const graficoDistribuicaoStatus = new Chart(ctxStatus, {
        type: 'pie',
        data: {
            labels: ['Pago', 'Pendente', 'Atrasado'],
            datasets: [{
                data: [{{ resumo.total_pagos }}, {{ resumo.total_pendentes }}, {{ resumo.total_atrasados }}],
                backgroundColor: [
                    'rgba(40, 167, 69, 0.7)',
                    'rgba(255, 193, 7, 0.7)',
                    'rgba(220, 53, 69, 0.7)'
                ],
                borderColor: [
                    'rgba(40, 167, 69, 1)',
                    'rgba(255, 193, 7, 1)',
                    'rgba(220, 53, 69, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: 'Distribuição de Pagamentos por Status'
                }
            }
        }
    });

    // Gráfico de distribuição por tipo
    const ctxTipo = document.getElementById('graficoDistribuicaoTipo').getContext('2d');
    const graficoDistribuicaoTipo = new Chart(ctxTipo, {
        type: 'pie',
        data: {
            labels: ['Mensalidade', 'Matrícula', 'Material', 'Outro'],
            datasets: [{
                data: [{{ resumo.mensalidades }}, {{ resumo.matriculas }}, {{ resumo.materiais }}, {{ resumo.outros }}],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: 'Distribuição de Pagamentos por Tipo'
                }
            }
        }
    });

    // Gráfico de distribuição por curso
    const ctxCurso = document.getElementById('graficoDistribuicaoCurso').getContext('2d');
    const graficoDistribuicaoCurso = new Chart(ctxCurso, {
        type: 'pie',
        data: {
            labels: {{ cursos_nomes|safe }},
            datasets: [{
                data: {{ cursos_valores|safe }},
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(153, 102, 255, 0.7)',
                    'rgba(255, 159, 64, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: 'Distribuição de Pagamentos por Curso'
                }
            }
        }
    });
</script>
{% endblock %}




### Arquivo: pagamentos\templates\pagamentos\dashboard_pagamentos.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Dashboard de Pagamentos{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.css">
{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Dashboard de Pagamentos</h1>
        <div>
            <a href="{% url 'pagamentos:dashboard' %}" class="btn btn-secondary me-2">
                <i class="fas fa-tachometer-alt"></i> Dashboard Principal
            </a>
            <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-primary">
                <i class="fas fa-list"></i> Listar Pagamentos
            </a>
        </div>
    </div>

    <!-- Estatísticas do mês atual -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Estatísticas do Mês ({{ mes_atual }})</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-4">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Pagamentos Pagos</h5>
                            <p class="card-text display-4 text-success">{{ pagos_mes }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Pagamentos Pendentes</h5>
                            <p class="card-text display-4 text-warning">{{ pendentes_mes }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Pagamentos Atrasados</h5>
                            <p class="card-text display-4 text-danger">{{ atrasados_mes }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row mt-3">
                <div class="col-md-4">
                    <div class="card border-success">
                        <div class="card-header bg-success text-white">
                            <h5 class="mb-0">Valor Pago</h5>
                        </div>
                        <div class="card-body">
                            <h3 class="text-success">R$ {{ valor_pago_mes|floatformat:2 }}</h3>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card border-warning">
                        <div class="card-header bg-warning text-dark">
                            <h5 class="mb-0">Valor Pendente</h5>
                        </div>
                        <div class="card-body">
                            <h3 class="text-warning">R$ {{ valor_pendente_mes|floatformat:2 }}</h3>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card border-danger">
                        <div class="card-header bg-danger text-white">
                            <h5 class="mb-0">Valor Atrasado</h5>
                        </div>
                        <div class="card-body">
                            <h3 class="text-danger">R$ {{ valor_atrasado_mes|floatformat:2 }}</h3>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Resumo estatístico -->
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="card bg-primary text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Total de Pagamentos</h5>
                    <p class="card-text display-6">{{ total_pagamentos }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card bg-success text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Valor Total</h5>
                    <p class="card-text display-6">R$ {{ valor_total|floatformat:2 }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Pagamentos por status -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Pagamentos por Status</h5>
        </div>
        <div class="card-body">
            {% if pagamentos_por_status %}
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Status</th>
                                <th>Quantidade</th>
                                <th>Valor Total</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for item in pagamentos_por_status %}
                                <tr>
                                    <td>
                                        <span class="badge {% if item.status == 'pago' %}bg-success{% elif item.status == 'pendente' %}bg-warning{% else %}bg-danger{% endif %}">
                                            {% if item.status == 'pago' %}Pago{% elif item.status == 'pendente' %}Pendente{% else %}Cancelado{% endif %}
                                        </span>
                                    </td>
                                    <td>{{ item.total }}</td>
                                    <td>R$ {{ item.valor_total|floatformat:2 }}</td>
                                    <td>
                                        <a href="{% url 'pagamentos:listar_pagamentos' %}?status={{ item.status }}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i> Ver Pagamentos
                                        </a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> Nenhum pagamento encontrado.
                </div>
            {% endif %}
        </div>
    </div>
    
    <!-- Pagamentos por mês -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Pagamentos por Mês (Últimos 6 meses)</h5>
        </div>
        <div class="card-body">
            {% if pagamentos_por_mes %}
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Mês</th>
                                <th>Quantidade</th>
                                <th>Valor Total</th>
                                <th>Média por Pagamento</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for item in pagamentos_por_mes %}
                                <tr>
                                    <td>{{ item.mes }}</td>
                                    <td>{{ item.total }}</td>
                                    <td>R$ {{ item.valor_total|floatformat:2 }}</td>
                                    <td>
                                        {% if item.total > 0 %}
                                            R$ {{ item.valor_total|floatformat:2|default:0|divisibleby:item.total }}
                                        {% else %}
                                            R$ 0,00
                                        {% endif %}
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> Nenhum pagamento encontrado nos últimos 6 meses.
                </div>
            {% endif %}
        </div>
    </div>

    <!-- Pagamentos por aluno -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Top 5 Alunos por Valor Total</h5>
        </div>
        <div class="card-body">
            {% if pagamentos_por_aluno %}
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Aluno</th>
                                <th>Quantidade de Pagamentos</th>
                                <th>Valor Total</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for item in pagamentos_por_aluno %}
                                <tr>
                                    <td>{{ item.aluno__nome }}</td>
                                    <td>{{ item.total }}</td>
                                    <td>R$ {{ item.valor_total|floatformat:2 }}</td>
                                    <td>
                                        <a href="{% url 'pagamentos:listar_pagamentos' %}?aluno={{ item.aluno__cpf }}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i> Ver Pagamentos
                                        </a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> Nenhum pagamento encontrado.
                </div>
            {% endif %}
        </div>
    </div>

    <!-- Gráficos -->
    <div class="row">
        <!-- Gráfico de pagamentos por dia -->
        <div class="col-md-8">
            <div class="card mb-4">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">Pagamentos por Dia ({{ mes_atual }})</h5>
                </div>
                <div class="card-body">
                    <canvas id="grafico-pagamentos-dia" height="300"></canvas>
                </div>
            </div>
        </div>

        <!-- Gráfico de métodos de pagamento -->
        <div class="col-md-4">
            <div class="card mb-4">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">Métodos de Pagamento</h5>
                </div>
                <div class="card-body">
                    <canvas id="grafico-metodos-pagamento" height="300"></canvas>
                </div>
            </div>
        </div>
    </div>

    <!-- Pagamentos atrasados por faixa -->
    <div class="card mb-4">
        <div class="card-header bg-danger text-white">
            <h5 class="mb-0">Pagamentos Atrasados por Faixa</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-4">
                    <div class="card text-center">
                        <div class="card-body">
                            <h5 class="card-title">Até 15 dias</h5>
                            <p class="card-text display-4 text-warning">{{ atrasados_ate_15 }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center">
                        <div class="card-body">
                            <h5 class="card-title">15 a 30 dias</h5>
                            <p class="card-text display-4 text-danger">{{ atrasados_15_30 }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center">
                        <div class="card-body">
                            <h5 class="card-title">Mais de 30 dias</h5>
                            <p class="card-text display-4 text-danger">{{ atrasados_mais_30 }}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="mt-3 text-center">
                <a href="{% url 'pagamentos:listar_pagamentos' %}?status=ATRASADO" class="btn btn-outline-danger">
                    <i class="fas fa-exclamation-triangle"></i> Ver Todos os Pagamentos Atrasados
                </a>
            </div>
        </div>
    </div>

    <div class="mt-4">
        <a href="javascript:history.back()" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.js"></script>
<script>
    // Gráfico de pagamentos por dia
    const ctxDia = document.getElementById('grafico-pagamentos-dia').getContext('2d');
    const graficoPagamentosDia = new Chart(ctxDia, {
        type: 'line',
        data: {
            labels: {{ dias|safe }},
            datasets: [{
                label: 'Valor Pago (R$)',
                data: {{ valores_por_dia|safe }},
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 2,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Pagamentos Recebidos por Dia'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return 'R$ ' + value.toFixed(2);
                        }
                    }
                }
            }
        }
    });

    // Gráfico de métodos de pagamento
    const ctxMetodos = document.getElementById('grafico-metodos-pagamento').getContext('2d');
    const graficoMetodosPagamento = new Chart(ctxMetodos, {
        type: 'doughnut',
        data: {
            labels: {{ metodos|safe }},
            datasets: [{
                data: {{ contagens|safe }},
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(153, 102, 255, 0.7)',
                    'rgba(255, 159, 64, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: 'Métodos de Pagamento'
                }
            }
        }
    });
</script>
{% endblock %}



### Arquivo: pagamentos\templates\pagamentos\detalhar_pagamento.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Detalhes do Pagamento{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Detalhes do Pagamento</h1>
        <div>
            <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'pagamentos:editar_pagamento' pagamento.id %}" class="btn btn-warning">
                <i class="fas fa-edit"></i> Editar
            </a>
            <a href="{% url 'pagamentos:excluir_pagamento' pagamento.id %}" class="btn btn-danger">
                <i class="fas fa-trash"></i> Excluir
            </a>
        </div>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Informações do Pagamento</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <h6>Aluno</h6>
                    <p>
                        <a href="{% url 'alunos:detalhar_aluno' pagamento.aluno.cpf %}">
                            {{ pagamento.aluno.nome }}
                        </a>
                    </p>
                    
                    <h6>Valor</h6>
                    <p>R$ {{ pagamento.valor|floatformat:2 }}</p>
                    
                    <h6>Data de Vencimento</h6>
                    <p>{{ pagamento.data_vencimento|date:"d/m/Y" }}</p>
                    
                    <h6>Descrição</h6>
                    <p>{{ pagamento.descricao }}</p>
                    
                    <h6>Tipo</h6>
                    <p>{{ pagamento.get_tipo_display }}</p>
                </div>
                <div class="col-md-6">
                    <h6>Status</h6>
                    <p>
                        {% if pagamento.status == 'PAGO' %}
                            <span class="badge bg-success">{{ pagamento.get_status_display }}</span>
                        {% elif pagamento.status == 'PENDENTE' %}
                            <span class="badge bg-warning">{{ pagamento.get_status_display }}</span>
                        {% elif pagamento.status == 'ATRASADO' %}
                            <span class="badge bg-danger">{{ pagamento.get_status_display }}</span>
                        {% else %}
                            <span class="badge bg-secondary">{{ pagamento.get_status_display }}</span>
                        {% endif %}
                    </p>
                    
                    {% if pagamento.status == 'PAGO' %}
                        <h6>Data de Pagamento</h6>
                        <p>{{ pagamento.data_pagamento|date:"d/m/Y" }}</p>
                        
                        <h6>Valor Pago</h6>
                        <p>R$ {{ pagamento.valor_pago|floatformat:2 }}</p>
                        
                        <h6>Método de Pagamento</h6>
                        <p>{{ pagamento.get_metodo_pagamento_display }}</p>
                        
                        {% if pagamento.comprovante %}
                            <h6>Comprovante</h6>
                            <p>
                                <a href="{{ pagamento.comprovante.url }}" target="_blank" class="btn btn-sm btn-info">
                                    <i class="fas fa-file-download"></i> Visualizar Comprovante
                                </a>
                            </p>
                        {% endif %}
                    {% else %}
                        <div class="alert alert-info">
                            <h6 class="mb-2">Ações Disponíveis</h6>
                            <a href="{% url 'pagamentos:registrar_pagamento' pagamento.id %}" class="btn btn-success">
                                <i class="fas fa-check-circle"></i> Registrar Pagamento
                            </a>
                        </div>
                    {% endif %}
                </div>
            </div>
            
            {% if pagamento.observacoes %}
                <div class="mt-3">
                    <h6>Observações</h6>
                    <div class="p-3 bg-light rounded">
                        {{ pagamento.observacoes|linebreaks }}
                    </div>
                </div>
            {% endif %}
            
            {% if pagamento.matricula %}
                <div class="mt-3">
                    <h6>Matrícula Associada</h6>
                    <div class="p-3 bg-light rounded">
                        <p><strong>Curso:</strong> {{ pagamento.matricula.turma.curso.nome }}</p>
                        <p><strong>Turma:</strong> {{ pagamento.matricula.turma.nome }}</p>
                        {% if pagamento.numero_parcela %}
                            <p><strong>Parcela:</strong> {{ pagamento.numero_parcela }} de {{ pagamento.total_parcelas }}</p>
                        {% endif %}
                    </div>
                </div>
            {% endif %}
        </div>
        <div class="card-footer text-muted">
            <small>Criado em: {{ pagamento.created_at|date:"d/m/Y H:i" }}</small>
            <br>
            <small>Última atualização: {{ pagamento.updated_at|date:"d/m/Y H:i" }}</small>
        </div>
    </div>
    
    {% if pagamentos_relacionados %}
        <div class="card mb-4">
            <div class="card-header">
                <h5 class="mb-0">Pagamentos Relacionados</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Descrição</th>
                                <th>Valor</th>
                                <th>Vencimento</th>
                                <th>Status</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for pag in pagamentos_relacionados %}
                                <tr>
                                    <td>
                                        {{ pag.descricao }}
                                        {% if pag.numero_parcela %}
                                            <br><small>Parcela {{ pag.numero_parcela }}/{{ pag.total_parcelas }}</small>
                                        {% endif %}
                                    </td>
                                    <td>R$ {{ pag.valor|floatformat:2 }}</td>
                                    <td>{{ pag.data_vencimento|date:"d/m/Y" }}</td>
                                    <td>
                                        {% if pag.status == 'PAGO' %}
                                            <span class="badge bg-success">Pago</span>
                                            {% if pag.data_pagamento %}
                                                <br><small>em {{ pag.data_pagamento|date:"d/m/Y" }}</small>
                                            {% endif %}
                                        {% elif pag.status == 'PENDENTE' %}
                                            <span class="badge bg-warning text-dark">Pendente</span>
                                        {% elif pag.status == 'ATRASADO' %}
                                            <span class="badge bg-danger">Atrasado</span>
                                        {% elif pag.status == 'CANCELADO' %}
                                            <span class="badge bg-secondary">Cancelado</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        <a href="{% url 'pagamentos:detalhar_pagamento' pag.id %}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i>
                                        </a>
                                        {% if pag.status == 'PENDENTE' or pag.status == 'ATRASADO' %}
                                            <a href="{% url 'pagamentos:registrar_pagamento' pag.id %}" class="btn btn-sm btn-success">
                                                <i class="fas fa-check"></i>
                                            </a>
                                        {% endif %}
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    {% endif %}
    
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">Histórico de Alterações</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Data</th>
                            <th>Usuário</th>
                            <th>Ação</th>
                            <th>Detalhes</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for log in historico %}
                            <tr>
                                <td>{{ log.timestamp|date:"d/m/Y H:i" }}</td>
                                <td>{{ log.usuario.username }}</td>
                                <td>{{ log.get_acao_display }}</td>
                                <td>{{ log.detalhes }}</td>
                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="4" class="text-center">Nenhum registro de alteração encontrado.</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}{% extends 'base.html' %}
{% load static %}

{% block title %}Detalhes do Pagamento{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Detalhes do Pagamento</h1>
        <div>
            <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'pagamentos:editar_pagamento' pagamento.id %}" class="btn btn-warning">
                <i class="fas fa-edit"></i> Editar
            </a>
            <a href="{% url 'pagamentos:excluir_pagamento' pagamento.id %}" class="btn btn-danger">
                <i class="fas fa-trash"></i> Excluir
            </a>
        </div>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Informações do Pagamento</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <h6>Aluno</h6>
                    <p>
                        <a href="{% url 'alunos:detalhar_aluno' pagamento.aluno.cpf %}">
                            {{ pagamento.aluno.nome }}
                        </a>
                    </p>
                    
                    <h6>Valor</h6>
                    <p>R$ {{ pagamento.valor|floatformat:2 }}</p>
                    
                    <h6>Data de Vencimento</h6>
                    <p>{{ pagamento.data_vencimento|date:"d/m/Y" }}</p>
                    
                    <h6>Descrição</h6>
                    <p>{{ pagamento.descricao }}</p>
                    
                    <h6>Tipo</h6>
                    <p>{{ pagamento.get_tipo_display }}</p>
                </div>
                <div class="col-md-6">
                    <h6>Status</h6>
                    <p>
                        {% if pagamento.status == 'PAGO' %}
                            <span class="badge bg-success">{{ pagamento.get_status_display }}</span>
                        {% elif pagamento.status == 'PENDENTE' %}
                            <span class="badge bg-warning">{{ pagamento.get_status_display }}</span>
                        {% elif pagamento.status == 'ATRASADO' %}
                            <span class="badge bg-danger">{{ pagamento.get_status_display }}</span>
                        {% else %}
                            <span class="badge bg-secondary">{{ pagamento.get_status_display }}</span>
                        {% endif %}
                    </p>
                    
                    {% if pagamento.status == 'PAGO' %}
                        <h6>Data de Pagamento</h6>
                        <p>{{ pagamento.data_pagamento|date:"d/m/Y" }}</p>
                        
                        <h6>Valor Pago</h6>
                        <p>R$ {{ pagamento.valor_pago|floatformat:2 }}</p>
                        
                        <h6>Método de Pagamento</h6>
                        <p>{{ pagamento.get_metodo_pagamento_display }}</p>
                        
                        {% if pagamento.comprovante %}
                            <h6>Comprovante</h6>
                            <p>
                                <a href="{{ pagamento.comprovante.url }}" target="_blank" class="btn btn-sm btn-info">
                                    <i class="fas fa-file-download"></i> Visualizar Comprovante
                                </a>
                            </p>
                        {% endif %}
                    {% else %}
                        <div class="alert alert-info">
                            <h6 class="mb-2">Ações Disponíveis</h6>
                            <a href="{% url 'pagamentos:registrar_pagamento' pagamento.id %}" class="btn btn-success">
                                <i class="fas fa-check-circle"></i> Registrar Pagamento
                            </a>
                        </div>
                    {% endif %}
                </div>
            </div>
            
            {% if pagamento.observacoes %}
                <div class="mt-3">
                    <h6>Observações</h6>
                    <div class="p-3 bg-light rounded">
                        {{ pagamento.observacoes|linebreaks }}
                    </div>
                </div>
            {% endif %}
            
            {% if pagamento.matricula %}
                <div class="mt-3">
                    <h6>Matrícula Associada</h6>
                    <div class="p-3 bg-light rounded">
                        <p><strong>Curso:</strong> {{ pagamento.matricula.turma.curso.nome }}</p>
                        <p><strong>Turma:</strong> {{ pagamento.matricula.turma.nome }}</p>
                        {% if pagamento.numero_parcela %}
                            <p><strong>Parcela:</strong> {{ pagamento.numero_parcela }} de {{ pagamento.total_parcelas }}</p>
                        {% endif %}
                    </div>
                </div>
            {% endif %}
        </div>
        <div class="card-footer text-muted">
            <small>Criado em: {{ pagamento.created_at|date:"d/m/Y H:i" }}</small>
            <br>
            <small>Última atualização: {{ pagamento.updated_at|date:"d/m/Y H:i" }}</small>
        </div>
    </div>
    
    {% if pagamentos_relacionados %}
        <div class="card mb-4">
            <div class="card-header">
                <h5 class="mb-0">Pagamentos Relacionados</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Descrição</th>
                                <th>Valor</th>
                                <th>Vencimento</th>
                                <th>Status</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for pag in pagamentos_relacionados %}
                                <tr>
                                    <td>
                                        {{ pag.descricao }}
                                        {% if pag.numero_parcela %}
                                            <br><small>Parcela {{ pag.numero_parcela }}/{{ pag.total_parcelas }}</small>
                                        {% endif %}
                                    </td>
                                    <td>R$ {{ pag.valor|floatformat:2 }}</td>
                                    <td>{{ pag.data_vencimento|date:"d/m/Y" }}</td>
                                    <td>
                                        {% if pag.status == 'PAGO' %}
                                            <span class="badge bg-success">Pago</span>
                                            {% if pag.data_pagamento %}
                                                <br><small>em {{ pag.data_pagamento|date:"d/m/Y" }}</small>
                                            {% endif %}
                                        {% elif pag.status == 'PENDENTE' %}
                                            <span class="badge bg-warning text-dark">Pendente</span>
                                        {% elif pag.status == 'ATRASADO' %}
                                            <span class="badge bg-danger">Atrasado</span>
                                        {% elif pag.status == 'CANCELADO' %}
                                            <span class="badge bg-secondary">Cancelado</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        <a href="{% url 'pagamentos:detalhar_pagamento' pag.id %}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i>
                                        </a>
                                        {% if pag.status == 'PENDENTE' or pag.status == 'ATRASADO' %}
                                            <a href="{% url 'pagamentos:registrar_pagamento' pag.id %}" class="btn btn-sm btn-success">
                                                <i class="fas fa-check"></i>
                                            </a>
                                        {% endif %}
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    {% endif %}
    
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">Histórico de Alterações</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Data</th>
                            <th>Usuário</th>
                            <th>Ação</th>
                            <th>Detalhes</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for log in historico %}
                            <tr>
                                <td>{{ log.timestamp|date:"d/m/Y H:i" }}</td>
                                <td>{{ log.usuario.username }}</td>
                                <td>{{ log.get_acao_display }}</td>
                                <td>{{ log.detalhes }}</td>
                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="4" class="text-center">Nenhum registro de alteração encontrado.</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}


'''