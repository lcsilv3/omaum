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


class Bairro(models.Model):
    """Modelo para bairros (associados a uma cidade). Simples para futura expansão.

    Motivação: Normalizar endereço e permitir autocomplete/controlar consistência.
    Não estamos vinculando ainda o campo Bairro do Aluno para manter compatibilidade.
    """

    nome = models.CharField(max_length=100, verbose_name=_("Nome do Bairro"))
    cidade = models.ForeignKey(
        Cidade,
        on_delete=models.CASCADE,
        related_name="bairros",
        verbose_name=_("Cidade"),
    )
    # Campo opcional para referência externa futura (IBGE ou outro)
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

    def __str__(self):  # pragma: no cover
        return f"{self.nome} - {self.cidade.nome}/{self.cidade.estado.codigo}"


class Aluno(models.Model):
    """Modelo que representa um aluno."""

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
    # Novas referências normalizadas (opcionais) - coexistem com campos texto legados
    cidade_ref = models.ForeignKey(
        Cidade,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alunos_cidade",
        verbose_name=("Cidade (Ref)"),
        help_text="Referência normalizada da cidade (mantém campo texto para compatibilidade)",
    )
    bairro_ref = models.ForeignKey(
        Bairro,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alunos_bairro",
        verbose_name=("Bairro (Ref)"),
        help_text="Referência normalizada do bairro (mantém campo texto para compatibilidade)",
    )

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
        max_length=4,
        choices=TIPO_SANGUINEO_CHOICES,
        blank=True,
        null=True,
        verbose_name=_("Tipo Sanguíneo"),
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

    # Dados iniciáticos simplificados
    grau_atual = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_("Grau Atual")
    )
    situacao_iniciatica = models.CharField(
        max_length=20,
        default="ATIVO",
        choices=SITUACAO_CHOICES,
        verbose_name=_("Situação Iniciática"),
    )

    # Histórico iniciático como JSON
    historico_iniciatico = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Histórico Iniciático"),
        help_text=_("Histórico de eventos, cargos e registros iniciáticos"),
    )
    historico_checksum = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_("Checksum Histórico"),
        help_text=_(
            "SHA256 do JSON normalizado do histórico iniciático para verificação de integridade."
        ),
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
            models.Index(fields=["cidade_ref"], name="aluno_cidade_ref_idx"),
            models.Index(fields=["bairro_ref"], name="aluno_bairro_ref_idx"),
        ]

    def __str__(self):
        return str(self.nome)

    def obter_historico_ordenado(self):
        """Retorna histórico ordenado por data (mais recente primeiro)."""
        if not isinstance(self.historico_iniciatico, list):
            return []

        try:
            return sorted(
                self.historico_iniciatico, key=lambda x: x.get("data", ""), reverse=True
            )
        except (TypeError, AttributeError):
            return []

    def obter_ultimo_evento(self):
        """Retorna o último evento do histórico."""
        historico = self.obter_historico_ordenado()
        return historico[0] if historico else None

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
        return "Não informada"

    @property
    def naturalidade_display(self):
        """Retorna a naturalidade para exibição, priorizando o novo campo."""
        if self.cidade_naturalidade:
            return self.cidade_naturalidade.nome_completo
        return "Não informada"

    @property
    def ultimo_curso_matriculado(self):
        """Retorna o nome do último curso em que o aluno foi matriculado."""
        try:
            from importlib import import_module

            matriculas_module = import_module("matriculas.models")
            Matricula = matriculas_module.Matricula

            ultima_matricula = (
                Matricula.objects.filter(aluno=self, ativa=True)
                .order_by("-data_matricula")
                .first()
            )

            if ultima_matricula and ultima_matricula.turma.curso:
                return ultima_matricula.turma.curso.nome
            return None
        except (ImportError, AttributeError):
            return None

    @property
    def grau_atual_automatico(self):
        """Retorna o grau atual baseado no último curso matriculado."""
        return self.ultimo_curso_matriculado or self.grau_atual or "Não informado"

    def clean(self):
        """Validações adicionais para o modelo Aluno."""
        super().clean()

        # Validação de data de nascimento
        if self.data_nascimento and self.data_nascimento > datetime.date.today():
            raise ValidationError(
                {"data_nascimento": _("A data de nascimento não pode ser no futuro.")}
            )

        # A lógica de validação de consistência foi removida após a migração dos dados.
        # O código foi mantido comentado para referência futura, se necessário.
        #
        # if self.pais_nacionalidade and self.nacionalidade:
        #     # Se ambos estão preenchidos, verificar se são consistentes
        #     if (
        #         self.nacionalidade.lower()
        #         != self.pais_nacionalidade.nacionalidade.lower()
        #     ):
        #         raise ValidationError(
        #             {
        #                 "nacionalidade": _(
        #                     "A nacionalidade em texto deve ser consistente com o país selecionado."
        #                 )
        #             }
        #         )

    def save(self, *args, **kwargs):
        """Override do save para lógicas automáticas."""

        # Lógica de sincronização removida após a migração dos dados.
        # O código foi mantido comentado para referência futura, se necessário.

        # # Sincronizar nacionalidade
        # if self.pais_nacionalidade and not self.nacionalidade:
        #     self.nacionalidade = self.pais_nacionalidade.nacionalidade
        #
        # # Sincronizar naturalidade
        # if self.cidade_naturalidade and not self.naturalidade:
        #     self.naturalidade = self.cidade_naturalidade.nome_completo
        #
        # # Sincronizar cidade/bairro normalizados -> texto
        # if self.cidade_ref and not self.cidade:
        #     self.cidade = self.cidade_ref.nome
        #     if self.cidade_ref.estado and not self.estado:
        #         self.estado = self.cidade_ref.estado.codigo
        # if self.bairro_ref and not self.bairro:
        #     self.bairro = self.bairro_ref.nome
        #     # Se não houver cidade_ref tentar inferir
        #     if not self.cidade_ref:
        #         self.cidade_ref = self.bairro_ref.cidade
        #         if not self.cidade:
        #             self.cidade = self.cidade_ref.nome
        #         if self.cidade_ref.estado and not self.estado:
        #             self.estado = self.cidade_ref.estado.codigo
        #
        # # Caso texto exista e ref vazia, tentar auto-vincular (best-effort)
        # if self.cidade and not self.cidade_ref:
        #     try:
        #         self.cidade_ref = Cidade.objects.filter(
        #             nome__iexact=self.cidade
        #         ).first()
        #     except Exception:
        #         pass
        # if self.bairro and not self.bairro_ref and self.cidade_ref:
        #     try:
        #         self.bairro_ref = self.cidade_ref.bairros.filter(
        #             nome__iexact=self.bairro
        #         ).first()
        #     except Exception:
        #         pass

        super().save(*args, **kwargs)


