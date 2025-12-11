"""
Views para o módulo de Turmas.

Padrão de Nomenclatura:
- Parâmetros de ID em URLs: Usamos o formato 'modelo_id' (ex: turma_id, aluno_id)
  para maior clareza e para evitar ambiguidades em views que manipulam múltiplos modelos.
- Nos templates, continuamos passando o atributo 'id' do objeto (ex: turma.id),
  mas nas views e URLs usamos nomes mais descritivos.
"""

from django.db import DatabaseError, IntegrityError
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from importlib import import_module

# Importar a função utilitária centralizada
from core.utils import get_model_dynamically


def get_model(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)


def get_aluno_model():
    return get_model_dynamically("alunos", "Aluno")


def get_turma_model():
    return get_model_dynamically("turmas", "Turma")


def get_curso_model():
    """Obtém o modelo Curso dinamicamente."""
    return get_model_dynamically("cursos", "Curso")


def get_matricula_model():
    """Obtém o modelo Matricula dinamicamente."""
    return get_model_dynamically("matriculas", "Matricula")


def get_atividade_model():
    """Obtém o modelo Atividade dinamicamente."""
    return get_model_dynamically("atividades", "Atividade")


def get_frequencia_model():
    """Obtém o modelo Frequencia dinamicamente."""
    return get_model_dynamically("frequencias", "Frequencia")


def get_turma_form():
    """Obtém o formulário TurmaForm dinamicamente."""
    try:
        forms_module = import_module("turmas.forms")
        return getattr(forms_module, "TurmaForm")
    except (ImportError, AttributeError) as import_error:
        print(f"Erro ao importar TurmaForm: {import_error}")
        # Fallback para o formulário da core, se existir
        try:
            core_forms = import_module("core.forms")
            return getattr(core_forms, "TurmaForm")
        except (ImportError, AttributeError) as core_import_error:
            print(f"Erro ao importar TurmaForm da core: {core_import_error}")
            return None


@login_required
def listar_turmas(request):
    """Lista todas as turmas cadastradas."""
    try:
        Turma = get_model_dynamically("turmas", "Turma")
        Curso = get_model_dynamically("cursos", "Curso")

        # Obter parâmetros de busca e filtro
        query = request.GET.get("q", "")
        curso_id = request.GET.get("curso", "")
        status = request.GET.get("status", "")

        # Filtrar turmas (sem select_related)
        turmas = Turma.objects.all()

        print("DEBUG - Turmas antes dos filtros:", Turma.objects.all().count())
        print("DEBUG - Query params:", request.GET)

        if query:
            turmas = turmas.filter(
                Q(nome__icontains=query)
                | Q(curso__nome__icontains=query)
                | Q(instrutor__nome__icontains=query)
            )

        if curso_id:
            turmas = turmas.filter(curso_id=curso_id)

        if status:
            turmas = turmas.filter(status=status)

        print("DEBUG - Turmas após filtros:", turmas.count())

        # Ordenar turmas por status, nome do curso e nome da turma
        turmas = turmas.order_by("status", "curso__nome", "nome")

        # Forçar avaliação do queryset para evitar problemas de lazy evaluation
        turmas_list = list(turmas)
        print("DEBUG - Lista de turmas (forçada):", [t.id for t in turmas_list])

        # Paginação
        paginator = Paginator(turmas_list, 10)  # 10 turmas por página
        page_number = request.GET.get("page")
        try:
            page_obj = paginator.get_page(page_number)
        except (ValueError, TypeError) as e:
            # Tratar erros específicos de paginação (página inválida, tipo incorreto)
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                "Erro na paginação de turmas - página solicitada: %s, erro: %s",
                page_number,
                e,
            )
            page_obj = paginator.get_page(1)

        # Debug detalhado do conteúdo da página
        ids_na_pagina = list(getattr(page_obj, "object_list", []))
        print("DEBUG - IDs das turmas na página:", [t.id for t in ids_na_pagina])
        print(
            "DEBUG - page_obj length:",
            len(ids_na_pagina),
            "| total_turmas:",
            len(turmas_list),
        )
        print("DEBUG - object_list:", ids_na_pagina)

        # Obter cursos para o filtro
        cursos = Curso.objects.all().order_by("nome")

        context = {
            "turmas": page_obj,  # O template deve iterar sobre page_obj.object_list
            "page_obj": page_obj,
            "query": query,
            "cursos": cursos,
            "curso_selecionado": curso_id,
            "status_selecionado": status,
            "total_turmas": len(turmas_list),
        }

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            tabela_html = render_to_string(
                "turmas/partials/tabela_turmas.html", context, request=request
            )
            paginacao_html = render_to_string(
                "turmas/partials/paginacao_turmas.html", context, request=request
            )
            rodape_html = render_to_string(
                "turmas/partials/rodape_turmas.html", context, request=request
            )
            return JsonResponse(
                {
                    "tabela_html": tabela_html,
                    "paginacao_html": paginacao_html,
                    "rodape_html": rodape_html,
                }
            )

        return render(request, "turmas/listar_turmas.html", context)
    except (ImportError, AttributeError) as e:
        # Tratar erros específicos de importação de modelos
        import logging

        logger = logging.getLogger(__name__)
        logger.error(
            "Erro ao importar modelos necessários na listagem de turmas: %s", e
        )
        messages.error(request, "Erro interno no sistema. Contate o administrador.")
        return render(
            request,
            "turmas/listar_turmas.html",
            {
                "turmas": [],
                "page_obj": None,
                "query": "",
                "cursos": [],
                "curso_selecionado": "",
                "error_message": "Erro ao carregar dados. Tente novamente mais tarde.",
            },
        )
    except DatabaseError as db_error:
        # Tratamento para erros não previstos - log detalhado mas mensagem genérica para usuário
        import logging

        logger = logging.getLogger(__name__)
        logger.error(
            "Erro inesperado na listagem de turmas: %s: %s",
            type(db_error).__name__,
            db_error,
            exc_info=True,
        )
        messages.error(request, "Erro interno no sistema. Contate o administrador.")
        return render(
            request,
            "turmas/listar_turmas.html",
            {
                "turmas": [],
                "page_obj": None,
                "query": "",
                "cursos": [],
                "curso_selecionado": "",
                "error_message": "Erro interno. Tente novamente mais tarde.",
            },
        )


