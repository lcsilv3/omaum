from django.db import models

class ConfiguracaoCorporativa(models.Model):
    """Configurações corporativas do sistema."""
    nome_organizacao = models.CharField(
        max_length=200,
        default='OM-AUM (Ordem Mística de Aspiração Universal ao Mestrado)'
    )
    logo = models.ImageField(upload_to='corporativo/logos/', blank=True)
    endereco = models.TextField(blank=True)
    telefone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    site = models.URLField(blank=True)
    mostrar_data_hora_cabecalho = models.BooleanField(default=True)
    formato_data_hora = models.CharField(
        max_length=50,
        default='%d/%m/%Y - %H:%M'
    )
    mostrar_numeracao_pagina = models.BooleanField(default=True)
    texto_rodape_personalizado = models.CharField(
        max_length=200,
        blank=True,
        help_text='Texto adicional para o rodapé (opcional)'
    )
    class Meta:
        verbose_name = 'Configuração Corporativa'
        verbose_name_plural = 'Configurações Corporativas'
    def __str__(self):
        return self.nome_organizacao
    @classmethod
    def get_configuracao(cls):
        config, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'nome_organizacao': 'OM-AUM (Ordem Mística de Aspiração Universal ao Mestrado)'
            }
        )
        return config
