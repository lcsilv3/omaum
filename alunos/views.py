from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from django.db import transaction
import logging
from django.template.loader import render_to_string

# Importações refatoradas e simplificadas
from .forms import AlunoForm, RegistroHistoricoFormSet
from .models import Aluno
from . import services
from cursos.services import listar_cursos as listar_todos_cursos

logger = logging.getLogger(__name__)


@login_required
def listar_alunos(request):
    """Lista todos os alunos, com suporte a busca dinâmica (AJAX)."""
    try:
        query = request.GET.get("q", "")
        curso_id = request.GET.get("curso", "")
        page_number = request.GET.get("page")

        # Utiliza o serviço para buscar e filtrar os alunos
        alunos_list = services.listar_alunos(query=query, curso_id=curso_id)
        total_alunos = alunos_list.count()

        paginator = Paginator(alunos_list, 10)  # 10 alunos por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Busca cursos para o dropdown de filtro
        cursos_para_filtro = listar_todos_cursos()

        # Se for uma requisição AJAX, retorna um JSON com os dados atualizados
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            tabela_html = render_to_string(
                'alunos/_tabela_alunos_parcial.html',
                {'alunos': page_obj, 'page_obj': page_obj, 'total_alunos': total_alunos}
            )
            paginacao_html = render_to_string(
                'alunos/_paginacao_parcial.html', {'page_obj': page_obj, 'query': query, 'curso_selecionado': curso_id}
            )
            return JsonResponse({
                'tabela_html': tabela_html,
                'paginacao_html': paginacao_html,
                'total_alunos': total_alunos
            })

        context = {
            'page_obj': page_obj,
            'query': query,
            'cursos': Curso.objects.all().order_by('nome'),
            'curso_selecionado': curso_id,
            'total_alunos': total_alunos,  # Garante que o total seja passado no contexto inicial
        }
        return render(request, 'alunos/listar_alunos.html', context)
    except Exception as e:
        logger.error(f"Erro ao listar alunos: {e}")
        # Para AJAX, retorna um erro em JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Ocorreu um erro ao processar a sua solicitação.'}, status=500)
        messages.error(request, "Ocorreu um erro ao listar os alunos.")
        return redirect("core:pagina_inicial") # Redireciona para uma página segura


@login_required
@permission_required("alunos.add_aluno", raise_exception=True)
def criar_aluno(request):
    """
    Cria um novo aluno e gerencia seu histórico de registros.
    """
    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES)
        historico_formset = RegistroHistoricoFormSet(request.POST, prefix='historico')

        if form.is_valid() and historico_formset.is_valid():
            try:
                with transaction.atomic():
                    aluno = form.save(commit=False)
                    aluno.cpf = ''.join(filter(str.isdigit, str(aluno.cpf)))
                    aluno.save()

                    historico_formset.instance = aluno
                    historico_formset.save()

                messages.success(request, "Aluno criado com sucesso!")
                return redirect("alunos:listar_alunos")
            except Exception as e:
                logger.error(f"Erro ao criar aluno: {e}")
                messages.error(request, f"Ocorreu um erro ao salvar o aluno: {e}")
    else:
        form = AlunoForm()
        historico_formset = RegistroHistoricoFormSet(prefix='historico')
    
    context = {
        "form": form,
        "historico_formset": historico_formset,
        "aluno": None
    }
    return render(request, "alunos/formulario_aluno.html", context)


@login_required
def detalhar_aluno(request, cpf):
    """Exibe os detalhes de um aluno e seu histórico de registros."""
    aluno = services.obter_aluno_por_cpf(cpf)
    if not aluno:
        messages.error(request, "Aluno não encontrado.")
        return redirect("alunos:listar_alunos")

    # A lógica de dependências pode ser mantida ou ajustada conforme necessário
    # dependencias = services.verificar_dependencias_aluno(aluno) 
    historico_list = services.listar_historico_aluno(aluno)

    context = {
        "aluno": aluno,
        # "dependencias": dependencias,
        "historico_list": historico_list,
    }
    return render(request, "alunos/detalhar_aluno.html", context)


@login_required
@permission_required("alunos.change_aluno", raise_exception=True)
def editar_aluno(request, cpf):
    """
    Edita um aluno existente e seu histórico de registros.
    """
    aluno = get_object_or_404(Aluno, cpf=cpf)

    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES, instance=aluno)
        historico_formset = RegistroHistoricoFormSet(request.POST, instance=aluno, prefix='historico')

        if form.is_valid() and historico_formset.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    historico_formset.save()
                
                messages.success(request, "Aluno atualizado com sucesso!")
                return redirect("alunos:listar_alunos")
            except Exception as e:
                logger.error(f"Erro ao editar aluno {cpf}: {e}")
                messages.error(request, f"Ocorreu um erro ao atualizar o aluno: {e}")
    else:
        form = AlunoForm(instance=aluno)
        historico_formset = RegistroHistoricoFormSet(instance=aluno, prefix='historico')

    context = {
        "form": form,
        "historico_formset": historico_formset,
        "aluno": aluno
    }
    return render(request, "alunos/formulario_aluno.html", context)


@login_required
@permission_required("alunos.delete_aluno", raise_exception=True)
def excluir_aluno(request, cpf):
    """Exclui um aluno utilizando a camada de serviço."""
    aluno = services.obter_aluno_por_cpf(cpf)
    if not aluno:
        messages.error(request, "Aluno não encontrado.")
        return redirect("alunos:listar_alunos")

    # A verificação de dependências pode ser mantida
    # dependencias = services.verificar_dependencias_aluno(aluno)

    if request.method == "POST":
        try:
            # A lógica de exclusão pode precisar de ajustes se houver dependências
            aluno.delete() 
            messages.success(request, "Aluno excluído com sucesso!")
            return redirect("alunos:listar_alunos")
        except Exception as e:
            messages.error(request, f"Não foi possível excluir o aluno. Erro: {e}")
            return redirect("alunos:detalhar_aluno", cpf=cpf)

    context = {
        "aluno": aluno,
        # "dependencias": dependencias
    }
    return render(request, "alunos/excluir_aluno.html", context)

# ... (O restante das views como importar/exportar podem ser refatoradas de forma similar se necessário)
# Por enquanto, o foco foi no CRUD principal e na listagem.