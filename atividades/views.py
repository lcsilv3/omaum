import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
import importlib

# Importar a função utilitária centralizada
from core.utils import get_model_dynamically, get_form_dynamically

# Set up logger
logger = logging.getLogger(__name__)

print(
    "ARQUIVO VIEWS.PY CARREGADO:",
    importlib.import_module("django.conf").settings.BASE_DIR,
)


def get_return_url(request, default_url):
    """Obtém a URL de retorno do request ou usa o valor padrão."""
    return_url = request.GET.get("return_url", "")
    # Verificação básica de segurança
    if not return_url or not return_url.startswith("/"):
        return default_url
    return return_url


def get_form_class(form_name):
    """Importa dinamicamente uma classe de formulário para evitar importações circulares."""
    return get_form_dynamically("atividades", form_name)


def get_model_class(model_name, module_name="atividades"):
    """Importa dinamicamente uma classe de modelo para evitar importações circulares."""
    return get_model_dynamically(module_name, model_name)


@login_required
def listar_atividades(request):
    """Página inicial do módulo de atividades."""
    return render(request, "atividades/listar_atividades.html")


@login_required
def listar_atividades_academicas(request):
    """Lista todas as atividades acadêmicas."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    
    # Adicionar suporte para busca e filtros
    query = request.GET.get('q', '')
    turma_id = request.GET.get('turma', '')
    
    atividades = AtividadeAcademica.objects.all().order_by('-data_inicio')
    
    # Aplicar filtros se fornecidos
    if query:
        atividades = atividades.filter(
            nome__icontains=query
        )
    
    if turma_id:
        atividades = atividades.filter(turmas__id=turma_id)
    
    # Paginação
    paginator = Paginator(atividades, 10)  # 10 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Armazenar a URL atual na sessão para uso posterior
    request.session["last_academicas_list_url"] = request.get_full_path()

    # Obter lista de turmas para o filtro
    Turma = get_model_class("Turma", "turmas")
    turmas = Turma.objects.filter(status="A")

    return render(
        request,
        "atividades/listar_atividades_academicas.html",
        {
            "atividades": page_obj,
            "page_obj": page_obj,
            "query": query,
            "turma_selecionada": turma_id,
            "turmas": turmas,
            "return_url": request.path,  # Armazena URL atual para retorno
        },
    )


@login_required
def listar_atividades_ritualisticas(request):
    """Lista todas as atividades ritualísticas."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    
    # Adicionar suporte para busca e filtros
    query = request.GET.get('q', '')
    turma_id = request.GET.get('turma', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    atividades = AtividadeRitualistica.objects.all().order_by('-data')
    
    # Aplicar filtros se fornecidos
    if query:
        atividades = atividades.filter(
            nome__icontains=query
        )
    
    if turma_id:
        atividades = atividades.filter(turma_id=turma_id)
        
    if data_inicio:
        atividades = atividades.filter(data__gte=data_inicio)
        
    if data_fim:
        atividades = atividades.filter(data__lte=data_fim)
    
    # Paginação
    paginator = Paginator(atividades, 10)  # 10 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Armazenar a URL atual na sessão para uso posterior
    request.session["last_ritualisticas_list_url"] = request.get_full_path()

    # Salvar URL referenciadora, exceto se vier do próprio formulário de atividade ritualística
    referer = request.META.get("HTTP_REFERER", "")
    if referer and not any(
        x in referer
        for x in [
            "criar_atividade_ritualistica",
            "editar_atividade_ritualistica",
        ]
    ):
        request.session["atividade_ritualistica_referer"] = referer

    # Usar a URL referenciadora armazenada ou a página inicial como fallback
    previous_url = request.session.get("atividade_ritualistica_referer", "/")
    
    # Obter lista de turmas para o filtro
    Turma = get_model_class("Turma", "turmas")
    turmas = Turma.objects.filter(status="A")

    return render(
        request,
        "atividades/listar_atividades_ritualisticas.html",
        {
            "atividades": page_obj,
            "page_obj": page_obj,
            "query": query,
            "turma_selecionada": turma_id,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "turmas": turmas,
            "previous_url": previous_url,
        },
    )


@login_required
def criar_atividade_academica(request):
    """Função para criar uma nova atividade acadêmica."""
    AtividadeAcademicaForm = get_form_class("AtividadeAcademicaForm")
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )

    if request.method == "POST":
        form = AtividadeAcademicaForm(request.POST)
        if form.is_valid():
            try:
                atividade = form.save(commit=False)
                
                # Verificar se é para todas as turmas
                todas_turmas = form.cleaned_data.get('todas_turmas', False)
                
                # Salvar a atividade primeiro
                atividade.save()
                
                if todas_turmas:
                    # Obter todas as turmas ativas
                    Turma = get_model_class("Turma", "turmas")
                    turmas_ativas = Turma.objects.filter(status="A")
                    
                    # Adicionar todas as turmas ativas
                    atividade.turmas.set(turmas_ativas)
                    
                    # Log para depuração
                    logger.info(f"Atividade {atividade.id} associada a {turmas_ativas.count()} turmas ativas")
                else:
                    # Usar as turmas selecionadas no formulário
                    form.save_m2m()  # Salvar relações ManyToMany
                    
                    # Log para depuração
                    logger.info(f"Atividade {atividade.id} associada a {atividade.turmas.count()} turmas selecionadas")
                
                messages.success(
                    request, "Atividade acadêmica criada com sucesso."
                )
                return redirect(return_url)
            except Exception as e:
                logger.error(f"Erro ao criar atividade acadêmica: {str(e)}", exc_info=True)
                messages.error(request, f"Erro ao criar atividade acadêmica: {str(e)}")
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = AtividadeAcademicaForm()

    return render(
        request,
        "atividades/formulario_atividade_academica.html",
        {"form": form, "return_url": return_url},
    )


