import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from atividades.models import AtividadeAcademica
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from importlib import import_module
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_GET

# Configurar logger
logger = logging.getLogger(__name__)

# Função centralizada para obter modelos
def get_models():
    """Obtém os modelos necessários dinamicamente."""
    try:
        atividades_module = import_module("atividades.models")
        cursos_module = import_module("cursos.models")
        turmas_module = import_module("turmas.models")
        
        return {
            'AtividadeAcademica': getattr(atividades_module, "AtividadeAcademica"),
            'Curso': getattr(cursos_module, "Curso"),
            'Turma': getattr(turmas_module, "Turma"),
        }
    except (ImportError, AttributeError) as e:
        logger.error("Erro ao obter modelos: %s", str(e), exc_info=True)
        raise

# Utilitários
def get_form_class(form_name):
    """Obtém uma classe de formulário dinamicamente."""
    try:
        forms_module = import_module("atividades.forms")
        return getattr(forms_module, form_name)
    except (ImportError, AttributeError) as e:
        logger.error("Erro ao obter formulário %s: %s", form_name, str(e))
        raise

def get_model_class(model_name, app_name="atividades"):
    """Obtém uma classe de modelo dinamicamente."""
    try:
        models_module = import_module(f"{app_name}.models")
        return getattr(models_module, model_name)
    except (ImportError, AttributeError) as e:
        logger.error("Erro ao obter modelo %s: %s", model_name, str(e))
        raise

@login_required
def listar_atividades_academicas(request):
    """
    Lista atividades acadêmicas com filtros dinâmicos por curso e turma.
    Suporta AJAX para atualização parcial da tabela.
    """
    query = request.GET.get("q", "")
    codigo_curso = request.GET.get("curso", "")
    turma_id = request.GET.get("turma", "")

    # Queryset de cursos (garante que cada curso tem .id e .nome)
    models = get_models()
    cursos = models['Curso'].objects.all()
    turmas = models['Turma'].objects.all()

    # Filtro de atividades
    atividades = models['AtividadeAcademica'].objects.all()
    if query:
        atividades = atividades.filter(nome__icontains=query)
    if codigo_curso:
        atividades = atividades.filter(curso__codigo_curso=codigo_curso)
        turmas = turmas.filter(curso__codigo_curso=codigo_curso)
    if turma_id:
        atividades = atividades.filter(turmas__id=turma_id)

    # Para manter o filtro selecionado
    context = {
        "atividades": atividades,
        "cursos": cursos,
        "turmas": turmas,
        "query": query,
        "curso_selecionado": codigo_curso,
        "turma_selecionada": turma_id,
    }

    # AJAX: retorna apenas o corpo da tabela para atualização dinâmica
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "atividades/partials/atividades_tabela_body.html", context)
    return render(request, "atividades/academicas/listar_atividades_academicas.html", context)

@require_GET
@login_required
def ajax_turmas_por_curso(request):
    """Endpoint AJAX: retorna as turmas de um curso em JSON."""
    curso_id = request.GET.get("curso_id")
    Turma = import_module("turmas.models").Turma
    turmas = Turma.objects.filter(curso_id=curso_id).values("id", "nome")
    return JsonResponse(list(turmas), safe=False)

@require_GET
@login_required
def ajax_atividades_filtradas(request):
    """
    Endpoint AJAX: retorna atividades filtradas por curso/turma/nome.
    Retorna HTML parcial da tabela.
    """
    return listar_atividades_academicas(request)

@login_required
def criar_atividade_academica(request):
    """Cria uma nova atividade acadêmica."""
    try:
        AtividadeAcademicaForm = get_form_class("AtividadeAcademicaForm")
        
        if request.method == "POST":
            form = AtividadeAcademicaForm(request.POST)
            if form.is_valid():
                atividade = form.save()
                messages.success(
                    request, 
                    "Atividade acadêmica criada com sucesso!"
                )
                return redirect("atividades:listar_atividades_academicas")
            else:
                messages.error(request, "Por favor, corrija os erros abaixo.")
        else:
            form = AtividadeAcademicaForm()
        
        return render(
            request, 
            "atividades/academicas/form_atividade_academica.html", 
            {"form": form}
        )
    except Exception as e:
        logger.error(
            f"Erro ao criar atividade acadêmica: {str(e)}", 
            exc_info=True
        )
        messages.error(
            request, 
            f"Ocorreu um erro ao criar a atividade: {str(e)}"
        )
        return redirect("atividades:listar_atividades_academicas")