@login_required
def criar_turma(request):
    """Cria uma nova turma."""
    # Obter o formulário dinamicamente
    TurmaForm = get_turma_form()

    # Verificar se o formulário foi encontrado
    if TurmaForm is None:
        messages.error(
            request, "Erro ao carregar o formulário de turma. Contate o administrador."
        )
        return redirect("turmas:listar_turmas")

    if request.method == "POST":
        form = TurmaForm(request.POST)
        if form.is_valid():
            turma = form.save()
            messages.success(request, "Turma criada com sucesso!")
            return redirect("turmas:detalhar_turma", turma_id=turma.id)
    else:
        form = TurmaForm()

    # Obter todos os alunos ativos para o contexto
    try:
        Aluno = get_aluno_model()
        alunos = Aluno.objects.filter(situacao="ATIVO")
    except (ImportError, AttributeError):
        alunos = []

    # Certifique-se de que os cursos estão sendo carregados
    try:
        Curso = get_curso_model()
        cursos = Curso.objects.all().order_by("nome")
    except (ImportError, AttributeError):
        cursos = []

    return render(
        request,
        "turmas/criar_turma.html",
        {
            "form": form,
            "alunos": alunos,
            "cursos": cursos,
        },
    )


@login_required
def detalhar_turma(request, turma_id):
    """Exibe os detalhes de uma turma."""
    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=turma_id)
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
        turma.matriculas.filter(status="A") if hasattr(turma, "matriculas") else []
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
def editar_turma(request, turma_id):
    """Edita uma turma existente."""
    # Obter o formulário dinamicamente
    TurmaForm = get_turma_form()

    # Verificar se o formulário foi encontrado
    if TurmaForm is None:
        messages.error(
            request, "Erro ao carregar o formulário de turma. Contate o administrador."
        )
        return redirect("turmas:listar_turmas")

    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=turma_id)
    if request.method == "POST":
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, "Turma atualizada com sucesso!")
            return redirect("turmas:detalhar_turma", turma_id=turma.id)
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = TurmaForm(instance=turma)
    # Obter todos os alunos ativos para o formulário
    try:
        Aluno = get_aluno_model()
        alunos = Aluno.objects.filter(situacao="ATIVO")
    except (ImportError, AttributeError):
        alunos = []
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
def excluir_turma(request, turma_id):
    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=turma_id)

    # Obter modelos dinamicamente para evitar importações circulares
    matriculas_module = import_module("matriculas.models")
    Matricula = getattr(matriculas_module, "Matricula")

    atividades_module = import_module("atividades.models")
    Atividade = getattr(atividades_module, "Atividade")

    presencas_module = import_module("presencas.models")
    Presenca = getattr(presencas_module, "Presenca")

    notas_module = import_module("notas.models")
    Nota = getattr(notas_module, "Nota")

    pagamentos_module = import_module("pagamentos.models")
    Pagamento = getattr(pagamentos_module, "Pagamento")

    matriculas = list(Matricula.objects.filter(turma=turma))
    atividades = list(Atividade.objects.filter(turmas=turma))
    presencas = list(Presenca.objects.filter(turma=turma))
    notas = list(Nota.objects.filter(turma=turma))
    pagamentos = list(Pagamento.objects.filter(turma=turma))
    dependencias = {
        "matriculas": matriculas,
        "atividades": atividades,
        "presencas": presencas,
        "notas": notas,
        "pagamentos": pagamentos,
    }
    if request.method == "POST":
        if any(len(lst) > 0 for lst in dependencias.values()):
            messages.error(
                request,
                (
                    "Não é possível excluir a turma pois existem registros vinculados "
                    "(matrículas, atividades, presenças, notas, pagamentos, etc.). "
                    "Remova as dependências antes de tentar novamente."
                ),
                extra_tags="safe",
            )
            return redirect("turmas:excluir_turma", id=turma.id)
        try:
            turma.delete()
            messages.success(request, "Turma excluída com sucesso!")
            return redirect("turmas:listar_turmas")
        except (ProtectedError, IntegrityError, DatabaseError) as exc:
            messages.error(request, f"Erro ao excluir turma: {exc}")
            return redirect("turmas:detalhar_turma", id=turma.id)
    return render(
        request,
        "turmas/excluir_turma.html",
        {"turma": turma, "dependencias": dependencias},
    )


