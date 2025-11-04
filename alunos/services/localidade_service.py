"""Serviço híbrido de resolução de localidades.

Fluxo resumido:
- consulta dados locais via modelos normalizados;
- se ausentes e ambiente permitir, consulta provedores externos (IBGE/ViaCEP);
- persiste os novos registros localmente e registra `LocalidadeFaltante` para auditoria;
- pode responder imediatamente com ``{'status': 'pending'}`` enquanto uma thread de
    background efetua a sincronização.
"""

import logging
from threading import Thread

import requests
from django.apps import apps
from django.conf import settings
from django.core.cache import cache
from django.db import IntegrityError, transaction

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = getattr(settings, "LOCALIDADES_REMOTE_TIMEOUT", 5)
PROVIDERS = (
    getattr(
        settings,
        "LOCALIDADES_REMOTE_PROVIDERS",
        ["viacep", "ibge"],
    )
    or []
)
ALLOW_REMOTE = getattr(settings, "LOCALIDADES_ALLOW_REMOTE", True)


def _cache_key(prefix, pk):
    return f"localidades:{prefix}:{pk}"


def _get_model(model_name):
    """Retorna dinamicamente o modelo solicitado do app `alunos`."""

    return apps.get_model("alunos", model_name)


def _persist_cidades(estado, cidades_data):
    """Persiste uma lista de dicionários com chaves 'nome' e opcional 'codigo_ibge'"""
    created = []
    CidadeModel = _get_model("Cidade")
    with transaction.atomic():
        for c in cidades_data:
            nome = c.get("nome") or c.get("municipio") or c.get("nome_municipio")
            codigo = c.get("codigo_ibge") or c.get("id") or None
            cidade_obj, _ = CidadeModel.objects.get_or_create(
                nome=nome,
                estado=estado,
                defaults={"codigo_ibge": str(codigo) if codigo else None},
            )
            created.append({"id": cidade_obj.id, "nome": cidade_obj.nome})
    return created


def _persist_bairros(cidade, bairros_data):
    """Persiste uma lista de bairros para a cidade informada."""

    created = []
    BairroModel = _get_model("Bairro")
    with transaction.atomic():
        for bairro in bairros_data:
            nome = bairro.get("nome") or bairro.get("bairro")
            if not nome:
                continue
            codigo_externo = bairro.get("codigo_ibge") or bairro.get("id") or None
            bairro_obj, _ = BairroModel.objects.get_or_create(
                nome=nome,
                cidade=cidade,
                defaults={
                    "codigo_externo": str(codigo_externo) if codigo_externo else None
                },
            )
            created.append({"id": bairro_obj.id, "nome": bairro_obj.nome})
    return created


def _fetch_cidades_from_ibge(estado_sigla):
    """Tenta obter municípios do IBGE usando a sigla do estado.
    Retorna lista de dicts com 'nome' e opcional 'id'"""
    try:
        # Primeiro, tentar endpoint direto (algumas impls aceitam sigla)
        url = (
            "https://servicodados.ibge.gov.br/api/v1/localidades/estados/"
            f"{estado_sigla}/municipios"
        )
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)
        if response.ok:
            data = response.json()
            return [{"nome": item.get("nome"), "id": item.get("id")} for item in data]
        # Fallback: listar estados e buscar por sigla para então pedir por ID
        response_estados = requests.get(
            "https://servicodados.ibge.gov.br/api/v1/localidades/estados",
            timeout=DEFAULT_TIMEOUT,
        )
        if response_estados.ok:
            estados = response_estados.json()
            match = next(
                (estado for estado in estados if estado.get("sigla") == estado_sigla),
                None,
            )
            if match:
                uid = match.get("id")
                url_uid = (
                    "https://servicodados.ibge.gov.br/api/v1/localidades/estados/"
                    f"{uid}/municipios"
                )
                response_por_uid = requests.get(url_uid, timeout=DEFAULT_TIMEOUT)
                if response_por_uid.ok:
                    data = response_por_uid.json()
                    return [
                        {"nome": item.get("nome"), "id": item.get("id")}
                        for item in data
                    ]
    except requests.RequestException as exc:
        logger.exception("Erro ao consultar IBGE: %s", exc)
    return []


def _fetch_bairros_from_ibge(cidade_ibge_id):
    """Placeholder para futura integração com API de bairros do IBGE."""

    del cidade_ibge_id
    return []


def _fetch_from_viacep_by_cep(cep):
    try:
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)
        if response.ok:
            return response.json()
    except requests.RequestException as exc:
        logger.exception("Erro ao consultar ViaCEP: %s", exc)
    return None


