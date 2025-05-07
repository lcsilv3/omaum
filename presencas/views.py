from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from importlib import import_module
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
import csv
import logging
from datetime import datetime

# Configurar logger
logger = logging.getLogger(__name__)

def get_models():
    """Obtém os modelos necessários dinamicamente."""
    presencas_module = import_module("presencas.models")
    return getattr(presencas_module, "Presenca")

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

@login_required
def listar_presencas(request):
    """Lista todas as presenças registradas."""
    Presenca = get_models()
    
    # Obter parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    turma_id = request.GET.get('turma', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Iniciar queryset
    presencas = Presenca.objects.all().select_related('aluno', 'turma', 'atividade')
    
    # Aplicar filtros
    if aluno_id:
        presencas = presencas.filter(aluno__cpf=aluno_id)
    if turma_id:
        presencas = presencas.filter(turma__id=turma_id)
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)
    
    # Obter dados para os filtros
    Aluno = get_aluno_model()
    Turma = get_turma_model()
    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()
    
    context = {
        'presencas': presencas,
        'alunos': alunos,
        'turmas': turmas,
        'filtros': {
            'aluno': aluno_id,
            'turma': turma_id,
            'data_inicio': data_inicio,
            'data_fim': data_fim
        }
    }
    
    return render(request, 'presencas/listar_presencas.html', context)

@login_required
def registrar_presenca(request):
    """Registra uma nova presença."""
    Presenca = get_models()
    Aluno = get_aluno_model()
    Turma = get_turma_model()
    AtividadeAcademica = get_atividade_model()
    
    if request.method == 'POST':
        aluno_id = request.POST.get('aluno')
        turma_id = request.POST.get('turma')
        atividade_id = request.POST.get('atividade')
        data = request.POST.get('data')
        presente = request.POST.get('presente') == 'on'
        justificativa = request.POST.get('justificativa', '')
        
        try:
            aluno = Aluno.objects.get(cpf=aluno_id)
            turma = Turma.objects.get(id=turma_id)
            atividade = None
            if atividade_id:
                atividade = AtividadeAcademica.objects.get(id=atividade_id)
            
            # Verificar se já existe registro para este aluno/turma/data
            if Presenca.objects.filter(aluno=aluno, turma=turma, data=data).exists():
                messages.warning(request, f'Já existe um registro de presença para {aluno.nome} na turma {turma.nome} na data {data}.')
                return redirect('presencas:listar_presencas')
            
            presenca = Presenca(
                aluno=aluno,
                turma=turma,
                atividade=atividade,
                data=data,
                presente=presente,
                justificativa=justificativa if not presente else '',
                registrado_por=request.user.username,
                data_registro=timezone.now()
            )
            presenca.save()
            
            messages.success(request, f'Presença registrada com sucesso para {aluno.nome}.')
            return redirect('presencas:listar_presencas')
        
        except Exception as e:
            messages.error(request, f'Erro ao registrar presença: {str(e)}')
    
    # Para requisições GET, exibir o formulário
    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()
    atividades = AtividadeAcademica.objects.all()
    
    context = {
        'alunos': alunos,
        'turmas': turmas,
        'atividades': atividades,
        'data_hoje': timezone.now().date()
    }
    
    return render(request, 'presencas/registrar_presenca.html', context)

@login_required
def editar_presenca(request, presenca_id):
    """Edita um registro de presença existente."""
    Presenca = get_models()
    presenca = get_object_or_404(Presenca, id=presenca_id)
    
    if request.method == 'POST':
        presente = request.POST.get('presente') == 'on'
        justificativa = request.POST.get('justificativa', '')
        
        presenca.presente = presente
        presenca.justificativa = justificativa if not presente else ''
        presenca.registrado_por = request.user.username
        presenca.data_registro = timezone.now()
        
        try:
            presenca.save()
            messages.success(request, 'Registro de presença atualizado com sucesso.')
            return redirect('presencas:listar_presencas')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar presença: {str(e)}')
    
    context = {
        'presenca': presenca
    }
    
    return render(request, 'presencas/editar_presenca.html', context)

