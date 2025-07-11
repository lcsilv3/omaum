import factory
from factory.django import DjangoModelFactory
from django.utils import timezone
from alunos import services as aluno_service  # Alterado
from turmas.models import Turma
from atividades.models import Atividade
from django.contrib.auth.models import User
import random
from datetime import timedelta

class UserFactory(DjangoModelFactory):
    """Factory para criar usuários."""
    
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_active = True

class AlunoFactory(factory.Factory):
    """Factory para criar alunos usando a camada de serviço."""

    class Meta:
        # Não estamos mais criando um modelo Aluno diretamente.
        # A fábrica agora chama a camada de serviço.
        pass

    # Definição dos campos para o dicionário 'aluno_data'
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