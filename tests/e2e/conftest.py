import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from alunos import services as aluno_service
from turmas.models import Turma
from atividades.models import AtividadeAcademica, AtividadeRitualistica
from django.utils import timezone

@pytest.fixture(scope='session')
def browser():
    """Configuração do navegador para testes E2E."""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Executar sem interface gráfica
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(10)
    
    yield browser
    
    browser.quit()

@pytest.fixture
def live_server_with_data(live_server):
    """Configura o servidor de teste com dados iniciais."""
    # Criar um usuário para autenticação
    user = User.objects.create_user(
        username='testuser',
        password='testpassword',
        email='test@example.com'
    )
    
    # Criar alguns alunos usando o serviço
    aluno_data1 = {
        "cpf": "12345678900",
        "nome": "João da Silva",
        "email": "joao@exemplo.com",
        "data_nascimento": "1990-01-01",
        "sexo": "M",
        "situacao": "ativo"
    }
    aluno1 = aluno_service.criar_aluno(aluno_data1)
    
    aluno_data2 = {
        "cpf": "98765432100",
        "nome": "Maria Souza",
        "email": "maria@exemplo.com",
        "data_nascimento": "1992-05-15",
        "sexo": "F",
        "situacao": "ativo"
    }
    aluno2 = aluno_service.criar_aluno(aluno_data2)
    
    # Criar algumas turmas
    turma1 = Turma.objects.create(
        nome="Turma de Filosofia 2023",
        codigo="FIL-2023",
        data_inicio=timezone.now().date(),
        status="A"
    )
    
    turma2 = Turma.objects.create(
        nome="Turma de História 2023",
        codigo="HIS-2023",
        data_inicio=timezone.now().date(),
        status="A"
    )
    
    # Criar algumas atividades
    atividade1 = AtividadeAcademica.objects.create(
        nome="Aula de Filosofia",
        descricao="Introdução à Filosofia",
        data_inicio=timezone.now(),
        responsavel="Prof. Silva",
        tipo_atividade="aula",
        status="agendada"
    )
    atividade1.turmas.add(turma1)
    
    atividade2 = AtividadeRitualistica.objects.create(
        nome="Ritual de Iniciação",
        descricao="Ritual para novos membros",
        data=timezone.now().date(),
        hora_inicio="19:00",
        hora_fim="21:00",
        local="Templo Principal",
        turma=turma1
    )
    
    return live_server