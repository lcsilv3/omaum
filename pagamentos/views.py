from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def listar_pagamentos(request):
    """Lista todos os pagamentos."""
    return render(request, "pagamentos/listar_pagamentos.html")
