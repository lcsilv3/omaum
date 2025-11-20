import unicodedata
from importlib import import_module
from typing import Any, Dict, Iterable, List, Optional

from django.db import transaction

from .models import Curso


def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


def get_atividade_model():
    """Obtém o modelo Atividade."""
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "Atividade")


def get_nota_model():
    """Obtém o modelo Nota."""
    notas_module = import_module("notas.models")
    return getattr(notas_module, "Nota")


def get_matricula_model():
    """Obtém o modelo Matricula."""
    matriculas_module = import_module("matriculas.models")
    return getattr(matriculas_module, "Matricula")


def get_pagamento_model():
    """Obtém o modelo Pagamento."""
    pagamentos_module = import_module("pagamentos.models")
    return getattr(pagamentos_module, "Pagamento")


# --- Utilidades compartilhadas ------------------------------------------------


def normalizar_texto(valor: Any) -> str:
    """Converte qualquer valor em string stripada (retorna vazio para None)."""

    if valor is None:
        return ""
    return str(valor).strip()


def converter_para_int(valor: Any) -> Optional[int]:
    """Converte valores textuais em inteiro, aceitando sufixos ".0"."""

    texto = normalizar_texto(valor)
    if not texto:
        return None
    if texto.endswith(".0"):
        texto = texto[:-2]
    try:
        return int(texto)
    except ValueError:
        try:
            return int(float(texto))
        except (TypeError, ValueError):
            return None


def interpretar_flag_ativo(valor: Any) -> Optional[bool]:
    """Interpreta diferentes representações de booleano (sim/não, 1/0, etc.)."""

    if valor is None:
        return None
    if isinstance(valor, bool):
        return valor

    texto = normalizar_texto(valor).lower()
    texto_ascii = (
        unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    )
    if not texto_ascii:
        return None

    if texto_ascii in {"1", "true", "t", "sim", "s", "yes", "ativo"}:
        return True
    if texto_ascii in {"0", "false", "f", "nao", "n", "no", "inativo"}:
        return False
    return None


# --- Sincronização de cursos --------------------------------------------------


@transaction.atomic
def sincronizar_cursos(
    dados: Iterable[Dict[str, Any]], desativar_nao_listados: bool = True
) -> Dict[str, Any]:
    """Sincroniza cursos a partir de uma coleção de dicionários normalizados."""

    resumo: Dict[str, Any] = {
        "processados": 0,
        "criados": 0,
        "atualizados": 0,
        "reativados": 0,
        "desativados": 0,
        "avisos": [],
    }

    ids_importados: List[int] = []
    nomes_importados: List[str] = []

    for indice, item in enumerate(dados, start=1):
        linha_planilha = item.get("linha", indice)
        identificador = converter_para_int(item.get("id"))
        nome = normalizar_texto(item.get("nome"))
        descricao = normalizar_texto(item.get("descricao"))
        flag_ativo = interpretar_flag_ativo(item.get("ativo"))

        if not nome and identificador is None:
            resumo["avisos"].append(
                f"Linha {linha_planilha}: curso sem identificador nem nome; ignorado."
            )
            continue

        curso = None

        if identificador is not None:
            curso = Curso.objects.filter(pk=identificador).first()

        if not curso and nome:
            cursos_encontrados = list(Curso.objects.filter(nome__iexact=nome))
            if len(cursos_encontrados) > 1:
                resumo["avisos"].append(
                    f"Linha {linha_planilha}: existem múltiplos cursos com nome '{nome}'."
                )
                continue
            curso = cursos_encontrados[0] if cursos_encontrados else None

        if curso:
            estado_anterior = curso.ativo
            campos_para_atualizar: List[str] = []

            if descricao != curso.descricao:
                curso.descricao = descricao
                campos_para_atualizar.append("descricao")

            if flag_ativo is not None and curso.ativo != flag_ativo:
                curso.ativo = flag_ativo
                campos_para_atualizar.append("ativo")

            if nome and curso.nome != nome:
                curso.nome = nome
                campos_para_atualizar.append("nome")

            if campos_para_atualizar:
                curso.save(update_fields=campos_para_atualizar)
                resumo["atualizados"] += 1
            if not estado_anterior and curso.ativo:
                resumo["reativados"] += 1
        else:
            if not nome:
                resumo["avisos"].append(
                    f"Linha {linha_planilha}: nome do curso ausente; registro ignorado."
                )
                continue

            curso = Curso.objects.create(
                nome=nome,
                descricao=descricao,
                ativo=True if flag_ativo is None else flag_ativo,
            )
            resumo["criados"] += 1

        resumo["processados"] += 1

        if curso.id is not None:
            ids_importados.append(curso.id)
        if curso.nome:
            nomes_importados.append(curso.nome)

    if desativar_nao_listados:
        cursos_para_desativar = Curso.objects.filter(ativo=True)
        if ids_importados:
            cursos_para_desativar = cursos_para_desativar.exclude(id__in=ids_importados)
        if nomes_importados:
            cursos_para_desativar = cursos_para_desativar.exclude(
                nome__in=nomes_importados
            )
        resumo["desativados"] = cursos_para_desativar.update(ativo=False)

    return resumo


