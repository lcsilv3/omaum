import logging

from django.dispatch import receiver
from django.template.signals import template_rendered

logger = logging.getLogger(__name__)


@receiver(template_rendered)
def log_template_renders(sender, template, context, **kwargs):
    """
    Loga cada vez que um template é renderizado. Útil para depuração.
    """
    logger.debug(f"Template renderizado: {template.name}")
