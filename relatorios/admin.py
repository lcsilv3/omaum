from django.contrib import admin
from django.contrib.auth.models import Permission

# Registrar permissões no admin para facilitar a atribuição
admin.site.register(Permission)
