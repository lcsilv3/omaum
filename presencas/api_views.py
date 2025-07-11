"""
API Views para o aplicativo presencas.
Views REST organizadas e seguindo padrões do projeto.
"""
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.db import transaction
import json
import logging
from atividades.models import Atividade
from alunos.models import Aluno

from .models import Presenca, TotalAtividadeMes, ObservacaoPresenca
from .serializers import PresencaSerializer, TotalAtividadeMesSerializer, ObservacaoPresencaSerializer
from .services import (
    listar_presencas,
    buscar_presencas_por_filtros,
    registrar_presenca,
    registrar_presencas_multiplas,
    atualizar_presenca,
    excluir_presenca,
    obter_presencas_por_aluno,
    obter_presencas_por_turma,
    calcular_frequencia_aluno,
    criar_observacao_presenca,
    registrar_total_atividade_mes
)
from .repositories import PresencaRepository, TotalAtividadeMesRepository, ObservacaoPresencaRepository

logger = logging.getLogger(__name__)


class PresencaViewSet(ModelViewSet):
    """ViewSet para gerenciar presenças via API REST."""
    
    queryset = Presenca.objects.select_related("aluno", "turma", "atividade").all()
    serializer_class = PresencaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Customiza o queryset com filtros opcionais."""
        queryset = self.queryset
        
        # Filtros via query parameters
        aluno_cpf = self.request.query_params.get('aluno_cpf')
        turma_id = self.request.query_params.get('turma_id')
        atividade_id = self.request.query_params.get('atividade_id')
        data_inicio = self.request.query_params.get('data_inicio')
        data_fim = self.request.query_params.get('data_fim')
        presente = self.request.query_params.get('presente')
        
        if aluno_cpf:
            queryset = queryset.filter(aluno__cpf=aluno_cpf)
        
        if turma_id:
            queryset = queryset.filter(turma_id=turma_id)
        
        if atividade_id:
            queryset = queryset.filter(atividade_id=atividade_id)
        
        if data_inicio:
            queryset = queryset.filter(data__gte=data_inicio)
        
        if data_fim:
            queryset = queryset.filter(data__lte=data_fim)
        
        if presente is not None:
            queryset = queryset.filter(presente=presente.lower() == 'true')
        
        return queryset.order_by('-data')
    
    @action(detail=False, methods=["get"], url_path="listar_presencas")
    def listar_presencas_action(self, request):
        """Lista todas as presenças."""
        try:
            tipo_presenca = request.query_params.get('tipo', 'todas')
            presencas = listar_presencas(tipo_presenca)
            
            # Paginação
            page = self.paginate_queryset(presencas)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(presencas, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": f"Erro ao listar presenças: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TotalAtividadeMesViewSet(ModelViewSet):
    """ViewSet para gerenciar totais de atividade por mês."""
    
    queryset = TotalAtividadeMes.objects.select_related("atividade", "turma").all()
    serializer_class = TotalAtividadeMesSerializer
    permission_classes = [IsAuthenticated]


class ObservacaoPresencaViewSet(ModelViewSet):
    """ViewSet para gerenciar observações de presença."""
    
    queryset = ObservacaoPresenca.objects.select_related("aluno", "turma").all()
    serializer_class = ObservacaoPresencaSerializer
    permission_classes = [IsAuthenticated]


# Mantendo as funções existentes para compatibilidade

@login_required
@require_POST
def obter_alunos_por_turmas(request):
    """
    API para obter alunos de turmas específicas.

    Retorna lista de alunos e atividades, ou mensagem de erro padronizada.
    """
    try:
        # Obter dados do corpo da requisição
        data = json.loads(request.body)
        turmas_ids = data.get('turmas_ids', [])
        
        if not turmas_ids:
            return JsonResponse({'error': 'Nenhuma turma selecionada.'}, status=400)
        
        # Obter turmas
        turmas = Turma.objects.filter(id__in=turmas_ids)
        
        if not turmas.exists():
            return JsonResponse({'error': 'Nenhuma turma encontrada com os IDs fornecidos.'}, status=404)
        
        # Obter matrículas ativas nas turmas
        matriculas = Matricula.objects.filter(turma__in=turmas, status='A').select_related('aluno')
        
        # Obter alunos únicos
        alunos = []
        alunos_ids = set()
        
        for matricula in matriculas:
            if matricula.aluno.cpf not in alunos_ids:
                alunos.append({
                    'cpf': matricula.aluno.cpf,
                    'nome': matricula.aluno.nome,
                    'foto': matricula.aluno.foto.url if matricula.aluno.foto else None,
                    'numero_iniciatico': matricula.aluno.numero_iniciatico
                })
                alunos_ids.add(matricula.aluno.cpf)
        
        # Obter atividades
        atividades = AtividadeAcademica.objects.all()
        
        atividades_data = [
            {
                'id': atividade.id,
                'titulo': atividade.titulo,
                'descricao': atividade.descricao
            }
            for atividade in atividades
        ]
        
        return JsonResponse({
            'alunos': alunos,
            'atividades': atividades_data
        })
    
    except Exception as e:
        logger.error("Erro ao obter alunos por turmas: %s", e, exc_info=True)
        return JsonResponse({'error': 'Ocorreu um erro inesperado ao buscar alunos. Tente novamente mais tarde.'}, status=500)

@login_required
@require_GET
def obter_atividades_por_data(request):
    """API para obter atividades disponíveis em uma data específica."""
    try:
        data = request.GET.get('data')
        
        if not data:
            return JsonResponse({'error': 'Data não fornecida.'}, status=400)
        
        # Obter atividades para a data
        atividades = AtividadeAcademica.objects.filter(data_inicio__date=data)
        
        atividades_data = [
            {
                'id': atividade.id,
                'titulo': atividade.titulo,
                'descricao': atividade.descricao
            }
            for atividade in atividades
        ]
        
        return JsonResponse({
            'atividades': atividades_data
        })
    
    except Exception as e:
        logger.error("Erro ao obter atividades por data: %s", e, exc_info=True)
        return JsonResponse({'error': f"Erro ao obter atividades: {str(e)}"}, status=500)

@login_required
@require_POST
def salvar_presencas_multiplas(request):
    """API para salvar múltiplas presenças de uma vez."""
    try:
        # Obter dados do corpo da requisição
        data = json.loads(request.body)
        presencas_data = data.get('presencas', [])
        
        if not presencas_data:
            return JsonResponse({'error': 'Nenhuma presença para salvar.'}, status=400)
        
        # Salvar presenças em uma transação
        with transaction.atomic():
            presencas_salvas = 0
            
            for presenca_data in presencas_data:
                aluno_id = presenca_data.get('aluno_id')
                atividade_id = presenca_data.get('atividade_id')
                data_presenca = presenca_data.get('data')
                situacao = presenca_data.get('situacao')
                justificativa = presenca_data.get('justificativa', '')
                
                # Validar dados
                if not all([aluno_id, atividade_id, data_presenca, situacao]):
                    continue
                
                # Obter aluno e atividade
                try:
                    aluno = Aluno.objects.get(cpf=aluno_id)
                    atividade = AtividadeAcademica.objects.get(id=atividade_id)
                except (Aluno.DoesNotExist, AtividadeAcademica.DoesNotExist):
                    continue
                
                # Verificar se já existe presença para este aluno/atividade/data
                presenca, created = Presenca.objects.update_or_create(
                    aluno=aluno,
                    atividade=atividade,
                    data=data_presenca,
                    defaults={
                        'situacao': situacao,
                        'justificativa': justificativa if situacao == 'JUSTIFICADO' else ''
                    }
                )
                
                presencas_salvas += 1
            
            return JsonResponse({
                'success': True,
                'message': f'{presencas_salvas} presenças salvas com sucesso.'
            })
    
    except Exception as e:
        logger.error("Erro ao salvar presenças múltiplas: %s", e, exc_info=True)
        return JsonResponse({'error': f"Erro ao salvar presenças: {str(e)}"}, status=500)