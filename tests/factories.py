import factory
from factory.django import DjangoModelFactory
from django.utils import timezone
from alunos.models import Aluno
from turmas.models import Turma
from atividades.models import AtividadeAcademica, AtividadeRitualistica
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

class AlunoFactory(DjangoModelFactory):
    """Factory para criar alunos."""
    
    class Meta:
        model = Aluno
    
    cpf = factory.Sequence(lambda n: f'{n:011d}')
    nome = factory.Faker('name')
    email = factory.Faker('email')
    data_nascimento = factory.Faker('date_of_birth', minimum_age=18, maximum_age=70)
    sexo = factory.Iterator(['M', 'F'])
    situacao = 'ativo'
    
    @factory.post_generation
    def add_details(self, create, extracted, **kwargs):
        if not create:
            return
        
        # Adicionar detalhes aleatórios
        self.nacionalidade = random.choice(['Brasileira', 'Portuguesa', 'Italiana', 'Espanhola'])
        self.naturalidade = factory.Faker('city').generate({})
        self.rua = factory.Faker('street_name').generate({})
        self.numero_imovel = str(random.randint(1, 999))
        self.bairro = factory.Faker('city_suffix').generate({})
        self.cidade = factory.Faker('city').generate({})
        self.estado = factory.Faker('state_abbr').generate({})
        self.cep = f'{random.randint(10000, 99999)}-{random.randint(100, 999)}'
        
        # Salvar as alterações
        self.save()

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

class AtividadeAcademicaFactory(DjangoModelFactory):
    """Factory para criar atividades acadêmicas."""
    
    class Meta:
        model = AtividadeAcademica
    
    nome = factory.Sequence(lambda n: f'Atividade Acadêmica {n}')
    descricao = factory.Faker('paragraph')
    data_inicio = factory.LazyFunction(lambda: timezone.now() + timedelta(days=random.randint(1, 30)))
    responsavel = factory.Faker('name')
    local = factory.Sequence(lambda n: f'Sala {n}')
    tipo_atividade = factory.Iterator(['aula', 'palestra', 'workshop', 'seminario', 'outro'])
    status = factory.Iterator(['agendada', 'em_andamento', 'concluida', 'cancelada'])
    
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

class AtividadeRitualisticaFactory(DjangoModelFactory):
    """Factory para criar atividades ritualísticas."""
    
    class Meta:
        model = AtividadeRitualistica
    
    nome = factory.Sequence(lambda n: f'Ritual {n}')
    descricao = factory.Faker('paragraph')
    data = factory.LazyFunction(lambda: timezone.now().date() + timedelta(days=random.randint(1, 30)))
    hora_inicio = factory.LazyFunction(lambda: f'{random.randint(18, 20)}:00')
    hora_fim = factory.LazyFunction(lambda: f'{random.randint(21, 23)}:00')
    local = factory.Iterator(['Templo Principal', 'Sala de Rituais', 'Salão Nobre'])
    
    @factory.post_generation
    def turma(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            # Usar a turma especificada
            self.turma = extracted
        else:
            # Criar uma nova turma
            self.turma = TurmaFactory.create()
        
        # Salvar as alterações
        self.save()
    
    @factory.post_generation
    def participantes(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            # Adicionar participantes específicos
            for aluno in extracted:
                self.participantes.add(aluno)
        else:
            # Adicionar participantes aleatórios
            alunos_count = random.randint(5, 15)
            alunos = AlunoFactory.create_batch(alunos_count)
            for aluno in alunos:
                self.participantes.add(aluno)