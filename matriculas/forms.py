"""
Formulários para o aplicativo de Matrículas.
"""

from django import forms
from django.core.exceptions import ValidationError
from importlib import import_module
from .models import Matricula


def get_aluno_model():
    """Obtém o modelo Aluno."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


class MatriculaForm(forms.ModelForm):
    """Formulário para criação e edição de matrículas."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        Aluno = get_aluno_model()
        Turma = get_turma_model()
        
        # Configurar campos
        self.fields['aluno'].queryset = Aluno.objects.filter(ativo=True)
        self.fields['turma'].queryset = Turma.objects.filter(
            ativo=True,
            status='A'
        )
        
        # Adicionar classes CSS
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })
        
        # Configurações específicas
        self.fields['data_matricula'].widget = forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        )
        
        self.fields['aluno'].widget.attrs.update({
            'class': 'form-control select2'
        })
        
        self.fields['turma'].widget.attrs.update({
            'class': 'form-control select2'
        })

    class Meta:
        model = Matricula
        fields = ['aluno', 'turma', 'data_matricula', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        aluno = cleaned_data.get('aluno')
        turma = cleaned_data.get('turma')
        
        if aluno and turma:
            # Verificar se já existe matrícula ativa para este aluno na turma
            existing = Matricula.objects.filter(
                aluno=aluno,
                turma=turma,
                status='A'
            )
            
            # Excluir a própria instância se estiver editando
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise ValidationError(
                    'Este aluno já possui uma matrícula ativa nesta turma.'
                )
        
        return cleaned_data


class FiltroMatriculaForm(forms.Form):
    """Formulário para filtros na listagem de matrículas."""
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nome do aluno ou turma...'
        })
    )
    
    status = forms.ChoiceField(
        choices=[('', 'Todos')] + Matricula.OPCOES_STATUS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        Turma = get_turma_model()
        turmas_choices = [('', 'Todas as turmas')]
        turmas_choices.extend([
            (turma.id, turma.nome)
            for turma in Turma.objects.filter(ativo=True).order_by('nome')
        ])
        
        self.fields['turma'] = forms.ChoiceField(
            choices=turmas_choices,
            required=False,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
