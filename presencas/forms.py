from django import forms
from datetime import date
import logging
from cursos.models import Curso
from turmas.models import Turma
from alunos.models import Aluno
from matriculas.models import Matricula
from atividades.models import PresencaAcademica
from django.utils import timezone
from django_select2.forms import Select2Widget


logger = logging.getLogger(__name__)

class RegistrarPresencaForm(forms.Form):
    """
    Formulário para o primeiro passo do registro de presença,
    com seleção de curso, turma, ano e mês.
    """
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.filter(ativo=True),
        label="Curso",
        widget=Select2Widget(attrs={'data-placeholder': 'Selecione um curso'}),
        required=True
    )
    turma = forms.ModelChoiceField(
        queryset=Turma.objects.none(),  # Populado via AJAX
        label="Turma",
        widget=Select2Widget(attrs={'data-placeholder': 'Selecione uma turma'}),
        required=True
    )

    ANO_CHOICES = [(ano, str(ano)) for ano in range(timezone.now().year, timezone.now().year - 5, -1)]
    MES_CHOICES = [(i, date(2000, i, 1).strftime('%B').capitalize()) for i in range(1, 13)]

    ano = forms.ChoiceField(
        choices=ANO_CHOICES,
        label="Ano",
        required=True,
        initial=timezone.now().year
    )
    mes = forms.ChoiceField(
        choices=MES_CHOICES,
        label="Mês",
        required=True,
        initial=timezone.now().month
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'curso' in self.data:
            try:
                curso_id = int(self.data.get('curso'))
                self.fields['turma'].queryset = Turma.objects.filter(
                    curso_id=curso_id,
                    status='A'
                ).order_by('nome')
            except (ValueError, TypeError):
                pass  # O queryset permanecerá como none()
        elif self.initial.get('curso'):
            curso_id = self.initial['curso'].pk
            self.fields['turma'].queryset = Turma.objects.filter(
                curso_id=curso_id,
                status='A'
            ).order_by('nome')

class TotaisAtividadesPresencaForm(forms.Form):
    """
    Formulário dinâmico para informar o total de atividades por mês.
    """
    def __init__(self, *args, atividades=None, **kwargs):
        super().__init__(*args, **kwargs)
        if atividades is not None:
            for atividade in atividades:
                self.fields[f'qtd_ativ_{atividade.id}'] = forms.IntegerField(
                    label=atividade.nome,
                    min_value=0,
                    max_value=999,
                    required=True,
                    widget=forms.NumberInput(
                        attrs={
                            'class': 'form-control',
                            'placeholder': 'Qtd. dias',
                            'aria-label': atividade.nome
                        }
                    )
                )
        self.atividades = atividades

    def clean(self):
        cleaned_data = super().clean()
        # Adicione validações customizadas se necessário
        return cleaned_data

class AlunosPresencaForm(forms.Form):
    """
    Formulário para seleção de presença/falta dos alunos convocados.
    """
    def __init__(self, *args, alunos=None, **kwargs):
        super().__init__(*args, **kwargs)
        if alunos:
            for aluno in alunos:
                self.fields[f'aluno_{aluno.id}_status'] = forms.ChoiceField(
                    choices=[('presente', 'Presente'), ('ausente', 'Ausente')],
                    initial='presente',
                    label=aluno.nome,
                    widget=forms.RadioSelect(attrs={'class': 'form-check-input', 'aria-label': aluno.nome})
                )
                self.fields[f'aluno_{aluno.id}_justificativa'] = forms.CharField(
                    required=False,
                    label='Justificativa',
                    widget=forms.TextInput(attrs={'placeholder': 'Justificativa da falta', 'class': 'form-control', 'aria-label': f'Justificativa {aluno.nome}'})
                )

class PresencaAcademicaForm(forms.ModelForm):
    """
    Formulário para criação/edição de PresencaAcademica.
    """
    class Meta:
        model = PresencaAcademica
        fields = [
            'aluno', 'turma', 'atividade', 'data', 'presente',
            'registrado_por', 'data_registro'
        ]
