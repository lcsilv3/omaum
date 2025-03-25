from django import forms
from .models import Turma, Matricula
from importlib import import_module

def get_aluno_model():
    alunos_module = import_module('alunos.models')
    return getattr(alunos_module, 'Aluno')

def get_curso_model():
    cursos_module = import_module('cursos.models')
    return getattr(cursos_module, 'Curso')
class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'curso', 'data_inicio', 'data_fim', 'capacidade', 'status', 'descricao']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['curso'].queryset = get_curso_model().objects.all()

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        if data_inicio and data_fim and data_inicio >= data_fim:
            raise forms.ValidationError("A data de início deve ser anterior à data de fim.")
        return cleaned_data

class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields = ['aluno', 'status']

    def __init__(self, *args, **kwargs):
        turma = kwargs.pop('turma', None)
        super().__init__(*args, **kwargs)

        if turma:
            # Filtra alunos pelo curso da turma
            self.fields['aluno'].queryset = get_aluno_model().objects.filter(curso=turma.curso)
            self.fields['aluno'].queryset = self.fields['aluno'].queryset.filter(curso=turma.curso)