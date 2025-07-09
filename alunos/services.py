"""
Serviços para o aplicativo alunos.
Contém a lógica de negócios complexa.
"""
import logging
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q  # Adicionado para resolver erro de variável indefinida
import requests  # Adicionado para resolver erro de variável indefinida
from alunos.utils import (
    get_aluno_model,
    get_turma_model,
    get_matricula_model,
    get_atribuicao_cargo_model,
    get_registro_historico_model,
)
from alunos.models import RegistroHistorico  # Adicionando importação do modelo RegistroHistorico

# pylint: disable=redefined-outer-name

logger = logging.getLogger(__name__)

def verificar_elegibilidade_instrutor(aluno):
    """
    Verifica se um aluno pode ser instrutor.

    Args:
        aluno: Instância do modelo Aluno

    Returns:
        dict: Dicionário com chaves 'elegivel' (bool) e 'motivo' (str)
    """
    if aluno.situacao != "ATIVO":
        return {
            "elegivel": False,
            "motivo": (
                f"O aluno não está ativo. Situação atual: "
                f"{aluno.get_situacao_display()}"
            )
        }

    if not hasattr(aluno, "pode_ser_instrutor"):
        return {
            "elegivel": False,
            "motivo": (
                "Erro na verificação: o método 'pode_ser_instrutor' "
                "não existe."
            )
        }

    try:
        pode_ser_instrutor = aluno.pode_ser_instrutor

        if not pode_ser_instrutor:
            matricula_model = get_matricula_model()
            if matricula_model:
                matriculas_pre_iniciatico = matricula_model.objects.filter(
                    aluno=aluno, turma__curso__nome__icontains="Pré-iniciático"
                )

                if matriculas_pre_iniciatico.exists():
                    cursos = ", ".join(
                        [f"{m.turma.curso.nome}" for m in matriculas_pre_iniciatico]
                    )
                    return {
                        "elegivel": False,
                        "motivo": (
                            "O aluno está matriculado em cursos pré-iniciáticos: "
                            f"{cursos}"
                        )
                    }

            return {
                "elegivel": False,
                "motivo": "O aluno não atende aos requisitos para ser instrutor."
            }

        return {"elegivel": True}

    except Exception as exc:
        logger.error("Erro ao verificar elegibilidade do instrutor: %s", exc)
        return {
            "elegivel": False,
            "motivo": f"Erro ao verificar requisitos de instrutor: {exc}"
        }

def remover_instrutor_de_turmas(aluno, nova_situacao):
    """
    Remove um aluno de todas as turmas onde ele é instrutor.

    Args:
        aluno: Instância do modelo Aluno
        nova_situacao: Nova situação do aluno

    Returns:
        dict: Resultado da operação com chaves 'sucesso' e 'mensagem'
    """
    try:
        turma_model = get_turma_model()
        atribuicao_cargo_model = get_atribuicao_cargo_model()

        turmas_instrutor = turma_model.objects.filter(instrutor=aluno, status="A")
        turmas_instrutor_auxiliar = turma_model.objects.filter(
            instrutor_auxiliar=aluno, status="A"
        )
        turmas_auxiliar_instrucao = turma_model.objects.filter(
            auxiliar_instrucao=aluno, status="A"
        )

        for turma in turmas_instrutor:
            turma.instrutor = None
            turma.alerta_instrutor = True
            turma.alerta_mensagem = (
                f"O instrutor {aluno.nome} foi removido devido à mudança de "
                f"situação para '{aluno.get_situacao_display()}'.")
            turma.save()

            if atribuicao_cargo_model:
                atribuicoes = atribuicao_cargo_model.objects.filter(
                    aluno=aluno,
                    cargo__nome__icontains="Instrutor Principal",
                    data_fim__isnull=True,
                )
                for atribuicao in atribuicoes:
                    atribuicao.data_fim = timezone.now().date()
                    atribuicao.save()

        for turma in turmas_instrutor_auxiliar:
            turma.instrutor_auxiliar = None
            turma.alerta_instrutor = True
            turma.alerta_mensagem = f"O instrutor auxiliar {aluno.nome} foi removido devido à mudança de situação para '{aluno.get_situacao_display()}'."
            turma.save()

            if atribuicao_cargo_model:
                atribuicoes = atribuicao_cargo_model.objects.filter(
                    aluno=aluno,
                    cargo__nome__icontains="Instrutor Auxiliar",
                    data_fim__isnull=True,
                )
                for atribuicao in atribuicoes:
                    atribuicao.data_fim = timezone.now().date()
                    atribuicao.save()

        for turma in turmas_auxiliar_instrucao:
            turma.auxiliar_instrucao = None
            turma.alerta_instrutor = True
            turma.alerta_mensagem = f"O auxiliar de instrução {aluno.nome} foi removido devido à mudança de situação para '{aluno.get_situacao_display()}'."
            turma.save()

            if atribuicao_cargo_model:
                atribuicoes = atribuicao_cargo_model.objects.filter(
                    aluno=aluno,
                    cargo__nome__icontains="Auxiliar de Instrução",
                    data_fim__isnull=True,
                )
                for atribuicao in atribuicoes:
                    atribuicao.data_fim = timezone.now().date()
                    atribuicao.save()

        total_turmas = (
            len(turmas_instrutor) + len(turmas_instrutor_auxiliar) +
            len(turmas_auxiliar_instrucao)
        )

        return {
            "sucesso": True,
            "mensagem": f"Aluno removido de {total_turmas} turmas com sucesso."
        }

    except AttributeError as attr_err:
        logger.error("Erro de atributo ao remover instrutor de turmas: %s", attr_err)
        return {
            "sucesso": False,
            "mensagem": f"Erro de atributo: {attr_err}"
        }
    except Exception as exc:
        logger.error("Erro inesperado ao remover instrutor de turmas: %s", exc)
        raise RuntimeError("Erro inesperado ao remover instrutor de turmas") from exc

