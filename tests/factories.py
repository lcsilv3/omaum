"""
Factories otimizadas para testes usando factory_boy.
"""

try:
    import factory
    from factory.django import DjangoModelFactory
    import factory.fuzzy
    from django.contrib.auth.models import User
    from django.utils import timezone
    from datetime import timedelta
    from decimal import Decimal

    # Importações dos modelos
    from cursos.models import Curso
    from alunos.models import Aluno
    from matriculas.models import Matricula
    from turmas.models import Turma
    from presencas.models import RegistroPresenca
    from atividades.models import Atividade

    FACTORY_BOY_AVAILABLE = True

except ImportError:
    # Se factory_boy não estiver disponível, criar classes mock
    FACTORY_BOY_AVAILABLE = False

    class DjangoModelFactory:
        pass

    class factory:
        class django:
            class DjangoModelFactory:
                pass

        class SubFactory:
            def __init__(self, factory_class):
                self.factory_class = factory_class

        class Faker:
            def __init__(self, provider, **kwargs):
                self.provider = provider
                self.kwargs = kwargs

        class LazyFunction:
            def __init__(self, func):
                self.func = func

        class Sequence:
            def __init__(self, func):
                self.func = func

        class LazyAttribute:
            def __init__(self, func):
                self.func = func

        class PostGenerationMethodCall:
            def __init__(self, method_name, *args, **kwargs):
                self.method_name = method_name
                self.args = args
                self.kwargs = kwargs

        def post_generation(func):
            return func

        class fuzzy:
            class FuzzyInteger:
                def __init__(self, low, high):
                    self.low = low
                    self.high = high


if FACTORY_BOY_AVAILABLE:
    # Factories reais usando factory_boy
    class UserFactory(DjangoModelFactory):
        class Meta:
            model = User

        username = factory.Sequence(lambda n: f"user{n}")
        email = factory.Faker("email")
        first_name = factory.Faker("first_name")
        last_name = factory.Faker("last_name")
        is_active = True
        is_staff = False
        is_superuser = False
        password = factory.PostGenerationMethodCall("set_password", "defaultpass")

    class CursoFactory(DjangoModelFactory):
        class Meta:
            model = Curso

        nome = factory.Sequence(lambda n: f"Curso {n}")
        descricao = factory.Faker("text", max_nb_chars=200)

    class AlunoFactory(DjangoModelFactory):
        class Meta:
            model = Aluno

        nome = factory.Faker("name")
        email = factory.Faker("email")
        data_nascimento = factory.Faker("date_of_birth")
        ativo = True
        usuario = factory.SubFactory(UserFactory)

    class TurmaFactory(DjangoModelFactory):
        class Meta:
            model = Turma

        nome = factory.Sequence(lambda n: f"Turma {n}")
        curso = factory.SubFactory(CursoFactory)
        data_inicio = factory.Faker("date_this_year")
        data_fim = factory.LazyAttribute(
            lambda obj: obj.data_inicio + timedelta(days=90)
        )
        ativa = True

    class MatriculaFactory(DjangoModelFactory):
        class Meta:
            model = Matricula

        aluno = factory.SubFactory(AlunoFactory)
        turma = factory.SubFactory(TurmaFactory)
        data_matricula = factory.Faker("date_this_year")
        ativa = True

    class AtividadeFactory(DjangoModelFactory):
        class Meta:
            model = Atividade

        nome = factory.Sequence(lambda n: f"Atividade {n}")
        tipo_atividade = "curso"
        data_inicio = factory.Faker("date_this_year")
        data_fim = factory.LazyAttribute(
            lambda obj: obj.data_inicio + timedelta(days=30)
        )
        hora_inicio = "09:00"
        hora_fim = "17:00"
        status = "ativa"
        ativo = True
        convocacao = True
        curso = factory.SubFactory(CursoFactory)

    class PresencaFactory(DjangoModelFactory):
        class Meta:
            model = RegistroPresenca

        aluno = factory.SubFactory(AlunoFactory)
        turma = factory.SubFactory(TurmaFactory)
        atividade = factory.SubFactory(AtividadeFactory)
        data = factory.Faker("date_this_year")
        status = "P"  # Presente por padrão
        convocado = False
        registrado_por = "sistema"

