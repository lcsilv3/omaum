from django import forms
from cursos.models import Curso
from .models import Turma

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nome', 'descricao']  # Adjust fields as needed

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'curso', 'data_inicio', 'data_fim']  # Adjust fields as needed