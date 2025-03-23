from django import forms
from .models import PresencaAcademica
import datetime
from django.core.exceptions import ValidationError

class PresencaForm(forms.ModelForm):
    class Meta:
        model = PresencaAcademica
        fields = ['aluno', 'turma', 'data', 'presente']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def clean_data(self):
        data = self.cleaned_data.get('data')
        if data and data > datetime.date.today():
            raise ValidationError("A data da presença não pode ser no futuro.")
        return data
        
    def clean(self):
        cleaned_data = super().clean()
        aluno = cleaned_data.get('aluno')
        turma = cleaned_data.get('turma')
        data = cleaned_data.get('data')
        
        if aluno and turma and data:
            if PresencaAcademica.objects.filter(aluno=aluno, turma=turma, data=data).exists():
                raise ValidationError("Já existe um registro de presença para este aluno nesta turma e data.")
        
        return cleaned_data