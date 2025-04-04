from django import forms
from importlib import import_module

def get_curso_model():
    cursos_module = import_module('cursos.models')
    return getattr(cursos_module, 'Curso')

class CursoForm(forms.ModelForm):
    class Meta:
        model = get_curso_model()
        fields = ['codigo_curso', 'nome', 'descricao', 'duracao']
        widgets = {
            'codigo_curso': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'duracao': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
        }
        
    def clean_codigo_curso(self):
        codigo = self.cleaned_data.get('codigo_curso')
        if codigo <= 0:
            raise forms.ValidationError('O código do curso deve ser um número inteiro positivo.')
        return codigo

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise ValidationError("O nome do curso deve ter pelo menos 3 caracteres.")
        return nome