import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator

from .utils import get_return_url, get_form_class, get_model_class

# Set up logger
logger = logging.getLogger(__name__)

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
def copiar_atividade_ritualistica(request, id):
    """Cria uma cópia de uma atividade ritualística existente."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    AtividadeRitualisticaForm = get_form_class("AtividadeRitualisticaForm")
    
    # Obter atividade original
    atividade_original = get_object_or_404(AtividadeRitualistica, id=id)
    
    if request.method == "POST":
        # Criar formulário com dados do POST
        form = AtividadeRitualisticaForm(request.POST)
        
        if form.is_valid():
            # Salvar nova atividade sem os participantes
            nova_atividade = form.save(commit=False)
            nova_atividade.save()
            
            # Verificar se deve copiar participantes
            copiar_participantes = request.POST.get('copiar_participantes') == 'on'
            
            if copiar_participantes:
                # Copiar participantes da atividade original
                for participante in atividade_original.participantes.all():
                    nova_atividade.participantes.add(participante)
                
                messages.success(
                    request, 
                    f"Atividade copiada com sucesso! {atividade_original.participantes.count()} participantes foram copiados."
                )
            else:
                # Salvar apenas os participantes selecionados no formulário
                form.save_m2m()
                messages.success(request, "Atividade copiada com sucesso!")
            
            return redirect("atividades:detalhar_atividade_ritualistica", pk=nova_atividade.id)
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        # Pré-preencher formulário com dados da atividade original
        initial_data = {
            'nome': f"Cópia de {atividade_original.nome}",
            'descricao': atividade_original.descricao,
            'data': atividade_original.data,
            'hora_inicio': atividade_original.hora_inicio,
            'hora_fim': atividade_original.hora_fim,
            'local': atividade_original.local,
            'turma': atividade_original.turma,
        }
        form = AtividadeRitualisticaForm(initial=initial_data)
    
    context = {
        "form": form,
        "atividade_original": atividade_original,
    }
    
    return render(request, "atividades/copiar_atividade_ritualistica.html", context)