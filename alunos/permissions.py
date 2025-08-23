from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from importlib import import_module

TipoCodigo = import_module('alunos.utils').get_tipo_codigo_model()
Codigo = import_module('alunos.utils').get_codigo_model()

def criar_permissoes_codigos():
    content_type_tipo = ContentType.objects.get_for_model(TipoCodigo)
    content_type_codigo = ContentType.objects.get_for_model(Codigo)
    Permission.objects.get_or_create(
        codename='gerenciar_tipocodigo',
        name='Pode gerenciar tipos de código',
        content_type=content_type_tipo
    )
    Permission.objects.get_or_create(
        codename='gerenciar_codigo',
        name='Pode gerenciar códigos',
        content_type=content_type_codigo
    )
