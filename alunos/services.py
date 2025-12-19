"""Serviços de negócio e utilidades do aplicativo de Alunos."""

from __future__ import annotations

import json
import logging
import re
from copy import deepcopy
from datetime import datetime
from hashlib import sha256
from importlib import import_module
from typing import Any, Iterable, Mapping, MutableMapping, Sequence

from django.core.files.base import ContentFile
from django.db import IntegrityError, transaction
from django.db.models import Q, QuerySet
from django.utils import timezone

from alunos.models import Aluno, RegistroHistorico

try:  # pragma: no cover - fallback quando requests não estiver instalado
    import requests
except ImportError:  # pragma: no cover
    requests = None


logger = logging.getLogger("alunos.services")

CPF_REGEX = re.compile(r"\d{11}")
DEFAULT_EMAIL_DOMAIN = "alunos.omaum.edu.br"

__all__ = [
    "buscar_aluno_por_id",
    "buscar_aluno_por_cpf",
    "buscar_alunos_por_nome_ou_cpf",
    "listar_alunos",
    "listar_alunos_para_relatorio",
    "listar_historico_aluno",
    "criar_aluno",
    "sincronizar_historico_iniciatico",
    "reconciliar_historico_if_divergente",
    "InstrutorService",
    "_calcular_checksum",
]


def _normalizar_cpf(valor: str | None) -> str:
    """Remove caracteres não numéricos e valida a estrutura básica do CPF."""

    if not valor:
        return ""
    somente_digitos = re.sub(r"\D", "", str(valor))
    if CPF_REGEX.fullmatch(somente_digitos):
        return somente_digitos
    return ""


def _normalizar_situacao(valor: str | None) -> str:
    """Normaliza o código de situação para os valores aceitos pelo modelo."""

    if not valor:
        return "a"

    mapeamento = {
        "ativo": "a",
        "a": "a",
        "desligado": "d",
        "d": "d",
        "falecido": "f",
        "f": "f",
        "excluido": "e",
        "excluído": "e",
        "e": "e",
    }
    valor_normalizado = mapeamento.get(str(valor).strip().lower())
    return valor_normalizado or "a"


def _gerar_email_padrao(nome: str | None) -> str:
    """Gera um e-mail institucional plausível a partir do nome."""

    if not nome:
        slug = f"aluno-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        return f"{slug}@{DEFAULT_EMAIL_DOMAIN}"

    slug = re.sub(r"[^a-z0-9]", ".", nome.lower())
    slug = re.sub(r"\.+", ".", slug).strip(".")
    slug = slug or "aluno"
    return f"{slug}@{DEFAULT_EMAIL_DOMAIN}"


def _gerar_numero_iniciatico(cpf: str) -> str:
    """Gera um número iniciático único com base no CPF e timestamp."""

    base = cpf[-6:] if CPF_REGEX.fullmatch(cpf) else re.sub(r"\D", "", cpf)[:6]
    base = base or timezone.now().strftime("%H%M%S")
    candidato = f"{timezone.now().strftime('%y%m%d')}{base}"[-12:]

    while Aluno.objects.filter(numero_iniciatico=candidato).exists():
        candidato = f"{timezone.now().strftime('%y%m%d%H%M%S%f')}"[-12:]
    return candidato


def _converter_eventos(
    eventos: Iterable[Mapping[str, Any]] | None,
) -> list[dict[str, Any]]:
    """Normaliza uma coleção de eventos de histórico para JSON serializável."""

    if not eventos:
        return []

    eventos_normalizados: list[dict[str, Any]] = []
    for evento in eventos:
        if not isinstance(evento, Mapping):  # pragma: no cover - sanitização defensiva
            continue
        data_valor = evento.get("data")
        if isinstance(data_valor, datetime):
            data_normalizada = data_valor.date().isoformat()
        else:
            data_normalizada = str(data_valor) if data_valor else None
        eventos_normalizados.append(
            {
                "tipo": evento.get("tipo", ""),
                "descricao": evento.get("descricao", ""),
                "data": data_normalizada,
                "observacoes": evento.get("observacoes", ""),
                "ordem_servico": evento.get("ordem_servico", ""),
                "codigo_id": evento.get("codigo_id"),
                "registrado_em": evento.get("registrado_em"),
            }
        )

    return sorted(
        eventos_normalizados,
        key=lambda item: (item.get("data") or "", item.get("ordem_servico") or ""),
        reverse=True,
    )


def buscar_aluno_por_id(aluno_id: int | str | None) -> Aluno | None:
    """Recupera um aluno pelo identificador primário."""

    if not aluno_id:
        return None

    try:
        return Aluno.objects.get(pk=aluno_id)
    except Aluno.DoesNotExist:
        return None