else:
    # Classes mock para quando factory_boy não estiver disponível
    class UserFactory:
        @classmethod
        def create(cls, **kwargs):
            from django.contrib.auth.models import User

            return User.objects.create_user(
                username=kwargs.get("username", "testuser"),
                email=kwargs.get("email", "test@example.com"),
                password=kwargs.get("password", "testpass"),
            )

        def __call__(self, **kwargs):
            return self.create(**kwargs)

    class CursoFactory:
        @classmethod
        def create(cls, **kwargs):
            from cursos.models import Curso

            return Curso.objects.create(
                nome=kwargs.get("nome", "Curso Teste"),
                descricao=kwargs.get("descricao", "Descrição teste"),
            )

        def __call__(self, **kwargs):
            return self.create(**kwargs)

    class AlunoFactory:
        @classmethod
        def create(cls, **kwargs):
            from alunos.models import Aluno

            return Aluno.objects.create(
                nome=kwargs.get("nome", "Aluno Teste"),
                email=kwargs.get("email", "aluno@teste.com"),
                data_nascimento=kwargs.get("data_nascimento", "1990-01-01"),
                ativo=kwargs.get("ativo", True),
                usuario=kwargs.get("usuario", UserFactory.create()),
            )

        def __call__(self, **kwargs):
            return self.create(**kwargs)

    class TurmaFactory:
        @classmethod
        def create(cls, **kwargs):
            from turmas.models import Turma

            return Turma.objects.create(
                nome=kwargs.get("nome", "Turma Teste"),
                curso=kwargs.get("curso", CursoFactory.create()),
                data_inicio=kwargs.get("data_inicio", "2024-01-01"),
                data_fim=kwargs.get("data_fim", "2024-03-31"),
            )

        def __call__(self, **kwargs):
            return self.create(**kwargs)

    class MatriculaFactory:
        @classmethod
        def create(cls, **kwargs):
            from matriculas.models import Matricula

            return Matricula.objects.create(
                aluno=kwargs.get("aluno", AlunoFactory.create()),
                turma=kwargs.get("turma", TurmaFactory.create()),
                data_matricula=kwargs.get("data_matricula", "2024-01-01"),
                ativa=kwargs.get("ativa", True),
            )

        def __call__(self, **kwargs):
            return self.create(**kwargs)

    class AtividadeFactory:
        @classmethod
        def create(cls, **kwargs):
            from atividades.models import Atividade
            from datetime import date, timedelta

            data_inicio = kwargs.get("data_inicio", date.today())
            return Atividade.objects.create(
                nome=kwargs.get("nome", "Atividade Teste"),
                tipo_atividade=kwargs.get("tipo_atividade", "curso"),
                data_inicio=data_inicio,
                data_fim=kwargs.get("data_fim", data_inicio + timedelta(days=30)),
                hora_inicio=kwargs.get("hora_inicio", "09:00"),
                hora_fim=kwargs.get("hora_fim", "17:00"),
                status=kwargs.get("status", "ativa"),
                ativo=kwargs.get("ativo", True),
                convocacao=kwargs.get("convocacao", True),
                curso=kwargs.get("curso", CursoFactory.create()),
            )

        def __call__(self, **kwargs):
            return self.create(**kwargs)

    class PresencaFactory:
        @classmethod
        def create(cls, **kwargs):
            from presencas.models import RegistroPresenca
            from django.utils import timezone

            return RegistroPresenca.objects.create(
                aluno=kwargs.get("aluno", AlunoFactory.create()),
                turma=kwargs.get("turma", TurmaFactory.create()),
                atividade=kwargs.get("atividade", AtividadeFactory.create()),
                data=kwargs.get("data", "2024-01-01"),
                status=kwargs.get("status", "P"),  # P=Presente por padrão
                convocado=kwargs.get("convocado", False),
                registrado_por=kwargs.get("registrado_por", "sistema"),
                data_registro=kwargs.get("data_registro", timezone.now()),
            )

        def __call__(self, **kwargs):
            return self.create(**kwargs)


