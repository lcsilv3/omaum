"""Serviços para o aplicativo alunos.

Contém a lógica de negócios complexa e utilitários relacionados ao histórico iniciático.
"""

import logging
from django.core.files.base import ContentFile

from django.utils import timezone
from django.db.models import Q  # Adicionado para resolver erro de variável indefinida
import requests  # Adicionado para resolver erro de variável indefinida
import hashlib
import json
from alunos.utils import (
    get_aluno_model,
    get_turma_model,
    get_matricula_model,
    get_atribuicao_cargo_model,
    get_registro_historico_model,
)
from alunos.models import (
    RegistroHistorico,
)  # Import base

# Modelos unificados em 'alunos' (app iniciaticos apenas reexporta).

# pylint: disable=redefined-outer-name

logger = logging.getLogger(__name__)


class InstrutorService:
    """Serviços relacionados à elegibilidade e gestão de instrutores."""

    @staticmethod
    def verificar_elegibilidade_completa(aluno):
        """
        Verifica se um aluno pode ser instrutor com validações completas.

        Args:
            aluno: Instância do modelo Aluno

        Returns:
            dict: Dicionário com chaves 'elegivel' (bool) e 'motivo' (str)
        """
        if aluno.situacao != "ATIVO":
            return {
                "elegivel": False,
                "motivo": (
                    f"O aluno não está ativo. Situação atual: "
                    f"{aluno.get_situacao_display()}"
                ),
            }

        if not hasattr(aluno, "pode_ser_instrutor"):
            return {
                "elegivel": False,
                "motivo": (
                    "Erro na verificação: o método 'pode_ser_instrutor' não existe."
                ),
            }

        try:
            pode_ser_instrutor = aluno.pode_ser_instrutor
            if not pode_ser_instrutor:
                matricula_model = get_matricula_model()
                if matricula_model:
                    matriculas_pre_iniciatico = matricula_model.objects.filter(
                        aluno=aluno, turma__curso__nome__icontains="Pré-iniciático"
                    )
                    if matriculas_pre_iniciatico.exists():
                        cursos = ", ".join(
                            [f"{m.turma.curso.nome}" for m in matriculas_pre_iniciatico]
                        )
                        return {
                            "elegivel": False,
                            "motivo": (
                                "O aluno está matriculado em cursos pré-iniciáticos: "
                                f"{cursos}"
                            ),
                        }
                return {
                    "elegivel": False,
                    "motivo": "O aluno não atende aos requisitos para ser instrutor.",
                }
            return {"elegivel": True}
        except Exception as exc:
            logger.error("Erro ao verificar elegibilidade do instrutor: %s", exc)
            return {
                "elegivel": False,
                "motivo": f"Erro ao verificar requisitos de instrutor: {exc}",
            }

    @staticmethod
    def remover_de_turmas(aluno, nova_situacao):
        """
        Remove um aluno de todas as turmas onde ele é instrutor.

        Args:
            aluno: Instância do modelo Aluno
            nova_situacao: Nova situação do aluno

        Returns:
            dict: Resultado da operação com chaves 'sucesso' e 'mensagem'
        """
        try:
            turma_model = get_turma_model()
            atribuicao_cargo_model = get_atribuicao_cargo_model()

            turmas_instrutor = turma_model.objects.filter(instrutor=aluno, status="A")
            turmas_instrutor_auxiliar = turma_model.objects.filter(
                instrutor_auxiliar=aluno, status="A"
            )
            turmas_auxiliar_instrucao = turma_model.objects.filter(
                auxiliar_instrucao=aluno, status="A"
            )

            for turma in turmas_instrutor:
                turma.instrutor = None
                turma.alerta_instrutor = True
                turma.alerta_mensagem = (
                    f"O instrutor {aluno.nome} foi removido devido à mudança de "
                    f"situação para '{aluno.get_situacao_display()}'."
                )
                turma.save()

                if atribuicao_cargo_model:
                    atribuicoes = atribuicao_cargo_model.objects.filter(
                        aluno=aluno,
                        cargo__nome__icontains="Instrutor Principal",
                        data_fim__isnull=True,
                    )
                    for atribuicao in atribuicoes:
                        atribuicao.data_fim = timezone.now().date()
                        atribuicao.save()

            for turma in turmas_instrutor_auxiliar:
                turma.instrutor_auxiliar = None
                turma.alerta_instrutor = True
                turma.alerta_mensagem = (
                    "O instrutor auxiliar "
                    f"{aluno.nome} foi removido devido à mudança de situação para "
                    f"'{aluno.get_situacao_display()}'."
                )
                turma.save()

                if atribuicao_cargo_model:
                    atribuicoes = atribuicao_cargo_model.objects.filter(
                        aluno=aluno,
                        cargo__nome__icontains="Instrutor Auxiliar",
                        data_fim__isnull=True,
                    )
                    for atribuicao in atribuicoes:
                        atribuicao.data_fim = timezone.now().date()
                        atribuicao.save()

            for turma in turmas_auxiliar_instrucao:
                turma.auxiliar_instrucao = None
                turma.alerta_instrutor = True
                turma.alerta_mensagem = (
                    "O auxiliar de instrução "
                    f"{aluno.nome} foi removido devido à mudança de situação para "
                    f"'{aluno.get_situacao_display()}'."
                )
                turma.save()

                if atribuicao_cargo_model:
                    atribuicoes = atribuicao_cargo_model.objects.filter(
                        aluno=aluno,
                        cargo__nome__icontains="Auxiliar de Instrução",
                        data_fim__isnull=True,
                    )
                    for atribuicao in atribuicoes:
                        atribuicao.data_fim = timezone.now().date()
                        atribuicao.save()

            total_turmas = (
                len(turmas_instrutor)
                + len(turmas_instrutor_auxiliar)
                + len(turmas_auxiliar_instrucao)
            )

            return {
                "sucesso": True,
                "mensagem": f"Aluno removido de {total_turmas} turmas com sucesso.",
            }

        except AttributeError as attr_err:
            logger.error(
                "Erro de atributo ao remover instrutor de turmas: %s", attr_err
            )
            return {"sucesso": False, "mensagem": f"Erro de atributo: {attr_err}"}
        except Exception as exc:
            logger.error("Erro inesperado ao remover instrutor de turmas: %s", exc)
            raise RuntimeError(
                "Erro inesperado ao remover instrutor de turmas"
            ) from exc


def verificar_elegibilidade_instrutor(aluno):
    """
    Verifica se um aluno pode ser instrutor.

    Args:
        aluno: Instância do modelo Aluno

    Returns:
        dict: Dicionário com chaves 'elegivel' (bool) e 'motivo' (str)
    """
    if aluno.situacao != "ATIVO":
        return {
            "elegivel": False,
            "motivo": (
                f"O aluno não está ativo. Situação atual: "
                f"{aluno.get_situacao_display()}"
            ),
        }

    if not hasattr(aluno, "pode_ser_instrutor"):
        return {
            "elegivel": False,
            "motivo": (
                "Erro na verificação: o método 'pode_ser_instrutor' não existe."
            ),
        }

    try:
        pode_ser_instrutor = aluno.pode_ser_instrutor

        if not pode_ser_instrutor:
            matricula_model = get_matricula_model()
            if matricula_model:
                matriculas_pre_iniciatico = matricula_model.objects.filter(
                    aluno=aluno, turma__curso__nome__icontains="Pré-iniciático"
                )

                if matriculas_pre_iniciatico.exists():
                    cursos = ", ".join(
                        [f"{m.turma.curso.nome}" for m in matriculas_pre_iniciatico]
                    )
                    return {
                        "elegivel": False,
                        "motivo": (
                            "O aluno está matriculado em cursos pré-iniciáticos: "
                            f"{cursos}"
                        ),
                    }

            return {
                "elegivel": False,
                "motivo": "O aluno não atende aos requisitos para ser instrutor.",
            }

        return {"elegivel": True}

    except Exception as exc:
        logger.error("Erro ao verificar elegibilidade do instrutor: %s", exc)
        return {
            "elegivel": False,
            "motivo": f"Erro ao verificar requisitos de instrutor: {exc}",
        }


def remover_instrutor_de_turmas(aluno, nova_situacao):
    """
    Remove um aluno de todas as turmas onde ele é instrutor.

    Args:
        aluno: Instância do modelo Aluno
        nova_situacao: Nova situação do aluno

    Returns:
        dict: Resultado da operação com chaves 'sucesso' e 'mensagem'
    """
    try:
        turma_model = get_turma_model()
        atribuicao_cargo_model = get_atribuicao_cargo_model()

        turmas_instrutor = turma_model.objects.filter(instrutor=aluno, status="A")
        turmas_instrutor_auxiliar = turma_model.objects.filter(
            instrutor_auxiliar=aluno, status="A"
        )
        turmas_auxiliar_instrucao = turma_model.objects.filter(
            auxiliar_instrucao=aluno, status="A"
        )

        for turma in turmas_instrutor:
            turma.instrutor = None
            turma.alerta_instrutor = True
            turma.alerta_mensagem = (
                f"O instrutor {aluno.nome} foi removido devido à mudança de "
                f"situação para '{aluno.get_situacao_display()}'."
            )
            turma.save()

            if atribuicao_cargo_model:
                atribuicoes = atribuicao_cargo_model.objects.filter(
                    aluno=aluno,
                    cargo__nome__icontains="Instrutor Principal",
                    data_fim__isnull=True,
                )
                for atribuicao in atribuicoes:
                    atribuicao.data_fim = timezone.now().date()
                    atribuicao.save()

        for turma in turmas_instrutor_auxiliar:
            turma.instrutor_auxiliar = None
            turma.alerta_instrutor = True
            turma.alerta_mensagem = (
                "O instrutor auxiliar "
                f"{aluno.nome} foi removido devido à mudança de situação para "
                f"'{aluno.get_situacao_display()}'."
            )
            turma.save()

            if atribuicao_cargo_model:
                atribuicoes = atribuicao_cargo_model.objects.filter(
                    aluno=aluno,
                    cargo__nome__icontains="Instrutor Auxiliar",
                    data_fim__isnull=True,
                )
                for atribuicao in atribuicoes:
                    atribuicao.data_fim = timezone.now().date()
                    atribuicao.save()

        for turma in turmas_auxiliar_instrucao:
            turma.auxiliar_instrucao = None
            turma.alerta_instrutor = True
            turma.alerta_mensagem = (
                "O auxiliar de instrução "
                f"{aluno.nome} foi removido devido à mudança de situação para "
                f"'{aluno.get_situacao_display()}'."
            )
            turma.save()

            if atribuicao_cargo_model:
                atribuicoes = atribuicao_cargo_model.objects.filter(
                    aluno=aluno,
                    cargo__nome__icontains="Auxiliar de Instrução",
                    data_fim__isnull=True,
                )
                for atribuicao in atribuicoes:
                    atribuicao.data_fim = timezone.now().date()
                    atribuicao.save()

        total_turmas = (
            len(turmas_instrutor)
            + len(turmas_instrutor_auxiliar)
            + len(turmas_auxiliar_instrucao)
        )

        return {
            "sucesso": True,
            "mensagem": f"Aluno removido de {total_turmas} turmas com sucesso.",
        }

    except AttributeError as attr_err:
        logger.error("Erro de atributo ao remover instrutor de turmas: %s", attr_err)
        return {"sucesso": False, "mensagem": f"Erro de atributo: {attr_err}"}
    except Exception as exc:
        logger.error("Erro inesperado ao remover instrutor de turmas: %s", exc)
        raise RuntimeError("Erro inesperado ao remover instrutor de turmas") from exc


def listar_alunos(query=None, curso_id=None):
    """
    Lista e filtra alunos com base na query e no curso.
    """
    from .repositories import AlunoRepository

    queryset = AlunoRepository.listar_com_filtros(query=query, curso_id=curso_id)

    logger.debug(
        "Query recebida: %s, Curso ID: %s, Resultados encontrados: %d",
        query,
        curso_id,
        queryset.count(),
    )

    return queryset


def buscar_aluno_por_cpf(cpf):
    """
    Busca um aluno pelo CPF.

    Args:
        cpf (str): O CPF do aluno a ser buscado.

    Returns:
        Aluno: A instância do aluno, ou None se não for encontrado.
    """
    Aluno = get_aluno_model()
    try:
        return Aluno.objects.get(cpf=cpf)
    except Aluno.DoesNotExist:
        return None


def buscar_alunos_por_nome_ou_cpf(query):
    """
    Busca alunos por nome ou CPF.

    Args:
        query (str): O termo de busca.

    Returns:
        QuerySet: Um queryset de alunos que correspondem à busca.
    """
    Aluno = get_aluno_model()
    cpf_query = "".join(filter(str.isdigit, query))
    return Aluno.objects.filter(Q(nome__icontains=query) | Q(cpf__icontains=cpf_query))


def buscar_aluno_por_email(email):
    """
    Busca um aluno pelo email.

    Args:
        email (str): O email do aluno a ser buscado.

    Returns:
        Aluno: A instância do aluno, ou None se não for encontrado.
    """
    Aluno = get_aluno_model()
    try:
        return Aluno.objects.get(email=email)
    except Aluno.DoesNotExist:
        return None


def criar_aluno(aluno_data, foto_url=None):
    """
    Cria um novo aluno com os dados fornecidos e, opcionalmente, uma foto.

    Args:
        aluno_data (dict): Dicionário com os dados do aluno (nome, email, cpf, etc.).
        foto_url (str, optional): URL da foto a ser baixada.

    Returns:
        Aluno: A instância do aluno criado, ou None em caso de erro.
    """
    Aluno = get_aluno_model()
    try:
        aluno = Aluno.objects.create(**aluno_data)

        if foto_url:
            try:
                response = requests.get(foto_url, stream=True, timeout=10)
                response.raise_for_status()
                file_name = f"{aluno_data['cpf']}_photo.jpg"
                aluno.foto.save(file_name, ContentFile(response.content), save=True)
            except requests.RequestException as e:
                logger.error("Erro ao realizar a requisição: %s", e)
                raise

        return aluno
    except Exception as e:
        logger.error("Erro ao criar o aluno %s: %s", aluno_data.get("nome"), e)
        return None


def listar_historico_aluno(aluno):
    """
    Retorna o histórico de registros (cargos, iniciações, punições) de um aluno.
    """
    RegistroHistorico = get_registro_historico_model()  # noqa: E1101
    return RegistroHistorico.objects.filter(aluno=aluno).order_by("-data_registro")


def criar_registro_historico(data, aluno):
    """Cria um registro histórico para o aluno."""
    data["aluno"] = aluno
    registro = RegistroHistorico.objects.create(**data)
    return registro


def atualizar_dados_aluno(aluno_id, dados):
    """
    Atualiza os dados de um aluno existente.

    Args:
        aluno_id (int): O ID do aluno a ser atualizado.
        dados (dict): Um dicionário contendo os novos dados do aluno.

    Returns:
        dict: Um dicionário contendo o status da operação e uma mensagem.
    """
    Aluno = get_aluno_model()
    try:
        aluno = Aluno.objects.get(id=aluno_id)
    except Aluno.DoesNotExist:
        return {
            "status": "erro",
            "mensagem": "Aluno não encontrado.",
        }

    # Atualiza os campos do aluno com os dados fornecidos
    for campo, valor in dados.items():
        setattr(aluno, campo, valor)

    aluno.save()

    logger.info(
        "Aluno %s foi atualizado com sucesso. Dados: %s",
        aluno_id,
        dados,
    )

    return {
        "status": "sucesso",
        "mensagem": "Dados do aluno atualizados com sucesso.",
    }


def listar_alunos_com_cache(query=None, curso_id=None, cache_timeout=300):
    """
    Lista alunos com cache básico para melhorar performance.

    Args:
        query: Termo de busca
        curso_id: ID do curso para filtrar
        cache_timeout: Tempo de cache em segundos

    Returns:
        QuerySet de alunos
    """
    from django.core.cache import cache

    # Gera chave de cache baseada nos parâmetros
    cache_key = f"alunos_lista_{query or 'all'}_{curso_id or 'all'}"

    # Tenta buscar no cache primeiro
    resultado = cache.get(cache_key)
    if resultado is not None:
        logger.debug(f"Cache hit para chave: {cache_key}")
        return resultado

    # Se não estiver no cache, busca no banco
    logger.debug(f"Cache miss para chave: {cache_key}")
    resultado = listar_alunos(query=query, curso_id=curso_id)

    # Salva no cache
    cache.set(cache_key, resultado, cache_timeout)

    return resultado


# ==============================================================
# Serviços de Histórico Iniciático (Fase 0 de refatoração)
# Centralizam criação/listagem/sincronização entre RegistroHistorico
# e o JSONField historico_iniciatico do Aluno.
# ==============================================================
from django.db import transaction, IntegrityError
from datetime import date, datetime


def _normalizar_data(valor):
    """Converte string (YYYY-MM-DD) ou datetime/date em date."""
    if isinstance(valor, date):
        return valor
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, str) and valor.strip():
        try:
            return datetime.strptime(valor[:10], "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Data inválida: {valor}") from None
    raise ValueError("Data não fornecida ou inválida")


def listar_eventos_iniciaticos(aluno, limite=None):
    """Retorna eventos do RegistroHistorico (ordenados) e aplica limite opcional."""
    RegistroHistorico = get_registro_historico_model()  # noqa
    qs = (
        RegistroHistorico.objects.filter(aluno=aluno, ativo=True)
        .select_related("codigo", "codigo__tipo_codigo")
        .order_by("-data_os", "-created_at")
    )
    if limite:
        return list(qs[:limite])
    return list(qs)


def _calcular_checksum(eventos):
    """Calcula SHA256 determinístico de lista de eventos.

    Serializa com sort_keys para estabilidade.
    """
    try:
        payload = json.dumps(eventos or [], sort_keys=True, ensure_ascii=False).encode(
            "utf-8"
        )
        return hashlib.sha256(payload).hexdigest()
    except Exception:  # noqa: BLE001
        return None


def verificar_integridade_historico(aluno, reparar: bool = False):
    """Verifica integridade do histórico iniciático de um aluno.

    Args:
        aluno: instância de Aluno
        reparar: se True e divergente, recalcula sincronizando a partir de RegistroHistorico.

    Returns:
        dict com chaves:
          integro (bool), checksum_atual, checksum_recomputado, reparado (bool)
    """
    eventos = (
        aluno.historico_iniciatico
        if isinstance(aluno.historico_iniciatico, list)
        else []
    )
    recomputado = _calcular_checksum(eventos)
    atual = aluno.historico_checksum
    integro = (atual == recomputado) and (atual is not None)
    reparado = False
    if not integro and reparar:
        sincronizar_historico_iniciatico(aluno)
        aluno.refresh_from_db()
        eventos = (
            aluno.historico_iniciatico
            if isinstance(aluno.historico_iniciatico, list)
            else []
        )
        recomputado = _calcular_checksum(eventos)
        atual = aluno.historico_checksum
        integro = (atual == recomputado) and (atual is not None)
        reparado = True
    return {
        "integro": integro,
        "checksum_atual": atual,
        "checksum_recomputado": recomputado,
        "reparado": reparado,
    }