@login_required
def editar_atividade_academica(request, id):
    """Edita uma atividade acadêmica existente."""
    try:
        models = get_models()
        AtividadeAcademica = models['AtividadeAcademica']
        AtividadeAcademicaForm = get_form_class("AtividadeAcademicaForm")
        
        atividade = get_object_or_404(AtividadeAcademica, id=id)
        
        if request.method == "POST":
            form = AtividadeAcademicaForm(request.POST, instance=atividade)
            if form.is_valid():
                form.save()
                messages.success(
                    request, 
                    "Atividade acadêmica atualizada com sucesso!"
                )
                return redirect("atividades:listar_atividades_academicas")
            else:
                messages.error(request, "Por favor, corrija os erros abaixo.")
        else:
            form = AtividadeAcademicaForm(instance=atividade)
        
        return render(
            request, 
            "atividades/academicas/form_atividade_academica.html", 
            {"form": form, "atividade": atividade}
        )
    except Exception as e:
        logger.error(
            f"Erro ao editar atividade acadêmica {id}: {str(e)}", 
            exc_info=True
        )
        messages.error(
            request, 
            f"Ocorreu um erro ao editar a atividade: {str(e)}"
        )
        return redirect("atividades:listar_atividades_academicas")

@login_required
def detalhar_atividade_academica(request, id):
    """Exibe detalhes de uma atividade acadêmica."""
    try:
        models = get_models()
        AtividadeAcademica = models['AtividadeAcademica']
        
        atividade = get_object_or_404(
            AtividadeAcademica.objects.select_related(
                "curso").prefetch_related("turmas"),
            id=id
        )
        
        return render(
            request, 
            "atividades/academicas/detalhar_atividade_academica.html", 
            {"atividade": atividade}
        )
    except Exception as e:
        logger.error(
            f"Erro ao detalhar atividade acadêmica {id}: {str(e)}", 
            exc_info=True
        )
        messages.error(
            request, 
            f"Ocorreu um erro ao exibir os detalhes da atividade: {str(e)}"
        )
        return redirect("atividades:listar_atividades_academicas")

@login_required
def excluir_atividade_academica(request, id):
    """Exclui uma atividade acadêmica."""
    try:
        models = get_models()
        AtividadeAcademica = models['AtividadeAcademica']
        
        atividade = get_object_or_404(AtividadeAcademica, id=id)
        
        if request.method == "POST":
            atividade.delete()
            messages.success(
                request, 
                "Atividade acadêmica excluída com sucesso!"
            )
            return redirect("atividades:listar_atividades_academicas")
        
        return render(
            request, 
            "atividades/academicas/excluir_atividade_academica.html", 
            {"atividade": atividade}
        )
    except Exception as e:
        logger.error(
            f"Erro ao excluir atividade acadêmica {id}: {str(e)}", 
            exc_info=True
        )
        messages.error(
            request, 
            f"Ocorreu um erro ao excluir a atividade: {str(e)}"
        )
        return redirect("atividades:listar_atividades_academicas")

@login_required
def confirmar_exclusao_academica(request, pk):
    """Função para confirmar a exclusão de uma atividade acadêmica."""
    try:
        AtividadeAcademica = get_model_class("AtividadeAcademica")
        atividade = get_object_or_404(AtividadeAcademica, pk=pk)
        return_url = request.GET.get(
            "return_url", 
            reverse("atividades:listar_atividades_academicas")
        )
        
        if request.method == "POST":
            try:
                nome_atividade = atividade.nome  # Guardar o nome para a mensagem
                atividade.delete()
                messages.success(
                    request, 
                    f"Atividade acadêmica '{nome_atividade}' excluída com sucesso."
                )
                return redirect(return_url)
            except (AtividadeAcademica.DoesNotExist, ValueError) as e:
                logger.error(
                    f"Erro ao excluir atividade acadêmica: {str(e)}", 
                    exc_info=True
                )
                messages.error(
                    request, 
                    f"Erro ao excluir atividade acadêmica: {str(e)}"
                )
                return redirect("atividades:detalhar_atividade_academica", pk=pk)
        
        return render(
            request,
            "atividades/confirmar_exclusao_academica.html",
            {"atividade": atividade, "return_url": return_url},
        )
    except Exception as e:
        logger.error(
            f"Erro ao processar confirmação de exclusão: {str(e)}", 
            exc_info=True
        )
        messages.error(
            request, 
            f"Ocorreu um erro ao processar a solicitação: {str(e)}"
        )
        return redirect("atividades:listar_atividades_academicas")

