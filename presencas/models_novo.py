"""
Novos modelos para o sistema de presenças - Versão Unificada
Implementação da proposta de refatoração seguindo as premissas estabelecidas.
"""

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal
import logging
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class RegistroPresenca(models.Model):
    """
    Modelo unificado para registro de presença de alunos.

    Este modelo substitui os modelos Presenca, PresencaDetalhada e ConvocacaoPresenca,
    centralizando toda a lógica de controle de presença em uma única estrutura.

    Segue as premissas estabelecidas:
    - Nomenclatura em português brasileiro
    - Evita importações circulares usando importlib
    - Mantém compatibilidade com dados existentes
    """

    # Relacionamentos usando strings para evitar importações circulares
    aluno = models.ForeignKey(
        "alunos.Aluno",
        on_delete=models.CASCADE,
        verbose_name="Aluno",
        related_name="registros_presenca",
        help_text="Aluno relacionado ao registro de presença",
    )

    turma = models.ForeignKey(
        "turmas.Turma",
        on_delete=models.CASCADE,
        verbose_name="Turma",
        related_name="registros_presenca",
        help_text="Turma onde ocorreu a atividade",
    )

    atividade = models.ForeignKey(
        "atividades.Atividade",
        on_delete=models.CASCADE,
        verbose_name="Atividade",
        related_name="registros_presenca",
        help_text="Atividade acadêmica ou ritualística",
    )

    # Informações temporais
    data = models.DateField(
        verbose_name="Data da Atividade", help_text="Data em que a atividade ocorreu"
    )

    periodo_mes = models.DateField(
        verbose_name="Período (Mês/Ano)",
        help_text="Primeiro dia do mês para agrupamento mensal",
        db_index=True,
    )

    # Status da presença - Seguindo padrão Excel existente
    STATUS_CHOICES = [
        ("P", "Presente"),
        ("F", "Falta"),
        ("J", "Falta Justificada"),
        ("V1", "Voluntário Extra"),
        ("V2", "Voluntário Simples"),
    ]

    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default="P",
        verbose_name="Status da Presença",
        help_text="Status conforme planilha Excel: P, F, J, V1, V2",
    )

    # Informações adicionais
    convocado = models.BooleanField(
        default=True,
        verbose_name="Foi Convocado",
        help_text="Indica se o aluno foi convocado para esta atividade",
    )

    justificativa = models.TextField(
        blank=True,
        null=True,
        verbose_name="Justificativa",
        help_text="Justificativa para faltas ou observações",
    )

    # Campos de controle e auditoria
    registrado_por = models.CharField(
        max_length=100,
        default="Sistema",
        verbose_name="Registrado por",
        help_text="Usuário ou sistema que registrou a presença",
    )

    data_registro = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data de Registro",
        help_text="Quando o registro foi criado no sistema",
    )

    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Atualização",
        help_text="Última atualização do registro",
    )

    class Meta:
        verbose_name = "Registro de Presença"
        verbose_name_plural = "Registros de Presença"
        ordering = ["-data", "aluno__nome"]

        # Constraint para evitar duplicatas
        unique_together = ["aluno", "turma", "atividade", "data"]

        # Índices para performance
        indexes = [
            models.Index(fields=["data"]),
            models.Index(fields=["periodo_mes"]),
            models.Index(fields=["status"]),
            models.Index(fields=["aluno", "turma"]),
            models.Index(fields=["turma", "periodo_mes"]),
        ]

    def __str__(self):
        """Representação string do registro."""
        return f"{self.aluno.nome} - {self.data} - {self.get_status_display()}"

    def clean(self):
        """
        Validações customizadas do modelo.

        Valida:
        - Data não pode ser futura
        - Período deve ser primeiro dia do mês
        - Justificativa obrigatória para faltas justificadas
        """
        super().clean()

        # Validar data futura
        if self.data and self.data > timezone.now().date():
            raise ValidationError({"data": "A data da atividade não pode ser futura."})

        # Validar período mensal
        if self.periodo_mes and self.periodo_mes.day != 1:
            raise ValidationError(
                {"periodo_mes": "O período deve ser o primeiro dia do mês."}
            )

        # Validar justificativa para faltas justificadas
        if self.status == "J" and not self.justificativa:
            raise ValidationError(
                {
                    "justificativa": "Justificativa é obrigatória para faltas justificadas."
                }
            )

    def save(self, *args, **kwargs):
        """
        Sobrescreve save para calcular campos automáticos.
        """
        # Calcular período mensal automaticamente
        if self.data and not self.periodo_mes:
            self.periodo_mes = self.data.replace(day=1)

        # Executar validações
        self.clean()

        super().save(*args, **kwargs)

        logger.info(
            f"Registro de presença salvo: {self.aluno.nome} - "
            f"{self.data} - {self.get_status_display()}"
        )

    @property
    def eh_presenca(self):
        """Verifica se é uma presença (P, V1, V2)."""
        return self.status in ["P", "V1", "V2"]

    @property
    def eh_falta(self):
        """Verifica se é uma falta (F, J)."""
        return self.status in ["F", "J"]

    @property
    def eh_voluntario(self):
        """Verifica se é atividade voluntária (V1, V2)."""
        return self.status in ["V1", "V2"]

    @classmethod
    def obter_estatisticas_aluno(
        cls, aluno_id, turma_id=None, periodo_inicio=None, periodo_fim=None
    ):
        """
        Obtém estatísticas de presença para um aluno.

        Args:
            aluno_id: ID do aluno
            turma_id: ID da turma (opcional)
            periodo_inicio: Data início do período (opcional)
            periodo_fim: Data fim do período (opcional)

        Returns:
            dict: Estatísticas calculadas
        """
        queryset = cls.objects.filter(aluno_id=aluno_id)

        if turma_id:
            queryset = queryset.filter(turma_id=turma_id)

        if periodo_inicio:
            queryset = queryset.filter(data__gte=periodo_inicio)

        if periodo_fim:
            queryset = queryset.filter(data__lte=periodo_fim)

        total_registros = queryset.count()
        total_presencas = queryset.filter(status__in=["P", "V1", "V2"]).count()
        total_faltas = queryset.filter(status__in=["F", "J"]).count()
        total_voluntarios = queryset.filter(status__in=["V1", "V2"]).count()

        percentual_presenca = (
            (total_presencas / total_registros * 100) if total_registros > 0 else 0
        )

        return {
            "total_registros": total_registros,
            "total_presencas": total_presencas,
            "total_faltas": total_faltas,
            "total_voluntarios": total_voluntarios,
            "percentual_presenca": round(percentual_presenca, 2),
        }

    @classmethod
    def obter_dados_consolidado_mensal(cls, turma_id, ano, mes):
        """
        Obtém dados consolidados para relatório mensal.

        Args:
            turma_id: ID da turma
            ano: Ano de referência
            mes: Mês de referência

        Returns:
            dict: Dados organizados por aluno
        """
        from datetime import date

        periodo = date(ano, mes, 1)

        registros = (
            cls.objects.filter(turma_id=turma_id, periodo_mes=periodo)
            .select_related("aluno")
            .order_by("aluno__nome", "data")
        )

        dados_alunos = {}

        for registro in registros:
            aluno_id = registro.aluno.id

            if aluno_id not in dados_alunos:
                dados_alunos[aluno_id] = {
                    "aluno": registro.aluno,
                    "registros_por_dia": {},
                    "totais": {"P": 0, "F": 0, "J": 0, "V1": 0, "V2": 0},
                }

            # Organizar por dia
            dia = registro.data.day
            dados_alunos[aluno_id]["registros_por_dia"][dia] = registro

            # Contabilizar totais
            status = registro.status
            dados_alunos[aluno_id]["totais"][status] += 1

        return dados_alunos


