from django.db import models
from django.utils import timezone


class Pagamento(models.Model):
    aluno = models.ForeignKey('alunos.Aluno', on_delete=models.CASCADE, 
                              related_name='pagamentos')
    observacoes = models.CharField(max_length=255, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('ATRASADO', 'Atrasado'),
        ('CANCELADO', 'Cancelado'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Se o status for alterado para PAGO e não houver data de pagamento, definir para hoje
        if self.status == 'PAGO' and not self.data_pagamento:
            self.data_pagamento = timezone.now().date()
        
        # Se o status for alterado para PAGO e não houver valor pago, usar o valor original
        if self.status == 'PAGO' and not self.valor_pago:
            self.valor_pago = self.valor
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Pagamento de {self.aluno.nome} - R${self.valor} ({self.get_status_display()})"
    
    class Meta:
        ordering = ['-data_vencimento']
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
