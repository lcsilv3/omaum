"""
Repository pattern para o modelo Aluno.
"""

import logging
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from alunos.utils import get_aluno_model

logger = logging.getLogger(__name__)


class AlunoRepository:
    """Repository para operações com o modelo Aluno."""

    @staticmethod
    def get_model():
        """Obtém o modelo Aluno dinamicamente."""
        return get_aluno_model()

    @staticmethod
    def buscar_por_id(aluno_id):
        """Busca aluno por ID."""
        try:
            Aluno = AlunoRepository.get_model()
            return Aluno.objects.get(id=aluno_id)
        except ObjectDoesNotExist:
            logger.warning(f"Aluno com ID {aluno_id} não encontrado")
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar aluno por ID {aluno_id}: {e}")
            return None

    @staticmethod
    def buscar_por_cpf(cpf):
        """Busca aluno por CPF."""
        try:
            Aluno = AlunoRepository.get_model()
            return Aluno.objects.get(cpf=cpf)
        except ObjectDoesNotExist:
            logger.warning(f"Aluno com CPF {cpf} não encontrado")
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar aluno por CPF {cpf}: {e}")
            return None

    @staticmethod
    def buscar_por_email(email):
        """Busca aluno por email."""
        try:
            Aluno = AlunoRepository.get_model()
            return Aluno.objects.get(email=email)
        except ObjectDoesNotExist:
            logger.warning(f"Aluno com email {email} não encontrado")
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar aluno por email {email}: {e}")
            return None

    @staticmethod
    def buscar_por_nome_ou_cpf(query):
        """Busca alunos por nome ou CPF."""
        Aluno = AlunoRepository.get_model()
        cpf_query = "".join(filter(str.isdigit, query))
        return Aluno.objects.filter(
            Q(nome__icontains=query) | Q(cpf__icontains=cpf_query)
        )

    @staticmethod
    def buscar_instrutores_ativos():
        """Busca alunos que podem ser instrutores."""
        try:
            Aluno = AlunoRepository.get_model()
            return Aluno.objects.filter(situacao="ATIVO").select_related()
        except Exception as e:
            logger.error(f"Erro ao buscar instrutores ativos: {e}")
            return Aluno.objects.none()

    @staticmethod
    def listar_com_filtros(query=None, curso_id=None, ativo=True):
        """Lista alunos com filtros otimizados."""
        try:
            Aluno = AlunoRepository.get_model()
            # Converte parâmetro 'ativo' para filtro por 'situacao'
            situacao_filter = "a" if ativo else "~Q(situacao='a')"
            queryset = (
                Aluno.objects.filter(situacao="a" if ativo else Q(~Q(situacao="a")), cpf__isnull=False)
                .exclude(cpf__exact="")
                .select_related()
                .prefetch_related("matricula_set__turma__curso")
                .order_by("nome")
            )

            if query:
                query = query.lower()
                if query.isdigit():
                    cpf_query = query
                    search_query = Q(cpf__icontains=cpf_query) | Q(
                        matricula__icontains=cpf_query
                    )
                else:
                    search_query = (
                        Q(nome__icontains=query)
                        | Q(email__icontains=query)
                        | Q(numero_iniciatico__icontains=query)
                        | Q(nome_iniciatico__icontains=query)
                    )
                queryset = queryset.filter(search_query).distinct()

            if curso_id:
                queryset = queryset.filter(
                    matricula__turma__curso_id=curso_id
                ).distinct()

            return queryset
        except Exception as e:
            logger.error(f"Erro ao listar alunos com filtros: {e}")
            return Aluno.objects.none()

    @staticmethod
    def criar(aluno_data):
        """Cria um novo aluno com os dados fornecidos."""
        Aluno = AlunoRepository.get_model()
        return Aluno.objects.create(**aluno_data)

    @staticmethod
    def atualizar(aluno, dados):
        """Atualiza os dados de um aluno existente."""
        for campo, valor in dados.items():
            setattr(aluno, campo, valor)
        aluno.save()
        return aluno
