from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django import forms


# Funções auxiliares para obter modelos dinamicamente
def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    try:
        from alunos.models import Aluno

        return Aluno
    except ImportError:
        from django.apps import apps

        return apps.get_model("alunos", "Aluno")


def get_matricula_model():
    """Obtém o modelo Matricula dinamicamente."""
    try:
        from matriculas.models import Matricula

        return Matricula
    except ImportError:
        from django.apps import apps

        return apps.get_model("matriculas", "Matricula")


def get_model_class(model_name):
    """Obtém uma classe de modelo dinamicamente."""
    try:
        # Tenta importar do app correto com base no nome do modelo
        if model_name == "Turma":
            from turmas.models import Turma

            return Turma
        elif model_name == "Aluno":
            from alunos.models import Aluno

            return Aluno
        elif model_name == "Matricula":
            from matriculas.models import Matricula  # Agora importa do app matriculas

            return Matricula
        elif model_name == "Curso":
            from cursos.models import Curso

            return Curso
        else:
            # Fallback usando apps.get_model
            from django.apps import apps

            app_label = (
                model_name.lower() + "s"
            )  # Convenção: modelo Aluno -> app alunos
            return apps.get_model(app_label, model_name)
    except (ImportError, LookupError):
        # Se falhar, tenta usar o sistema de apps do Django
        from django.apps import apps

        for app_config in apps.get_app_configs():
            try:
                model = app_config.get_model(model_name)
                return model
            except LookupError:
                continue
        raise ImportError(f"Não foi possível importar o modelo {model_name}")


@login_required
def listar_turmas(request):
    """Lista todas as turmas."""
    # Importações necessárias
    from django.db.models import Count

    # Obter o modelo Turma
    Turma = get_model_class("Turma")

    # Obter parâmetros de busca e filtro
    query = request.GET.get("q", "")
    curso_id = request.GET.get("curso", "")
    status = request.GET.get("status", "")

    # Consulta base
    turmas = Turma.objects.all().select_related("curso")

    # Anotar com contagem de alunos
    turmas = turmas.annotate(alunos_count=Count("matriculas"))

    # Aplicar filtros se fornecidos
    if query:
        turmas = turmas.filter(
            Q(nome__icontains=query) | Q(curso__nome__icontains=query)
        )

    if curso_id:
        turmas = turmas.filter(curso__codigo_curso=curso_id)

    if status:
        turmas = turmas.filter(status=status)

    # Obter cursos para o filtro
    Curso = get_model_class("Curso")
    cursos = Curso.objects.all()

    # Contexto para o template
    context = {
        "turmas": turmas,
        "cursos": cursos,
        "query": query,
        "curso_selecionado": curso_id,
        "status_selecionado": status,
    }

    return render(request, "turmas/listar_turmas.html", context)