@login_required
def editar_atividade_academica(request, pk):
    """Função para editar uma atividade acadêmica existente."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    AtividadeAcademicaForm = get_form_class("AtividadeAcademicaForm")
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )

    if request.method == "POST":
        try:
            form = AtividadeAcademicaForm(request.POST, instance=atividade)
            if form.is_valid():
                atividade = form.save(commit=False)
                
                # Verificar se é para todas as turmas
                todas_turmas = form.cleaned_data.get('todas_turmas', False)
                
                # Salvar a atividade primeiro
                atividade.save()
                
                if todas_turmas:
                    # Obter todas as turmas ativas
                    Turma = get_model_class("Turma", "turmas")
                    turmas_ativas = Turma.objects.filter(status="A")
                    
                    # Adicionar todas as turmas ativas
                    atividade.turmas.set(turmas_ativas)
                    
                    # Log para depuração
                    logger.info(f"Atividade {atividade.id} atualizada com {turmas_ativas.count()} turmas ativas")
                else:
                    # Usar as turmas selecionadas no formulário
                    form.save_m2m()  # Salvar relações ManyToMany
                    
                    # Log para depuração
                    logger.info(f"Atividade {atividade.id} atualizada com {atividade.turmas.count()} turmas selecionadas")
                
                messages.success(
                    request, "Atividade acadêmica atualizada com sucesso."
                )
                return redirect(return_url)
            else:
                messages.error(request, "Corrija os erros no formulário.")
        except Exception as e:
            logger.error(f"Erro ao atualizar atividade acadêmica: {str(e)}", exc_info=True)
            messages.error(
                request,
                f"Erro ao processar formulário de atividade acadêmica: {str(e)}",
            )
    else:
        # Verificar se a atividade está associada a todas as turmas ativas
        Turma = get_model_class("Turma", "turmas")
        turmas_ativas = Turma.objects.filter(status="A")
        todas_turmas_selecionadas = (
            atividade.turmas.count() == turmas_ativas.count() and
            all(turma in atividade.turmas.all() for turma in turmas_ativas)
        )
        
        # Inicializar o formulário com o valor correto para todas_turmas
        form = AtividadeAcademicaForm(
            instance=atividade, 
            initial={'todas_turmas': todas_turmas_selecionadas}
        )

    return render(
        request,
        "atividades/formulario_atividade_academica.html",
        {"form": form, "atividade": atividade, "return_url": return_url},
    )


@login_required
def excluir_atividade_academica(request, pk):
    """Função para excluir uma atividade acadêmica."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )

    if request.method == "POST":
        try:
            nome_atividade = atividade.nome  # Guardar o nome para a mensagem
            atividade.delete()
            messages.success(
                request, f"Atividade acadêmica '{nome_atividade}' excluída com sucesso."
            )
            return redirect(return_url)
        except Exception as e:
            logger.error(f"Erro ao excluir atividade acadêmica: {str(e)}", exc_info=True)
            messages.error(
                request, f"Erro ao excluir atividade acadêmica: {str(e)}"
            )
            return redirect("atividades:listar_atividades_academicas")

    return render(
        request,
        "atividades/confirmar_exclusao_academica.html",
        {"atividade": atividade, "return_url": return_url},
    )


