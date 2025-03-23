from django import forms
from alunos.models import Aluno  # Corrigido: importar do módulo alunos
from django.core.exceptions import ValidationError


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = [
            'cpf', 'nome', 'data_nascimento', 'hora_nascimento', 'email', 
            'sexo', 'nacionalidade', 'naturalidade', 'rua', 'numero_imovel', 
            'cidade', 'estado', 'bairro', 'cep', 'nome_primeiro_contato', 
            'celular_primeiro_contato', 'tipo_relacionamento_primeiro_contato', 
            'nome_segundo_contato', 'celular_segundo_contato', 
            'tipo_relacionamento_segundo_contato', 'tipo_sanguineo', 'fator_rh',
            'curso'
        ]
        # Você pode adicionar widgets personalizados aqui se necessário

    def clean(self):
        cleaned_data = super().clean()
        # Adicionar validações cruzadas aqui se necessário
        return cleaned_data


class ImportForm(forms.Form):
    file = forms.FileField()
