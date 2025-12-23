"""
Views otimizadas para registro rápido de presenças.
"""

import logging
from datetime import datetime
from importlib import import_module
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.db import transaction

from presencas.models import RegistroPresenca


def _get_model(app_name: str, model_name: str):
    """Importa modelo dinamicamente para evitar circularidade."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)


Atividade = _get_model("atividades", "Atividade")
Turma = _get_model("turmas", "Turma")
Aluno = _get_model("alunos", "Aluno")

logger = logging.getLogger(__name__)


class RegistroRapidoView:
    @staticmethod
    @require_POST
    @csrf_exempt
    def atualizar_convocacao_ajax(request):
        """Atualiza o status de convocação (convocado/voluntário) de um aluno para uma atividade/data/turma."""
        try:
            import json

            data = json.loads(request.body)
            turma_id = data.get("turma_id")
            atividade_id = data.get("atividade_id")
            data_str = data.get("data")
            aluno_cpf = data.get("aluno_cpf")
            convocado = data.get("convocado")
            if not all(
                [turma_id, atividade_id, data_str, aluno_cpf, convocado is not None]
            ):
                return JsonResponse({"error": "Dados incompletos"}, status=400)
            from datetime import datetime

            try:
                data_obj = datetime.strptime(data_str, "%Y-%m-%d").date()
            except Exception:
                return JsonResponse({"error": "Data inválida"}, status=400)
            try:
                aluno = Aluno.objects.get(cpf=aluno_cpf)
            except Aluno.DoesNotExist:
                return JsonResponse({"error": "Aluno não encontrado"}, status=404)
            # Atualizar ou criar registro de presença com convocação
            obj, created = RegistroPresenca.objects.update_or_create(
                turma_id=turma_id,
                atividade_id=atividade_id,
                data=data_obj,
                aluno=aluno,
                defaults={"convocado": convocado},
            )
            return JsonResponse(
                {"success": True, "created": created, "convocado": convocado}
            )
        except Exception as e:
            logger.error(f"Erro ao atualizar convocação: {str(e)}")
            import traceback

            logger.error(traceback.format_exc())
            return JsonResponse(
                {"error": f"Erro ao atualizar convocação: {str(e)}"}, status=500
            )

    """View otimizada para registro rápido de presenças."""

    @staticmethod
    @login_required
    def registro_rapido_otimizado(request):
        """Interface principal de registro rápido otimizada."""
        context = {
            "data_hoje": timezone.now().date(),
            "turmas": Turma.objects.all().select_related("curso"),
            "atividades": Atividade.objects.all(),
        }
        return render(request, "presencas/registro_rapido_otimizado.html", context)

    @staticmethod
    @require_GET
    def buscar_alunos_ajax(request):
        """Busca alunos via AJAX com auto-complete."""
        query = request.GET.get("q", "").strip()
        turma_id = request.GET.get("turma_id")
        limit = int(request.GET.get("limit", 10))

        if len(query) < 2:
            return JsonResponse({"alunos": []})

        try:
            # Base queryset
            alunos_queryset = Aluno.objects.select_related("curso")

            # Filtro por turma se especificado
            if turma_id:
                alunos_queryset = alunos_queryset.filter(
                    matriculas__turma_id=turma_id
                ).distinct()

            # Busca por nome ou CPF
            alunos_queryset = alunos_queryset.filter(
                Q(nome__icontains=query) | Q(cpf__icontains=query)
            ).order_by("nome")[:limit]

            alunos_data = []
            for aluno in alunos_queryset:
                alunos_data.append(
                    {
                        "id": aluno.cpf,
                        "cpf": aluno.cpf,
                        "nome": aluno.nome,
                        "curso": aluno.curso.nome if aluno.curso else "Sem curso",
                        "display": f"{aluno.nome} - {aluno.cpf}",
                    }
                )

            return JsonResponse({"alunos": alunos_data})

        except Exception as e:
            logger.error(f"Erro na busca de alunos: {str(e)}")
            return JsonResponse({"error": "Erro na busca"}, status=500)

    @staticmethod
    @require_GET
    def obter_alunos_turma_ajax(request):
        """Obtém todos os alunos de uma turma específica, incluindo status de convocação para atividade/dia."""
        turma_id = request.GET.get("turma_id")
        atividade_id = request.GET.get("atividade_id")
        data_str = request.GET.get("data")  # formato esperado: YYYY-MM-DD

        if not turma_id:
            return JsonResponse({"error": "Turma não especificada"}, status=400)

        try:
            logger.info(f"Buscando alunos da turma ID: {turma_id}")
            alunos = (
                Aluno.objects.filter(matricula__turma_id=turma_id, situacao="a")
                .distinct()
                .order_by("nome")
            )

            logger.info(
                f"Encontrados {alunos.count()} alunos ativos na turma {turma_id}"
            )

            # Buscar status de convocação se atividade_id e data forem fornecidos
            convoc_status = {}
            if atividade_id and data_str:
                from datetime import datetime

                try:
                    data_obj = datetime.strptime(data_str, "%Y-%m-%d").date()
                except Exception:
                    data_obj = None
                if data_obj:
                    presencas_no_dia = RegistroPresenca.objects.filter(
                        turma_id=turma_id, atividade_id=atividade_id, data=data_obj
                    )
                    for presenca in presencas_no_dia:
                        convoc_status[str(presenca.aluno.cpf)] = presenca.convocado

            alunos_data = []
            for aluno in alunos:
                # Por padrão, todos são convocados se não houver registro
                convocado = True
                if atividade_id and data_str:
                    convocado = convoc_status.get(str(aluno.cpf), True)
                aluno_info = {
                    "id": aluno.cpf,
                    "cpf": aluno.cpf,
                    "nome": aluno.nome,
                    "curso": "N/A",
                    "presente": None,
                    "ja_registrado": False,
                    "convocado": convocado,
                }
                alunos_data.append(aluno_info)
                logger.debug(
                    f"Aluno adicionado: {aluno.nome} (CPF: {aluno.cpf}) - Convocado: {convocado}"
                )

            logger.info(f"Retornando {len(alunos_data)} alunos para a turma {turma_id}")
            return JsonResponse({"alunos": alunos_data})

        except Exception as e:
            logger.error(f"Erro ao obter alunos da turma {turma_id}: {str(e)}")
            import traceback

            logger.error(traceback.format_exc())
            return JsonResponse(
                {"error": f"Erro ao obter alunos: {str(e)}"}, status=500
            )

    @staticmethod
    @require_POST
    @csrf_exempt
    def salvar_presencas_lote_ajax(request):
        """Salva presenças em lote via AJAX."""
        try:
            import json

            data = json.loads(request.body)

            turma_id = data.get("turma_id")
            atividade_id = data.get("atividade_id")
            data_presenca = data.get("data")
            presencas = data.get("presencas", [])

            if not all([turma_id, atividade_id, data_presenca, presencas]):
                return JsonResponse({"error": "Dados incompletos"}, status=400)

            # Validação de objetos
            try:
                turma = Turma.objects.get(id=turma_id)
                atividade = Atividade.objects.get(id=atividade_id)
                data_obj = datetime.strptime(data_presenca, "%Y-%m-%d").date()
            except (Turma.DoesNotExist, Atividade.DoesNotExist, ValueError) as e:
                return JsonResponse({"error": f"Dados inválidos: {str(e)}"}, status=400)

            registradas = 0
            atualizadas = 0
            erros = []

            with transaction.atomic():
                for presenca_data in presencas:
                    try:
                        aluno_id = presenca_data.get("aluno_id")
                        presente = presenca_data.get("presente", False)
                        observacao = presenca_data.get("observacao", "")

                        if not aluno_id:
                            continue

                        aluno = Aluno.objects.get(id=aluno_id)

                        # Criar ou atualizar presença
                        presenca_obj, created = RegistroPresenca.objects.get_or_create(
                            aluno=aluno,
                            turma=turma,
                            atividade=atividade,
                            data=data_obj,
                            defaults={
                                "status": "P" if presente else "F",
                                "justificativa": observacao or "",
                                "registrado_por": request.user.username,
                                "data_registro": timezone.now(),
                            },
                        )

                        if not created:
                            presenca_obj.status = "P" if presente else "F"
                            if observacao:
                                presenca_obj.justificativa = observacao
                            presenca_obj.registrado_por = request.user.username
                            presenca_obj.data_registro = timezone.now()
                            presenca_obj.save()
                            atualizadas += 1
                        else:
                            registradas += 1

                    except Aluno.DoesNotExist:
                        erros.append(f"Aluno ID {aluno_id} não encontrado")
                    except Exception as e:
                        erros.append(f"Erro ao processar aluno {aluno_id}: {str(e)}")

            return JsonResponse(
                {
                    "success": True,
                    "registradas": registradas,
                    "atualizadas": atualizadas,
                    "erros": erros,
                    "total_processadas": registradas + atualizadas,
                }
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)
        except Exception as e:
            logger.error(f"Erro no salvamento em lote: {str(e)}")
            return JsonResponse({"error": "Erro interno do servidor"}, status=500)

    @staticmethod
    @require_GET
    def validar_presenca_ajax(request):
        """Valida se uma presença já existe."""
        aluno_id = request.GET.get("aluno_id")
        turma_id = request.GET.get("turma_id")
        atividade_id = request.GET.get("atividade_id")
        data_presenca = request.GET.get("data")

        if not all([aluno_id, turma_id, atividade_id, data_presenca]):
            return JsonResponse({"error": "Parâmetros incompletos"}, status=400)

        try:
            data_obj = datetime.strptime(data_presenca, "%Y-%m-%d").date()
            aluno = Aluno.objects.get(id=aluno_id)

            presenca_existente = RegistroPresenca.objects.filter(
                aluno=aluno, turma_id=turma_id, atividade_id=atividade_id, data=data_obj
            ).first()

            if presenca_existente:
                return JsonResponse(
                    {
                        "existe": True,
                        "presente": presenca_existente.status == "P",
                        "registrado_por": presenca_existente.registrado_por,
                        "data_registro": presenca_existente.data_registro.strftime(
                            "%d/%m/%Y %H:%M"
                        ),
                    }
                )
            else:
                return JsonResponse({"existe": False})

        except (Aluno.DoesNotExist, ValueError):
            return JsonResponse({"error": "Dados inválidos"}, status=400)
        except Exception as e:
            logger.error(f"Erro na validação: {str(e)}")
            return JsonResponse({"error": "Erro interno"}, status=500)


# Funções de conveniência para URLs
registro_rapido_otimizado = RegistroRapidoView.registro_rapido_otimizado
buscar_alunos_ajax = RegistroRapidoView.buscar_alunos_ajax
obter_alunos_turma_ajax = RegistroRapidoView.obter_alunos_turma_ajax
salvar_presencas_lote_ajax = RegistroRapidoView.salvar_presencas_lote_ajax
validar_presenca_ajax = RegistroRapidoView.validar_presenca_ajax
atualizar_convocacao_ajax = RegistroRapidoView.atualizar_convocacao_ajax