@login_required
def confirmar_exclusao_academica(request, pk):
    """Função para confirmar a exclusão de uma atividade acadêmica."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )

    if request.method == "POST":
        try:
            nome_atividade = atividade.nome  # Guardar o nome para a mensagem
            atividade.delete()
            messages.success(
                request, f"Atividade acadêmica '{nome_atividade}' excluída com sucesso."
            )
            return redirect(return_url)
        except Exception as e:
            logger.error(f"Erro ao excluir atividade acadêmica: {str(e)}", exc_info=True)
            messages.error(
                request, f"Erro ao excluir atividade acadêmica: {str(e)}"
            )
            return redirect("atividades:detalhar_atividade_academica", pk=pk)

    return render(
        request,
        "atividades/confirmar_exclusao_academica.html",
        {"atividade": atividade, "return_url": return_url},
    )


@login_required
def detalhar_atividade_academica(request, pk):
    """Função para mostrar detalhes de uma atividade acadêmica."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )
    
    # Calcular estatísticas sobre as turmas
    total_turmas = atividade.turmas.count()
    turmas_ativas = atividade.turmas.filter(status="A").count()
    
    # Verificar se está associada a todas as turmas ativas do sistema
    Turma = get_model_class("Turma", "turmas")
    total_turmas_ativas_sistema = Turma.objects.filter(status="A").count()
    todas_turmas_ativas = (turmas_ativas == total_turmas_ativas_sistema)

    return render(
        request,
        "atividades/detalhar_atividade_academica.html",
        {
            "atividade": atividade, 
            "return_url": return_url,
            "total_turmas": total_turmas,
            "turmas_ativas": turmas_ativas,
            "todas_turmas_ativas": todas_turmas_ativas
        },
    )


@login_required
def criar_atividade_ritualistica(request):
    """Função para criar uma nova atividade ritualística."""
    AtividadeRitualisticaForm = get_form_class("AtividadeRitualisticaForm")
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    if request.method == "POST":
        try:
            form = AtividadeRitualisticaForm(request.POST)
            if form.is_valid():
                atividade = form.save(commit=False)
                atividade.save()

                # Processar o campo todos_alunos se existir
                if hasattr(form, "cleaned_data") and form.cleaned_data.get(
                    "todos_alunos"
                ):
                    # Obter todos os alunos da turma e adicioná-los à atividade
                    Aluno = get_model_class(
                        "Aluno", module_name="alunos"
                    )
                    alunos_da_turma = Aluno.objects.filter(
                        turmas=atividade.turma
                    )
                    for aluno in alunos_da_turma:
                        atividade.participantes.add(aluno)
                else:
                    # Salvar apenas os participantes selecionados no formulário
                    form.save_m2m()

                messages.success(
                    request, "Atividade ritualística criada com sucesso."
                )
                return redirect(return_url)
            else:
                messages.error(request, "Corrija os erros no formulário.")
        except Exception as e:
            logger.error(f"Erro ao criar atividade ritualística: {str(e)}", exc_info=True)
            messages.error(
                request,
                f"Erro ao processar formulário de atividade ritualística: {str(e)}",
            )
    else:
        form = AtividadeRitualisticaForm()

    return render(
        request,
        "atividades/criar_atividade_ritualistica.html",
        {"form": form, "return_url": return_url},
    )


@login_required
def editar_atividade_ritualistica(request, pk):
    """Função para editar uma atividade ritualística existente."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    AtividadeRitualisticaForm = get_form_class("AtividadeRitualisticaForm")
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    if request.method == "POST":
        try:
            form = AtividadeRitualisticaForm(request.POST, instance=atividade)
            if form.is_valid():
                atividade = form.save(commit=False)
                atividade.save()

                # Processar o campo todos_alunos se existir
                if hasattr(form, "cleaned_data") and form.cleaned_data.get(
                    "todos_alunos"
                ):
                    # Limpar participantes existentes
                    atividade.participantes.clear()
                    # Obter todos os alunos da turma e adicioná-los à atividade
                    Aluno = get_model_class(
                        "Aluno", module_name="alunos"
                    )
                    alunos_da_turma = Aluno.objects.filter(
                        turmas=atividade.turma
                    )
                    for aluno in alunos_da_turma:
                        atividade.participantes.add(aluno)
                else:
                    # Salvar apenas os participantes selecionados no formulário
                    form.save_m2m()

                messages.success(
                    request, "Atividade ritualística atualizada com sucesso."
                )
                return redirect(return_url)
            else:
                messages.error(request, "Corrija os erros no formulário.")
        except Exception as e:
            logger.error(f"Erro ao atualizar atividade ritualística: {str(e)}", exc_info=True)
            messages.error(
                request,
                f"Erro ao processar formulário de atividade ritualística: {str(e)}",
            )
    else:
        form = AtividadeRitualisticaForm(instance=atividade)

    return render(
        request,
        "atividades/editar_atividade_ritualistica.html",
        {"form": form, "atividade": atividade, "return_url": return_url},
    )


@login_required
def excluir_atividade_ritualistica(request, pk):
    """Função para excluir uma atividade ritualística."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    if request.method == "POST":
        try:
            nome_atividade = atividade.nome  # Guardar o nome para a mensagem
            atividade.delete()
            messages.success(
                request, f"Atividade ritualística '{nome_atividade}' excluída com sucesso."
            )
            return redirect(return_url)
        except Exception as e:
            logger.error(f"Erro ao excluir atividade ritualística: {str(e)}", exc_info=True)
            messages.error(
                request, f"Erro ao excluir atividade ritualística: {str(e)}"
            )
            return redirect("atividades:listar_atividades_ritualisticas")

    return render(
        request,
        "atividades/confirmar_exclusao_ritualistica.html",
        {"atividade": atividade, "return_url": return_url},
    )


