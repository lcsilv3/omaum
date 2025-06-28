from django import forms
import logging
from cursos.models import Curso
from turmas.models import Turma
from alunos.models import Aluno
from matriculas.models import Matricula
from atividades.models import PresencaAcademica

logger = logging.getLogger(__name__)

class DadosBasicosPresencaForm(forms.Form):
    """
    Formulário para seleção de curso, turma, ano e mês para registro de presença.
    """
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        label="Curso",
        required=True,
        empty_label="Selecione..."
    )
    turma = forms.ModelChoiceField(
        queryset=Turma.objects.none(),
        label="Turma",
        required=True,
        empty_label="Selecione..."
    )
    ano = forms.IntegerField(label="Ano", required=True)
    mes = forms.IntegerField(label="Mês", required=True, min_value=1, max_value=12)

    def __init__(self, *args, **kwargs):
        """
        Atualiza o queryset de turmas conforme o curso selecionado.
        """
        super().__init__(*args, **kwargs)
        if 'curso' in self.data:
            try:
                curso_id = int(self.data.get('curso'))
                self.fields['turma'].queryset = Turma.objects.filter(curso_id=curso_id, status='A')
            except (ValueError, TypeError) as e:
                logger.warning("Erro ao filtrar turmas por curso: %s", e)
                self.fields['turma'].queryset = Turma.objects.none()
        elif self.initial.get('curso'):
            curso_id = self.initial.get('curso').id if hasattr(self.initial.get('curso'), 'id') else self.initial.get('curso')
            self.fields['turma'].queryset = Turma.objects.filter(curso_id=curso_id, status='A')
        else:
            self.fields['turma'].queryset = Turma.objects.none()

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
