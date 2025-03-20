from django import forms
from .models import Punicao
from django.core.exceptions import ValidationError

class PunicaoForm(forms.ModelForm):
    class Meta:
        model = Punicao
        fields = ['aluno', 'descricao', 'data', 'tipo_punicao', 'observacoes']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_descricao(self):
        descricao = self.cleaned_data.get('descricao')
        if len(descricao) < 10:
            raise ValidationError("A descrição da punição deve ter pelo menos 10 caracteres.")
        return descricao

    def clean_data(self):
        data = self.cleaned_data.get('data')
        if data and data > datetime.date.today():
            raise ValidationError("A data da punição não pode ser no futuro.")
        return data