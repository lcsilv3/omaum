"""
Views otimizadas para registro rápido de presenças.
"""

import logging
from datetime import datetime, date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Prefetch
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.core.paginator import Paginator
from django.db import transaction

from atividades.models import Atividade
from presencas.models import PresencaAcademica, ObservacaoPresenca
from alunos.services import listar_alunos as listar_alunos_service, buscar_aluno_por_cpf as buscar_aluno_por_cpf_service
from turmas.models import Turma
from alunos.models import Aluno

logger = logging.getLogger(__name__)


class RegistroRapidoView:
    """View otimizada para registro rápido de presenças."""
    
    @staticmethod
    @login_required
    def registro_rapido_otimizado(request):
        """Interface principal de registro rápido otimizada."""
        context = {
            'data_hoje': timezone.now().date(),
            'turmas': Turma.objects.all().select_related('curso'),
            'atividades': Atividade.objects.all(),
        }
        return render(request, 'presencas/registro_rapido_otimizado.html', context)
    
    @staticmethod
    @require_GET
    def buscar_alunos_ajax(request):
        """Busca alunos via AJAX com auto-complete."""
        query = request.GET.get('q', '').strip()
        turma_id = request.GET.get('turma_id')
        limit = int(request.GET.get('limit', 10))
        
        if len(query) < 2:
            return JsonResponse({'alunos': []})
        
        try:
            # Base queryset
            alunos_queryset = Aluno.objects.select_related('curso')
            
            # Filtro por turma se especificado
            if turma_id:
                alunos_queryset = alunos_queryset.filter(
                    matriculas__turma_id=turma_id
                ).distinct()
            
            # Busca por nome ou CPF
            alunos_queryset = alunos_queryset.filter(
                Q(nome__icontains=query) | 
                Q(cpf__icontains=query)
            ).order_by('nome')[:limit]
            
            alunos_data = []
            for aluno in alunos_queryset:
                alunos_data.append({
                    'id': aluno.id,
                    'cpf': aluno.cpf,
                    'nome': aluno.nome,
                    'curso': aluno.curso.nome if aluno.curso else 'Sem curso',
                    'display': f"{aluno.nome} - {aluno.cpf}"
                })
            
            return JsonResponse({'alunos': alunos_data})
            
        except Exception as e:
            logger.error(f"Erro na busca de alunos: {str(e)}")
            return JsonResponse({'error': 'Erro na busca'}, status=500)
    
    @staticmethod
    @require_GET
    def obter_alunos_turma_ajax(request):
        """Obtém todos os alunos de uma turma específica."""
        turma_id = request.GET.get('turma_id')
        
        if not turma_id:
            return JsonResponse({'error': 'Turma não especificada'}, status=400)
        
        try:
            # Busca alunos da turma com presenças já registradas para hoje
            data_hoje = timezone.now().date()
            alunos = Aluno.objects.filter(
                matriculas__turma_id=turma_id
            ).select_related('curso').distinct().order_by('nome')
            
            # Prefetch presenças já registradas hoje
            alunos = alunos.prefetch_related(
                Prefetch(
                    'presencaacademica_set',
                    queryset=PresencaAcademica.objects.filter(
                        data=data_hoje,
                        turma_id=turma_id
                    ),
                    to_attr='presencas_hoje'
                )
            )
            
            alunos_data = []
            for aluno in alunos:
                # Verifica se já tem presença registrada hoje
                presenca_existente = None
                for presenca in aluno.presencas_hoje:
                    presenca_existente = presenca
                    break
                
                alunos_data.append({
                    'id': aluno.id,
                    'cpf': aluno.cpf,
                    'nome': aluno.nome,
                    'curso': aluno.curso.nome if aluno.curso else 'Sem curso',
                    'presente': presenca_existente.presente if presenca_existente else None,
                    'ja_registrado': bool(presenca_existente)
                })
            
            return JsonResponse({'alunos': alunos_data})
            
        except Exception as e:
            logger.error(f"Erro ao obter alunos da turma: {str(e)}")
            return JsonResponse({'error': 'Erro ao obter alunos'}, status=500)
    
    @staticmethod
    @require_POST
    @csrf_exempt
    def salvar_presencas_lote_ajax(request):
        """Salva presenças em lote via AJAX."""
        try:
            import json
            data = json.loads(request.body)
            
            turma_id = data.get('turma_id')
            atividade_id = data.get('atividade_id')
            data_presenca = data.get('data')
            presencas = data.get('presencas', [])
            
            if not all([turma_id, atividade_id, data_presenca, presencas]):
                return JsonResponse({'error': 'Dados incompletos'}, status=400)
            
            # Validação de objetos
            try:
                turma = Turma.objects.get(id=turma_id)
                atividade = Atividade.objects.get(id=atividade_id)
                data_obj = datetime.strptime(data_presenca, '%Y-%m-%d').date()
            except (Turma.DoesNotExist, Atividade.DoesNotExist, ValueError) as e:
                return JsonResponse({'error': f'Dados inválidos: {str(e)}'}, status=400)
            
            registradas = 0
            atualizadas = 0
            erros = []
            
            with transaction.atomic():
                for presenca_data in presencas:
                    try:
                        aluno_id = presenca_data.get('aluno_id')
                        presente = presenca_data.get('presente', False)
                        observacao = presenca_data.get('observacao', '')
                        
                        if not aluno_id:
                            continue
                        
                        aluno = Aluno.objects.get(id=aluno_id)
                        
                        # Criar ou atualizar presença
                        presenca_obj, created = PresencaAcademica.objects.get_or_create(
                            aluno=aluno,
                            turma=turma,
                            atividade=atividade,
                            data=data_obj,
                            defaults={
                                'presente': presente,
                                'registrado_por': request.user.username,
                                'data_registro': timezone.now()
                            }
                        )
                        
                        if not created:
                            presenca_obj.presente = presente
                            presenca_obj.registrado_por = request.user.username
                            presenca_obj.data_registro = timezone.now()
                            presenca_obj.save()
                            atualizadas += 1
                        else:
                            registradas += 1
                        
                        # Criar observação se fornecida
                        if observacao.strip():
                            ObservacaoPresenca.objects.create(
                                aluno=aluno,
                                turma=turma,
                                data=data_obj,
                                atividade=atividade,
                                texto=observacao,
                                registrado_por=request.user.username,
                                data_registro=timezone.now()
                            )
                    
                    except Aluno.DoesNotExist:
                        erros.append(f'Aluno ID {aluno_id} não encontrado')
                    except Exception as e:
                        erros.append(f'Erro ao processar aluno {aluno_id}: {str(e)}')
            
            return JsonResponse({
                'success': True,
                'registradas': registradas,
                'atualizadas': atualizadas,
                'erros': erros,
                'total_processadas': registradas + atualizadas
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            logger.error(f"Erro no salvamento em lote: {str(e)}")
            return JsonResponse({'error': 'Erro interno do servidor'}, status=500)
    
    @staticmethod
    @require_GET
    def validar_presenca_ajax(request):
        """Valida se uma presença já existe."""
        aluno_id = request.GET.get('aluno_id')
        turma_id = request.GET.get('turma_id')
        atividade_id = request.GET.get('atividade_id')
        data_presenca = request.GET.get('data')
        
        if not all([aluno_id, turma_id, atividade_id, data_presenca]):
            return JsonResponse({'error': 'Parâmetros incompletos'}, status=400)
        
        try:
            data_obj = datetime.strptime(data_presenca, '%Y-%m-%d').date()
            aluno = Aluno.objects.get(id=aluno_id)
            
            presenca_existente = PresencaAcademica.objects.filter(
                aluno=aluno,
                turma_id=turma_id,
                atividade_id=atividade_id,
                data=data_obj
            ).first()
            
            if presenca_existente:
                return JsonResponse({
                    'existe': True,
                    'presente': presenca_existente.presente,
                    'registrado_por': presenca_existente.registrado_por,
                    'data_registro': presenca_existente.data_registro.strftime('%d/%m/%Y %H:%M')
                })
            else:
                return JsonResponse({'existe': False})
                
        except (Aluno.DoesNotExist, ValueError) as e:
            return JsonResponse({'error': 'Dados inválidos'}, status=400)
        except Exception as e:
            logger.error(f"Erro na validação: {str(e)}")
            return JsonResponse({'error': 'Erro interno'}, status=500)


# Funções de conveniência para URLs
registro_rapido_otimizado = RegistroRapidoView.registro_rapido_otimizado
buscar_alunos_ajax = RegistroRapidoView.buscar_alunos_ajax
obter_alunos_turma_ajax = RegistroRapidoView.obter_alunos_turma_ajax
salvar_presencas_lote_ajax = RegistroRapidoView.salvar_presencas_lote_ajax
validar_presenca_ajax = RegistroRapidoView.validar_presenca_ajax
