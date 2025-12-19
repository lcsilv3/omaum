"""
Formulários completos para o aplicativo de Matrículas.
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from importlib import import_module
from .models import Matricula


def get_aluno_model():
    """Obtém o modelo Aluno."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


class MatriculaForm(forms.ModelForm):
    """Formulário para criação e edição de matrículas."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        Aluno = get_aluno_model()
        Turma = get_turma_model()

        # Configurar queryset para alunos ativos (situacao='a')
        self.fields["aluno"].queryset = Aluno.objects.filter(situacao="a").order_by(
            "nome"
        )
        self.fields["aluno"].widget.attrs.update(
            {"class": "form-select", "placeholder": "Selecione um aluno"}
        )

        # Configurar queryset para turmas ativas
        self.fields["turma"].queryset = Turma.objects.filter(ativo=True).order_by(
            "nome"
        )
        self.fields["turma"].widget.attrs.update(
            {"class": "form-select", "placeholder": "Selecione uma turma"}
        )

        # Configurar campo de data (padrão hoje)
        self.fields["data_matricula"].widget = forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
                "value": timezone.now().date(),
            }
        )

        # Configurar campo de status
        self.fields["status"].widget.attrs.update({"class": "form-select"})

        # Tornar campos obrigatórios
        self.fields["aluno"].required = True
        self.fields["turma"].required = True
        self.fields["data_matricula"].required = True

        # Configurar labels
        self.fields["aluno"].label = "Aluno *"
        self.fields["turma"].label = "Turma *"
        self.fields["data_matricula"].label = "Data da Matrícula *"
        self.fields["status"].label = "Status"

        # Configurar help_text
        self.fields["aluno"].help_text = "Selecione o aluno que será matriculado"
        self.fields["turma"].help_text = "Selecione a turma para a matrícula"
        self.fields[
            "data_matricula"
        ].help_text = "Data em que a matrícula foi realizada"
        self.fields["status"].help_text = "Status atual da matrícula"

    class Meta:
        model = Matricula
        fields = ["aluno", "turma", "data_matricula", "status"]
        widgets = {
            "aluno": forms.Select(attrs={"class": "form-select"}),
            "turma": forms.Select(attrs={"class": "form-select"}),
            "data_matricula": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

    def clean(self):
        """Validação personalizada."""
        cleaned_data = super().clean()
        aluno = cleaned_data.get("aluno")
        turma = cleaned_data.get("turma")

        if aluno and turma:
            # Verificar se o aluno já está matriculado nesta turma
            existing_matricula = Matricula.objects.filter(
                aluno=aluno,
                turma=turma,
                status="A",  # Apenas matrículas ativas
            ).exclude(pk=self.instance.pk if self.instance else None)

            if existing_matricula.exists():
                raise ValidationError(
                    "Este aluno já possui uma matrícula ativa nesta turma."
                )

            # Verificar se a turma está ativa
            if not turma.ativo:
                raise ValidationError("Não é possível matricular em uma turma inativa.")

        return cleaned_data


class MatriculaFiltroForm(forms.Form):
    """Formulário para filtros de matrícula."""

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Buscar por nome do aluno ou turma...",
            }
        ),
    )

    status = forms.ChoiceField(
        required=False,
        choices=[("", "Todos os Status")] + Matricula.OPCOES_STATUS,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    turma = forms.ModelChoiceField(
        required=False,
        queryset=None,
        empty_label="Todas as Turmas",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        Turma = get_turma_model()
        self.fields["turma"].queryset = Turma.objects.filter(ativo=True).order_by(
            "nome"
        )
