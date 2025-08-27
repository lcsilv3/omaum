import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..views_ext.utils import get_model_class, get_turma_model

logger = logging.getLogger(__name__)


@login_required
def relatorio_atividades_ritualisticas(request):
    Turma = get_turma_model()
    turmas = Turma.objects.filter(status="A")
    turma_id = request.GET.get("turma")
    data = request.GET.get("data")

    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividades = AtividadeRitualistica.objects.all()
    if turma_id:
        atividades = atividades.filter(turma_id=turma_id)
    if data:
        atividades = atividades.filter(data=data)

    context = {
        "atividades": atividades,
        "turmas": turmas,
        "turma_selecionada": turma_id,
        "data_selecionada": data,
    }
    return render(
        request,
        "atividades/ritualisticas/relatorio_atividades_ritualisticas.html",
        context,
    )
