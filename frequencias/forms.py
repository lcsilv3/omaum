from django import forms
from .models import Frequencia
import datetime
from django.core.exceptions import ValidationError


class FrequenciaForm(forms.ModelForm):
    class Meta:
        model = Frequencia
        fields = ["aluno", "turma", "data", "presente", "justificativa"]
        widgets = {
            "aluno": forms.Select(attrs={"class": "form-select"}),
            "turma": forms.Select(attrs={"class": "form-select"}),
            "data": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "presente": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "justificativa": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),
        }

    def clean_data(self):
        data = self.cleaned_data.get("data")
        if data and data > datetime.date.today():
            raise ValidationError(
                "A data da frequência não pode ser no futuro."
            )
        return data

    def clean(self):
        cleaned_data = super().clean()
        aluno = cleaned_data.get("aluno")
        turma = cleaned_data.get("turma")
        data = cleaned_data.get("data")

        # Se for uma atualização (instância existe), precisamos excluir a instância atual da verificação de unicidade
        if self.instance.pk:
            if (
                Frequencia.objects.filter(aluno=aluno, turma=turma, data=data)
                .exclude(pk=self.instance.pk)
                .exists()
            ):
                raise ValidationError(
                    "Já existe um registro de frequência para este aluno nesta turma e data."
                )
        else:
            if aluno and turma and data:
                if Frequencia.objects.filter(
                    aluno=aluno, turma=turma, data=data
                ).exists():
                    raise ValidationError(
                        "Já existe um registro de frequência para este aluno nesta turma e data."
                    )

        return cleaned_data
