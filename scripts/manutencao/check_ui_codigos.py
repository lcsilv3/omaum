import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings.development")
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.conf import settings

print("Usando settings:", os.environ.get("DJANGO_SETTINGS_MODULE"))
print("DATABASES:", settings.DATABASES)

User = get_user_model()
username = "omaum_debug_admin"
password = "debugpass123"
user, created = User.objects.get_or_create(username=username)
if created:
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print("Criado usuário temporário:", username)
else:
    print("Usuário já existe:", username)

client = Client()
logged = client.login(username=username, password=password)
print("Login bem-sucedido?", logged)

# Chamar endpoint AJAX de tipos (forçar Host válido para evitar DisallowedHost)
resp = client.get("/alunos/api/tipos-codigos/", HTTP_HOST="127.0.0.1")
print("\nGET /alunos/api/tipos-codigos/ =>", resp.status_code)
try:
    print("json:", json.dumps(resp.json(), indent=2, ensure_ascii=False))
except Exception:
    print("Resposta (texto):", resp.content.decode(errors="replace"))

# Chamar página de listagem de tipos (server-rendered) — também forçar Host
resp2 = client.get("/alunos/tipos/", HTTP_HOST="127.0.0.1")
print("\nGET /alunos/tipos/ =>", resp2.status_code)
text = resp2.content.decode(errors="replace")
if "Nenhum tipo de código cadastrado." in text:
    print("Página contém a mensagem de vazio: sim")
else:
    print("Página contém a mensagem de vazio: NÃO")

# Mostrar breve trecho do HTML (2000 chars)
print("\nTrecho HTML (até 2000 chars):")
print(text[:2000])
