"""Script de teste para a view listar_turmas."""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings.development")
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from turmas.views import listar_turmas

# Criar factory e request
rf = RequestFactory()
req = rf.get("/turmas/")

# Obter ou criar usuário
user = User.objects.first()
if not user:
    user = User.objects.create_user("testuser", "test@test.com", "testpass123")

req.user = user

# Chamar a view
response = listar_turmas(req)

# Exibir resultados
print("✓ Status:", response.status_code)
print("✓ Turmas no contexto:", response.context_data["total_turmas"])
print("✓ Cursos disponíveis:", len(response.context_data["cursos"]))
print("✓ Páginas:", response.context_data["page_obj"].paginator.num_pages)
print("\n✅ SUCESSO! View listar_turmas funcionando corretamente.")
