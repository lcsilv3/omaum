from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from core.models import Aluno, Curso, Turma
from core.forms import AlunoForm, CursoForm, TurmaForm, AlunoTurmaForm
from django.contrib.auth import login, authenticate
from .forms import RegistroForm

def home(request):
    return render(request, 'core/home.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = RegistroForm()
    return render(request, 'core/registro.html', {'form': form})

# Aluno views
@login_required
def aluno_list(request):
    alunos = Aluno.objects.all()
    return render(request, 'core/listar_alunos.html', {'alunos': alunos})

@login_required
def aluno_create(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:listar_alunos')
    else:
        form = AlunoForm()
    return render(request, 'core/aluno_form.html', {'form': form})

@login_required
def aluno_detail(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    return render(request, 'core/aluno_detail.html', {'aluno': aluno})

@login_required
def aluno_update(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect('core:listar_alunos')
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'core/aluno_form.html', {'form': form})

@login_required
def aluno_delete(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        aluno.delete()
        return redirect('core:listar_alunos')
    return render(request, 'core/aluno_confirm_delete.html', {'aluno': aluno})

# Turma views
@login_required
def turma_list(request):
    turmas = Turma.objects.all()
    return render(request, 'core/turma_list.html', {'turmas': turmas})

@login_required
def turma_create(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:listar_turmas')
    else:
        form = TurmaForm()
    return render(request, 'core/turma_form.html', {'form': form})

@login_required
def turma_detail(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    return render(request, 'core/turma_detail.html', {'turma': turma})

@login_required
def turma_update(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            return redirect('core:listar_turmas')
    else:
        form = TurmaForm(instance=turma)
    return render(request, 'core/turma_form.html', {'form': form})

@login_required
def turma_delete(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    if request.method == 'POST':
        turma.delete()
        return redirect('core:listar_turmas')
    return render(request, 'core/turma_confirm_delete.html', {'turma': turma})

# Presença views
@login_required
def listar_presencas_academicas(request):
    # Adicione a lógica para listar presenças acadêmicas
    pass

# Cargo views
@login_required
def listar_cargos_administrativos(request):
    # Adicione a lógica para listar cargos administrativos
    pass

# Relatório views
@login_required
def relatorio_alunos(request):
    # Adicione a lógica para gerar relatórios de alunos
    pass

# Punição views
@login_required
def listar_punicoes(request):
    # Adicione a lógica para listar punições
    pass

# Iniciação views
@login_required
def listar_iniciacoes(request):
    # Adicione a lógica para listar iniciações
    pass
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        # Forçar a geração do token CSRF
        csrf_token = get_token(request)

        logger.info(f"GET CSRF cookie: {request.META.get('CSRF_COOKIE')}")
        logger.info(f"GET CSRF token: {csrf_token}")
        response = super().get(request, *args, **kwargs)
        response.set_cookie('csrftoken', csrf_token, httponly=False, samesite='Lax')
        return response

    def post(self, request, *args, **kwargs):
        logger.info(f"POST CSRF cookie: {request.META.get('CSRF_COOKIE')}")
        logger.info(f"POST CSRF token: {request.POST.get('csrfmiddlewaretoken')}")
        return super().post(request, *args, **kwargs)

def test_csrf(request):
    csrf_token = get_token(request)
    return HttpResponse(f"CSRF Token: {csrf_token}")
