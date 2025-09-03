import sys
import os

# Obtenha o caminho absoluto do diretório onde o script está localizado (scripts)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Obtenha o caminho absoluto do diretório raiz do projeto (um nível acima de scripts)
project_root = os.path.dirname(script_dir)
# Adicione o diretório raiz do projeto ao sys.path
sys.path.append(project_root)

# Agora, configure o ambiente Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
import django

django.setup()

from alunos.models import Aluno, TipoCodigo, Codigo, RegistroHistorico
from cursos.models import Curso
from turmas.models import Turma
from matriculas.models import Matricula
import random
import requests
from datetime import date, time, timedelta
from django.core.files import File

# Listas de nomes, sobrenomes e cidades para gerar dados variados
nomes = [
    "Ana",
    "João",
    "Maria",
    "Pedro",
    "Carla",
    "Lucas",
    "Fernanda",
    "Rafael",
    "Juliana",
    "Bruno",
    "Camila",
    "Rodrigo",
    "Patrícia",
    "Marcelo",
    "Aline",
    "Gustavo",
    "Mariana",
    "Felipe",
    "Daniela",
    "André",
]

sobrenomes = [
    "Silva",
    "Santos",
    "Oliveira",
    "Souza",
    "Pereira",
    "Lima",
    "Costa",
    "Ferreira",
    "Rodrigues",
    "Almeida",
    "Nascimento",
    "Carvalho",
    "Gomes",
    "Martins",
    "Araújo",
    "Ribeiro",
    "Mendes",
    "Barbosa",
    "Cardoso",
    "Rocha",
]

cidades = [
    "São Paulo",
    "Rio de Janeiro",
    "Belo Horizonte",
    "Salvador",
    "Fortaleza",
    "Brasília",
    "Curitiba",
    "Recife",
    "Porto Alegre",
    "Manaus",
    "Belém",
    "Goiânia",
    "Guarulhos",
    "Campinas",
    "São Luís",
    "Maceió",
    "Natal",
    "Teresina",
    "João Pessoa",
    "Florianópolis",
]

estados = [
    "SP",
    "RJ",
    "MG",
    "BA",
    "CE",
    "DF",
    "PR",
    "PE",
    "RS",
    "AM",
    "PA",
    "GO",
    "SP",
    "SP",
    "MA",
    "AL",
    "RN",
    "PI",
    "PB",
    "SC",
]

bairros = [
    "Centro",
    "Jardim Paulista",
    "Copacabana",
    "Savassi",
    "Barra",
    "Asa Norte",
    "Batel",
    "Boa Viagem",
    "Moinhos de Vento",
    "Adrianópolis",
    "Nazaré",
    "Setor Bueno",
    "Vila Madalena",
    "Cambuí",
    "Renascença",
    "Ponta Verde",
    "Petrópolis",
    "Jóquei",
    "Manaíra",
    "Trindade",
]

tipos_sanguineos = ["A", "B", "AB", "O"]
fatores_rh = ["+", "-"]
sexos = ["M", "F"]

convenios = [
    "Unimed",
    "Amil",
    "SulAmérica",
    "Bradesco Saúde",
    "NotreDame Intermédica",
    "Hapvida",
    "Golden Cross",
    "Medial Saúde",
    "Porto Seguro Saúde",
    "Cassi",
]

hospitais = [
    "Hospital Albert Einstein",
    "Hospital Sírio-Libanês",
    "Hospital Samaritano",
    "Hospital São Luiz",
    "Hospital Moinhos de Vento",
    "Hospital Português",
    "Hospital Santa Joana",
    "Hospital Mater Dei",
    "Hospital São Lucas",
    "Hospital Esperança",
]


# Função para gerar CPF único
def gerar_cpf_unico():
    while True:
        cpf = "".join([str(random.randint(0, 9)) for _ in range(11)])
        if not Aluno.objects.filter(cpf=cpf).exists():
            return cpf


def gerar_email_unico(nome, sobrenome):
    base_email = f"{nome.lower()}.{sobrenome.lower()}@exemplo.com"
    if Aluno.objects.filter(email=base_email).exists():
        return (
            f"{nome.lower()}.{sobrenome.lower()}{random.randint(1, 999)}" "@exemplo.com"
        )
    return base_email


