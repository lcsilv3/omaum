from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Iniciacao
from .forms import IniciacaoForm

def listar_iniciacoes(request):
    iniciacoes = Iniciacao.objects.all()
    return render(request, 'iniciacoes/listar_iniciacoes.html', {'iniciacoes': iniciacoes})

def criar_iniciacao(request):
    if request.method == 'POST':
        form = IniciacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Iniciação criada com sucesso.')
            return redirect('listar_iniciacoes')
    else:
        form = IniciacaoForm()
    return render(request, 'iniciacoes/criar_iniciacao.html', {'form': form})

def detalhe_iniciacao(request, id):
    iniciacao = get_object_or_404(Iniciacao, id=id)
    return render(request, 'iniciacoes/detalhe_iniciacao.html', {'iniciacao': iniciacao})

def editar_iniciacao(request, id):
    iniciacao = get_object_or_404(Iniciacao, id=id)
    if request.method == 'POST':
        form = IniciacaoForm(request.POST, instance=iniciacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Iniciação atualizada com sucesso.')
            return redirect('listar_iniciacoes')
    else:
        form = IniciacaoForm(instance=iniciacao)
    return render(request, 'iniciacoes/editar_iniciacao.html', {'form': form, 'iniciacao': iniciacao})

def excluir_iniciacao(request, id):
    iniciacao = get_object_or_404(Iniciacao, id=id)
    if request.method == 'POST':
        iniciacao.delete()
        messages.success(request, 'Iniciação excluída com sucesso.')
        return redirect('listar_iniciacoes')
    return render(request, 'iniciacoes/excluir_iniciacao.html', {'iniciacao': iniciacao})