@login_required
def matricular_aluno(request, turma_id):
    """Matricula um aluno em uma turma."""
    # Importações necessárias
    from django.db.models import Q
    from django.core.paginator import Paginator
    from matriculas.models import Matricula  # Importar diretamente do app matriculas

    # Obter os modelos necessários
    Turma = get_model_class("Turma")
    Aluno = get_model_class("Aluno")

    turma = get_object_or_404(Turma, id=turma_id)

    # Obter o parâmetro de busca
    query = request.GET.get("q", "")

    # Verificar se a turma está cheia
    if hasattr(turma, "capacidade") and turma.total_alunos >= turma.capacidade:
        messages.error(
            request,
            "Não é possível matricular mais alunos. A turma está com capacidade máxima.",
        )
        return redirect("turmas:detalhar_turma", id=turma.id)

    if request.method == "POST":
        aluno_cpf = request.POST.get("aluno")
        if not aluno_cpf:
            messages.error(request, "Selecione um aluno para matricular.")
            return redirect("turmas:matricular_aluno", turma_id=turma.id)

        aluno = get_object_or_404(Aluno, cpf=aluno_cpf)

        # Verificar se o aluno já está matriculado na turma
        if Matricula.objects.filter(turma=turma, aluno=aluno).exists():
            messages.warning(
                request, f"O aluno {aluno.nome} já está matriculado nesta turma."
            )
            return redirect("turmas:detalhar_turma", id=turma.id)

        # Criar a matrícula
        try:
            matricula = Matricula(
                turma=turma,
                aluno=aluno,
                data_matricula=timezone.now().date(),
                ativa=True,
                status="A",
            )
            matricula.full_clean()  # Validar o modelo antes de salvar
            matricula.save()
            messages.success(
                request,
                f"Aluno {aluno.nome} matriculado com sucesso na turma {turma.nome}.",
            )
            return redirect("turmas:detalhar_turma", id=turma.id)
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        except Exception as e:
            messages.error(request, f"Erro ao matricular aluno: {str(e)}")

    # Obter alunos que ainda não estão matriculados na turma
    alunos_matriculados = Matricula.objects.filter(turma=turma).values_list(
        "aluno__cpf", flat=True
    )
    alunos_disponiveis = Aluno.objects.exclude(cpf__in=alunos_matriculados)

    # Filtrar por termo de busca se fornecido
    if query:
        alunos_disponiveis = alunos_disponiveis.filter(
            Q(cpf__icontains=query)
            | Q(nome__icontains=query)
            | Q(numero_iniciatico__icontains=query)
        )

    # Paginação para lidar com muitos alunos
    paginator = Paginator(alunos_disponiveis, 10)  # 10 alunos por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Calcular vagas disponíveis
    vagas_disponiveis = (
        getattr(turma, "capacidade", 0) - turma.total_alunos
        if hasattr(turma, "total_alunos")
        else "Ilimitada"
    )

    return render(
        request,
        "turmas/matricular_aluno.html",
        {
            "turma": turma,
            "alunos": page_obj,
            "query": query,
            "vagas_disponiveis": vagas_disponiveis,
        },
    )


@login_required
def criar_turma(request):
    """Cria uma nova turma."""
    # Importações necessárias
    from django import forms

    # Obter os modelos e formulários necessários
    Turma = get_model_class("Turma")

    # Definir o formulário para a turma
    class TurmaForm(forms.ModelForm):
        class Meta:
            model = Turma
            fields = [
                "nome",
                "curso",
                "data_inicio",
                "data_fim",
                "capacidade",
                "status",
            ]
            widgets = {
                "nome": forms.TextInput(attrs={"class": "form-control"}),
                "curso": forms.Select(attrs={"class": "form-control"}),
                "data_inicio": forms.DateInput(
                    attrs={"class": "form-control", "type": "date"},
                    format="%Y-%m-%d",  # Formato ISO
                ),
                "data_fim": forms.DateInput(
                    attrs={"class": "form-control", "type": "date"},
                    format="%Y-%m-%d",  # Formato ISO
                ),
                "capacidade": forms.NumberInput(
                    attrs={"class": "form-control", "min": "1"}
                ),
                "status": forms.Select(attrs={"class": "form-control"}),
            }

    if request.method == "POST":
        form = TurmaForm(request.POST)
        if form.is_valid():
            try:
                turma = form.save()
                messages.success(request, "Turma criada com sucesso!")
                return redirect("turmas:detalhar_turma", id=turma.id)
            except Exception as e:
                messages.error(request, f"Erro ao criar turma: {str(e)}")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = TurmaForm()

    return render(request, "turmas/criar_turma.html", {"form": form})


@login_required
def detalhar_turma(request, id):
    """Exibe os detalhes de uma turma."""
    Turma = get_model_class("Turma")
    turma = get_object_or_404(Turma, id=id)
    # Get matriculas for this turma
    from matriculas.models import Matricula

    matriculas = Matricula.objects.filter(turma=turma).select_related("aluno")

    # Extract the actual student objects from matriculas
    alunos = [matricula.aluno for matricula in matriculas]

    # Calculate these values explicitly
    alunos_matriculados_count = len(alunos)
    vagas_disponiveis = (
        turma.capacidade - alunos_matriculados_count
        if hasattr(turma, "capacidade")
        else "Ilimitada"
    )

    return render(
        request,
        "turmas/detalhar_turma.html",
        {
            "turma": turma,
            "matriculas": matriculas,
            "alunos_matriculados": alunos,  # List of student objects
            "alunos_matriculados_count": alunos_matriculados_count,  # Integer count
            "vagas_disponiveis": vagas_disponiveis,
        },
    )


