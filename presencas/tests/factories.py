"""
Factories para criação de dados de teste usando factory_boy.
Facilita a criação de objetos para testes com dados realistas.
"""

import factory
from factory.django import DjangoModelFactory
from factory import SubFactory, LazyAttribute, Sequence, Faker
from datetime import date, datetime, timedelta
from decimal import Decimal
import random

from django.contrib.auth import get_user_model
from presencas.models import (
    Presenca, PresencaDetalhada, ConfiguracaoPresenca,
    TotalAtividadeMes, ObservacaoPresenca, AgendamentoRelatorio
)
from alunos.models import Aluno
from turmas.models import Turma
from atividades.models import Atividade
from cursos.models import Curso

User = get_user_model()


class UserFactory(DjangoModelFactory):
    """Factory para criação de usuários."""
    
    class Meta:
        model = User
    
    username = Sequence(lambda n: f"user{n}")
    email = Faker('email')
    first_name = Faker('first_name', locale='pt_BR')
    last_name = Faker('last_name', locale='pt_BR')
    is_active = True
    
    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return
        
        password = extracted or 'testpass123'
        self.set_password(password)
        self.save()


class CursoFactory(DjangoModelFactory):
    """Factory para criação de cursos."""
    
    class Meta:
        model = Curso
    
    nome = Faker('sentence', nb_words=3, locale='pt_BR')
    descricao = Faker('text', max_nb_chars=200, locale='pt_BR')
    ativo = True


class TurmaFactory(DjangoModelFactory):
    """Factory para criação de turmas."""
    
    class Meta:
        model = Turma
    
    nome = Sequence(lambda n: f"Turma {chr(65 + n % 26)}")  # A, B, C...
    ano = factory.LazyFunction(lambda: datetime.now().year)
    semestre = factory.Faker('random_element', elements=[1, 2])
    perc_carencia = factory.Faker('random_int', min=60, max=90)
    
    # Relacionamentos opcionais
    curso = SubFactory(CursoFactory)


class AlunoFactory(DjangoModelFactory):
    """Factory para criação de alunos."""
    
    class Meta:
        model = Aluno
    
    nome = Faker('name', locale='pt_BR')
    cpf = Sequence(lambda n: f"{11111111111 + n}")  # CPFs sequenciais
    data_nascimento = Faker('date_between', start_date='-30y', end_date='-18y')
    email = Faker('email')
    telefone = Faker('phone_number', locale='pt_BR')
    endereco = Faker('address', locale='pt_BR')


class AtividadeFactory(DjangoModelFactory):
    """Factory para criação de atividades."""
    
    class Meta:
        model = Atividade
    
    nome = Faker('sentence', nb_words=2, locale='pt_BR')
    descricao = Faker('text', max_nb_chars=200, locale='pt_BR')
    tipo = factory.Faker('random_element', elements=['academica', 'ritualistica'])
    ativa = True


class PresencaFactory(DjangoModelFactory):
    """Factory para criação de presenças básicas."""
    
    class Meta:
        model = Presenca
    
    aluno = SubFactory(AlunoFactory)
    turma = SubFactory(TurmaFactory)
    atividade = SubFactory(AtividadeFactory)
    data = Faker('date_between', start_date='-1y', end_date='today')
    presente = factory.Faker('boolean', chance_of_getting_true=80)
    registrado_por = Faker('name', locale='pt_BR')
    
    # Condicional: justificativa apenas se ausente
    justificativa = factory.LazyAttribute(
        lambda obj: Faker('sentence', locale='pt_BR').generate()
        if not obj.presente else ''
    )


class PresencaDetalhadaFactory(DjangoModelFactory):
    """Factory para criação de presenças detalhadas."""
    
    class Meta:
        model = PresencaDetalhada
    
    aluno = SubFactory(AlunoFactory)
    turma = SubFactory(TurmaFactory)
    atividade = SubFactory(AtividadeFactory)
    periodo = factory.LazyFunction(
        lambda: date(datetime.now().year, random.randint(1, 12), 1)
    )
    
    # Campos calculados de forma realista
    convocacoes = factory.Faker('random_int', min=8, max=20)
    presencas = factory.LazyAttribute(
        lambda obj: random.randint(
            int(obj.convocacoes * 0.6),  # Mínimo 60%
            obj.convocacoes  # Máximo 100%
        )
    )
    faltas = factory.LazyAttribute(
        lambda obj: obj.convocacoes - obj.presencas
    )
    voluntario_extra = factory.Faker('random_int', min=0, max=3)
    voluntario_simples = factory.Faker('random_int', min=0, max=5)
    
    registrado_por = Faker('name', locale='pt_BR')