# --- Funções de Leitura (Read) ---


def listar_cursos(query=None):
    """Retorna uma queryset com todos os cursos, opcionalmente filtrados por nome."""
    cursos = Curso.objects.all()
    if query:
        cursos = cursos.filter(nome__icontains=query)
    return cursos.order_by("id")


def obter_curso_por_id(curso_id):
    """
    Busca um curso pelo seu ID.
    Retorna o objeto Curso ou None se não for encontrado.
    """
    try:
        return Curso.objects.get(pk=curso_id)
    except Curso.DoesNotExist:
        return None


# --- Funções de Escrita (Create, Update, Delete) ---


@transaction.atomic
def criar_curso(nome, descricao):
    """
    Cria um novo curso no banco de dados.
    Retorna a instância do curso criado.
    """
    if not nome:
        raise ValueError("O nome do curso é obrigatório.")

    curso = Curso.objects.create(nome=nome, descricao=descricao)
    return curso


@transaction.atomic
def atualizar_curso(curso_id, nome, descricao):
    """
    Atualiza os dados de um curso existente.
    Retorna a instância do curso atualizado ou None se não for encontrado.
    """
    curso = obter_curso_por_id(curso_id)
    if curso:
        curso.nome = nome
        curso.descricao = descricao
        curso.save()
    return curso


@transaction.atomic
def excluir_curso(curso_id):
    """
    Exclui um curso, desde que não hajam dependências.
    Retorna True se a exclusão for bem-sucedida, False caso contrário.
    Levanta uma exceção ValueError se houver dependências.
    """
    curso = obter_curso_por_id(curso_id)
    if not curso:
        return False  # Curso não existe

    dependencias = verificar_dependencias_curso(curso)
    # Verifica se alguma lista de dependência não está vazia
    if any(dependencias.values()):
        raise ValueError(
            "Não é possível excluir o curso pois existem dependências associadas."
        )

    curso.delete()
    return True


# --- Funções de Lógica de Negócio ---


def verificar_dependencias_curso(curso):
    """
    Verifica e retorna um dicionário com todas as dependências de um curso.
    """
    # Obter modelos dinamicamente
    Turma = get_turma_model()
    Atividade = get_atividade_model()
    Nota = get_nota_model()
    Matricula = get_matricula_model()
    Pagamento = get_pagamento_model()

    # Alunos matriculados em turmas deste curso
    alunos_ids = Matricula.objects.filter(turma__curso=curso).values_list(
        "aluno_id", flat=True
    )

    dependencias = {
        "turmas": list(Turma.objects.filter(curso=curso)),
        "atividades": list(Atividade.objects.filter(curso=curso)),
        "notas": list(Nota.objects.filter(curso=curso)),
        "matriculas": list(Matricula.objects.filter(turma__curso=curso)),
        "pagamentos": list(Pagamento.objects.filter(aluno_id__in=alunos_ids)),
    }
    return {key: value for key, value in dependencias.items() if value}
