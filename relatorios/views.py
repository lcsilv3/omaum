from django.shortcuts import render
from core.models import Aluno  # Assumindo que o modelo Aluno está no aplicativo 'core'

def relatorio_alunos(request):
    alunos = Aluno.objects.all()
    context = {
        'alunos': alunos,
    }
    return render(request, 'relatorios/relatorio_alunos.html', context)
