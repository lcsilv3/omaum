from django import forms
from core.models import Aluno

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome']  # Add other fields that exist in your Aluno model

class ImportForm(forms.Form):
    file = forms.FileField()

