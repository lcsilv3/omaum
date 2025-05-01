print("ARQUIVO FORMS.PY CARREGADO")
from django import forms
from django.core.validators import RegexValidator
from importlib import import_module

# resto do código...


def get_atividade_academica_model():
    try:
        atividades_module = import_module("atividades.models")
        return getattr(atividades_module, "AtividadeAcademica")
    except (ImportError, AttributeError):
        return None


def get_atividade_ritualistica_model():
    try:
        atividades_module = import_module("atividades.models")
        return getattr(atividades_module, "AtividadeRitualistica")
    except (ImportError, AttributeError):
        return None


class AtividadeAcademicaForm(forms.ModelForm):
    todas_turmas = forms.BooleanField(
        required=False, 
        label="Aplicar a todas as turmas ativas", 
        initial=False
    )
    
    class Meta:
        model = get_atividade_academica_model()
        fields = ["nome", "descricao", "data_inicio", "data_fim", "turmas", "responsavel", 
                  "local", "tipo_atividade", "status"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "data_inicio": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "data_fim": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "turmas": forms.SelectMultiple(attrs={"class": "form-control"}),
            "responsavel": forms.TextInput(attrs={"class": "form-control"}),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "tipo_atividade": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tornar o campo turmas não obrigatório, já que pode ser preenchido automaticamente
        self.fields['turmas'].required = False
        
        # Converter o formato da data para YYYY-MM-DD se estiver editando uma atividade existente
        if self.instance and self.instance.pk and self.instance.data_inicio:
            # Converter para o formato esperado pelo input type="date"
            self.initial['data_inicio'] = self.instance.data_inicio.strftime('%Y-%m-%d')
            if self.instance.data_fim:
                self.initial['data_fim'] = self.instance.data_fim.strftime('%Y-%m-%d')


class AtividadeRitualisticaForm(forms.ModelForm):
    todos_alunos = forms.BooleanField(
        required=False, label="Incluir todos os alunos da turma", initial=False
    )

    class Meta:
        model = get_atividade_ritualistica_model()
        fields = [
            "nome",
            "descricao",
            "data",
            "hora_inicio",
            "hora_fim",
            "local",
            "turma",
            "participantes",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "data": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "hora_inicio": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "hora_fim": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "turma": forms.Select(attrs={"class": "form-control"}),
            "participantes": forms.SelectMultiple(
                attrs={"class": "form-control"}
            ),
        }


def criar_form_atividade_academica():
    return AtividadeAcademicaForm


def criar_form_atividade_ritualistica():
    return AtividadeRitualisticaForm
