"""
Service de validação de atividades duplicadas por turma.

Regra: Uma turma não pode ter duas atividades com o mesmo tipo + nome
no mesmo período. Aviso se períodos diferentes.
"""
import logging
from datetime import datetime
from django.core.exceptions import ValidationError
from atividades.models import Atividade

logger = logging.getLogger(__name__)


class ValidacaoDuplicatasAtividades:
    """Valida duplicação de atividades (mesmo tipo + nome) em uma turma."""

    @staticmethod
    def verificar_duplicatas_na_turma(atividade, turma_id):
        """
        Verifica se há atividades duplicadas na turma para a atividade dada.

        Args:
            atividade: Instância de Atividade (pode estar sem ID se for nova)
            turma_id: ID da turma a validar

        Returns:
            dict: {
                'tem_duplicatas': bool,
                'tem_warning': bool,
                'tem_bloqueio': bool,
                'mensagem': str,
                'duplicatas': list de Atividades duplicadas
            }
        """
        resultado = {
            "tem_duplicatas": False,
            "tem_warning": False,
            "tem_bloqueio": False,
            "mensagem": "",
            "duplicatas": [],
        }

        # Buscar atividades com mesmo tipo + nome já vinculadas à turma
        duplicatas = Atividade.objects.filter(
            turmas__id=turma_id,
            tipo_atividade=atividade.tipo_atividade,
            nome=atividade.nome,
        )

        # Excluir a própria atividade se for edição (já tem ID)
        if atividade.pk:
            duplicatas = duplicatas.exclude(pk=atividade.pk)

        if not duplicatas.exists():
            return resultado

        resultado["tem_duplicatas"] = True
        resultado["duplicatas"] = list(duplicatas)

        # Verificar se há sobreposição de períodos
        for dup in duplicatas:
            tem_bloqueio = ValidacaoDuplicatasAtividades._verificar_sobreposicao(
                atividade, dup
            )

            if tem_bloqueio:
                resultado["tem_bloqueio"] = True
                resultado["mensagem"] = (
                    f"BLOQUEADO: Já existe a atividade '{dup.nome}' "
                    f"({dup.get_tipo_atividade_display()}) no período "
                    f"{dup.data_inicio} a {dup.data_fim} nesta turma. "
                    f"Altere o nome ou período da atividade."
                )
                break
            else:
                resultado["tem_warning"] = True
                if not resultado["mensagem"]:
                    resultado["mensagem"] = (
                        f"AVISO: Já existe a atividade '{dup.nome}' "
                        f"({dup.get_tipo_atividade_display()}) em período diferente. "
                        f"Considere renomear ou ajustar o período para evitar confusão."
                    )

        return resultado

    @staticmethod
    def _verificar_sobreposicao(atividade1, atividade2):
        """
        Verifica se dois períodos de atividades se sobrepõem.

        Considera também data_fim como None = mesma data de início.
        """
        # Ajustar datas finais se forem None
        fim1 = atividade1.data_fim or atividade1.data_inicio
        fim2 = atividade2.data_fim or atividade2.data_inicio

        # Verifica sobreposição: não(A antes B E B antes A)
        # Sobreposição ocorre se: A.inicio <= B.fim E B.inicio <= A.fim
        return (
            atividade1.data_inicio <= fim2 and atividade2.data_inicio <= fim1
        )

    @staticmethod
    def validar_ao_vincular_turma(atividade, turma_id):
        """
        Valida quando uma atividade está sendo vinculada a uma turma.
        Lança ValidationError se houver bloqueio.

        Args:
            atividade: Instância de Atividade
            turma_id: ID da turma a vincular

        Raises:
            ValidationError: Se houver duplicata no mesmo período
        """
        resultado = ValidacaoDuplicatasAtividades.verificar_duplicatas_na_turma(
            atividade, turma_id
        )

        if resultado["tem_bloqueio"]:
            logger.warning(
                f"[Validação Duplicata] BLOQUEIO: {resultado['mensagem']} "
                f"(atividade={atividade.id}, turma={turma_id})"
            )
            raise ValidationError(resultado["mensagem"])

        if resultado["tem_warning"]:
            logger.info(
                f"[Validação Duplicata] AVISO: {resultado['mensagem']} "
                f"(atividade={atividade.id}, turma={turma_id})"
            )

        return resultado

    @staticmethod
    def get_duplicatas_para_exibicao(atividade, turma_id):
        """
        Retorna duplicatas formatadas para exibição na UI.

        Returns:
            list de dicts com info das duplicatas
        """
        resultado = ValidacaoDuplicatasAtividades.verificar_duplicatas_na_turma(
            atividade, turma_id
        )

        return [
            {
                "id": dup.id,
                "nome": dup.nome,
                "tipo": dup.get_tipo_atividade_display(),
                "data_inicio": dup.data_inicio.strftime("%d/%m/%Y"),
                "data_fim": (
                    dup.data_fim.strftime("%d/%m/%Y") if dup.data_fim else "---"
                ),
                "status": dup.status,
            }
            for dup in resultado["duplicatas"]
        ]
