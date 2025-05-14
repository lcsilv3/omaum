from django.urls import path
from . import views

app_name = "pagamentos"

urlpatterns = [
    path("", views.listar_pagamentos, name="listar_pagamentos"),
    path("criar/", views.criar_pagamento, name="criar_pagamento"),
    path("<int:pagamento_id>/", views.detalhar_pagamento, name="detalhar_pagamento"),
    path("<int:pagamento_id>/editar/", views.editar_pagamento, name="editar_pagamento"),
    path("<int:pagamento_id>/excluir/", views.excluir_pagamento, name="excluir_pagamento"),
    path("<int:pagamento_id>/registrar/", views.registrar_pagamento, name="registrar_pagamento"),
    path("exportar/csv/", views.exportar_pagamentos_csv, name="exportar_pagamentos_csv"),
    path("exportar/excel/", views.exportar_pagamentos_excel, name="exportar_pagamentos_excel"),
    path("dashboard/", views.dashboard_pagamentos, name="dashboard_pagamentos"),
    # Adicionar a URL para buscar alunos
    path("api/buscar-alunos/", views.buscar_alunos, name="buscar_alunos"),
]