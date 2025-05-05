from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.db import transaction
import json
import logging
from importlib import import_module

logger = logging.getLogger(__name__)

def get_models():
    """Obtém o modelo Presenca."""
    presencas_module = import_module("presencas.models")
    return getattr(presencas_module, "Presenca")

def get_aluno_model():
    """Obtém o modelo Aluno."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

def get_atividade_model():
    """Obtém o modelo Atividade."""
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "Atividade")

def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

def get_matricula_model():
    """Obtém o modelo Matricula."""
    matriculas_module = import_module("matriculas.models")
    return getattr(matriculas_module, "Matricula")

@login_required
@require_POST
def obter_alunos_por_turmas(request):
    """API para obter alunos de turmas específicas."""
    try:
        # Obter dados do corpo da requisição
        data = json.loads(request.body)
        turmas_ids = data.get('turmas_ids', [])
        
        if not turmas_ids:
            return JsonResponse({'error': 'Nenhuma turma selecionada.'}, status=400)
        
        # Obter turmas
        Turma = get_turma_model()
        turmas = Turma.objects.filter(id__in=turmas_ids)
        
        if not turmas.exists():
            return JsonResponse({'error': 'Nenhuma turma encontrada com os IDs fornecidos.'}, status=404)
        
        # Obter matrículas ativas nas turmas
        Matricula = get_matricula_model()
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
        Atividade = get_atividade_model()
        atividades = Atividade.objects.all()
        
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
        logger.error(f"Erro ao obter alunos por turmas: {str(e)}", exc_info=True)
        return JsonResponse({'error': f"Erro ao obter alunos: {str(e)}"}, status=500)

@login_required
@require_GET
def obter_atividades_por_data(request):
    """API para obter atividades disponíveis em uma data específica."""
    try:
        data = request.GET.get('data')
        
        if not data:
            return JsonResponse({'error': 'Data não fornecida.'}, status=400)
        
        # Obter atividades para a data
        Atividade = get_atividade_model()
        atividades = Atividade.objects.filter(data_inicio__date=data)
        
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
        logger.error(f"Erro ao obter atividades por data: {str(e)}", exc_info=True)
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
        
        # Obter modelos
        Presenca = get_models()
        Aluno = get_aluno_model()
        Atividade = get_atividade_model()
        
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
                    atividade = Atividade.objects.get(id=atividade_id)
                except (Aluno.DoesNotExist, Atividade.DoesNotExist):
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
        logger.error(f"Erro ao salvar presenças múltiplas: {str(e)}", exc_info=True)
        return JsonResponse({'error': f"Erro ao salvar presenças: {str(e)}"}, status=500)