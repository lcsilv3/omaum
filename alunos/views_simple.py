from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from datetime import date
from .models import Aluno


@login_required
def listar_alunos_simple(request):
    alunos = Aluno.objects.all()
    return render(request, "alunos/listar_alunos_simple.html", {"alunos": alunos})


@login_required
def criar_aluno_simple(request):
    if request.method == "POST":
        data = request.POST
        aluno = Aluno.objects.create(
            cpf=data.get("cpf", "99999999999"),
            nome=data.get("nome", "Aluno Teste"),
            data_nascimento=data.get("data_nascimento", date(2000, 1, 1)),
            email=data.get("email", "teste@exemplo.com"),
        )
        return redirect(reverse("alunos:detalhar_aluno_simple", args=[aluno.cpf]))
    return render(request, "alunos/criar_aluno_simple.html")


@login_required
def detalhar_aluno_simple(request, cpf):
    aluno = get_object_or_404(Aluno, cpf=cpf)
    return render(request, "alunos/detalhar_aluno_simple.html", {"aluno": aluno})


@login_required
def editar_aluno_simple(request, cpf):
    aluno = get_object_or_404(Aluno, cpf=cpf)
    if request.method == "POST":
        aluno.nome = request.POST.get("nome", aluno.nome)
        aluno.save()
        return redirect(reverse("alunos:detalhar_aluno_simple", args=[aluno.cpf]))
    return render(request, "alunos/editar_aluno_simple.html", {"aluno": aluno})


@login_required
def excluir_aluno_simple(request, cpf):
    aluno = get_object_or_404(Aluno, cpf=cpf)
    if request.method == "POST":
        aluno.delete()
        return redirect(reverse("alunos:listar_alunos_simple"))
    return render(request, "alunos/excluir_aluno_simple.html", {"aluno": aluno})
