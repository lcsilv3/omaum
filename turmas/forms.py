from django import forms
from .models import Turma
from cursos.models import Curso
from django.core.exceptions import ValidationError

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'curso', 'data_inicio', 'data_fim']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
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

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nome', 'descricao', 'duracao']

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise ValidationError("O nome do curso deve ter pelo menos 3 caracteres.")
        return nome