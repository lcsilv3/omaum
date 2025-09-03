import os
import sys
import django
import random
import json
from datetime import date, time, timedelta

# Configuração do ambiente Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from django.core.management import call_command

from alunos.models import (  # noqa: E402
    Aluno,
    Estado,
    Cidade,
    Bairro,
    RegistroHistorico,
    Codigo,
    TipoCodigo,
)
from cursos.models import Curso  # noqa: E402
from turmas.models import Turma  # noqa: E402
from presencas.models import Presenca  # noqa: E402
from pagamentos.models import Pagamento  # noqa: E402
from notas.models import Nota  # noqa: E402
from matriculas.models import Matricula  # noqa: E402
from atividades.models import Atividade  # noqa: E402

# Importa a função do script de popular cursos
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
    return f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}"


def gerar_email_unico(nome, sobrenome):
    return f"{nome.lower()}.{sobrenome.lower()}{random.randint(1,9999)}@exemplo.com"


def baixar_foto_aleatoria(sexo, nome, sobrenome):
    return None


def popular_dados_base():
    """Garante que os dados essenciais (Cursos, Códigos) existam."""
    print("--- Garantindo a existência de dados base ---")
    # 1. Popula os cursos usando o script dedicado
    popular_cursos()

    # 2. Popula os códigos usando o script da planilha
    print("\nIniciando a importação de códigos iniciáticos da planilha...")
    try:
        popular_codigos_planilha()
    except Exception as e:
        print(f"ERRO ao importar códigos da planilha: {e}")
    print("--- Dados base garantidos ---")


def popular_turmas():
    """Garante que existam turmas de teste no banco de dados."""
    if Turma.objects.exists():
        print("Turmas já existem, pulando criação.")
        return list(Turma.objects.all())

    print("Criando 30 turmas de teste...")
    turmas = []
    cursos = list(Curso.objects.all())
    if not cursos:
        print(
            "ERRO: Nenhum curso encontrado para criar turmas. Execute popular_dados_base primeiro."
        )
        return turmas

    for i in range(30):
        turma = Turma.objects.create(
            nome=f"Turma Teste {i+1}", curso=random.choice(cursos)
        )
        turmas.append(turma)
    return turmas


def popular_atividades(turmas):
    """
    Cria algumas atividades de teste se não existirem.

    Args:
        turmas (list): Uma lista de objetos Turma para associar às atividades.

    Returns:
        QuerySet: Um QuerySet de objetos Atividade.
    """
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


def _criar_dados_aluno_aleatorio(nomes, sobrenomes, sexos, estados, cidades, bairros):
    """Gera um dicionário com dados aleatórios para um novo aluno."""
    nome_idx = random.randint(0, len(nomes) - 1)
    sobrenome_idx = random.randint(0, len(sobrenomes) - 1)
    cidade_ref = random.choice(cidades) if cidades else None
    estado_ref = (
        cidade_ref.estado
        if cidade_ref
        else (random.choice(estados) if estados else None)
    )
    return {
        "cpf": gerar_cpf_unico(),
        "nome": f"{nomes[nome_idx]} {sobrenomes[sobrenome_idx]}",
        "data_nascimento": date(
            random.randint(1970, 2000), random.randint(1, 12), random.randint(1, 28)
        ),
        "hora_nascimento": time(random.randint(0, 23), random.randint(0, 59)),
        "email": gerar_email_unico(nomes[nome_idx], sobrenomes[sobrenome_idx]),
        "sexo": random.choice(sexos),
        "rua": f"Rua {random.choice(sobrenomes)} {random.randint(1, 100)}",
        "numero_imovel": str(random.randint(1, 999)),
        "complemento": f"Apto {random.randint(1, 100)}"
        if random.random() > 0.5
        else "",
        "cep": f"{random.randint(10000, 99999)}{random.randint(100, 999)}",
        "cidade_ref": cidade_ref,
        "bairro_ref": random.choice(bairros) if bairros else None,
        "nome_primeiro_contato": f"{random.choice(nomes)} {random.choice(sobrenomes)}",
        "celular_primeiro_contato": f"{random.randint(10, 99)}9{random.randint(10000000, 99999999)}",
        "tipo_relacionamento_primeiro_contato": random.choice(
            ["Pai", "Mãe", "Irmão", "Irmã", "Cônjuge"]
        ),
        "nome_segundo_contato": f"{random.choice(nomes)} {random.choice(sobrenomes)}",
        "celular_segundo_contato": f"{random.randint(10, 99)}9{random.randint(10000000, 99999999)}",
        "tipo_relacionamento_segundo_contato": random.choice(
            ["Pai", "Mãe", "Irmão", "Irmã", "Amigo", "Amiga"]
        ),
        "tipo_sanguineo": random.choice(
            [a + b for a in tipos_sanguineos for b in fatores_rh]
        ),
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
            else random.choice(["Asma", "Hipertensão", "Diabetes", "Rinite alérgica"])
        ),
        "convenio_medico": random.choice(convenios),
        "hospital": random.choice(hospitais),
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
                Matricula.objects.create(
                    aluno=aluno,
                    turma=turma,
                    data_matricula=date.today()
                    - timedelta(days=random.randint(0, 365)),
                )
                matriculas_ids.append(turma.id)

    for turma in turmas_selecionadas:
        atividade_da_turma = atividades.filter(turmas=turma).first()
        if not atividade_da_turma:
            continue
        for _ in range(random.randint(1, 2)):
            pres = Presenca.objects.create(
                aluno=aluno,
                turma=turma,
                atividade=atividade_da_turma,
                data=date.today() - timedelta(days=random.randint(0, 180)),
                presente=random.choice([True, False]),
                registrado_por="Script",
            )
            presencas_ids.append(pres.id)

    for turma_matriculada in turmas_selecionadas:
        for _ in range(random.randint(5, 10)):
            nota = Nota.objects.create(
                aluno=aluno,
                curso=turma_matriculada.curso,
                turma=turma_matriculada,
                tipo_avaliacao=random.choice(
                    ["prova", "trabalho", "atividade", "exame", "outro"]
                ),
                valor=random.uniform(0, 10),
                peso=random.choice([1.0, 1.5, 2.0, 2.5]),
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


def popular_alunos_e_matriculas(turmas, atividades):
    """
    Popula o banco de dados com alunos, matrículas e dados relacionados.

    Cria uma quantidade definida de alunos com dados aleatórios, os matricula em
    turmas, e gera registros de presença, notas, pagamentos e histórico.

    Args:
        turmas (list): Lista de objetos Turma disponíveis para matrícula.
        atividades (QuerySet): QuerySet de objetos Atividade disponíveis.
    """
    QUANTIDADE_ALUNOS = 50
    alunos_criados = 0
    matriculas_criadas = 0
    dados_export = []

    estados = list(Estado.objects.all())
    cidades = list(Cidade.objects.all())
    bairros = list(Bairro.objects.all())
    tipo_codigo_teste, _ = TipoCodigo.objects.get_or_create(
        nome="Tipo Teste", defaults={"descricao": "Tipo de Código para testes"}
    )
    codigo_teste, _ = Codigo.objects.get_or_create(
        nome="TESTE",
        defaults={"descricao": "Código de Teste", "tipo_codigo": tipo_codigo_teste},
    )

    for i in range(QUANTIDADE_ALUNOS):
        try:
            aluno_dados = _criar_dados_aluno_aleatorio(
                nomes, sobrenomes, sexos, estados, cidades, bairros
            )
            aluno = Aluno.objects.create(**aluno_dados)

            _criar_registros_historicos(aluno, codigo_teste)
            pagamentos_ids = _criar_pagamentos(aluno)
            (
                matriculas_ids,
                presencas_ids,
                notas_ids,
            ) = _realizar_matriculas_e_criar_dados_relacionados(
                aluno, turmas, atividades
            )

            matriculas_criadas += len(matriculas_ids)

            dados_export.append(
                {
                    "aluno": aluno.cpf,
                    "matriculas": matriculas_ids,
                    "presencas": presencas_ids,
                    "pagamentos": pagamentos_ids,
                    "notas": notas_ids,
                }
            )
            print(
                f'({i+1}/{QUANTIDADE_ALUNOS}) Aluno "{aluno.nome}" criado com sucesso!'
            )
            alunos_criados += 1
        except Exception as e:
            print(f"Erro ao criar aluno {i+1}: {str(e)}")
    print(f"\nTotal de {alunos_criados} alunos criados com sucesso!")
    print(f"Total de {matriculas_criadas} matrículas criadas.")
    print(f"Total geral de alunos no banco: {Aluno.objects.count()}")
    print(f"Total geral de matrículas no banco: {Matricula.objects.count()}")
    with open("dados_teste_gerados.json", "w", encoding="utf-8") as f:
        json.dump(dados_export, f, ensure_ascii=False, indent=2)


def _criar_alunos_com_dados_nulos():
    """Cria alguns alunos com campos importantes nulos ou vazios."""
    print("\nCriando alunos com dados nulos/vazios...")
    Aluno.objects.create(
        nome="Aluno Sem CPF",
        email="semcpf@exemplo.com",
        data_nascimento=date(1990, 1, 1),
    )
    Aluno.objects.create(
        nome="Aluno Sem Email", cpf=gerar_cpf_unico(), data_nascimento=date(1991, 2, 2)
    )
    print("Alunos com dados nulos criados.")


def _criar_entidades_vazias():
    """Garante que o sistema lide com entidades sem associações."""
    print("\nCriando entidades vazias...")
    curso_sem_turma = Curso.objects.create(nome="Curso Sem Turma")
    Turma.objects.create(nome="Turma Vazia", curso=curso_sem_turma)
    print("Entidades vazias criadas.")


def _criar_dados_com_valores_limite():
    """Cria dados que testam os limites dos campos (ex: datas futuras)."""
    print("\nCriando dados com valores limite...")
    aluno_limite = Aluno.objects.create(
        nome="Aluno Data Futura",
        cpf=gerar_cpf_unico(),
        email="futuro@exemplo.com",
        data_nascimento=date.today() + timedelta(days=365),
    )
    turma = Turma.objects.first()
    if turma:
        Matricula.objects.create(
            aluno=aluno_limite,
            turma=turma,
            data_matricula=date.today() + timedelta(days=1),
        )
    print("Dados com valores limite criados.")


def popular_casos_de_borda():
    """
    Cria dados de teste para cenários de borda e exceções.

    Isso inclui alunos com dados faltando, entidades sem associações
    e valores que testam os limites dos campos do modelo.
    """
    print("\n--- Iniciando População de Casos de Borda ---")
    _criar_alunos_com_dados_nulos()
    _criar_entidades_vazias()
    _criar_dados_com_valores_limite()
    print("\n--- População de Casos de Borda Concluída ---")


def verificar_populacao():
    """Verifica e imprime a contagem de objetos para cada modelo populado."""
    print("\n--- Verificando a População do Banco de Dados ---")

    counts = {
        "Alunos": Aluno.objects.count(),
        "Cursos": Curso.objects.count(),
        "Tipos de Código": TipoCodigo.objects.count(),
        "Códigos Iniciáticos": Codigo.objects.count(),
        "Turmas": Turma.objects.count(),
        "Matrículas": Matricula.objects.count(),
        "Atividades": Atividade.objects.count(),
        "Notas": Nota.objects.count(),
        "Pagamentos": Pagamento.objects.count(),
        "Registros de Presença": Presenca.objects.count(),
    }

    for model, count in counts.items():
        print(f"- {model}: {count}")

    print("\n--- Verificação Concluída ---")

    # Análise básica baseada na execução do script de população
    # 50 normais + alunos de borda (sem cpf, sem email, data futura)
    alunos_esperados = 50 + 3
    # 30 normais + 1 turma de borda (vazia)
    turmas_esperadas = 30 + 1
    # 8 do script + 1 curso de borda (sem turma)
    cursos_esperados = 8 + 1

    print("\n--- Análise Rápida ---")
    if counts["Alunos"] >= alunos_esperados:
        print(
            f"✅ Contagem de Alunos ({counts['Alunos']}) está OK (Esperado: >= {alunos_esperados})."
        )
    else:
        print(
            f"⚠️  Contagem de Alunos ({counts['Alunos']}) abaixo do esperado (Esperado: >= {alunos_esperados})."
        )

    if counts["Turmas"] >= turmas_esperadas:
        print(
            f"✅ Contagem de Turmas ({counts['Turmas']}) está OK (Esperado: >= {turmas_esperadas})."
        )
    else:
        print(
            f"⚠️  Contagem de Turmas ({counts['Turmas']}) abaixo do esperado (Esperado: >= {turmas_esperadas})."
        )

    if counts["Cursos"] >= cursos_esperados:
        print(
            f"✅ Contagem de Cursos ({counts['Cursos']}) está OK (Esperado: >= {cursos_esperados})."
        )
    else:
        print(
            f"⚠️  Contagem de Cursos ({counts['Cursos']}) abaixo do esperado (Esperado: >= {cursos_esperados})."
        )

    if counts["Matrículas"] > 0 and counts["Notas"] > 0 and counts["Pagamentos"] > 0:
        print(
            "✅ Dados relacionados (Matrículas, Notas, Pagamentos) parecem ter sido criados."
        )
    else:
        print(
            "⚠️  Dados relacionados (Matrículas, Notas, Pagamentos) podem estar faltando."
        )


if __name__ == "__main__":
    try:
        print("Iniciando população consolidada das bases de teste...")
        popular_dados_base()
        turmas = popular_turmas()
        atividades = popular_atividades(turmas)
        if turmas:
            popular_alunos_e_matriculas(turmas, atividades)
        popular_casos_de_borda()
        print("\nPopulação consolidada concluída!")

        # Executa a verificação no final
        verificar_populacao()

    except Exception as e:
        with open("population_error.log", "w") as f:
            f.write(f"Ocorreu um erro durante a população:\n{e}\n")
        print(
            f"ERRO CRÍTICO: A população falhou. Verifique o arquivo 'population_error.log'."
        )