@login_required
def editar_turma(request, id):
    """Edita uma turma existente."""
    # Obter os modelos necessários
    Turma = get_model_class("Turma")

    turma = get_object_or_404(Turma, id=id)

    # Definir o formulário para a turma
    class TurmaForm(forms.ModelForm):
        class Meta:
            model = Turma
            fields = [
                "nome",
                "curso",
                "data_inicio",
                "data_fim",
                "capacidade",
                "status",
            ]
            widgets = {
                "nome": forms.TextInput(attrs={"class": "form-control"}),
                "curso": forms.Select(attrs={"class": "form-control"}),
                "data_inicio": forms.DateInput(
                    attrs={"class": "form-control", "type": "date"}
                ),
                "data_fim": forms.DateInput(
                    attrs={"class": "form-control", "type": "date"}
                ),
                "capacidade": forms.NumberInput(
                    attrs={"class": "form-control", "min": "1"}
                ),
                "status": forms.Select(attrs={"class": "form-control"}),
            }

    if request.method == "POST":
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Turma atualizada com sucesso!")
                return redirect("turmas:detalhar_turma", id=turma.id)
            except Exception as e:
                messages.error(request, f"Erro ao atualizar turma: {str(e)}")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        # Formatar as datas para o formato ISO antes de passar para o formulário
        turma_data = {
            "nome": turma.nome,
            "curso": turma.curso,
            "capacidade": turma.capacidade,
            "status": turma.status,
        }

        # Adicionar as datas formatadas
        if turma.data_inicio:
            turma_data["data_inicio"] = turma.data_inicio.strftime("%Y-%m-%d")
        if turma.data_fim:
            turma_data["data_fim"] = turma.data_fim.strftime("%Y-%m-%d")

        form = TurmaForm(initial=turma_data, instance=turma)

    return render(request, "turmas/editar_turma.html", {"form": form, "turma": turma})


@login_required
def excluir_turma(request, id):
    """Exclui uma turma."""
    # Obter os modelos necessários
    Turma = get_model_class("Turma")

    turma = get_object_or_404(Turma, id=id)

    if request.method == "POST":
        try:
            turma.delete()
            messages.success(request, "Turma excluída com sucesso!")
            return redirect("turmas:listar_turmas")
        except Exception as e:
            messages.error(request, f"Erro ao excluir turma: {str(e)}")
            return redirect("turmas:detalhar_turma", id=turma.id)

    return render(request, "turmas/excluir_turma.html", {"turma": turma})


@login_required
def listar_alunos_matriculados(request, turma_id):
    """Lista os alunos matriculados em uma turma."""
    Turma = get_model_class("Turma")
    from matriculas.models import Matricula  # Import from the correct app

    turma = get_object_or_404(Turma, id=turma_id)

    # Get matriculas for this turma
    matriculas = Matricula.objects.filter(turma=turma).select_related("aluno")

    # Extract alunos from matriculas to ensure we have the CPF
    alunos = [matricula.aluno for matricula in matriculas]

    return render(
        request,
        "turmas/listar_alunos_matriculados.html",
        {
            "turma": turma,
            "alunos": alunos,
            "matriculas": matriculas,  # Pass both for flexibility
        },
    )


@login_required
def cancelar_matricula(request, turma_id, aluno_cpf):
    """Cancela a matrícula de um aluno em uma turma."""
    # Obter os modelos necessários
    from matriculas.models import Matricula  # Importar diretamente do app matriculas

    Turma = get_model_class("Turma")
    Aluno = get_model_class("Aluno")

    turma = get_object_or_404(Turma, id=turma_id)
    aluno = get_object_or_404(Aluno, cpf=aluno_cpf)

    try:
        matricula = Matricula.objects.get(turma=turma, aluno=aluno)
        matricula.delete()
        messages.success(
            request, f"Matrícula do aluno {aluno.nome} cancelada com sucesso."
        )
    except Matricula.DoesNotExist:
        messages.error(
            request, f"O aluno {aluno.nome} não está matriculado nesta turma."
        )
    except Exception as e:
        messages.error(request, f"Erro ao cancelar matrícula: {str(e)}")

    return redirect("turmas:detalhar_turma", id=turma.id)