def baixar_foto_aleatoria(sexo, nome, sobrenome):
    genero = "men" if sexo == "M" else "women"
    numero = random.randint(0, 99)
    url = f"https://randomuser.me/api/portraits/{genero}/{numero}.jpg"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            filename = (
                f"temp_{nome.lower()}_{sobrenome.lower()}_{random.randint(1,9999)}.jpg"
            )
            with open(filename, "wb") as f:
                f.write(response.content)
            return filename
    except requests.RequestException:
        return None
    return None


def popular_codigos():
    tipos_e_codigos = {
        "Iniciação": {
            "descricao": "Registros relacionados a graus e etapas iniciáticas.",
            "codigos": ["Iniciação 1", "Iniciação 2", "Iniciação 3"],
        },
        "Cargo": {
            "descricao": "Cargos e funções desempenhadas na organização.",
            "codigos": ["Líder de Grupo", "Coordenador de Ala", "Secretário"],
        },
        "Punição": {
            "descricao": "Sanções e medidas disciplinares aplicadas.",
            "codigos": ["Advertência Leve", "Suspensão Curta", "Advertência Grave"],
        },
    }
    for nome_tipo, dados in tipos_e_codigos.items():
        tipo, _ = TipoCodigo.objects.get_or_create(
            nome=nome_tipo, defaults={"descricao": dados["descricao"]}
        )
        for nome_codigo in dados["codigos"]:
            Codigo.objects.get_or_create(
                tipo_codigo=tipo,
                nome=nome_codigo,
                defaults={"descricao": f"Descrição padrão para {nome_codigo}"},
            )
    print("Tipos de Códigos e Códigos populados com sucesso!")


def popular_cursos_e_turmas():
    """Cria cursos e turmas de exemplo se não existirem."""
    cursos_data = [
        ("Curso Básico de Doutrina", "Fundamentos da doutrina e filosofia."),
        ("Estudos Avançados de Rituais", "Aprofundamento nas práticas ritualísticas."),
        ("História da Ordem", "Estudo cronológico da história da organização."),
        ("Liderança e Gestão", "Capacitação para futuras lideranças."),
        ("Filosofia Hermética", "Estudos sobre o hermetismo e seus princípios."),
        ("Pré-iniciático", "Curso de preparação para novos membros."),
    ]

    if Curso.objects.exists():
        print("Cursos já existem. Pulando a criação.")
    else:
        for nome, desc in cursos_data:
            curso, created = Curso.objects.get_or_create(
                nome=nome, defaults={"descricao": desc, "ativo": True}
            )
            if created:
                # Para cada curso, cria de 1 a 3 turmas
                for i in range(random.randint(1, 3)):
                    ano_atual = date.today().year
                    Turma.objects.create(
                        curso=curso,
                        nome=f"Turma {i+1} - {curso.nome} ({ano_atual})",
                        # O campo 'ativo' não existe mais diretamente no modelo Turma,
                        # o status é controlado pelo campo 'status'.
                        # 'A' para Ativa.
                        status="A",
                    )
        print("Cursos e Turmas populados com sucesso!")


# --- INÍCIO DA EXECUÇÃO DO SCRIPT ---

# 1. Popular pré-requisitos
popular_codigos()
popular_cursos_e_turmas()

# 2. Obter dados disponíveis para o loop
codigos_disponiveis = list(Codigo.objects.all())
turmas_disponiveis = list(Turma.objects.filter(status="A"))
count = 0
alunos_criados = 0
matriculas_criadas = 0

# Aumentando a quantidade para 250 para garantir massa de teste robusta
QUANTIDADE_ALUNOS = 250
print(f"\nIniciando a criação de {QUANTIDADE_ALUNOS} alunos...")

