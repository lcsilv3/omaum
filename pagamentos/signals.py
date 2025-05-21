"""
Signals para o aplicativo de pagamentos.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender='pagamentos.Pagamento')
def atualizar_status_pagamento(sender, instance, created, **kwargs):
    """
    Atualiza o status do pagamento com base na data de vencimento.
    """
    try:
        # Evitar recursão infinita
        if kwargs.get('update_fields') == {'status'}:
            return
        
        # Se o pagamento já foi pago ou cancelado, não alterar o status
        if instance.status in ['PAGO', 'CANCELADO']:
            return
        
        # Verificar se o pagamento está atrasado
        hoje = timezone.now().date()
        if instance.status == 'PENDENTE' and instance.data_vencimento < hoje:
            # Atualizar para ATRASADO
            sender.objects.filter(pk=instance.pk).update(status='ATRASADO')
            logger.info(f"Pagamento {instance.pk} atualizado para ATRASADO")
    
    except Exception as e:
        logger.error(f"Erro ao atualizar status do pagamento: {str(e)}")