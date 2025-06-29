import os
import django
from datetime import time, date, timedelta
import random

# Django configuration
os.environ["DJANGO_SETTINGS_MODULE"] = "omaum.settings"
django.setup()

from faker import Faker
from django.utils import timezone
from alunos.models import Aluno
from cursos.models import Curso
from turmas.models import Turma

# Initialize Faker with Brazilian locale
fake = Faker("pt_BR")


def criar_cursos_teste():
    """Cria cursos de teste para associar aos alunos"""
    cursos_dados = [
        {
            "codigo_curso": 101,
            "nome": "Iniciação Básica",
            "descricao": "Curso introdutório aos princípios da OmAum",
            "duracao": 3,
        },
        {
            "codigo_curso": 102,
            "nome": "Meditação Avançada",
            "descricao": "Técnicas avançadas de meditação e concentração",
            "duracao": 6,
        },
        {
            "codigo_curso": 103,
            "nome": "Filosofia Oriental",
            "descricao": "Estudo dos fundamentos filosóficos orientais",
            "duracao": 12,
        },
        {
            "codigo_curso": 104,
            "nome": "Práticas Ritualísticas",
            "descricao": "Aprendizado e prática de rituais tradicionais",
            "duracao": 9,
        },
        {
            "codigo_curso": 105,
            "nome": "Desenvolvimento Espiritual",
            "descricao": "Técnicas para desenvolvimento da espiritualidade",
            "duracao": 18,
        },
    ]

    cursos_criados = []
    print("Criando cursos de teste...")

    for curso_dados in cursos_dados:
        curso, created = Curso.objects.update_or_create(
            codigo_curso=curso_dados["codigo_curso"], defaults=curso_dados
        )
        cursos_criados.append(curso)
        status = "Criado" if created else "Atualizado"
        print(f"  {status}: {curso.id} - {curso.nome}")

    return cursos_criados


def criar_turmas_teste(cursos):
    """Cria turmas de teste para os cursos"""
    turmas_criadas = []
    print("\nCriando turmas de teste...")

    # Criar turmas em diferentes estados (passadas, atuais, futuras)
    hoje = timezone.now().date()

    for curso in cursos:
        # Turma passada (concluída)
        inicio_passada = hoje - timedelta(days=365)
        fim_passada = inicio_passada + timedelta(days=curso.duracao * 30)

        # Turma atual (em andamento)
        inicio_atual = hoje - timedelta(days=curso.duracao * 15)
        fim_atual = inicio_atual + timedelta(days=curso.duracao * 30)

        # Turma futura
        inicio_futura = hoje + timedelta(days=30)
        fim_futura = inicio_futura + timedelta(days=curso.duracao * 30)

        turmas_dados = [
            {
                "nome": f"Turma {curso.nome} - Concluída",
                "data_inicio": inicio_passada,
                "data_fim": fim_passada,
                "vagas": 20,
            },
            {
                "nome": f"Turma {curso.nome} - Em Andamento",
                "data_inicio": inicio_atual,
                "data_fim": fim_atual,
                "vagas": 15,
            },
            {
                "nome": f"Turma {curso.nome} - Futura",
                "data_inicio": inicio_futura,
                "data_fim": fim_futura,
                "vagas": 25,
            },
        ]

        for turma_dados in turmas_dados:
            try:
                turma, created = Turma.objects.update_or_create(
                    nome=turma_dados["nome"],
                    defaults={
                        "curso": curso,
                        "data_inicio": turma_dados["data_inicio"],
                        "data_fim": turma_dados["data_fim"],
                        "vagas": turma_dados["vagas"],
                    },
                )
                turmas_criadas.append(turma)
                status = "Criada" if created else "Atualizada"
                print(f"  {status}: {turma.nome}")
            except Exception as e:
                print(f"  Erro ao criar turma {turma_dados['nome']}: {str(e)}")

    return turmas_criadas


