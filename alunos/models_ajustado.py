"""
Ajustes no modelo Aluno para atender às premissas estabelecidas.
Mantém compatibilidade com dados existentes através de migração.
"""

# Importações existentes mantidas...
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Pais(models.Model):
    """Modelo para países."""

    codigo = models.CharField(
        max_length=3,
        unique=True,
        help_text="Código ISO do país (ex: BRA, ARG, USA)",
        verbose_name=_("Código ISO"),
    )
    nome = models.CharField(max_length=100, unique=True, verbose_name=_("Nome do País"))
    nacionalidade = models.CharField(
        max_length=100,
        help_text="Gentílico (ex: brasileiro, argentino, americano)",
        verbose_name=_("Nacionalidade"),
    )
    ativo = models.BooleanField(default=True, verbose_name=_("Ativo"))

    class Meta:
        verbose_name = _("País")
        verbose_name_plural = _("Países")
        ordering = ["nome"]
        indexes = [
            models.Index(fields=["nome"]),
            models.Index(fields=["nacionalidade"]),
            models.Index(fields=["ativo"]),
        ]

    def __str__(self):
        return self.nome


class Estado(models.Model):
    """Modelo para estados brasileiros."""

    REGIAO_CHOICES = [
        ("Norte", "Norte"),
        ("Nordeste", "Nordeste"),
        ("Centro-Oeste", "Centro-Oeste"),
        ("Sudeste", "Sudeste"),
        ("Sul", "Sul"),
    ]

    codigo = models.CharField(
        max_length=2,
        unique=True,
        help_text="Sigla do estado (ex: SP, RJ, MG)",
        verbose_name=_("Sigla"),
    )
    nome = models.CharField(
        max_length=100, unique=True, verbose_name=_("Nome do Estado")
    )
    regiao = models.CharField(
        max_length=20, choices=REGIAO_CHOICES, verbose_name=_("Região")
    )

    class Meta:
        verbose_name = _("Estado")
        verbose_name_plural = _("Estados")
        ordering = ["nome"]
        indexes = [
            models.Index(fields=["nome"]),
            models.Index(fields=["codigo"]),
            models.Index(fields=["regiao"]),
        ]

    def __str__(self):
        return f"{self.nome} ({self.codigo})"


class Cidade(models.Model):
    """Modelo para cidades brasileiras."""

    nome = models.CharField(max_length=100, verbose_name=_("Nome da Cidade"))
    estado = models.ForeignKey(
        Estado,
        on_delete=models.CASCADE,
        related_name="cidades",
        verbose_name=_("Estado"),
    )
    codigo_ibge = models.CharField(
        max_length=7,
        unique=True,
        null=True,
        blank=True,
        help_text="Código IBGE da cidade",
        verbose_name=_("Código IBGE"),
    )

    class Meta:
        verbose_name = _("Cidade")
        verbose_name_plural = _("Cidades")
        ordering = ["nome"]
        unique_together = ["nome", "estado"]
        indexes = [
            models.Index(fields=["nome"]),
            models.Index(fields=["estado"]),
            models.Index(fields=["codigo_ibge"]),
        ]

    def __str__(self):
        return f"{self.nome} - {self.estado.codigo}"

    @property
    def nome_completo(self):
        """Retorna nome completo da cidade com estado."""
        return f"{self.nome}, {self.estado.nome}"


class Bairro(models.Model):
    """Modelo para bairros (associados a uma cidade)."""

    nome = models.CharField(max_length=100, verbose_name=_("Nome do Bairro"))
    cidade = models.ForeignKey(
        Cidade,
        on_delete=models.CASCADE,
        related_name="bairros",
        verbose_name=_("Cidade"),
    )
    codigo_externo = models.CharField(
        max_length=30, blank=True, null=True, verbose_name=_("Código Externo")
    )

    class Meta:
        verbose_name = _("Bairro")
        verbose_name_plural = _("Bairros")
        ordering = ["nome"]
        unique_together = ["nome", "cidade"]
        indexes = [
            models.Index(fields=["nome"]),
            models.Index(fields=["cidade"]),
        ]

    def __str__(self):
        return f"{self.nome} - {self.cidade.nome}/{self.cidade.estado.codigo}"