@login_required
def listar_alunos_turma(request, turma_id):
    """Lista todos os alunos matriculados em uma turma específica."""
    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=turma_id)

    # Obter alunos matriculados na turma
    try:
        Matricula = get_matricula_model()
        matriculas = Matricula.objects.filter(turma=turma, status="A").select_related(
            "aluno"
        )
        alunos = [matricula.aluno for matricula in matriculas]
    except (ImportError, AttributeError):
        # Fallback caso o modelo Matricula não esteja disponível
        alunos = []

    return render(
        request,
        "turmas/listar_alunos_turma.html",
        {
            "turma": turma,
            "alunos": alunos,
        },
    )


@login_required
def matricular_aluno(request, turma_id):
    """Matricula um aluno na turma."""
    Turma = get_model("turmas", "Turma")
    Aluno = get_model("alunos", "Aluno")
    Matricula = get_model("matriculas", "Matricula")

    turma = get_object_or_404(Turma, id=turma_id)

    if request.method == "POST":
        aluno_cpf = request.POST.get("aluno")
        if not aluno_cpf:
            messages.error(request, "Selecione um aluno para matricular.")
            return redirect("turmas:matricular_aluno", turma_id=turma_id)

        aluno = get_object_or_404(Aluno, cpf=aluno_cpf)

        # Verificar se já existe matrícula
        if Matricula.objects.filter(aluno=aluno, turma=turma).exists():
            messages.warning(
                request, f"O aluno {aluno.nome} já está matriculado nesta turma."
            )
            return redirect("turmas:detalhar_turma", turma_id=turma_id)

        # Verificar se há vagas disponíveis
        if turma.vagas_disponiveis <= 0:
            messages.error(request, "Não há vagas disponíveis nesta turma.")
            return redirect("turmas:detalhar_turma", turma_id=turma_id)

        try:
            matricula = Matricula(
                aluno=aluno,
                turma=turma,
                data_matricula=timezone.now().date(),
                ativa=True,
                status="A",  # Ativa
            )
            matricula.save()
            messages.success(
                request,
                f"Aluno {aluno.nome} matriculado com sucesso na turma {turma.nome}.",
            )
        except (IntegrityError, DatabaseError) as exc:
            messages.error(request, f"Erro ao matricular aluno: {exc}")

        return redirect("turmas:detalhar_turma", turma_id=turma_id)

    # Para requisições GET, exibir formulário de matrícula
    alunos = Aluno.objects.filter(situacao="ATIVO")
    return render(
        request, "turmas/matricular_aluno.html", {"turma": turma, "alunos": alunos}
    )


