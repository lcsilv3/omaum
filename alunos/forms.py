from django import forms
from alunos.models import Aluno, RegistroHistorico, Estado, Codigo, TipoCodigo
from django_select2.forms import ModelSelect2Widget


class AlunoForm(forms.ModelForm):
    # Substituir widgets de cidade_ref e bairro_ref por AJAX
    cidade_ref = forms.ModelChoiceField(
        queryset=None,
        required=False,
        widget=ModelSelect2Widget(
            model=Aluno._meta.get_field("cidade_ref").related_model,
            search_fields=["nome__icontains"],
            attrs={"data-placeholder": "Busque a cidade..."},
        ),
        label="Cidade (Ref)",
    )
    bairro_ref = forms.ModelChoiceField(
        queryset=None,
        required=False,
        widget=ModelSelect2Widget(
            model=Aluno._meta.get_field("bairro_ref").related_model,
            search_fields=["nome__icontains"],
            attrs={"data-placeholder": "Busque o bairro..."},
        ),
        label="Bairro (Ref)",
    )
    grau_atual_automatico = forms.CharField(
        label="Grau Atual (automático)",
        required=False,
        widget=forms.TextInput(
            attrs={
                "readonly": "readonly",
                "class": "form-control-plaintext",
                "tabindex": "-1",
                "style": "background: #f8f9fa; color: #333; font-weight: bold;",
            }
        ),
    )
    """Formulário simplificado para criação e edição de alunos."""

    class Meta:
        model = Aluno
        fields = [
            # Identificação
            "nome",
            "cpf",
            "email",
            "foto",
            "data_nascimento",
            "hora_nascimento",
            "sexo",
            "situacao",
            # Iniciáticos
            "numero_iniciatico",
            "nome_iniciatico",
            "grau_atual_automatico",
            "grau_atual",
            "situacao_iniciatica",
            # Nacionalidade / Naturalidade (novos + legacy)
            "pais_nacionalidade",
            "cidade_naturalidade",
            "nacionalidade",
            "naturalidade",
            # Endereço
            "rua",
            "numero_imovel",
            "complemento",
            "bairro",
            "cidade",
            "estado",
            "cep",
            "cidade_ref",
            "bairro_ref",
            # Contatos
            "nome_primeiro_contato",
            "celular_primeiro_contato",
            "tipo_relacionamento_primeiro_contato",
            "nome_segundo_contato",
            "celular_segundo_contato",
            "tipo_relacionamento_segundo_contato",
            # Outros pessoais
            "estado_civil",
            "profissao",
            "ativo",
            # Médicos
            "tipo_sanguineo",
            "alergias",
            "condicoes_medicas_gerais",
            "convenio_medico",
            "hospital",
        ]
        widgets = {
            "data_nascimento": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "hora_nascimento": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),
            "numero_iniciatico": forms.TextInput(attrs={"class": "form-control"}),
            "nome_iniciatico": forms.TextInput(attrs={"class": "form-control"}),
            "grau_atual": forms.TextInput(attrs={"class": "form-control"}),
            "situacao_iniciatica": forms.Select(attrs={"class": "form-control"}),
            "tipo_sanguineo": forms.Select(attrs={"class": "form-control"}),
            "alergias": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "condicoes_medicas_gerais": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }

    def _add_selecione_to_selects(self):
        # Adiciona a opção 'Selecione' a todos os campos Select
        for field in self.fields.values():
            if not isinstance(field.widget, forms.Select):
                continue
            base_choices = []
            if hasattr(field, "choices"):
                base_choices = list(field.choices)  # type: ignore[attr-defined]
            if not base_choices and hasattr(field.widget, "choices"):
                base_choices = list(field.widget.choices)
            base_choices = [
                c
                for c in base_choices
                if not (
                    isinstance(c, (list, tuple))
                    and len(c) >= 2
                    and c[0] == ""
                    and str(c[1]).lower() == "selecione"
                )
            ]
            nova_lista = [("", "Selecione")] + base_choices
            field.widget.choices = nova_lista  # type: ignore[attr-defined]
            if hasattr(field, "choices"):
                field.choices = nova_lista  # type: ignore[attr-defined]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajusta queryset dos widgets AJAX
        if "cidade_ref" in self.fields:
            self.fields["cidade_ref"].queryset = self.fields[
                "cidade_ref"
            ].widget.model.objects.all()
        if "bairro_ref" in self.fields:
            self.fields["bairro_ref"].queryset = self.fields[
                "bairro_ref"
            ].widget.model.objects.all()
        # Datas
        if self.instance and self.instance.pk and self.instance.data_nascimento:
            self.initial["data_nascimento"] = self.instance.data_nascimento.strftime(
                "%Y-%m-%d"
            )
        # Grau automático
        self.fields["grau_atual_automatico"].initial = (
            self.instance.grau_atual_automatico
            if self.instance and self.instance.pk
            else "Não informado"
        )
        # Placeholders
        placeholders = {
            "cpf": "___.___.___-__",
            # Novo formato de CEP com ponto após 2 dígitos: 00.000-000
            "cep": "__.___-___",
            "celular_primeiro_contato": "(99) 99999-9999",
            "celular_segundo_contato": "(99) 99999-9999",
            "email": "usuario@exemplo.com",
        }
        for (
            field_name,
            field,
        ) in self.fields.items():  # field_name usado para placeholders
            if not field.widget.attrs.get("class"):
                field.widget.attrs["class"] = "form-control"
            if field_name in placeholders:
                field.widget.attrs.setdefault("placeholder", placeholders[field_name])
        # CEP: permitir máscara com hífen (99999-999 -> 9 caracteres). O modelo armazena 8 dígitos limpos.
        if "cep" in self.fields:
            # Aumenta limite para incluir ponto e hífen (00.000-000 -> 10 chars visuais)
            self.fields[
                "cep"
            ].max_length = 10  # somente apresentação; modelo continua 8 dígitos
            self.fields["cep"].widget.attrs["maxlength"] = "10"
        # Campos referência exibidos em modo avançado: usar css helper
        for ref_field in ["cidade_ref", "bairro_ref"]:
            if ref_field in self.fields:
                self.fields[ref_field].widget.attrs.setdefault(
                    "class", "form-select text-muted"
                )
                self.fields[ref_field].required = False
        # Label
        if "rua" in self.fields:
            self.fields["rua"].label = "Endereço"
        # Estado como select
        # Otimização: só carrega estados se realmente houver campo e só busca os campos necessários
        if "estado" in self.fields:
            estados_qs = Estado.objects.only("id", "codigo", "nome").order_by("nome")
            escolha_estado = [(e.codigo, f"{e.nome} ({e.codigo})") for e in estados_qs]
            inicial = self.fields["estado"].initial
            self.fields["estado"] = forms.ChoiceField(
                choices=[("", "Selecione")] + escolha_estado,
                required=False,
                widget=forms.Select(attrs={"class": "form-select"}),
                label=self.fields["estado"].label,
                initial=inicial,
            )
            self.estado_codigo_to_id = {e.codigo: e.id for e in estados_qs}
        # Email pattern
        if "email" in self.fields:
            self.fields["email"].widget.attrs.setdefault(
                "pattern", r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
            )
        # Selects adicionam 'Selecione'
        self._add_selecione_to_selects()
        # Após adicionar selects, se campo estado existir, injeta data-id em cada option via atributo 'data-ids-json'
        if "estado" in self.fields:
            # Serializa mapping para uso em template/JS
            mapping = {e.codigo: e.id for e in Estado.objects.all()}
            self.fields["estado"].widget.attrs["data-mapping-json"] = mapping

    # Limpeza de campos com máscaras
    def clean_cpf(self):
        v = self.cleaned_data.get("cpf", "")
        return v.replace(".", "").replace("-", "")

    def clean_celular_primeiro_contato(self):
        v = self.cleaned_data.get("celular_primeiro_contato") or ""
        return "".join(filter(str.isdigit, v))

    def clean_celular_segundo_contato(self):
        v = self.cleaned_data.get("celular_segundo_contato") or ""
        return "".join(filter(str.isdigit, v))

    def clean_cep(self):
        v = self.cleaned_data.get("cep", "")
        if not v:
            return ""
        return v.replace("-", "").replace(".", "")