class Aluno(models.Model):
    """
    Modelo que representa um aluno.

    AJUSTES REALIZADOS conforme premissas:
    - Situação do aluno ajustada para: 'a' (ativo), 'd' (desligado), 'f' (falecido), 'e' (excluído)
    - Mantém numero_iniciatico existente
    - Compatibilidade com dados existentes através de migração
    """

    SEXO_CHOICES = [
        ("M", "Masculino"),
        ("F", "Feminino"),
        ("O", "Outro"),
    ]

    TIPO_SANGUINEO_CHOICES = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]

    # AJUSTE: Situação conforme premissas estabelecidas
    SITUACAO_CHOICES = [
        ("a", "Ativo"),  # Mapeamento: ATIVO -> a
        ("d", "Desligado"),  # Mapeamento: AFASTADO/LOI -> d
        ("f", "Falecido"),  # Mapeamento: FALECIDO -> f
        ("e", "Excluído"),  # Mapeamento: EXCLUIDO -> e
        # Mantém ESPECIAIS como caso especial que será migrado para 'a'
    ]

    # Validadores
    cpf_validator = RegexValidator(
        regex=r"^\d{11}$", message=_("CPF deve conter 11 dígitos numéricos")
    )

    celular_validator = RegexValidator(
        regex=r"^\d{10,11}$", message=_("Número de celular inválido")
    )

    # Campos básicos
    cpf = models.CharField(
        max_length=11,
        unique=True,
        db_index=True,
        validators=[cpf_validator],
        verbose_name=_("CPF"),
    )
    nome = models.CharField(max_length=100, verbose_name=_("Nome Completo"))
    data_nascimento = models.DateField(verbose_name=_("Data de Nascimento"))
    hora_nascimento = models.TimeField(
        null=True, blank=True, verbose_name=_("Hora de Nascimento")
    )
    email = models.EmailField(unique=True, verbose_name=_("E-mail"))
    foto = models.ImageField(
        upload_to="alunos/fotos/",
        null=True,
        blank=True,
        verbose_name=_("Foto"),
    )
    sexo = models.CharField(
        max_length=1, choices=SEXO_CHOICES, default="M", verbose_name=_("Sexo")
    )

    # CAMPO AJUSTADO: Situação conforme premissas
    situacao = models.CharField(
        max_length=1,  # Alterado de 10 para 1 caractere
        choices=SITUACAO_CHOICES,
        default="a",  # Alterado de "ATIVO" para "a"
        verbose_name=_("Situação do Aluno"),
        help_text="Situação conforme planilha Excel: a=ativo, d=desligado, f=falecido, e=excluído",
    )

    # Campos iniciáticos (já existentes, mantidos)
    numero_iniciatico = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Número Iniciático"),
        help_text="Número único de identificação iniciática (campo 'Inic' da planilha)",
    )
    nome_iniciatico = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("Nome Iniciático"),
    )

    # Campos de nacionalidade e naturalidade
    pais_nacionalidade = models.ForeignKey(
        Pais,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="nacionais",
        verbose_name=_("País de Nacionalidade"),
        help_text="País que define a nacionalidade do aluno",
    )
    cidade_naturalidade = models.ForeignKey(
        Cidade,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="naturais",
        verbose_name=_("Cidade de Naturalidade"),
        help_text="Cidade onde o aluno nasceu",
    )

    # Endereço
    rua = models.CharField(max_length=150, verbose_name=_("Rua"), blank=True, null=True)
    numero_imovel = models.CharField(
        max_length=10, verbose_name=_("Número"), blank=True, null=True
    )
    complemento = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_("Complemento")
    )
    cep = models.CharField(max_length=8, verbose_name=_("CEP"), blank=True, null=True)

    # Referências normalizadas
    cidade_ref = models.ForeignKey(
        Cidade,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alunos_cidade",
        verbose_name=("Cidade (Ref)"),
        help_text="Referência normalizada da cidade",
    )
    bairro_ref = models.ForeignKey(
        Bairro,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alunos_bairro",
        verbose_name=("Bairro (Ref)"),
        help_text="Referência normalizada do bairro",
    )

    # Campos de contato
    telefone = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        validators=[celular_validator],
        verbose_name=_("Telefone"),
    )
    celular = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        validators=[celular_validator],
        verbose_name=_("Celular"),
    )

    # Informações médicas
    tipo_sanguineo = models.CharField(
        max_length=3,
        choices=TIPO_SANGUINEO_CHOICES,
        blank=True,
        null=True,
        verbose_name=_("Tipo Sanguíneo"),
    )

    # Campos de controle
    ativo = models.BooleanField(default=True, verbose_name=_("Ativo no Sistema"))
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name=_("Atualizado em"))

    class Meta:
        verbose_name = _("Aluno")
        verbose_name_plural = _("Alunos")
        ordering = ["nome"]
        indexes = [
            models.Index(fields=["nome"]),
            models.Index(fields=["cpf"]),
            models.Index(fields=["numero_iniciatico"]),
            models.Index(fields=["situacao"]),
            models.Index(fields=["ativo"]),
        ]

    def __str__(self):
        if self.numero_iniciatico:
            return f"{self.numero_iniciatico} - {self.nome}"
        return self.nome

    def clean(self):
        """Validações customizadas."""
        super().clean()

        # Validar data de nascimento
        if self.data_nascimento and self.data_nascimento > timezone.now().date():
            raise ValidationError(
                {"data_nascimento": "A data de nascimento não pode ser futura."}
            )

        # Validar idade mínima (exemplo: 16 anos)
        if self.data_nascimento:
            idade = (timezone.now().date() - self.data_nascimento).days // 365
            if idade < 16:
                raise ValidationError(
                    {"data_nascimento": "O aluno deve ter pelo menos 16 anos."}
                )

    @property
    def idade(self):
        """Calcula a idade do aluno."""
        if self.data_nascimento:
            hoje = timezone.now().date()
            return (
                hoje.year
                - self.data_nascimento.year
                - (
                    (hoje.month, hoje.day)
                    < (self.data_nascimento.month, self.data_nascimento.day)
                )
            )
        return None

    @property
    def nome_completo_situacao(self):
        """Retorna nome com situação."""
        return f"{self.nome} ({self.get_situacao_display()})"

    def esta_ativo(self):
        """Verifica se o aluno está ativo."""
        return self.situacao == "a" and self.ativo

    def pode_participar_atividades(self):
        """Verifica se o aluno pode participar de atividades."""
        return self.situacao in ["a"] and self.ativo

    @classmethod
    def obter_ativos(cls):
        """Retorna queryset com alunos ativos."""
        return cls.objects.filter(situacao="a", ativo=True)

    @classmethod
    def obter_por_situacao(cls, situacao):
        """Retorna alunos por situação específica."""
        return cls.objects.filter(situacao=situacao)

    # Métodos para compatibilidade com sistema de relatórios
    def get_situacao_excel(self):
        """Retorna situação no formato da planilha Excel."""
        return self.situacao

    def get_numero_iniciatico_display(self):
        """Retorna número iniciático formatado."""
        return self.numero_iniciatico or "N/A"


# Modelo para controlar migração da situação
class MigracaoSituacaoAluno(models.Model):
    """
    Modelo temporário para controlar a migração das situações dos alunos.
    """

    aluno = models.OneToOneField(Aluno, on_delete=models.CASCADE, verbose_name="Aluno")

    situacao_anterior = models.CharField(
        max_length=10, verbose_name="Situação Anterior"
    )

    situacao_nova = models.CharField(max_length=1, verbose_name="Situação Nova")

    migrado_em = models.DateTimeField(auto_now_add=True, verbose_name="Migrado em")

    class Meta:
        verbose_name = "Migração de Situação"
        verbose_name_plural = "Migrações de Situação"

    def __str__(self):
        return f"{self.aluno.nome}: {self.situacao_anterior} -> {self.situacao_nova}"
