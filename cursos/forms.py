from django import forms
from importlib import import_module


def get_curso_model():
    cursos_module = import_module("cursos.models")
    return getattr(cursos_module, "Curso")


class CursoForm(forms.ModelForm):
    class Meta:
        model = get_curso_model()
        fields = ["nome", "descricao"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get("nome")
        if len(nome) < 3:
            raise forms.ValidationError(
                "O nome do curso deve ter pelo menos 3 caracteres."
            )
        return nome
