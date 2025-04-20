from django.shortcuts import render, get_object_or_404
from .models import Nota


def listar_notas(request):
    notas = Nota.objects.all()
    return render(request, "notas/listar_notas.html", {"notas": notas})


def detalhar_nota(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id)
    return render(request, "notas/detalhar_nota.html", {"nota": nota})