@login_required
def confirmar_exclusao_ritualistica(request, pk):
    """Função para confirmar a exclusão de uma atividade ritualística."""
    AtividadeRitualistica = get
@login_required
def confirmar_exclusao_ritualistica(request, pk):
    """Função para confirmar a exclusão de uma atividade ritualística."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    if request.method == "POST":
        try:
            nome_atividade = atividade.nome  # Guardar o nome para a mensagem
            atividade.delete()
            messages.success(
                request, f"Atividade ritualística '{nome_atividade}' excluída com sucesso."
            )
            return redirect(return_url)
        except Exception as e:
            logger.error(f"Erro ao excluir atividade ritualística: {str(e)}", exc_info=True)
            messages.error(
                request, f"Erro ao excluir atividade ritualística: {str(e)}"
            )
            return redirect(
                "atividades:detalhar_atividade_ritualistica", pk=pk
            )

    return render(
        request,
        "atividades/confirmar_exclusao_ritualistica.html",
        {"atividade": atividade, "return_url": return_url},
    )


@login_required
def detalhar_atividade_ritualistica(request, pk):
    """Função para mostrar detalhes de uma atividade ritualística."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    # Calcular o total de participantes para exibição
    total_participantes = atividade.participantes.count()
    
    # Verificar se todos os alunos da turma estão participando
    Aluno = get_model_class("Aluno", module_name="alunos")
    total_alunos_turma = Aluno.objects.filter(turmas=atividade.turma).count()
    todos_alunos_participando = (total_participantes == total_alunos_turma) and (total_alunos_turma > 0)

    return render(
        request,
        "atividades/detalhar_atividade_ritualistica.html",
        {
            "atividade": atividade, 
            "return_url": return_url,
            "total_participantes": total_participantes,
            "total_alunos_turma": total_alunos_turma,
            "todos_alunos_participando": todos_alunos_participando
        },
    )


@login_required
def relatorio_atividades(request):
    """Gera um relatório de atividades."""
    # Obter parâmetros de filtro
    tipo = request.GET.get('tipo', 'todas')  # 'academicas', 'ritualisticas', 'todas'
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    turma_id = request.GET.get('turma', '')
    
    # Obter atividades acadêmicas
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividades_academicas = AtividadeAcademica.objects.all().order_by('-data_inicio')
    
    # Obter atividades ritualísticas
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividades_ritualisticas = AtividadeRitualistica.objects.all().order_by('-data')
    
    # Aplicar filtros
    if data_inicio:
        atividades_academicas = atividades_academicas.filter(data_inicio__gte=data_inicio)
        atividades_ritualisticas = atividades_ritualisticas.filter(data__gte=data_inicio)
    
    if data_fim:
        atividades_academicas = atividades_academicas.filter(data_inicio__lte=data_fim)
        atividades_ritualisticas = atividades_ritualisticas.filter(data__lte=data_fim)
    
    if turma_id:
        atividades_academicas = atividades_academicas.filter(turmas__id=turma_id)
        atividades_ritualisticas = atividades_ritualisticas.filter(turma_id=turma_id)
    
    # Filtrar por tipo se necessário
    if tipo == 'academicas':
        atividades_ritualisticas = AtividadeRitualistica.objects.none()
    elif tipo == 'ritualisticas':
        atividades_academicas = AtividadeAcademica.objects.none()
    
    # Obter lista de turmas para o filtro
    Turma = get_model_class("Turma", "turmas")
    turmas = Turma.objects.filter(status="A")
    
    # Estatísticas
    total_academicas = atividades_academicas.count()
    total_ritualisticas = atividades_ritualisticas.count()
    total_atividades = total_academicas + total_ritualisticas
    
    return render(
        request,
        "atividades/relatorio_atividades.html",
        {
            "atividades_academicas": atividades_academicas,
            "atividades_ritualisticas": atividades_ritualisticas,
            "tipo": tipo,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "turma_id": turma_id,
            "turmas": turmas,
            "total_academicas": total_academicas,
            "total_ritualisticas": total_ritualisticas,
            "total_atividades": total_atividades,
        },
    )