@login_required
def remover_aluno_turma(request, turma_id, aluno_id):
    """Remove um aluno de uma turma."""
    Turma = get_turma_model()
    Aluno = get_aluno_model()

    turma = get_object_or_404(Turma, id=turma_id)
    aluno = get_object_or_404(Aluno, cpf=aluno_id)

    try:
        Matricula = get_matricula_model()
        # Verificar se o aluno está matriculado na turma
        matricula = get_object_or_404(Matricula, aluno=aluno, turma=turma, status="A")

        if request.method == "POST":
            # Cancelar a matrícula
            matricula.status = "C"  # Cancelada
            matricula.save()

            messages.success(
                request,
                f"Aluno {aluno.nome} removido da turma {turma.nome} com sucesso.",
            )
            return redirect("turmas:detalhar_turma", turma_id=turma_id)

        return render(
            request,
            "turmas/confirmar_remocao_aluno.html",
            {"turma": turma, "aluno": aluno},
        )
    except (ImportError, AttributeError) as e:
        messages.error(request, f"Erro ao acessar o modelo de matrículas: {str(e)}")
        return redirect("turmas:detalhar_turma", turma_id=turma_id)


@login_required
def atualizar_instrutores(request, turma_id):
    """Atualiza os instrutores de uma turma."""
    Turma = get_turma_model()
    Aluno = get_aluno_model()

    turma = get_object_or_404(Turma, id=turma_id)

    if request.method == "POST":
        instrutor_cpf = request.POST.get("instrutor")
        instrutor_auxiliar_cpf = request.POST.get("instrutor_auxiliar")
        auxiliar_instrucao_cpf = request.POST.get("auxiliar_instrucao")

        # Atualizar instrutor principal
        if instrutor_cpf:
            instrutor = get_object_or_404(Aluno, cpf=instrutor_cpf)
            turma.instrutor = instrutor

        # Atualizar instrutor auxiliar
        if instrutor_auxiliar_cpf:
            instrutor_auxiliar = get_object_or_404(Aluno, cpf=instrutor_auxiliar_cpf)
            turma.instrutor_auxiliar = instrutor_auxiliar

        # Atualizar auxiliar de instrução
        if auxiliar_instrucao_cpf:
            auxiliar_instrucao = get_object_or_404(Aluno, cpf=auxiliar_instrucao_cpf)
            turma.auxiliar_instrucao = auxiliar_instrucao

        turma.save()
        messages.success(request, "Instrutores atualizados com sucesso!")
        return redirect("turmas:detalhar_turma", turma_id=turma_id)

    # Obter alunos elegíveis para serem instrutores
    try:
        alunos_elegiveis = Aluno.objects.filter(situacao="ATIVO")
    except (ImportError, AttributeError):
        alunos_elegiveis = []

    return render(
        request,
        "turmas/atualizar_instrutores.html",
        {
            "turma": turma,
            "alunos_elegiveis": alunos_elegiveis,
        },
    )


@login_required
def remover_instrutor(request, turma_id, tipo):
    """Remove um instrutor de uma turma."""
    Turma = get_turma_model()

    turma = get_object_or_404(Turma, id=turma_id)

    if request.method == "POST":
        if tipo == "principal":
            instrutor_nome = turma.instrutor.nome if turma.instrutor else "Não definido"
            turma.instrutor = None
            messages.success(
                request, f"Instrutor principal {instrutor_nome} removido com sucesso."
            )
        elif tipo == "auxiliar":
            instrutor_nome = (
                turma.instrutor_auxiliar.nome
                if turma.instrutor_auxiliar
                else "Não definido"
            )
            turma.instrutor_auxiliar = None
            messages.success(
                request, f"Instrutor auxiliar {instrutor_nome} removido com sucesso."
            )
        elif tipo == "auxiliar_instrucao":
            instrutor_nome = (
                turma.auxiliar_instrucao.nome
                if turma.auxiliar_instrucao
                else "Não definido"
            )
            turma.auxiliar_instrucao = None
            messages.success(
                request, f"Auxiliar de instrução {instrutor_nome} removido com sucesso."
            )

        turma.save()
        return redirect("turmas:detalhar_turma", turma_id=turma_id)

    # Determinar qual instrutor será removido
    instrutor_a_remover = None
    titulo = ""
    if tipo == "principal" and turma.instrutor:
        instrutor_a_remover = turma.instrutor
        titulo = "Remover Instrutor Principal"
    elif tipo == "auxiliar" and turma.instrutor_auxiliar:
        instrutor_a_remover = turma.instrutor_auxiliar
        titulo = "Remover Instrutor Auxiliar"
    elif tipo == "auxiliar_instrucao" and turma.auxiliar_instrucao:
        instrutor_a_remover = turma.auxiliar_instrucao
        titulo = "Remover Auxiliar de Instrução"

    if not instrutor_a_remover:
        messages.warning(request, "Não há instrutor para remover.")
        return redirect("turmas:detalhar_turma", turma_id=turma_id)

    return render(
        request,
        "turmas/confirmar_remocao_instrutor.html",
        {
            "turma": turma,
            "instrutor": instrutor_a_remover,
            "tipo": tipo,
            "titulo": titulo,
        },
    )


