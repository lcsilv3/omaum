from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Importar a função utilitária centralizada
from .utils import get_model_dynamically

# Substituir a função get_model pela função utilitária centralizada
get_model = get_model_dynamically


class AlunoForm(forms.ModelForm):
    class Meta:
        model = get_model("alunos", "Aluno")
        fields = (
            "cpf",
            "nome",
            "data_nascimento",
            "hora_nascimento",
            "email",
            "foto",
            "sexo",
            "situacao",
            "numero_iniciatico",
            "nome_iniciatico",
            "nacionalidade",
            "naturalidade",
            "rua",
            "numero_imovel",
            "complemento",
            "bairro",
            "cidade",
            "estado",
            "cep",
            "nome_primeiro_contato",
            "celular_primeiro_contato",
            "tipo_relacionamento_primeiro_contato",
            "nome_segundo_contato",
            "celular_segundo_contato",
            "tipo_relacionamento_segundo_contato",
            "tipo_sanguineo",
            "fator_rh",
            "alergias",
            "condicoes_medicas_gerais",
            "convenio_medico",
            "hospital",
        )
        widgets = {
            "data_nascimento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "hora_nascimento": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
        }


class CursoForm(forms.ModelForm):
    class Meta:
        model = get_model("cursos", "Curso")
        fields = ("codigo_curso", "nome", "descricao", "duracao")
        widgets = {
            "codigo_curso": forms.NumberInput(
                attrs={"class": "form-control", "min": "1"}
            ),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "duracao": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
        }


class TurmaForm(forms.ModelForm):
    class Meta:
        model = get_model("turmas", "Turma")
        fields = [
            "nome",
            "curso",
            "vagas",
            "status",
            "data_inicio",
            "data_fim",
            "instrutor",
            "instrutor_auxiliar",
            "auxiliar_instrucao",
            "dias_semana",
            "local",
            "horario",
            "descricao",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "curso": forms.Select(attrs={"class": "form-select"}),
            "vagas": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "data_inicio": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "data_fim": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "instrutor": forms.Select(attrs={"class": "form-control"}),
            "instrutor_auxiliar": forms.Select(attrs={"class": "form-control"}),
            "auxiliar_instrucao": forms.Select(attrs={"class": "form-control"}),
            "dias_semana": forms.TextInput(attrs={"class": "form-control"}),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "horario": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class AtividadeAcademicaForm(forms.ModelForm):
    class Meta:
        model = get_model("atividades", "AtividadeAcademica")
        fields = [
            "nome",
            "descricao",
            "data_inicio",
            "data_fim",
            "turma",
            "responsavel",
            "local",
            "tipo_atividade",
            "status",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "data_inicio": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "data_fim": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "turma": forms.Select(attrs={"class": "form-control"}),
            "responsavel": forms.TextInput(attrs={"class": "form-control"}),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "tipo_atividade": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class AtividadeRitualisticaForm(forms.ModelForm):
    todos_alunos = forms.BooleanField(
        required=False, label="Incluir todos os alunos da turma", initial=False
    )

    class Meta:
        model = get_model("atividades", "AtividadeRitualistica")
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
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "data": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "hora_inicio": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "hora_fim": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "turma": forms.Select(attrs={"class": "form-control"}),
            "participantes": forms.SelectMultiple(attrs={"class": "form-control"}),
        }


class PresencaForm(forms.ModelForm):
    class Meta:
        model = get_model("presencas", "Presenca")
        fields = ["aluno", "turma", "data", "status"]
        widgets = {
            "data": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class FrequenciaForm(forms.ModelForm):
    class Meta:
        model = get_model("frequencias", "Frequencia")
        fields = ["aluno", "atividade", "data", "presente", "justificativa"]
        widgets = {
            "aluno": forms.Select(attrs={"class": "form-select"}),
            "atividade": forms.Select(attrs={"class": "form-select"}),
            "data": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "presente": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "justificativa": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }


class IniciacaoForm(forms.ModelForm):
    class Meta:
        model = get_model("iniciacoes", "Iniciacao")
        fields = ["aluno", "curso", "data_iniciacao", "grau", "observacoes"]
        widgets = {
            "data_iniciacao": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "aluno": forms.Select(attrs={"class": "form-control"}),
            "curso": forms.Select(attrs={"class": "form-control"}),
            "grau": forms.TextInput(attrs={"class": "form-control"}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class PunicaoForm(forms.ModelForm):
    class Meta:
        model = get_model("punicoes", "Punicao")
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
            "motivo": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class CargoAdministrativoForm(forms.ModelForm):
    class Meta:
        model = get_model("cargos", "CargoAdministrativo")
        fields = ["codigo_cargo", "nome", "descricao"]
        widgets = {
            "codigo_cargo": forms.TextInput(attrs={"class": "form-control"}),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class RelatorioForm(forms.ModelForm):
    class Meta:
        model = get_model("relatorios", "Relatorio")
        fields = ["titulo", "conteudo"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "conteudo": forms.Textarea(attrs={"class": "form-control"}),
        }


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ConfiguracaoSistemaForm(forms.ModelForm):
    class Meta:
        model = get_model("core", "ConfiguracaoSistema")
        fields = [
            "nome_sistema",
            "versao",
            "manutencao_ativa",
            "mensagem_manutencao",
        ]
        widgets = {
            "nome_sistema": forms.TextInput(attrs={"class": "form-control"}),
            "versao": forms.TextInput(attrs={"class": "form-control"}),
            "manutencao_ativa": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "mensagem_manutencao": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }
