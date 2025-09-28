"""Serviços para o aplicativo alunos."""

import logging
import requests

from django.core.cache import cache
from django.core.files.base import ContentFile
from django.utils import timezone

from alunos.utils import (
    get_atribuicao_cargo_model,
    get_matricula_model,
    get_registro_historico_model,
    get_turma_model,
)
from .repositories import AlunoRepository

logger = logging.getLogger(__name__)


class InstrutorService:
    """Serviços relacionados à elegibilidade e gestão de instrutores."""

    @staticmethod
    def verificar_elegibilidade_completa(aluno):
        """
        Verifica se um aluno pode ser instrutor com validações completas.
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
                    f"situação para '{aluno.get_situacao_display()}'!"
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
                    f"'{aluno.get_situacao_display()}'!"
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
                    f"'{aluno.get_situacao_display()}'!"
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


def criar_aluno(aluno_data, foto_url=None):
    """
    Cria um novo aluno com os dados fornecidos e, opcionalmente, uma foto.
    Esta função permanece no service layer por orquestrar a criação no repositório
    e o download da foto, uma lógica de aplicação.
    """
    try:
        aluno = AlunoRepository.criar(aluno_data)
        if foto_url:
            try:
                response = requests.get(foto_url, stream=True, timeout=10)
                response.raise_for_status()
                file_name = f"{aluno_data['cpf']}_photo.jpg"
                aluno.foto.save(file_name, ContentFile(response.content), save=True)
            except requests.RequestException as e:
                logger.error("Erro ao realizar a requisição da foto: %s", e)
        return aluno
    except Exception as e:
        logger.error("Erro ao criar o aluno %s: %s", aluno_data.get("nome"), e)
        return None


def listar_alunos(query=None, curso_id=None):
    """
    Lista e filtra alunos com base na query e no curso.
    """
    queryset = AlunoRepository.listar_com_filtros(query=query, curso_id=curso_id)

    logger.debug(
        "Query recebida: %s, Curso ID: %s, Resultados encontrados: %d",
        query,
        curso_id,
        queryset.count(),
    )

    return queryset


def buscar_aluno_por_id(aluno_id):
    """
    Busca um aluno pelo ID usando o repositório."""
    return AlunoRepository.buscar_por_id(aluno_id)


def buscar_aluno_por_cpf(cpf):
    """
    Busca um aluno pelo CPF usando o repositório."""
    return AlunoRepository.buscar_por_cpf(cpf)


def buscar_alunos_por_nome_ou_cpf(query):
    """
    Busca alunos por nome ou CPF usando o repositório."""
    return AlunoRepository.buscar_por_nome_ou_cpf(query)


def buscar_aluno_por_email(email):
    """
    Busca um aluno pelo email usando o repositório."""
    return AlunoRepository.buscar_por_email(email)


def listar_historico_aluno(aluno):
    """
    Retorna o histórico de registros de um aluno."""
    RegistroHistorico = get_registro_historico_model()
    return RegistroHistorico.objects.filter(aluno=aluno).order_by("-data_os")


def criar_registro_historico(data, aluno):
    """
    Cria um registro histórico para o aluno."""
    RegistroHistorico = get_registro_historico_model()

    data["aluno"] = aluno
    return RegistroHistorico.objects.create(**data)


def atualizar_dados_aluno(aluno_id, dados):
    """
    Atualiza os dados de um aluno existente usando o repositório."""
    aluno = AlunoRepository.buscar_por_id(aluno_id)
    if not aluno:
        return {"status": "erro", "mensagem": "Aluno não encontrado."}

    try:
        AlunoRepository.atualizar(aluno, dados)
        logger.info("Aluno %s foi atualizado com sucesso.", aluno_id)
        return {
            "status": "sucesso",
            "mensagem": "Dados do aluno atualizados com sucesso.",
        }
    except Exception as e:
        logger.error("Erro ao atualizar o aluno %s: %s", aluno_id, e)
        return {"status": "erro", "mensagem": f"Erro inesperado: {e}"}


def listar_alunos_com_cache(query=None, curso_id=None, cache_timeout=300):
    """
    Lista alunos com cache básico para melhorar performance."""
    cache_key = f"alunos_lista_{query or 'all'}_{curso_id or 'all'}"
    resultado = cache.get(cache_key)
    if resultado is not None:
        return resultado
    resultado = listar_alunos(query=query, curso_id=curso_id)
    cache.set(cache_key, resultado, cache_timeout)
    return resultado
