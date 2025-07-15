"""
Módulo de views para o aplicativo presencas.
"""

# Importar views das extensões para manter compatibilidade com URLs
from ..views_ext.academicas import listar_presencas_academicas


# Placeholder functions para URLs que não têm implementação ainda
def registrar_presenca_academica(request):
    from django.http import HttpResponse
    return HttpResponse("Função não implementada ainda")


def editar_presenca_academica(request, pk):
    from django.http import HttpResponse
    return HttpResponse("Função não implementada ainda")


def excluir_presenca_academica(request, pk):
    from django.http import HttpResponse
    return HttpResponse("Função não implementada ainda")


def detalhar_presenca_academica(request, pk):
    from django.http import HttpResponse
    return HttpResponse("Função não implementada ainda")


def exportar_presencas_academicas(request):
    from django.http import HttpResponse
    return HttpResponse("Função não implementada ainda")


def importar_presencas_academicas(request):
    from django.http import HttpResponse
    return HttpResponse("Função não implementada ainda")


def listar_observacoes_presenca(request):
    from django.http import HttpResponse
    return HttpResponse("Função não implementada ainda")
