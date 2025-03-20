from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Punicao
from .forms import PunicaoForm

def criar_punicao(request):
    if request.method == 'POST':
        form = PunicaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Punição criada com sucesso!')
            return redirect('listar_punicoes')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = PunicaoForm()
    return render(request, 'punicoes/criar_punicao.html', {'form': form})

def editar_punicao(request, id):
    punicao = get_object_or_404(Punicao, id=id)
    if request.method == 'POST':
        form = PunicaoForm(request.POST, instance=punicao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Punição atualizada com sucesso!')
            return redirect('listar_punicoes')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = PunicaoForm(instance=punicao)
    return render(request, 'punicoes/editar_punicao.html', {'form': form, 'punicao': punicao})

def listar_punicoes(request):
    punicoes = Punicao.objects.all()
    return render(request, 'punicoes/listar_punicoes.html', {'punicoes': punicoes})

def detalhe_punicao(request, id):
    punicao = get_object_or_404(Punicao, id=id)
    return render(request, 'punicoes/detalhe_punicao.html', {'punicao': punicao})

def excluir_punicao(request, id):
    punicao = get_object_or_404(Punicao, id=id)
    if request.method == 'POST':
        punicao.delete()
        messages.success(request, 'Punição excluída com sucesso.')
        return redirect('listar_punicoes')
    return render(request, 'punicoes/excluir_punicao.html', {'punicao': punicao})