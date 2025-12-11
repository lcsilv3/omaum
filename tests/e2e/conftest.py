import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from django.contrib.auth.models import User
from alunos import services as aluno_service
from turmas.models import Turma
from atividades.models import Atividade
from django.utils import timezone


CHROME_BINARY = "/usr/bin/chromium"
if not os.path.exists(CHROME_BINARY):
    CHROME_BINARY = "/usr/bin/chromium-browser"

CHROMEDRIVER_BINARY = "/usr/bin/chromedriver"


@pytest.fixture(scope="session")
def browser():
    """Configuração do navegador para testes E2E."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Executar sem interface gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = CHROME_BINARY

    service = Service(executable_path=CHROMEDRIVER_BINARY)
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.implicitly_wait(10)

    yield browser

    browser.quit()


@pytest.fixture
def live_server_with_data(live_server):
    """Configura o servidor de teste com dados iniciais."""
    # Criar usuários padrão usados nos testes
    users = [
        ("desenv", "desenv123", True),
        ("testuser", "testpassword", False),
        ("lcsilv3", "iG356900", False),
    ]

    for username, password, is_superuser in users:
        if not User.objects.filter(username=username).exists():
            if is_superuser:
                User.objects.create_superuser(
                    username=username,
                    password=password,
                    email="desenv@example.com",
                )
            else:
                User.objects.create_user(
                    username=username, password=password, email="test@example.com"
                )

    # Criar alguns alunos usando o serviço
    aluno_data1 = {
        "cpf": "12345678900",
        "nome": "João da Silva",
        "email": "joao@exemplo.com",
        "data_nascimento": "1990-01-01",
        "sexo": "M",
        "situacao": "ativo",
    }
    aluno_service.criar_aluno(aluno_data1)

    aluno_data2 = {
        "cpf": "98765432100",
        "nome": "Maria Souza",
        "email": "maria@exemplo.com",
        "data_nascimento": "1992-05-15",
        "sexo": "F",
        "situacao": "ativo",
    }
    aluno_service.criar_aluno(aluno_data2)

    # Criar um curso para as turmas
    from cursos.models import Curso

    curso = Curso.objects.create(
        nome="Curso de Filosofia", descricao="Curso de Filosofia", ativo=True
    )

    turma1 = Turma.objects.create(
        nome="Turma de Filosofia 2023", curso=curso, status="A"
    )
    Turma.objects.create(nome="Turma de História 2023", curso=curso, status="A")

    # Criar algumas atividades
    atividade1 = Atividade.objects.create(
        nome="Aula de Filosofia",
        descricao="Introdução à Filosofia",
        tipo_atividade="AULA",
        data_inicio=timezone.now().date(),
        hora_inicio=timezone.now().time(),
        responsavel="Prof. Silva",
        status="CONFIRMADA",
    )
    atividade1.turmas.add(turma1)

    Atividade.objects.create(
        nome="Ritual de Iniciação",
        descricao="Ritual para novos membros",
        tipo_atividade="OUTRO",
        data_inicio=timezone.now().date(),
        hora_inicio=timezone.now().time(),
        data_fim=timezone.now().date(),
        responsavel="Teste",
        local="Templo Principal",
        status="CONFIRMADA",
    )

    return live_server
