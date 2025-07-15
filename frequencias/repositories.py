"""
Repositórios para o aplicativo frequencias.
Camada de acesso a dados.
"""
from django.db.models import Q, Count, Avg, Sum, Max, Min
from datetime import date, timedelta
from .models import FrequenciaMensal, Carencia


class FrequenciaMensalRepository:
    """Repositório para operações de consulta do modelo FrequenciaMensal."""
    
    @staticmethod
    def listar_todas():
        """Lista todas as frequências mensais com relacionamentos."""
        return FrequenciaMensal.objects.select_related('turma').all()
    
    @staticmethod
    def buscar_por_id(frequencia_id):
        """Busca frequência mensal por ID."""
        try:
            return FrequenciaMensal.objects.select_related('turma').get(id=frequencia_id)
        except FrequenciaMensal.DoesNotExist:
            return None
    
    @staticmethod
    def buscar_por_turma(turma_id):
        """Busca frequências mensais de uma turma."""
        return FrequenciaMensal.objects.filter(
            turma_id=turma_id
        ).order_by('-ano', '-mes')
    
    @staticmethod
    def buscar_por_periodo(ano, mes=None):
        """Busca frequências mensais por período."""
        frequencias = FrequenciaMensal.objects.filter(ano=ano)
        
        if mes:
            frequencias = frequencias.filter(mes=mes)
        
        return frequencias.select_related('turma').order_by('-mes')
    
    @staticmethod
    def buscar_com_filtros(filtros):
        """
        Busca frequências mensais com filtros específicos.
        
        Args:
            filtros (dict): Dicionário com filtros
        """
        frequencias = FrequenciaMensal.objects.select_related('turma').all()
        
        if filtros.get('turma_id'):
            frequencias = frequencias.filter(turma_id=filtros['turma_id'])
        
        if filtros.get('ano'):
            frequencias = frequencias.filter(ano=filtros['ano'])
        
        if filtros.get('mes'):
            frequencias = frequencias.filter(mes=filtros['mes'])
        
        if filtros.get('curso_id'):
            frequencias = frequencias.filter(turma__curso_id=filtros['curso_id'])
        
        if filtros.get('percentual_minimo'):
            frequencias = frequencias.filter(
                percentual_minimo=filtros['percentual_minimo']
            )
        
        if filtros.get('search'):
            search_term = filtros['search']
            frequencias = frequencias.filter(
                Q(turma__nome__icontains=search_term) |
                Q(turma__curso__nome__icontains=search_term)
            )
        
        return frequencias.order_by('-ano', '-mes')
    
    @staticmethod
    def verificar_existencia(turma_id, mes, ano):
        """Verifica se já existe frequência mensal para o período."""
        return FrequenciaMensal.objects.filter(
            turma_id=turma_id,
            mes=mes,
            ano=ano
        ).exists()
    
    @staticmethod
    def obter_anos_disponiveis():
        """Obtém lista de anos com frequências cadastradas."""
        return FrequenciaMensal.objects.values_list(
            'ano', flat=True
        ).distinct().order_by('-ano')
    
    @staticmethod
    def obter_estatisticas_por_turma(turma_id):
        """Obtém estatísticas de frequência por turma."""
        frequencias = FrequenciaMensal.objects.filter(turma_id=turma_id)
        
        total_frequencias = frequencias.count()
        
        if total_frequencias == 0:
            return {
                'total_frequencias': 0,
                'percentual_medio': 0,
                'por_mes': []
            }
        
        # Estatísticas por mês
        por_mes = []
        for frequencia in frequencias:
            carencias = Carencia.objects.filter(frequencia_mensal=frequencia)
            total_alunos = carencias.count()
            liberados = carencias.filter(liberado=True).count()
            
            percentual_liberacao = (liberados / total_alunos * 100) if total_alunos > 0 else 0
            
            por_mes.append({
                'mes': frequencia.mes,
                'ano': frequencia.ano,
                'mes_nome': frequencia.get_mes_display(),
                'total_alunos': total_alunos,
                'liberados': liberados,
                'percentual_liberacao': round(percentual_liberacao, 2)
            })
        
        # Percentual médio
        percentuais = [item['percentual_liberacao'] for item in por_mes if item['total_alunos'] > 0]
        percentual_medio = sum(percentuais) / len(percentuais) if percentuais else 0
        
        return {
            'total_frequencias': total_frequencias,
            'percentual_medio': round(percentual_medio, 2),
            'por_mes': sorted(por_mes, key=lambda x: (x['ano'], x['mes']))
        }
    
    @staticmethod
    def obter_ranking_turmas_por_frequencia(ano=None, limite=10):
        """Obtém ranking de turmas por frequência."""
        frequencias = FrequenciaMensal.objects.select_related('turma')
        
        if ano:
            frequencias = frequencias.filter(ano=ano)
        
        ranking = []
        turmas_processadas = set()
        
        for frequencia in frequencias:
            if frequencia.turma_id in turmas_processadas:
                continue
            
            turmas_processadas.add(frequencia.turma_id)
            estatisticas = FrequenciaMensalRepository.obter_estatisticas_por_turma(
                frequencia.turma_id
            )
            
            ranking.append({
                'turma_id': frequencia.turma_id,
                'turma_nome': frequencia.turma.nome,
                'curso_nome': getattr(frequencia.turma.curso, 'nome', 'N/A'),
                'percentual_medio': estatisticas['percentual_medio'],
                'total_frequencias': estatisticas['total_frequencias']
            })
        
        # Ordenar por percentual médio (decrescente)
        ranking.sort(key=lambda x: x['percentual_medio'], reverse=True)
        
        return ranking[:limite]