def criar_alunos_ficticios(quantidade=50, cursos=None, turmas=None):
    """Cria alunos fictícios e os associa a cursos e turmas"""
    alunos_criados = 0

    print(f"\nIniciando criação de {quantidade} alunos fictícios...")

    # Garantir diversidade de dados para testes
    sexos = ["M", "F", "O"]
    tipos_sanguineos = ["A", "B", "AB", "O"]
    fatores_rh = ["+", "-"]

    # Criar alguns alunos com características específicas para testes
    alunos_especiais = [
        # Aluno menor de idade
        {
            "nome": "Aluno Menor de Idade",
            "data_nascimento": fake.date_of_birth(
                minimum_age=16, maximum_age=17
            ),
            "sexo": "M",
        },
        # Aluno idoso
        {
            "nome": "Aluno Idoso",
            "data_nascimento": fake.date_of_birth(
                minimum_age=65, maximum_age=80
            ),
            "sexo": "M",
        },
        # Aluno com necessidades especiais
        {
            "nome": "Aluno com Necessidades Especiais",
            "condicoes_medicas_gerais": "Cadeirante, necessita de acessibilidade",
            "sexo": "M",
        },
        # Aluna gestante
        {
            "nome": "Aluna Gestante",
            "sexo": "F",
            "condicoes_medicas_gerais": "Gestante de 6 meses, necessita de cuidados especiais",
        },
        # Aluno estrangeiro
        {
            "nome": "Aluno Estrangeiro",
            "nacionalidade": "Portuguesa",
            "sexo": "M",
        },
    ]

    # Primeiro criar os alunos especiais
    for i, aluno_especial in enumerate(alunos_especiais):
        try:
            # Generate random time for hora_nascimento
            random_hour = random.randint(0, 23)
            random_minute = random.randint(0, 59)
            hora_nascimento = time(hour=random_hour, minute=random_minute)

            # Gerar CPF válido (apenas números, 11 dígitos)
            cpf = "".join([str(random.randint(0, 9)) for _ in range(11)])

            # Gerar número de celular válido (formato brasileiro)
            celular1 = f"({random.randint(11, 99)}) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            celular2 = f"({random.randint(11, 99)}) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"

            # Valores padrão
            dados_aluno = {
                "cpf": cpf,
                "nome": aluno_especial.get("nome", fake.name()),
                "data_nascimento": aluno_especial.get(
                    "data_nascimento",
                    fake.date_of_birth(minimum_age=18, maximum_age=65),
                ),
                "hora_nascimento": hora_nascimento,
                "email": fake.unique.email(),
                "foto": None,
                "numero_iniciatico": fake.unique.numerify("######"),
                "nome_iniciatico": fake.name(),
                "sexo": aluno_especial.get(
                    "sexo", fake.random_element(elements=sexos)
                ),
                "nacionalidade": aluno_especial.get(
                    "nacionalidade", "Brasileira"
                ),
                "naturalidade": fake.city(),
                "rua": fake.street_name(),
                "numero_imovel": fake.building_number(),
                "complemento": fake.random_element(
                    elements=["Apto 101", "Casa 1", "Bloco A", "Fundos"]
                ),
                "cidade": fake.city(),
                "estado": fake.estado_sigla(),
                "bairro": fake.bairro(),
                "cep": fake.postcode().replace("-", ""),
                "nome_primeiro_contato": fake.name(),
                "celular_primeiro_contato": celular1,
                "tipo_relacionamento_primeiro_contato": fake.random_element(
                    elements=("Pai", "Mãe", "Irmão", "Amigo")
                ),
                "nome_segundo_contato": fake.name(),
                "celular_segundo_contato": celular2,
                "tipo_relacionamento_segundo_contato": fake.random_element(
                    elements=("Pai", "Mãe", "Irmão", "Amigo")
                ),
                "tipo_sanguineo": fake.random_element(
                    elements=tipos_sanguineos
                ),
                "fator_rh": fake.random_element(elements=fatores_rh),
                "alergias": aluno_especial.get(
                    "alergias", fake.text(max_nb_chars=200)
                ),
                "condicoes_medicas_gerais": aluno_especial.get(
                    "condicoes_medicas_gerais", fake.text(max_nb_chars=200)
                ),
                "convenio_medico": fake.company(),
                "hospital": fake.company(),
            }

            aluno = Aluno.objects.create(**dados_aluno)

            # Associar a um curso, se disponível
            if cursos and len(cursos) > 0:
                curso = cursos[i % len(cursos)]
                # Aqui você associaria o aluno ao curso, dependendo da estrutura do seu modelo
                # Se houver um campo curso no modelo Aluno:
                # aluno.curso = curso
                # aluno.save()

            # Associar a uma turma, se disponível
            if turmas and len(turmas) > 0:
                turma = turmas[i % len(turmas)]
                # Aqui você associaria o aluno à turma, dependendo da estrutura do seu modelo
                # Se houver um relacionamento ManyToMany:
                # aluno.turmas.add(turma)
                # Ou se for uma relação direta:
                # aluno.turma = turma
                # aluno.save()

            alunos_criados += 1
            print(f"  Criado aluno especial: {aluno.nome}")

        except Exception as e:
            print(f"  Erro ao criar aluno especial #{i+1}: {str(e)}")

    # Criar o restante dos alunos regulares
    for i in range(quantidade - len(alunos_especiais)):
        try:
            # Generate random time for hora_nascimento
            random_hour = random.randint(0, 23)
            random_minute = random.randint(0, 59)
            hora_nascimento = time(hour=random_hour, minute=random_minute)

            # Gerar CPF válido (apenas números, 11 dígitos)
            cpf = "".join([str(random.randint(0, 9)) for _ in range(11)])

            # Gerar número de celular válido (formato brasileiro)
            celular1 = f"({random.randint(11, 99)}) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            celular2 = f"({random.randint(11, 99)}) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"

            # Garantir diversidade de dados
            sexo = sexos[i % len(sexos)]
            tipo_sanguineo = tipos_sanguineos[i % len(tipos_sanguineos)]
            fator_rh = fatores_rh[i % len(fatores_rh)]

            aluno = Aluno.objects.create(
                cpf=cpf,
                nome=fake.name(),
                data_nascimento=fake.date_of_birth(
                    minimum_age=18, maximum_age=65
                ),
                hora_nascimento=hora_nascimento,
                email=fake.unique.email(),
                foto=None,
                numero_iniciatico=fake.unique.numerify("######"),
                nome_iniciatico=fake.name(),
                sexo=sexo,
                nacionalidade="Brasileira",
                naturalidade=fake.city(),
                rua=fake.street_name(),
                numero_imovel=fake.building_number(),
                complemento=fake.random_element(
                    elements=["Apto 101", "Casa 1", "Bloco A", "Fundos"]
                ),
                cidade=fake.city(),
                estado=fake.estado_sigla(),
                bairro=fake.bairro(),
                cep=fake.postcode().replace("-", ""),
                nome_primeiro_contato=fake.name(),
                celular_primeiro_contato=celular1,
                tipo_relacionamento_primeiro_contato=fake.random_element(
                    elements=("Pai", "Mãe", "Irmão", "Amigo")
                ),
                nome_segundo_contato=fake.name(),
                celular_segundo_contato=celular2,
                tipo_relacionamento_segundo_contato=fake.random_element(
                    elements=("Pai", "Mãe", "Irmão", "Amigo")
                ),
                tipo_sanguineo=tipo_sanguineo,
                fator_rh=fator_rh,
                alergias=fake.text(max_nb_chars=200),
                condicoes_medicas_gerais=fake.text(max_nb_chars=200),
                convenio_medico=fake.company(),
                hospital=fake.company(),
            )

            # Associar a um curso e turma, se disponíveis
            if cursos and len(cursos) > 0:
                curso = cursos[i % len(cursos)]
                # Aqui você associaria o aluno ao curso

            if turmas and len(turmas) > 0:
                turma = turmas[i % len(turmas)]
                # Aqui você associaria o aluno à turma

            alunos_criados += 1

            # Mostrar progresso a cada 10 alunos
            if (i + 1) % 10 == 0 or i == 0:
                print(
                    f"  Criados {i + 1 + len(alunos_especiais)} alunos de {quantidade}..."
                )

        except Exception as e:
            print(
                f"  Erro ao criar aluno #{i+1+len(alunos_especiais)}: {str(e)}"
            )

    print(f"\n{alunos_criados} alunos fictícios criados com sucesso!")
    return alunos_criados


def main():
    # Verificar se já existem alunos no banco
    total_alunos = Aluno.objects.count()
    if total_alunos > 0:
        print(f"Já existem {total_alunos} alunos no banco de dados.")
        resposta = input("Deseja criar mais alunos e dados de teste? (s/n): ")
        if resposta.lower() != "s":
            print("Operação cancelada.")
            return

    # Criar cursos
    cursos = criar_cursos_teste()

    # Criar turmas
    turmas = criar_turmas_teste(cursos)

    # Perguntar quantos alunos criar
    try:
        qtd = int(input("Quantos alunos deseja criar? (padrão: 50): ") or "50")
    except ValueError:
        qtd = 50
        print("Valor inválido. Usando o padrão de 50 alunos.")

    # Criar alunos e associá-los a cursos e turmas
    criar_alunos_ficticios(qtd, cursos, turmas)

    print("\nProcesso de criação de dados de teste concluído!")
    print(
        "Agora você pode testar todas as funcionalidades do sistema com estes dados."
    )


if __name__ == "__main__":
    main()