def buscar_aluno_por_cpf(cpf: str | None) -> Aluno | None:
    """Busca um aluno pelo CPF, tratando formatação e ausência."""

    cpf_normalizado = _normalizar_cpf(cpf)
    if not cpf_normalizado:
        return None

    try:
        return Aluno.objects.get(cpf=cpf_normalizado)
    except Aluno.DoesNotExist:
        return None


def buscar_alunos_por_nome_ou_cpf(
    termo: str | None, limite: int = 20
) -> QuerySet[Aluno]:
    """Busca alunos por nome, CPF ou número iniciático."""

    if not termo:
        return Aluno.objects.none()

    termo_limpo = termo.strip()
    cpf_normalizado = _normalizar_cpf(termo_limpo)

    filtros = Q(nome__icontains=termo_limpo) | Q(email__icontains=termo_limpo)
    filtros |= Q(numero_iniciatico__icontains=termo_limpo)
    if cpf_normalizado:
        filtros |= Q(cpf__icontains=cpf_normalizado)

    return (
        Aluno.objects.filter(filtros)
        .select_related("pais_nacionalidade", "cidade_ref", "bairro_ref")
        .order_by("nome")[:limite]
    )


def listar_alunos(
    query: str | None = None,
    curso_id: int | str | None = None,
    apenas_ativos: bool | None = None,
) -> QuerySet[Aluno]:
    """Lista alunos com filtros opcionais para buscas e dashboards."""

    alunos = Aluno.objects.all().select_related(
        "pais_nacionalidade",
        "cidade_ref",
        "bairro_ref",
    )

    if apenas_ativos is True:
        alunos = alunos.filter(situacao="a")
    elif apenas_ativos is False:
        alunos = alunos.filter(~Q(situacao="a"))

    if query:
        termo = query.strip()
        cpf_normalizado = _normalizar_cpf(termo)
        filtros = (
            Q(nome__icontains=termo)
            | Q(email__icontains=termo)
            | Q(numero_iniciatico__icontains=termo)
        )
        if cpf_normalizado:
            filtros |= Q(cpf__icontains=cpf_normalizado)
        alunos = alunos.filter(filtros)

    if curso_id:
        try:
            Matricula = import_module("matriculas.models").Matricula
            alunos = alunos.filter(matriculas__turma__curso_id=curso_id)
        except ModuleNotFoundError:
            logger.warning(
                "Aplicativo 'matriculas' indisponível ao filtrar alunos por curso."
            )
        except Exception:  # pragma: no cover - diagnóstico defensivo
            logger.exception(
                "Erro inesperado ao filtrar alunos por curso.",
            )

    return alunos.order_by("nome").distinct()


def listar_alunos_para_relatorio(
    aluno_id: int | None = None,
    turma_id: int | None = None,
    curso_id: int | None = None,
    situacao: str | None = None,
) -> QuerySet[Aluno]:
    """Retorna uma queryset otimizada para geração de relatórios."""

    queryset = Aluno.objects.all()

    if aluno_id:
        queryset = queryset.filter(id=aluno_id)
    if turma_id:
        queryset = queryset.filter(matriculas__turma_id=turma_id)
    if curso_id:
        queryset = queryset.filter(matriculas__turma__curso_id=curso_id)
    if situacao:
        queryset = queryset.filter(situacao=_normalizar_situacao(situacao))

    return queryset.select_related("pais_nacionalidade").distinct().order_by("nome")


def listar_historico_aluno(
    aluno: Aluno, *, incluir_inativos: bool = False
) -> QuerySet[RegistroHistorico]:
    """Retorna a queryset de registros históricos ordenada e otimizada."""

    registros = RegistroHistorico.objects.filter(aluno=aluno)
    if not incluir_inativos:
        registros = registros.filter(ativo=True)  # RegistroHistorico TEM campo ativo

    return registros.select_related("codigo", "codigo__tipo_codigo").order_by(
        "-data_os", "-created_at"
    )


