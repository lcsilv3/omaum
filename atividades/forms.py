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
            "Atividade": getattr(atividades_module, "Atividade"),
            "Curso": getattr(cursos_module, "Curso"),
            "Turma": getattr(turmas_module, "Turma"),
            "Aluno": getattr(alunos_module, "Aluno"),
        }
    except (ImportError, AttributeError) as e:
        logger.error("Erro ao obter modelos: %s", e)
        raise


class AtividadeFiltroForm(forms.Form):
    """Filtro de atividades."""

    q = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Buscar por nome ou descrição...",
            }
        ),
    )

    curso = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="Selecione",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    turma = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="Selecione",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, **kwargs):
        """Inicializa o filtro com os querysets corretos."""
        super().__init__(*args, **kwargs)
        try:
            models = get_models()
            self.fields["curso"].queryset = models["Curso"].objects.all()
            self.fields["turma"].queryset = models["Turma"].objects.all()
            if "curso" in self.data and self.data["curso"]:
                try:
                    curso_id = int(self.data["curso"])
                    self.fields["turma"].queryset = models["Turma"].objects.filter(
                        curso_id=curso_id
                    )
                except (ValueError, TypeError):
                    logger.warning(
                        "Valor inválido para curso_id: %s", self.data["curso"]
                    )
        except Exception as e:
            logger.error("Erro ao inicializar AtividadeFiltroForm: %s", e)
            self.fields["curso"].queryset = []
            self.fields["turma"].queryset = []


def get_atividade_model():
    """Retorna o modelo Atividade."""
    return get_models()["Atividade"]


class AtividadeForm(forms.ModelForm):
    """Formulário para criação e edição de atividades."""

    class Meta:
        from atividades.models import Atividade

        model = Atividade
        fields = [
            "nome",
            "descricao",
            "tipo_atividade",
            "data_inicio",
            "data_fim",
            "hora_inicio",
            "hora_fim",
            "local",
            "responsavel",
            "status",
            "curso",
            "turmas",
            "convocacao",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "tipo_atividade": forms.Select(attrs={"class": "form-select"}),
            "data_inicio": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "data_fim": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "hora_inicio": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "hora_fim": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "responsavel": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "curso": forms.Select(attrs={"class": "form-select"}),
            "turmas": forms.SelectMultiple(attrs={"class": "form-control"}),
            "convocacao": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "nome": "Nome da Atividade",
            "descricao": "Descrição",
            "tipo_atividade": "Tipo de Atividade",
            "data_inicio": "Data de Início",
            "data_fim": "Data de Término",
            "hora_inicio": "Hora de Início",
            "hora_fim": "Hora de Término",
            "local": "Local",
            "responsavel": "Responsável",
            "status": "Status",
            "curso": "Curso",
            "turmas": "Turmas",
            "convocacao": "Convocação",
        }
        help_texts = {
            "data_fim": (
                "Opcional. Deixe em branco se a atividade ocorre apenas em um dia."
            ),
            "hora_fim": (
                "Opcional. Deixe em branco se não há horário específico de término."
            ),
            "turmas": "Selecione uma ou mais turmas para esta atividade.",
        }

    def __init__(self, *args, **kwargs):
        """Inicializa o formulário filtrando as turmas pelo curso."""
        super().__init__(*args, **kwargs)
        self.fields["data_inicio"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        self.fields["data_fim"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        models = get_models()
        Turma = models["Turma"]

        # Para edição, usar o curso da instância, senão usar os dados do formulário
        if self.instance and self.instance.pk:
            curso_id = self.instance.curso_id if self.instance.curso else None
        else:
            curso_id = self.initial.get("curso") or self.data.get("curso")

        if curso_id:
            self.fields["turmas"].queryset = Turma.objects.filter(curso_id=curso_id)
        else:
            # Para criação inicial, mostra todas as turmas disponíveis
            self.fields["turmas"].queryset = Turma.objects.all()
        self.fields["curso"].empty_label = "Selecione"

    def clean(self):
        """Validação customizada do formulário."""
        cleaned_data = super().clean()
        curso = cleaned_data.get("curso")
        turmas = cleaned_data.get("turmas")

        if turmas:
            # Se não foi selecionado um curso, mas há turmas, usar o curso da primeira turma
            if not curso:
                primeira_turma = turmas.first()
                if primeira_turma and primeira_turma.curso:
                    cleaned_data["curso"] = primeira_turma.curso

            # Validar se todas as turmas pertencem ao mesmo curso
            cursos_das_turmas = set(turma.curso_id for turma in turmas if turma.curso)
            if len(cursos_das_turmas) > 1:
                self.add_error(
                    "turmas", "Todas as turmas devem pertencer ao mesmo curso."
                )
            elif len(cursos_das_turmas) == 1 and curso:
                curso_das_turmas = list(cursos_das_turmas)[0]
                if curso.id != curso_das_turmas:
                    self.add_error(
                        "curso",
                        "O curso selecionado deve ser o mesmo das turmas escolhidas.",
                    )

        return cleaned_data

    def save(self, commit=True):
        """Salva a instância garantindo consistência entre curso e turmas."""
        instance = super().save(commit=False)

        # Se não há curso definido mas há turmas, definir o curso baseado nas turmas
        turmas = self.cleaned_data.get("turmas")
        if turmas and not instance.curso:
            primeira_turma = turmas.first()
            if primeira_turma and primeira_turma.curso:
                instance.curso = primeira_turma.curso

        if commit:
            instance.save()
            self.save_m2m()

        return instance


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
        empty_label="Selecione",
        widget=forms.Select(attrs={"class": "form-select", "id": "filtro-curso"}),
    )
    turma = forms.ModelChoiceField(
        queryset=get_turma_queryset(),
        required=False,
        label="Turma",
        empty_label="Selecione",
        widget=forms.Select(attrs={"class": "form-select", "id": "filtro-turma"}),
    )
    q = forms.CharField(
        required=False,
        label="Buscar",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Buscar por nome ou descrição...",
            }
        ),
    )