@login_required
def excluir_presenca(request, presenca_id):
    """Exclui um registro de presença."""
    Presenca = get_models()
    presenca = get_object_or_404(Presenca, id=presenca_id)
    
    if request.method == 'POST':
        try:
            presenca.delete()
            messages.success(request, 'Registro de presença excluído com sucesso.')
            return redirect('presencas:listar_presencas')
        except Exception as e:
            messages.error(request, f'Erro ao excluir presença: {str(e)}')
    
    context = {
        'presenca': presenca
    }
    
    return render(request, 'presencas/excluir_presenca.html', context)

@login_required
def detalhar_presenca(request, presenca_id):
    """Exibe os detalhes de um registro de presença."""
    Presenca = get_models()
    presenca = get_object_or_404(Presenca, id=presenca_id)
    
    context = {
        'presenca': presenca
    }
    
    return render(request, 'presencas/detalhar_presenca.html', context)

@login_required
def registrar_presenca_turma(request, turma_id):
    """Registra presença para todos os alunos de uma turma."""
    Presenca = get_models()
    Turma = get_turma_model()
    
    turma = get_object_or_404(Turma, id=turma_id)
    
    # Obter todos os alunos matriculados na turma
    try:
        Matricula = import_module("matriculas.models").Matricula
        matriculas = Matricula.objects.filter(turma=turma, status='A')
        alunos = [m.aluno for m in matriculas]
    except Exception as e:
        messages.error(request, f'Erro ao obter alunos da turma: {str(e)}')
        return redirect('turmas:detalhar_turma', turma_id=turma_id)
    
    if request.method == 'POST':
        data = request.POST.get('data')
        atividade_id = request.POST.get('atividade')
        
        try:
            atividade = None
            if atividade_id:
                AtividadeAcademica = get_atividade_model()
                atividade = AtividadeAcademica.objects.get(id=atividade_id)
            
            # Processar presenças para cada aluno
            for aluno in alunos:
                presente = request.POST.get(f'presente_{aluno.cpf}') == 'on'
                justificativa = request.POST.get(f'justificativa_{aluno.cpf}', '')
                
                # Verificar se já existe registro
                if Presenca.objects.filter(aluno=aluno, turma=turma, data=data).exists():
                    # Atualizar registro existente
                    presenca = Presenca.objects.get(aluno=aluno, turma=turma, data=data)
                    presenca.presente = presente
                    presenca.justificativa = justificativa if not presente else ''
                    presenca.atividade = atividade
                    presenca.registrado_por = request.user.username
                    presenca.data_registro = timezone.now()
                    presenca.save()
                else:
                    # Criar novo registro
                    Presenca.objects.create(
                        aluno=aluno,
                        turma=turma,
                        atividade=atividade,
                        data=data,
                        presente=presente,
                        justificativa=justificativa if not presente else '',
                        registrado_por=request.user.username,
                        data_registro=timezone.now()
                    )
            
            messages.success(request, f'Presenças registradas com sucesso para a turma {turma.nome}.')
            return redirect('turmas:detalhar_turma', turma_id=turma_id)
            
        except Exception as e:
            messages.error(request, f'Erro ao registrar presenças: {str(e)}')
    
    # Para requisições GET, exibir o formulário
    AtividadeAcademica = get_atividade_model()
    atividades = AtividadeAcademica.objects.filter(turmas=turma)
    
    context = {
        'turma': turma,
        'alunos': alunos,
        'atividades': atividades,
        'data_hoje': timezone.now().date()
    }
    
    return render(request, 'presencas/registrar_presenca_turma.html', context)

@login_required
def exportar_presencas(request):
    """Exporta os dados das presenças para um arquivo CSV."""
    try:
        import csv
        from django.http import HttpResponse
        
        Presenca = get_model("presencas", "Presenca")
        presencas = Presenca.objects.all().select_related('aluno', 'turma')
        
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="presencas.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "ID",
            "Aluno (CPF)",
            "Aluno (Nome)",
            "Turma",
            "Data",
            "Presente",
            "Justificativa"
        ])
        
        for presenca in presencas:
            writer.writerow([
                presenca.id,
                presenca.aluno.cpf,
                presenca.aluno.nome,
                presenca.turma.nome,
                presenca.data,
                "Sim" if presenca.presente else "Não",
                presenca.justificativa if not presenca.presente else ""
            ])
        
        return response
    except Exception as e:
        messages.error(request, f"Erro ao exportar presenças: {str(e)}")
        return redirect("presencas:listar_presencas")

