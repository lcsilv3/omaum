from django import forms
from importlib import import_module

TipoCodigo = import_module("alunos.utils").get_tipo_codigo_model()
Codigo = import_module("alunos.utils").get_codigo_model()


class TipoCodigoForm(forms.ModelForm):
    class Meta:
        model = TipoCodigo
        fields = ["nome", "descricao"]
        labels = {
            "nome": "Nome do Tipo",
            "descricao": "Descrição",
        }


class CodigoForm(forms.ModelForm):
    class Meta:
        model = Codigo
        fields = ["tipo_codigo", "nome", "descricao"]
        labels = {
            "tipo_codigo": "Tipo",
            "nome": "Número",
            "descricao": "Descrição",
        }