def listar_alunos(query=None, curso_id=None):
    """
    Lista e filtra alunos com base na query e no curso.
    """
    aluno_model = get_aluno_model()
    queryset = aluno_model.objects.filter(ativo=True).order_by("nome")

    if query:
        query = query.lower()
        if query.isdigit():
            cpf_query = query
            search_query = Q(cpf__icontains=cpf_query) | Q(matricula__icontains=cpf_query)
        else:
            search_query = (
                Q(nome__icontains=query) |
                Q(email__icontains=query) |
                Q(numero_iniciatico__icontains=query) |
                Q(nome_iniciatico__icontains=query)
            )
        queryset = queryset.filter(search_query).distinct()

    if curso_id:
        queryset = queryset.filter(matricula__turma__curso_id=curso_id).distinct()

    paginator = Paginator(queryset, 10)  # 10 resultados por página
    page_number = 1  # Página padrão
    try:
        page_number = int(query.get('page', 1))  # Obtém o número da página da query
    except ValueError:
        logger.warning("Número de página inválido, usando a página 1.")

    page_obj = paginator.get_page(page_number)

    logger.debug(
        "Query recebida: %s, Curso ID: %s, Resultados encontrados: %d, Página atual: %d, Total de páginas: %d",
        query,
        curso_id,
        queryset.count(),
        page_number,
        paginator.num_pages,
    )

    return page_obj

def buscar_aluno_por_cpf(cpf):
    """
    Busca um aluno pelo CPF.

    Args:
        cpf (str): O CPF do aluno a ser buscado.

    Returns:
        Aluno: A instância do aluno, ou None se não for encontrado.
    """
    Aluno = get_aluno_model()
    try:
        return Aluno.objects.get(cpf=cpf)
    except Aluno.DoesNotExist:
        return None

def buscar_alunos_por_nome_ou_cpf(query):
    """
    Busca alunos por nome ou CPF.

    Args:
        query (str): O termo de busca.

    Returns:
        QuerySet: Um queryset de alunos que correspondem à busca.
    """
    Aluno = get_aluno_model()
    cpf_query = ''.join(filter(str.isdigit, query))
    return Aluno.objects.filter(
        Q(nome__icontains=query) | Q(cpf__icontains=cpf_query)
    )

def buscar_aluno_por_email(email):
    """
    Busca um aluno pelo email.

    Args:
        email (str): O email do aluno a ser buscado.

    Returns:
        Aluno: A instância do aluno, ou None se não for encontrado.
    """
    Aluno = get_aluno_model()
    try:
        return Aluno.objects.get(email=email)
    except Aluno.DoesNotExist:
        return None

def criar_aluno(aluno_data, foto_url=None):
    """
    Cria um novo aluno com os dados fornecidos e, opcionalmente, uma foto.

    Args:
        aluno_data (dict): Dicionário com os dados do aluno (nome, email, cpf, etc.).
        foto_url (str, optional): URL da foto a ser baixada.

    Returns:
        Aluno: A instância do aluno criado, ou None em caso de erro.
    """
    Aluno = get_aluno_model()
    try:
        aluno = Aluno.objects.create(**aluno_data)

        if foto_url:
            try:
                response = requests.get(foto_url, stream=True, timeout=10)
                response.raise_for_status()
                file_name = f'{aluno_data["cpf"]}_photo.jpg'
                aluno.foto.save(file_name, ContentFile(response.content), save=True)
            except requests.RequestException as e:
                logger.error("Erro ao realizar a requisição: %s", e)
                raise

        return aluno
    except Exception as e:
        logger.error("Erro ao criar o aluno %s: %s", aluno_data.get("nome"), e)
        return None

def listar_historico_aluno(aluno):
    """
    Retorna o histórico de registros (cargos, iniciações, punições) de um aluno.
    """
    RegistroHistorico = get_registro_historico_model()  # noqa: E1101
    return RegistroHistorico.objects.filter(aluno=aluno).order_by('-data_registro')

def criar_registro_historico(data, aluno):
    """Cria um registro histórico para o aluno."""
    data['aluno'] = aluno
    registro = RegistroHistorico.objects.create(**data)
    return registro

def atualizar_dados_aluno(aluno_id, dados):
    """
    Atualiza os dados de um aluno existente.

    Args:
        aluno_id (int): O ID do aluno a ser atualizado.
        dados (dict): Um dicionário contendo os novos dados do aluno.

    Returns:
        dict: Um dicionário contendo o status da operação e uma mensagem.
    """
    Aluno = get_aluno_model()
    try:
        aluno = Aluno.objects.get(id=aluno_id)
    except Aluno.DoesNotExist:
        return {
            "status": "erro",
            "mensagem": "Aluno não encontrado.",
        }

    # Atualiza os campos do aluno com os dados fornecidos
    for campo, valor in dados.items():
        setattr(aluno, campo, valor)

    aluno.save()

    logger.info(
        "Aluno %s foi atualizado com sucesso. Dados: %s",
        aluno_id,
        dados_atualizados,
    )

    return {
        "status": "sucesso",
        "mensagem": "Dados do aluno atualizados com sucesso.",
    }