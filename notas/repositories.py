"""
Repositories para o app Notas - Camada de acesso a dados
"""
import importlib
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class NotaRepository:
    """
    Repository para gerenciar acesso aos dados das notas
    """
    
    def __init__(self):
        self.model = self._get_model()
    
    def _get_model(self):
        """Importação dinâmica do modelo"""
        try:
            models_module = importlib.import_module('notas.models')
            return getattr(models_module, 'Nota')
        except (ImportError, AttributeError) as e:
            logger.error(f"Erro ao importar modelo Nota: {e}")
            raise ImportError(f"Erro ao importar modelo Nota: {e}")
    
    def get_all(self):
        """Retorna todas as notas"""
        try:
            return self.model.objects.select_related('aluno', 'atividade').all()
        except Exception as e:
            logger.error(f"Erro ao buscar todas as notas: {e}")
            raise
    
    def get_by_id(self, nota_id):
        """Retorna uma nota por ID"""
        try:
            return self.model.objects.select_related('aluno', 'atividade').get(id=nota_id)
        except self.model.DoesNotExist:
            raise ObjectDoesNotExist(f"Nota com ID {nota_id} não encontrada")
        except Exception as e:
            logger.error(f"Erro ao buscar nota por ID {nota_id}: {e}")
            raise
    
    def get_by_aluno(self, aluno_id):
        """Retorna notas de um aluno específico"""
        try:
            return self.model.objects.select_related('aluno', 'atividade').filter(aluno_id=aluno_id)
        except Exception as e:
            logger.error(f"Erro ao buscar notas do aluno {aluno_id}: {e}")
            raise
    
    def get_by_turma(self, turma_id):
        """Retorna notas de uma turma específica"""
        try:
            return self.model.objects.select_related('aluno', 'atividade').filter(atividade__turma_id=turma_id)
        except Exception as e:
            logger.error(f"Erro ao buscar notas da turma {turma_id}: {e}")
            raise
    
    def get_by_atividade(self, atividade_id):
        """Retorna notas de uma atividade específica"""
        try:
            return self.model.objects.select_related('aluno', 'atividade').filter(atividade_id=atividade_id)
        except Exception as e:
            logger.error(f"Erro ao buscar notas da atividade {atividade_id}: {e}")
            raise
    
    def get_by_aluno_and_atividade(self, aluno_id, atividade_id):
        """Retorna nota específica de um aluno em uma atividade"""
        try:
            return self.model.objects.select_related('aluno', 'atividade').filter(
                aluno_id=aluno_id, atividade_id=atividade_id
            ).first()
        except Exception as e:
            logger.error(f"Erro ao buscar nota do aluno {aluno_id} na atividade {atividade_id}: {e}")
            raise
    
    def get_by_periodo(self, data_inicio, data_fim):
        """Retorna notas por período"""
        try:
            return self.model.objects.select_related('aluno', 'atividade').filter(
                data_registro__gte=data_inicio,
                data_registro__lte=data_fim
            )
        except Exception as e:
            logger.error(f"Erro ao buscar notas por período: {e}")
            raise
    
    def get_by_valor_range(self, valor_min, valor_max):
        """Retorna notas dentro de uma faixa de valores"""
        try:
            return self.model.objects.select_related('aluno', 'atividade').filter(
                valor__gte=valor_min,
                valor__lte=valor_max
            )
        except Exception as e:
            logger.error(f"Erro ao buscar notas por faixa de valor: {e}")
            raise
    
    @transaction.atomic
    def create(self, nota_data):
        """Cria uma nova nota"""
        try:
            # Buscar instâncias relacionadas
            aluno = self._get_aluno_by_id(nota_data.get('aluno_id'))
            atividade = self._get_atividade_by_id(nota_data.get('atividade_id'))
            
            # Criar nota
            nota = self.model.objects.create(
                aluno=aluno,
                atividade=atividade,
                valor=nota_data.get('valor'),
                observacoes=nota_data.get('observacoes', ''),
                data_registro=nota_data.get('data_registro', timezone.now())
            )
            
            logger.info(f"Nota criada com sucesso: ID {nota.id}")
            return nota
        except Exception as e:
            logger.error(f"Erro ao criar nota: {e}")
            raise
    
    @transaction.atomic
    def update(self, nota_id, nota_data):
        """Atualiza uma nota existente"""
        try:
            nota = self.get_by_id(nota_id)
            
            # Atualizar campos
            if 'valor' in nota_data:
                nota.valor = nota_data['valor']
            if 'observacoes' in nota_data:
                nota.observacoes = nota_data['observacoes']
            if 'aluno_id' in nota_data:
                nota.aluno = self._get_aluno_by_id(nota_data['aluno_id'])
            if 'atividade_id' in nota_data:
                nota.atividade = self._get_atividade_by_id(nota_data['atividade_id'])
            
            nota.save()
            
            logger.info(f"Nota atualizada com sucesso: ID {nota_id}")
            return nota
        except Exception as e:
            logger.error(f"Erro ao atualizar nota {nota_id}: {e}")
            raise
    
    @transaction.atomic
    def delete(self, nota_id):
        """Remove uma nota"""
        try:
            nota = self.get_by_id(nota_id)
            nota.delete()
            logger.info(f"Nota deletada com sucesso: ID {nota_id}")
            return True
        except Exception as e:
            logger.error(f"Erro ao deletar nota {nota_id}: {e}")
            raise
    
    def exists(self, nota_id):
        """Verifica se uma nota existe"""
        try:
            return self.model.objects.filter(id=nota_id).exists()
        except Exception as e:
            logger.error(f"Erro ao verificar existência da nota {nota_id}: {e}")
            raise
    
    def count(self):
        """Retorna o total de notas"""
        try:
            return self.model.objects.count()
        except Exception as e:
            logger.error(f"Erro ao contar notas: {e}")
            raise
    
    def get_media_by_aluno(self, aluno_id):
        """Calcula a média de um aluno"""
        try:
            from django.db.models import Avg
            resultado = self.model.objects.filter(aluno_id=aluno_id).aggregate(
                media=Avg('valor')
            )
            return resultado['media'] or 0
        except Exception as e:
            logger.error(f"Erro ao calcular média do aluno {aluno_id}: {e}")
            raise
    
    def get_media_by_turma(self, turma_id):
        """Calcula a média de uma turma"""
        try:
            from django.db.models import Avg
            resultado = self.model.objects.filter(atividade__turma_id=turma_id).aggregate(
                media=Avg('valor')
            )
            return resultado['media'] or 0
        except Exception as e:
            logger.error(f"Erro ao calcular média da turma {turma_id}: {e}")
            raise
    
    def get_estatisticas_notas(self):
        """Retorna estatísticas gerais das notas"""
        try:
            from django.db.models import Avg, Max, Min, Count
            
            stats = self.model.objects.aggregate(
                total=Count('id'),
                media_geral=Avg('valor'),
                nota_maxima=Max('valor'),
                nota_minima=Min('valor')
            )
            
            return {
                'total_notas': stats['total'] or 0,
                'media_geral': round(stats['media_geral'] or 0, 2),
                'nota_maxima': stats['nota_maxima'] or 0,
                'nota_minima': stats['nota_minima'] or 0
            }
        except Exception as e:
            logger.error(f"Erro ao calcular estatísticas: {e}")
            raise
    
    def _get_aluno_by_id(self, aluno_id):
        """Busca aluno por ID usando importação dinâmica"""
        try:
            alunos_module = importlib.import_module('alunos.models')
            Aluno = getattr(alunos_module, 'Aluno')
            return Aluno.objects.get(id=aluno_id)
        except Exception as e:
            logger.error(f"Erro ao buscar aluno {aluno_id}: {e}")
            raise ObjectDoesNotExist(f"Aluno com ID {aluno_id} não encontrado")
    
    def _get_atividade_by_id(self, atividade_id):
        """Busca atividade por ID usando importação dinâmica"""
        try:
            atividades_module = importlib.import_module('atividades.models')
            Atividade = getattr(atividades_module, 'Atividade')
            return Atividade.objects.get(id=atividade_id)
        except Exception as e:
            logger.error(f"Erro ao buscar atividade {atividade_id}: {e}")
            raise ObjectDoesNotExist(f"Atividade com ID {atividade_id} não encontrada")
