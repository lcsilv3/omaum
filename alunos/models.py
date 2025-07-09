"""Modelos do aplicativo Alunos."""

import datetime
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError


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
    nacionalidade = models.CharField(
        max_length=50, default="Brasileira", verbose_name=_("Nacionalidade")
    )
    naturalidade = models.CharField(
        max_length=50, verbose_name=_("Naturalidade")
    )
    rua = models.CharField(
        max_length=150, verbose_name=_("Rua"), blank=True, null=True
    )
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
    cep = models.CharField(
        max_length=8, verbose_name=_("CEP"), blank=True, null=True
    )
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
    estado_civil = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_("Estado Civil")
    )
    profissao = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_("Profissão")
    )
    ativo = models.BooleanField(default=True, verbose_name=_("Ativo"))
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
    alergias = models.TextField(
        blank=True, null=True, verbose_name=_("Alergias")
    )
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
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name=_("Criado em")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Atualizado em")
    )

    def __str__(self):
        return str(self.nome)

    @property
    def esta_ativo(self):
        """Verifica se o aluno está ativo."""
        return self.situacao == "ATIVO"

    @property
    def pode_ser_instrutor(self):
        """Verifica se o aluno pode ser instrutor."""
        from importlib import import_module  # Importação movida para o topo

        if not self.esta_ativo:
            return False

        try:
            matriculas_module = import_module("matriculas.models")
            matricula_model = getattr(matriculas_module, "Matricula")
            matriculas_nao_pre_iniciatico = matricula_model.objects.filter(
                aluno=self
            ).exclude(turma__curso__nome__icontains="Pré-iniciático")
            return matriculas_nao_pre_iniciatico.exists()
        except (ImportError, AttributeError):
            return False

    def clean(self):
        """Validações adicionais para o modelo Aluno."""
        super().clean()
        if self.data_nascimento and self.data_nascimento > datetime.date.today():
            raise ValidationError({
                "data_nascimento": _(
                    "A data de nascimento não pode ser no futuro."
                )
            })


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
    observacoes = models.TextField(
        blank=True, null=True, verbose_name=_("Observações")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Data do Registro")
    )
    ativo = models.BooleanField(default=True, verbose_name=_("Ativo"))

    class Meta:
        verbose_name = _("Registro Histórico")
        verbose_name_plural = _("Registros Históricos")
        ordering = ["-data_os", "-created_at"]
        unique_together = [
            ["aluno", "codigo", "ordem_servico"]
        ]

    def __str__(self):
        return f"Registro de {self.aluno} - {self.codigo} em {self.data_os}"
