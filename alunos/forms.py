from django import forms
from .models import Aluno, RegistroHistorico, Codigo


class AlunoForm(forms.ModelForm):
    """Formulário para criação e edição de alunos."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Formata a data para o input type="date"
        instance_exists = (
            self.instance and self.instance.pk and self.instance.data_nascimento
        )
        if instance_exists:
            self.initial["data_nascimento"] = self.instance.data_nascimento.strftime(
                "%Y-%m-%d"
            )

        # Adiciona classes CSS e placeholders
        placeholders = {
            "cpf": "Somente números",
            "cep": "Somente números",
            "celular_primeiro_contato": "Somente números",
            "celular_segundo_contato": "Somente números",
        }
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            if field_name in placeholders:
                field.widget.attrs["placeholder"] = placeholders[field_name]

    class Meta:
        model = Aluno
        fields = "__all__"
        # Excluir campos que não devem ser editados pelo usuário no formulário público
        exclude = ["ativo", "created_at", "updated_at"]
        widgets = {
            "data_nascimento": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "hora_nascimento": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),
            "alergias": forms.Textarea(attrs={"rows": 3}),
            "condicoes_medicas_gerais": forms.Textarea(attrs={"rows": 3}),
            "numero_iniciatico": forms.TextInput(attrs={"class": "form-control"}),
            "nome_iniciatico": forms.TextInput(attrs={"class": "form-control"}),
        }


class RegistroHistoricoForm(forms.ModelForm):
    """Formulário para adicionar e editar registros do histórico de um aluno."""

    class Meta:
        model = RegistroHistorico
        fields = [
            "codigo",
            "data_os",
            "ordem_servico",
            "numero_iniciatico",
            "nome_iniciatico",
            "observacoes",
        ]
        widgets = {
            "codigo": forms.Select(attrs={"class": "form-control django-select2"}),
            "data_os": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "ordem_servico": forms.TextInput(attrs={"class": "form-control"}),
            "numero_iniciatico": forms.TextInput(attrs={"class": "form-control"}),
            "nome_iniciatico": forms.TextInput(attrs={"class": "form-control"}),
            "observacoes": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["codigo"].queryset = Codigo.objects.order_by("tipo_codigo", "nome")


# Usando inlineformset_factory para vincular o histórico diretamente ao aluno
RegistroHistoricoFormSet = forms.inlineformset_factory(
    Aluno,
    RegistroHistorico,
    form=RegistroHistoricoForm,
    extra=1,  # Sempre começa com 1 formulário extra para facilitar adição
    can_delete=True,  # Permite a exclusão de registros
    edit_only=False,
    min_num=0,  # Mínimo de 0 formulários obrigatórios
    max_num=20,  # Máximo de 20 registros históricos
    validate_min=False,  # Não força o mínimo
    validate_max=True,  # Valida o máximo
)
