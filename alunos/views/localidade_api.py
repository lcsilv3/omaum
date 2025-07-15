from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)


@require_GET
@login_required
def search_paises(request):
    """API para buscar países por nome ou nacionalidade."""
    try:
        from alunos.models import Pais

        query = request.GET.get("q", "").strip()
        if len(query) < 2:
            return JsonResponse([], safe=False)

        paises = Pais.objects.filter(
            Q(nome__icontains=query) | Q(nacionalidade__icontains=query), ativo=True
        ).order_by("nome")[:10]

        results = []
        for pais in paises:
            results.append(
                {
                    "id": pais.id,
                    "codigo": pais.codigo,
                    "nome": pais.nome,
                    "nacionalidade": pais.nacionalidade,
                    "display": f"{pais.nome} ({pais.nacionalidade})",
                }
            )

        return JsonResponse(results, safe=False)
    except Exception as e:
        logger.error(f"Erro ao buscar países: {e}")
        return JsonResponse({"error": str(e)}, status=500)


@require_GET
@login_required
def search_estados(request):
    """API para buscar estados brasileiros."""
    try:
        from alunos.models import Estado

        query = request.GET.get("q", "").strip()
        if len(query) < 1:
            return JsonResponse([], safe=False)

        estados = Estado.objects.filter(
            Q(nome__icontains=query) | Q(codigo__icontains=query)
        ).order_by("nome")[:10]

        results = []
        for estado in estados:
            results.append(
                {
                    "id": estado.id,
                    "codigo": estado.codigo,
                    "nome": estado.nome,
                    "regiao": estado.regiao,
                    "display": f"{estado.nome} ({estado.codigo})",
                }
            )

        return JsonResponse(results, safe=False)
    except Exception as e:
        logger.error(f"Erro ao buscar estados: {e}")
        return JsonResponse({"error": str(e)}, status=500)


@require_GET
@login_required
def search_cidades(request):
    """API para buscar cidades por nome e opcionalmente por estado."""
    try:
        from alunos.models import Cidade

        query = request.GET.get("q", "").strip()
        estado_id = request.GET.get("estado_id")

        if len(query) < 2:
            return JsonResponse([], safe=False)

        cidades = Cidade.objects.select_related("estado").filter(nome__icontains=query)

        if estado_id:
            cidades = cidades.filter(estado_id=estado_id)

        cidades = cidades.order_by("nome")[:15]

        results = []
        for cidade in cidades:
            results.append(
                {
                    "id": cidade.id,
                    "nome": cidade.nome,
                    "estado_id": cidade.estado.id,
                    "estado_nome": cidade.estado.nome,
                    "estado_codigo": cidade.estado.codigo,
                    "codigo_ibge": cidade.codigo_ibge,
                    "display": f"{cidade.nome} - {cidade.estado.codigo}",
                    "nome_completo": cidade.nome_completo,
                }
            )

        return JsonResponse(results, safe=False)
    except Exception as e:
        logger.error(f"Erro ao buscar cidades: {e}")
        return JsonResponse({"error": str(e)}, status=500)


@require_GET
@login_required
def get_cidades_por_estado(request, estado_id):
    """API para obter todas as cidades de um estado específico."""
    try:
        from alunos.models import Cidade

        cidades = Cidade.objects.filter(estado_id=estado_id).order_by("nome")

        results = []
        for cidade in cidades:
            results.append(
                {
                    "id": cidade.id,
                    "nome": cidade.nome,
                    "codigo_ibge": cidade.codigo_ibge,
                    "display": cidade.nome,
                }
            )

        return JsonResponse(results, safe=False)
    except Exception as e:
        logger.error(f"Erro ao buscar cidades do estado: {e}")
        return JsonResponse({"error": str(e)}, status=500)