@login_required
def importar_presencas(request):
    """Importa presenças de um arquivo CSV."""
    if request.method == "POST" and request.FILES.get("csv_file"):
        try:
            import csv
            from io import TextIOWrapper
            from django.utils import timezone
            
            Presenca = get_model("presencas", "Presenca")
            Aluno = get_model("alunos", "Aluno")
            Turma = get_model("turmas", "Turma")
            
            csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")
            reader = csv.DictReader(csv_file)
            count = 0
            errors = []
            
            for row in reader:
                try:
                    # Buscar aluno pelo CPF
                    aluno = None
                    aluno_cpf = row.get("Aluno (CPF)", "").strip()
                    if aluno_cpf:
                        try:
                            aluno = Aluno.objects.get(cpf=aluno_cpf)
                        except Aluno.DoesNotExist:
                            errors.append(f"Aluno não encontrado com CPF: {aluno_cpf}")
                            continue
                    else:
                        errors.append("CPF do aluno não especificado")
                        continue
                    
                    # Buscar turma pelo nome ou ID
                    turma = None
                    turma_nome = row.get("Turma", "").strip()
                    if turma_nome:
                        try:
                            turma = Turma.objects.get(nome=turma_nome)
                        except Turma.DoesNotExist:
                            try:
                                turma = Turma.objects.get(id=turma_nome)
                            except (Turma.DoesNotExist, ValueError):
                                errors.append(f"Turma não encontrada: {turma_nome}")
                                continue
                    else:
                        errors.append("Turma não especificada")
                        continue
                    
                    # Processar data
                    data = None
                    try:
                        if row.get("Data"):
                            data = timezone.datetime.strptime(
                                row.get("Data"), "%d/%m/%Y"
                            ).date()
                        else:
                            data = timezone.now().date()
                    except ValueError as e:
                        errors.append(f"Erro no formato de data: {str(e)}")
                        continue
                    
                    # Processar presença
                    presente = True
                    presente_texto = row.get("Presente", "").strip().lower()
                    if presente_texto in ["não", "nao", "n", "no", "false", "0"]:
                        presente = False
                    
                    # Verificar se já existe registro para este aluno/turma/data
                    if Presenca.objects.filter(aluno=aluno, turma=turma, data=data).exists():
                        errors.append(f"Já existe um registro de presença para o aluno {aluno.nome} na turma {turma.nome} na data {data}")
                        continue
                    
                    # Criar o registro de presença
                    Presenca.objects.create(
                        aluno=aluno,
                        turma=turma,
                        data=data,
                        presente=presente,
                        justificativa=row.get("Justificativa", "").strip() if not presente else ""
                    )
                    
                    count += 1
                except Exception as e:
                    errors.append(f"Erro na linha {count+1}: {str(e)}")
            
            if errors:
                messages.warning(
                    request,
                    f"{count} presenças importadas com {len(errors)} erros.",
                )
                for error in errors[:5]:  # Mostrar apenas os 5 primeiros erros
                    messages.error(request, error)
                if len(errors) > 5:
                    messages.error(
                        request, f"... e mais {len(errors) - 5} erros."
                    )
            else:
                messages.success(
                    request, f"{count} presenças importadas com sucesso!"
                )
            return redirect("presencas:listar_presencas")
        except Exception as e:
            messages.error(request, f"Erro ao importar presenças: {str(e)}")
    
    return render(request, "presencas/importar_presencas.html")