@login_required
def listar_atividades_turma(request, turma_id):
    """Lista todas as atividades de uma turma."""
    Turma = get_turma_model()

    turma = get_object_or_404(Turma, id=turma_id)

    try:
        Atividade = get_atividade_model()
        atividades = Atividade.objects.filter(turmas=turma).order_by("-data_inicio")
    except (ImportError, AttributeError):
        atividades = []

    return render(
        request,
        "turmas/listar_atividades_turma.html",
        {
            "turma": turma,
            "atividades": atividades,
        },
    )


@login_required
def adicionar_atividade_turma(request, turma_id):
    """Adiciona uma atividade a uma turma."""
    Turma = get_turma_model()

    turma = get_object_or_404(Turma, id=turma_id)

    try:
        forms_module = import_module("atividades.forms")
        AtividadeForm = getattr(forms_module, "AtividadeForm")

        if request.method == "POST":
            form = AtividadeForm(request.POST)
            if form.is_valid():
                atividade = form.save(commit=False)
                atividade.turmas.add(turma)
                atividade.save()
                messages.success(request, "Atividade adicionada com sucesso!")
                return redirect("turmas:listar_atividades_turma", turma_id=turma_id)
        else:
            # Pré-selecionar a turma no formulário
            form = AtividadeForm(initial={"turmas": [turma]})

        return render(
            request,
            "turmas/adicionar_atividade_turma.html",
            {
                "turma": turma,
                "form": form,
            },
        )
    except (ImportError, AttributeError) as e:
        messages.error(request, f"Erro ao carregar o formulário de atividade: {str(e)}")
        return redirect("turmas:detalhar_turma", turma_id=turma_id)


@login_required
def registrar_frequencia_turma(request, turma_id):
    """Registra a frequência dos alunos em uma atividade da turma."""
    Turma = get_turma_model()

    turma = get_object_or_404(Turma, id=turma_id)

    try:
        # Obter matrículas ativas
        Matricula = get_matricula_model()
        matriculas = Matricula.objects.filter(turma=turma, status="A").select_related(
            "aluno"
        )
        alunos = [matricula.aluno for matricula in matriculas]

        # Obter atividades da turma
        Atividade = get_atividade_model()
        atividades = Atividade.objects.filter(turmas=turma).order_by("-data_inicio")

        if request.method == "POST":
            atividade_id = request.POST.get("atividade")
            if not atividade_id:
                messages.error(
                    request, "Selecione uma atividade para registrar a frequência."
                )
                return redirect("turmas:registrar_frequencia_turma", turma_id=turma_id)

            atividade = get_object_or_404(Atividade, id=atividade_id)
            presentes = request.POST.getlist("presentes")

            # Obter modelo de Frequencia
            Frequencia = get_frequencia_model()

            # Registrar frequência para cada aluno
            for aluno in alunos:
                presente = aluno.cpf in presentes
                justificativa = request.POST.get(f"justificativa_{aluno.cpf}", "")

                # Verificar se já existe registro para este aluno nesta atividade
                Frequencia.objects.update_or_create(
                    aluno=aluno,
                    atividade=atividade,
                    defaults={
                        "presente": presente,
                        "justificativa": justificativa if not presente else "",
                    },
                )

            messages.success(request, "Frequência registrada com sucesso!")
            return redirect("turmas:detalhar_turma", turma_id=turma_id)

        return render(
            request,
            "turmas/registrar_frequencia_turma.html",
            {
                "turma": turma,
                "alunos": alunos,
                "atividades": atividades,
            },
        )

    except (ImportError, AttributeError) as e:
        messages.error(request, f"Erro ao registrar frequência: {str(e)}")
        return redirect("turmas:detalhar_turma", turma_id=turma_id)


