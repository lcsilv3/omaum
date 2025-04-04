from django import forms
from importlib import import_module

def get_punicao_model():
    punicoes_module = import_module('punicoes.models')
    return getattr(punicoes_module, 'Punicao')

def get_tipo_punicao_model():
    punicoes_module = import_module('punicoes.models')
    return getattr(punicoes_module, 'TipoPunicao')

class PunicaoForm(forms.ModelForm):
    class Meta:
        model = get_punicao_model()
        fields = ['aluno', 'tipo_punicao', 'data_aplicacao', 'motivo', 'observacoes']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-control'}),
            'tipo_punicao': forms.Select(attrs={'class': 'form-control'}),
            'data_aplicacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TipoPunicaoForm(forms.ModelForm):
    class Meta:
        model = get_model('punicoes', 'TipoPunicao')
        fields = ['nome', 'descricao', 'gravidade']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }