"""Camada de serviços dedicada ao histórico iniciático dos alunos."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Iterable

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from alunos.models import Aluno, Codigo, RegistroHistorico

logger = logging.getLogger("alunos.services.historico")


class HistoricoValidationError(ValidationError):
    """Erro de validação específico da camada de histórico."""


@dataclass(slots=True)
class HistoricoEventoDados:
    """Estrutura padronizada para criação de eventos no histórico."""

    tipo_codigo_id: int | None = None
    codigo_id: int | None = None
    data_os: date | None = None
    ordem_servico: str | None = None
    observacoes: str | None = None
    origem: str = "manual"
    usuario_responsavel: Any | None = None


class HistoricoService:
    """Orquestra operações relacionadas ao histórico dos alunos.

    Métodos públicos centralizam regras de negócio e atualizam o cache JSON
    do modelo ``Aluno`` quando necessário. Todas as validações relevantes são
    agregadas aqui para permitir reuso por views, APIs e comandos de migração.
    """

    @staticmethod
    def listar(
        aluno: Aluno, *, incluir_inativos: bool = False
    ) -> Iterable[RegistroHistorico]:
        """Retorna os registros históricos do aluno ordenados por data.

        Args:
            aluno (Aluno): Instância de aluno com ``pk`` definido.
            incluir_inativos (bool): Quando ``True`` retorna registros com ``ativo=False``.

        Returns:
            Iterable[RegistroHistorico]: Queryset otimizada para iteração.

        Raises:
            HistoricoValidationError: Caso o aluno seja inválido.
        """

        if not isinstance(aluno, Aluno) or not getattr(aluno, "pk", None):
            raise HistoricoValidationError("Aluno inválido ou não persistido.")

        queryset = RegistroHistorico.objects.filter(aluno=aluno)
        if not incluir_inativos:
            queryset = queryset.filter(ativo=True)

        return queryset.select_related("codigo", "codigo__tipo_codigo").order_by(
            "-data_os", "-created_at"
        )

    @staticmethod
    def converter_evento_legado(
        evento: Mapping[str, Any],
        *,
        cache_codigos: dict[str, int] | None = None,
    ) -> HistoricoEventoDados:
        """Converte um evento legado (JSON) em estrutura compatível com o service.

        Args:
            evento (Mapping[str, Any]): Evento extraído de ``historico_iniciatico``.
            cache_codigos (dict[str, int] | None): Cache opcional para evitar lookups
                repetidos de códigos.

        Returns:
            HistoricoEventoDados: Estrutura pronta para ser consumida por
            ``criar_evento``.

        Raises:
            HistoricoValidationError: Quando o evento possui dados insuficientes.
        """

        if not isinstance(evento, Mapping):
            raise HistoricoValidationError(
                {"evento": ["Estrutura inválida recebida para migração."]}
            )

        dados_brutos = {chave.lower(): valor for chave, valor in evento.items()}
        data_os = HistoricoService._interpretar_data(
            dados_brutos.get("data") or dados_brutos.get("data_os")
        )

        if data_os is None:
            raise HistoricoValidationError(
                {"data_os": ["Não foi possível interpretar a data do evento legado."]}
            )

        ordem_servico_raw = dados_brutos.get("ordem_servico") or dados_brutos.get(
            "ordemservico"
        )
        ordem_servico = (
            str(ordem_servico_raw).strip() or None
            if ordem_servico_raw is not None
            else None
        )

        observacoes_raw = dados_brutos.get("observacoes") or dados_brutos.get(
            "observacao"
        )
        observacoes = (
            str(observacoes_raw).strip() or None
            if observacoes_raw is not None
            else None
        )

        codigo_id = HistoricoService._resolver_codigo_legado(
            dados_brutos, cache_codigos=cache_codigos
        )

        return HistoricoEventoDados(
            codigo_id=codigo_id,
            data_os=data_os,
            ordem_servico=ordem_servico,
            observacoes=observacoes,
            origem="migracao-json",
        )

    @staticmethod
    def criar_evento(
        aluno: Aluno, dados: HistoricoEventoDados | dict[str, Any]
    ) -> RegistroHistorico:
        """Cria um novo registro histórico aplicando validações de negócio.

        Args:
            aluno (Aluno): Aluno alvo do registro.
            dados (HistoricoEventoDados | dict): Estrutura com os campos necessários.

        Returns:
            RegistroHistorico: Registro criado e sincronizado com o cache JSON.

        Raises:
            HistoricoValidationError: Se os dados estiverem inconsistentes.
        """

        if not isinstance(aluno, Aluno) or not getattr(aluno, "pk", None):
            raise HistoricoValidationError("Aluno inválido ou não persistido.")

        payload = HistoricoService._coagir_payload(dados)
        ordem_servico = HistoricoService._validar_payload(aluno, payload)

        codigo = HistoricoService._resolver_codigo(payload)
        observacoes_normalizadas = (payload.observacoes or "").strip() or None

        with transaction.atomic():
            registro = RegistroHistorico.objects.create(
                aluno=aluno,
                codigo=codigo,
                data_os=payload.data_os,
                ordem_servico=ordem_servico,
                observacoes=observacoes_normalizadas,
            )

            HistoricoService._sincronizar_cache(aluno)

        logger.info(
            "Registro histórico criado para aluno %s (codigo=%s, data=%s, ordem=%s)",
            getattr(aluno, "id", aluno.pk),
            codigo.id,
            payload.data_os,
            ordem_servico,
        )

        return registro

    @staticmethod
    def desativar_evento(
        registro: RegistroHistorico,
        *,
        motivo: str | None = None,
        atualizar_cache: bool = True,
    ) -> RegistroHistorico:
        """Realiza soft delete de um evento e sincroniza o cache JSON.

        Args:
            registro (RegistroHistorico): Registro a ser desativado.
            motivo (str | None): Texto opcional a ser anexado nas observações.
            atualizar_cache (bool): Se ``True`` sincroniza o campo JSON do aluno.

        Returns:
            RegistroHistorico: Instância atualizada.

        Raises:
            HistoricoValidationError: Quando o registro não é válido.
        """

        if not isinstance(registro, RegistroHistorico) or not getattr(
            registro, "pk", None
        ):
            raise HistoricoValidationError(
                "Registro histórico inválido ou não persistido."
            )

        if not registro.ativo and motivo is None:
            return registro

        registro.ativo = False

        if motivo:
            marcador = f"[Inativado {timezone.now().date():%Y-%m-%d}] {motivo.strip()}"
            texto_atual = registro.observacoes or ""
            registro.observacoes = f"{texto_atual}\n{marcador}".strip()

        registro.save(update_fields=["ativo", "observacoes"])

        if atualizar_cache:
            HistoricoService._sincronizar_cache(registro.aluno)

        return registro

    @staticmethod
    def reativar_evento(
        registro: RegistroHistorico, atualizar_cache: bool = True
    ) -> RegistroHistorico:
        """Reativa um evento previamente desativado.

        Args:
            registro (RegistroHistorico): Registro alvo da reativação.
            atualizar_cache (bool): Se ``True`` reprocessa o JSON do aluno.

        Returns:
            RegistroHistorico: Instância atualizada.

        Raises:
            HistoricoValidationError: Quando o registro é inválido.
        """

        if not isinstance(registro, RegistroHistorico) or not getattr(
            registro, "pk", None
        ):
            raise HistoricoValidationError(
                "Registro histórico inválido ou não persistido."
            )

        if registro.ativo:
            return registro

        registro.ativo = True
        registro.save(update_fields=["ativo"])

        if atualizar_cache:
            HistoricoService._sincronizar_cache(registro.aluno)

        return registro

    @staticmethod
    def _coagir_payload(
        dados: HistoricoEventoDados | dict[str, Any],
    ) -> HistoricoEventoDados:
        """Garante que o payload esteja no formato dataclass esperado."""

        if isinstance(dados, HistoricoEventoDados):
            return dados

        if not isinstance(dados, dict):
            raise HistoricoValidationError(
                "Estrutura de dados inválida para criação do histórico."
            )

        return HistoricoEventoDados(
            tipo_codigo_id=dados.get("tipo_codigo_id"),
            codigo_id=dados.get("codigo_id"),
            data_os=dados.get("data_os"),
            ordem_servico=dados.get("ordem_servico"),
            observacoes=dados.get("observacoes"),
            origem=dados.get("origem", "manual"),
            usuario_responsavel=dados.get("usuario_responsavel"),
        )

    @staticmethod
    def _validar_payload(aluno: Aluno, payload: HistoricoEventoDados) -> str | None:
        """Executa validações de negócio antes da criação do registro."""

        erros: dict[str, list[str]] = {}
        ordem_normalizada: str | None = None

        if not payload.codigo_id and not payload.tipo_codigo_id:
            erros.setdefault("codigo_id", []).append(
                "Informe um código válido para o registro."
            )

        if payload.data_os is None:
            erros.setdefault("data_os", []).append(
                "Informe uma data para a ordem de serviço."
            )

        if payload.data_os and payload.data_os > date.today():
            erros.setdefault("data_os", []).append(
                "A data da ordem de serviço não pode estar no futuro."
            )

        if payload.ordem_servico:
            try:
                ordem_normalizada = HistoricoService._normalizar_ordem_servico(
                    payload.ordem_servico
                )
            except HistoricoValidationError as exc:
                erros.setdefault("ordem_servico", []).extend(exc.messages)

        if ordem_normalizada and payload.codigo_id:
            duplicado = RegistroHistorico.objects.filter(
                aluno=aluno,
                codigo_id=payload.codigo_id,
                ordem_servico=ordem_normalizada,
            ).exists()
            if duplicado:
                erros.setdefault("ordem_servico", []).append(
                    "Já existe um registro com este código e ordem de serviço."
                )

        if erros:
            raise HistoricoValidationError(erros)

        return ordem_normalizada

    @staticmethod
    def _resolver_codigo(payload: HistoricoEventoDados) -> Codigo:
        """Resolve a instância de ``Codigo`` a partir do payload."""

        if payload.codigo_id:
            try:
                return Codigo.objects.get(pk=payload.codigo_id)
            except Codigo.DoesNotExist as exc:
                raise HistoricoValidationError(
                    {"codigo_id": ["Código não encontrado."]}
                ) from exc

        raise HistoricoValidationError({"codigo_id": ["Código não informado."]})

    @staticmethod
    def _normalizar_ordem_servico(valor: str | None) -> str | None:
        """Normaliza a ordem de serviço para o padrão ``XXXX/AAAA``."""

        if not valor:
            return None

        texto = str(valor).strip()
        if not texto:
            return None

        import re

        match = re.match(r"^(\S+)/(\d{2,4})$", texto)
        if not match:
            raise HistoricoValidationError(["Formato inválido. Use PREFIXO/ANO."])

        prefixo, ano = match.groups()
        if len(ano) == 2:
            ano_int = int(ano)
            ano = f"20{ano}" if ano_int < 50 else f"19{ano}"
        else:
            ano_int = int(ano)
            if ano_int < 1900 or ano_int > 2100:
                raise HistoricoValidationError(
                    ["Ano inválido informado na ordem de serviço."]
                )

        return f"{prefixo}/{ano}"

    @staticmethod
    def _sincronizar_cache(aluno: Aluno) -> None:
        """Sincroniza o cache JSON do aluno utilizando o helper legado."""

        from . import sincronizar_historico_iniciatico

        sincronizar_historico_iniciatico(aluno)

    @staticmethod
    def _interpretar_data(valor: Any) -> date | None:
        """Tenta converter diferentes representações de data em ``date``."""

        if valor is None:
            return None

        if isinstance(valor, date) and not isinstance(valor, datetime):
            return valor

        if isinstance(valor, datetime):
            return valor.date()

        if not isinstance(valor, str):
            return None

        texto = valor.strip()
        if not texto:
            return None

        formatos = (
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%Y/%m/%d",
            "%d-%m-%Y",
        )

        for formato in formatos:
            try:
                return datetime.strptime(texto, formato).date()
            except ValueError:
                continue

        try:
            return datetime.fromisoformat(texto).date()
        except ValueError:
            return None

    @staticmethod
    def _resolver_codigo_legado(
        dados_brutos: Mapping[str, Any],
        *,
        cache_codigos: dict[str, int] | None = None,
    ) -> int:
        """Resolve o identificador de ``Codigo`` a partir de um evento legado."""

        codigo_id = dados_brutos.get("codigo_id") or dados_brutos.get("codigo")
        if codigo_id:
            try:
                codigo = Codigo.objects.get(pk=int(codigo_id))
            except (Codigo.DoesNotExist, ValueError) as exc:
                raise HistoricoValidationError(
                    {"codigo_id": ["Código informado não encontrado."]}
                ) from exc
            return codigo.id

        descricao = (
            dados_brutos.get("descricao") or dados_brutos.get("titulo") or ""
        ).strip()
        tipo_nome = (dados_brutos.get("tipo") or "").strip()

        if not descricao:
            raise HistoricoValidationError(
                {
                    "codigo_id": [
                        "Evento legado não possui descrição/código identificável."
                    ]
                }
            )

        cache = cache_codigos if cache_codigos is not None else {}
        chave_cache = f"{tipo_nome.lower()}::{descricao.lower()}"
        if chave_cache in cache:
            return cache[chave_cache]

        consulta = Codigo.objects.filter(nome__iexact=descricao)
        if tipo_nome:
            consulta = consulta.filter(tipo_codigo__nome__iexact=tipo_nome)

        codigo = consulta.first()
        if codigo is None:
            raise HistoricoValidationError(
                {
                    "codigo_id": [
                        f"Código '{descricao}' não localizado no cadastro atual."
                    ]
                }
            )

        cache[chave_cache] = codigo.id
        return codigo.id
