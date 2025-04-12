from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def listar_matriculas(request):
    """Lista todas as matrículas."""
    return render(request, 'matriculas/listar_matriculas.html')

@login_required
def detalhar_matricula(request, id):
    """Exibe os detalhes de uma matrícula."""
    return render(request, 'matriculas/detalhes_matricula.html')

@login_required
def realizar_matricula(request):
    """Realiza uma nova matrícula."""
    return render(request, 'matriculas/realizar_matricula.html')
