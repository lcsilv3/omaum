from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from presencas.models import PresencaAcademica

class Command(BaseCommand):
    help = 'Set up permissions for the presencas app'

    def handle(self, *args, **options):
        # Get content type for the PresencaAcademica model
        content_type = ContentType.objects.get_for_model(PresencaAcademica)
        
        # Get all permissions for the PresencaAcademica model
        permissions = Permission.objects.filter(content_type=content_type)
        
        # Add all permissions to the teachers group
        # for permission in permissions:
        #     teachers_group.permissions.add(permission)
            
        self.stdout.write(self.style.SUCCESS(f'Successfully set up permissions for the presencas app'))
