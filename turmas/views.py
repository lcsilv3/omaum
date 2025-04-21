from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from importlib import import_module
from django.utils import timezone
from django.conf import settings
from .forms import TurmaForm

def get_model(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)


def get_turma_model():
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


@login_required
def listar_turmas(request):
    Turma = get_turma_model()
    turmas = Turma.objects.all()
    # Preparar informações adicionais para cada turma
    turmas_com_info = []
    for turma in turmas:
        # Verificar pendências na instrutoria
        tem_pendencia_instrutoria = (
            not turma.instrutor
            or not turma.instrutor_auxiliar
            or not turma.auxiliar_instrucao
        )
        # Calcular vagas disponíveis
        total_alunos = (
            turma.matriculas.filter(status="A").count()
            if hasattr(turma, "matriculas")
            else 0
        )
        vagas_disponiveis = turma.vagas - total_alunos

        turmas_com_info.append(
            {
                "turma": turma,
                "total_alunos": total_alunos,
                "vagas_disponiveis": vagas_disponiveis,
                "tem_pendencia_instrutoria": tem_pendencia_instrutoria,
            }
        )

    return render(
        request,
        "turmas/listar_turmas.html",
        {"turmas_com_info": turmas_com_info},
    )


@login_required
def criar_turma(request):
    """Cria uma nova turma."""
    if request.method == "POST":
        form = TurmaForm(request.POST)
        if form.is_valid():
            turma = form.save(commit=False)
            
            # Processar horários se existirem
            horarios_json = request.POST.get('horarios_json')
            if horarios_json:
                import json
                try:
                    turma.horarios = json.loads(horarios_json)
                except json.JSONDecodeError:
                    turma.horarios = []
            
            turma.save()
            messages.success(request, "Turma criada com sucesso!")
            return redirect("turmas:detalhar_turma", id=turma.id)
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = TurmaForm()

    # Obter todos os alunos ativos para o formulário
    Aluno = get_model("alunos", "Aluno")
    alunos = Aluno.objects.filter(situacao="ATIVO")

    context = {
        'form': form,
        'alunos': alunos,
        'debug_mode': getattr(settings, 'DEBUG_INSTRUTORES', False)
    }

    return render(request, "turmas/criar_turma.html", context)
@login_required
def detalhar_turma(request, id):
    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=id)
    # Verificar pendências na instrutoria
    tem_pendencia_instrutoria = (
        not turma.instrutor
        or not turma.instrutor_auxiliar
        or not turma.auxiliar_instrucao
    )
    # Calcular informações de matrículas
    alunos_matriculados_count = (
        turma.matriculas.filter(status="A").count()
        if hasattr(turma, "matriculas")
        else 0
    )
    vagas_disponiveis = turma.vagas - alunos_matriculados_count
    # Obter matrículas ativas
    matriculas = (
        turma.matriculas.filter(status="A")
        if hasattr(turma, "matriculas")
        else []
    )
    context = {
        "turma": turma,
        "matriculas": matriculas,
        "alunos_matriculados_count": alunos_matriculados_count,
        "vagas_disponiveis": vagas_disponiveis,
        "tem_pendencia_instrutoria": tem_pendencia_instrutoria,
    }
    return render(request, "turmas/detalhar_turma.html", context)


@login_required
def editar_turma(request, id):
    """Edita uma turma existente."""
    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=id)
    if request.method == "POST":
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, "Turma atualizada com sucesso!")
            return redirect("turmas:detalhar_turma", id=turma.id)
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = TurmaForm(instance=turma)
    # Obter todos os alunos ativos para o formulário
    Aluno = get_model("alunos", "Aluno")
    alunos = Aluno.objects.filter(situacao="ATIVO")
    return render(
        request,
        "turmas/editar_turma.html",
        {
            "form": form,
            "turma": turma,
            "alunos": alunos,  # Passar todos os alunos ativos para o template
        },
    )


@login_required
def excluir_turma(request, id):
    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=id)
    if request.method == "POST":
        turma.delete()
        messages.success(request, "Turma excluída com sucesso!")
        return redirect("turmas:listar_turmas")
    return render(request, "turmas/excluir_turma.html", {"turma": turma})


