from django import forms
from .models import Iniciacao

class IniciacaoForm(forms.ModelForm):
    class Meta:
        model = Iniciacao
        fields = ['aluno', 'nome_curso', 'data_iniciacao', 'observacoes']
        widgets = {
            'data_iniciacao': forms.DateInput(attrs={'type': 'date'}),
        }