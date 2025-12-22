"""
Serviços para o aplicativo presencas.
Contém a lógica de negócios complexa.
"""

import logging
from django.core.exceptions import ValidationError
from django.db import transaction
from importlib import import_module
from datetime import date, datetime

# Importar nova calculadora de estatísticas

logger = logging.getLogger(__name__)


def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_turma_model():
    """Obtém o modelo Turma dinamicamente."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


def get_atividade_model():
    """Obtém o modelo Atividade dinamicamente (novo modelo unificado)."""
    atividades_module = import_module("atividades.models")
    # Compatível com arquitetura atual: "Atividade"
    return getattr(atividades_module, "Atividade")


def get_presenca_models():
    """Obtém os modelos de presença dinamicamente, alinhados ao modelo unificado.

    Retorna somente os modelos atuais necessários para os serviços.
    """
    from .models import RegistroPresenca, PresencaDetalhada

    return {
        "RegistroPresenca": RegistroPresenca,
        "PresencaDetalhada": PresencaDetalhada,
    }


def listar_presencas():
    """Lista registros de presença (modelo unificado)."""
    modelos = get_presenca_models()
    return (
        modelos["RegistroPresenca"]
        .objects.select_related("aluno", "turma", "atividade")
        .order_by("-data")
    )


def buscar_presencas_por_filtros(filtros):
    """
    Busca presenças com filtros específicos.

    Args:
        filtros (dict): Dicionário com filtros
    """
    modelos = get_presenca_models()
    presencas = (
        modelos["RegistroPresenca"]
        .objects.select_related("aluno", "turma", "atividade")
        .all()
    )

    if filtros.get("aluno_cpf"):
        presencas = presencas.filter(aluno__cpf=filtros["aluno_cpf"])

    if filtros.get("turma_id"):
        presencas = presencas.filter(turma_id=filtros["turma_id"])

    if filtros.get("atividade_id"):
        presencas = presencas.filter(atividade_id=filtros["atividade_id"])

    if filtros.get("data_inicio"):
        presencas = presencas.filter(data__gte=filtros["data_inicio"])

    if filtros.get("data_fim"):
        presencas = presencas.filter(data__lte=filtros["data_fim"])

    # Compatibilidade: mapear "presente" bool para status
    if filtros.get("presente") is not None:
        presencas = presencas.filter(status=("P" if filtros["presente"] else "F"))

    # Novo filtro direto por status (quando fornecido)
    if filtros.get("status"):
        presencas = presencas.filter(status=filtros["status"])

    return presencas.order_by("-data")


def registrar_presenca(dados_presenca):
    """
    Registra uma nova presença.

    Args:
        dados_presenca (dict): Dados da presença
    """
    try:
        with transaction.atomic():
            Aluno = get_aluno_model()
            Turma = get_turma_model()
            Atividade = get_atividade_model()
            modelos = get_presenca_models()

            # Buscar relacionamentos
            aluno = Aluno.objects.get(cpf=dados_presenca["aluno_cpf"])
            turma = (
                Turma.objects.get(id=dados_presenca["turma_id"])
                if dados_presenca.get("turma_id")
                else None
            )
            atividade = (
                Atividade.objects.get(id=dados_presenca["atividade_id"])
                if dados_presenca.get("atividade_id")
                else None
            )

            # Validar data
            data_presenca = dados_presenca.get("data")
            if isinstance(data_presenca, str):
                data_presenca = datetime.strptime(data_presenca, "%Y-%m-%d").date()
            elif isinstance(data_presenca, datetime):
                data_presenca = data_presenca.date()

            if data_presenca > date.today():
                raise ValidationError("A data da presença não pode ser futura.")

            # Verificar se já existe presença para essa data
            presenca_existente = (
                modelos["RegistroPresenca"]
                .objects.filter(aluno=aluno, turma=turma, atividade=atividade, data=data_presenca)
                .exists()
            )

            if presenca_existente:
                raise ValidationError(
                    "Já existe registro de presença para este aluno nesta data."
                )

            # Criar presença
            # Mapear campo legado "presente" para "status"
            presente_flag = dados_presenca.get("presente", True)
            status = dados_presenca.get("status") or ("P" if presente_flag else "F")

            presenca = modelos["RegistroPresenca"].objects.create(
                aluno=aluno,
                turma=turma,
                atividade=atividade,
                data=data_presenca,
                status=status,
                justificativa=dados_presenca.get("justificativa", ""),
                registrado_por=dados_presenca.get("registrado_por", "Sistema"),
            )

            logger.info(f"Presença registrada: {presenca}")
            return presenca

    except (Aluno.DoesNotExist, Turma.DoesNotExist, Atividade.DoesNotExist) as e:
        raise ValidationError(f"Relacionamento não encontrado: {str(e)}")
    except Exception as e:
        logger.error(f"Erro ao registrar presença: {str(e)}")
        raise ValidationError(f"Erro ao registrar presença: {str(e)}")


def registrar_presencas_multiplas(lista_presencas):
    """
    Registra múltiplas presenças de uma vez.

    Args:
        lista_presencas (list): Lista com dados das presenças
    """
    presencas_criadas = []
    erros = []

    with transaction.atomic():
        for dados in lista_presencas:
            try:
                presenca = registrar_presenca(dados)
                presencas_criadas.append(presenca)
            except ValidationError as e:
                erros.append({"dados": dados, "erro": str(e)})

    return {
        "criadas": presencas_criadas,
        "erros": erros,
        "total_criadas": len(presencas_criadas),
        "total_erros": len(erros),
    }


def atualizar_presenca(presenca_id, dados_atualizacao):
    """
    Atualiza uma presença existente.

    Args:
        presenca_id (int): ID da presença
        dados_atualizacao (dict): Dados para atualização
    """
    try:
        with transaction.atomic():
            modelos = get_presenca_models()
            presenca = modelos["RegistroPresenca"].objects.get(id=presenca_id)

            # Campos permitidos para atualização
            campos_permitidos = ["status", "justificativa", "data", "registrado_por"]

            for campo in campos_permitidos:
                if campo in dados_atualizacao:
                    if campo == "data":
                        nova_data = dados_atualizacao[campo]
                        if isinstance(nova_data, str):
                            nova_data = datetime.strptime(nova_data, "%Y-%m-%d").date()
                        elif isinstance(nova_data, datetime):
                            nova_data = nova_data.date()

                        if nova_data > date.today():
                            raise ValidationError(
                                "A data da presença não pode ser futura."
                            )

                        setattr(presenca, campo, nova_data)
                    else:
                        setattr(presenca, campo, dados_atualizacao[campo])

            presenca.full_clean()
            presenca.save()

            logger.info(f"Presença atualizada: {presenca}")
            return presenca

    except modelos["RegistroPresenca"].DoesNotExist:
        raise ValidationError("Presença não encontrada.")
    except Exception as e:
        logger.error(f"Erro ao atualizar presença: {str(e)}")
        raise ValidationError(f"Erro ao atualizar presença: {str(e)}")


def excluir_presenca(presenca_id):
    """
    Exclui uma presença.

    Args:
        presenca_id (int): ID da presença
    """
    try:
        with transaction.atomic():
            modelos = get_presenca_models()
            presenca = modelos["RegistroPresenca"].objects.get(id=presenca_id)
            presenca.delete()

            logger.info(f"Presença excluída: ID {presenca_id}")
            return True

    except modelos["RegistroPresenca"].DoesNotExist:
        raise ValidationError("Presença não encontrada.")
    except Exception as e:
        logger.error(f"Erro ao excluir presença: {str(e)}")
        raise ValidationError(f"Erro ao excluir presença: {str(e)}")


def obter_presencas_por_aluno(aluno_cpf, data_inicio=None, data_fim=None):
    """Obtém presenças de um aluno específico."""
    modelos = get_presenca_models()
    presencas = (
        modelos["RegistroPresenca"]
        .objects.filter(aluno__cpf=aluno_cpf)
        .select_related("turma", "atividade")
    )

    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)

    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)

    return presencas.order_by("-data")


def obter_presencas_por_turma(turma_id, data_inicio=None, data_fim=None):
    """Obtém presenças de uma turma específica."""
    modelos = get_presenca_models()
    presencas = (
        modelos["RegistroPresenca"]
        .objects.filter(turma_id=turma_id)
        .select_related("aluno", "atividade")
    )

    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)

    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)

    return presencas.order_by("-data", "aluno__nome")


def calcular_frequencia_aluno(
    aluno_cpf, turma_id=None, periodo_inicio=None, periodo_fim=None
):
    """
    Calcula a frequência de um aluno.

    Args:
        aluno_cpf (str): CPF do aluno
        turma_id (int): ID da turma (opcional)
        periodo_inicio (date): Data início do período
        periodo_fim (date): Data fim do período

    Returns:
        dict: Estatísticas de frequência
    """
    modelos = get_presenca_models()

    # Filtrar presenças
    presencas = modelos["RegistroPresenca"].objects.filter(aluno__cpf=aluno_cpf)

    if turma_id:
        presencas = presencas.filter(turma_id=turma_id)

    if periodo_inicio:
        presencas = presencas.filter(data__gte=periodo_inicio)

    if periodo_fim:
        presencas = presencas.filter(data__lte=periodo_fim)

    total_registros = presencas.count()
    total_presencas = presencas.filter(status="P").count()
    total_faltas = presencas.filter(status="F").count()

    percentual_presenca = (
        (total_presencas / total_registros * 100) if total_registros > 0 else 0
    )

    return {
        "total_registros": total_registros,
        "total_presencas": total_presencas,
        "total_faltas": total_faltas,
        "percentual_presenca": round(percentual_presenca, 2),
    }


def criar_observacao_presenca(dados_observacao):
    """
    Cria uma observação de presença.

    Args:
        dados_observacao (dict): Dados da observação
    """
    try:
        with transaction.atomic():
            Aluno = get_aluno_model()
            Turma = get_turma_model()
            modelos = get_presenca_models()

            # Buscar relacionamentos
            aluno = None
            if dados_observacao.get("aluno_cpf"):
                aluno = Aluno.objects.get(cpf=dados_observacao["aluno_cpf"])

            turma = Turma.objects.get(id=dados_observacao["turma_id"])

            # Criar/atualizar observação via RegistroPresenca.justificativa
            data_obs = dados_observacao.get("data", date.today())
            atividade = None
            if dados_observacao.get("atividade_id"):
                Atividade = get_atividade_model()
                atividade = Atividade.objects.get(id=dados_observacao["atividade_id"])

            status = dados_observacao.get("status") or "P"

            registro, created = modelos["RegistroPresenca"].objects.get_or_create(
                aluno=aluno,
                turma=turma,
                atividade=atividade,
                data=data_obs,
                defaults={
                    "status": status,
                    "justificativa": dados_observacao.get("texto", ""),
                    "registrado_por": dados_observacao.get("registrado_por", "Sistema"),
                },
            )

            if not created:
                registro.justificativa = dados_observacao.get("texto", "")
                # Opcionalmente ajustar status se fornecido
                if dados_observacao.get("status"):
                    registro.status = dados_observacao["status"]
                registro.save()

            logger.info(f"Observação registrada em RegistroPresenca: {registro}")
            return registro

    except Exception as e:
        logger.error(f"Erro ao criar observação: {str(e)}")
        raise ValidationError(f"Erro ao criar observação: {str(e)}")


def calcular_total_atividade_mes(turma_id, atividade_id, ano, mes):
    """Calcula o total de registros de atividade por mês via agregação.

    Retorna um dicionário com a quantidade, sem persistir tabela de totais.
    """
    try:
        modelos = get_presenca_models()
        Turma = get_turma_model()
        Atividade = get_atividade_model()

        turma = Turma.objects.get(id=turma_id)
        atividade = Atividade.objects.get(id=atividade_id)

        # Filtrar por ano/mes usando campo data
        qs = modelos["RegistroPresenca"].objects.filter(
            turma=turma,
            atividade=atividade,
            data__year=ano,
            data__month=mes,
        )

        quantidade = qs.count()
        result = {
            "turma_id": turma_id,
            "atividade_id": atividade_id,
            "ano": ano,
            "mes": mes,
            "qtd_ativ_mes": quantidade,
        }

        logger.info(f"Total calculado (sem persistência): {result}")
        return result
    except Exception as e:
        logger.error(f"Erro ao calcular total atividade mês: {str(e)}")
        raise ValidationError(f"Erro ao calcular total atividade mês: {str(e)}")