@login_required
def exportar_atividades(request, formato='csv'):
    """Exporta atividades para CSV ou PDF."""
    # Obter parâmetros de filtro
    tipo = request.GET.get('tipo', 'todas')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    turma_id = request.GET.get('turma', '')
    
    # Obter atividades acadêmicas
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividades_academicas = AtividadeAcademica.objects.all().order_by('-data_inicio')
    
    # Obter atividades ritualísticas
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividades_ritualisticas = AtividadeRitualistica.objects.all().order_by('-data')
    
    # Aplicar filtros
    if data_inicio:
        atividades_academicas = atividades_academicas.filter(data_inicio__gte=data_inicio)
        atividades_ritualisticas = atividades_ritualisticas.filter(data__gte=data_inicio)
    
    if data_fim:
        atividades_academicas = atividades_academicas.filter(data_inicio__lte=data_fim)
        atividades_ritualisticas = atividades_ritualisticas.filter(data__lte=data_fim)
    
    if turma_id:
        atividades_academicas = atividades_academicas.filter(turmas__id=turma_id)
        atividades_ritualisticas = atividades_ritualisticas.filter(turma_id=turma_id)
    
    # Filtrar por tipo se necessário
    if tipo == 'academicas':
        atividades_ritualisticas = AtividadeRitualistica.objects.none()
    elif tipo == 'ritualisticas':
        atividades_academicas = AtividadeAcademica.objects.none()
    
    if formato == 'csv':
        # Exportar para CSV
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="atividades.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Tipo', 'Nome', 'Data', 'Local', 'Turma(s)', 'Status'])
        
        # Adicionar atividades acadêmicas
        for atividade in atividades_academicas:
            turmas = ", ".join([t.nome for t in atividade.turmas.all()])
            writer.writerow([
                'Acadêmica',
                atividade.nome,
                atividade.data_inicio.strftime('%d/%m/%Y'),
                atividade.local or 'N/A',
                turmas,
                atividade.get_status_display()
            ])
        
        # Adicionar atividades ritualísticas
        for atividade in atividades_ritualisticas:
            writer.writerow([
                'Ritualística',
                atividade.nome,
                atividade.data.strftime('%d/%m/%Y'),
                atividade.local,
                atividade.turma.nome,
                'N/A'  # Atividades ritualísticas não têm status
            ])
        
        return response
    else:
        # Implementação futura para outros formatos
        messages.warning(request, f"Formato de exportação '{formato}' não implementado.")
        return redirect('atividades:relatorio_atividades')
@login_required
def calendario_atividades(request):
    """Exibe um calendário com todas as atividades."""
    # Obter parâmetros de filtro
    tipo = request.GET.get('tipo', 'todas')  # 'academicas', 'ritualisticas', 'todas'
    turma_id = request.GET.get('turma', '')
    mes = request.GET.get('mes', '')
    ano = request.GET.get('ano', '')
    
    # Definir mês e ano padrão se não fornecidos
    from datetime import datetime
    hoje = datetime.now()
    if not mes:
        mes = hoje.month
    else:
        mes = int(mes)
    
    if not ano:
        ano = hoje.year
    else:
        ano = int(ano)
    
    # Obter atividades acadêmicas
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividades_academicas = AtividadeAcademica.objects.all()
    
    # Obter atividades ritualísticas
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividades_ritualisticas = AtividadeRitualistica.objects.all()
    
    # Filtrar por mês e ano
    from django.db.models import Q
    import calendar
    
    # Último dia do mês
    ultimo_dia = calendar.monthrange(ano, mes)[1]
    
    # Datas de início e fim do mês
    from datetime import date
    data_inicio_mes = date(ano, mes, 1)
    data_fim_mes = date(ano, mes, ultimo_dia)
    
    # Filtrar atividades acadêmicas
    atividades_academicas = atividades_academicas.filter(
        Q(data_inicio__gte=data_inicio_mes, data_inicio__lte=data_fim_mes) |  # Começa no mês
        Q(data_fim__gte=data_inicio_mes, data_fim__lte=data_fim_mes) |  # Termina no mês
        Q(data_inicio__lte=data_inicio_mes, data_fim__gte=data_fim_mes)  # Abrange todo o mês
    )
    
    # Filtrar atividades ritualísticas
    atividades_ritualisticas = atividades_ritualisticas.filter(
        data__gte=data_inicio_mes, data__lte=data_fim_mes
    )
    
    # Filtrar por turma se especificado
    if turma_id:
        atividades_academicas = atividades_academicas.filter(turmas__id=turma_id)
        atividades_ritualisticas = atividades_ritualisticas.filter(turma_id=turma_id)
    
    # Filtrar por tipo se necessário
    if tipo == 'academicas':
        atividades_ritualisticas = AtividadeRitualistica.objects.none()
    elif tipo == 'ritualisticas':
        atividades_academicas = AtividadeAcademica.objects.none()
    
    # Obter lista de turmas para o filtro
    Turma = get_model_class("Turma", "turmas")
    turmas = Turma.objects.filter(status="A")
    
    # Preparar dados do calendário
    calendario_dados = {}
    
    # Adicionar atividades acadêmicas ao calendário
    for atividade in atividades_academicas:
        data_inicio = max(atividade.data_inicio.date(), data_inicio_mes)
        data_fim = min(atividade.data_fim.date() if atividade.data_fim else data_inicio, data_fim_mes)
        
        # Para cada dia entre data_inicio e data_fim
        current_date = data_inicio
        while current_date <= data_fim:
            dia = current_date.day
            if dia not in calendario_dados:
                calendario_dados[dia] = []
            
            calendario_dados[dia].append({
                'tipo': 'academica',
                'id': atividade.id,
                'nome': atividade.nome,
                'url': reverse('atividades:detalhar_atividade_academica', args=[atividade.id]),
                'turmas': [t.nome for t in atividade.turmas.all()],
                'status': atividade.get_status_display()
            })
            
            # Avançar para o próximo dia
            from datetime import timedelta
            current_date += timedelta(days=1)
    
    # Adicionar atividades ritualísticas ao calendário
    for atividade in atividades_ritualisticas:
        dia = atividade.data.day
        if dia not in calendario_dados:
            calendario_dados[dia] = []
        
        calendario_dados[dia].append({
            'tipo': 'ritualistica',
            'id': atividade.id,
            'nome': atividade.nome,
            'url': reverse('atividades:detalhar_atividade_ritualistica', args=[atividade.id]),
            'turma': atividade.turma.nome,
            'hora': f"{atividade.hora_inicio.strftime('%H:%M')} - {atividade.hora_fim.strftime('%H:%M')}"
        })
    
    # Gerar estrutura do calendário
    import calendar
    cal = calendar.monthcalendar(ano, mes)
    
    # Nomes dos meses em português
    meses = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ]
    
    # Mês anterior e próximo mês para navegação
    if mes == 1:
        mes_anterior = 12
        ano_anterior = ano - 1
    else:
        mes_anterior = mes - 1
        ano_anterior = ano
    
    if mes == 12:
        proximo_mes = 1
        proximo_ano = ano + 1
    else:
        proximo_mes = mes + 1
        proximo_ano = ano
    
    return render(
        request,
        "atividades/calendario_atividades.html",
        {
            "calendario": cal,
            "calendario_dados": calendario_dados,
            "mes": mes,
            "ano": ano,
            "nome_mes": meses[mes-1],
            "mes_anterior": mes_anterior,
            "ano_anterior": ano_anterior,
            "proximo_mes": proximo_mes,
            "proximo_ano": proximo_ano,
            "tipo": tipo,
            "turma_id": turma_id,
            "turmas": turmas,
        },
    )