@login_required
def relatorio_frequencia_turma(request, turma_id):
    """Gera um relatório de frequência para uma turma específica."""
    Turma = get_turma_model()

    turma = get_object_or_404(Turma, id=turma_id)

    try:
        # Obter matrículas ativas
        Matricula = get_matricula_model()
        matriculas = Matricula.objects.filter(turma=turma, status="A").select_related(
            "aluno"
        )
        alunos = [matricula.aluno for matricula in matriculas]

        # Obter frequências
        Frequencia = get_frequencia_model()

        # Obter datas das atividades da turma
        Atividade = get_atividade_model()
        atividades = Atividade.objects.filter(turmas=turma).order_by("data_inicio")
        datas_atividades = [atividade.data_inicio.date() for atividade in atividades]

        # Preparar dados para o relatório
        dados_frequencia = []
        for aluno in alunos:
            frequencias_aluno = Frequencia.objects.filter(
                aluno=aluno, atividade__turma=turma
            )

            # Calcular estatísticas
            total_presencas = frequencias_aluno.filter(presente=True).count()
            total_atividades = atividades.count()

            if total_atividades > 0:
                percentual_presenca = (total_presencas / total_atividades) * 100
            else:
                percentual_presenca = 0

            dados_frequencia.append(
                {
                    "aluno": aluno,
                    "total_presencas": total_presencas,
                    "total_atividades": total_atividades,
                    "percentual_presenca": percentual_presenca,
                    "frequencias": frequencias_aluno,
                }
            )

        context = {
            "turma": turma,
            "alunos": alunos,
            "datas_atividades": datas_atividades,
            "dados_frequencia": dados_frequencia,
        }

        return render(request, "turmas/relatorio_frequencia_turma.html", context)

    except (ImportError, AttributeError) as e:
        messages.error(request, f"Erro ao gerar relatório de frequência: {str(e)}")
        return redirect("turmas:detalhar_turma", turma_id=turma_id)


@login_required
def exportar_turmas(request):
    """Exporta os dados das turmas para um arquivo CSV."""
    import csv
    try:

        Turma = get_turma_model()
        turmas = Turma.objects.all()
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="turmas.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                "ID",
                "Nome",
                "Curso",
                "Vagas",
                "Status",
                "Data Início",
                "Data Fim",
                "Instrutor",
                "Local",
                "Horário",
                "Número do Livro",
                "Percentual de Presença Mínima",
                "Data de Iniciação",
                "Data de Início das Atividades",
                "Data da Primeira Aula",
            ]
        )
        for turma in turmas:
            writer.writerow(
                [
                    turma.id,
                    turma.nome,
                    turma.curso.nome if turma.curso else "",
                    turma.vagas,
                    turma.get_status_display(),
                    turma.data_inicio,
                    turma.data_fim,
                    turma.instrutor.nome if turma.instrutor else "",
                    turma.local,
                    turma.horario,
                    turma.num_livro,
                    getattr(turma, "perc_presenca_minima", None),
                    turma.data_iniciacao,
                    turma.data_inicio_ativ,
                    turma.data_prim_aula,
                ]
            )
        return response
    except (csv.Error, OSError, DatabaseError) as exc:
        messages.error(request, f"Erro ao exportar turmas: {exc}")
        return redirect("turmas:listar_turmas")


