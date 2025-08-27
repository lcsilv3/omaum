from django.urls import path
from . import autocomplete

urlpatterns = [
    path(
        "cidade-autocomplete/",
        autocomplete.CidadeAutocomplete.as_view(),
        name="cidade-autocomplete",
    ),
    path(
        "bairro-autocomplete/",
        autocomplete.BairroAutocomplete.as_view(),
        name="bairro-autocomplete",
    ),
    path(
        "tipo-codigo-autocomplete/",
        autocomplete.TipoCodigoAutocomplete.as_view(),
        name="tipo-codigo-autocomplete",
    ),
    path(
        "codigo-autocomplete/",
        autocomplete.CodigoAutocomplete.as_view(),
        name="codigo-autocomplete",
    ),
]
