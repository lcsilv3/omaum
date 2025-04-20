from django import forms
from .models import Relatorio


class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = ["titulo", "conteudo"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "conteudo": forms.Textarea(attrs={"class": "form-control"}),
        }
