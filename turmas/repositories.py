"""
Repositórios para os modelos dos aplicativos Turmas e Cargos.
"""
import logging
from django.utils import timezone
from alunos.utils import get_turma_model, get_atribuicao_cargo_model

logger = logging.getLogger(__name__)

class TurmaRepository:
    """Repository para operações com o modelo Turma."""

    @staticmethod
    def get_model():
        """Obtém o modelo Turma dinamicamente."""
        return get_turma_model()

    @staticmethod
    def buscar_turmas_por_instrutor(aluno):
        """Busca turmas ativas onde o aluno é instrutor principal."""
        Turma = TurmaRepository.get_model()
        return Turma.objects.filter(instrutor=aluno, status="A")

    @staticmethod
    def buscar_turmas_por_instrutor_auxiliar(aluno):
        """Busca turmas ativas onde o aluno é instrutor auxiliar."""
        Turma = TurmaRepository.get_model()
        return Turma.objects.filter(instrutor_auxiliar=aluno, status="A")

    @staticmethod
    def buscar_turmas_por_auxiliar_instrucao(aluno):
        """Busca turmas ativas onde o aluno é auxiliar de instrução."""
        Turma = TurmaRepository.get_model()
        return Turma.objects.filter(auxiliar_instrucao=aluno, status="A")

    @staticmethod
    def desvincular_instrutor(turma):
        """Remove o instrutor principal de uma turma."""
        turma.instrutor = None
        turma.alerta_instrutor = True
        turma.alerta_mensagem = (
            f"O instrutor foi removido devido à mudança de situação."
        )
        turma.save()

    @staticmethod
    def desvincular_instrutor_auxiliar(turma):
        """Remove o instrutor auxiliar de uma turma."""
        turma.instrutor_auxiliar = None
        turma.alerta_instrutor = True
        turma.alerta_mensagem = (
            "O instrutor auxiliar foi removido devido à mudança de situação."
        )
        turma.save()

    @staticmethod
    def desvincular_auxiliar_instrucao(turma):
        """Remove o auxiliar de instrução de uma turma."""
        turma.auxiliar_instrucao = None
        turma.alerta_instrutor = True
        turma.alerta_mensagem = (
            "O auxiliar de instrução foi removido devido à mudança de situação."
        )
        turma.save()


class AtribuicaoCargoRepository:
    """Repository para operações com o modelo AtribuicaoCargo."""

    @staticmethod
    def get_model():
        """Obtém o modelo AtribuicaoCargo dinamicamente."""
        return get_atribuicao_cargo_model()

    @staticmethod
    def buscar_atribuicoes_ativas_por_aluno_e_cargo(aluno, nome_cargo):
        """Busca atribuições de cargo ativas para um aluno com um cargo específico."""
        AtribuicaoCargo = AtribuicaoCargoRepository.get_model()
        if not AtribuicaoCargo:
            return []
        return AtribuicaoCargo.objects.filter(
            aluno=aluno, cargo__nome__icontains=nome_cargo, data_fim__isnull=True
        )

    @staticmethod
    def finalizar_atribuicao(atribuicao):
        """Finaliza uma atribuição de cargo definindo a data de fim."""
        atribuicao.data_fim = timezone.now().date()
        atribuicao.save()
