from django import forms
from .models import Turma, Matricula
from cursos.models import Curso
from alunos.models import Aluno
from django.core.exceptions import ValidationError

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'curso', 'data_inicio', 'data_fim', 'capacidade', 'status', 'descricao']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise ValidationError("O nome da turma deve ter pelo menos 3 caracteres.")
        return nome

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        if data_inicio and data_fim and data_inicio >= data_fim:
            raise ValidationError("A data de início deve ser anterior à data de fim.")
        return cleaned_data

class AlunoSelecionadoForm(forms.Form):
    aluno = forms.ModelChoiceField(
        queryset=Aluno.objects.all(),
        label="Selecione pelo menos um aluno",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        curso = kwargs.pop('curso', None)
        super().__init__(*args, **kwargs)
        
        if curso:
            # Filtra alunos pelo curso selecionado
            self.fields['aluno'].queryset = Aluno.objects.filter(curso=curso)

class TurmaComAlunoForm(forms.Form):
    """Formulário combinado para criar uma turma com pelo menos um aluno"""
    # Campos da turma
    nome = forms.CharField(max_length=100, label="Nome da Turma")
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(), 
        label="Curso",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_curso'})
    )
    data_inicio = forms.DateField(
        label="Data de Início",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    data_fim = forms.DateField(
        label="Data de Fim",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    capacidade = forms.IntegerField(
        label="Capacidade de Alunos",
        initial=30,
        min_value=1
    )
    status = forms.ChoiceField(
        choices=Turma.OPCOES_STATUS,
        initial='A',
        label="Status"
    )
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label="Descrição"
    )
    
    # Campo para selecionar pelo menos um aluno
    alunos = forms.ModelMultipleChoiceField(
        queryset=Aluno.objects.all(),
        label="Selecione pelo menos um aluno",
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        help_text="Mantenha pressionado Ctrl (ou Command no Mac) para selecionar múltiplos alunos."
    )
    
    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        alunos = cleaned_data.get('alunos')
        curso = cleaned_data.get('curso')
        
        if data_inicio and data_fim and data_inicio >= data_fim:
            raise ValidationError("A data de início deve ser anterior à data de fim.")
        
        if not alunos or len(alunos) < 1:
            raise ValidationError("É necessário selecionar pelo menos um aluno para criar uma turma.")
        
        # Verifica se todos os alunos pertencem ao curso selecionado
        if alunos and curso:
            for aluno in alunos:
                if aluno.curso != curso:
                    raise ValidationError(f"O aluno {aluno.nome} não pertence ao curso {curso.nome}.")
        
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
            self.fields['aluno'].queryset = self.fields['aluno'].queryset.filter(curso=turma.curso)