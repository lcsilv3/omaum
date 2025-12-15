from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Q
from django.db import DatabaseError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import logging
import unicodedata
import requests

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


@require_GET
@login_required
def buscar_cep(request, cep):
    """
    Busca dados de endereço via CEP usando a API ViaCEP.
    
    Args:
        request: HttpRequest
        cep: CEP com ou sem formatação (ex: 65000-000 ou 65000000)
    
    Returns:
        JsonResponse com dados do endereço ou erro
    """
    from alunos.models import Estado, Cidade, Bairro
    
    # Remove formatação do CEP
    cep_limpo = ''.join(filter(str.isdigit, cep))
    
    if len(cep_limpo) != 8:
        return JsonResponse(
            {"success": False, "error": "CEP inválido. Deve conter 8 dígitos."},
            status=400
        )
    
    try:
        # Busca dados na API ViaCEP
        response = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/", timeout=5)
        
        if response.status_code != 200:
            logger.error(f"Erro ao buscar CEP {cep_limpo}: status {response.status_code}")
            return JsonResponse(
                {"success": False, "error": "Erro ao consultar API de CEP."},
                status=500
            )
        
        dados_cep = response.json()
        
        # Verifica se CEP foi encontrado
        if dados_cep.get("erro"):
            return JsonResponse(
                {"success": False, "error": "CEP não encontrado."},
                status=404
            )
        
        # Busca o estado no banco
        uf = dados_cep.get("uf", "")
        estado = Estado.objects.filter(codigo=uf).first()
        
        if not estado:
            logger.warning(f"Estado não encontrado para UF: {uf}")
            return JsonResponse(
                {"success": False, "error": f"Estado {uf} não encontrado no banco de dados."},
                status=404
            )
        
        # Busca a cidade no banco usando código IBGE
        codigo_ibge_cidade = dados_cep.get("ibge", "")
        cidade = None
        
        if codigo_ibge_cidade:
            cidade = Cidade.objects.filter(codigo_ibge=codigo_ibge_cidade).first()
        
        # Se não encontrou por código IBGE, busca por nome + estado
        if not cidade:
            nome_cidade = dados_cep.get("localidade", "")
            cidade = Cidade.objects.filter(
                nome__iexact=nome_cidade,
                estado=estado
            ).first()
        
        if not cidade:
            logger.warning(f"Cidade não encontrada: {dados_cep.get('localidade')} - {uf}")
            return JsonResponse(
                {
                    "success": False,
                    "error": f"Cidade {dados_cep.get('localidade')} não encontrada no banco de dados."
                },
                status=404
            )
        
        # Busca ou cria o bairro
        nome_bairro = dados_cep.get("bairro", "").strip()
        bairro = None
        bairro_criado = False
        
        if nome_bairro:
            bairro = Bairro.objects.filter(
                nome__iexact=nome_bairro,
                cidade=cidade
            ).first()
            
            # Se bairro não existe, cria automaticamente
            if not bairro:
                try:
                    bairro = Bairro.objects.create(
                        nome=nome_bairro,
                        cidade=cidade
                    )
                    bairro_criado = True
                    logger.info(f"Bairro criado automaticamente via CEP: {nome_bairro} - {cidade.nome}/{uf}")
                except Exception as e:
                    logger.error(f"Erro ao criar bairro via CEP: {e}")
        
        # Monta resposta
        resultado = {
            "success": True,
            "cep": cep_limpo,
            "logradouro": dados_cep.get("logradouro", ""),
            "complemento": dados_cep.get("complemento", ""),
            "bairro": nome_bairro,
            "cidade": dados_cep.get("localidade", ""),
            "uf": uf,
            "estado_id": estado.id,
            "cidade_id": cidade.id,
            "bairro_id": bairro.id if bairro else None,
            "bairro_criado": bairro_criado,
        }
        
        logger.info(f"CEP {cep_limpo} consultado com sucesso")
        return JsonResponse(resultado)
        
    except requests.Timeout:
        logger.error(f"Timeout ao buscar CEP {cep_limpo}")
        return JsonResponse(
            {"success": False, "error": "Timeout ao consultar API de CEP. Tente novamente."},
            status=504
        )
    except requests.RequestException as e:
        logger.error(f"Erro de requisição ao buscar CEP {cep_limpo}: {e}")
        return JsonResponse(
            {"success": False, "error": "Erro ao conectar com a API de CEP."},
            status=500
        )
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar CEP {cep_limpo}: {e}")
        return JsonResponse(
            {"success": False, "error": "Erro inesperado ao processar CEP."},
            status=500
        )


@require_POST
@login_required
def criar_bairro(request):
    """
    Cria um novo bairro no banco de dados.
    
    Espera JSON com:
    - nome: Nome do bairro
    - cidade_id: ID da cidade
    
    Returns:
        JsonResponse com dados do bairro criado ou erro
    """
    from alunos.models import Bairro, Cidade
    import json
    
    try:
        dados = json.loads(request.body)
        nome_bairro = dados.get("nome", "").strip()
        cidade_id = dados.get("cidade_id")
        
        if not nome_bairro:
            return JsonResponse(
                {"success": False, "error": "Nome do bairro é obrigatório."},
                status=400
            )
        
        if not cidade_id:
            return JsonResponse(
                {"success": False, "error": "Cidade é obrigatória."},
                status=400
            )
        
        # Verifica se a cidade existe
        try:
            cidade = Cidade.objects.get(id=cidade_id)
        except Cidade.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Cidade não encontrada."},
                status=404
            )
        
        # Verifica se o bairro já existe
        bairro_existente = Bairro.objects.filter(
            nome__iexact=nome_bairro,
            cidade=cidade
        ).first()
        
        if bairro_existente:
            return JsonResponse(
                {
                    "success": True,
                    "bairro_id": bairro_existente.id,
                    "nome": bairro_existente.nome,
                    "cidade_nome": cidade.nome,
                    "estado_codigo": cidade.estado.codigo,
                    "ja_existia": True,
                    "message": "Bairro já existe no banco de dados."
                }
            )
        
        # Cria o novo bairro
        novo_bairro = Bairro.objects.create(
            nome=nome_bairro,
            cidade=cidade
        )
        
        logger.info(f"Bairro criado: {nome_bairro} - {cidade.nome}/{cidade.estado.codigo}")
        
        return JsonResponse(
            {
                "success": True,
                "bairro_id": novo_bairro.id,
                "nome": novo_bairro.nome,
                "cidade_nome": cidade.nome,
                "estado_codigo": cidade.estado.codigo,
                "ja_existia": False,
                "message": "Bairro criado com sucesso."
            }
        )
        
    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "error": "JSON inválido."},
            status=400
        )
    except Exception as e:
        logger.error(f"Erro ao criar bairro: {e}")
        return JsonResponse(
            {"success": False, "error": f"Erro ao criar bairro: {str(e)}"},
            status=500
        )