def sincronizar_historico_iniciatico(aluno):
    """Recria o JSON historico_iniciatico a partir de RegistroHistorico."""
    eventos = []
    for reg in listar_eventos_iniciaticos(aluno):
        eventos.append(
            {
                "tipo": reg.codigo.tipo_codigo.nome,
                "descricao": reg.codigo.nome,
                "data": reg.data_os.isoformat(),
                "observacoes": reg.observacoes or "",
                "ordem_servico": reg.ordem_servico or "",
                "criado_em": reg.created_at.isoformat(),
            }
        )
    aluno.historico_iniciatico = eventos
    aluno.historico_checksum = _calcular_checksum(eventos)
    aluno.save(update_fields=["historico_iniciatico", "historico_checksum"])
    return eventos


def criar_evento_iniciatico(
    *,
    aluno,
    codigo,
    tipo_evento: str,
    data_os,
    data_evento,
    ordem_servico="",
    observacoes="",
    sincronizar_cache_incremental=True,
):
    """Cria um RegistroHistorico + insere evento no JSON.

    Args:
        aluno: instância de Aluno
        codigo: instância de Codigo
        tipo_evento: categoria textual (ex: CARGO, INICIAÇÃO)
        data_os: data formal do documento (string YYYY-MM-DD ou date)
        data_evento: data exibida no histórico (string YYYY-MM-DD ou date)
        ordem_servico: identificador opcional
        observacoes: texto opcional
        sincronizar_cache_incremental: se True, faz append em vez de reconstruir tudo

    Returns:
        dict com chaves: registro, evento_json
    """
    RegistroHistorico = get_registro_historico_model()  # noqa
    data_os_norm = _normalizar_data(data_os)
    data_evt_norm = _normalizar_data(data_evento)

    try:
        with transaction.atomic():
            registro = RegistroHistorico.objects.create(
                aluno=aluno,
                codigo=codigo,
                ordem_servico=ordem_servico or None,
                data_os=data_os_norm,
                observacoes=observacoes or None,
            )
            # Append incremental ao JSON (mantendo método existente para consistência)
            if sincronizar_cache_incremental:
                aluno.adicionar_evento_historico(
                    tipo=tipo_evento,
                    descricao=f"{codigo.nome}{' - ' + codigo.descricao if codigo.descricao else ''}",
                    data=data_evt_norm,
                    observacoes=observacoes or "",
                    ordem_servico=ordem_servico or "",
                )
                # Recarrega eventos para checksum coerente
                eventos = (
                    aluno.historico_iniciatico
                    if isinstance(aluno.historico_iniciatico, list)
                    else []
                )
                aluno.historico_checksum = _calcular_checksum(eventos)
                aluno.save(update_fields=["historico_iniciatico", "historico_checksum"])
                evento_json = aluno.historico_iniciatico[-1]
            else:
                # Reconstrói tudo (fallback)
                eventos = sincronizar_historico_iniciatico(aluno)
                evento_json = eventos[-1] if eventos else None
            return {"registro": registro, "evento_json": evento_json}
    except IntegrityError as exc:
        logger.warning("Violação de integridade ao criar evento iniciático: %s", exc)
        raise
    except Exception as exc:  # noqa: BLE001
        logger.error("Erro inesperado ao criar evento iniciático: %s", exc)
        raise


def reconciliar_historico_if_divergente(aluno):
    """Verifica contagem & datas para detectar divergência simples e reconcilia se necessário."""
    try:
        registros = listar_eventos_iniciaticos(aluno)
        json_len = (
            len(aluno.historico_iniciatico or [])
            if isinstance(aluno.historico_iniciatico, list)
            else 0
        )
        if json_len != len(registros):
            return sincronizar_historico_iniciatico(aluno)
        # Checagem superficial: comparar datas do primeiro
        if registros:
            reg_top = registros[0].data_os.isoformat()
            json_top = aluno.historico_iniciatico[0].get("data") if json_len else None
            if reg_top != json_top:
                return sincronizar_historico_iniciatico(aluno)
        return aluno.historico_iniciatico
    except Exception as exc:  # noqa: BLE001
        logger.error("Falha ao reconciliar histórico: %s", exc)
        return aluno.historico_iniciatico
