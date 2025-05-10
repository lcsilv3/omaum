from django.db import models
from django.utils import timezone
from alunos.models import Aluno
from matriculas.models import Matricula
from datetime import timedelta


class Pagamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ]
    
    METODO_PAGAMENTO_CHOICES = [
        ('pix', 'PIX'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('boleto', 'Boleto Bancário'),
        ('dinheiro', 'Dinheiro'),
        ('transferencia', 'Transferência Bancária'),
        ('outro', 'Outro'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='pagamentos')
    matricula = models.ForeignKey(
        Matricula, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='pagamentos'
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    metodo_pagamento = models.CharField(
        max_length=20, 
        choices=METODO_PAGAMENTO_CHOICES, 
        null=True, 
        blank=True
    )
    comprovante = models.FileField(
        upload_to='pagamentos/comprovantes/', 
        null=True, 
        blank=True
    )
    numero_parcela = models.PositiveIntegerField(null=True, blank=True)
    total_parcelas = models.PositiveIntegerField(null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-data_vencimento']
    
    def __str__(self):
        return f"Pagamento de {self.aluno} - R$ {self.valor} ({self.get_status_display()})"
    
    @property
    def atrasado(self):
        """Verifica se o pagamento está atrasado."""
        return self.status == 'pendente' and self.data_vencimento < timezone.now().date()
    
    @property
    def dias_atraso(self):
        """Retorna o número de dias em atraso."""
        if not self.atrasado:
            return 0
        return (timezone.now().date() - self.data_vencimento).days
    
    @property
    def descricao_completa(self):
        """Retorna uma descrição completa do pagamento."""
        if self.matricula:
            desc = f"Pagamento de {self.matricula.turma.curso.nome} - {self.matricula.turma.nome}"
            if self.numero_parcela and self.total_parcelas:
                desc += f" ({self.numero_parcela}/{self.total_parcelas})"
            return desc
        return "Pagamento Avulso"
    
    def save(self, *args, **kwargs):
        # Se o status for alterado para 'pago' e não houver data de pagamento, definir como hoje
        if self.status == 'pago' and not self.data_pagamento:
            self.data_pagamento = timezone.now().date()
        
        # Se o status for alterado para 'pendente' ou 'cancelado', limpar a data de pagamento
        if self.status in ['pendente', 'cancelado']:
            self.data_pagamento = None
            self.metodo_pagamento = None
        
        super().save(*args, **kwargs)
