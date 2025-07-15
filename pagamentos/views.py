import logging
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import models
from django.urls import reverse
from .forms import PagamentoForm, FiltroPagamentosForm, PagamentoRapidoForm
from .models import Pagamento
from .exporters import exportar_pagamentos_csv, exportar_pagamentos_excel, exportar_pagamentos_pdf
from pagamentos.helpers import get_aluno_model  # helpers.py deve conter get_aluno_model

from .views.pagamento_views import (
    listar_pagamentos,
    criar_pagamento,
    editar_pagamento,
    excluir_pagamento,
    detalhar_pagamento,
    pagamentos_aluno,
    registrar_pagamento_rapido,
    importar_pagamentos_csv,
    exportar_pagamentos_csv,
    exportar_pagamentos_excel,
    exportar_pagamentos_pdf,
)

from .views.relatorio_views import (
    relatorio_financeiro,
    exportar_pagamentos_excel,
    exportar_pagamentos_pdf,
    dados_grafico_pagamentos,
    pagamentos_por_turma,
    dados_distribuicao_pagamentos,
)

from .views.dashboard_views import (
    painel_geral,
    painel_mensal,
    painel_financeiro,
)

# Função duplicada - removida para evitar F811
# def editar_pagamento(request, id):
#     pagamento = get_object_or_404(Pagamento, id=id)
#     if request.method == 'POST':
#         form = PagamentoForm(request.POST, request.FILES, instance=pagamento)
#         if form.is_valid():
#             form.save()
#             # redirecione conforme sua lógica
#         else:
#             # Se inválido, o form já vem preenchido com os dados e erros
#             pass
#     else:
#         form = PagamentoForm(instance=pagamento)
#     return render(request, 'pagamentos/editar_pagamento.html', {
#         'form': form,
#         'pagamento': pagamento,
#     })