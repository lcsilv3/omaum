"""Modelos do aplicativo Alunos."""

import datetime
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


class Aluno(models.Model):
    """Modelo que representa um aluno."""

    SEXO_CHOICES = [
        ("M", "Masculino"),
        ("F", "Feminino"),
        ("O", "Outro"),
    ]

    FATOR_RH_CHOICES = [
        ("+", "Positivo"),
        ("-", "Negativo"),
    ]

    SITUACAO_CHOICES = [
        ("ATIVO", "Ativo"),
        ("AFASTADO", "Afastado"),
        ("ESPECIAIS", "Especiais"),
        ("EXCLUIDO", "Excluído"),
        ("FALECIDO", "Falecido"),
        ("LOI", "LOI"),
    ]

    cpf_validator = RegexValidator(
        regex=r"^\d{11}$", message=_("CPF deve conter 11 dígitos numéricos")
    )

    celular_validator = RegexValidator(
        regex=r"^\d{10,11}$", message=_("Número de celular inválido")
    )

    # Campos básicos
    cpf = models.CharField(
        max_length=11,
        primary_key=True,
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
    situacao = models.CharField(
        max_length=10,
        choices=SITUACAO_CHOICES,
        default="ATIVO",
        verbose_name=_("Situação"),
    )

    # Campos iniciáticos
    numero_iniciatico = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Número Iniciático"),
    )
    nome_iniciatico = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("Nome Iniciático"),
    )

    # Campos de nacionalidade e naturalidade - NOVOS CAMPOS
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

    # Campos de nacionalidade e naturalidade antigos - MANTIDOS PARA COMPATIBILIDADE
    nacionalidade = models.CharField(
        max_length=50,
        default="Brasileira",
        verbose_name=_("Nacionalidade (Texto)"),
        help_text="Campo de texto livre - será substituído pelo campo País de Nacionalidade",
        blank=True,
        null=True,
    )
    naturalidade = models.CharField(
        max_length=50,
        verbose_name=_("Naturalidade (Texto)"),
        help_text="Campo de texto livre - será substituído pelo campo Cidade de Naturalidade",
        blank=True,
        null=True,
    )

    # Endereço
    rua = models.CharField(max_length=150, verbose_name=_("Rua"), blank=True, null=True)
    numero_imovel = models.CharField(
        max_length=10, verbose_name=_("Número"), blank=True, null=True
    )
    complemento = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_("Complemento")
    )
    bairro = models.CharField(
        max_length=50, verbose_name=_("Bairro"), blank=True, null=True
    )
    cidade = models.CharField(
        max_length=50, verbose_name=_("Cidade"), blank=True, null=True
    )
    estado = models.CharField(
        max_length=2, verbose_name=_("Estado"), blank=True, null=True
    )
    cep = models.CharField(max_length=8, verbose_name=_("CEP"), blank=True, null=True)

    # Contatos
    nome_primeiro_contato = models.CharField(
        max_length=100,
        verbose_name=_("Nome do 1º Contato"),
        blank=True,
        null=True,
    )
    celular_primeiro_contato = models.CharField(
        max_length=11,
        validators=[celular_validator],
        verbose_name=_("Celular do 1º Contato"),
        blank=True,
        null=True,
    )
    tipo_relacionamento_primeiro_contato = models.CharField(
        max_length=50,
        verbose_name=_("Relacionamento com 1º Contato"),
        blank=True,
        null=True,
    )
    nome_segundo_contato = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Nome do 2º Contato"),
    )
    celular_segundo_contato = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        validators=[celular_validator],
        verbose_name=_("Celular do 2º Contato"),
    )
    tipo_relacionamento_segundo_contato = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("Relacionamento com 2º Contato"),
    )

    # Outros dados pessoais
    estado_civil = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_("Estado Civil")
    )
    profissao = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_("Profissão")
    )
    ativo = models.BooleanField(default=True, verbose_name=_("Ativo"))

    # Dados médicos
    tipo_sanguineo = models.CharField(
        max_length=3, blank=True, null=True, verbose_name=_("Tipo Sanguíneo")
    )
    fator_rh = models.CharField(
        max_length=1,
        choices=FATOR_RH_CHOICES,
        blank=True,
        null=True,
        verbose_name=_("Fator RH"),
    )
    alergias = models.TextField(blank=True, null=True, verbose_name=_("Alergias"))
    condicoes_medicas_gerais = models.TextField(
        blank=True, null=True, verbose_name=_("Condições Médicas Gerais")
    )
    convenio_medico = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Convênio Médico"),
    )
    hospital = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Hospital de Preferência"),
    )

    # Metadados
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("Criado em"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Atualizado em"))

    class Meta:
        verbose_name = _("Aluno")
        verbose_name_plural = _("Alunos")
        ordering = ["nome"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["numero_iniciatico"]),
            models.Index(fields=["situacao"]),
            models.Index(fields=["ativo"]),
            models.Index(fields=["pais_nacionalidade"]),
            models.Index(fields=["cidade_naturalidade"]),
            models.Index(fields=["nome"]),
        ]

    def __str__(self):
        return str(self.nome)

    @property
    def esta_ativo(self):
        """Verifica se o aluno está ativo."""
        return self.situacao == "ATIVO"

    @property
    def pode_ser_instrutor(self):
        """Verifica se o aluno pode ser instrutor usando lógica básica."""
        if not self.esta_ativo:
            return False

        # Verificação básica: aluno com número iniciático pode ser instrutor
        return bool(self.numero_iniciatico)

    @property
    def nacionalidade_display(self):
        """Retorna a nacionalidade para exibição, priorizando o novo campo."""
        if self.pais_nacionalidade:
            return self.pais_nacionalidade.nacionalidade
        return self.nacionalidade or "Não informada"

    @property
    def naturalidade_display(self):
        """Retorna a naturalidade para exibição, priorizando o novo campo."""
        if self.cidade_naturalidade:
            return self.cidade_naturalidade.nome_completo
        return self.naturalidade or "Não informada"

    def clean(self):
        """Validações adicionais para o modelo Aluno."""
        super().clean()

        # Validação de data de nascimento
        if self.data_nascimento and self.data_nascimento > datetime.date.today():
            raise ValidationError(
                {"data_nascimento": _("A data de nascimento não pode ser no futuro.")}
            )

        # Validação de consistência entre campos novos e antigos
        if self.pais_nacionalidade and self.nacionalidade:
            # Se ambos estão preenchidos, verificar se são consistentes
            if (
                self.nacionalidade.lower()
                != self.pais_nacionalidade.nacionalidade.lower()
            ):
                raise ValidationError(
                    {
                        "nacionalidade": _(
                            "A nacionalidade em texto deve ser consistente com o país selecionado."
                        )
                    }
                )

    def save(self, *args, **kwargs):
        """Override do save para manter sincronização entre campos novos e antigos."""
        # Sincronizar nacionalidade
        if self.pais_nacionalidade and not self.nacionalidade:
            self.nacionalidade = self.pais_nacionalidade.nacionalidade

        # Sincronizar naturalidade
        if self.cidade_naturalidade and not self.naturalidade:
            self.naturalidade = self.cidade_naturalidade.nome_completo

        super().save(*args, **kwargs)


