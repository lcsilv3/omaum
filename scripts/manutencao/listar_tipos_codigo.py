import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from alunos.utils import get_tipo_codigo_model

TipoCodigo = get_tipo_codigo_model()
if not TipoCodigo:
    print("Modelo TipoCodigo não encontrado!")
else:
    print("Tipos de Código cadastrados:")
    for tipo in TipoCodigo.objects.all():
        print(f"- {tipo.id}: {tipo.nome}")
