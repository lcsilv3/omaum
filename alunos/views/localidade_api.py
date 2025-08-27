from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
from django.db import DatabaseError
from django.contrib.auth.decorators import login_required
import logging
import unicodedata

logger = logging.getLogger(__name__)


def _strip_accents(s: str) -> str:
    if not isinstance(s, str):
        return s
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    ).lower()


@require_GET
@login_required
def search_paises(request):
    """API para buscar países por nome ou nacionalidade."""
    from alunos.models import Pais

    query = request.GET.get("q", "").strip()
    if len(query) < 2:
        return JsonResponse([], safe=False)
    try:
        paises = Pais.objects.filter(
            Q(nome__icontains=query) | Q(nacionalidade__icontains=query), ativo=True
        ).order_by("nome")[:10]
    except DatabaseError as e:  # pragma: no cover
        logger.error(f"Erro DB países: {e}")
        return JsonResponse({"error": "Erro de banco."}, status=500)

    results = [
        {
            "id": p.id,
            "codigo": p.codigo,
            "nome": p.nome,
            "nacionalidade": p.nacionalidade,
            "display": f"{p.nome} ({p.nacionalidade})",
        }
        for p in paises
    ]
    return JsonResponse(results, safe=False)


@require_GET
@login_required
def search_estados(request):
    """API para buscar estados brasileiros."""
    from alunos.models import Estado

    query = request.GET.get("q", "").strip()
    if len(query) < 1:
        return JsonResponse([], safe=False)
    try:
        estados = Estado.objects.filter(
            Q(nome__icontains=query) | Q(codigo__icontains=query)
        ).order_by("nome")[:10]
    except DatabaseError as e:  # pragma: no cover
        logger.error(f"Erro DB estados: {e}")
        return JsonResponse({"error": "Erro de banco."}, status=500)
    if not estados:
        q_norm = _strip_accents(query)
        estados = [
            e
            for e in Estado.objects.all().order_by("nome")
            if q_norm in _strip_accents(e.nome) or q_norm in e.codigo.lower()
        ][:10]

    results = [
        {
            "id": e.id,
            "codigo": e.codigo,
            "nome": e.nome,
            "regiao": e.regiao,
            "display": f"{e.nome} ({e.codigo})",
        }
        for e in estados
    ]
    return JsonResponse(results, safe=False)


@require_GET
@login_required
def search_cidades(request):
    """API para buscar cidades por nome e opcionalmente por estado."""
    from alunos.models import Cidade

    query = request.GET.get("q", "").strip()
    estado_id = request.GET.get("estado_id")
    if len(query) < 2:
        return JsonResponse([], safe=False)
    try:
        cidades_qs = Cidade.objects.select_related("estado").filter(
            nome__icontains=query
        )
        if estado_id:
            cidades_qs = cidades_qs.filter(estado_id=estado_id)
        cidades = list(cidades_qs.order_by("nome")[:15])
    except DatabaseError as e:  # pragma: no cover
        logger.error(f"Erro DB cidades: {e}")
        return JsonResponse({"error": "Erro de banco."}, status=500)
    if not cidades:
        q_norm = _strip_accents(query)
        cidades = [
            c
            for c in Cidade.objects.select_related("estado").all()
            if q_norm in _strip_accents(c.nome)
        ][:15]
    results = [
        {
            "id": c.id,
            "nome": c.nome,
            "estado_id": c.estado.id,
            "estado_nome": c.estado.nome,
            "estado_codigo": c.estado.codigo,
            "codigo_ibge": c.codigo_ibge,
            "display": f"{c.nome} - {c.estado.codigo}",
            "nome_completo": c.nome_completo,
        }
        for c in cidades
    ]
    return JsonResponse(results, safe=False)


@require_GET
@login_required
def get_cidades_por_estado(request, estado_id):
    """API para obter todas as cidades de um estado específico."""
    from alunos.models import Cidade

    try:
        cidades = Cidade.objects.filter(estado_id=estado_id).order_by("nome")
    except DatabaseError as e:  # pragma: no cover
        logger.error(f"Erro DB cidades por estado: {e}")
        return JsonResponse({"error": "Erro de banco."}, status=500)
    results = [
        {
            "id": c.id,
            "nome": c.nome,
            "codigo_ibge": c.codigo_ibge,
            "display": c.nome,
        }
        for c in cidades
    ]
    return JsonResponse(results, safe=False)


@require_GET
@login_required
def search_bairros(request):
    """API para buscar bairros por nome e opcionalmente por cidade."""
    from alunos.models import Bairro

    query = request.GET.get("q", "").strip()
    cidade_id = request.GET.get("cidade_id")
    if len(query) < 2:
        return JsonResponse([], safe=False)
    try:
        bairros = Bairro.objects.select_related("cidade", "cidade__estado").filter(
            nome__icontains=query
        )
        if cidade_id:
            bairros = bairros.filter(cidade_id=cidade_id)
        bairros = bairros.order_by("nome")[:15]
    except DatabaseError as e:  # pragma: no cover
        logger.error(f"Erro DB bairros: {e}")
        return JsonResponse({"error": "Erro de banco."}, status=500)
    if not bairros:
        q_norm = _strip_accents(query)
        bairros = [
            b
            for b in Bairro.objects.select_related("cidade", "cidade__estado").all()
            if q_norm in _strip_accents(b.nome)
        ][:15]
    results = [
        {
            "id": b.id,
            "nome": b.nome,
            "cidade_id": b.cidade.id,
            "cidade_nome": b.cidade.nome,
            "estado_codigo": b.cidade.estado.codigo,
            "display": f"{b.nome} - {b.cidade.nome}/{b.cidade.estado.codigo}",
        }
        for b in bairros
    ]
    return JsonResponse(results, safe=False)


@require_GET
@login_required
def get_bairros_por_cidade(request, cidade_id):
    """API para obter todos os bairros de uma cidade específica."""
    from alunos.models import Bairro

    try:
        bairros = Bairro.objects.filter(cidade_id=cidade_id).order_by("nome")
    except DatabaseError as e:  # pragma: no cover
        logger.error(f"Erro DB bairros por cidade: {e}")
        return JsonResponse({"error": "Erro de banco."}, status=500)
    results = [{"id": b.id, "nome": b.nome, "display": b.nome} for b in bairros]
    return JsonResponse(results, safe=False)
