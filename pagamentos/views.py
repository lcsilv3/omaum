from django.shortcuts import render, get_object_or_404
from .models import Pagamento


def listar_pagamentos(request):
    pagamentos = Pagamento.objects.all()
    return render(
        request,
        "pagamentos/listar_pagamentos.html",
        {"pagamentos": pagamentos},
    )


def detalhar_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    return render(
        request, "pagamentos/detalhar_pagamento.html", {"pagamento": pagamento}
    )
