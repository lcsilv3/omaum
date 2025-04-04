print("ARQUIVO FORMS.PY CARREGADO")
from django import forms
from importlib import import_module
# resto do código...

def get_atividade_academica_model():
    try:
        atividades_module = import_module('atividades.models')
        return getattr(atividades_module, 'AtividadeAcademica')
    except (ImportError, AttributeError):
        return None

def get_atividade_ritualistica_model():
    try:
        atividades_module = import_module('atividades.models')
        return getattr(atividades_module, 'AtividadeRitualistica')
    except (ImportError, AttributeError):
        return None

class AtividadeAcademicaForm(forms.ModelForm):
    class Meta:
        model = get_atividade_academica_model()
        fields = ['nome', 'descricao', 'data_inicio', 'data_fim', 'turma']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'turma': forms.Select(attrs={'class': 'form-control'}),
        }

class AtividadeRitualisticaForm(forms.ModelForm):
    todos_alunos = forms.BooleanField(
        required=False, 
        label="Incluir todos os alunos da turma",
        initial=False
    )
    
    class Meta:
        model = get_atividade_ritualistica_model()
        fields = ['nome', 'descricao', 'data', 'hora_inicio', 'hora_fim', 'local', 'turma', 'participantes']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fim': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
            'turma': forms.Select(attrs={'class': 'form-control'}),
            'participantes': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
def criar_form_atividade_academica():
    return AtividadeAcademicaForm
def criar_form_atividade_ritualistica():
    return AtividadeRitualisticaForm
