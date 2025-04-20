from django import forms
from .models import Presenca


class PresencaForm(forms.ModelForm):
    class Meta:
        model = Presenca
        fields = ["aluno", "turma", "data", "status"]
        widgets = {
            "data": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "aluno": "Aluno",
            "turma": "Turma",
            "data": "Data",
            "status": "Status",
        }
        help_texts = {
            "status": "Selecione o status de presença do aluno.",
        }