class ConfiguracaoPresenca(models.Model):
    """
    Configurações específicas de presença por turma/atividade.

    Define parâmetros para cálculo de carências e limites de presença
    conforme as regras de negócio específicas de cada turma/atividade.
    """

    # Relacionamentos
    turma = models.ForeignKey(
        "turmas.Turma",
        on_delete=models.CASCADE,
        verbose_name="Turma",
        related_name="configuracoes_presenca",
    )

    atividade = models.ForeignKey(
        "atividades.Atividade",
        on_delete=models.CASCADE,
        verbose_name="Atividade",
        related_name="configuracoes_presenca",
    )

    # Configurações de presença
    percentual_minimo_presenca = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("75.00"),
        verbose_name="Percentual Mínimo de Presença (%)",
        help_text="Percentual mínimo de presença exigido",
    )

    obrigatoria = models.BooleanField(
        default=True,
        verbose_name="Atividade Obrigatória",
        help_text="Define se a atividade é obrigatória para a turma",
    )

    peso_calculo = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("1.00"),
        verbose_name="Peso no Cálculo",
        help_text="Peso da atividade no cálculo geral de presença",
    )

    # Campos de controle
    ativo = models.BooleanField(default=True, verbose_name="Configuração Ativa")

    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Configuração de Presença"
        verbose_name_plural = "Configurações de Presença"
        ordering = ["turma__nome", "atividade__nome"]
        unique_together = ["turma", "atividade"]

    def __str__(self):
        return f"{self.turma} - {self.atividade}"

    def clean(self):
        """Validações do modelo."""
        super().clean()

        if self.peso_calculo <= 0:
            raise ValidationError(
                {"peso_calculo": "O peso no cálculo deve ser maior que zero."}
            )

        if self.percentual_minimo_presenca < 0 or self.percentual_minimo_presenca > 100:
            raise ValidationError(
                {"percentual_minimo_presenca": "O percentual deve estar entre 0 e 100."}
            )


class HistoricoMigracao(models.Model):
    """
    Modelo para controlar a migração dos dados antigos.

    Registra quais dados foram migrados e quando, permitindo
    rastreabilidade e rollback se necessário.
    """

    TIPO_CHOICES = [
        ("presenca", "Presença"),
        ("presenca_detalhada", "Presença Detalhada"),
        ("convocacao", "Convocação"),
    ]

    tipo_origem = models.CharField(
        max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo de Origem"
    )

    id_origem = models.PositiveIntegerField(verbose_name="ID do Registro Original")

    registro_presenca = models.ForeignKey(
        RegistroPresenca,
        on_delete=models.CASCADE,
        verbose_name="Registro de Presença Criado",
    )

    migrado_em = models.DateTimeField(auto_now_add=True, verbose_name="Migrado em")

    observacoes = models.TextField(
        blank=True, null=True, verbose_name="Observações da Migração"
    )

    class Meta:
        verbose_name = "Histórico de Migração"
        verbose_name_plural = "Históricos de Migração"
        ordering = ["-migrado_em"]
        unique_together = ["tipo_origem", "id_origem"]

    def __str__(self):
        return f"Migração {self.tipo_origem} #{self.id_origem} -> {self.registro_presenca.id}"