@login_required
def buscar_atividades(request):
    """API para buscar atividades."""
    query = request.GET.get('q', '')
    tipo = request.GET.get('tipo', 'todas')
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    resultados = []
    
    # Buscar atividades acadêmicas
    if tipo in ['todas', 'academicas']:
        AtividadeAcademica = get_model_class("AtividadeAcademica")
        atividades_academicas = AtividadeAcademica.objects.filter(
            nome__icontains=query
        )[:10]  # Limitar a 10 resultados
        
        for atividade in atividades_academicas:
            resultados.append({
                'id': atividade.id,
                'nome': atividade.nome,
                'tipo': 'Acadêmica',
                'data': atividade.data_inicio.strftime('%d/%m/%Y'),
                'url': reverse('atividades:detalhar_atividade_academica', args=[atividade.id])
            })
    
    # Buscar atividades ritualísticas
    if tipo in ['todas', 'ritualisticas']:
        AtividadeRitualistica = get_model_class("AtividadeRitualistica")
        atividades_ritualisticas = AtividadeRitualistica.objects.filter(
            nome__icontains=query
        )[:10]  # Limitar a 10 resultados
        
        for atividade in atividades_ritualisticas:
            resultados.append({
                'id': atividade.id,
                'nome': atividade.nome,
                'tipo': 'Ritualística',
                'data': atividade.data.strftime('%d/%m/%Y'),
                'url': reverse('atividades:detalhar_atividade_ritualistica', args=[atividade.id])
            })
    
    return JsonResponse(resultados, safe=False)


