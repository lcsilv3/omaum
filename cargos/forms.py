from django import forms
from .models import CargoAdministrativo

class CargoAdministrativoForm(forms.ModelForm):
    """
    Formulário para criação e edição de Cargos Administrativos.
    """
    class Meta:
        model = CargoAdministrativo
        fields = ['codigo_cargo', 'nome', 'descricao']
        widgets = {
            'codigo_cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'codigo_cargo': 'Código do Cargo',
            'nome': 'Nome',
            'descricao': 'Descrição',
        }
        help_texts = {
            'codigo_cargo': 'Código único que identifica o cargo (ex: COORD, DIR, etc.)',
            'nome': 'Nome completo do cargo administrativo',
            'descricao': 'Descrição detalhada das responsabilidades do cargo',
        }
        error_messages = {
            'codigo_cargo': {
                'unique': 'Este código de cargo já está em uso. Por favor, escolha outro.',
                'required': 'O código do cargo é obrigatório.',
                'max_length': 'O código do cargo não pode ter mais de 10 caracteres.',
            },
            'nome': {
                'required': 'O nome do cargo é obrigatório.',
                'max_length': 'O nome do cargo não pode ter mais de 100 caracteres.',
            },
        }

    def clean_codigo_cargo(self):
        """
        Validação personalizada para o campo codigo_cargo.
        Converte o código para maiúsculas e remove espaços extras.
        """
        codigo = self.cleaned_data.get('codigo_cargo')
        if codigo:
            return codigo.upper().strip()
        return codigo

    def clean_nome(self):
        """
        Validação personalizada para o campo nome.
        Capitaliza a primeira letra de cada palavra e remove espaços extras.
        """
        nome = self.cleaned_data.get('nome')
        if nome:
            return ' '.join(word.capitalize() for word in nome.split())
        return nome