def criar_aluno(
    dados: Mapping[str, Any],
    *,
    foto_url: str | None = None,
    eventos_historico: Iterable[Mapping[str, Any]] | None = None,
) -> Aluno | None:
    """Cria um aluno no banco garantindo consistência mínima de dados."""

    if not isinstance(dados, Mapping):
        raise TypeError("dados deve ser um mapping com os atributos do aluno")

    dados_limpos: MutableMapping[str, Any] = deepcopy(dict(dados))
    cpf = _normalizar_cpf(dados_limpos.get("cpf"))
    if not cpf:
        raise ValueError("CPF inválido ou não informado para criação do aluno")

    email = dados_limpos.get("email") or _gerar_email_padrao(dados_limpos.get("nome"))
    situacao = _normalizar_situacao(dados_limpos.get("situacao"))
    numero_iniciatico = dados_limpos.get("numero_iniciatico")
    numero_iniciatico = numero_iniciatico or _gerar_numero_iniciatico(cpf)

    if Aluno.objects.filter(Q(cpf=cpf) | Q(email=email)).exists():
        logger.warning("Tentativa de criar aluno com CPF/E-mail duplicado: %s", cpf)
        return None

    dados_limpos.update(
        {
            "cpf": cpf,
            "email": email,
            "situacao": situacao,
            "numero_iniciatico": numero_iniciatico,
        }
    )
    dados_limpos.setdefault("ativo", True)

    eventos_iniciais = eventos_historico or dados_limpos.pop(
        "historico_iniciatico", None
    )

    try:
        with transaction.atomic():
            aluno = Aluno.objects.create(**dados_limpos)

            if eventos_iniciais:
                eventos_normalizados = _converter_eventos(eventos_iniciais)
                aluno.historico_iniciatico = eventos_normalizados
                aluno.historico_checksum = _calcular_checksum(eventos_normalizados)
                aluno.save(
                    update_fields=[
                        "historico_iniciatico",
                        "historico_checksum",
                        "updated_at",
                    ]
                )

    except IntegrityError:
        logger.warning("Violação de integridade ao criar aluno %s", cpf)
        return None
    except Exception:  # pragma: no cover - tratamento defensivo
        logger.exception("Erro inesperado ao criar aluno %s", cpf)
        return None

    if foto_url:
        _atribuir_foto_remota(aluno, foto_url)

    return aluno


def _atribuir_foto_remota(aluno: Aluno, foto_url: str) -> None:
    """Baixa e associa uma foto remota ao aluno quando possível."""

    if not requests:
        logger.debug("Biblioteca requests indisponível; não é possível baixar foto.")
        return

    try:
        resposta = requests.get(foto_url, timeout=5)
        resposta.raise_for_status()
    except Exception:  # pragma: no cover - ambiente pode não ter acesso externo
        logger.warning("Não foi possível baixar a foto do aluno em %s", foto_url)
        return

    nome_arquivo = f"{aluno.cpf}_foto.jpg"
    aluno.foto.save(nome_arquivo, ContentFile(resposta.content), save=True)


