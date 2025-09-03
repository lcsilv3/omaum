from django.db import models
from django.utils import timezone


class ConfiguracaoSistema(models.Model):
    """Configurações globais do sistema"""

    nome_sistema = models.CharField(max_length=100, default="OMAUM")
    versao = models.CharField(max_length=20, default="1.0.0")
    data_atualizacao = models.DateTimeField(default=timezone.now)
    manutencao_ativa = models.BooleanField(default=False)
    mensagem_manutencao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome_sistema} v{self.versao}"

    class Meta:
        verbose_name = "Configuração do Sistema"
        verbose_name_plural = "Configurações do Sistema"


class LogAtividade(models.Model):
    """Registro de atividades do sistema"""

    TIPO_CHOICES = [
        ("INFO", "Informação"),
        ("AVISO", "Aviso"),
        ("ERRO", "Erro"),
        ("DEBUG", "Depuração"),
    ]

    usuario = models.CharField(max_length=100)
    acao = models.CharField(max_length=255)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default="INFO")
    data = models.DateTimeField(default=timezone.now)
    detalhes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo}: {self.acao} por {self.usuario}"

    class Meta:
        verbose_name = "Log de Atividade"
        verbose_name_plural = "Logs de Atividades"
        ordering = ["-data"]  # Garante que os logs mais recentes apareçam primeiro
