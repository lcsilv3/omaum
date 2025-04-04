from django import forms
from django.core.validators import RegexValidator
from importlib import import_module

def get_aluno_model():
    alunos_module = import_module('alunos.models')
    return getattr(alunos_module, 'Aluno')

class AlunoForm(forms.ModelForm):
    """
    Formulário para criação e edição de alunos.
    """
    # Validadores personalizados
    cpf_validator = RegexValidator(
        r'^\d{11}$',
        'O CPF deve conter exatamente 11 dígitos numéricos.'
    )
    
    # Campos com validação adicional
    cpf = forms.CharField(
        validators=[cpf_validator],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Somente números'})
    )
    
    class Meta:
        model = get_aluno_model()
        fields = [
            'cpf', 'nome', 'data_nascimento', 'hora_nascimento', 'email', 'foto', 'sexo',
            'numero_iniciatico', 'nome_iniciatico',
            'nacionalidade', 'naturalidade',
            'rua', 'numero_imovel', 'complemento', 'bairro', 'cidade', 'estado', 'cep',
            'nome_primeiro_contato', 'celular_primeiro_contato', 'tipo_relacionamento_primeiro_contato',
            'nome_segundo_contato', 'celular_segundo_contato', 'tipo_relacionamento_segundo_contato',
            'tipo_sanguineo', 'fator_rh', 'alergias', 'condicoes_medicas_gerais', 'convenio_medico', 'hospital'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_nascimento': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'numero_iniciatico': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_iniciatico': forms.TextInput(attrs={'class': 'form-control'}),
            'nacionalidade': forms.TextInput(attrs={'class': 'form-control', 'value': 'Brasileira'}),
            'naturalidade': forms.TextInput(attrs={'class': 'form-control'}),
            'rua': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_imovel': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Somente números'}),
            'nome_primeiro_contato': forms.TextInput(attrs={'class': 'form-control'}),
            'celular_primeiro_contato': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_relacionamento_primeiro_contato': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_segundo_contato': forms.TextInput(attrs={'class': 'form-control'}),
            'celular_segundo_contato': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_relacionamento_segundo_contato': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_sanguineo': forms.TextInput(attrs={'class': 'form-control'}),
            'fator_rh': forms.Select(attrs={'class': 'form-control'}),
            'alergias': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'condicoes_medicas_gerais': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'convenio_medico': forms.TextInput(attrs={'class': 'form-control'}),
            'hospital': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'cpf': 'CPF',
            'nome': 'Nome Completo',
            'data_nascimento': 'Data de Nascimento',
            'hora_nascimento': 'Hora de Nascimento',
            'email': 'E-mail',
            'foto': 'Foto',
            'sexo': 'Sexo',
            'numero_iniciatico': 'Número Iniciático',
            'nome_iniciatico': 'Nome Iniciático',
            'nacionalidade': 'Nacionalidade',
            'naturalidade': 'Naturalidade',
            'rua': 'Rua',
            'numero_imovel': 'Número',
            'complemento': 'Complemento',
            'bairro': 'Bairro',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'cep': 'CEP',
            'nome_primeiro_contato': 'Nome do Primeiro Contato',
            'celular_primeiro_contato': 'Celular do Primeiro Contato',
            'tipo_relacionamento_primeiro_contato': 'Relacionamento',
            'nome_segundo_contato': 'Nome do Segundo Contato',
            'celular_segundo_contato': 'Celular do Segundo Contato',
            'tipo_relacionamento_segundo_contato': 'Relacionamento',
            'tipo_sanguineo': 'Tipo Sanguíneo',
            'fator_rh': 'Fator RH',
            'alergias': 'Alergias',
            'condicoes_medicas_gerais': 'Condições Médicas',
            'convenio_medico': 'Convênio Médico',
            'hospital': 'Hospital de Preferência',
        }
        help_texts = {
            'cpf': 'Digite apenas os 11 números do CPF, sem pontos ou traços.',
            'data_nascimento': 'Formato: DD/MM/AAAA',
            'hora_nascimento': 'Formato: HH:MM',
            'numero_iniciatico': 'Número único de identificação do iniciado.',
            'cep': 'Digite apenas os 8 números do CEP, sem hífen.',
            'tipo_sanguineo': 'Ex: A, B, AB, O',
            'fator_rh': 'Positivo (+) ou Negativo (-)',
            'alergias': 'Liste todas as alergias conhecidas. Deixe em branco se não houver.',
            'condicoes_medicas_gerais': 'Descreva condições médicas relevantes. Deixe em branco se não houver.',
        }
    
    def clean_cpf(self):
        """Validação personalizada para o campo CPF."""
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            # Remove caracteres não numéricos
            cpf = ''.join(filter(str.isdigit, cpf))
            
            # Verifica se tem 11 dígitos
            if len(cpf) != 11:
                raise forms.ValidationError('O CPF deve conter exatamente 11 dígitos.')
            
            # Aqui você poderia adicionar uma validação mais complexa do CPF
            # como verificar os dígitos verificadores
            
        return cpf
    
    def clean_nome(self):
        """Validação personalizada para o campo nome."""
        nome = self.cleaned_data.get('nome')
        if nome:
            # Capitaliza a primeira letra de cada palavra
            nome = ' '.join(word.capitalize() for word in nome.split())
        return nome
    
    def clean_email(self):
        """Validação personalizada para o campo email."""
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()  # Converte para minúsculas
            
            # Verifica se o email já existe (exceto para o próprio registro em caso de edição)
            Aluno = get_aluno_model()
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                if Aluno.objects.filter(email=email).exclude(pk=instance.pk).exists():
                    raise forms.ValidationError('Este e-mail já está em uso por outro aluno.')
            else:
                if Aluno.objects.filter(email=email).exists():
                    raise forms.ValidationError('Este e-mail já está em uso.')
        return email
    
    def clean_cep(self):
        """Validação personalizada para o campo CEP."""
        cep = self.cleaned_data.get('cep')
        if cep:
            # Remove caracteres não numéricos
            cep = ''.join(filter(str.isdigit, cep))
            
            # Verifica se tem 8 dígitos
            if len(cep) != 8:
                raise forms.ValidationError('O CEP deve conter exatamente 8 dígitos.')
        return cep
    
    def clean(self):
        """Validação global do formulário."""
        cleaned_data = super().clean()
        
        # Verifica se pelo menos um contato de emergência foi fornecido
        nome_primeiro_contato = cleaned_data.get('nome_primeiro_contato')
        celular_primeiro_contato = cleaned_data.get('celular_primeiro_contato')
        
        if not nome_primeiro_contato or not celular_primeiro_contato:
            self.add_error('nome_primeiro_contato', 'É necessário fornecer pelo menos um contato de emergência.')
            self.add_error('celular_primeiro_contato', 'É necessário fornecer pelo menos um contato de emergência.')
        
        return cleaned_data