class TipoCodigo(models.Model):
    """Categoriza os códigos (ex: Cargo, Punição, Iniciação)."""

    nome = models.CharField(max_length=50, unique=True, verbose_name=_("Nome"))
    descricao = models.TextField(blank=True, null=True, verbose_name=_("Descrição"))

    class Meta:
        verbose_name = _("Tipo de Código")
        verbose_name_plural = _("Tipos de Códigos")
        ordering = ["nome"]

    def __str__(self):
        return str(self.nome)


class Codigo(models.Model):
    """Códigos específicos dentro de cada tipo (ex: Mestre, Aprendiz, Advertência)."""

    tipo_codigo = models.ForeignKey(
        TipoCodigo, on_delete=models.CASCADE, verbose_name=_("Tipo de Código")
    )
    nome = models.CharField(max_length=100, unique=True, verbose_name=_("Nome"))
    descricao = models.TextField(blank=True, null=True, verbose_name=_("Descrição"))

    class Meta:
        verbose_name = _("Código")
        verbose_name_plural = _("Códigos")
        ordering = ["tipo_codigo__nome", "nome"]

    def __str__(self):
        return str(self.nome)


class RegistroHistorico(models.Model):
    """Registra um evento (baseado em um Código) para um Aluno."""

    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE,
        related_name="historico",
        verbose_name=_("Aluno"),
    )
    codigo = models.ForeignKey(
        Codigo,
        on_delete=models.PROTECT,
        related_name="registros",
        verbose_name=_("Código"),
    )
    ordem_servico = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_("Ordem de Serviço")
    )
    data_os = models.DateField(verbose_name=_("Data da Ordem de Serviço"))
    numero_iniciatico = models.CharField(
        max_length=10, null=True, blank=True, verbose_name=_("Número Iniciático")
    )
    nome_iniciatico = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("Nome Iniciático")
    )
    observacoes = models.TextField(blank=True, null=True, verbose_name=_("Observações"))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Data do Registro")
    )
    ativo = models.BooleanField(default=True, verbose_name=_("Ativo"))

    class Meta:
        verbose_name = _("Registro Histórico")
        verbose_name_plural = _("Registros Históricos")
        ordering = ["-data_os", "-created_at"]
        unique_together = [["aluno", "codigo", "ordem_servico"]]

    def __str__(self):
        return f"Registro de {self.aluno} - {self.codigo} em {self.data_os}"
