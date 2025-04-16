from django import forms
from .models import Turma
from django.core.exceptions import ValidationError
from django.utils import timezone
from importlib import import_module  # Add this import


def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = [
            "nome",
            "curso",
            "vagas",
            "status",
            "data_inicio",
            "data_fim",
            "instrutor",
            "instrutor_auxiliar",
            "auxiliar_instrucao",
            "dias_semana",
            "local",
            "horario",
            "descricao",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "curso": forms.Select(attrs={"class": "form-select"}),
            "vagas": forms.NumberInput(
                attrs={"class": "form-control", "min": "1"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "data_inicio": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "data_fim": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "instrutor": forms.Select(attrs={"class": "form-control"}),
            "instrutor_auxiliar": forms.Select(
                attrs={"class": "form-control"}
            ),
            "auxiliar_instrucao": forms.Select(
                attrs={"class": "form-control"}
            ),
            "dias_semana": forms.TextInput(attrs={"class": "form-control"}),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "horario": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }
        help_texts = {
            "vagas": "Número máximo de alunos que podem ser matriculados na turma.",
            "data_inicio": "Data de início das aulas.",
            "data_fim": "Data prevista para o término das aulas.",
            "status": "Status atual da turma.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convert date format for display in the form
        if self.instance and self.instance.pk:
            if self.instance.data_inicio:
                self.initial[
                    "data_inicio"
                ] = self.instance.data_inicio.strftime("%Y-%m-%d")
            if self.instance.data_fim:
                self.initial["data_fim"] = self.instance.data_fim.strftime(
                    "%Y-%m-%d"
                )

        # Tornar os campos de instrutores opcionais
        self.fields["instrutor"].required = False
        self.fields["instrutor_auxiliar"].required = False
        self.fields["auxiliar_instrucao"].required = False

        # Configurar os querysets para mostrar apenas alunos elegíveis
        Aluno = get_aluno_model()
        alunos_elegíveis = Aluno.objects.filter(situacao="A")

        # Filtrar alunos que podem ser instrutores
        alunos_instrutores = [
            aluno for aluno in alunos_elegíveis if aluno.pode_ser_instrutor
        ]

        self.fields["instrutor"].queryset = Aluno.objects.filter(
            cpf__in=[a.cpf for a in alunos_instrutores]
        )
        self.fields["instrutor_auxiliar"].queryset = Aluno.objects.filter(
            cpf__in=[a.cpf for a in alunos_instrutores]
        )
        self.fields["auxiliar_instrucao"].queryset = Aluno.objects.filter(
            cpf__in=[a.cpf for a in alunos_instrutores]
        )

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get("data_inicio")
        data_fim = cleaned_data.get("data_fim")

        # Validar que a data de início é anterior à data de fim
        if data_inicio and data_fim and data_inicio > data_fim:
            raise ValidationError(
                "A data de início não pode ser posterior à data de fim."
            )

        # Validar que a data de início não é no passado (para novas turmas)
        if (
            not self.instance.pk
            and data_inicio
            and data_inicio < timezone.now().date()
        ):
            raise ValidationError(
                "A data de início não pode ser no passado para novas turmas."
            )

        # Verificar se os instrutores são diferentes entre si
        instrutor = cleaned_data.get("instrutor")
        instrutor_auxiliar = cleaned_data.get("instrutor_auxiliar")
        auxiliar_instrucao = cleaned_data.get("auxiliar_instrucao")

        if (
            instrutor
            and instrutor_auxiliar
            and instrutor == instrutor_auxiliar
        ):
            self.add_error(
                "instrutor_auxiliar",
                "O instrutor auxiliar deve ser diferente do instrutor principal.",
            )

        if (
            instrutor
            and auxiliar_instrucao
            and instrutor == auxiliar_instrucao
        ):
            self.add_error(
                "auxiliar_instrucao",
                "O auxiliar de instrução deve ser diferente do instrutor principal.",
            )

        if (
            instrutor_auxiliar
            and auxiliar_instrucao
            and instrutor_auxiliar == auxiliar_instrucao
        ):
            self.add_error(
                "auxiliar_instrucao",
                "O auxiliar de instrução deve ser diferente do instrutor auxiliar.",
            )

        return cleaned_data

    def clean_nome(self):
        nome = self.cleaned_data.get("nome")
        if nome:
            # Verificar se já existe uma turma com o mesmo nome (ignorando case)
            instance_id = getattr(self.instance, "id", None)
            turmas_existentes = Turma.objects.filter(nome__iexact=nome)

            if instance_id:
                turmas_existentes = turmas_existentes.exclude(id=instance_id)

            if turmas_existentes.exists():
                raise ValidationError(
                    "Já existe uma turma com este nome. Por favor, escolha um nome diferente."
                )

            # Opcional: normalizar o nome (por exemplo, primeira letra maiúscula)
            nome = nome.strip().capitalize()

        return nome
