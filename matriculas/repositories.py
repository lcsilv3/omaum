"""
Repositórios para o aplicativo matriculas.
Camada de acesso a dados.
"""
from django.db.models import Q, Count
from django.utils import timezone
from .models import Matricula

class MatriculaRepository:
    """Repositório para operações de consulta do modelo Matricula."""
    
    @staticmethod
    def listar_todas():
        """Lista todas as matrículas com relacionamentos."""
        return Matricula.objects.select_related('aluno', 'turma', 'turma__curso').all()
    
    @staticmethod
    def buscar_por_id(matricula_id):
        """Busca matrícula por ID."""
        try:
            return Matricula.objects.select_related('aluno', 'turma', 'turma__curso').get(id=matricula_id)
        except Matricula.DoesNotExist:
            return None
    
    @staticmethod
    def buscar_por_aluno_e_turma(aluno_cpf, turma_id):
        """Busca matrícula por aluno e turma."""
        return Matricula.objects.filter(
            aluno__cpf=aluno_cpf,
            turma_id=turma_id
        ).first()
    
    @staticmethod
    def listar_por_aluno(aluno_cpf, apenas_ativas=False):
        """Lista matrículas de um aluno."""
        matriculas = Matricula.objects.filter(aluno__cpf=aluno_cpf)
        
        if apenas_ativas:
            matriculas = matriculas.filter(status='A', ativa=True)
        
        return matriculas.select_related('turma', 'turma__curso').order_by('-data_matricula')
    
    @staticmethod
    def listar_por_turma(turma_id, apenas_ativas=False):
        """Lista matrículas de uma turma."""
        matriculas = Matricula.objects.filter(turma_id=turma_id)
        
        if apenas_ativas:
            matriculas = matriculas.filter(status='A', ativa=True)
        
        return matriculas.select_related('aluno').order_by('aluno__nome')
    
    @staticmethod
    def buscar_com_filtros(filtros):
        """
        Busca matrículas com filtros específicos.
        
        Args:
            filtros (dict): Dicionário com filtros
                - aluno_cpf: CPF do aluno
                - turma_id: ID da turma
                - status: Status da matrícula
                - data_inicio: Data início para filtro de data_matricula
                - data_fim: Data fim para filtro de data_matricula
                - curso_id: ID do curso (via turma)
                - search: Termo de busca (nome aluno ou turma)
        
        Returns:
            QuerySet: Matrículas filtradas
        """
        matriculas = Matricula.objects.select_related('aluno', 'turma', 'turma__curso').all()
        
        if filtros.get('aluno_cpf'):
            matriculas = matriculas.filter(aluno__cpf=filtros['aluno_cpf'])
        
        if filtros.get('turma_id'):
            matriculas = matriculas.filter(turma_id=filtros['turma_id'])
        
        if filtros.get('status'):
            matriculas = matriculas.filter(status=filtros['status'])
        
        if filtros.get('data_inicio'):
            matriculas = matriculas.filter(data_matricula__gte=filtros['data_inicio'])
        
        if filtros.get('data_fim'):
            matriculas = matriculas.filter(data_matricula__lte=filtros['data_fim'])
        
        if filtros.get('curso_id'):
            matriculas = matriculas.filter(turma__curso_id=filtros['curso_id'])
        
        if filtros.get('search'):
            search_term = filtros['search']
            matriculas = matriculas.filter(
                Q(aluno__nome__icontains=search_term) |
                Q(aluno__cpf__icontains=search_term) |
                Q(turma__nome__icontains=search_term) |
                Q(turma__curso__nome__icontains=search_term)
            )
        
        return matriculas.order_by('-data_matricula')
    
    @staticmethod
    def contar_por_status():
        """Conta matrículas por status."""
        return Matricula.objects.values('status').annotate(
            total=Count('id')
        ).order_by('status')
    
    @staticmethod
    def contar_por_turma():
        """Conta matrículas por turma."""
        return Matricula.objects.values(
            'turma__nome',
            'turma__id'
        ).annotate(
            total=Count('id'),
            ativas=Count('id', filter=Q(status='A'))
        ).order_by('turma__nome')
    
    @staticmethod
    def matriculas_ativas():
        """Retorna apenas matrículas ativas."""
        return Matricula.objects.filter(
            status='A',
            ativa=True
        ).select_related('aluno', 'turma', 'turma__curso')
    
    @staticmethod
    def matriculas_canceladas():
        """Retorna apenas matrículas canceladas."""
        return Matricula.objects.filter(
            status='C'
        ).select_related('aluno', 'turma', 'turma__curso')
    
    @staticmethod
    def matriculas_finalizadas():
        """Retorna apenas matrículas finalizadas."""
        return Matricula.objects.filter(
            status='F'
        ).select_related('aluno', 'turma', 'turma__curso')
    
    @staticmethod
    def matriculas_por_periodo(data_inicio, data_fim):
        """Retorna matrículas em um período específico."""
        return Matricula.objects.filter(
            data_matricula__gte=data_inicio,
            data_matricula__lte=data_fim
        ).select_related('aluno', 'turma', 'turma__curso').order_by('-data_matricula')
    
    @staticmethod
    def verificar_matricula_existente(aluno_cpf, turma_id):
        """Verifica se já existe matrícula para o aluno na turma."""
        return Matricula.objects.filter(
            aluno__cpf=aluno_cpf,
            turma_id=turma_id,
            status__in=['A', 'F']  # Ativa ou Finalizada
        ).exists()
    
    @staticmethod
    def obter_estatisticas_gerais():
        """Obtém estatísticas gerais das matrículas."""
        total = Matricula.objects.count()
        ativas = Matricula.objects.filter(status='A').count()
        canceladas = Matricula.objects.filter(status='C').count()
        finalizadas = Matricula.objects.filter(status='F').count()
        
        # Matrículas por mês (últimos 6 meses)
        from datetime import timedelta
        hoje = timezone.now().date()
        seis_meses_atras = hoje - timedelta(days=180)
        
        matriculas_recentes = Matricula.objects.filter(
            data_matricula__gte=seis_meses_atras
        ).values(
            'data_matricula__year',
            'data_matricula__month'
        ).annotate(
            total=Count('id')
        ).order_by('data_matricula__year', 'data_matricula__month')
        
        return {
            'total': total,
            'ativas': ativas,
            'canceladas': canceladas,
            'finalizadas': finalizadas,
            'percentual_ativas': (ativas / total * 100) if total > 0 else 0,
            'matriculas_por_mes': list(matriculas_recentes)
        }
    
    @staticmethod
    def alunos_com_multiplas_matriculas():
        """Retorna alunos que possuem múltiplas matrículas ativas."""
        return Matricula.objects.filter(
            status='A'
        ).values(
            'aluno__cpf',
            'aluno__nome'
        ).annotate(
            total_matriculas=Count('id')
        ).filter(
            total_matriculas__gt=1
        ).order_by('-total_matriculas')