for i in range(QUANTIDADE_ALUNOS):
    try:
        nome_idx = random.randint(0, len(nomes) - 1)
        sobrenome_idx = random.randint(0, len(sobrenomes) - 1)
        cidade_idx = random.randint(0, len(cidades) - 1)
        nome_completo = f"{nomes[nome_idx]} {sobrenomes[sobrenome_idx]}"
        ano_nascimento = random.randint(1970, 2000)
        mes_nascimento = random.randint(1, 12)
        dia_nascimento = random.randint(1, 28)
        hora_nascimento = random.randint(0, 23)
        minuto_nascimento = random.randint(0, 59)
        sexo = random.choice(sexos)
        aluno_dados = {
            "cpf": gerar_cpf_unico(),
            "nome": nome_completo,
            "data_nascimento": date(ano_nascimento, mes_nascimento, dia_nascimento),
            "hora_nascimento": time(hora_nascimento, minuto_nascimento),
            "email": gerar_email_unico(nomes[nome_idx], sobrenomes[sobrenome_idx]),
            "sexo": sexo,
            "nacionalidade": "Brasileira",
            "naturalidade": cidades[cidade_idx],
            "rua": f"Rua {random.choice(sobrenomes)} {random.randint(1, 100)}",
            "numero_imovel": str(random.randint(1, 999)),
            "complemento": (
                f"Apto {random.randint(1, 100)}" if random.random() > 0.5 else ""
            ),
            "bairro": bairros[cidade_idx % len(bairros)],
            "cidade": cidades[cidade_idx],
            "estado": estados[cidade_idx % len(estados)],
            "cep": f"{random.randint(10000, 99999)}{random.randint(100, 999)}",
            "nome_primeiro_contato": (
                f"{random.choice(nomes)} {random.choice(sobrenomes)}"
            ),
            "celular_primeiro_contato": (
                f"{random.randint(10, 99)}9" f"{random.randint(10000000, 99999999)}"
            ),
            "tipo_relacionamento_primeiro_contato": random.choice(
                ["Pai", "Mãe", "Irmão", "Irmã", "Cônjuge"]
            ),
            "nome_segundo_contato": (
                f"{random.choice(nomes)} {random.choice(sobrenomes)}"
            ),
            "celular_segundo_contato": (
                f"{random.randint(10, 99)}9" f"{random.randint(10000000, 99999999)}"
            ),
            "tipo_relacionamento_segundo_contato": random.choice(
                ["Pai", "Mãe", "Irmão", "Irmã", "Amigo", "Amiga"]
            ),
            "tipo_sanguineo": random.choice(tipos_sanguineos),
            "fator_rh": random.choice(fatores_rh),
            "alergias": (
                "Nenhuma"
                if random.random() > 0.3
                else random.choice(
                    ["Poeira", "Pólen", "Penicilina", "Frutos do mar", "Amendoim"]
                )
            ),
            "condicoes_medicas_gerais": (
                "Nenhuma"
                if random.random() > 0.3
                else random.choice(
                    ["Asma", "Hipertensão", "Diabetes", "Rinite alérgica"]
                )
            ),
            "convenio_medico": random.choice(convenios),
            "hospital": random.choice(hospitais),
        }
        # Baixar foto aleatória e adicionar ao dict se possível
        foto_path = baixar_foto_aleatoria(
            sexo, nomes[nome_idx], sobrenomes[sobrenome_idx]
        )

        aluno = Aluno.objects.create(**aluno_dados)

        if foto_path:
            with open(foto_path, "rb") as f:
                aluno.foto.save(os.path.basename(foto_path), File(f))
            os.remove(foto_path)

        # Criar registros históricos para o aluno (1 a 4 registros)
        for _ in range(random.randint(1, 4)):
            codigo_aleatorio = random.choice(codigos_disponiveis)
            data_os = date.today() - timedelta(days=random.randint(0, 365 * 5))
            RegistroHistorico.objects.create(
                aluno=aluno,
                codigo=codigo_aleatorio,
                ordem_servico=f"OS-{random.randint(1000, 9999)}",
                data_os=data_os,
                observacoes=f"Registro automático para {codigo_aleatorio.nome}.",
            )

        # Matricular o aluno em turmas aleatórias
        if turmas_disponiveis and random.random() > 0.1:  # 90% de chance de matricular
            # Matricular em 1 a 3 turmas
            num_matriculas = random.randint(1, min(3, len(turmas_disponiveis)))
            turmas_selecionadas = random.sample(turmas_disponiveis, num_matriculas)

            for turma in turmas_selecionadas:
                # Evitar matricular no mesmo curso duas vezes
                if not Matricula.objects.filter(
                    aluno=aluno, turma__curso=turma.curso
                ).exists():
                    Matricula.objects.create(
                        aluno=aluno,
                        turma=turma,
                        data_matricula=date.today()
                        - timedelta(days=random.randint(0, 365)),
                    )
                    matriculas_criadas += 1

        print(
            f'({i+1}/{QUANTIDADE_ALUNOS}) Aluno "{aluno.nome}" criado com sucesso com histórico!'
        )
        alunos_criados += 1

    except Exception as e:
        print(f"Erro ao criar aluno {i+1}: {str(e)}")

print(f"\nTotal de {alunos_criados} alunos criados com sucesso!")
print(f"Total de {matriculas_criadas} matrículas criadas.")
print(f"Total geral de alunos no banco: {Aluno.objects.count()}")
print(f"Total geral de matrículas no banco: {Matricula.objects.count()}")
