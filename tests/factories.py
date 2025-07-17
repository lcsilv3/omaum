"""
Factories otimizadas para testes usando factory_boy.
"""

try:
    import factory
    import factory.fuzzy
except ImportError:
    # Se factory_boy não estiver disponível, criar classes mock
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
            
            class FuzzyDecimal:
                def __init__(self, low, high, precision=2):
                    self.low = low
                    self.high = high
                    self.precision = precision

from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from datetime import date, timedelta

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
        django_get_or_create = ('username',)
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_staff = False
    is_superuser = False
    
    @factory.post_generation
    def password(self, create, extracted):
        if not create:
            return
        password = extracted or 'testpassword'
        self.set_password(password)
        self.save()


class AdminUserFactory(UserFactory):
    """Factory para usuário administrador."""
    
    is_staff = True
    is_superuser = True


# Factories básicas para modelos mock
class AlunoFactory(factory.django.DjangoModelFactory):
    """Factory para Aluno."""
    
    class Meta:
        model = Aluno
        django_get_or_create = ('cpf',) if hasattr(Aluno, 'objects') else ()
    
    nome = factory.Faker('name')
    cpf = factory.Faker('cpf', locale='pt_BR')
    email = factory.Faker('email')
    telefone = factory.Faker('phone_number')
    endereco = factory.Faker('address')
    data_nascimento = factory.Faker('date_of_birth', minimum_age=18, maximum_age=65)
    ativo = True
    data_cadastro = factory.LazyFunction(timezone.now)
    
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
    
    nome = factory.Faker('sentence', nb_words=3)
    descricao = factory.Faker('text', max_nb_chars=500)
    carga_horaria = factory.fuzzy.FuzzyInteger(20, 200)
    preco = factory.fuzzy.FuzzyDecimal(100.0, 1000.0, 2)
    ativo = True
    data_criacao = factory.LazyFunction(timezone.now)


class MatriculaFactory(factory.django.DjangoModelFactory):
    """Factory para Matricula."""
    
    class Meta:
        model = Matricula
    
    aluno = factory.SubFactory(AlunoFactory)
    curso = factory.SubFactory(CursoFactory)
    data_matricula = factory.LazyFunction(timezone.now)
    valor_pago = factory.fuzzy.FuzzyDecimal(0.0, 1000.0, 2)
    observacoes = factory.Faker('text', max_nb_chars=300)
    ativo = True


class TurmaFactory(factory.django.DjangoModelFactory):
    """Factory para Turma."""
    
    class Meta:
        model = Turma
    
    nome = factory.Faker('sentence', nb_words=2)
    curso = factory.SubFactory(CursoFactory)
    data_inicio = factory.LazyFunction(lambda: timezone.now().date())
    data_fim = factory.LazyFunction(lambda: timezone.now().date() + timedelta(days=90))
    horario = factory.Faker('time')
    capacidade_maxima = factory.fuzzy.FuzzyInteger(10, 50)
    professor = factory.Faker('name')
    local = factory.Faker('address')
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
    observacoes = factory.Faker('text', max_nb_chars=200)
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
        if hasattr(Matricula, 'objects') and Matricula.objects.filter(
            aluno=self.aluno,
            curso=self.turma.curso
        ).exists():
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
            'curso': curso,
            'turma': turma,
            'alunos': alunos,
            'matriculas': matriculas,
            'presencas': presencas
        }
    
    @classmethod
    def criar_cenario_complexo(cls):
        """Cria um cenário complexo com múltiplos cursos e turmas."""
        cenarios = []
        
        for i in range(3):
            cenario = cls.criar_cenario_basico()
            cenarios.append(cenario)
        
        return cenarios
    cpf = factory.Sequence(lambda n: f'{n:011d}')
    nome = factory.Faker('name')
    email = factory.Faker('email')
    data_nascimento = factory.Faker(
        'date_of_birth', minimum_age=18, maximum_age=70
    )
    sexo = factory.Iterator(['M', 'F'])
    situacao = 'ativo'
    nacionalidade = factory.LazyFunction(
        lambda: random.choice(
            ['Brasileira', 'Portuguesa', 'Italiana', 'Espanhola']
        )
    )
    naturalidade = factory.Faker('city')
    rua = factory.Faker('street_name')
    numero_imovel = factory.LazyFunction(lambda: str(random.randint(1, 999)))
    bairro = factory.Faker('city_suffix')
    cidade = factory.Faker('city')
    estado = factory.Faker('state_abbr')
    cep = factory.LazyFunction(
        lambda: f'{random.randint(10000, 99999)}-{random.randint(100, 999)}'
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Chama o serviço criar_aluno para criar a instância do aluno.""" 
        foto_url = kwargs.pop('foto_url', None)
        aluno = aluno_service.criar_aluno(kwargs, foto_url=foto_url)
        if not aluno:
            # Lança uma exceção se o serviço falhar em criar o aluno
            raise Exception(
                f"O serviço criar_aluno falhou com os seguintes dados: {kwargs}"
            )
        return aluno


class TurmaFactory(DjangoModelFactory):
    """Factory para criar turmas."""
    
    class Meta:
        model = Turma
    
    nome = factory.Sequence(lambda n: f'Turma {n}')
    codigo = factory.Sequence(lambda n: f'T{n:03d}')
    data_inicio = factory.LazyFunction(timezone.now)
    status = 'A'
    
    @factory.post_generation
    def add_details(self, create, extracted, **kwargs):
        if not create:
            return
        
        # Adicionar data de fim aleatória (entre 6 meses e 1 ano após o início)
        dias_aleatorios = random.randint(180, 365)
        self.data_fim = self.data_inicio + timedelta(days=dias_aleatorios)
        
        # Salvar as alterações
        self.save()


class AtividadeFactory(DjangoModelFactory):
    """Factory para criar atividades."""

    class Meta:
        model = Atividade

    nome = factory.Sequence(lambda n: f'Atividade {n}')
    descricao = factory.Faker('paragraph')
    data_inicio = factory.LazyFunction(
        lambda: timezone.now().date() + timedelta(days=random.randint(1, 30))
    )
    hora_inicio = factory.LazyFunction(
        lambda: timezone.now().time()
    )
    responsavel = factory.Faker('name')
    local = factory.Sequence(lambda n: f'Sala {n}')
    tipo_atividade = factory.Iterator(
        ['AULA', 'PALESTRA', 'WORKSHOP', 'SEMINARIO', 'OUTRO']
    )
    status = factory.Iterator(
        ['PENDENTE', 'CONFIRMADA', 'REALIZADA', 'CANCELADA']
    )

    @factory.post_generation
    def turmas(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            # Adicionar turmas específicas
            for turma in extracted:
                self.turmas.add(turma)
        else:
            # Adicionar turmas aleatórias
            turmas_count = random.randint(1, 3)
            turmas = TurmaFactory.create_batch(turmas_count)
            for turma in turmas:
                self.turmas.add(turma)
    
    @factory.post_generation
    def add_details(self, create, extracted, **kwargs):
        if not create:
            return
        
        # Adicionar data de fim aleatória (entre 1 e 5 dias após o início)
        dias_aleatorios = random.randint(1, 5)
        self.data_fim = self.data_inicio + timedelta(days=dias_aleatorios)
        
        # Salvar as alterações
        self.save()