# Manter formulário original para compatibilidade durante migração
class RegistroHistoricoForm(forms.ModelForm):
    def clean_ordem_servico(self):
        """Garante que o ano da ordem de serviço seja sempre salvo com 4 dígitos."""
        valor = self.cleaned_data.get("ordem_servico", "")
        if not valor:
            return valor
        import re

        match = re.match(r"^(\S+)/(\d{2,4})$", valor)
        if not match:
            raise forms.ValidationError(
                "Formato inválido. Use XXXX/AAAA, onde AAAA é o ano."
            )
        prefixo, ano = match.groups()
        if len(ano) == 2:
            # Converte para 4 dígitos (ex: 25 -> 2025, 99 -> 1999, lógica pode ser ajustada)
            ano_int = int(ano)
            ano = f"20{ano}" if ano_int < 50 else f"19{ano}"
        elif len(ano) == 4:
            ano_int = int(ano)
            if ano_int < 1900 or ano_int > 2100:
                raise forms.ValidationError("Ano inválido na ordem de serviço.")
        else:
            raise forms.ValidationError("Ano inválido na ordem de serviço.")
        return f"{prefixo}/{ano}"

    """Formulário para registros históricos - mantido para compatibilidade."""

    # Campo auxiliar (não pertence ao modelo) para o usuário filtrar códigos por tipo.
    tipo_codigo = forms.ModelChoiceField(
        queryset=TipoCodigo.objects.all(),
        required=False,
        label="Tipo",
        widget=forms.Select(
            attrs={
                "class": "form-control tipo-codigo-select",
            }
        ),
        help_text="Selecione primeiro um tipo para filtrar os códigos",
    )

    class Meta:
        model = RegistroHistorico
        fields = [
            # Campo extra (UI) - inserido antes de 'codigo'
            # será ordenado via order_fields no __init__
            # 'tipo_codigo' não é campo de modelo
            "codigo",
            "data_os",
            "ordem_servico",
            "numero_iniciatico",
            "nome_iniciatico",
            "observacoes",
        ]
        widgets = {
            "codigo": forms.Select(
                attrs={
                    "class": "form-control codigo-select",
                    # Será habilitado dinamicamente quando um tipo for escolhido (para novos forms)
                }
            ),
            "data_os": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "ordem_servico": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "____/____"}
            ),
            "numero_iniciatico": forms.TextInput(attrs={"class": "form-control"}),
            "nome_iniciatico": forms.TextInput(attrs={"class": "form-control"}),
            "observacoes": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Otimização: carrega apenas os campos necessários para o select
        self.fields["tipo_codigo"].queryset = TipoCodigo.objects.all()
        self.fields["codigo"].queryset = Codigo.objects.all()
        # Widget simples, populado via JS customizado
        self.fields["codigo"].widget = forms.Select(
            attrs={"class": "form-control codigo-select"}
        )

        # Se já houver um código selecionado (edição), preencher o tipo inicial
        codigo_obj = (
            self.instance.codigo if getattr(self.instance, "codigo_id", None) else None
        )
        if codigo_obj and codigo_obj.tipo_codigo_id:
            self.fields["tipo_codigo"].initial = codigo_obj.tipo_codigo_id

        # Ordem dos campos no form (inserir tipo antes de código)
        desired = [
            "tipo_codigo",
            "codigo",
            "ordem_servico",
            "data_os",
            "numero_iniciatico",
            "nome_iniciatico",
            "observacoes",
        ]
        self.order_fields(desired)


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
