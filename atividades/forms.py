"""Formulários para o módulo de atividades."""

import logging
from importlib import import_module

from django import forms

logger = logging.getLogger(__name__)


def get_models():
    """
    Obtém todos os modelos necessários dinamicamente.

    Returns:
        dict: Dicionário com todos os modelos necessários
    Raises:
        ImportError: Se algum módulo não puder ser importado
        AttributeError: Se algum modelo não for encontrado no módulo
    """
    try:
        atividades_module = import_module("atividades.models")
        cursos_module = import_module("cursos.models")
        turmas_module = import_module("turmas.models")
        alunos_module = import_module("alunos.models")

        return {
            'AtividadeAcademica': getattr(atividades_module, "AtividadeAcademica"),
            'AtividadeRitualistica': getattr(atividades_module, "AtividadeRitualistica"),
            'Curso': getattr(cursos_module, "Curso"),
            'Turma': getattr(turmas_module, "Turma"),
            'Aluno': getattr(alunos_module, "Aluno"),
        }
    except (ImportError, AttributeError) as e:
        logger.error("Erro ao obter modelos: %s", e)
        raise


class AtividadeAcademicaFiltroForm(forms.Form):
    """Filtro de atividades acadêmicas."""

    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nome ou descrição...'
        })
    )

    curso = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="Todos os cursos",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    turma = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="Todas as turmas",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        """Inicializa o filtro com os querysets corretos."""
        super().__init__(*args, **kwargs)
        try:
            models = get_models()
            self.fields['curso'].queryset = models['Curso'].objects.all()
            self.fields['turma'].queryset = models['Turma'].objects.all()
            if 'curso' in self.data and self.data['curso']:
                try:
                    curso_id = int(self.data['curso'])
                    self.fields['turma'].queryset = (
                        models['Turma'].objects.filter(curso_id=curso_id)
                    )
                except (ValueError, TypeError):
                    logger.warning(
                        "Valor inválido para curso_id: %s", self.data['curso']
                    )
        except Exception as e:
            logger.error(
                "Erro ao inicializar AtividadeAcademicaFiltroForm: %s", e
            )
            self.fields['curso'].queryset = []
            self.fields['turma'].queryset = []


def get_atividade_academica_model():
    """Retorna o modelo AtividadeAcademica."""
    return get_models()['AtividadeAcademica']


class AtividadeAcademicaForm(forms.ModelForm):
    """Formulário para criação e edição de atividades acadêmicas."""

    class Meta:
        model = get_atividade_academica_model()
        fields = [
            'nome', 'descricao', 'tipo_atividade', 'data_inicio', 'data_fim',
            'hora_inicio', 'hora_fim', 'local', 'responsavel', 'status',
            'curso', 'turmas'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'tipo_atividade': forms.Select(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'data_fim': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'hora_inicio': forms.TimeInput(
                attrs={'class': 'form-control', 'type': 'time'}
            ),
            'hora_fim': forms.TimeInput(
                attrs={'class': 'form-control', 'type': 'time'}
            ),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'curso': forms.Select(attrs={'class': 'form-select'}),
            'turmas': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome da Atividade',
            'descricao': 'Descrição',
            'tipo_atividade': 'Tipo de Atividade',
            'data_inicio': 'Data de Início',
            'data_fim': 'Data de Término',
            'hora_inicio': 'Hora de Início',
            'hora_fim': 'Hora de Término',
            'local': 'Local',
            'responsavel': 'Responsável',
            'status': 'Status',
            'curso': 'Curso',
            'turmas': 'Turmas',
        }
        help_texts = {
            'data_fim': (
                'Opcional. Se não informada, será considerada a mesma data de início.'
            ),
            'hora_fim': (
                'Opcional. Se não informada, será considerada 1 hora após o início.'
            ),
            'turmas': 'Selecione uma ou mais turmas para esta atividade.',
        }

    def __init__(self, *args, **kwargs):
        """Inicializa o formulário filtrando as turmas pelo curso."""
        super().__init__(*args, **kwargs)
        models = get_models()
        Turma = models['Turma']
        curso_id = self.initial.get('curso') or self.data.get('curso')
        if curso_id:
            self.fields['turmas'].queryset = Turma.objects.filter(
                curso_id=curso_id
            )
        else:
            self.fields['turmas'].queryset = Turma.objects.none()
        self.fields['curso'].empty_label = "Selecione um curso"


def get_atividade_ritualistica_model():
    """Retorna o modelo AtividadeRitualistica."""
    return get_models()['AtividadeRitualistica']


class AtividadeRitualisticaForm(forms.ModelForm):
    """Formulário para criação e edição de atividades ritualísticas."""

    class Meta:
        model = get_atividade_ritualistica_model()
        fields = [
            'nome', 'descricao', 'data', 'hora_inicio', 'hora_fim',
            'local', 'responsavel', 'status', 'participantes'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'data': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'hora_inicio': forms.TimeInput(
                attrs={'class': 'form-control', 'type': 'time'}
            ),
            'hora_fim': forms.TimeInput(
                attrs={'class': 'form-control', 'type': 'time'}
            ),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'participantes': forms.SelectMultiple(
                attrs={'class': 'form-control'}
            ),
        }
        labels = {
            'nome': 'Nome da Atividade',
            'descricao': 'Descrição',
            'data': 'Data',
            'hora_inicio': 'Hora de Início',
            'hora_fim': 'Hora de Término',
            'local': 'Local',
            'responsavel': 'Responsável',
            'status': 'Status',
            'participantes': 'Participantes',
        }
        help_texts = {
            'hora_fim': (
                'Opcional. Se não informada, será considerada 1 hora após o início.'
            ),
            'participantes': (
                'Selecione um ou mais participantes para esta atividade.'
            ),
        }

    def clean(self):
        """Valida o formulário de atividade ritualística."""
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fim = cleaned_data.get('hora_fim')

        if hora_inicio and hora_fim and hora_fim < hora_inicio:
            self.add_error(
                'hora_fim',
                'A hora de término não pode ser anterior à hora de início.'
            )

        return cleaned_data


def get_curso_queryset():
    """Retorna o queryset de cursos."""
    Curso = import_module("cursos.models").Curso
    return Curso.objects.all()


def get_turma_queryset():
    """Retorna o queryset de turmas."""
    Turma = import_module("turmas.models").Turma
    return Turma.objects.all()


class FiltroAtividadesForm(forms.Form):
    """Filtro alternativo para atividades."""
    curso = forms.ModelChoiceField(
        queryset=get_curso_queryset(),
        required=False,
        label="Curso",
        widget=forms.Select(attrs={"class": "form-select", "id": "filtro-curso"})
    )
    turma = forms.ModelChoiceField(
        queryset=get_turma_queryset(),
        required=False,
        label="Turma",
        widget=forms.Select(attrs={"class": "form-select", "id": "filtro-turma"})
    )
    q = forms.CharField(
        required=False,
        label="Buscar",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Buscar por nome ou descrição..."}
        )
    )