@login_required
def copiar_atividade_academica(request, id):
    """Cria uma cópia de uma atividade acadêmica existente."""
    try:
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
                        frequencias_originais = Frequencia.objects.filter(
                            atividade=atividade_original
                        )
                        
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
                            f"Atividade copiada com sucesso! "
                            f"{frequencias_originais.count()} registros de "
                            f"frequência foram copiados."
                        )
                    except (ImportError, AttributeError, ValueError, TypeError) as e:
                        logger.error(
                            "Erro ao copiar frequências: %s", 
                            str(e), 
                            exc_info=True
                        )
                        messages.warning(
                            request,
                            f"Atividade copiada, mas ocorreu um erro ao copiar "
                            f"as frequências: {str(e)}"
                        )
                else:
                    messages.success(request, "Atividade copiada com sucesso!")
                
                return redirect(
                    "atividades:detalhar_atividade_academica",
                    id=nova_atividade.id
                )
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
                'status': 'PENDENTE',  # Sempre começa como pendente
                'curso': atividade_original.curso_id,
            }
            form = AtividadeAcademicaForm(initial=initial_data)
            # Para M2M, setar manualmente:
            form.fields['turmas'].initial = atividade_original.turmas.all()
        
        return render(
            request,
            "atividades/academicas/copiar_atividade_academica.html",
            {
                "form": form,
                "atividade_original": atividade_original,
            },
        )
    except (ImportError, AttributeError, ValueError) as e:
        logger.error(
            "Erro ao copiar atividade acadêmica %s: %s",
            id,
            str(e),
            exc_info=True
        )
        messages.error(
            request,
            f"Ocorreu um erro ao copiar a atividade: {str(e)}"
        )
        return redirect("atividades:listar_atividades_academicas")
    except ObjectDoesNotExist as e:
        logger.error(
            "Objeto não encontrado ao copiar atividade acadêmica %s: %s",
            id,
            str(e),
            exc_info=True
        )
        messages.error(
            request,
            f"Atividade acadêmica não encontrada: {str(e)}"
        )
        return redirect("atividades:listar_atividades_academicas")

@login_required
def alunos_por_turma(request, turma_id):
    """Retorna os alunos de uma turma em formato JSON."""
    try:
        Matricula = import_module("matriculas.models").Matricula
        alunos = Matricula.objects.filter(
            turma_id=turma_id
        ).select_related('aluno')
        
        data = [
            {
                "nome": m.aluno.nome,
                "foto": m.aluno.foto.url if m.aluno.foto else None,
                "cpf": m.aluno.cpf,
            }
            for m in alunos
        ]
        
        return JsonResponse(data, safe=False)
    except Exception as e:
        logger.error(
            "Erro ao obter alunos da turma %s: %s", 
            turma_id, 
            str(e),
            exc_info=True
        )
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def api_get_turmas_por_curso(request):
    """API para obter turmas por curso."""
    try:
        curso_id = request.GET.get("curso_id")
        
        models = get_models()
        Turma = models['Turma']
        
        if curso_id:
            try:
                # Validar que o curso_id é um inteiro válido
                curso_id = int(curso_id)
                turmas = Turma.objects.filter(curso_id=curso_id)
            except ValueError:
                return JsonResponse(
                    {
                        "error": "ID do curso inválido. Deve ser um número inteiro."
                    },
                    status=400
                )
        else:
            turmas = Turma.objects.all()
        
        # Serializar manualmente sem depender do REST Framework
        data = [
            {
                "id": turma.id,
                "nome": turma.nome,
                "codigo": turma.codigo if hasattr(turma, 'codigo') else None,
            }
            for turma in turmas
        ]
        
        return JsonResponse({"turmas": data})
    except Exception as e:
        logger.error(
            "Erro ao obter turmas por curso: %s", 
            str(e), 
            exc_info=True
        )
        return JsonResponse(
            {
                "error": "Erro ao processar a solicitação. Tente novamente."
            },
            status=500
        )

@login_required
def api_get_cursos_por_turma(request):
    """API para obter cursos por turma."""
    try:
        turma_id = request.GET.get("turma_id")
        
        if not turma_id:
            models = get_models()
            Curso = models['Curso']
            cursos = Curso.objects.all()
            
            # Serializar manualmente sem depender do REST Framework
            data = [
                {
                    "id": curso.id,
                    "nome": curso.nome,
                    "codigo_curso": (
                        curso.codigo_curso 
                        if hasattr(curso, 'codigo_curso') 
                        else None
                    ),
                }
                for curso in cursos
            ]
            
            return JsonResponse({"cursos": data})
        
        try:
            # Validar que o turma_id é um inteiro válido
            turma_id = int(turma_id)
        except ValueError:
            return JsonResponse(
                {
                    "error": "ID da turma inválido. Deve ser um número inteiro."
                },
                status=400
            )
        
        models = get_models()
        Turma = models['Turma']
        
        try:
            turma = Turma.objects.get(id=turma_id)
            curso = turma.curso
            
            if curso:
                data = {
                    "id": curso.id,
                    "nome": curso.nome,
                    "codigo_curso": (
                        curso.codigo_curso 
                        if hasattr(curso, 'codigo_curso') 
                        else None
                    ),
                }
                return JsonResponse({"cursos": [data]})
            else:
                return JsonResponse({"cursos": []})
        except Turma.DoesNotExist:
            return JsonResponse(
                {"error": "Turma não encontrada."},
                status=404
            )
    except Exception as e:
        logger.error(
            "Erro ao obter cursos por turma: %s", 
            str(e), 
            exc_info=True
        )
        return JsonResponse(
            {
                "error": "Erro ao processar a solicitação. Tente novamente."
            },
            status=500
        )