@login_required
def copiar_atividade_academica(request, pk):
    """Cria uma cópia de uma atividade acadêmica existente."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividade_original = get_object_or_404(AtividadeAcademica, pk=pk)
    
    if request.method == "POST":
        # Criar uma nova atividade com os mesmos dados
        nova_atividade = AtividadeAcademica.objects.create(
            nome=f"Cópia de {atividade_original.nome}",
            descricao=atividade_original.descricao,
            data_inicio=atividade_original.data_inicio,
            data_fim=atividade_original.data_fim,
            responsavel=atividade_original.responsavel,
            local=atividade_original.local,
            tipo_atividade=atividade_original.tipo_atividade,
            status="agendada"  # Sempre começa como agendada
        )
        
        # Copiar as turmas associadas
        for turma in atividade_original.turmas.all():
            nova_atividade.turmas.add(turma)
        
        messages.success(request, "Atividade acadêmica copiada com sucesso.")
        return redirect("atividades:editar_atividade_academica", pk=nova_atividade.id)
    
    return render(
        request,
        "atividades/confirmar_copia_academica.html",
        {"atividade": atividade_original},
    )


@login_required
def copiar_atividade_ritualistica(request, pk):
    """Cria uma cópia de uma atividade ritualística existente."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividade_original = get_object_or_404(AtividadeRitualistica, pk=pk)
    
    if request.method == "POST":
        # Criar uma nova atividade com os mesmos dados
        nova_atividade = AtividadeRitualistica.objects.create(
            nome=f"Cópia de {atividade_original.nome}",
            descricao=atividade_original.descricao,
            data=atividade_original.data,
            hora_inicio=atividade_original.hora_inicio,
            hora_fim=atividade_original.hora_fim,
            local=atividade_original.local,
            turma=atividade_original.turma
        )
        
        # Copiar os participantes
        for participante in atividade_original.participantes.all():
            nova_atividade.participantes.add(participante)
        
        messages.success(request, "Atividade ritualística copiada com sucesso.")
        return redirect("atividades:editar_atividade_ritualistica", pk=nova_atividade.id)
    
    return render(
        request,
        "atividades/confirmar_copia_ritualistica.html",
        {"atividade": atividade_original},
    )
from django.http import JsonResponse