class FuzzyDecimal:
    def __init__(self, low, high, precision=2):
        self.low = low
        self.high = high
        self.precision = precision


from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Importar modelos principais
try:
    from alunos.models import Aluno
    from cursos.models import Curso
    from matriculas.models import Matricula
    from turmas.models import Turma
    from presencas.models import Presenca
except ImportError:
    # Se os modelos não estiverem disponíveis, usar classes mock
    class Aluno:
        objects = None

    class Curso:
        objects = None

    class Matricula:
        objects = None

    class Turma:
        objects = None

    class Presenca:
        objects = None


class UserFactory(factory.django.DjangoModelFactory):
    """Factory para User Django."""

    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True
    is_staff = False
    is_superuser = False

    @factory.post_generation
    def password(self, create, extracted):
        if not create:
            return
        password = extracted or "testpassword"
        self.set_password(password)


class AdminUserFactory(UserFactory):
    """Factory para usuário administrador."""

    is_staff = True
    is_superuser = True


# Factories básicas para modelos mock
class AlunoFactory(factory.django.DjangoModelFactory):
    """Factory para Aluno."""

    class Meta:
        model = Aluno
        django_get_or_create = ("cpf",) if hasattr(Aluno, "objects") else ()

    nome = factory.Faker("name")
    cpf = factory.Faker("cpf", locale="pt_BR")
    email = factory.Faker("email")
    data_nascimento = factory.Faker("date_of_birth", minimum_age=18, maximum_age=65)
    ativo = True

    @factory.post_generation
    def codigo_iniciatico(self, create, extracted):
        if not create:
            return
        if extracted is not None:
            self.codigo_iniciatico = extracted


class CursoFactory(factory.django.DjangoModelFactory):
    """Factory para Curso."""

    class Meta:
        model = Curso

    nome = factory.Faker("sentence", nb_words=3)
    descricao = factory.Faker("text", max_nb_chars=500)
    ativo = True


class MatriculaFactory(factory.django.DjangoModelFactory):
    """Factory para Matricula."""

    class Meta:
        model = Matricula

    aluno = factory.SubFactory(AlunoFactory)
    curso = factory.SubFactory(CursoFactory)
    data_matricula = factory.LazyFunction(timezone.now)
    valor_pago = factory.fuzzy.FuzzyDecimal(0.0, 1000.0, 2)
    observacoes = factory.Faker("text", max_nb_chars=300)
    ativo = True


class TurmaFactory(factory.django.DjangoModelFactory):
    """Factory para Turma."""

    class Meta:
        model = Turma

    nome = factory.Faker("sentence", nb_words=2)
    curso = factory.SubFactory(CursoFactory)
    data_inicio = factory.LazyFunction(lambda: timezone.now().date())
    data_fim = factory.LazyFunction(lambda: timezone.now().date() + timedelta(days=90))
    horario = factory.Faker("time")
    capacidade_maxima = factory.fuzzy.FuzzyInteger(10, 50)
    professor = factory.Faker("name")
    local = factory.Faker("address")
    ativo = True

    @factory.post_generation
    def alunos(self, create, extracted):
        if not create:
            return
        if extracted:
            for aluno in extracted:
                self.alunos.add(aluno)


class PresencaFactory(factory.django.DjangoModelFactory):
    """Factory para Presenca."""

    class Meta:
        model = Presenca

    aluno = factory.SubFactory(AlunoFactory)
    turma = factory.SubFactory(TurmaFactory)
    data_aula = factory.LazyFunction(lambda: timezone.now().date())
    observacoes = factory.Faker("text", max_nb_chars=200)
    registrado_por = factory.SubFactory(UserFactory)
    data_registro = factory.LazyFunction(timezone.now)


