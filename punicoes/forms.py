from django import forms
from importlib import import_module


def get_punicao_model():
    punicoes_module = import_module("punicoes.models")
    return getattr(punicoes_module, "Punicao")


def get_tipo_punicao_model():
    punicoes_module = import_module("punicoes.models")
    return getattr(punicoes_module, "TipoPunicao")


def get_model(app_name, model_name):
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)


class PunicaoForm(forms.ModelForm):
    class Meta:
        model = get_punicao_model()
        fields = [
            "aluno",
            "tipo_punicao",
            "data_aplicacao",
            "motivo",
            "observacoes",
        ]
        widgets = {
            "aluno": forms.Select(attrs={"class": "form-control"}),
            "tipo_punicao": forms.Select(attrs={"class": "form-control"}),
            "data_aplicacao": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "motivo": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "observacoes": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }


class TipoPunicaoForm(forms.ModelForm):
    class Meta:
        model = get_tipo_punicao_model()
        fields = [
            "nome",
            "descricao",
        ]  # Removed 'gravidade' since it's not in the model
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 3}),
        }
