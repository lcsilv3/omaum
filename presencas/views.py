from django.shortcuts import render, redirect
from .models import PresencaAcademica
from .forms import PresencaForm

def registrar_presenca(request):
    if request.method == 'POST':
        form = PresencaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_presencas')
    else:
        form = PresencaForm()
    return render(request, 'presencas/registrar_presenca.html', {'form': form})

def lista_presencas(request):
    presencas = PresencaAcademica.objects.all()
    return render(request, 'presencas/lista_presencas.html', {'presencas': presencas})
