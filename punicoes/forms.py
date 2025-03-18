from django import forms
from .models import Punicao

class PunicaoForm(forms.ModelForm):
    class Meta:
        model = Punicao
        fields = ['aluno', 'descricao', 'data', 'tipo_punicao', 'observacoes']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }