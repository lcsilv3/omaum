"""
Serviços para o aplicativo presencas.
Contém a lógica de negócios complexa.
"""
import logging
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from importlib import import_module
from datetime import date, datetime

# Importar nova calculadora de estatísticas
from .services.calculadora_estatisticas import CalculadoraEstatisticas

logger = logging.getLogger(__name__)

def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

def get_turma_model():
    """Obtém o modelo Turma dinamicamente."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

def get_atividade_model():
    """Obtém o modelo AtividadeAcademica dinamicamente."""
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "AtividadeAcademica")

def get_presenca_models():
    """Obtém os modelos de presença dinamicamente."""
    from .models import Presenca, TotalAtividadeMes, ObservacaoPresenca
    
    # Tentar obter modelos específicos de atividades
    try:
        atividades_module = import_module("atividades.models")
        PresencaAcademica = getattr(atividades_module, "PresencaAcademica", None)
        PresencaRitualistica = getattr(atividades_module, "PresencaRitualistica", None)
    except (ImportError, AttributeError):
        PresencaAcademica = None
        PresencaRitualistica = None
    
    return {
        'Presenca': Presenca,
        'TotalAtividadeMes': TotalAtividadeMes,
        'ObservacaoPresenca': ObservacaoPresenca,
        'PresencaAcademica': PresencaAcademica,
        'PresencaRitualistica': PresencaRitualistica
    }

def listar_presencas(tipo_presenca='academica'):
    """
    Lista presenças de acordo com o tipo.
    
    Args:
        tipo_presenca (str): 'academica', 'ritualistica' ou 'todas'
    """
    modelos = get_presenca_models()
    
    if tipo_presenca == 'academica' and modelos['PresencaAcademica']:
        return modelos['PresencaAcademica'].objects.select_related(
            'aluno', 'turma', 'atividade'
        ).order_by('-data')
    elif tipo_presenca == 'ritualistica' and modelos['PresencaRitualistica']:
        return modelos['PresencaRitualistica'].objects.select_related(
            'aluno', 'atividade'
        ).order_by('-data')
    else:
        return modelos['Presenca'].objects.select_related(
            'aluno', 'turma', 'atividade'
        ).order_by('-data')

def buscar_presencas_por_filtros(filtros):
    """
    Busca presenças com filtros específicos.
    
    Args:
        filtros (dict): Dicionário com filtros
    """
    modelos = get_presenca_models()
    presencas = modelos['Presenca'].objects.select_related(
        'aluno', 'turma', 'atividade'
    ).all()
    
    if filtros.get('aluno_cpf'):
        presencas = presencas.filter(aluno__cpf=filtros['aluno_cpf'])
    
    if filtros.get('turma_id'):
        presencas = presencas.filter(turma_id=filtros['turma_id'])
    
    if filtros.get('atividade_id'):
        presencas = presencas.filter(atividade_id=filtros['atividade_id'])
    
    if filtros.get('data_inicio'):
        presencas = presencas.filter(data__gte=filtros['data_inicio'])
    
    if filtros.get('data_fim'):
        presencas = presencas.filter(data__lte=filtros['data_fim'])
    
    if filtros.get('presente') is not None:
        presencas = presencas.filter(presente=filtros['presente'])
    
    return presencas.order_by('-data')

def registrar_presenca(dados_presenca):
    """
    Registra uma nova presença.
    
    Args:
        dados_presenca (dict): Dados da presença
    """
    try:
        with transaction.atomic():
            Aluno = get_aluno_model()
            Turma = get_turma_model()
            Atividade = get_atividade_model()
            modelos = get_presenca_models()
            
            # Buscar relacionamentos
            aluno = Aluno.objects.get(cpf=dados_presenca['aluno_cpf'])
            turma = Turma.objects.get(id=dados_presenca['turma_id']) if dados_presenca.get('turma_id') else None
            atividade = Atividade.objects.get(id=dados_presenca['atividade_id']) if dados_presenca.get('atividade_id') else None
            
            # Validar data
            data_presenca = dados_presenca.get('data')
            if isinstance(data_presenca, str):
                data_presenca = datetime.strptime(data_presenca, '%Y-%m-%d').date()
            elif isinstance(data_presenca, datetime):
                data_presenca = data_presenca.date()
            
            if data_presenca > date.today():
                raise ValidationError("A data da presença não pode ser futura.")
            
            # Verificar se já existe presença para essa data
            presenca_existente = modelos['Presenca'].objects.filter(
                aluno=aluno,
                turma=turma,
                data=data_presenca
            ).exists()
            
            if presenca_existente:
                raise ValidationError("Já existe registro de presença para este aluno nesta data.")
            
            # Criar presença
            presenca = modelos['Presenca'].objects.create(
                aluno=aluno,
                turma=turma,
                atividade=atividade,
                data=data_presenca,
                presente=dados_presenca.get('presente', True),
                justificativa=dados_presenca.get('justificativa', ''),
                registrado_por=dados_presenca.get('registrado_por', 'Sistema')
            )
            
            logger.info(f"Presença registrada: {presenca}")
            return presenca
            
    except (Aluno.DoesNotExist, Turma.DoesNotExist, Atividade.DoesNotExist) as e:
        raise ValidationError(f"Relacionamento não encontrado: {str(e)}")
    except Exception as e:
        logger.error(f"Erro ao registrar presença: {str(e)}")
        raise ValidationError(f"Erro ao registrar presença: {str(e)}")

def registrar_presencas_multiplas(lista_presencas):
    """
    Registra múltiplas presenças de uma vez.
    
    Args:
        lista_presencas (list): Lista com dados das presenças
    """
    presencas_criadas = []
    erros = []
    
    with transaction.atomic():
        for dados in lista_presencas:
            try:
                presenca = registrar_presenca(dados)
                presencas_criadas.append(presenca)
            except ValidationError as e:
                erros.append({
                    'dados': dados,
                    'erro': str(e)
                })
    
    return {
        'criadas': presencas_criadas,
        'erros': erros,
        'total_criadas': len(presencas_criadas),
        'total_erros': len(erros)
    }

def atualizar_presenca(presenca_id, dados_atualizacao):
    """
    Atualiza uma presença existente.
    
    Args:
        presenca_id (int): ID da presença
        dados_atualizacao (dict): Dados para atualização
    """
    try:
        with transaction.atomic():
            modelos = get_presenca_models()
            presenca = modelos['Presenca'].objects.get(id=presenca_id)
            
            # Campos permitidos para atualização
            campos_permitidos = ['presente', 'justificativa', 'data', 'registrado_por']
            
            for campo in campos_permitidos:
                if campo in dados_atualizacao:
                    if campo == 'data':
                        nova_data = dados_atualizacao[campo]
                        if isinstance(nova_data, str):
                            nova_data = datetime.strptime(nova_data, '%Y-%m-%d').date()
                        elif isinstance(nova_data, datetime):
                            nova_data = nova_data.date()
                        
                        if nova_data > date.today():
                            raise ValidationError("A data da presença não pode ser futura.")
                        
                        setattr(presenca, campo, nova_data)
                    else:
                        setattr(presenca, campo, dados_atualizacao[campo])
            
            presenca.full_clean()
            presenca.save()
            
            logger.info(f"Presença atualizada: {presenca}")
            return presenca
            
    except modelos['Presenca'].DoesNotExist:
        raise ValidationError("Presença não encontrada.")
    except Exception as e:
        logger.error(f"Erro ao atualizar presença: {str(e)}")
        raise ValidationError(f"Erro ao atualizar presença: {str(e)}")

def excluir_presenca(presenca_id):
    """
    Exclui uma presença.
    
    Args:
        presenca_id (int): ID da presença
    """
    try:
        with transaction.atomic():
            modelos = get_presenca_models()
            presenca = modelos['Presenca'].objects.get(id=presenca_id)
            presenca.delete()
            
            logger.info(f"Presença excluída: ID {presenca_id}")
            return True
            
    except modelos['Presenca'].DoesNotExist:
        raise ValidationError("Presença não encontrada.")
    except Exception as e:
        logger.error(f"Erro ao excluir presença: {str(e)}")
        raise ValidationError(f"Erro ao excluir presença: {str(e)}")

def obter_presencas_por_aluno(aluno_cpf, data_inicio=None, data_fim=None):
    """Obtém presenças de um aluno específico."""
    modelos = get_presenca_models()
    presencas = modelos['Presenca'].objects.filter(
        aluno__cpf=aluno_cpf
    ).select_related('turma', 'atividade')
    
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)
    
    return presencas.order_by('-data')

def obter_presencas_por_turma(turma_id, data_inicio=None, data_fim=None):
    """Obtém presenças de uma turma específica."""
    modelos = get_presenca_models()
    presencas = modelos['Presenca'].objects.filter(
        turma_id=turma_id
    ).select_related('aluno', 'atividade')
    
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)
    
    return presencas.order_by('-data', 'aluno__nome')

def calcular_frequencia_aluno(aluno_cpf, turma_id=None, periodo_inicio=None, periodo_fim=None):
    """
    Calcula a frequência de um aluno.
    
    Args:
        aluno_cpf (str): CPF do aluno
        turma_id (int): ID da turma (opcional)
        periodo_inicio (date): Data início do período
        periodo_fim (date): Data fim do período
    
    Returns:
        dict: Estatísticas de frequência
    """
    modelos = get_presenca_models()
    
    # Filtrar presenças
    presencas = modelos['Presenca'].objects.filter(aluno__cpf=aluno_cpf)
    
    if turma_id:
        presencas = presencas.filter(turma_id=turma_id)
    
    if periodo_inicio:
        presencas = presencas.filter(data__gte=periodo_inicio)
    
    if periodo_fim:
        presencas = presencas.filter(data__lte=periodo_fim)
    
    total_registros = presencas.count()
    total_presencas = presencas.filter(presente=True).count()
    total_faltas = presencas.filter(presente=False).count()
    
    percentual_presenca = (total_presencas / total_registros * 100) if total_registros > 0 else 0
    
    return {
        'total_registros': total_registros,
        'total_presencas': total_presencas,
        'total_faltas': total_faltas,
        'percentual_presenca': round(percentual_presenca, 2)
    }

def criar_observacao_presenca(dados_observacao):
    """
    Cria uma observação de presença.
    
    Args:
        dados_observacao (dict): Dados da observação
    """
    try:
        with transaction.atomic():
            Aluno = get_aluno_model()
            Turma = get_turma_model()
            modelos = get_presenca_models()
            
            # Buscar relacionamentos
            aluno = None
            if dados_observacao.get('aluno_cpf'):
                aluno = Aluno.objects.get(cpf=dados_observacao['aluno_cpf'])
            
            turma = Turma.objects.get(id=dados_observacao['turma_id'])
            
            # Criar observação
            observacao = modelos['ObservacaoPresenca'].objects.create(
                aluno=aluno,
                turma=turma,
                data=dados_observacao.get('data', date.today()),
                texto=dados_observacao.get('texto', ''),
                registrado_por=dados_observacao.get('registrado_por', 'Sistema')
            )
            
            logger.info(f"Observação de presença criada: {observacao}")
            return observacao
            
    except Exception as e:
        logger.error(f"Erro ao criar observação: {str(e)}")
        raise ValidationError(f"Erro ao criar observação: {str(e)}")

def registrar_total_atividade_mes(turma_id, atividade_id, ano, mes, quantidade):
    """
    Registra o total de atividades em um mês.
    
    Args:
        turma_id (int): ID da turma
        atividade_id (int): ID da atividade
        ano (int): Ano
        mes (int): Mês
        quantidade (int): Quantidade de atividades
    """
    try:
        with transaction.atomic():
            Turma = get_turma_model()
            Atividade = get_atividade_model()
            modelos = get_presenca_models()
            
            turma = Turma.objects.get(id=turma_id)
            atividade = Atividade.objects.get(id=atividade_id)
            
            # Criar ou atualizar total
            total, created = modelos['TotalAtividadeMes'].objects.get_or_create(
                atividade=atividade,
                turma=turma,
                ano=ano,
                mes=mes,
                defaults={
                    'qtd_ativ_mes': quantidade,
                    'registrado_por': 'Sistema'
                }
            )
            
            if not created:
                total.qtd_ativ_mes = quantidade
                total.save()
            
            logger.info(f"Total atividade mês registrado: {total}")
            return total
            
    except Exception as e:
        logger.error(f"Erro ao registrar total atividade: {str(e)}")
        raise ValidationError(f"Erro ao registrar total atividade: {str(e)}")
