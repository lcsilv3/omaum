from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import HttpResponse
import csv
from io import StringIO
from importlib import import_module

# Importar modelos e formulários
Aluno = import_module('alunos.models').Aluno
AlunoForm = import_module('alunos.forms').AlunoForm
ImportForm = import_module('alunos.forms').ImportForm
# Obter o modelo Curso de onde estiver definido
Curso = import_module('cursos.models').Curso

@login_required
def listar_alunos(request):
    query = request.GET.get('q')
    curso_id = request.GET.get('curso')

    queryset = Aluno.objects.all()

    if query:
        queryset = queryset.filter(
            Q(nome__icontains=query) | 
            Q(cpf__icontains=query) | 
            Q(email__icontains=query)
        )

    if curso_id:
        queryset = queryset.filter(curso_id=curso_id)

    queryset = queryset.select_related('curso')

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cursos = Curso.objects.all()

    return render(request, 'alunos/listar_alunos.html', {
        'page_obj': page_obj,
        'alunos': page_obj,
        'query': query,
        'cursos': cursos,
        'curso_selecionado': curso_id
    })

@login_required
def cadastrar_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _('Aluno cadastrado com sucesso!'))
            return redirect('alunos:listar')
        else:
            messages.error(request, _('Erro ao cadastrar aluno. Verifique os dados.'))
    else:
        form = AlunoForm()
    return render(request, 'alunos/aluno_form.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Aluno
from .forms import AlunoForm
@login_required
def editar_aluno(request, cpf):
    aluno = get_object_or_404(Aluno, cpf=cpf)
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, _('Dados do aluno atualizados com sucesso!'))
            return redirect('alunos:detalhes', cpf=aluno.cpf)
        else:
            messages.error(request, _('Erro ao atualizar dados do aluno. Por favor, verifique os dados.'))
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'alunos/editar_aluno.html', {'form': form, 'aluno': aluno})

@login_required
def detalhes_aluno(request, cpf):
    aluno = get_object_or_404(Aluno, cpf=cpf)
    return render(request, 'alunos/detalhes_aluno.html', {'aluno': aluno})

@login_required
def excluir_aluno(request, cpf):
    aluno = get_object_or_404(Aluno, cpf=cpf)
    if request.method == 'POST':
        if request.POST.get('confirmar') == 'sim':
            aluno.delete()
            messages.success(request, _('Aluno excluído com sucesso!'))
            return redirect('alunos:listar')
        else:
            messages.info(request, _('Exclusão cancelada.'))
            return redirect('alunos:detalhes', cpf=cpf)
    return render(request, 'alunos/excluir_aluno.html', {'aluno': aluno})

@login_required
def buscar_alunos(request):
    query = request.GET.get('q', '')
    alunos = Aluno.objects.filter(
        Q(nome__icontains=query) |
        Q(cpf__icontains=query) |
        Q(email__icontains=query)
    ) if query else Aluno.objects.none()
    return render(request, 'alunos/buscar.html', {'alunos': alunos, 'query': query})

@login_required
def exportar_alunos(request):
    alunos = Aluno.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="alunos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nome', 'CPF', 'Email', 'Data de Nascimento'])

    for aluno in alunos:
        writer.writerow([aluno.nome, aluno.cpf, aluno.email, aluno.data_nascimento])
    return response

@login_required
def importar_alunos(request):
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = StringIO(decoded_file)
            next(io_string)  # Pular o cabeçalho
            for row in csv.reader(io_string, delimiter=','):
                _, created = Aluno.objects.update_or_create(
                    cpf=row[1],
                    defaults={
                        'nome': row[0],
                        'email': row[2],
                        'data_nascimento': row[3],
                    }
                )
            messages.success(request, _('Alunos importados com sucesso!'))
            return redirect('alunos:listar')
    else:
        form = ImportForm()
    return render(request, 'alunos/importar.html', {'form': form})

@login_required
def relatorio_alunos(request):
    alunos = Aluno.objects.all()
    total_alunos = alunos.count()
    # Remover referência a curso se não existir no modelo
    context = {
        'alunos': alunos,
        'total_alunos': total_alunos,
    }
    return render(request, 'alunos/relatorio.html', context)

@login_required
def dashboard(request):
    context = {
        'total_alunos': Aluno.objects.count(),
        'alunos_ativos': Aluno.objects.filter(status='A').count(),
        'alunos_recentes': Aluno.objects.order_by('-created_at')[:5],
    }
    
    try:
        Curso = apps.get_model('core', 'Curso')
        context['total_cursos'] = Curso.objects.count()
        
        # Dados para o gráfico
        cursos = Curso.objects.all()
        context['cursos_labels'] = [curso.nome for curso in cursos]
        context['alunos_por_curso_data'] = [0] * len(cursos)  # Placeholder
    except:
        context['total_cursos'] = 0
        context['cursos_labels'] = []
        context['alunos_por_curso_data'] = []

    return render(request, 'alunos/dashboard.html', context)