@login_required
def importar_turmas(request):
    """Importa turmas de um arquivo CSV."""
    import csv
    from io import TextIOWrapper

    if request.method == "POST" and request.FILES.get("csv_file"):
        try:
            Turma = get_turma_model()
            Curso = get_curso_model()
            Aluno = get_aluno_model()

            csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")
            reader = csv.DictReader(csv_file)
            count = 0
            errors = []

            for row in reader:
                try:
                    # Buscar curso pelo nome ou código
                    curso = None
                    curso_nome = row.get("Curso", "").strip()
                    if curso_nome:
                        try:
                            curso = Curso.objects.get(nome=curso_nome)
                        except Curso.DoesNotExist:
                            try:
                                curso = Curso.objects.get(id=curso_nome)
                            except Curso.DoesNotExist:
                                errors.append(f"Curso não encontrado: {curso_nome}")
                                continue

                    # Buscar instrutor pelo nome ou CPF
                    instrutor = None
                    instrutor_nome = row.get("Instrutor", "").strip()
                    if instrutor_nome:
                        try:
                            instrutor = Aluno.objects.get(nome=instrutor_nome)
                        except Aluno.DoesNotExist:
                            try:
                                instrutor = Aluno.objects.get(cpf=instrutor_nome)
                            except Aluno.DoesNotExist:
                                errors.append(
                                    f"Instrutor não encontrado: {instrutor_nome}"
                                )
                                continue

                    # Processar datas
                    data_inicio = None
                    data_fim = None
                    data_iniciacao = None
                    data_inicio_ativ = None
                    data_prim_aula = None
                    try:
                        if row.get("Data Início"):
                            data_inicio = timezone.datetime.strptime(
                                row.get("Data Início"), "%d/%m/%Y"
                            ).date()
                        if row.get("Data Fim"):
                            data_fim = timezone.datetime.strptime(
                                row.get("Data Fim"), "%d/%m/%Y"
                            ).date()
                        if row.get("Data de Iniciação"):
                            data_iniciacao = timezone.datetime.strptime(
                                row.get("Data de Iniciação"), "%d/%m/%Y"
                            ).date()
                        if row.get("Data de Início das Atividades"):
                            data_inicio_ativ = timezone.datetime.strptime(
                                row.get("Data de Início das Atividades"), "%d/%m/%Y"
                            ).date()
                        if row.get("Data da Primeira Aula"):
                            data_prim_aula = timezone.datetime.strptime(
                                row.get("Data da Primeira Aula"), "%d/%m/%Y"
                            ).date()
                    except ValueError as e:
                        errors.append(f"Erro no formato de data: {str(e)}")
                        continue

                    # Validar obrigatoriedade dos campos iniciáticos
                    obrigatorios = [
                        ("Número do Livro", row.get("Número do Livro")),
                        (
                            "Percentual de Presença Mínima",
                            row.get("Percentual de Presença Mínima")
                            or row.get("Percentual de Carência"),
                        ),
                        ("Data de Iniciação", data_iniciacao),
                        ("Data de Início das Atividades", data_inicio_ativ),
                        ("Data da Primeira Aula", data_prim_aula),
                    ]
                    for label, valor in obrigatorios:
                        if not valor:
                            errors.append(f"Campo obrigatório não informado: {label}")
                            continue

                    # Criar a turma
                    perc_presenca = (
                        row.get("Percentual de Presença Mínima")
                        or row.get("Percentual de Carência")
                        or None
                    )

                    Turma.objects.create(
                        nome=row.get("Nome", "").strip(),
                        curso=curso,
                        vagas=int(row.get("Vagas", 0)),
                        status=row.get("Status", "A")[0].upper(),
                        data_inicio=data_inicio,
                        data_fim=data_fim,
                        instrutor=instrutor,
                        local=row.get("Local", "").strip(),
                        horario=row.get("Horário", "").strip(),
                        num_livro=row.get("Número do Livro"),
                        perc_presenca_minima=perc_presenca,
                        data_iniciacao=data_iniciacao,
                        data_inicio_ativ=data_inicio_ativ,
                        data_prim_aula=data_prim_aula,
                    )
                    count += 1
                except (ValueError, KeyError, IntegrityError, DatabaseError) as exc:
                    errors.append(f"Erro na linha {count + 1}: {exc}")

            if errors:
                messages.warning(
                    request,
                    f"{count} turmas importadas com {len(errors)} erros.",
                )
                for error in errors[:5]:  # Mostrar apenas os 5 primeiros erros
                    messages.error(request, error)
                if len(errors) > 5:
                    messages.error(request, f"... e mais {len(errors) - 5} erros.")
            else:
                messages.success(request, f"{count} turmas importadas com sucesso!")
            return redirect("turmas:listar_turmas")
        except (csv.Error, OSError, IntegrityError, DatabaseError, ValueError) as exc:
            messages.error(request, f"Erro ao importar turmas: {exc}")

    return render(request, "turmas/importar_turmas.html")


