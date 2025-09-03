"""
Factories simplificadas para testes.
"""

from django.contrib.auth.models import User
from cursos.models import Curso
from alunos.models import Aluno
from matriculas.models import Matricula
from turmas.models import Turma
from presencas.models import Presenca


class UserFactory:
    """Factory simples para User."""

    @classmethod
    def create(cls, **kwargs):
        """Cria um usuário para testes."""
        return User.objects.create_user(
            username=kwargs.get("username", "testuser"),
            email=kwargs.get("email", "test@example.com"),
            password=kwargs.get("password", "testpass"),
            first_name=kwargs.get("first_name", "Test"),
            last_name=kwargs.get("last_name", "User"),
        )

    def __call__(self, **kwargs):
        return self.create(**kwargs)


class CursoFactory:
    """Factory simples para Curso."""

    @classmethod
    def create(cls, **kwargs):
        """Cria um curso para testes."""
        return Curso.objects.create(
            nome=kwargs.get("nome", "Curso Teste"),
            descricao=kwargs.get("descricao", "Descrição teste"),
            ativo=kwargs.get("ativo", True),
        )

    def __call__(self, **kwargs):
        return self.create(**kwargs)


class AlunoFactory:
    """Factory simples para Aluno."""

    @classmethod
    def create(cls, **kwargs):
        """Cria um aluno para testes."""
        user = kwargs.get("usuario", UserFactory.create())
        return Aluno.objects.create(
            nome=kwargs.get("nome", "Aluno Teste"),
            email=kwargs.get("email", "aluno@teste.com"),
            telefone=kwargs.get("telefone", "11999999999"),
            endereco=kwargs.get("endereco", "Endereço teste"),
            data_nascimento=kwargs.get("data_nascimento", "1990-01-01"),
            ativo=kwargs.get("ativo", True),
            usuario=user,
        )

    def __call__(self, **kwargs):
        return self.create(**kwargs)


class TurmaFactory:
    """Factory simples para Turma."""

    @classmethod
    def create(cls, **kwargs):
        """Cria uma turma para testes."""
        curso = kwargs.get("curso", CursoFactory.create())
        return Turma.objects.create(
            nome=kwargs.get("nome", "Turma Teste"),
            curso=curso,
            data_inicio=kwargs.get("data_inicio", "2024-01-01"),
            data_fim=kwargs.get("data_fim", "2024-03-31"),
            ativa=kwargs.get("ativa", True),
        )

    def __call__(self, **kwargs):
        return self.create(**kwargs)


class MatriculaFactory:
    """Factory simples para Matricula."""

    @classmethod
    def create(cls, **kwargs):
        """Cria uma matrícula para testes."""
        aluno = kwargs.get("aluno", AlunoFactory.create())
        turma = kwargs.get("turma", TurmaFactory.create())
        return Matricula.objects.create(
            aluno=aluno,
            turma=turma,
            data_matricula=kwargs.get("data_matricula", "2024-01-01"),
            ativa=kwargs.get("ativa", True),
        )

    def __call__(self, **kwargs):
        return self.create(**kwargs)


class PresencaFactory:
    """Factory simples para Presenca."""

    @classmethod
    def create(cls, **kwargs):
        """Cria uma presença para testes."""
        aluno = kwargs.get("aluno", AlunoFactory.create())
        turma = kwargs.get("turma", TurmaFactory.create())
        return Presenca.objects.create(
            aluno=aluno,
            turma=turma,
            data=kwargs.get("data", "2024-01-01"),
            presente=kwargs.get("presente", True),
        )

    def __call__(self, **kwargs):
        return self.create(**kwargs)


# Instanciar factories
UserFactory = UserFactory()
CursoFactory = CursoFactory()
AlunoFactory = AlunoFactory()
TurmaFactory = TurmaFactory()
MatriculaFactory = MatriculaFactory()
PresencaFactory = PresencaFactory()