class ConfiguracaoPresencaFactory(DjangoModelFactory):
    """Factory para criação de configurações de presença."""
    
    class Meta:
        model = ConfiguracaoPresenca
    
    turma = SubFactory(TurmaFactory)
    atividade = SubFactory(AtividadeFactory)
    
    # Limites progressivos de carência
    limite_carencia_0_25 = 0
    limite_carencia_26_50 = factory.Faker('random_int', min=1, max=2)
    limite_carencia_51_75 = factory.Faker('random_int', min=2, max=4)
    limite_carencia_76_100 = factory.Faker('random_int', min=3, max=6)
    
    obrigatoria = factory.Faker('boolean', chance_of_getting_true=80)
    peso_calculo = factory.LazyFunction(
        lambda: Decimal(str(round(random.uniform(0.5, 2.0), 2)))
    )
    ativo = True
    registrado_por = Faker('name', locale='pt_BR')


class TotalAtividadeMesFactory(DjangoModelFactory):
    """Factory para criação de totais de atividade por mês."""
    
    class Meta:
        model = TotalAtividadeMes
    
    atividade = SubFactory(AtividadeFactory)
    turma = SubFactory(TurmaFactory)
    ano = factory.LazyFunction(lambda: datetime.now().year)
    mes = factory.Faker('random_int', min=1, max=12)
    qtd_ativ_mes = factory.Faker('random_int', min=5, max=25)
    registrado_por = Faker('name', locale='pt_BR')


class ObservacaoPresencaFactory(DjangoModelFactory):
    """Factory para criação de observações de presença."""
    
    class Meta:
        model = ObservacaoPresenca
    
    turma = SubFactory(TurmaFactory)
    data = Faker('date_between', start_date='-6m', end_date='today')
    texto = Faker('text', max_nb_chars=300, locale='pt_BR')
    registrado_por = Faker('name', locale='pt_BR')
    
    # Aluno opcional (70% das observações são específicas de aluno)
    aluno = factory.Maybe(
        'tem_aluno_especifico',
        yes_declaration=SubFactory(AlunoFactory),
        no_declaration=None
    )
    tem_aluno_especifico = factory.Faker('boolean', chance_of_getting_true=70)
    
    # Atividade opcional (60% das observações são específicas de atividade)
    atividade = factory.Maybe(
        'tem_atividade_especifica',
        yes_declaration=SubFactory(AtividadeFactory),
        no_declaration=None
    )
    tem_atividade_especifica = factory.Faker('boolean', chance_of_getting_true=60)


class AgendamentoRelatorioFactory(DjangoModelFactory):
    """Factory para criação de agendamentos de relatório."""
    
    class Meta:
        model = AgendamentoRelatorio
    
    nome = Faker('sentence', nb_words=3, locale='pt_BR')
    usuario = SubFactory(UserFactory)
    
    formato = factory.Faker('random_element', elements=[
        'excel_basico', 'excel_avancado', 'excel_graficos', 'csv', 'pdf_simples'
    ])
    
    template = factory.Faker('random_element', elements=[
        'consolidado_geral', 'por_turma', 'por_curso', 'estatisticas_executivas'
    ])
    
    periodo = factory.Faker('random_element', elements=[
        'atual', 'ultimo_mes', 'ultimo_trimestre', 'ano_atual'
    ])
    
    frequencia = factory.Faker('random_element', elements=[
        'semanal', 'mensal', 'trimestral'
    ])
    
    # Campos condicionais baseados na frequência
    dia_semana = factory.Maybe(
        'frequencia_semanal',
        yes_declaration=factory.Faker('random_int', min=0, max=6),
        no_declaration=None
    )
    frequencia_semanal = factory.LazyAttribute(
        lambda obj: obj.frequencia == 'semanal'
    )
    
    dia_mes = factory.Maybe(
        'frequencia_mensal_ou_maior',
        yes_declaration=factory.Faker('random_int', min=1, max=28),
        no_declaration=None
    )
    frequencia_mensal_ou_maior = factory.LazyAttribute(
        lambda obj: obj.frequencia in ['mensal', 'trimestral', 'semestral', 'anual']
    )
    
    hora_execucao = Faker('time')
    emails_destino = Faker('email')
    ativo = True
    
    # Datas de execução
    proxima_execucao = factory.LazyFunction(
        lambda: datetime.now() + timedelta(days=random.randint(1, 30))
    )


# Factories compostas para cenários específicos

class PresencaCompletoFactory(PresencaFactory):
    """Factory para presença com todos os relacionamentos preenchidos."""
    
    aluno = SubFactory(AlunoFactory)
    turma = SubFactory(TurmaFactory)
    atividade = SubFactory(AtividadeFactory)
    justificativa = factory.LazyAttribute(
        lambda obj: Faker('sentence', locale='pt_BR').generate()
        if not obj.presente else ''
    )


