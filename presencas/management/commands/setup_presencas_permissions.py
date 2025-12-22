from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from presencas.models import RegistroPresenca


class Command(BaseCommand):
    help = "Set up permissions for the presencas app"

    def handle(self, *args, **options):
        # Get content type for the RegistroPresenca model
        content_type = ContentType.objects.get_for_model(RegistroPresenca)

        # Get all permissions for the RegistroPresenca model
        Permission.objects.filter(content_type=content_type)

        # Add all permissions to the teachers group
        # for permission in permissions:
        #     teachers_group.permissions.add(permission)

        self.stdout.write(
            self.style.SUCCESS("Successfully set up permissions for the presencas app")
        )