def _calcular_checksum(eventos: Sequence[Mapping[str, Any]] | None) -> str:
    """Calcula o checksum SHA256 do histórico normalizado."""

    if not eventos:
        return ""

    json_normalizado = json.dumps(
        list(eventos),
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return sha256(json_normalizado.encode("utf-8")).hexdigest()


def _coletar_eventos_registro(aluno: Aluno) -> list[dict[str, Any]]:
    """Transforma registros estruturados em eventos JSON serializáveis."""

    registros = (
        RegistroHistorico.objects.filter(aluno=aluno, ativo=True)  # RegistroHistorico TEM campo ativo
        .select_related("codigo", "codigo__tipo_codigo")
        .order_by("-data_os", "-created_at")
    )

    eventos: list[dict[str, Any]] = []
    for registro in registros:
        codigo = registro.codigo
        tipo_codigo = getattr(codigo, "tipo_codigo", None)
        eventos.append(
            {
                "tipo": getattr(tipo_codigo, "nome", ""),
                "descricao": getattr(codigo, "nome", ""),
                "data": registro.data_os.isoformat() if registro.data_os else None,
                "observacoes": registro.observacoes or "",
                "ordem_servico": registro.ordem_servico or "",
                "codigo_id": registro.codigo_id,
                "registrado_em": registro.created_at.isoformat()
                if registro.created_at
                else None,
            }
        )

    return eventos


def sincronizar_historico_iniciatico(aluno: Aluno) -> list[dict[str, Any]]:
    """Sincroniza o JSONField com os registros estruturados do histórico."""

    eventos = _converter_eventos(_coletar_eventos_registro(aluno))
    checksum = _calcular_checksum(eventos)

    aluno.historico_iniciatico = eventos
    aluno.historico_checksum = checksum
    aluno.save(
        update_fields=["historico_iniciatico", "historico_checksum", "updated_at"]
    )

    return eventos


def reconciliar_historico_if_divergente(aluno: Aluno) -> list[dict[str, Any]]:
    """Reconstrói o histórico quando checksum salvo e calculado divergem."""

    historico_atual = (
        list(aluno.historico_iniciatico)
        if isinstance(aluno.historico_iniciatico, Iterable)
        else []
    )
    checksum_atual = _calcular_checksum(historico_atual)
    checksum_salvo = aluno.historico_checksum or ""

    eventos_registro = _converter_eventos(_coletar_eventos_registro(aluno))
    checksum_registro = _calcular_checksum(eventos_registro)

    if checksum_registro == checksum_atual == checksum_salvo:
        return historico_atual

    aluno.historico_iniciatico = eventos_registro
    aluno.historico_checksum = checksum_registro
    aluno.save(
        update_fields=["historico_iniciatico", "historico_checksum", "updated_at"]
    )

    return eventos_registro


class InstrutorService:
    """Serviços de negócio relacionados à atuação de alunos como instrutores."""

    @staticmethod
    def remover_de_turmas(
        aluno: Aluno | None, nova_situacao: str | None = None
    ) -> dict:
        """Remove o aluno de turmas em que atua como instrutor ou auxiliar."""

        if aluno is None:
            return {
                "sucesso": False,
                "mensagem": "Aluno não informado para remoção das turmas.",
                "turmas_afetadas": 0,
            }

        try:
            Turma = import_module("turmas.models").Turma
        except ModuleNotFoundError:
            logger.exception("Aplicativo de turmas não está disponível.")
            return {
                "sucesso": False,
                "mensagem": "Aplicativo de turmas indisponível no momento.",
                "turmas_afetadas": 0,
            }

        campos_instrutor = ("instrutor", "instrutor_auxiliar", "auxiliar_instrucao")
        turmas_afetadas = 0

        try:
            with transaction.atomic():
                for campo in campos_instrutor:
                    filtros = {campo: aluno}
                    turmas_afetadas += Turma.objects.filter(**filtros).update(
                        **{campo: None}
                    )

            mensagem = (
                "Aluno removido de {quantidade} atribuição(ões) como instrutor.".format(
                    quantidade=turmas_afetadas
                )
                if turmas_afetadas
                else "Aluno não estava vinculado como instrutor em turmas ativas."
            )

            if nova_situacao:
                logger.info(
                    "Aluno %s definido para nova situação '%s' após remoção das turmas.",
                    getattr(aluno, "cpf", aluno.pk),
                    nova_situacao,
                )

            return {
                "sucesso": True,
                "mensagem": mensagem,
                "turmas_afetadas": turmas_afetadas,
            }
        except Exception as exc:  # pragma: no cover - caminho defensivo
            logger.exception("Erro ao remover o aluno das turmas como instrutor.")
            return {
                "sucesso": False,
                "mensagem": f"Erro ao remover aluno como instrutor: {exc}",
                "turmas_afetadas": turmas_afetadas,
            }

    @staticmethod
    def verificar_elegibilidade_completa(aluno: Aluno | None) -> dict[str, Any]:
        """Analisa elegibilidade de um aluno para atuar como instrutor."""

        if aluno is None:
            return {
                "elegivel": False,
                "motivo": "Aluno não localizado.",
                "pendencias": ["Registro de aluno inexistente."],
            }

        pendencias: list[str] = []
        situacao = str(getattr(aluno, "situacao", "")).lower()
        esta_ativo = situacao in {"a", "ativo"} or getattr(aluno, "esta_ativo", False)

        if not esta_ativo:
            pendencias.append("Aluno não está marcado como ativo.")
        if not getattr(aluno, "numero_iniciatico", ""):
            pendencias.append("Número iniciático não informado.")
        if not getattr(aluno, "email", ""):
            pendencias.append("E-mail não cadastrado.")
        if not getattr(aluno, "pode_ser_instrutor", False):
            pendencias.append("Regras básicas de elegibilidade do aluno não atendidas.")

        try:
            Turma = import_module("turmas.models").Turma
            turmas_com_alerta = Turma.objects.filter(
                Q(instrutor=aluno)
                | Q(instrutor_auxiliar=aluno)
                | Q(auxiliar_instrucao=aluno)
            ).filter(alerta_instrutor=True, status="A")  # BUG FIX: apenas turmas ativas
            if turmas_com_alerta.exists():
                pendencias.append("Aluno possui alertas ativos em turmas.")
        except ModuleNotFoundError:
            logger.warning(
                "Aplicativo de turmas não disponível durante verificação de elegibilidade."
            )
        except Exception:  # pragma: no cover - diagnóstico defensivo
            logger.exception(
                "Falha ao verificar turmas do aluno durante análise de elegibilidade."
            )
            pendencias.append(
                "Não foi possível validar vínculos do aluno com turmas no momento."
            )

        elegivel = len(pendencias) == 0
        motivo = (
            "Aluno elegível para atuar como instrutor." if elegivel else pendencias[0]
        )

        return {
            "elegivel": elegivel,
            "motivo": motivo,
            "pendencias": pendencias,
        }
