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
def copiar_atividade_academica(request, id):
    """Cria uma cópia de uma atividade acadêmica existente."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    AtividadeAcademicaForm = get_form_class("AtividadeAcademicaForm")
    
    # Obter atividade original
    atividade_original = get_object_or_404(AtividadeAcademica, id=id)
    
    if request.method == "POST":
        # Criar formulário com dados do POST
        form = AtividadeAcademicaForm(request.POST)
        
        if form.is_valid():
            # Salvar nova atividade
            nova_atividade = form.save()
            
            # Verificar se deve copiar frequências
            copiar_frequencias = request.POST.get('copiar_frequencias') == 'on'
            
            if copiar_frequencias:
                try:
                    # Importar modelo de Frequencia
                    Frequencia = get_model_class("Frequencia", "frequencias")
                    
                    # Obter frequências da atividade original
                    frequencias_originais = Frequencia.objects.filter(atividade=atividade_original)
                    
                    # Criar novas frequências
                    for freq in frequencias_originais:
                        Frequencia.objects.create(
                            aluno=freq.aluno,
                            atividade=nova_atividade,
                            data=nova_atividade.data_inicio,  # Usar a nova data
                            presente=False,  # Inicialmente todos ausentes
                            justificativa=None
                        )
                    
                    messages.success(
                        request, 
                        f"Atividade copiada com sucesso! {frequencias_originais.count()} registros de frequência foram copiados."
                    )
                except Exception as e:
                    logger.error(f"Erro ao copiar frequências: {str(e)}")
                    messages.warning(
                        request, 
                        f"Atividade copiada, mas ocorreu um erro ao copiar as frequências: {str(e)}"
                    )
            else:
                messages.success(request, "Atividade copiada com sucesso!")
            
            return redirect("atividades:detalhar_atividade_academica", pk=nova_atividade.id)
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        # Pré-preencher formulário com dados da atividade original
        initial_data = {
            'nome': f"Cópia de {atividade_original.nome}",
            'descricao': atividade_original.descricao,
            'tipo_atividade': atividade_original.tipo_atividade,
            'responsavel': atividade_original.responsavel,
            'local': atividade_original.local,
            'status': 'agendada',  # Sempre começa como agendada
        }
        form = AtividadeAcademicaForm(initial=initial_data)
    
    return render(
        request,
        "atividades/copiar_atividade_academica.html",
        {
            "form": form,
            "atividade_original": atividade_original,
        },
    )