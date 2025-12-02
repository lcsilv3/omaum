import os
import sys

# Ajustes de caminho e settings
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings.production")

import django

django.setup()

from alunos.models import Codigo, TipoCodigo
from django.db.models import Count

print("Top 20 tipos por quantidade de códigos:")
for t in TipoCodigo.objects.annotate(qtd=Count("codigos")).order_by("-qtd")[:20]:
    print(f"{t.id} - {t.nome} -> {t.qtd}")

print("\nAmostra de 20 códigos:")
for c in Codigo.objects.select_related("tipo_codigo").all()[:20]:
    tipo = c.tipo_codigo.nome if c.tipo_codigo else "N/A"
    descricao = c.descricao or ""
    print(f"{c.id} | {tipo} | {c.nome} | {descricao[:120]}")