class TurmaComAlunosFactory(TurmaFactory):
    """Factory para turma com alunos já matriculados."""
    
    @factory.post_generation
    def alunos(self, create, extracted, **kwargs):
        if not create:
            return
        
        quantidade = extracted or random.randint(15, 30)
        
        for _ in range(quantidade):
            aluno = AlunoFactory()
            # Aqui seria criada a matrícula, dependendo do modelo
            # Matricula.objects.create(aluno=aluno, turma=self)


class ConsolidadoCompletoFactory:
    """Factory composta para criar um consolidado completo de teste."""
    
    @staticmethod
    def create(turma=None, alunos_count=20, meses=6):
        """
        Cria um consolidado completo com turma, alunos e presenças.
        
        Args:
            turma: Turma existente ou None para criar nova
            alunos_count: Número de alunos a criar
            meses: Número de meses de presenças a criar
        
        Returns:
            dict com turma, alunos e presenças criados
        """
        if not turma:
            turma = TurmaFactory()
        
        atividade = AtividadeFactory()
        
        # Criar configuração de presença
        config = ConfiguracaoPresencaFactory(
            turma=turma,
            atividade=atividade
        )
        
        alunos = []
        presencas = []
        
        for _ in range(alunos_count):
            aluno = AlunoFactory()
            alunos.append(aluno)
            
            # Criar presenças para cada mês
            for mes in range(1, meses + 1):
                presenca = PresencaDetalhadaFactory(
                    aluno=aluno,
                    turma=turma,
                    atividade=atividade,
                    periodo=date(datetime.now().year, mes, 1)
                )
                presencas.append(presenca)
        
        return {
            'turma': turma,
            'atividade': atividade,
            'configuracao': config,
            'alunos': alunos,
            'presencas': presencas
        }


# Traits para variações específicas

class PresencaPerfeita(PresencaDetalhadaFactory):
    """Presença com 100% de comparecimento."""
    
    convocacoes = 20
    presencas = 20
    faltas = 0
    voluntario_extra = factory.Faker('random_int', min=0, max=3)
    voluntario_simples = factory.Faker('random_int', min=0, max=5)


class PresencaCritica(PresencaDetalhadaFactory):
    """Presença com baixo comparecimento."""
    
    convocacoes = 20
    presencas = factory.Faker('random_int', min=1, max=10)  # Máximo 50%
    faltas = factory.LazyAttribute(lambda obj: obj.convocacoes - obj.presencas)
    voluntario_extra = 0
    voluntario_simples = 0


class AlunoProblematico(AlunoFactory):
    """Aluno com histórico de problemas de presença."""
    
    @factory.post_generation
    def criar_presencas_problematicas(self, create, extracted, **kwargs):
        if not create:
            return
        
        turma = TurmaFactory()
        atividade = AtividadeFactory()
        
        # Criar várias presenças com baixo comparecimento
        for mes in range(1, 7):
            PresencaCritica(
                aluno=self,
                turma=turma,
                atividade=atividade,
                periodo=date(datetime.now().year, mes, 1)
            )


# Sequências personalizadas para testes específicos

class CPFSequence:
    """Gerador de CPFs válidos sequenciais para testes."""
    
    def __init__(self):
        self.counter = 11111111111
    
    def __call__(self):
        cpf = str(self.counter)
        self.counter += 1
        return cpf


# Funções auxiliares para criação em lote

def criar_turma_completa(nome=None, alunos_count=25):
    """Cria uma turma completa com alunos e presenças."""
    turma = TurmaFactory(nome=nome or f"Turma Teste {random.randint(1, 100)}")
    atividade = AtividadeFactory()
    
    alunos = AlunoFactory.create_batch(alunos_count)
    
    presencas = []
    for aluno in alunos:
        for mes in range(1, 7):  # 6 meses
            presenca = PresencaDetalhadaFactory(
                aluno=aluno,
                turma=turma,
                atividade=atividade,
                periodo=date(datetime.now().year, mes, 1)
            )
            presencas.append(presenca)
    
    return {
        'turma': turma,
        'atividade': atividade,
        'alunos': alunos,
        'presencas': presencas
    }


def criar_dataset_performance(turmas_count=5, alunos_por_turma=50):
    """Cria dataset grande para testes de performance."""
    datasets = []
    
    for _ in range(turmas_count):
        dataset = criar_turma_completa(alunos_count=alunos_por_turma)
        datasets.append(dataset)
    
    return datasets
