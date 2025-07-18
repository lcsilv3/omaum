from django import forms
from alunos.models import Aluno, RegistroHistorico, Codigo


class AlunoForm(forms.ModelForm):
    grau_atual_automatico = forms.CharField(
        label="Grau Atual (automático)",
        required=False,
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
            'class': 'form-control-plaintext',
            'tabindex': '-1',
            'style': 'background: #f8f9fa; color: #333; font-weight: bold;',
        })
    )
    """Formulário simplificado para criação e edição de alunos."""
    
    # Campos para adicionar novo evento ao histórico
    novo_evento_tipo = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: CARGO, INICIAÇÃO, PUNIÇÃO'}),
        label="Tipo do Evento"
    )
    novo_evento_descricao = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição do evento'}),
        label="Descrição do Evento"
    )
    novo_evento_data = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Data do Evento"
    )
    novo_evento_observacoes = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Observações (opcional)'}),
        label="Observações"
    )

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

        # Preencher campo automático
        if self.instance and self.instance.pk:
            self.fields['grau_atual_automatico'].initial = self.instance.grau_atual_automatico
        else:
            self.fields['grau_atual_automatico'].initial = "Não informado"

        # Adiciona classes CSS e placeholders
        placeholders = {
            "cpf": "Somente números",
            "cep": "Somente números",
            "celular_primeiro_contato": "Somente números",
            "celular_segundo_contato": "Somente números",
        }
        for field_name, field in self.fields.items():
            if not field.widget.attrs.get('class'):
                field.widget.attrs["class"] = "form-control"
            if field_name in placeholders:
                field.widget.attrs["placeholder"] = placeholders[field_name]

    def save(self, commit=True):
        """Salva o aluno e adiciona evento ao histórico se preenchido."""
        instance = super().save(commit=False)
        
        # Adicionar novo evento se todos os campos obrigatórios estiverem preenchidos
        if (
            self.cleaned_data.get('novo_evento_tipo') and
            self.cleaned_data.get('novo_evento_descricao') and
            self.cleaned_data.get('novo_evento_data')
        ):
            
            if commit:
                instance.save()  # Salva primeiro para garantir que tem ID
                instance.adicionar_evento_historico(
                    tipo=self.cleaned_data['novo_evento_tipo'],
                    descricao=self.cleaned_data['novo_evento_descricao'],
                    data=self.cleaned_data['novo_evento_data'],
                    observacoes=self.cleaned_data.get('novo_evento_observacoes', '')
                )
        elif commit:
            instance.save()
        
        return instance

    class Meta:
        model = Aluno
        fields = [
            "nome", "cpf", "email", "celular_primeiro_contato", "data_nascimento", "sexo", "estado_civil",
            "nome_iniciatico", "numero_iniciatico", "grau_atual_automatico", "grau_atual", "situacao_iniciatica",
            "rua", "cidade", "estado", "cep"
        ]
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
            "grau_atual": forms.TextInput(attrs={"class": "form-control"}),
            "situacao_iniciatica": forms.Select(attrs={"class": "form-control"}),
        }

    def _add_selecione_to_selects(self):
        # Adiciona a opção 'Selecione' a todos os campos Select
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Select) and not field.required:
                field.choices = [('', 'Selecione')] + list(field.choices)
            elif isinstance(field.widget, forms.Select) and field.required:
                # Se for required, ainda assim força 'Selecione' como primeira opção
                field.choices = [('', 'Selecione')] + [c for c in field.choices if c[0] != '']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ...existing code...
        self._add_selecione_to_selects()


# Manter formulário original para compatibilidade durante migração
class RegistroHistoricoForm(forms.ModelForm):
    """Formulário para registros históricos - mantido para compatibilidade."""

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


# Manter formset para compatibilidade durante migração
RegistroHistoricoFormSet = forms.inlineformset_factory(
    Aluno,
    RegistroHistorico,
    form=RegistroHistoricoForm,
    extra=1,
    can_delete=True,
    edit_only=False,
    min_num=0,
    max_num=20,
    validate_min=False,
    validate_max=True,
)
