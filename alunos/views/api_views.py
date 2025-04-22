"""
Views relacionadas a endpoints de API.
"""
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
import logging
import traceback

from ..utils import get_aluno_model
from ..services import verificar_elegibilidade_instrutor

logger = logging.getLogger(__name__)

@login_required
def search_alunos(request):
    """API endpoint para buscar alunos."""
    try:
        query = request.GET.get("q", "")
        if len(query) < 2:
            return JsonResponse([], safe=False)
        
        Aluno = get_aluno_model()
        # Buscar alunos por nome, CPF ou número iniciático
        alunos = Aluno.objects.filter(
            Q(nome__icontains=query)
            | Q(cpf__icontains=query)
            | Q(numero_iniciatico__icontains=query)
        )[:10]  # Limitar a 10 resultados
        
        # Formatar resultados
        results = []
        for aluno in alunos:
            results.append({
                "cpf": aluno.cpf,
                "nome": aluno.nome,
                "numero_iniciatico": aluno.numero_iniciatico or "N/A",
                "foto": aluno.foto.url if hasattr(aluno, "foto") and aluno.foto else None,
                "situacao": aluno.get_situacao_display() if hasattr(aluno, "get_situacao_display") else ""
            })
        return JsonResponse(results, safe=False)
    except Exception as e:
        logger.error(f"Error in search_alunos: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def search_instrutores(request):
    """API endpoint para buscar alunos elegíveis para serem instrutores."""
    try:
        query = request.GET.get("q", "")
        Aluno = get_aluno_model()
        # Buscar apenas alunos ativos
        alunos = Aluno.objects.filter(situacao="ATIVO")
        
        # Se houver uma consulta, filtrar por ela
        if query and len(query) >= 2:
            alunos = alunos.filter(
                Q(nome__icontains=query)
                | Q(cpf__icontains=query)
                | Q(numero_iniciatico__icontains=query)
            )
        
        # Filtrar alunos que podem ser instrutores
        alunos_elegiveis = []
        for aluno in alunos[:10]:  # Limitar a 10 resultados
            # Buscar matrículas do aluno
            matriculas = []
            try:
                from importlib import import_module
                Matricula = import_module("matriculas.models").Matricula
                matriculas_obj = Matricula.objects.filter(aluno=aluno)
                matriculas = [f"{m.turma.curso.nome} ({m.turma.nome})" for m in matriculas_obj]
            except (ImportError, AttributeError):
                pass
            
            # Verificar se o aluno pode ser instrutor
            pode_ser_instrutor = getattr(aluno, 'pode_ser_instrutor', False)
            
            alunos_elegiveis.append({
                "cpf": aluno.cpf,
                "nome": aluno.nome,
                "numero_iniciatico": aluno.numero_iniciatico or "N/A",
                "foto": aluno.foto.url if hasattr(aluno, "foto") and aluno.foto else None,
                "situacao": aluno.get_situacao_display(),
                "situacao_codigo": aluno.situacao,
                "esta_ativo": aluno.esta_ativo,
                "matriculas": matriculas,
                "elegivel": pode_ser_instrutor
            })
        
        logger.info(f"Alunos elegíveis para instrutores: {len(alunos_elegiveis)}")
        return JsonResponse(alunos_elegiveis, safe=False)
    except Exception as e:
        logger.error(f"Erro em search_instrutores: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def get_aluno(request, cpf):
    """API endpoint para obter dados de um aluno específico."""
    try:
        Aluno = get_aluno_model()
        aluno = get_object_or_404(Aluno, cpf=cpf)
        return JsonResponse(
            {
                "success": True,
                "aluno": {
                    "cpf": aluno.cpf,
                    "nome": aluno.nome,
                    "numero_iniciatico": aluno.numero_iniciatico or "N/A",
                    "foto": (
                        aluno.foto.url
                        if hasattr(aluno, "foto") and aluno.foto
                        else None
                    ),
                },
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=404)

@login_required
@permission_required('alunos.view_aluno', raise_exception=True)
def verificar_elegibilidade_instrutor_api(request, cpf):
    """API endpoint para verificar se um aluno pode ser instrutor."""
    try:
        # Configurar logging
        logger.info(f"Verificando elegibilidade do instrutor com CPF: {cpf}")
        
        Aluno = get_aluno_model()
        aluno = get_object_or_404(Aluno, cpf=cpf)
        
        # Usar o serviço para verificar elegibilidade
        resultado = verificar_elegibilidade_instrutor(aluno)
        return JsonResponse(resultado)
        
    except Exception as e:
        error_msg = str(e)
        stack_trace = traceback.format_exc()
        logger.error(f"Erro ao verificar elegibilidade: {error_msg}")
        logger.error(f"Traceback: {stack_trace}")
        return JsonResponse(
            {"elegivel": False, "motivo": f"Erro na busca: {error_msg}"},
            status=500
        )