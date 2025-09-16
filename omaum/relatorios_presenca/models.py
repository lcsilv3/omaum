"""
Modelos para o app relatorios_presenca.
Gerencia configurações e histórico de relatórios de presença.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
import json


class ConfiguracaoRelatorio(models.Model):
    """
    Configurações para geração de relatórios de presença.

    Permite personalizar templates, formatos e parâmetros
    para diferentes tipos de relatórios.
    """

    TIPO_RELATORIO_CHOICES = [
        ("consolidado", "Consolidado por Período (grau)"),
        ("mensal", "Apuração Mensal (mes01-99)"),
        ("coleta", "Formulário de Coleta (mod)"),
        ("controle_geral", "Controle Geral da Turma (pcg)"),
    ]

    FORMATO_CHOICES = [
        ("excel", "Excel (.xlsx)"),
        ("pdf", "PDF (.pdf)"),
        ("csv", "CSV (.csv)"),
    ]

    nome = models.CharField(
        max_length=200,
        verbose_name="Nome da Configuração",
        help_text="Nome identificador da configuração",
    )

    tipo_relatorio = models.CharField(
        max_length=20, choices=TIPO_RELATORIO_CHOICES, verbose_name="Tipo de Relatório"
    )

    formato_saida = models.CharField(
        max_length=10,
        choices=FORMATO_CHOICES,
        default="excel",
        verbose_name="Formato de Saída",
    )

    template_excel = models.FileField(
        upload_to="templates_relatorio/",
        blank=True,
        null=True,
        verbose_name="Template Excel",
        help_text="Arquivo Excel modelo para manter formatação visual",
    )

    parametros_padrao = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Parâmetros Padrão",
        help_text="Configurações padrão em formato JSON",
    )

    ativo = models.BooleanField(default=True, verbose_name="Configuração Ativa")

    criado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Criado por",
    )

    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Configuração de Relatório"
        verbose_name_plural = "Configurações de Relatórios"
        ordering = ["tipo_relatorio", "nome"]

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_relatorio_display()})"

    def clean(self):
        """Validações customizadas."""
        super().clean()

        # Validar JSON dos parâmetros
        if self.parametros_padrao:
            try:
                if isinstance(self.parametros_padrao, str):
                    json.loads(self.parametros_padrao)
            except json.JSONDecodeError:
                raise ValidationError(
                    {
                        "parametros_padrao": "Parâmetros devem estar em formato JSON válido."
                    }
                )


class HistoricoRelatorio(models.Model):
    """
    Histórico de relatórios gerados.

    Mantém registro de todos os relatórios gerados,
    permitindo rastreabilidade e regeração.
    """

    STATUS_CHOICES = [
        ("processando", "Processando"),
        ("concluido", "Concluído"),
        ("erro", "Erro"),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuário",
        related_name="relatorios_gerados",
    )

    configuracao = models.ForeignKey(
        ConfiguracaoRelatorio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Configuração Utilizada",
    )

    tipo_relatorio = models.CharField(max_length=20, verbose_name="Tipo de Relatório")

    parametros = models.JSONField(
        default=dict,
        verbose_name="Parâmetros Utilizados",
        help_text="Parâmetros específicos usados na geração",
    )

    arquivo_gerado = models.FileField(
        upload_to="relatorios_gerados/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Arquivo Gerado",
    )

    nome_arquivo = models.CharField(
        max_length=255, blank=True, verbose_name="Nome do Arquivo"
    )

    tamanho_arquivo = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Tamanho do Arquivo (bytes)"
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="processando",
        verbose_name="Status",
    )

    mensagem_erro = models.TextField(
        blank=True, null=True, verbose_name="Mensagem de Erro"
    )

    tempo_processamento = models.DurationField(
        null=True, blank=True, verbose_name="Tempo de Processamento"
    )

    data_geracao = models.DateTimeField(
        auto_now_add=True, verbose_name="Data de Geração"
    )

    class Meta:
        verbose_name = "Histórico de Relatório"
        verbose_name_plural = "Históricos de Relatórios"
        ordering = ["-data_geracao"]
        indexes = [
            models.Index(fields=["usuario", "data_geracao"]),
            models.Index(fields=["tipo_relatorio"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.tipo_relatorio} - {self.usuario.username} - {self.data_geracao.strftime('%d/%m/%Y %H:%M')}"

    @property
    def tamanho_arquivo_formatado(self):
        """Retorna tamanho do arquivo formatado."""
        if not self.tamanho_arquivo:
            return "N/A"

        if self.tamanho_arquivo < 1024:
            return f"{self.tamanho_arquivo} bytes"
        elif self.tamanho_arquivo < 1024 * 1024:
            return f"{self.tamanho_arquivo / 1024:.1f} KB"
        else:
            return f"{self.tamanho_arquivo / (1024 * 1024):.1f} MB"

    def marcar_como_concluido(self, arquivo_path, tamanho):
        """Marca relatório como concluído."""
        self.status = "concluido"
        self.arquivo_gerado = arquivo_path
        self.tamanho_arquivo = tamanho
        self.save()

    def marcar_como_erro(self, mensagem_erro):
        """Marca relatório como erro."""
        self.status = "erro"
        self.mensagem_erro = mensagem_erro
        self.save()


class AgendamentoRelatorio(models.Model):
    """
    Agendamento de relatórios automáticos.

    Permite configurar geração automática de relatórios
    em intervalos específicos.
    """

    FREQUENCIA_CHOICES = [
        ("diario", "Diário"),
        ("semanal", "Semanal"),
        ("quinzenal", "Quinzenal"),
        ("mensal", "Mensal"),
        ("trimestral", "Trimestral"),
    ]

    nome = models.CharField(max_length=200, verbose_name="Nome do Agendamento")

    configuracao = models.ForeignKey(
        ConfiguracaoRelatorio,
        on_delete=models.CASCADE,
        verbose_name="Configuração do Relatório",
    )

    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Usuário Responsável"
    )

    frequencia = models.CharField(
        max_length=15, choices=FREQUENCIA_CHOICES, verbose_name="Frequência"
    )

    hora_execucao = models.TimeField(default="08:00", verbose_name="Hora de Execução")

    emails_destino = models.TextField(
        verbose_name="E-mails de Destino", help_text="E-mails separados por vírgula"
    )

    parametros_fixos = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Parâmetros Fixos",
        help_text="Parâmetros que não mudam entre execuções",
    )

    ativo = models.BooleanField(default=True, verbose_name="Agendamento Ativo")

    proxima_execucao = models.DateTimeField(
        null=True, blank=True, verbose_name="Próxima Execução"
    )

    ultima_execucao = models.DateTimeField(
        null=True, blank=True, verbose_name="Última Execução"
    )

    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Agendamento de Relatório"
        verbose_name_plural = "Agendamentos de Relatórios"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} - {self.get_frequencia_display()}"

    def calcular_proxima_execucao(self):
        """Calcula a próxima data de execução."""
        from datetime import timedelta

        agora = timezone.now()
        base_date = agora.replace(
            hour=self.hora_execucao.hour,
            minute=self.hora_execucao.minute,
            second=0,
            microsecond=0,
        )

        if self.frequencia == "diario":
            if base_date <= agora:
                base_date += timedelta(days=1)
            self.proxima_execucao = base_date

        elif self.frequencia == "semanal":
            dias_ate_proxima = 7 - agora.weekday()
            if dias_ate_proxima == 7 and base_date <= agora:
                dias_ate_proxima = 7
            self.proxima_execucao = base_date + timedelta(days=dias_ate_proxima)

        elif self.frequencia == "quinzenal":
            self.proxima_execucao = base_date + timedelta(days=15)

        elif self.frequencia == "mensal":
            if agora.month == 12:
                proximo_mes = base_date.replace(year=agora.year + 1, month=1)
            else:
                proximo_mes = base_date.replace(month=agora.month + 1)
            self.proxima_execucao = proximo_mes

        elif self.frequencia == "trimestral":
            meses_adicionar = 3
            novo_mes = agora.month + meses_adicionar
            novo_ano = agora.year

            while novo_mes > 12:
                novo_mes -= 12
                novo_ano += 1

            self.proxima_execucao = base_date.replace(year=novo_ano, month=novo_mes)

    def save(self, *args, **kwargs):
        """Sobrescreve save para calcular próxima execução."""
        if not self.proxima_execucao:
            self.calcular_proxima_execucao()
        super().save(*args, **kwargs)


class TemplatePersonalizado(models.Model):
    """
    Templates personalizados para relatórios.

    Permite criar templates específicos para diferentes
    necessidades de formatação.
    """

    nome = models.CharField(max_length=200, verbose_name="Nome do Template")

    tipo_relatorio = models.CharField(
        max_length=20,
        choices=ConfiguracaoRelatorio.TIPO_RELATORIO_CHOICES,
        verbose_name="Tipo de Relatório",
    )

    arquivo_template = models.FileField(
        upload_to="templates_personalizados/", verbose_name="Arquivo do Template"
    )

    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    ativo = models.BooleanField(default=True, verbose_name="Template Ativo")

    criado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Criado por",
    )

    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Template Personalizado"
        verbose_name_plural = "Templates Personalizados"
        ordering = ["tipo_relatorio", "nome"]

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_relatorio_display()})"
