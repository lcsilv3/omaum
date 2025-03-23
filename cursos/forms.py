from django import forms
from .models import Curso
from django.core.exceptions import ValidationError

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['codigo_curso', 'nome', 'descricao', 'duracao']

    def clean_codigo_curso(self):
        codigo = self.cleaned_data.get('codigo_curso')
        if len(codigo) != 5:
            raise ValidationError("O código do curso deve ter exatamente 5 caracteres.")
        return codigo

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise ValidationError("O nome do curso deve ter pelo menos 3 caracteres.")
        return nome