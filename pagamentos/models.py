"""
Modelos para o aplicativo de pagamentos.
"""
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from importlib import import_module


def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


class Pagamento(models.Model):
    """
    Modelo para armazenar informações de pagamentos dos alunos.
    """
    # Opções para o campo status
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('ATRASADO', 'Atrasado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    # Opções para o campo método de pagamento
    METODO_PAGAMENTO_CHOICES = [
        ('DINHEIRO', 'Dinheiro'),
        ('PIX', 'PIX'),
        ('CARTAO_CREDITO', 'Cartão de Crédito'),
        ('CARTAO_DEBITO', 'Cartão de Débito'),
        ('TRANSFERENCIA', 'Transferência Bancária'),
        ('BOLETO', 'Boleto'),
        ('OUTRO', 'Outro'),
    ]
    
    # Relacionamentos
    aluno = models.ForeignKey(
        'alunos.Aluno',
        on_delete=models.CASCADE,
        verbose_name=_('Aluno')
    )
    
    # Campos de pagamento
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Valor')
    )
    
    data_vencimento = models.DateField(
        verbose_name=_('Data de Vencimento')
    )
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDENTE',
        verbose_name=_('Status')
    )
    
    data_pagamento = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Data de Pagamento')
    )
    
    valor_pago = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Valor Pago')
    )
    
    metodo_pagamento = models.CharField(
        max_length=20,
        choices=METODO_PAGAMENTO_CHOICES,
        null=True,
        blank=True,
        verbose_name=_('Método de Pagamento')
    )
    
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Observações')
    )
    
    # Metadados
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Criado em')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Atualizado em')
    )
    
    class Meta:
        verbose_name = _('Pagamento')
        verbose_name_plural = _('Pagamentos')
        ordering = ['-data_vencimento']
    
    def __str__(self):
        return f"Pagamento de {self.aluno.nome} - R$ {self.valor} ({self.get_status_display()})"
    
    def save(self, *args, **kwargs):
        """Sobrescreve o método save para atualizar campos automaticamente."""
        # Se o status for PAGO e não houver data de pagamento, definir como hoje
        if self.status == 'PAGO' and not self.data_pagamento:
            self.data_pagamento = timezone.now().date()
        
        # Se o status for PAGO e não houver valor_pago, usar o valor original
        if self.status == 'PAGO' and not self.valor_pago:
            self.valor_pago = self.valor
        
        # Verificar se o pagamento está atrasado
        hoje = timezone.now().date()
        if self.status == 'PENDENTE' and self.data_vencimento < hoje:
            self.status = 'ATRASADO'
        
        super().save(*args, **kwargs)
