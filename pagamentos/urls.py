from django.urls import path
from . import views

app_name = "pagamentos"

urlpatterns = [
    path("", views.listar_pagamentos, name="listar_pagamentos"),
    path(
        "<int:pagamento_id>/",
        views.detalhar_pagamento,
        name="detalhar_pagamento",
    ),
]
