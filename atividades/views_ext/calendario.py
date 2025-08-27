import logging
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .utils import get_model_class

# Set up logger
logger = logging.getLogger(__name__)


@login_required
def calendario_atividades(request):
    """Exibe o calendário de atividades."""
    # Obter todas as turmas para o filtro
    Turma = get_model_class("Turma", "turmas")
    turmas = Turma.objects.filter(status="A")  # Apenas turmas ativas

    return render(
        request,
        "atividades/calendario_atividades.html",
        {
            "turmas": turmas,
        },
    )


@login_required
def api_eventos_calendario(request):
    """API para fornecer eventos para o calendário."""
    # Obter parâmetros
    start_date = request.GET.get("start", "")
    end_date = request.GET.get("end", "")
    tipo_filtro = request.GET.get("tipo", "todas")
    turma_filtro = request.GET.get("turma", "todas")
    mostrar_concluidas = request.GET.get("concluidas", "1") == "1"

    # Obter modelos
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")

    eventos = []

    # Adicionar atividades acadêmicas
    if tipo_filtro in ["todas", "academicas"]:
        atividades_academicas = AtividadeAcademica.objects.all()

        # Aplicar filtro de data
        if start_date:
            atividades_academicas = atividades_academicas.filter(
                data_inicio__gte=start_date
            )
        if end_date:
            atividades_academicas = atividades_academicas.filter(
                data_inicio__lte=end_date
            )

        # Aplicar filtro de turma
        if turma_filtro != "todas":
            atividades_academicas = atividades_academicas.filter(
                turmas__id=turma_filtro
            )

        # Aplicar filtro de status concluído
        if not mostrar_concluidas:
            atividades_academicas = atividades_academicas.exclude(status="concluida")

        # Converter para formato de evento do FullCalendar
        for atividade in atividades_academicas:
            evento = {
                "id": atividade.id,
                "title": atividade.nome,
                "start": atividade.data_inicio.isoformat(),
                "end": atividade.data_fim.isoformat() if atividade.data_fim else None,
                "allDay": True,  # Por padrão, eventos de dia inteiro
                "tipo": "academica",
                "status": atividade.status,
                "description": atividade.descricao or "",
            }
            eventos.append(evento)

    # Adicionar atividades ritualísticas
    if tipo_filtro in ["todas", "ritualisticas"]:
        atividades_ritualisticas = AtividadeRitualistica.objects.all()

        # Aplicar filtro de data
        if start_date:
            atividades_ritualisticas = atividades_ritualisticas.filter(
                data__gte=start_date
            )
        if end_date:
            atividades_ritualisticas = atividades_ritualisticas.filter(
                data__lte=end_date
            )

        # Aplicar filtro de turma
        if turma_filtro != "todas":
            atividades_ritualisticas = atividades_ritualisticas.filter(
                turma_id=turma_filtro
            )

        # Converter para formato de evento do FullCalendar
        for atividade in atividades_ritualisticas:
            # Combinar data e hora para criar datetime completo
            data = atividade.data

            # Converter hora_inicio e hora_fim para objetos time
            hora_inicio = atividade.hora_inicio
            hora_fim = atividade.hora_fim

            # Criar datetime para início e fim
            start_datetime = datetime.combine(data, hora_inicio)
            end_datetime = datetime.combine(data, hora_fim)

            evento = {
                "id": atividade.id,
                "title": atividade.nome,
                "start": start_datetime.isoformat(),
                "end": end_datetime.isoformat(),
                "allDay": False,  # Eventos ritualísticos têm horário específico
                "tipo": "ritualistica",
                "description": atividade.descricao or "",
            }
            eventos.append(evento)

    return JsonResponse(eventos, safe=False)


@login_required
def api_detalhe_evento(request, evento_id):
    """API para fornecer detalhes de um evento específico."""
    tipo = request.GET.get("tipo", "")

    try:
        if tipo == "academica":
            AtividadeAcademica = get_model_class("AtividadeAcademica")
            atividade = get_object_or_404(AtividadeAcademica, id=evento_id)

            # Formatar dados para resposta JSON
            evento = {
                "nome": atividade.nome,
                "descricao": atividade.descricao,
                "data_inicio": atividade.data_inicio.strftime("%d/%m/%Y"),
                "data_fim": atividade.data_fim.strftime("%d/%m/%Y")
                if atividade.data_fim
                else None,
                "responsavel": atividade.responsavel,
                "local": atividade.local,
                "tipo": atividade.tipo_atividade,
                "tipo_display": atividade.get_tipo_atividade_display(),
                "status": atividade.status,
                "status_display": atividade.get_status_display(),
                "turmas": [turma.nome for turma in atividade.turmas.all()],
            }

            return JsonResponse({"success": True, "evento": evento})

        elif tipo == "ritualistica":
            AtividadeRitualistica = get_model_class("AtividadeRitualistica")
            atividade = get_object_or_404(AtividadeRitualistica, id=evento_id)

            # Formatar dados para resposta JSON
            evento = {
                "nome": atividade.nome,
                "descricao": atividade.descricao,
                "data": atividade.data.strftime("%d/%m/%Y"),
                "hora_inicio": atividade.hora_inicio.strftime("%H:%M"),
                "hora_fim": atividade.hora_fim.strftime("%H:%M"),
                "local": atividade.local,
                "turma": atividade.turma.nome if atividade.turma else "Sem turma",
                "total_participantes": atividade.participantes.count(),
            }

            return JsonResponse({"success": True, "evento": evento})

        else:
            return JsonResponse(
                {"success": False, "error": "Tipo de evento inválido"}, status=400
            )

    except Exception as e:
        logger.error(f"Erro ao obter detalhes do evento: {str(e)}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)
