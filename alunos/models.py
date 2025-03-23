from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.utils import timezone

class Aluno(models.Model):
    SEXO_CHOICES = [
        ('M', _('Masculino')),
        ('F', _('Feminino')),
        ('O', _('Outro')),
    ]

    TIPO_SANGUINEO_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ]

    FATOR_RH_CHOICES = [
        ('+', 'Positivo'),
        ('-', 'Negativo'),
    ]

    ESTADO_CIVIL_CHOICES = [
        ('S', _('Solteiro(a)')),
        ('C', _('Casado(a)')),
        ('D', _('Divorciado(a)')),
        ('V', _('Viúvo(a)')),
        ('U', _('União Estável')),
    ]

    ESCOLARIDADE_CHOICES = [
        ('EF', _('Ensino Fundamental')),
        ('EM', _('Ensino Médio')),
        ('ES', _('Ensino Superior')),
        ('PG', _('Pós-Graduação')),
        ('ME', _('Mestrado')),
        ('DO', _('Doutorado')),
    ]

    STATUS_CHOICES = [
        ('A', _('Ativo')),
        ('I', _('Inativo')),
        ('S', _('Suspenso')),
    ]
    cpf_validator = RegexValidator(
        regex=r'^\d{11}$',
        message=_('CPF deve conter 11 dígitos numéricos')
    )

    celular_validator = RegexValidator(
        regex=r'^\d{10,11}$',
        message=_('Número de celular inválido')
    )

    cep_validator = RegexValidator(
        regex=r'^\d{8}$',
        message=_('CEP deve conter 8 dígitos numéricos')
    )

    telefone_fixo_validator = RegexValidator(
        regex=r'^\d{10,11}$',
        message=_('Número de telefone fixo inválido')
    )
    cpf = models.CharField(
        _('CPF'),
        max_length=11,
        primary_key=True,
        validators=[cpf_validator],
        help_text=_('Digite apenas números')
    )
    foto = models.ImageField(
        _('Foto'),
        upload_to='alunos/',
        null=True,
        blank=True
    )
    nome = models.CharField(
        _('Nome completo'),
        max_length=100
    )
    data_nascimento = models.DateField(_('Data de nascimento'))
    hora_nascimento = models.TimeField(_('Hora de nascimento'))
    numero_iniciatico = models.CharField(
        _('Número iniciático'),
        max_length=20,
        blank=True,
        null=True
    )
    nome_iniciatico = models.CharField(
        _('Nome iniciático'),
        max_length=100,
        blank=True,
        null=True
    )
    data_iniciacao = models.DateField(_('Data de iniciação'), null=True, blank=True)

    sexo = models.CharField(
        _('Sexo'),
        max_length=1,
        choices=SEXO_CHOICES
    )
    estado_civil = models.CharField(
        _('Estado Civil'),
        max_length=1,
        choices=ESTADO_CIVIL_CHOICES,
        null=True,  # Adicione esta linha
        blank=True,  # Adicione esta linha
        default='S'  # Adicione esta linha (S para Solteiro como padrão)
    )

    profissao = models.CharField(
        _('Profissão'), 
        max_length=100,
        null=True,  # Adicione esta linha
        blank=True  # Adicione esta linha
    )
    escolaridade = models.CharField(
        _('Escolaridade'),
        max_length=2,
        choices=ESCOLARIDADE_CHOICES,
        null=True,  # Adicione esta linha
        blank=True  # Adicione esta linha
    )

    email = models.EmailField(
        _('E-mail'),
        validators=[EmailValidator()]
    )
    telefone_fixo = models.CharField(
        _('Telefone Fixo'),
        max_length=11,
        validators=[telefone_fixo_validator],
        blank=True,
        null=True
    )
    nacionalidade = models.CharField(_('Nacionalidade'), max_length=50)
    naturalidade = models.CharField(_('Naturalidade'), max_length=50)
    cep = models.CharField(
        _('CEP'),
        max_length=8,
        validators=[cep_validator]
    )
    rua = models.CharField(_('Rua'), max_length=100)
    numero_imovel = models.CharField(_('Número'), max_length=10)
    complemento = models.CharField(
        _('Complemento'),
        max_length=50,
        blank=True,
        null=True
    )
    bairro = models.CharField(_('Bairro'), max_length=50)
    cidade = models.CharField(_('Cidade'), max_length=50)
    estado = models.CharField(_('Estado'), max_length=2)
    nome_primeiro_contato = models.CharField(
        _('Nome do primeiro contato'),
        max_length=100
    )
    celular_primeiro_contato = models.CharField(
        _('Celular do primeiro contato'),
        max_length=11,
        validators=[celular_validator]
    )
    tipo_relacionamento_primeiro_contato = models.CharField(
        _('Relacionamento do primeiro contato'),
        max_length=50
    )
    nome_segundo_contato = models.CharField(
        _('Nome do segundo contato'),
        max_length=100
    )
    celular_segundo_contato = models.CharField(
        _('Celular do segundo contato'),
        max_length=11,
        validators=[celular_validator]
    )
    tipo_relacionamento_segundo_contato = models.CharField(
        _('Relacionamento do segundo contato'),
        max_length=50
    )
    tipo_sanguineo = models.CharField(
        _('Tipo sanguíneo'),
        max_length=2,
        choices=TIPO_SANGUINEO_CHOICES
    )
    fator_rh = models.CharField(
        _('Fator RH'),
        max_length=1,
        choices=FATOR_RH_CHOICES
    )
    alergias = models.TextField(
        _('Alergias'),
        blank=True,
        null=True
    )
    condicoes_medicas_gerais = models.TextField(
        _('Condições médicas'),
        blank=True,
        null=True
    )
    convenio_medico = models.CharField(
        _('Convênio médico'),
        max_length=100,
        blank=True,
        null=True
    )
    hospital = models.CharField(
        _('Hospital de preferência'),
        max_length=100,
        blank=True,
        null=True
    )
    status = models.CharField(
        _('Status'),
        max_length=1,
        choices=STATUS_CHOICES,
        default='A'
    )

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(
        _('Atualizado em'),
        auto_now=True
    )

    curso = models.ForeignKey(
        'cursos.Curso',  # Use string reference to avoid circular imports
        on_delete=models.SET_NULL,  # Prevent deletion of Curso if students are enrolled
        verbose_name=_('Curso'),
        related_name='alunos',  # This allows curso.alunos.all() to get all students in a course
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Aluno')
        verbose_name_plural = _('Alunos')
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf})"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('aluno-detail', args=[str(self.cpf)])

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if not self.curso_id:
            raise ValidationError({'curso': _('Todo aluno deve estar associado a um curso.')})

    @property
    def idade(self):
        today = date.today()
        return today.year - self.data_nascimento.year - (
            (today.month, today.day) <
            (self.data_nascimento.month, self.data_nascimento.day)
        )

    @property
    def tempo_desde_iniciacao(self):
        if self.data_iniciacao:
            today = date.today()
            delta = today - self.data_iniciacao
            return delta.days
        return None
