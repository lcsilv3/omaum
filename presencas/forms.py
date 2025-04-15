from django import forms
from datetime import date
from django.core.exceptions import ValidationError
from .models import PresencaAcademica


class PresencaForm(forms.ModelForm):
    class Meta:
        model = PresencaAcademica
        fields = ["aluno", "turma", "data", "presente", "justificativa"]
        widgets = {
            "aluno": forms.Select(attrs={"class": "form-control"}),
            "turma": forms.Select(attrs={"class": "form-control"}),
            "data": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "presente": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "justificativa": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }

    def clean_data(self):
        data = self.cleaned_data.get("data")
        if data and data > date.today():
            raise ValidationError("A data da presença não pode ser no futuro.")
        return data

    def clean(self):
        cleaned_data = super().clean()
        aluno = cleaned_data.get("aluno")
        turma = cleaned_data.get("turma")
        data = cleaned_data.get("data")

        if aluno and turma and data:
            # Check if this is an update (instance exists)
            if self.instance.pk:
                # Exclude the current instance from the uniqueness check
                existing = (
                    PresencaAcademica.objects.filter(
                        aluno=aluno, turma=turma, data=data
                    )
                    .exclude(pk=self.instance.pk)
                    .exists()
                )
            else:
                # For new instances, check if any record exists
                existing = PresencaAcademica.objects.filter(
                    aluno=aluno, turma=turma, data=data
                ).exists()

            if existing:
                raise ValidationError(
                    "Já existe um registro de presença para este aluno nesta turma e data."
                )

        return cleaned_data