class TipoCodigo(models.Model):
    """Tipo de código iniciático (modelo concreto original)."""

    nome = models.CharField(max_length=50, unique=True, verbose_name=_("Nome"))
    descricao = models.TextField(blank=True, null=True, verbose_name=_("Descrição"))

    class Meta:
        verbose_name = _("Tipo de Código")
        verbose_name_plural = _("Tipos de Códigos")
        ordering = ["nome"]

    def __str__(self):  # pragma: no cover
        return str(self.nome)


class Codigo(models.Model):
    """Código iniciático associado a um TipoCodigo."""

    tipo_codigo = models.ForeignKey(
        TipoCodigo,
        on_delete=models.CASCADE,
        verbose_name=_("Tipo de Código"),
        related_name="codigos",
    )
    nome = models.CharField(max_length=100, unique=True, verbose_name=_("Nome"))
    descricao = models.TextField(blank=True, null=True, verbose_name=_("Descrição"))

    class Meta:
        verbose_name = _("Código")
        verbose_name_plural = _("Códigos")
        ordering = ["tipo_codigo__nome", "nome"]

    def __str__(self):  # pragma: no cover
        if self.descricao:
            return f"{self.nome} - {self.descricao}"
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
        indexes = [
            models.Index(fields=["aluno", "-data_os"], name="rh_aluno_dataos_desc"),
            models.Index(fields=["codigo"], name="rh_codigo_idx"),
        ]

    def __str__(self):
        return f"Registro de {self.aluno} - {self.codigo} em {self.data_os}"