def get_cidades_por_estado(estado_id, async_when_remote=True):
    """Retorna lista de cidades locais; se vazio e remoto permitido, dispara fetch remoto.
    Se async_when_remote=True, inicia thread de background e retorna {'status':'pending'}.
    Caso contrário, faz fetch síncrono e retorna lista (possivelmente vazia).
    """
    cache_key = _cache_key("cidades", estado_id)
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    EstadoModel = _get_model("Estado")
    try:
        estado = EstadoModel.objects.get(pk=estado_id)
    except EstadoModel.DoesNotExist:  # type: ignore[attr-defined]
        return []

    qs = estado.cidades.all().values("id", "nome")
    results = list(qs)
    if results:
        cache.set(cache_key, results, timeout=60 * 60 * 24)
        return results

    # Não há dados locais
    if not ALLOW_REMOTE:
        return []

    # Registrar tentativa pendente
    chave = f"estado:{estado.codigo}"
    LocalidadeFaltanteModel = _get_model("LocalidadeFaltante")
    faltante, _ = LocalidadeFaltanteModel.objects.get_or_create(
        chave=chave,
        defaults={
            "provedor": ",".join(PROVIDERS),
            "parametros": {"estado_codigo": estado.codigo},
            "status": "pending",
        },
    )
    if faltante.status != "pending":
        faltante.status = "pending"
    faltante.parametros = {"estado_codigo": estado.codigo}
    faltante.provedor = ",".join(PROVIDERS)
    faltante.save(update_fields=["status", "parametros", "provedor", "updated_at"])

    def background_fetch():
        try:
            # tentar IBGE primeiro
            cidades_data = []
            if "ibge" in PROVIDERS:
                cidades_data = _fetch_cidades_from_ibge(estado.codigo)
            # persistir
            if cidades_data:
                created = _persist_cidades(estado, cidades_data)
                faltante.resultado_cache = {"created": created}
                faltante.status = "success"
                faltante.tentativas += 1
                faltante.save(
                    update_fields=[
                        "resultado_cache",
                        "status",
                        "tentativas",
                        "updated_at",
                    ]
                )
                cache.set(cache_key, created, timeout=60 * 60 * 24)
                return
            # se nada encontrado, marcar erro
            faltante.status = "error"
            faltante.tentativas += 1
            faltante.save(update_fields=["status", "tentativas", "updated_at"])
        except IntegrityError as exc:
            logger.exception("Erro no background_fetch de cidades: %s", exc)
            faltante.status = "error"
            faltante.tentativas += 1
            faltante.save(update_fields=["status", "tentativas", "updated_at"])

    if async_when_remote:
        Thread(target=background_fetch, daemon=True).start()
        return {"status": "pending"}

    # Caso for síncrono
    cidades_data = []
    if "ibge" in PROVIDERS:
        cidades_data = _fetch_cidades_from_ibge(estado.codigo)
    if cidades_data:
        created = _persist_cidades(estado, cidades_data)
        cache.set(cache_key, created, timeout=60 * 60 * 24)
        return created
    return []


def get_bairros_por_cidade(cidade_id, async_when_remote=True):
    cache_key = _cache_key("bairros", cidade_id)
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    CidadeModel = _get_model("Cidade")
    try:
        cidade = CidadeModel.objects.get(pk=cidade_id)
    except CidadeModel.DoesNotExist:  # type: ignore[attr-defined]
        return []

    qs = cidade.bairros.all().values("id", "nome")
    results = list(qs)
    if results:
        cache.set(cache_key, results, timeout=60 * 60 * 24)
        return results

    if not ALLOW_REMOTE:
        return []

    chave = f"cidade:{cidade.id}"
    LocalidadeFaltanteModel = _get_model("LocalidadeFaltante")
    faltante, _ = LocalidadeFaltanteModel.objects.get_or_create(
        chave=chave,
        defaults={
            "provedor": ",".join(PROVIDERS),
            "parametros": {"cidade_nome": cidade.nome},
            "status": "pending",
        },
    )
    if faltante.status != "pending":
        faltante.status = "pending"
    faltante.parametros = {"cidade_nome": cidade.nome}
    faltante.provedor = ",".join(PROVIDERS)
    faltante.save(update_fields=["status", "parametros", "provedor", "updated_at"])

    def registrar_sucesso(payload):
        faltante.resultado_cache = {"created": payload}
        faltante.status = "success"
        faltante.tentativas += 1
        faltante.save(
            update_fields=[
                "resultado_cache",
                "status",
                "tentativas",
                "updated_at",
            ]
        )

    def registrar_falha():
        faltante.status = "error"
        faltante.tentativas += 1
        faltante.save(update_fields=["status", "tentativas", "updated_at"])

    def background_fetch():
        try:
            bairros_data = []
            if "ibge" in PROVIDERS and getattr(cidade, "codigo_ibge", None):
                bairros_data = _fetch_bairros_from_ibge(cidade.codigo_ibge)
            if bairros_data:
                created = _persist_bairros(cidade, bairros_data)
                registrar_sucesso(created)
                cache.set(cache_key, created, timeout=60 * 60 * 24)
                return
            registrar_falha()
        except (requests.RequestException, IntegrityError) as exc:
            logger.exception("Erro no background_fetch de bairros: %s", exc)
            registrar_falha()

    if async_when_remote:
        Thread(target=background_fetch, daemon=True).start()
        return {"status": "pending"}

    bairros_data = []
    if "ibge" in PROVIDERS and getattr(cidade, "codigo_ibge", None):
        bairros_data = _fetch_bairros_from_ibge(cidade.codigo_ibge)
    if bairros_data:
        created = _persist_bairros(cidade, bairros_data)
        registrar_sucesso(created)
        cache.set(cache_key, created, timeout=60 * 60 * 24)
        return created
    registrar_falha()
    return []
