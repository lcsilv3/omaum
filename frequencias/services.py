"""
Serviços para o aplicativo frequencias.
Contém a lógica de negócios complexa.
"""
import logging
from django.core.exceptions import ValidationError
from django.db import transaction, models
from importlib import import_module

logger = logging.getLogger(__name__)

def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

def get_turma_model():
    """Obtém o modelo Turma dinamicamente."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

def get_matricula_model():
    """Obtém o modelo Matricula dinamicamente."""
    matriculas_module = import_module("matriculas.models")
    return getattr(matriculas_module, "Matricula")

def get_presenca_model():
    """Obtém o modelo Presenca dinamicamente."""
    presencas_module = import_module("presencas.models")
    return getattr(presencas_module, "Presenca")

def get_atividade_model():
    """Obtém o modelo AtividadeAcademica dinamicamente."""
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "AtividadeAcademica")

def get_frequencia_models():
    """Obtém os modelos de frequência dinamicamente."""
    from .models import FrequenciaMensal, Carencia
    
    # Tentar obter modelos de notificação se existirem
    try:
        NotificacaoCarencia = getattr(import_module("frequencias.models"), "NotificacaoCarencia", None)
    except (ImportError, AttributeError):
        NotificacaoCarencia = None
    
    return {
        'FrequenciaMensal': FrequenciaMensal,
        'Carencia': Carencia,
        'NotificacaoCarencia': NotificacaoCarencia
    }

def listar_frequencias_mensais():
    """Lista todas as frequências mensais."""
    modelos = get_frequencia_models()
    return modelos['FrequenciaMensal'].objects.select_related('turma').order_by('-ano', '-mes')

def buscar_frequencias_por_filtros(filtros):
    """
    Busca frequências com filtros específicos.
    
    Args:
        filtros (dict): Dicionário com filtros
    """
    modelos = get_frequencia_models()
    frequencias = modelos['FrequenciaMensal'].objects.select_related('turma').all()
    
    if filtros.get('turma_id'):
        frequencias = frequencias.filter(turma_id=filtros['turma_id'])
    
    if filtros.get('ano'):
        frequencias = frequencias.filter(ano=filtros['ano'])
    
    if filtros.get('mes'):
        frequencias = frequencias.filter(mes=filtros['mes'])
    
    if filtros.get('curso_id'):
        frequencias = frequencias.filter(turma__curso_id=filtros['curso_id'])
    
    return frequencias.order_by('-ano', '-mes')

def criar_frequencia_mensal(dados_frequencia):
    """
    Cria uma nova frequência mensal.
    
    Args:
        dados_frequencia (dict): Dados da frequência
    """
    try:
        with transaction.atomic():
            Turma = get_turma_model()
            modelos = get_frequencia_models()
            
            # Buscar turma
            turma = Turma.objects.get(id=dados_frequencia['turma_id'])
            
            # Verificar se já existe frequência para este período
            frequencia_existente = modelos['FrequenciaMensal'].objects.filter(
                turma=turma,
                mes=dados_frequencia['mes'],
                ano=dados_frequencia['ano']
            ).exists()
            
            if frequencia_existente:
                raise ValidationError("Já existe frequência mensal para este período.")
            
            # Criar frequência mensal
            frequencia = modelos['FrequenciaMensal'].objects.create(
                turma=turma,
                mes=dados_frequencia['mes'],
                ano=dados_frequencia['ano'],
                percentual_minimo=dados_frequencia.get('percentual_minimo', 75)
            )
            
            # Calcular carências automaticamente
            if dados_frequencia.get('calcular_carencias', True):
                frequencia.calcular_carencias()
            
            logger.info(f"Frequência mensal criada: {frequencia}")
            return frequencia
            
    except Turma.DoesNotExist:
        raise ValidationError("Turma não encontrada.")
    except Exception as e:
        logger.error(f"Erro ao criar frequência mensal: {str(e)}")
        raise ValidationError(f"Erro ao criar frequência mensal: {str(e)}")

def atualizar_frequencia_mensal(frequencia_id, dados_atualizacao):
    """
    Atualiza uma frequência mensal existente.
    
    Args:
        frequencia_id (int): ID da frequência
        dados_atualizacao (dict): Dados para atualização
    """
    try:
        with transaction.atomic():
            modelos = get_frequencia_models()
            frequencia = modelos['FrequenciaMensal'].objects.get(id=frequencia_id)
            
            # Campos permitidos para atualização
            campos_permitidos = ['percentual_minimo']
            
            for campo in campos_permitidos:
                if campo in dados_atualizacao:
                    setattr(frequencia, campo, dados_atualizacao[campo])
            
            frequencia.save()
            
            # Recalcular carências se solicitado
            if dados_atualizacao.get('recalcular_carencias', False):
                frequencia.calcular_carencias()
            
            logger.info(f"Frequência mensal atualizada: {frequencia}")
            return frequencia
            
    except modelos['FrequenciaMensal'].DoesNotExist:
        raise ValidationError("Frequência mensal não encontrada.")
    except Exception as e:
        logger.error(f"Erro ao atualizar frequência mensal: {str(e)}")
        raise ValidationError(f"Erro ao atualizar frequência mensal: {str(e)}")

def excluir_frequencia_mensal(frequencia_id):
    """
    Exclui uma frequência mensal.
    
    Args:
        frequencia_id (int): ID da frequência
    """
    try:
        with transaction.atomic():
            modelos = get_frequencia_models()
            frequencia = modelos['FrequenciaMensal'].objects.get(id=frequencia_id)
            
            # Verificar dependências (carências, notificações)
            carencias = modelos['Carencia'].objects.filter(frequencia_mensal=frequencia)
            if carencias.exists():
                carencias.delete()  # Excluir carências em cascata
            
            frequencia.delete()
            
            logger.info(f"Frequência mensal excluída: ID {frequencia_id}")
            return True
            
    except modelos['FrequenciaMensal'].DoesNotExist:
        raise ValidationError("Frequência mensal não encontrada.")
    except Exception as e:
        logger.error(f"Erro ao excluir frequência mensal: {str(e)}")
        raise ValidationError(f"Erro ao excluir frequência mensal: {str(e)}")

def recalcular_carencias_frequencia(frequencia_id):
    """
    Recalcula as carências de uma frequência mensal.
    
    Args:
        frequencia_id (int): ID da frequência
    """
    try:
        modelos = get_frequencia_models()
        frequencia = modelos['FrequenciaMensal'].objects.get(id=frequencia_id)
        
        frequencia.calcular_carencias()
        
        logger.info(f"Carências recalculadas para frequência: {frequencia}")
        return frequencia
        
    except modelos['FrequenciaMensal'].DoesNotExist:
        raise ValidationError("Frequência mensal não encontrada.")
    except Exception as e:
        logger.error(f"Erro ao recalcular carências: {str(e)}")
        raise ValidationError(f"Erro ao recalcular carências: {str(e)}")

def obter_carencias_por_frequencia(frequencia_id, apenas_pendentes=False):
    """Obtém carências de uma frequência mensal."""
    modelos = get_frequencia_models()
    carencias = modelos['Carencia'].objects.filter(
        frequencia_mensal_id=frequencia_id
    ).select_related('aluno')
    
    if apenas_pendentes:
        carencias = carencias.filter(liberado=False)
    
    return carencias.order_by('aluno__nome')

def atualizar_carencia(carencia_id, dados_atualizacao):
    """
    Atualiza uma carência.
    
    Args:
        carencia_id (int): ID da carência
        dados_atualizacao (dict): Dados para atualização
    """
    try:
        with transaction.atomic():
            modelos = get_frequencia_models()
            carencia = modelos['Carencia'].objects.get(id=carencia_id)
            
            # Campos permitidos para atualização
            campos_permitidos = ['status', 'observacoes', 'liberado']
            
            for campo in campos_permitidos:
                if campo in dados_atualizacao:
                    setattr(carencia, campo, dados_atualizacao[campo])
            
            carencia.save()
            
            logger.info(f"Carência atualizada: {carencia}")
            return carencia
            
    except modelos['Carencia'].DoesNotExist:
        raise ValidationError("Carência não encontrada.")
    except Exception as e:
        logger.error(f"Erro ao atualizar carência: {str(e)}")
        raise ValidationError(f"Erro ao atualizar carência: {str(e)}")

def resolver_carencia(carencia_id, observacoes=''):
    """
    Resolve uma carência marcando-a como resolvida.
    
    Args:
        carencia_id (int): ID da carência
        observacoes (str): Observações sobre a resolução
    """
    try:
        dados_atualizacao = {
            'status': 'RESOLVIDO',
            'liberado': True,
            'observacoes': observacoes
        }
        
        return atualizar_carencia(carencia_id, dados_atualizacao)
        
    except Exception as e:
        logger.error(f"Erro ao resolver carência: {str(e)}")
        raise ValidationError(f"Erro ao resolver carência: {str(e)}")

def iniciar_acompanhamento_carencia(carencia_id, observacoes=''):
    """
    Inicia acompanhamento de uma carência.
    
    Args:
        carencia_id (int): ID da carência
        observacoes (str): Observações sobre o acompanhamento
    """
    try:
        dados_atualizacao = {
            'status': 'EM_ACOMPANHAMENTO',
            'observacoes': observacoes
        }
        
        return atualizar_carencia(carencia_id, dados_atualizacao)
        
    except Exception as e:
        logger.error(f"Erro ao iniciar acompanhamento: {str(e)}")
        raise ValidationError(f"Erro ao iniciar acompanhamento: {str(e)}")

def obter_estatisticas_frequencia(frequencia_id):
    """
    Obtém estatísticas de uma frequência mensal.
    
    Args:
        frequencia_id (int): ID da frequência
    
    Returns:
        dict: Estatísticas da frequência
    """
    try:
        modelos = get_frequencia_models()
        frequencia = modelos['FrequenciaMensal'].objects.get(id=frequencia_id)
        
        carencias = modelos['Carencia'].objects.filter(frequencia_mensal=frequencia)
        
        total_alunos = carencias.count()
        liberados = carencias.filter(liberado=True).count()
        com_carencia = carencias.filter(liberado=False).count()
        pendentes = carencias.filter(status='PENDENTE').count()
        em_acompanhamento = carencias.filter(status='EM_ACOMPANHAMENTO').count()
        resolvidos = carencias.filter(status='RESOLVIDO').count()
        
        # Média de presença
        if total_alunos > 0:
            media_presenca = carencias.aggregate(
                media=models.Avg('percentual_presenca')
            )['media'] or 0
        else:
            media_presenca = 0
        
        return {
            'frequencia': {
                'id': frequencia.id,
                'turma': frequencia.turma.nome,
                'periodo': f"{frequencia.get_mes_display()}/{frequencia.ano}",
                'percentual_minimo': frequencia.percentual_minimo
            },
            'totais': {
                'total_alunos': total_alunos,
                'liberados': liberados,
                'com_carencia': com_carencia,
                'percentual_liberados': (liberados / total_alunos * 100) if total_alunos > 0 else 0
            },
            'status_carencias': {
                'pendentes': pendentes,
                'em_acompanhamento': em_acompanhamento,
                'resolvidos': resolvidos
            },
            'media_presenca': round(float(media_presenca), 2)
        }
        
    except modelos['FrequenciaMensal'].DoesNotExist:
        raise ValidationError("Frequência mensal não encontrada.")
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {str(e)}")
        raise ValidationError(f"Erro ao obter estatísticas: {str(e)}")

def gerar_relatorio_frequencias(filtros=None):
    """
    Gera relatório de frequências com base nos filtros.
    
    Args:
        filtros (dict): Filtros para o relatório
    
    Returns:
        dict: Dados do relatório
    """
    try:
        get_frequencia_models()
        
        if filtros:
            frequencias = buscar_frequencias_por_filtros(filtros)
        else:
            frequencias = listar_frequencias_mensais()
        
        relatorio_dados = []
        
        for frequencia in frequencias:
            estatisticas = obter_estatisticas_frequencia(frequencia.id)
            relatorio_dados.append(estatisticas)
        
        # Estatísticas gerais do relatório
        if relatorio_dados:
            total_frequencias = len(relatorio_dados)
            media_liberacao = sum(item['totais']['percentual_liberados'] for item in relatorio_dados) / total_frequencias
            total_alunos_geral = sum(item['totais']['total_alunos'] for item in relatorio_dados)
            total_liberados_geral = sum(item['totais']['liberados'] for item in relatorio_dados)
        else:
            total_frequencias = 0
            media_liberacao = 0
            total_alunos_geral = 0
            total_liberados_geral = 0
        
        return {
            'frequencias': relatorio_dados,
            'resumo': {
                'total_frequencias': total_frequencias,
                'media_liberacao': round(media_liberacao, 2),
                'total_alunos': total_alunos_geral,
                'total_liberados': total_liberados_geral,
                'percentual_geral': (total_liberados_geral / total_alunos_geral * 100) if total_alunos_geral > 0 else 0
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar relatório: {str(e)}")
        raise ValidationError(f"Erro ao gerar relatório: {str(e)}")

def calcular_frequencia_aluno_periodo(aluno_cpf, data_inicio, data_fim):
    """
    Calcula a frequência de um aluno em um período específico.
    
    Args:
        aluno_cpf (str): CPF do aluno
        data_inicio (date): Data início do período
        data_fim (date): Data fim do período
    
    Returns:
        dict: Dados de frequência do aluno
    """
    try:
        Presenca = get_presenca_model()
        Aluno = get_aluno_model()
        
        # Buscar aluno
        aluno = Aluno.objects.get(cpf=aluno_cpf)
        
        # Buscar presenças no período
        presencas = Presenca.objects.filter(
            aluno=aluno,
            data__gte=data_inicio,
            data__lte=data_fim
        )
        
        total_registros = presencas.count()
        total_presencas = presencas.filter(presente=True).count()
        total_faltas = presencas.filter(presente=False).count()
        
        percentual_presenca = (total_presencas / total_registros * 100) if total_registros > 0 else 0
        
        return {
            'aluno': {
                'cpf': aluno.cpf,
                'nome': aluno.nome
            },
            'periodo': {
                'inicio': data_inicio,
                'fim': data_fim
            },
            'frequencia': {
                'total_registros': total_registros,
                'total_presencas': total_presencas,
                'total_faltas': total_faltas,
                'percentual_presenca': round(percentual_presenca, 2)
            }
        }
        
    except Aluno.DoesNotExist:
        raise ValidationError("Aluno não encontrado.")
    except Exception as e:
        logger.error(f"Erro ao calcular frequência do aluno: {str(e)}")
        raise ValidationError(f"Erro ao calcular frequência do aluno: {str(e)}")
