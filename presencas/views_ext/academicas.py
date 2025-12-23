# ...código existente...
from importlib import import_module
from django.shortcuts import render
from presencas.models import RegistroPresenca


def _get_model(app_name: str, model_name: str):
    """Importa modelo dinamicamente para evitar circularidade."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)


Curso = _get_model("cursos", "Curso")
Turma = _get_model("turmas", "Turma")
AtividadeAcademica = _get_model("atividades", "AtividadeAcademica")
Aluno = _get_model("alunos", "Aluno")


def listar_presencas_academicas(request):
    # Auto-correção de dados inconsistentes (executa uma vez por carregamento)
    if not request.GET.get("corrected"):
        try:
            from django.db import transaction

            with transaction.atomic():
                # Corrigir presenças sem turma quando há atividade
                presencas_sem_turma = RegistroPresenca.objects.filter(
                    turma__isnull=True, atividade__isnull=False
                ).select_related("atividade")

                corrigidas = 0
                for presenca in presencas_sem_turma[
                    :50
                ]:  # Limitar para não sobrecarregar
                    if (
                        hasattr(presenca.atividade, "turmas")
                        and presenca.atividade.turmas.exists()
                    ):
                        presenca.turma = presenca.atividade.turmas.first()
                        presenca.save()
                        corrigidas += 1

                if corrigidas > 0:
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.info(
                        f"Auto-correção: {corrigidas} presenças receberam turmas automaticamente"
                    )
        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Erro na auto-correção de presenças: {str(e)}")

    # Otimização de queries com relacionamentos
    cursos = Curso.objects.all()
    turmas = Turma.objects.select_related("curso").all()
    atividades = (
        AtividadeAcademica.objects.select_related("curso")
        .prefetch_related("turmas")
        .all()
    )
    alunos = Aluno.objects.all()

    # Filtros
    curso_id = request.GET.get("curso")
    turma_id = request.GET.get("turma")
    atividade_id = request.GET.get("atividade")
    aluno_id = request.GET.get("aluno")
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")

    # Query otimizada para presenças com relacionamentos
    presencas = RegistroPresenca.objects.select_related(
        "aluno", "turma__curso", "atividade"
    ).all()

    if curso_id:
        turmas = turmas.filter(curso_id=curso_id)
        presencas = presencas.filter(turma__curso_id=curso_id)
    if turma_id:
        atividades = atividades.filter(turmas__id=turma_id).distinct()
        presencas = presencas.filter(turma_id=turma_id)
    if atividade_id:
        presencas = presencas.filter(atividade_id=atividade_id)
    if aluno_id:
        presencas = presencas.filter(aluno_id=aluno_id)
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)

    # Ordenação para melhor apresentação
    presencas = presencas.order_by("-data", "aluno__nome")

    context = {
        "presencas": presencas,
        "cursos": cursos,
        "turmas": turmas,
        "atividades": atividades,
        "alunos": alunos,
    }
    return render(
        request, "presencas/academicas/listar_presencas_academicas.html", context
    )


# ...código existente...
