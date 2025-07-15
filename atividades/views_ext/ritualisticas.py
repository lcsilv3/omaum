import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .utils import get_form_class, get_model_class

# Configurar logger
logger = logging.getLogger(__name__)


@login_required
def listar_atividades_ritualisticas(request):
    """Lista todas as atividades ritualísticas."""
    try:
        AtividadeRitualistica = get_model_class("AtividadeRitualistica")
        
        # Obter parâmetros de filtro
        query = request.GET.get("q", "")
        
        # Consulta base
        atividades = AtividadeRitualistica.objects.all().prefetch_related("participantes")
        
        # Aplicar filtros
        if query:
            atividades = atividades.filter(
                Q(nome__icontains=query) |
                Q(descricao__icontains=query)
            )
        
        # Paginação
        paginator = Paginator(atividades, 10)  # 10 itens por página
        page = request.GET.get('page')
        
        try:
            atividades_paginadas = paginator.page(page)
        except PageNotAnInteger:
            atividades_paginadas = paginator.page(1)
        except EmptyPage:
            atividades_paginadas = paginator.page(paginator.num_pages)
        
        context = {
            "atividades": atividades_paginadas,
            "page_obj": atividades_paginadas,
            "query": query,
            "total_atividades": atividades.count(),
        }
        
        return render(
            request, 
            "atividades/ritualisticas/listar_atividades_ritualisticas.html", 
            context
        )
    except Exception as e:
        logger.error(
            f"Erro ao listar atividades ritualísticas: {str(e)}", 
            exc_info=True
        )
        messages.error(
            request, 
            f"Ocorreu um erro ao listar as atividades: {str(e)}"
        )
        return render(
            request,
            "atividades/ritualisticas/listar_atividades_ritualisticas.html",
            {
                "atividades": [],
                "page_obj": None,
                "query": "",
                "error_message": f"Erro ao listar atividades: {str(e)}",
            }
        )

@login_required
def criar_atividade_ritualistica(request):
    """Cria uma nova atividade ritualística."""
    try:
        AtividadeRitualisticaForm = get_form_class("AtividadeRitualisticaForm")
        
        if request.method == "POST":
            form = AtividadeRitualisticaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request, 
                    "Atividade ritualística criada com sucesso!"
                )
                return redirect("atividades:listar_atividades_ritualisticas")
            else:
                messages.error(request, "Por favor, corrija os erros abaixo.")
        else:
            form = AtividadeRitualisticaForm()
        
        return render(
            request, 
            "atividades/ritualisticas/form_atividade_ritualistica.html", 
            {"form": form}
        )
    except Exception as e:
        logger.error(
            f"Erro ao criar atividade ritualística: {str(e)}", 
            exc_info=True
        )
        messages.error(
            request, 
            f"Ocorreu um erro ao criar a atividade: {str(e)}"
        )
        return redirect("atividades:listar_atividades_ritualisticas")

@login_required
def editar_atividade_ritualistica(request, id):
    """Edita uma atividade ritualística existente."""
    try:
        AtividadeRitualistica = get_model_class("AtividadeRitualistica")
        AtividadeRitualisticaForm = get_form_class("AtividadeRitualisticaForm")
        
        atividade = get_object_or_404(AtividadeRitualistica, id=id)
        
        if request.method == "POST":
            form = AtividadeRitualisticaForm(request.POST, instance=atividade)
            if form.is_valid():
                form.save()
                messages.success(
                    request, 
                    "Atividade ritualística atualizada com sucesso!"
                )
                return redirect("atividades:listar_atividades_ritualisticas")
            else:
                messages.error(request, "Por favor, corrija os erros abaixo.")
        else:
            form = AtividadeRitualisticaForm(instance=atividade)
        
        return render(
            request, 
            "atividades/ritualisticas/form_atividade_ritualistica.html", 
            {"form": form, "atividade": atividade}
        )
    except Exception as e:
        logger.error(
            f"Erro ao editar atividade ritualística {id}: {str(e)}", 
            exc_info=True
        )
        messages.error(
            request, 
            f"Ocorreu um erro ao editar a atividade: {str(e)}"
        )
        return redirect("atividades:listar_atividades_ritualisticas")

@login_required
def detalhar_atividade_ritualistica(request, id):
    """Exibe detalhes de uma atividade ritualística."""
    try:
        AtividadeRitualistica = get_model_class("AtividadeRitualistica")
        
        atividade = get_object_or_404(
            AtividadeRitualistica.objects.prefetch_related("participantes"),
            id=id
        )
        
        return render(
            request, 
            "atividades/ritualisticas/detalhar_atividade_ritualistica.html", 
            {"atividade": atividade}
        )
    except Exception as e:
        logger.error(
            f"Erro ao detalhar atividade ritualística {id}: {str(e)}", 
            exc_info=True
        )
        messages.error(
            request, 
            f"Ocorreu um erro ao exibir os detalhes da atividade: {str(e)}"
        )
        return redirect("atividades:listar_atividades_ritualisticas")

@login_required
def excluir_atividade_ritualistica(request, id):
    """Exclui uma atividade ritualística."""
    try:
        AtividadeRitualistica = get_model_class("AtividadeRitualistica")
        
        atividade = get_object_or_404(AtividadeRitualistica, id=id)
        
        if request.method == "POST":
            atividade.delete()
            messages.success(
                request, 
                "Atividade ritualística excluída com sucesso!"
            )
            return redirect("atividades:listar_atividades_ritualisticas")
        
        return render(
            request, 
            "atividades/ritualisticas/excluir_atividade_ritualistica.html", 
            {"atividade": atividade}
        )
    except Exception as e:
        logger.error(
            f"Erro ao excluir atividade ritualística {id}: {str(e)}", 
            exc_info=True
        )
        messages.error(
            request, 
            f"Ocorreu um erro ao excluir a atividade: {str(e)}"
        )
        return redirect("atividades:listar_atividades_ritualisticas")

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