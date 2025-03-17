from django import forms
from .models import AtividadeAcademica, AtividadeRitualistica

class AtividadeAcademicaForm(forms.ModelForm):
    class Meta:
        model = AtividadeAcademica
        fields = ('nome', 'descricao', 'data', 'turma')

class AtividadeRitualisticaForm(forms.ModelForm):
    class Meta:
        model = AtividadeRitualistica
        fields = ('nome', 'descricao', 'data', 'alunos')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['alunos'].widget = forms.CheckboxSelectMultiple()