"""
Formulários para o aplicativo de pagamentos.
"""

from django import forms
from django.utils import timezone
from importlib import import_module

from .models import Pagamento  # <-- Adicione esta linha


def get_aluno_model():
    """Importa o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


class PagamentoForm(forms.ModelForm):
    """Formulário para criação e edição de pagamentos."""

    class Meta:
        model = Pagamento
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Aluno = get_aluno_model()
        self.fields["aluno"].queryset = Aluno.objects.filter(situacao="ATIVO")

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        data_pagamento = cleaned_data.get("data_pagamento")

        # Se o status for PAGO, a data de pagamento é obrigatória
        if status == "PAGO" and not data_pagamento:
            self.add_error(
                "data_pagamento",
                "A data de pagamento é obrigatória quando o status é Pago.",
            )

        # Se o status não for PAGO, a data de pagamento deve ser None
        if status != "PAGO" and data_pagamento:
            cleaned_data["data_pagamento"] = None

        return cleaned_data


class PagamentoRapidoForm(forms.ModelForm):
    """Formulário simplificado para registro rápido de pagamentos."""

    aluno_cpf = forms.CharField(
        label="CPF do Aluno",
        max_length=11,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Digite o CPF do aluno"}
        ),
    )

    class Meta:
        from .models import Pagamento

        model = Pagamento
        fields = [
            "valor",
            "data_vencimento",
            "status",
            "metodo_pagamento",
            "observacoes",
        ]
        widgets = {
            "valor": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "min": "0"}
            ),
            "data_vencimento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
            "metodo_pagamento": forms.Select(attrs={"class": "form-control"}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Definir valores padrão
        self.fields["data_vencimento"].initial = timezone.now().date()
        self.fields["status"].initial = "PENDENTE"

    def clean_aluno_cpf(self):
        cpf = self.cleaned_data.get("aluno_cpf")
        if cpf:
            # Remover caracteres não numéricos
            cpf = "".join(filter(str.isdigit, cpf))

            # Verificar se o CPF tem 11 dígitos
            if len(cpf) != 11:
                raise forms.ValidationError("O CPF deve conter 11 dígitos.")

            # Verificar se o aluno existe
            Aluno = get_aluno_model()
            try:
                aluno = Aluno.objects.get(cpf=cpf)
                return aluno
            except Aluno.DoesNotExist:
                raise forms.ValidationError("Aluno não encontrado com este CPF.")

        return cpf

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.aluno = self.cleaned_data.get("aluno_cpf")

        if commit:
            instance.save()

        return instance


class FiltroPagamentosForm(forms.Form):
    """
    Formulário para filtrar pagamentos.
    """

    q = forms.CharField(
        required=False,
        label="Buscar",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Buscar por aluno, CPF ou observações...",
            }
        ),
    )

    status = forms.ChoiceField(
        choices=[("", "Todos")] + list(Pagamento.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    data_inicio = forms.DateField(
        required=False,
        label="Data início",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

    data_fim = forms.DateField(
        required=False,
        label="Data fim",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