@login_required
def obter_alunos_turma(request):
    """API para obter alunos de uma turma específica."""
    turma_id = request.GET.get('turma_id')
    
    if not turma_id:
        return JsonResponse({'error': 'ID da turma não fornecido'}, status=400)
    
    try:
        # Obter a turma
        Turma = get_model_class("Turma", "turmas")
        turma = Turma.objects.get(id=turma_id)
        
        # Obter alunos matriculados na turma
        Aluno = get_model_class("Aluno", "alunos")
        Matricula = get_model_class("Matricula", "matriculas")
        
        # Verificar se o modelo Matricula tem o campo 'aluno' e 'turma'
        matriculas = Matricula.objects.filter(turma=turma, status='A')
        alunos = [matricula.aluno for matricula in matriculas]
        
        # Formatar dados para retorno
        alunos_data = []
        for aluno in alunos:
            alunos_data.append({
                'id': aluno.cpf,  # Usando CPF como ID conforme o modelo
                'nome': aluno.nome,
                'numero_iniciatico': aluno.numero_iniciatico or 'N/A'
            })
        
        return JsonResponse({'alunos': alunos_data})
    
    except Turma.DoesNotExist:
        return JsonResponse({'error': 'Turma não encontrada'}, status=404)
    except Exception as e:
        logger.error(f"Erro ao obter alunos da turma: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def registrar_frequencia_atividade(request, pk):
    """Registra frequência dos alunos em uma atividade acadêmica."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    
    # Obter o modelo de Frequência
    Frequencia = get_model_class("Frequencia", "frequencias")
    
    if request.method == "POST":
        # Obter dados do formulário
        data = request.POST.get('data')
        alunos_presentes = request.POST.getlist('presentes')
        
        # Obter alunos das turmas associadas à atividade
        Aluno = get_model_class("Aluno", "alunos")
        Matricula = get_model_class("Matricula", "matriculas")
        
        alunos_turmas = set()
        for turma in atividade.turmas.all():
            matriculas = Matricula.objects.filter(turma=turma, status='A')
            for matricula in matriculas:
                alunos_turmas.add(matricula.aluno)
        
        # Registrar frequência para cada aluno
        registros_criados = 0
        registros_atualizados = 0
        
        for aluno in alunos_turmas:
            presente = str(aluno.cpf) in alunos_presentes
            justificativa = request.POST.get(f'justificativa_{aluno.cpf}', '')
            
            # Verificar se já existe registro para este aluno, atividade e data
            frequencia, created = Frequencia.objects.update_or_create(
                aluno=aluno,
                atividade=atividade,
                data=data,
                defaults={
                    'presente': presente,
                    'justificativa': justificativa if not presente else ''
                }
            )
            
            if created:
                registros_criados += 1
            else:
                registros_atualizados += 1
        
        messages.success(
            request, 
            f"Frequência registrada com sucesso. {registros_criados} novos registros, {registros_atualizados} atualizados."
        )
        return redirect("atividades:detalhar_atividade_academica", pk=atividade.id)
    
    # Para requisições GET, exibir o formulário
    # Obter alunos das turmas associadas à atividade
    Aluno = get_model_class("Aluno", "alunos")
    Matricula = get_model_class("Matricula", "matriculas")
    
    alunos = []
    for turma in atividade.turmas.all():
        matriculas = Matricula.objects.filter(turma=turma, status='A')
        for matricula in matriculas:
            if matricula.aluno not in alunos:
                alunos.append(matricula.aluno)
    
    # Ordenar alunos por nome
    alunos.sort(key=lambda x: x.nome)
    
    return render(
        request,
        "atividades/registrar_frequencia.html",
        {
            "atividade": atividade,
            "alunos": alunos,
            "data_hoje": timezone.now().date().isoformat()
        },
    )


@login_required
def visualizar_frequencia_atividade(request, pk):
    """Visualiza a frequência dos alunos em uma atividade acadêmica."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    
    # Obter o modelo de Frequência
    Frequencia = get_model_class("Frequencia", "frequencias")
    
    # Obter data selecionada ou usar a mais recente
    data_selecionada = request.GET.get('data', None)
    
    # Obter datas disponíveis para esta atividade
    datas_disponiveis = Frequencia.objects.filter(
        atividade=atividade
    ).values_list('data', flat=True).distinct().order_by('-data')
    
    if not data_selecionada and datas_disponiveis:
        data_selecionada = datas_disponiveis[0]
    
    # Obter frequências para a data selecionada
    frequencias = []
    if data_selecionada:
        frequencias = Frequencia.objects.filter(
            atividade=atividade,
            data=data_selecionada
        ).select_related('aluno')
    
    # Calcular estatísticas
    total_registros = len(frequencias)
    presentes = sum(1 for f in frequencias if f.presente)
    ausentes = total_registros - presentes
    
    # Calcular taxa de presença
    taxa_presenca = (presentes / total_registros * 100) if total_registros > 0 else 0
    
    return render(
        request,
        "atividades/visualizar_frequencia.html",
        {
            "atividade": atividade,
            "frequencias": frequencias,
            "datas_disponiveis": datas_disponiveis,
            "data_selecionada": data_selecionada,
            "total_registros": total_registros,
            "presentes": presentes,
            "ausentes": ausentes,
            "taxa_presenca": taxa_presenca
        },
    )


@login_required
def dashboard_atividades(request):
    """Dashboard com estatísticas de atividades."""
    # Obter contagens
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    
    total_academicas = AtividadeAcademica.objects.count()
    total_ritualisticas = AtividadeRitualistica.objects.count()
    
    # Atividades por status
    academicas_por_status = {
        status[0]: AtividadeAcademica.objects.filter(status=status[0]).count()
        for status in AtividadeAcademica.STATUS_CHOICES
    }
    
    # Atividades por tipo
    academicas_por_tipo = {
        tipo[0]: AtividadeAcademica.objects.filter(tipo_atividade=tipo[0]).count()
        for tipo in AtividadeAcademica.TIPO_CHOICES
    }
    
    # Atividades recentes
    atividades_academicas_recentes = AtividadeAcademica.objects.order_by('-data_inicio')[:5]
    atividades_ritualisticas_recentes = AtividadeRitualistica.objects.order_by('-data')[:5]
    
    # Atividades por mês (últimos 6 meses)
    from django.db.models import Count
    from django.db.models.functions import TruncMonth
    import datetime
    
    # Data de 6 meses atrás
    seis_meses_atras = datetime.date.today() - datetime.timedelta(days=180)
    
    # Atividades acadêmicas por mês
    academicas_por_mes = AtividadeAcademica.objects.filter(
        data_inicio__gte=seis_meses_atras
    ).annotate(
        mes=TruncMonth('data_inicio')
    ).values('mes').annotate(
        total=Count('id')
    ).order_by('mes')
    
    # Atividades ritualísticas por mês
    ritualisticas_por_mes = AtividadeRitualistica.objects.filter(
        data__gte=seis_meses_atras
    ).annotate(
        mes=TruncMonth('data')
    ).values('mes').annotate(
        total=Count('id')
    ).order_by('mes')
    
    # Preparar dados para o gráfico
    meses = []
    dados_academicas = []
    dados_ritualisticas = []
    
    # Criar dicionários para facilitar o acesso
    dict_academicas = {item['mes'].strftime('%Y-%m'): item['total'] for item in academicas_por_mes}
    dict_ritualisticas = {item['mes'].strftime('%Y-%m'): item['total'] for item in ritualisticas_por_mes}
    
    # Gerar lista de meses (últimos 6)
    current_date = datetime.date.today()
    for i in range(5, -1, -1):
        date = current_date - datetime.timedelta(days=30*i)
        month_key = date.strftime('%Y-%m')
        month_name = date.strftime('%b/%Y')
        
        meses.append(month_name)
        dados_academicas.append(dict_academicas.get(month_key, 0))
        dados_ritualisticas.append(dict_ritualisticas.get(month_key, 0))
    
    return render(
        request,
        "atividades/dashboard.html",
        {
            "total_academicas": total_academicas,
            "total_ritualisticas": total_ritualisticas,
            "academicas_por_status": academicas_por_status,
            "academicas_por_tipo": academicas_por_tipo,
            "atividades_academicas_recentes": atividades_academicas_recentes,
            "atividades_ritualisticas_recentes": atividades_ritualisticas_recentes,
            "meses": meses,
            "dados_academicas": dados_academicas,
            "dados_ritualisticas": dados_ritualisticas,
        },
    )