@login_required
def listar_alunos_matriculados(request, id):
    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=id)
    alunos = turma.alunos.all() if hasattr(turma, "alunos") else []
    return render(
        request,
        "turmas/listar_alunos_matriculados.html",
        {"turma": turma, "alunos": alunos},
    )


@login_required
def matricular_aluno(request, id):
    """Matricula um aluno em uma turma específica."""
    Turma = get_turma_model()
    Aluno = get_aluno_model()
    turma = get_object_or_404(Turma, id=id)
    if request.method == "POST":
        aluno_cpf = request.POST.get("aluno")
        aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
        # Verificar se existe um modelo de Matricula
        try:
            Matricula = import_module("matriculas.models").Matricula
            # Criar uma matrícula em vez de adicionar diretamente à relação many-to-many
            Matricula.objects.create(
                aluno=aluno,
                turma=turma,
                data_matricula=timezone.now().date(),
                status="A",  # Ativa
            )
        except (ImportError, AttributeError):
            # Fallback: adicionar diretamente à relação many-to-many se o modelo Matricula não existir
            if hasattr(turma, "alunos"):
                turma.alunos.add(aluno)
        messages.success(
            request, f"Aluno {aluno.nome} matriculado com sucesso!"
        )
        return redirect("turmas:detalhar_turma", id=turma.id)
    # Obter alunos disponíveis para matrícula
    try:
        # Se existir um modelo de Matricula, excluir alunos já matriculados
        Matricula = import_module("matriculas.models").Matricula
        alunos_matriculados = Matricula.objects.filter(
            turma=turma, status="A"
        ).values_list("aluno__cpf", flat=True)
        alunos_disponiveis = Aluno.objects.exclude(cpf__in=alunos_matriculados)
    except (ImportError, AttributeError):
        # Fallback
        if hasattr(turma, "alunos"):
            alunos_disponiveis = Aluno.objects.exclude(turmas=turma)
        else:
            alunos_disponiveis = Aluno.objects.all()
    # Adicionar informação de vagas disponíveis
    vagas_disponiveis = (
        turma.vagas_disponiveis
        if hasattr(turma, "vagas_disponiveis")
        else turma.vagas
    )
    return render(
        request,
        "turmas/matricular_aluno.html",
        {
            "turma": turma,
            "alunos": alunos_disponiveis,
            "vagas_disponiveis": vagas_disponiveis,
        },
    )


@login_required
def cancelar_matricula(request, turma_id, aluno_cpf):
    """Cancela a matrícula de um aluno em uma turma."""
    Turma = get_turma_model()
    Aluno = get_aluno_model()
    turma = get_object_or_404(Turma, id=turma_id)
    aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
    # Verificar se o aluno está matriculado na turma
    try:
        # Importar o modelo Matricula dinamicamente
        from importlib import import_module

        matriculas_module = import_module("matriculas.models")
        Matricula = getattr(matriculas_module, "Matricula")
        matricula = Matricula.objects.get(aluno=aluno, turma=turma)
        if request.method == "POST":
            # Cancelar a matrícula
            matricula.status = "C"  # Cancelada
            matricula.save()
            messages.success(
                request,
                f"Matrícula do aluno {aluno.nome} na turma {turma.nome} cancelada com sucesso.",
            )
            return redirect("turmas:detalhar_turma", id=turma.id)
        # Se for GET, mostrar página de confirmação
        return render(
            request,
            "turmas/cancelar_matricula.html",
            {"turma": turma, "aluno": aluno},
        )
    except (ImportError, AttributeError) as e:
        messages.error(
            request, f"Erro ao acessar o modelo de matrículas: {str(e)}"
        )
        return redirect("turmas:detalhar_turma", id=turma.id)
    except Matricula.DoesNotExist:
        messages.error(
            request,
            f"O aluno {aluno.nome} não está matriculado na turma {turma.nome}.",
        )
        return redirect("turmas:detalhar_turma", id=turma.id)