class CarenciaRepository:
    """Repositório para operações de consulta do modelo Carencia."""
    
    @staticmethod
    def listar_todas():
        """Lista todas as carências com relacionamentos."""
        return Carencia.objects.select_related(
            'frequencia_mensal',
            'frequencia_mensal__turma',
            'aluno'
        ).all()
    
    @staticmethod
    def buscar_por_id(carencia_id):
        """Busca carência por ID."""
        try:
            return Carencia.objects.select_related(
                'frequencia_mensal',
                'frequencia_mensal__turma',
                'aluno'
            ).get(id=carencia_id)
        except Carencia.DoesNotExist:
            return None
    
    @staticmethod
    def buscar_por_frequencia(frequencia_id):
        """Busca carências de uma frequência mensal."""
        return Carencia.objects.filter(
            frequencia_mensal_id=frequencia_id
        ).select_related('aluno').order_by('aluno__nome')
    
    @staticmethod
    def buscar_por_aluno(aluno_cpf):
        """Busca carências de um aluno."""
        return Carencia.objects.filter(
            aluno__cpf=aluno_cpf
        ).select_related(
            'frequencia_mensal',
            'frequencia_mensal__turma'
        ).order_by('-frequencia_mensal__ano', '-frequencia_mensal__mes')
    
    @staticmethod
    def buscar_por_status(status):
        """Busca carências por status."""
        return Carencia.objects.filter(
            status=status
        ).select_related(
            'frequencia_mensal',
            'frequencia_mensal__turma',
            'aluno'
        ).order_by('-created_at')
    
    @staticmethod
    def buscar_nao_liberadas():
        """Busca carências não liberadas (com problemas de frequência)."""
        return Carencia.objects.filter(
            liberado=False
        ).select_related(
            'frequencia_mensal',
            'frequencia_mensal__turma',
            'aluno'
        ).order_by('-frequencia_mensal__ano', '-frequencia_mensal__mes')
    
    @staticmethod
    def buscar_com_filtros(filtros):
        """
        Busca carências com filtros específicos.
        
        Args:
            filtros (dict): Dicionário com filtros
        """
        carencias = Carencia.objects.select_related(
            'frequencia_mensal',
            'frequencia_mensal__turma',
            'aluno'
        ).all()
        
        if filtros.get('aluno_cpf'):
            carencias = carencias.filter(aluno__cpf=filtros['aluno_cpf'])
        
        if filtros.get('turma_id'):
            carencias = carencias.filter(frequencia_mensal__turma_id=filtros['turma_id'])
        
        if filtros.get('status'):
            carencias = carencias.filter(status=filtros['status'])
        
        if filtros.get('liberado') is not None:
            carencias = carencias.filter(liberado=filtros['liberado'])
        
        if filtros.get('ano'):
            carencias = carencias.filter(frequencia_mensal__ano=filtros['ano'])
        
        if filtros.get('mes'):
            carencias = carencias.filter(frequencia_mensal__mes=filtros['mes'])
        
        if filtros.get('percentual_min'):
            carencias = carencias.filter(
                percentual_presenca__gte=filtros['percentual_min']
            )
        
        if filtros.get('percentual_max'):
            carencias = carencias.filter(
                percentual_presenca__lte=filtros['percentual_max']
            )
        
        if filtros.get('search'):
            search_term = filtros['search']
            carencias = carencias.filter(
                Q(aluno__nome__icontains=search_term) |
                Q(aluno__cpf__icontains=search_term) |
                Q(frequencia_mensal__turma__nome__icontains=search_term)
            )
        
        return carencias.order_by('-frequencia_mensal__ano', '-frequencia_mensal__mes')
    
    @staticmethod
    def contar_por_status():
        """Conta carências por status."""
        return Carencia.objects.values('status').annotate(
            total=Count('id')
        ).order_by('status')
    
    @staticmethod
    def contar_por_turma():
        """Conta carências por turma."""
        return Carencia.objects.values(
            'frequencia_mensal__turma__nome',
            'frequencia_mensal__turma__id'
        ).annotate(
            total=Count('id'),
            nao_liberadas=Count('id', filter=Q(liberado=False)),
            pendentes=Count('id', filter=Q(status='PENDENTE')),
            em_acompanhamento=Count('id', filter=Q(status='EM_ACOMPANHAMENTO')),
            resolvidas=Count('id', filter=Q(status='RESOLVIDO'))
        ).order_by('frequencia_mensal__turma__nome')
    
    @staticmethod
    def obter_alunos_problematicos(limite_carencias=3, periodo_meses=6):
        """
        Obtém alunos com muitas carências no período.
        
        Args:
            limite_carencias (int): Número mínimo de carências
            periodo_meses (int): Período em meses para análise
        """
        # Calcular data limite
        hoje = date.today()
        ano_limite = hoje.year if hoje.month > periodo_meses else hoje.year - 1
        mes_limite = hoje.month - periodo_meses if hoje.month > periodo_meses else 12 + (hoje.month - periodo_meses)
        
        return Carencia.objects.filter(
            frequencia_mensal__ano__gte=ano_limite,
            frequencia_mensal__mes__gte=mes_limite if ano_limite == hoje.year else 1,
            liberado=False
        ).values(
            'aluno__cpf',
            'aluno__nome'
        ).annotate(
            total_carencias=Count('id'),
            media_percentual=Avg('percentual_presenca'),
            numero_carencias_total=Sum('numero_carencias')
        ).filter(
            total_carencias__gte=limite_carencias
        ).order_by('-total_carencias', 'media_percentual')
    
    @staticmethod
    def obter_estatisticas_gerais():
        """Obtém estatísticas gerais das carências."""
        total = Carencia.objects.count()
        liberadas = Carencia.objects.filter(liberado=True).count()
        nao_liberadas = Carencia.objects.filter(liberado=False).count()
        
        # Por status
        por_status = Carencia.objects.values('status').annotate(
            total=Count('id')
        ).order_by('status')
        
        # Percentuais médios
        stats_numericas = Carencia.objects.aggregate(
            media_presenca=Avg('percentual_presenca'),
            media_carencias=Avg('numero_carencias'),
            max_carencias=Max('numero_carencias'),
            min_presenca=Min('percentual_presenca')
        )
        
        # Carências por período (últimos 6 meses)
        seis_meses_atras = date.today().replace(day=1) - timedelta(days=180)
        ano_inicio = seis_meses_atras.year
        mes_inicio = seis_meses_atras.month
        
        por_periodo = Carencia.objects.filter(
            Q(frequencia_mensal__ano__gt=ano_inicio) |
            Q(frequencia_mensal__ano=ano_inicio, frequencia_mensal__mes__gte=mes_inicio)
        ).values(
            'frequencia_mensal__ano',
            'frequencia_mensal__mes'
        ).annotate(
            total=Count('id'),
            nao_liberadas=Count('id', filter=Q(liberado=False))
        ).order_by('frequencia_mensal__ano', 'frequencia_mensal__mes')
        
        return {
            'totais': {
                'total': total,
                'liberadas': liberadas,
                'nao_liberadas': nao_liberadas,
                'percentual_liberadas': (liberadas / total * 100) if total > 0 else 0
            },
            'por_status': list(por_status),
            'medias': {
                'media_presenca': round(float(stats_numericas['media_presenca'] or 0), 2),
                'media_carencias': round(float(stats_numericas['media_carencias'] or 0), 2),
                'max_carencias': stats_numericas['max_carencias'] or 0,
                'min_presenca': round(float(stats_numericas['min_presenca'] or 0), 2)
            },
            'por_periodo': list(por_periodo)
        }
    
    @staticmethod
    def verificar_carencia_existente(frequencia_id, aluno_cpf):
        """Verifica se já existe carência para aluno/frequência."""
        return Carencia.objects.filter(
            frequencia_mensal_id=frequencia_id,
            aluno__cpf=aluno_cpf
        ).exists()
    
    @staticmethod
    def obter_historico_aluno(aluno_cpf, limite=10):
        """Obtém histórico de carências de um aluno."""
        return Carencia.objects.filter(
            aluno__cpf=aluno_cpf
        ).select_related(
            'frequencia_mensal',
            'frequencia_mensal__turma'
        ).order_by(
            '-frequencia_mensal__ano',
            '-frequencia_mensal__mes'
        )[:limite]
