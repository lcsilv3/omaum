from django import forms
from importlib import import_module

def get_presenca_model():
    presencas_module = import_module('presencas.models')
    return getattr(presencas_module, 'PresencaAcademica')

def get_aluno_model():
    alunos_module = import_module('alunos.models')
    return getattr(alunos_module, 'Aluno')

def get_turma_model():
    turmas_module = import_module('turmas.models')
    return getattr(turmas_module, 'Turma')

class PresencaForm(forms.ModelForm):
    class Meta:
        model = get_presenca_model()
        fields = ['aluno', 'turma', 'data', 'presente', 'justificativa']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-control'}),
            'turma': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'presente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'justificativa': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
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