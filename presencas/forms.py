from django import forms
from importlib import import_module
from datetime import date

def get_turma_model():
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

def get_atividade_model():
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "AtividadeAcademica")

def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

def get_curso_model():
    cursos_module = import_module("cursos.models")
    return getattr(cursos_module, "Curso")

def get_matricula_model():
    matriculas_module = import_module("matriculas.models")
    return getattr(matriculas_module, "Matricula")

class DadosBasicosPresencaForm(forms.Form):
    curso = forms.ModelChoiceField(
        queryset=get_curso_model().objects.all(),
        label="Curso",
        required=True,
        empty_label="Selecione..."
    )
    turma = forms.ModelChoiceField(
        queryset=get_turma_model().objects.none(),
        label="Turma",
        required=True,
        empty_label="Selecione..."
    )
    ano = forms.IntegerField(label="Ano", required=True)
    mes = forms.IntegerField(label="Mês", required=True, min_value=1, max_value=12)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'curso' in self.data:
            try:
                curso_id = int(self.data.get('curso'))
                self.fields['turma'].queryset = get_turma_model().objects.filter(curso_id=curso_id, status='A')
            except (ValueError, TypeError):
                self.fields['turma'].queryset = get_turma_model().objects.none()
        elif self.initial.get('curso'):
            curso_id = self.initial.get('curso').id if hasattr(self.initial.get('curso'), 'id') else self.initial.get('curso')
            self.fields['turma'].queryset = get_turma_model().objects.filter(curso_id=curso_id, status='A')
        else:
            self.fields['turma'].queryset = get_turma_model().objects.none()

class TotaisAtividadesPresencaForm(forms.Form):
    def __init__(self, *args, atividades=None, **kwargs):
        super().__init__(*args, **kwargs)
        if atividades is not None:
            for atividade in atividades:
                self.fields[f'qtd_ativ_{atividade.id}'] = forms.IntegerField(
                    label=atividade.nome,
                    min_value=0,
                    max_value=999,
                    required=True,
                    widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Qtd. dias'})
                )
        self.atividades = atividades

    def clean(self):
        cleaned_data = super().clean()
        faltantes = []
        for atividade in getattr(self, 'atividades', []):
            key = f'qtd_ativ_{atividade.id}'
            if cleaned_data.get(key) in [None, '']:
                faltantes.append(atividade.nome)
        if faltantes:
            raise forms.ValidationError(
                f"As seguintes atividades não tiveram quantidade informada: {', '.join(faltantes)}. "
                "As atividades não informadas não poderão sofrer alterações na seção seguinte."
            )
        return cleaned_data

class AlunosPresencaForm(forms.Form):
    alunos_presentes = forms.ModelMultipleChoiceField(
        queryset=get_aluno_model().objects.none(),
        label="Alunos Presentes",
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, turma=None, **kwargs):
        super().__init__(*args, **kwargs)
        if turma:
            Matricula = get_matricula_model()
            matriculas = Matricula.objects.filter(turma=turma, status='A')
            alunos_ids = matriculas.values_list('aluno_id', flat=True)
            self.fields['alunos_presentes'].queryset = get_aluno_model().objects.filter(
                pk__in=alunos_ids, situacao='ATIVO'
            ).order_by('nome')
