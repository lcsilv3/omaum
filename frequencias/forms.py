from django import forms
from django.utils import timezone
from importlib import import_module


def get_models():
    """Obtém os modelos FrequenciaMensal e Carencia."""
    frequencias_module = import_module("frequencias.models")
    FrequenciaMensal = getattr(frequencias_module, "FrequenciaMensal")
    Carencia = getattr(frequencias_module, "Carencia")
    return FrequenciaMensal, Carencia


def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


class FrequenciaMensalForm(forms.ModelForm):
    """Formulário para criação e edição de frequência mensal."""

    class Meta:
        FrequenciaMensal, _ = get_models()
        model = FrequenciaMensal
        fields = ["turma", "mes", "ano", "percentual_minimo"]
        widgets = {
            "percentual_minimo": forms.NumberInput(
                attrs={"class": "form-control", "min": "0", "max": "100"}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configurar campos
        self.fields["turma"].queryset = get_turma_model().objects.filter(status="A")
        self.fields["turma"].widget.attrs.update({"class": "form-control select2"})

        self.fields["mes"].widget.attrs.update({"class": "form-control"})

        # Definir ano padrão como o atual
        if not self.instance.pk:
            self.fields["ano"].initial = timezone.now().year

        self.fields["ano"].widget.attrs.update(
            {"class": "form-control", "min": "2000", "max": "2100"}
        )

    def clean(self):
        cleaned_data = super().clean()
        turma = cleaned_data.get("turma")
        mes = cleaned_data.get("mes")
        ano = cleaned_data.get("ano")

        # Validar se já existe frequência para esta turma/mês/ano
        if turma and mes and ano:
            FrequenciaMensal, _ = get_models()

            # Verificar se já existe, excluindo a instância atual em caso de edição
            query = FrequenciaMensal.objects.filter(turma=turma, mes=mes, ano=ano)
            if self.instance.pk:
                query = query.exclude(pk=self.instance.pk)

            if query.exists():
                self.add_error(
                    None, "Já existe uma frequência mensal para esta turma, mês e ano."
                )

        return cleaned_data


class FiltroPainelFrequenciasForm(forms.Form):
    """Formulário para filtrar o painel de frequências."""

    turma = forms.ModelChoiceField(
        label="Turma",
        queryset=get_turma_model().objects.filter(status="A"),
        widget=forms.Select(attrs={"class": "form-control select2"}),
    )

    mes_inicio = forms.ChoiceField(
        label="Mês Inicial",
        choices=get_models()[0].MES_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    ano_inicio = forms.IntegerField(
        label="Ano Inicial",
        initial=timezone.now().year,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "min": "2000", "max": "2100"}
        ),
    )

    mes_fim = forms.ChoiceField(
        label="Mês Final",
        choices=get_models()[0].MES_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    ano_fim = forms.IntegerField(
        label="Ano Final",
        initial=timezone.now().year,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "min": "2000", "max": "2100"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        mes_inicio = int(cleaned_data.get("mes_inicio", 1))
        ano_inicio = cleaned_data.get("ano_inicio")
        mes_fim = int(cleaned_data.get("mes_fim", 12))
        ano_fim = cleaned_data.get("ano_fim")

        # Validar período
        if ano_inicio and ano_fim:
            data_inicio = ano_inicio * 12 + mes_inicio
            data_fim = ano_fim * 12 + mes_fim

            if data_fim < data_inicio:
                self.add_error(
                    None, "O período final deve ser posterior ao período inicial."
                )

        return cleaned_data
