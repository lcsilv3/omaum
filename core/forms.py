from django import forms
from core.models import Aluno, Curso, Turma, AtividadeAcademica, AtividadeRitualistica
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ('nome', 'matricula', 'curso')

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ('nome', 'descricao')

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ('nome', 'curso', 'data_inicio', 'data_fim', 'vagas')

class AtividadeAcademicaForm(forms.ModelForm):
    class Meta:
        model = AtividadeAcademica
        # Corrigir para usar os campos corretos
        fields = ('nome', 'descricao', 'data_inicio', 'data_fim', 'turma')

class AtividadeRitualisticaForm(forms.ModelForm):
    class Meta:
        model = AtividadeRitualistica
        fields = ['nome', 'descricao', 'turma', 'alunos']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['turma'].queryset = Turma.objects.all()
        self.fields['alunos'].queryset = Aluno.objects.all()
        self.fields['alunos'].widget = forms.CheckboxSelectMultiple()

class AlunoTurmaForm(forms.Form):
    aluno = forms.ModelChoiceField(queryset=Aluno.objects.all(), label="Aluno")

    def __init__(self, *args, **kwargs):
        turma = kwargs.pop('turma', None)
        super().__init__(*args, **kwargs)
        if turma:
            self.fields['aluno'].queryset = Aluno.objects.exclude(turmas=turma)

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user