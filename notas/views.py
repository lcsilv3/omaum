from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def listar_notas(request):
    """Lista todas as notas."""
    return render(request, 'notas/listar_notas.html')