# Factories para cenários específicos
class AlunoComMatriculaFactory(AlunoFactory):
    """Factory para Aluno com Matrícula."""

    @factory.post_generation
    def matricula(self, create, extracted):
        if not create:
            return
        MatriculaFactory(aluno=self)


class TurmaComAlunosFactory(TurmaFactory):
    """Factory para Turma com Alunos."""

    @factory.post_generation
    def criar_alunos(self, create, extracted):
        if not create:
            return

        numero_alunos = extracted or 5
        alunos = AlunoFactory.create_batch(numero_alunos)

        for aluno in alunos:
            MatriculaFactory(aluno=aluno, curso=self.curso)
            self.alunos.add(aluno)


class PresencaCompletoFactory(PresencaFactory):
    """Factory para Presença completa com todas as relações."""

    @factory.post_generation
    def setup_completo(self, create, extracted):
        if not create:
            return

        # Garantir que o aluno está matriculado na turma
        if (
            hasattr(Matricula, "objects")
            and Matricula.objects.filter(
                aluno=self.aluno, curso=self.turma.curso
            ).exists()
        ):
            MatriculaFactory(aluno=self.aluno, curso=self.turma.curso)

        # Adicionar aluno à turma
        self.turma.alunos.add(self.aluno)


# Factories para dados de teste específicos
class DadosTesteCompletos:
    """Classe para criar conjuntos completos de dados de teste."""

    @classmethod
    def criar_cenario_basico(cls):
        """Cria um cenário básico de teste."""
        # Criar curso
        curso = CursoFactory()

        # Criar turma
        turma = TurmaFactory(curso=curso)

        # Criar alunos
        alunos = AlunoFactory.create_batch(3)

        # Criar matrículas
        matriculas = []
        for aluno in alunos:
            matricula = MatriculaFactory(aluno=aluno, curso=curso)
            matriculas.append(matricula)
            turma.alunos.add(aluno)

        # Criar presenças
        presencas = []
        for aluno in alunos:
            presenca = PresencaFactory(aluno=aluno, turma=turma)
            presencas.append(presenca)

        return {
            "curso": curso,
            "turma": turma,
            "alunos": alunos,
            "matriculas": matriculas,
            "presencas": presencas,
        }

    @classmethod
    def criar_cenario_complexo(cls):
        """Cria um cenário complexo com múltiplos cursos e turmas."""
        cenarios = []

        for i in range(3):
            cenario = cls.criar_cenario_basico()
            cenarios.append(cenario)

        return cenarios

    cpf = factory.Sequence(lambda n: f"{n:011d}")
    nome = factory.Faker("name")
    email = factory.Faker("email")
    data_nascimento = factory.Faker("date_of_birth", minimum_age=18, maximum_age=70)
    sexo = factory.Iterator(["M", "F"])
    situacao = "ativo"
    nacionalidade = "Brasileira"
    naturalidade = factory.Faker("city")
    rua = factory.Faker("street_name")
    numero_imovel = "123"
    bairro = factory.Faker("city_suffix")
    cidade = factory.Faker("city")
    estado = factory.Faker("state_abbr")
    cep = "12345-678"


class TurmaFactory(DjangoModelFactory):
    """Factory para criar turmas."""

    class Meta:
        model = Turma

    nome = factory.Sequence(lambda n: f"Turma {n}")
    codigo = factory.Sequence(lambda n: f"T{n:03d}")
    data_inicio = factory.LazyFunction(timezone.now)
    status = "A"

    @factory.post_generation
    def add_details(self, create, extracted, **kwargs):
        if not create:
            return

    # Adicionar data de fim fixa (6 meses após o início)
    # Salvar as alterações
