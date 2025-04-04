from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone

class Aluno(models.Model):
    # Opções para o campo sexo
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    
    # Opções para o campo fator_rh
    FATOR_RH_CHOICES = [
        ('+', 'Positivo'),
        ('-', 'Negativo'),
    ]
    
    # Validadores
    cpf_validator = RegexValidator(
        regex=r'^\d{11}$',
        message=_('CPF deve conter 11 dígitos numéricos')
    )
    
    celular_validator = RegexValidator(
        regex=r'^\d{10,11}$',
        message=_('Número de celular inválido')
    )
    
    # Campos do modelo
    cpf = models.CharField(
        max_length=11,
        primary_key=True,
        validators=[cpf_validator],
        verbose_name=_('CPF')
    )
    nome = models.CharField(max_length=100, verbose_name=_('Nome Completo'))
    data_nascimento = models.DateField(verbose_name=_('Data de Nascimento'))
    hora_nascimento = models.TimeField(
        null=True, 
        blank=True, 
        verbose_name=_('Hora de Nascimento')
    )
    email = models.EmailField(unique=True, verbose_name=_('E-mail'))
    foto = models.ImageField(
        upload_to='alunos/fotos/', 
        null=True, 
        blank=True, 
        verbose_name=_('Foto')
    )
    sexo = models.CharField(
        max_length=1, 
        choices=SEXO_CHOICES, 
        default='M', 
        verbose_name=_('Sexo')
    )
    
    # Dados iniciáticos - Tornando estes campos nullable
    numero_iniciatico = models.CharField(
        max_length=10, 
        unique=True, 
        null=True,  # Permitir nulo
        blank=True,  # Permitir em branco
        verbose_name=_('Número Iniciático')
    )
    nome_iniciatico = models.CharField(
        max_length=100, 
        null=True,  # Permitir nulo
        blank=True,  # Permitir em branco
        verbose_name=_('Nome Iniciático')
    )
    
    # Nacionalidade e naturalidade
    nacionalidade = models.CharField(
        max_length=50, 
        default='Brasileira', 
        verbose_name=_('Nacionalidade')
    )
    naturalidade = models.CharField(
        max_length=50, 
        verbose_name=_('Naturalidade')
    )
    
    # Endereço
    rua = models.CharField(max_length=100, verbose_name=_('Rua'))
    numero_imovel = models.CharField(max_length=10, verbose_name=_('Número'))
    complemento = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name=_('Complemento')
    )
    bairro = models.CharField(max_length=50, verbose_name=_('Bairro'))
    cidade = models.CharField(max_length=50, verbose_name=_('Cidade'))
    estado = models.CharField(max_length=2, verbose_name=_('Estado'))
    cep = models.CharField(max_length=8, verbose_name=_('CEP'))
    
    # Contatos de emergência
    nome_primeiro_contato = models.CharField(
        max_length=100, 
        verbose_name=_('Nome do Primeiro Contato')
    )
    celular_primeiro_contato = models.CharField(
        max_length=11, 
        validators=[celular_validator], 
        verbose_name=_('Celular do Primeiro Contato')
    )
    tipo_relacionamento_primeiro_contato = models.CharField(
        max_length=50, 
        verbose_name=_('Tipo de Relacionamento do Primeiro Contato')
    )
    
    nome_segundo_contato = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name=_('Nome do Segundo Contato')
    )
    celular_segundo_contato = models.CharField(
        max_length=11, 
        blank=True, 
        null=True, 
        validators=[celular_validator], 
        verbose_name=_('Celular do Segundo Contato')
    )
    tipo_relacionamento_segundo_contato = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name=_('Tipo de Relacionamento do Segundo Contato')
    )
    
    # Informações médicas
    tipo_sanguineo = models.CharField(
        max_length=3, 
        verbose_name=_('Tipo Sanguíneo')
    )
    fator_rh = models.CharField(
        max_length=1, 
        choices=FATOR_RH_CHOICES, 
        verbose_name=_('Fator RH')
    )
    alergias = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=_('Alergias')
    )
    condicoes_medicas_gerais = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=_('Condições Médicas Gerais')
    )
    convenio_medico = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name=_('Convênio Médico')
    )
    hospital = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name=_('Hospital de Preferência')
    )
    
    # Metadados - Definindo um valor padrão para created_at
    created_at = models.DateTimeField(
        default=timezone.now,  # Valor padrão
        verbose_name=_('Criado em')
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_('Atualizado em')
    )
    
    def __str__(self):
        return self.nome
    
    def clean(self):
        """Validação personalizada para o modelo."""
        super().clean()
    
    class Meta:
        verbose_name = _('Aluno')
        verbose_name_plural = _('Alunos')
        ordering = ['nome']
