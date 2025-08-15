"""
Serviços para o aplicativo matriculas.
Contém a lógica de negócios complexa.
"""

import logging
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from importlib import import_module
from .models import Matricula

logger = logging.getLogger(__name__)


def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_turma_model():
    """Obtém o modelo Turma dinamicamente."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


def listar_matriculas():
    """Lista todas as matrículas."""
    return Matricula.objects.select_related("aluno", "turma").all()


def buscar_matriculas_por_filtros(aluno_cpf=None, turma_id=None, status=None):
    """Busca matrículas com filtros específicos."""
    matriculas = Matricula.objects.select_related("aluno", "turma").all()

    if aluno_cpf:
        matriculas = matriculas.filter(aluno__cpf=aluno_cpf)

    if turma_id:
        matriculas = matriculas.filter(turma_id=turma_id)

    if status:
        matriculas = matriculas.filter(status=status)

    return matriculas.order_by("-data_matricula")


def obter_matricula_por_id(matricula_id):
    """Obtém uma matrícula por ID."""
    try:
        return Matricula.objects.select_related("aluno", "turma").get(id=matricula_id)
    except Matricula.DoesNotExist:
        logger.error(f"Matrícula com ID {matricula_id} não encontrada")
        return None


def criar_matricula(dados_matricula):
    """
    Cria uma nova matrícula.

    Args:
        dados_matricula (dict): Dados da matrícula

    Returns:
        Matricula: Instância da matrícula criada

    Raises:
        ValidationError: Se os dados forem inválidos
    """
    try:
        with transaction.atomic():
            Aluno = get_aluno_model()
            Turma = get_turma_model()

            # Buscar aluno e turma
            aluno = Aluno.objects.get(cpf=dados_matricula["aluno_cpf"])
            turma = Turma.objects.get(id=dados_matricula["turma_id"])

            # Verificar se já existe matrícula ativa
            matricula_existente = Matricula.objects.filter(
                aluno=aluno, turma=turma, status="A"
            ).exists()

            if matricula_existente:
                raise ValidationError("Aluno já possui matrícula ativa nesta turma.")

            # Verificar vagas disponíveis
            if turma.vagas_disponiveis <= 0:
                raise ValidationError("Não há vagas disponíveis nesta turma.")

            # Criar matrícula
            matricula = Matricula.objects.create(
                aluno=aluno,
                turma=turma,
                data_matricula=dados_matricula.get(
                    "data_matricula", timezone.now().date()
                ),
                status=dados_matricula.get("status", "A"),
                ativa=True,
            )

            logger.info(f"Matrícula criada: {matricula}")
            return matricula

    except Aluno.DoesNotExist:
        raise ValidationError("Aluno não encontrado.")
    except Turma.DoesNotExist:
        raise ValidationError("Turma não encontrada.")
    except Exception as e:
        logger.error(f"Erro ao criar matrícula: {str(e)}")
        raise ValidationError(f"Erro ao criar matrícula: {str(e)}")


def atualizar_matricula(matricula_id, dados_atualizacao):
    """
    Atualiza uma matrícula existente.

    Args:
        matricula_id (int): ID da matrícula
        dados_atualizacao (dict): Dados para atualização

    Returns:
        Matricula: Instância da matrícula atualizada

    Raises:
        ValidationError: Se a matrícula não for encontrada ou dados inválidos
    """
    try:
        with transaction.atomic():
            matricula = Matricula.objects.get(id=matricula_id)

            # Atualizar campos permitidos
            campos_permitidos = ["status", "ativa", "data_matricula"]
            for campo in campos_permitidos:
                if campo in dados_atualizacao:
                    setattr(matricula, campo, dados_atualizacao[campo])

            matricula.full_clean()
            matricula.save()

            logger.info(f"Matrícula atualizada: {matricula}")
            return matricula

    except Matricula.DoesNotExist:
        raise ValidationError("Matrícula não encontrada.")
    except Exception as e:
        logger.error(f"Erro ao atualizar matrícula: {str(e)}")
        raise ValidationError(f"Erro ao atualizar matrícula: {str(e)}")


def cancelar_matricula(matricula_id, motivo=None):
    """
    Cancela uma matrícula.

    Args:
        matricula_id (int): ID da matrícula
        motivo (str): Motivo do cancelamento

    Returns:
        Matricula: Instância da matrícula cancelada
    """
    try:
        with transaction.atomic():
            matricula = Matricula.objects.get(id=matricula_id)
            matricula.status = "C"
            matricula.ativa = False
            matricula.save()

            logger.info(f"Matrícula cancelada: {matricula}. Motivo: {motivo}")
            return matricula

    except Matricula.DoesNotExist:
        raise ValidationError("Matrícula não encontrada.")
    except Exception as e:
        logger.error(f"Erro ao cancelar matrícula: {str(e)}")
        raise ValidationError(f"Erro ao cancelar matrícula: {str(e)}")


def obter_matriculas_ativas_por_aluno(aluno_cpf):
    """Obtém todas as matrículas ativas de um aluno."""
    return Matricula.objects.filter(
        aluno__cpf=aluno_cpf, status="A", ativa=True
    ).select_related("turma__curso")


def obter_matriculas_por_turma(turma_id):
    """Obtém todas as matrículas de uma turma."""
    return (
        Matricula.objects.filter(turma_id=turma_id)
        .select_related("aluno")
        .order_by("aluno__nome")
    )


def verificar_dependencias_matricula(matricula_id):
    """
    Verifica dependências de uma matrícula antes da exclusão.

    Returns:
        dict: Dicionário com informações sobre dependências
    """
    try:
        matricula = Matricula.objects.get(id=matricula_id)
        dependencias = {
            "presencas": [],
            "notas": [],
            "pagamentos": [],
            "frequencias": [],
        }

        # Verificar presenças
        try:
            presencas_module = import_module("presencas.models")
            Presenca = getattr(presencas_module, "Presenca")
            presencas = Presenca.objects.filter(
                aluno=matricula.aluno, turma=matricula.turma
            )
            dependencias["presencas"] = list(presencas[:5])  # Primeiras 5
        except (ImportError, AttributeError):
            pass

        # Verificar notas
        try:
            notas_module = import_module("notas.models")
            Nota = getattr(notas_module, "Nota")
            notas = Nota.objects.filter(aluno=matricula.aluno, turma=matricula.turma)
            dependencias["notas"] = list(notas[:5])  # Primeiras 5
        except (ImportError, AttributeError):
            pass

        # Verificar pagamentos
        try:
            pagamentos_module = import_module("pagamentos.models")
            Pagamento = getattr(pagamentos_module, "Pagamento")
            pagamentos = Pagamento.objects.filter(aluno=matricula.aluno)
            dependencias["pagamentos"] = list(pagamentos[:5])  # Primeiros 5
        except (ImportError, AttributeError):
            pass

        return dependencias

    except Matricula.DoesNotExist:
        return {}


def excluir_matricula(matricula_id):
    """
    Exclui uma matrícula após verificar dependências.

    Args:
        matricula_id (int): ID da matrícula

    Returns:
        bool: True se excluído com sucesso

    Raises:
        ValidationError: Se existirem dependências
    """
    try:
        dependencias = verificar_dependencias_matricula(matricula_id)

        # Verificar se existem dependências
        tem_dependencias = any(len(deps) > 0 for deps in dependencias.values())

        if tem_dependencias:
            raise ValidationError(
                "Não é possível excluir esta matrícula pois existem registros dependentes."
            )

        with transaction.atomic():
            matricula = Matricula.objects.get(id=matricula_id)
            matricula.delete()

            logger.info(f"Matrícula excluída: ID {matricula_id}")
            return True

    except Matricula.DoesNotExist:
        raise ValidationError("Matrícula não encontrada.")
    except Exception as e:
        logger.error(f"Erro ao excluir matrícula: {str(e)}")
        raise ValidationError(f"Erro ao excluir matrícula: {str(e)}")