class AtividadeAcademicaForm(forms.ModelForm):
    """Formulário para atividades acadêmicas."""

    class Meta:
        from atividades.models import Atividade

        model = Atividade
        fields = [
            "nome",
            "descricao",
            "tipo_atividade",
            "data_inicio",
            "data_fim",
            "hora_inicio",
            "hora_fim",
            "local",
            "responsavel",
            "status",
            "curso",
            "turmas",
            "convocacao",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "tipo_atividade": forms.Select(attrs={"class": "form-select"}),
            "data_inicio": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "data_fim": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "hora_inicio": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "hora_fim": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "responsavel": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "curso": forms.Select(attrs={"class": "form-select"}),
            "turmas": forms.SelectMultiple(attrs={"class": "form-control"}),
            "convocacao": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "nome": "Nome da Atividade",
            "descricao": "Descrição",
            "tipo_atividade": "Tipo de Atividade",
            "data_inicio": "Data de Início",
            "data_fim": "Data de Término",
            "hora_inicio": "Hora de Início",
            "hora_fim": "Hora de Término",
            "local": "Local",
            "responsavel": "Responsável",
            "status": "Status",
            "curso": "Curso",
            "turmas": "Turmas",
            "convocacao": "Convocação",
        }

    def __init__(self, *args, **kwargs):
        """Inicializa o formulário filtrando as turmas pelo curso."""
        super().__init__(*args, **kwargs)
        self.fields["data_inicio"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        self.fields["data_fim"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        models = get_models()
        Turma = models["Turma"]

        # Para edição, usar o curso da instância, senão usar os dados do formulário
        if self.instance and self.instance.pk:
            curso_id = self.instance.curso_id if self.instance.curso else None
        else:
            curso_id = self.initial.get("curso") or self.data.get("curso")

        if curso_id:
            self.fields["turmas"].queryset = Turma.objects.filter(curso_id=curso_id)
        else:
            # Para criação inicial, mostra todas as turmas disponíveis
            self.fields["turmas"].queryset = Turma.objects.all()
        self.fields["curso"].empty_label = "Selecione"

    def clean(self):
        """Validação customizada do formulário."""
        cleaned_data = super().clean()
        curso = cleaned_data.get("curso")
        turmas = cleaned_data.get("turmas")

        if turmas:
            # Se não foi selecionado um curso, mas há turmas, usar o curso da primeira turma
            if not curso:
                primeira_turma = turmas.first()
                if primeira_turma and primeira_turma.curso:
                    cleaned_data["curso"] = primeira_turma.curso

            # Validar se todas as turmas pertencem ao mesmo curso
            cursos_das_turmas = set(turma.curso_id for turma in turmas if turma.curso)
            if len(cursos_das_turmas) > 1:
                self.add_error(
                    "turmas", "Todas as turmas devem pertencer ao mesmo curso."
                )
            elif len(cursos_das_turmas) == 1 and curso:
                curso_das_turmas = list(cursos_das_turmas)[0]
                if curso.id != curso_das_turmas:
                    self.add_error(
                        "curso",
                        "O curso selecionado deve ser o mesmo das turmas escolhidas.",
                    )

        return cleaned_data

    def save(self, commit=True):
        """Salva a instância garantindo consistência entre curso e turmas."""
        instance = super().save(commit=False)

        # Se não há curso definido mas há turmas, definir o curso baseado nas turmas
        turmas = self.cleaned_data.get("turmas")
        if turmas and not instance.curso:
            primeira_turma = turmas.first()
            if primeira_turma and primeira_turma.curso:
                instance.curso = primeira_turma.curso

        if commit:
            instance.save()
            self.save_m2m()

        return instance
