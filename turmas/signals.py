"""
Signals para o módulo de Turmas.

Este módulo contém os signals que são disparados quando ocorrem
eventos relacionados a turmas, como criação de atividades padrão.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender='turmas.Turma')
def criar_atividades_padrao(sender, instance, created, **kwargs):
    """
    Cria automaticamente as atividades padrão 'Aula' e 'Plenilúnio' 
    quando uma nova turma é criada.
    
    Args:
        sender: O modelo que enviou o signal (Turma)
        instance: A instância da turma que foi salva
        created: Boolean indicando se é uma nova turma
        **kwargs: Argumentos adicionais
    """
    # Só cria atividades na criação inicial da turma
    if not created:
        return
    
    try:
        # Importar o modelo Atividade dinamicamente para evitar importação circular
        from importlib import import_module
        atividades_module = import_module('atividades.models')
        Atividade = getattr(atividades_module, 'Atividade')
        
        # Data padrão: hoje se não tiver data_inicio_ativ
        data_padrao = instance.data_inicio_ativ if instance.data_inicio_ativ else timezone.now().date()
        
        # Criar Atividade "Aula"
        atividade_aula = Atividade.objects.create(
            nome="Aula",
            tipo_atividade="AULA",
            data_inicio=data_padrao,
            hora_inicio=timezone.now().time(),  # Horário padrão (será ajustado depois)
            status="PENDENTE",
            curso=instance.curso if hasattr(instance, 'curso') else None,
        )
        atividade_aula.turmas.add(instance)
        
        logger.info(
            f"Atividade 'Aula' (ID: {atividade_aula.id}) criada automaticamente "
            f"para a turma '{instance.nome}' (ID: {instance.id})"
        )
        
        # Criar Atividade "Plenilúnio"
        atividade_plenilunio = Atividade.objects.create(
            nome="Plenilúnio",
            tipo_atividade="PLENILUNIO",
            data_inicio=data_padrao,
            hora_inicio=timezone.now().time(),  # Horário padrão (será ajustado depois)
            status="PENDENTE",
            curso=instance.curso if hasattr(instance, 'curso') else None,
        )
        atividade_plenilunio.turmas.add(instance)
        
        logger.info(
            f"Atividade 'Plenilúnio' (ID: {atividade_plenilunio.id}) criada automaticamente "
            f"para a turma '{instance.nome}' (ID: {instance.id})"
        )
        
    except Exception as e:
        logger.error(
            f"Erro ao criar atividades padrão para a turma '{instance.nome}' (ID: {instance.id}): {str(e)}",
            exc_info=True
        )
