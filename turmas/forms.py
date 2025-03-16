from django import forms
from .models import Curso, Turma

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['codigo_curso', 'nome', 'descricao']

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['curso', 'nome', 'descricao', 'data_inicio', 'data_fim']