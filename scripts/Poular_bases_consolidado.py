import os
import sys
import django
import random
import json
from datetime import date, time, timedelta
from decimal import Decimal

# Configuração do ambiente Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from django.contrib.auth.models import User
from django.core.management import call_command

# --- Model Imports ---
from alunos.models import (
    Aluno,
    Pais,
    Estado,
    Cidade,
    Bairro,
    RegistroHistorico,
    Codigo,
    TipoCodigo,
)
from core.models import ConfiguracaoSistema
from cursos.models import Curso
from turmas.models import Turma
from matriculas.models import Matricula
from atividades.models import Atividade
from pagamentos.models import Pagamento
from notas.models import Nota
from presencas.models import (
    Presenca,
    ConfiguracaoPresenca,
    PresencaDetalhada,
    AgendamentoRelatorio,
)
from frequencias.models import FrequenciaMensal, Carencia

# --- Script Imports ---
from scripts.popular_cursos import popular_cursos
from scripts.importar_codigos_planilha import main as popular_codigos_planilha

# --- DADOS DE AMOSTRA PARA GERAÇÃO ALEATÓRIA ---
nomes = [
    "Miguel",
    "Arthur",
    "Gael",
    "Heitor",
    "Theo",
    "Davi",
    "Gabriel",
    "Bernardo",
    "Samuel",
    "Helena",
    "Alice",
    "Laura",
    "Maria Alice",
    "Sophia",
    "Manuela",
    "Maitê",
    "Liz",
    "Cecília",
    "Isabella",
]
sobrenomes = [
    "Silva",
    "Santos",
    "Oliveira",
    "Souza",
    "Rodrigues",
    "Ferreira",
    "Alves",
    "Pereira",
    "Lima",
    "Gomes",
    "Costa",
    "Ribeiro",
    "Martins",
    "Carvalho",
    "Almeida",
    "Lopes",
    "Soares",
    "Fernandes",
    "Vieira",
]
sexos = ["Masculino", "Feminino"]
tipos_sanguineos = ["A", "B", "AB", "O"]
fatores_rh = ["+", "-"]
convenios = [
    "Unimed",
    "Bradesco Saúde",
    "Amil",
    "SulAmérica",
    "NotreDame Intermédica",
    "Hapvida",
    "Golden Cross",
    "Porto Seguro Saúde",
]
hospitais = [
    "Hospital Sírio-Libanês",
    "Hospital Albert Einstein",
    "Hospital Oswaldo Cruz",
    "HCor",
    "Hospital Samaritano",
    "Rede D'Or São Luiz",
]
# --- FIM DOS DADOS DE AMOSTRA ---


def gerar_cpf_unico():
    return f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"


def gerar_email_unico(nome, sobrenome):
    return f"{nome.lower()}.{sobrenome.lower()}{random.randint(1, 9999)}@exemplo.com"


def popular_paises():
    """Garante que alguns países de exemplo existam."""
    if Pais.objects.exists():
        print("Países já existem, pulando criação.")
        return
    print("Criando países de exemplo...")
    Pais.objects.create(codigo="BRA", nome="Brasil", nacionalidade="Brasileiro(a)")
    Pais.objects.create(
        codigo="USA", nome="Estados Unidos", nacionalidade="Americano(a)"
    )
    Pais.objects.create(codigo="PRT", nome="Portugal", nacionalidade="Português(a)")
    print("Países criados.")


def popular_configuracao_sistema():
    """Garante que uma configuração de sistema padrão exista."""
    if not ConfiguracaoSistema.objects.exists():
        print("Criando configuração padrão do sistema...")
        ConfiguracaoSistema.objects.create(nome_sistema="OmAum", versao="1.0.0-dev")
        print("Configuração do sistema criada.")


def popular_dados_base():
    """Garante que os dados essenciais (Países, Cursos, Códigos) existam."""
    print("--- Garantindo a existência de dados base ---")
    popular_paises()
    popular_configuracao_sistema()
    popular_cursos()
    # Evita erro de ProtectedError em execuções repetidas
    if Codigo.objects.count() < 10:
        print("\nIniciando a importação de códigos iniciáticos da planilha...")
        try:
            popular_codigos_planilha()
        except Exception as e:
            print(f"ERRO ao importar códigos da planilha: {e}")
    else:
        print("\nCódigos iniciáticos já existem, pulando importação da planilha.")
    print("--- Dados base garantidos ---")


def popular_turmas():
    """Garante que existam turmas de teste no banco de dados."""
    if Turma.objects.count() >= 30:
        print("Turmas já existem em quantidade suficiente, pulando criação.")
        return list(Turma.objects.all())
    print("Criando 30 turmas de teste...")
    turmas = []
    cursos = list(Curso.objects.all())
    if not cursos:
        print("ERRO: Nenhum curso encontrado para criar turmas.")
        return turmas
    for i in range(30):
        turma = Turma.objects.create(
            nome=f"Turma Teste {i+1}",
            curso=random.choice(cursos),
            perc_carencia=Decimal(random.choice([70, 75, 80])),
        )
        turmas.append(turma)
    return turmas


def popular_atividades(turmas):
    """Cria algumas atividades de teste se não existirem."""
    if Atividade.objects.count() >= 40:
        print("Atividades já existem em quantidade suficiente, pulando criação.")
        return Atividade.objects.all()
    print("Criando 40 atividades de teste com dados variados...")
    tipos_atividade = ["Aula", "Palestra", "Workshop", "Seminário", "Laboratório"]
    responsaveis = ["Professor A", "Professor B", "Convidado Especial", "Monitor C"]
    status_opcoes = ["CONFIRMADA", "PENDENTE", "CANCELADA"]
    for i in range(40):
        tipo = random.choice(tipos_atividade)
        atividade = Atividade.objects.create(
            nome=f"Atividade de {tipo} {i+1}",
            tipo_atividade=tipo.upper(),
            data_inicio=date.today() - timedelta(days=random.randint(1, 365)),
            hora_inicio=time(random.randint(9, 20), random.choice([0, 30])),
            responsavel=random.choice(responsaveis),
            status=random.choice(status_opcoes),
        )
        if turmas:
            turmas_para_ativ = random.sample(
                turmas, min(len(turmas), random.randint(1, 5))
            )
            atividade.turmas.set(turmas_para_ativ)
    print("Criação de atividades concluída.")
    return Atividade.objects.all()


def _criar_dados_aluno_aleatorio(nomes, sobrenomes, sexos, paises, cidades, bairros):
    """Gera um dicionário com dados aleatórios para um novo aluno."""
    nome_idx = random.randint(0, len(nomes) - 1)
    sobrenome_idx = random.randint(0, len(sobrenomes) - 1)
    cidade_ref = random.choice(cidades) if cidades else None
    return {
        "cpf": gerar_cpf_unico(),
        "nome": f"{nomes[nome_idx]} {sobrenomes[sobrenome_idx]}",
        "data_nascimento": date(
            random.randint(1970, 2000), random.randint(1, 12), random.randint(1, 28)
        ),
        "hora_nascimento": time(random.randint(0, 23), random.randint(0, 59)),
        "email": gerar_email_unico(nomes[nome_idx], sobrenomes[sobrenome_idx]),
        "sexo": random.choice(sexos)[0],
        "pais_nacionalidade": random.choice(paises) if paises else None,
        "cidade_naturalidade": cidade_ref,
        "rua": f"Rua {random.choice(sobrenomes)} {random.randint(1, 100)}",
        "numero_imovel": str(random.randint(1, 999)),
        "cidade_ref": cidade_ref,
        "bairro_ref": random.choice(bairros) if bairros else None,
        "tipo_sanguineo": random.choice(
            [a + b for a in tipos_sanguineos for b in fatores_rh]
        ),
    }


def _criar_registros_historicos(aluno, codigo_teste):
    """Cria registros históricos de teste para um aluno."""
    for _ in range(random.randint(1, 3)):
        RegistroHistorico.objects.create(
            aluno=aluno,
            codigo=codigo_teste,
            ordem_servico=f"OS-{random.randint(1000, 9999)}",
            data_os=date.today() - timedelta(days=random.randint(0, 365 * 5)),
            observacoes="Registro automático.",
        )


def _realizar_matriculas_e_criar_dados_relacionados(aluno, turmas, atividades):
    """Realiza matrículas e cria presenças e notas relacionadas."""
    matriculas_ids = []
    presencas_ids = []
    notas_ids = []
    turmas_selecionadas = []
    if turmas and random.random() > 0.1:
        num_matriculas = random.randint(1, min(2, len(turmas)))
        turmas_selecionadas = random.sample(turmas, num_matriculas)
        for turma in turmas_selecionadas:
            if not Matricula.objects.filter(aluno=aluno, turma=turma).exists():
                matricula = Matricula.objects.create(
                    aluno=aluno,
                    turma=turma,
                    data_matricula=date.today()
                    - timedelta(days=random.randint(0, 365)),
                )
                matriculas_ids.append(matricula.id)
    for turma in turmas_selecionadas:
        atividades_da_turma = atividades.filter(turmas=turma)
        if not atividades_da_turma.exists():
            continue
        for atividade_da_turma in atividades_da_turma.order_by("?")[:2]:
            pres = Presenca.objects.create(
                aluno=aluno,
                turma=turma,
                atividade=atividade_da_turma,
                data=atividade_da_turma.data_inicio,
                presente=random.choice([True, False]),
                registrado_por="Script",
            )
            presencas_ids.append(pres.id)
    for turma_matriculada in turmas_selecionadas:
        for _ in range(random.randint(1, 3)):
            nota = Nota.objects.create(
                aluno=aluno,
                curso=turma_matriculada.curso,
                turma=turma_matriculada,
                tipo_avaliacao=random.choice(["prova", "trabalho", "atividade"]),
                valor=random.uniform(5, 10),
                data=date.today() - timedelta(days=random.randint(0, 365)),
            )
            notas_ids.append(nota.id)
    return matriculas_ids, presencas_ids, notas_ids


def _criar_pagamentos(aluno):
    """Cria pagamentos de teste para um aluno."""
    pagamentos_ids = []
    for _ in range(random.randint(1, 2)):
        pag = Pagamento.objects.create(
            aluno=aluno,
            valor=random.randint(100, 500),
            data_vencimento=date.today() - timedelta(days=random.randint(0, 90)),
            status=random.choice(["PENDENTE", "PAGO", "ATRASADO"]),
            metodo_pagamento=random.choice(["DINHEIRO", "PIX", "CARTAO_CREDITO"]),
        )
        pagamentos_ids.append(pag.id)
    return pagamentos_ids


def popular_alunos_e_relacionados(turmas, atividades):
    """Popula alunos e todos os dados relacionados (matrículas, presenças, etc.)."""
    QUANTIDADE_ALUNOS = 50
    if Aluno.objects.count() >= QUANTIDADE_ALUNOS:
        print("Alunos já existem em quantidade suficiente, pulando criação.")
        return
    print(f"Criando {QUANTIDADE_ALUNOS} alunos e dados relacionados...")
    paises = list(Pais.objects.all())
    cidades = list(Cidade.objects.all())
    bairros = list(Bairro.objects.all())
    tipo_codigo_teste, _ = TipoCodigo.objects.get_or_create(nome="Tipo Teste")
    codigo_teste, _ = Codigo.objects.get_or_create(
        nome="TESTE", tipo_codigo=tipo_codigo_teste
    )
    for i in range(QUANTIDADE_ALUNOS):
        try:
            aluno_dados = _criar_dados_aluno_aleatorio(
                nomes, sobrenomes, sexos, paises, cidades, bairros
            )
            aluno = Aluno.objects.create(**aluno_dados)
            _criar_registros_historicos(aluno, codigo_teste)
            _criar_pagamentos(aluno)
            _realizar_matriculas_e_criar_dados_relacionados(aluno, turmas, atividades)
            if (i + 1) % 10 == 0:
                print(f"  ... {i+1}/{QUANTIDADE_ALUNOS} alunos criados.")
        except Exception as e:
            print(f"Erro ao criar aluno {i+1}: {str(e)}")
    print(f"Total de {Aluno.objects.count()} alunos no banco.")


def popular_casos_de_borda():
    """Cria dados de teste para cenários de borda e exceções."""
    print("\n--- Iniciando População de Casos de Borda ---")
    if not Aluno.objects.filter(nome="Aluno Sem CPF").exists():
        Aluno.objects.create(
            nome="Aluno Sem CPF",
            email="semcpf@exemplo.com",
            data_nascimento=date(1990, 1, 1),
        )
    if not Aluno.objects.filter(nome="Aluno Sem Email").exists():
        Aluno.objects.create(
            nome="Aluno Sem Email",
            cpf=gerar_cpf_unico(),
            data_nascimento=date(1991, 2, 2),
        )
    if not Aluno.objects.filter(nome="Aluno Data Futura").exists():
        aluno_limite = Aluno.objects.create(
            nome="Aluno Data Futura",
            cpf=gerar_cpf_unico(),
            email="futuro@exemplo.com",
            data_nascimento=date.today() + timedelta(days=365),
        )
        turma = Turma.objects.first()
        if turma:
            Matricula.objects.get_or_create(
                aluno=aluno_limite,
                turma=turma,
                defaults={"data_matricula": date.today()},
            )
    if not Curso.objects.filter(nome="Curso Sem Turma").exists():
        curso_sem_turma = Curso.objects.create(nome="Curso Sem Turma")
        if not Turma.objects.filter(nome="Turma Vazia").exists():
            Turma.objects.create(nome="Turma Vazia", curso=curso_sem_turma)
    print("--- População de Casos de Borda Concluída ---")


def popular_configuracao_presenca(turmas, atividades):
    """Cria configurações de presença para algumas turmas e atividades."""
    if ConfiguracaoPresenca.objects.exists():
        print("Configurações de presença já existem, pulando criação.")
        return
    print("Criando configurações de presença...")
    for turma in random.sample(turmas, min(len(turmas), 5)):
        for atividade in random.sample(list(atividades), min(len(atividades), 2)):
            ConfiguracaoPresenca.objects.get_or_create(
                turma=turma,
                atividade=atividade,
                defaults={
                    "limite_carencia_0_25": random.randint(3, 4),
                    "limite_carencia_26_50": random.randint(2, 3),
                    "limite_carencia_51_75": random.randint(1, 2),
                    "limite_carencia_76_100": random.randint(0, 1),
                    "peso_calculo": Decimal(random.choice(["1.0", "1.5", "2.0"])),
                },
            )
    print("Configurações de presença criadas.")


def popular_frequencias(turmas):
    """Cria registros de FrequenciaMensal e Carencia."""
    if FrequenciaMensal.objects.exists():
        print("Frequências mensais já existem, pulando criação.")
        return
    print("Criando frequências mensais e calculando carências...")
    hoje = date.today()
    for turma in random.sample(turmas, min(len(turmas), 10)):
        for i in range(1, 4):  # Para os últimos 3 meses
            mes = (hoje.month - i) % 12 + 1
            ano = hoje.year if hoje.month > i else hoje.year - 1
            fm, created = FrequenciaMensal.objects.get_or_create(
                turma=turma, ano=ano, mes=mes
            )
            if created:
                fm.calcular_carencias()  # Reusa a lógica do modelo
    print("Frequências e carências criadas.")


def popular_agendamentos_relatorios():
    """Cria um agendamento de relatório de exemplo."""
    if AgendamentoRelatorio.objects.exists():
        print("Agendamentos de relatório já existem, pulando criação.")
        return
    print("Criando agendamento de relatório de exemplo...")
    user, _ = User.objects.get_or_create(
        username="admin", defaults={"is_staff": True, "is_superuser": True}
    )
    AgendamentoRelatorio.objects.create(
        nome="Relatório Mensal de Carências",
        usuario=user,
        formato="excel_avancado",
        template="carencia_presencas",
        frequencia="mensal",
        dia_mes=5,
        hora_execucao=time(9, 0, 0),
        emails_destino="admin@example.com,diretor@example.com",
    )
    print("Agendamento de relatório criado.")


def verificar_populacao():
    """Verifica e imprime a contagem de objetos para cada modelo populado."""
    print("\n--- Verificando a População do Banco de Dados ---")
    counts = {
        "Países": Pais.objects.count(),
        "Config. Sistema": ConfiguracaoSistema.objects.count(),
        "Alunos": Aluno.objects.count(),
        "Cursos": Curso.objects.count(),
        "Turmas": Turma.objects.count(),
        "Matrículas": Matricula.objects.count(),
        "Atividades": Atividade.objects.count(),
        "Notas": Nota.objects.count(),
        "Pagamentos": Pagamento.objects.count(),
        "Presenças (Simples)": Presenca.objects.count(),
        "Config. Presença": ConfiguracaoPresenca.objects.count(),
        "Frequências Mensais": FrequenciaMensal.objects.count(),
        "Carências": Carencia.objects.count(),
        "Agendamentos de Relatório": AgendamentoRelatorio.objects.count(),
    }
    for model, count in counts.items():
        print(f"- {model}: {count}")
    print("\n--- Verificação Concluída ---")
    # ASCII-safe verification
    if all(c > 0 for c in counts.values()):
        print(
            "[OK] Todas as tabelas principais parecem ter sido populadas com sucesso."
        )
    else:
        print("[ATENCAO] Algumas tabelas principais estão vazias.")


if __name__ == "__main__":
    try:
        print("Iniciando população consolidada das bases de teste...")
        popular_dados_base()
        turmas = popular_turmas()
        atividades = popular_atividades(turmas)
        if turmas and atividades:
            popular_alunos_e_relacionados(turmas, atividades)
            popular_configuracao_presenca(turmas, atividades)
            popular_frequencias(turmas)
            popular_agendamentos_relatorios()
        popular_casos_de_borda()
        print("\nPopulação consolidada concluída!")
        verificar_populacao()
    except Exception as e:
        import traceback

        with open("population_error.log", "w", encoding="utf-8") as f:
            f.write(f"Ocorreu um erro durante a população:\n{e}\n")
            f.write(traceback.format_exc())
        print(
            f"ERRO CRÍTICO: A população falhou. Verifique o arquivo 'population_error.log'."
        )
