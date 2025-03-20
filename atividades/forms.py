from django import forms
from django.core.exceptions import ValidationError
from .models import AtividadeAcademica, AtividadeRitualistica
import datetime

class AtividadeAcademicaForm(forms.ModelForm):
    class Meta:
        model = AtividadeAcademica
        fields = ('nome', 'descricao', 'data_inicio', 'data_fim', 'turma')
    widgets = {
        'data_inicio': forms.DateInput(attrs={'type': 'date'}),
        'data_fim': forms.DateInput(attrs={'type': 'date'}),
    }

    def clean_data_inicio(self):
        data_inicio = self.cleaned_data.get('data_inicio')
        if data_inicio and data_inicio < datetime.date.today():
            raise ValidationError("A data de início da atividade não pode ser no passado.")
        return data_inicio

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        if data_inicio and data_fim and data_fim < data_inicio:
            raise ValidationError("A data de fim não pode ser anterior à data de início.")
        return cleaned_data

class AtividadeRitualisticaForm(forms.ModelForm):
    class Meta:
        model = AtividadeRitualistica
        fields = ('nome', 'descricao', 'data_inicio', 'data_fim', 'turma', 'alunos', 'todos_alunos')
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
            'alunos': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['alunos'].required = False

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        todos_alunos = cleaned_data.get('todos_alunos')
        alunos = cleaned_data.get('alunos')
        if data_inicio and data_fim and data_fim < data_inicio:
            raise ValidationError("A data de fim não pode ser anterior à data de início.")

        if not todos_alunos and not alunos:
            raise ValidationError("Selecione alunos específicos ou marque 'Todos os Alunos'.")

        if todos_alunos and alunos:
            raise ValidationError("Você não pode selecionar alunos específicos quando 'Todos os Alunos' está marcado.")
        return cleaned_data