@login_required
def relatorio_presencas(request):
    """Exibe um relatório de presenças."""
    Presenca = get_models()
    
    # Obter parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    turma_id = request.GET.get('turma', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Iniciar queryset
    presencas = Presenca.objects.all().select_related('aluno', 'turma')
    
    # Aplicar filtros
    if aluno_id:
        presencas = presencas.filter(aluno__cpf=aluno_id)
    if turma_id:
        presencas = presencas.filter(turma__id=turma_id)
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)
    
    # Calcular estatísticas
    total = presencas.count()
    presentes = presencas.filter(presente=True).count()
    ausentes = total - presentes
    taxa_presenca = (presentes / total * 100) if total > 0 else 0
    
    # Obter dados para os filtros
    Aluno = get_aluno_model()
    Turma = get_turma_model()
    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()
    
    context = {
        'presencas': presencas,
        'alunos': alunos,
        'turmas': turmas,
        'filtros': {
            'aluno': aluno_id,
            'turma': turma_id,
            'data_inicio': data_inicio,
            'data_fim': data_fim
        },
        'estatisticas': {
            'total': total,
            'presentes': presentes,
            'ausentes': ausentes,
            'taxa_presenca': taxa_presenca
        }
    }
    
    return render(request, 'presencas/relatorio_presencas.html', context)

@login_required
def registrar_presenca_em_massa(request):
    """Registra presença em massa para uma turma."""
    Turma = get_turma_model()
    Presenca = get_models()
    Aluno = get_aluno_model()
    AtividadeAcademica = get_atividade_model()
    
    # Para requisições POST (quando o formulário é enviado)
    if request.method == "POST":
        turma_id = request.POST.get("turma")
        atividade_id = request.POST.get("atividade")
        data = request.POST.get("data")
        presentes = request.POST.getlist("presentes")
        
        if not turma_id or not atividade_id or not data:
            messages.error(request, "Por favor, preencha todos os campos obrigatórios.")
            return redirect("presencas:registrar_presenca_em_massa")
        
        try:
            turma = Turma.objects.get(id=turma_id)
            atividade = AtividadeAcademica.objects.get(id=atividade_id)
            data_obj = datetime.strptime(data, "%Y-%m-%d").date()
            
            # Obter todos os alunos da turma
            Matricula = import_module("matriculas.models").Matricula
            matriculas = Matricula.objects.filter(turma=turma, status="A")
            alunos = [m.aluno for m in matriculas]
            
            # Registrar presenças/ausências
            for aluno in alunos:
                presente = aluno.cpf in presentes
                justificativa = request.POST.get(f"justificativa_{aluno.cpf}", "") if not presente else ""
                
                # Verificar se já existe registro para este aluno/atividade/data
                presenca, created = Presenca.objects.update_or_create(
                    aluno=aluno,
                    atividade=atividade,
                    turma=turma,
                    data=data_obj,
                    defaults={
                        "presente": presente,
                        "justificativa": justificativa,
                        "registrado_por": request.user.username
                    }
                )
            
            messages.success(request, f"Presenças registradas com sucesso para {len(alunos)} alunos.")
            return redirect("presencas:listar_presencas")
            
        except Exception as e:
            messages.error(request, f"Erro ao registrar presenças: {str(e)}")
            return redirect("presencas:registrar_presenca_em_massa")
    
    # Para requisições GET (quando a página é carregada)
    turmas = Turma.objects.filter(status="A")
    data_hoje = timezone.now().date()
    
    return render(
        request, 
        "presencas/registrar_presenca_em_massa.html",
        {
            "turmas": turmas,
            "data_hoje": data_hoje
        }
    )

@login_required
def api_atividades_por_turma(request, turma_id):
    """API para obter atividades de uma turma."""
    try:
        Turma = get_turma_model()
        AtividadeAcademica = get_atividade_model()
        
        turma = Turma.objects.get(id=turma_id)
        atividades = AtividadeAcademica.objects.filter(turmas=turma)
        
        return JsonResponse({
            "success": True,
            "atividades": [
                {
                    "id": atividade.id,
                    "nome": atividade.nome
                }
                for atividade in atividades
            ]
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

@login_required
def api_alunos_por_turma(request, turma_id):
    """API para obter alunos de uma turma."""
    try:
        Turma = get_turma_model()
        
        turma = Turma.objects.get(id=turma_id)
        Matricula = import_module("matriculas.models").Matricula
        matriculas = Matricula.objects.filter(turma=turma, status="A")
        
        return JsonResponse({
            "success": True,
            "alunos": [
                {
                    "cpf": m.aluno.cpf,
                    "nome": m.aluno.nome,
                    "foto": m.aluno.foto.url if m.aluno.foto else None
                }
                for m in matriculas
            ]
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)