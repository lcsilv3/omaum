from django import forms
from .models import PresencaAcademica

class PresencaForm(forms.ModelForm):
    class Meta:
        model = PresencaAcademica
        fields = ['aluno', 'turma', 'data', 'presente']