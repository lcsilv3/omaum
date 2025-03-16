from django import forms
from .models import AtividadeAcademica, AtividadeRitualistica

class AtividadeAcademicaForm(forms.ModelForm):
    class Meta:
        model = AtividadeAcademica
        fields = ['nome', 'descricao', 'turma', 'data_inicio', 'data_fim']

class AtividadeRitualisticaForm(forms.ModelForm):
    class Meta:
        model = AtividadeRitualistica
        fields = ['nome', 'descricao', 'turma', 'data_inicio', 'data_fim']

