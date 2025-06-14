from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from importlib import import_module
import json

def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)

@login_required
def registrar_presencas_multiplas(request):
    """Registra presenças para múltiplos alunos em múltiplas atividades."""
    if request.method == 'POST':
        # Processar o formulário
        data = request.POST.get('data')
        turma_ids = request.POST.getlist('turmas')
        atividade_ids = request.POST.getlist('atividades')
        
        if not data or not turma_ids or not atividade_ids:
            messages.error(request, "Data, turmas e atividades são obrigatórios.")
            return redirect('presencas:registrar_presencas_multiplas')
        
        # Redirecionar para a página de registro com os parâmetros
        return redirect('presencas:formulario_presencas_multiplas', 
                       data=data, 
                       turmas=','.join(turma_ids), 
                       atividades=','.join(atividade_ids))
    else:
        # Exibir o formulário inicial
        Turma = get_model_dynamically("turmas", "Turma")
        AtividadeAcademica = get_model_dynamically("atividades", "AtividadeAcademica")
        
        turmas = Turma.objects.filter(status='A')
        atividades = AtividadeAcademica.objects.all().order_by('-data_inicio')
        
        context = {
            'turmas': turmas,
            'atividades': atividades,
            'data_hoje': timezone.now().date().strftime('%Y-%m-%d')
        }
        
        return render(request, 'presencas/formulario_presencas_multiplas_passo1.html', context)

@login_required
def formulario_presencas_multiplas(request, data, turmas, atividades):
    """Exibe o formulário para registro de presenças múltiplas."""
    # Converter parâmetros
    turma_ids = turmas.split(',')
    atividade_ids = atividades.split(',')
    
    Turma = get_model_dynamically("turmas", "Turma")
    AtividadeAcademica = get_model_dynamically("atividades", "AtividadeAcademica")
    Aluno = get_model_dynamically("alunos", "Aluno")
    
    # Obter objetos
    turmas_obj = Turma.objects.filter(id__in=turma_ids)
    atividades_obj = AtividadeAcademica.objects.filter(id__in=atividade_ids)
    
    # Obter alunos das turmas
    alunos = []
    for turma in turmas_obj:
        # Obter alunos matriculados na turma
        Matricula = get_model_dynamically("matriculas", "Matricula")
        matriculas = Matricula.objects.filter(turma=turma, status='A')
        alunos.extend([m.aluno for m in matriculas])
    
    # Remover duplicatas
    alunos = list(set(alunos))
    
    if request.method == 'POST':
        # Processar o formulário
        Presenca = get_model_dynamically("presencas", "Presenca")
        presencas_data = json.loads(request.POST.get('presencas_data', '[]'))
        
        for presenca_info in presencas_data:
            aluno_id = presenca_info.get('aluno_id')
            atividade_id = presenca_info.get('atividade_id')
            presente = presenca_info.get('presente', True)
            justificativa = presenca_info.get('justificativa', '')
            
            aluno = get_object_or_404(Aluno, cpf=aluno_id)
            atividade = get_object_or_404(AtividadeAcademica, id=atividade_id)
            
            # Verificar se já existe registro
            presenca, created = Presenca.objects.update_or_create(
                aluno=aluno,
                atividade=atividade,
                data=data,
                defaults={
                    'presente': presente,
                    'justificativa': justificativa,
                    'registrado_por': request.user
                }
            )
        
        messages.success(request, "Presenças registradas com sucesso!")
        return redirect('presencas:listar_presencas')
    else:
        context = {
            'data': data,
            'turmas': turmas_obj,
            'atividades': atividades_obj,
            'alunos': alunos
        }
        
        return render(request, 'presencas/formulario_presencas_multiplas.html', context)