@login_required
def relatorio_turmas(request):
    """Gera um relatório com estatísticas sobre as turmas."""
    try:
        Turma = get_turma_model()

        # Estatísticas gerais
        total_turmas = Turma.objects.count()
        turmas_ativas = Turma.objects.filter(status="A").count()
        turmas_concluidas = Turma.objects.filter(status="C").count()
        turmas_canceladas = Turma.objects.filter(status="X").count()

        # Turmas por curso
        Curso = get_curso_model()
        cursos = Curso.objects.all()

        turmas_por_curso_stats = []
        for curso in cursos:
            count = Turma.objects.filter(curso=curso).count()
            if count > 0:
                turmas_por_curso_stats.append(
                    {
                        "curso": curso,
                        "count": count,
                        "percentage": (count / total_turmas * 100)
                        if total_turmas > 0
                        else 0,
                    }
                )

        # Turmas por instrutor
        Aluno = get_aluno_model()
        instrutores = Aluno.objects.filter(
            Q(turma_instrutor__isnull=False)
            | Q(turma_instrutor_auxiliar__isnull=False)
            | Q(turma_auxiliar_instrucao__isnull=False)
        ).distinct()

        turmas_por_instrutor = []
        for instrutor in instrutores:
            count_principal = Turma.objects.filter(instrutor=instrutor).count()
            count_auxiliar = Turma.objects.filter(instrutor_auxiliar=instrutor).count()
            count_aux_instrucao = Turma.objects.filter(
                auxiliar_instrucao=instrutor
            ).count()

            if count_principal > 0 or count_auxiliar > 0 or count_aux_instrucao > 0:
                turmas_por_instrutor.append(
                    {
                        "instrutor": instrutor,
                        "count_principal": count_principal,
                        "count_auxiliar": count_auxiliar,
                        "count_aux_instrucao": count_aux_instrucao,
                        "total": count_principal + count_auxiliar + count_aux_instrucao,
                    }
                )

        # Ordenar por total de turmas
        turmas_por_instrutor.sort(key=lambda x: x["total"], reverse=True)

        context = {
            "total_turmas": total_turmas,
            "turmas_ativas": turmas_ativas,
            "turmas_concluidas": turmas_concluidas,
            "turmas_canceladas": turmas_canceladas,
            "turmas_por_curso": turmas_por_curso_stats,
            "turmas_por_instrutor": turmas_por_instrutor,
        }

        return render(request, "turmas/relatorio_turmas.html", context)

    except DatabaseError as exc:
        messages.error(request, f"Erro ao gerar relatório de turmas: {exc}")
        return redirect("turmas:listar_turmas")


@login_required
def dashboard_turmas(request):
    """Exibe um dashboard com informações e estatísticas sobre as turmas."""
    try:
        Turma = get_turma_model()

        # Estatísticas gerais
        total_turmas = Turma.objects.count()
        turmas_ativas = Turma.objects.filter(status="A").count()
        turmas_concluidas = Turma.objects.filter(status="C").count()
        turmas_canceladas = Turma.objects.filter(status="X").count()

        # Turmas recentes
        turmas_recentes = Turma.objects.order_by("-data_inicio")[:5]

        # Turmas com mais alunos
        Matricula = get_matricula_model()

        turmas_com_contagem = []
        for turma in Turma.objects.filter(status="A"):
            count = Matricula.objects.filter(turma=turma, status="A").count()
            turmas_com_contagem.append(
                {
                    "turma": turma,
                    "alunos_count": count,
                    "vagas_disponiveis": turma.vagas - count
                    if turma.vagas > count
                    else 0,
                }
            )

        # Ordenar por número de alunos
        turmas_com_contagem.sort(key=lambda x: x["alunos_count"], reverse=True)
        turmas_populares = turmas_com_contagem[:5]

        # Turmas por curso (para gráfico)
        Curso = get_curso_model()
        cursos = Curso.objects.all()

        dados_grafico = {"labels": [], "data": []}

        for curso in cursos:
            count = Turma.objects.filter(curso=curso).count()
            if count > 0:
                dados_grafico["labels"].append(curso.nome)
                dados_grafico["data"].append(count)

        context = {
            "total_turmas": total_turmas,
            "turmas_ativas": turmas_ativas,
            "turmas_concluidas": turmas_concluidas,
            "turmas_canceladas": turmas_canceladas,
            "turmas_recentes": turmas_recentes,
            "turmas_populares": turmas_populares,
            "dados_grafico": dados_grafico,
        }

        return render(request, "turmas/dashboard_turmas.html", context)

    except DatabaseError as exc:
        messages.error(request, f"Erro ao carregar dashboard de turmas: {exc}")
        return redirect("turmas:listar_turmas")


def turmas_por_curso(request):
    Turma = get_model_dynamically("turmas", "Turma")
    codigo_curso = request.GET.get("curso")
    turmas = []
    if codigo_curso:
        turmas_qs = Turma.objects.filter(curso_id=codigo_curso)
        turmas = [{"id": t.id, "nome": t.nome} for t in turmas_qs]
    return JsonResponse({"turmas": turmas})
