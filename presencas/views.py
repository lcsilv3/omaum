from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
import csv
import logging
from importlib import import_module
from datetime import datetime

logger = logging.getLogger(__name__)

def get_models():
    """Obtém o modelo Presenca."""
    presencas_module = import_module("presencas.models")
    return getattr(presencas_module, "Presenca")

def get_forms():
    """Obtém os formulários relacionados a presenças."""
    presencas_forms = import_module("presencas.forms")
    return (
        getattr(presencas_forms, "PresencaForm"),
        getattr(presencas_forms, "PresencaMultiplaForm"),
        getattr(presencas_forms, "FiltroPresencaForm")
    )

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

def obter_alunos_para_registro_presenca(atividade_id, data=None):
    """
    Função auxiliar para obter alunos para registro de presença.
    Retorna uma lista de alunos com informações de presença existente, se houver.
    """
    try:
        # Obter modelos dinamicamente
        AtividadeAcademica = get_model_dynamically("atividades", "AtividadeAcademica")
        Matricula = get_model_dynamically("matriculas", "Matricula")
        Presenca = get_model_dynamically("presencas", "Presenca")
        
        # Obter a atividade
        atividade = get_object_or_404(AtividadeAcademica, id=atividade_id)
        
        # Obter alunos matriculados nas turmas da atividade
        matriculas = Matricula.objects.filter(
            turma__in=atividade.turmas.all(),
            status='A'
        ).select_related('aluno')
        
        alunos = []
        for matricula in matriculas:
            aluno = matricula.aluno
            
            # Verificar se já existe registro de presença para este aluno/atividade/data
            presenca = None
            if data:
                presenca = Presenca.objects.filter(
                    aluno=aluno,
                    atividade=atividade,
                    data=data
                ).first()
            
            # Adicionar informações do aluno e da presença (se existir)
            aluno_info = {
                'cpf': aluno.cpf,
                'nome': aluno.nome,
                'foto': aluno.foto.url if hasattr(aluno, 'foto') and aluno.foto else None,
                'presenca': presenca
            }
            
            alunos.append(aluno_info)
        
        # Ordenar por nome
        alunos.sort(key=lambda x: x['nome'])
        
        return alunos
    except Exception as e:
        logger.error(f"Erro ao obter alunos para registro de presença: {str(e)}", exc_info=True)
        return []

@login_required
def listar_presencas(request):
    """Lista todas as presenças com suporte a filtros avançados."""
    try:
        # Obter modelos dinamicamente
        Presenca = get_model_dynamically("presencas", "Presenca")
        Aluno = get_model_dynamically("alunos", "Aluno")
        Turma = get_model_dynamically("turmas", "Turma")
        AtividadeAcademica = get_model_dynamically("atividades", "AtividadeAcademica")
        
        # Obter parâmetros de filtro
        aluno_id = request.GET.get('aluno')
        turma_id = request.GET.get('turma')
        atividade_id = request.GET.get('atividade')
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        status = request.GET.get('status')
        ordenar = request.GET.get('ordenar', 'data')
        
        # Construir query base
        presencas = Presenca.objects.all().select_related('aluno', 'atividade')
        
        # Aplicar filtros
        if aluno_id:
            presencas = presencas.filter(aluno__cpf=aluno_id)
        
        if turma_id:
            presencas = presencas.filter(atividade__turmas__id=turma_id)
        
        if atividade_id:
            presencas = presencas.filter(atividade__id=atividade_id)
        
        if data_inicio:
            presencas = presencas.filter(data__gte=data_inicio)
        
        if data_fim:
            presencas = presencas.filter(data__lte=data_fim)
        
        if status:
            if status == 'presente':
                presencas = presencas.filter(presente=True)
            elif status == 'ausente':
                presencas = presencas.filter(presente=False)
        
        # Aplicar ordenação
        if ordenar == 'data':
            presencas = presencas.order_by('-data')
        elif ordenar == 'data_asc':
            presencas = presencas.order_by('data')
        elif ordenar == 'aluno':
            presencas = presencas.order_by('aluno__nome')
        elif ordenar == 'atividade':
            presencas = presencas.order_by('atividade__nome')
        
        # Paginação
        paginator = Paginator(presencas, 20)  # 20 itens por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Obter dados para filtros
        alunos = Aluno.objects.all().order_by('nome')
        turmas = Turma.objects.filter(status='A').order_by('nome')
        atividades = AtividadeAcademica.objects.all().order_by('-data_inicio')
        
        # Calcular estatísticas
        total = presencas.count()
        presentes = presencas.filter(presente=True).count()
        ausentes = presencas.filter(presente=False).count()
        
        # Calcular taxa de presença
        taxa_presenca = (presentes / total * 100) if total > 0 else 0
        
        context = {
            'presencas': page_obj,
            'page_obj': page_obj,
            'alunos': alunos,
            'turmas': turmas,
            'atividades': atividades,
            'total': total,
            'presentes': presentes,
            'ausentes': ausentes,
            'taxa_presenca': taxa_presenca,
            'filtros': {
                'aluno': aluno_id,
                'turma': turma_id,
                'atividade': atividade_id,
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'status': status,
                'ordenar': ordenar,
            }
        }
        
        return render(request, 'presencas/listar_presencas.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao listar presenças: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao listar presenças: {str(e)}")
        return render(request, 'presencas/listar_presencas.html', {'presencas': []})

@login_required
def registrar_presenca(request):
    """Registra a presença de um aluno em uma atividade."""
    try:
        # Importar modelos dinamicamente
        Aluno = get_model_dynamically("alunos", "Aluno")
        Atividade = get_model_dynamically("atividades", "AtividadeAcademica")
        Presenca = get_model_dynamically("presencas", "Presenca")
        
        if request.method == "POST":
            aluno_id = request.POST.get("aluno")
            atividade_id = request.POST.get("atividade")
            data = request.POST.get("data")
            presente = request.POST.get("presente") == "on"
            justificativa = request.POST.get("justificativa", "")
            
            # Validar dados
            if not aluno_id or not atividade_id or not data:
                messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
                return redirect('presencas:registrar_presenca')
            
            # Obter objetos
            aluno = get_object_or_404(Aluno, cpf=aluno_id)
            atividade = get_object_or_404(Atividade, id=atividade_id)
            
            # Verificar se já existe registro para este aluno/atividade/data
            presenca_existente = Presenca.objects.filter(
                aluno=aluno,
                atividade=atividade,
                data=data
            ).first()
            
            if presenca_existente:
                # Atualizar registro existente
                presenca_existente.presente = presente
                presenca_existente.justificativa = justificativa if not presente else ""
                presenca_existente.save()
                messages.success(request, "Registro de presença atualizado com sucesso!")
            else:
                # Criar novo registro
                Presenca.objects.create(
                    aluno=aluno,
                    atividade=atividade,
                    data=data,
                    presente=presente,
                    justificativa=justificativa if not presente else ""
                )
                messages.success(request, "Presença registrada com sucesso!")
            
            return redirect('presencas:listar_presencas')
        
        # Para o método GET, exibir o formulário
        alunos = Aluno.objects.filter(situacao="ATIVO").order_by('nome')
        atividades = Atividade.objects.filter(status__in=['agendada', 'em_andamento']).order_by('-data_inicio')
        
        context = {
            'alunos': alunos,
            'atividades': atividades,
            'data_hoje': timezone.now().date().isoformat()
        }
        
        return render(request, 'presencas/registrar_presenca.html', context)
    
    except ValidationError as e:
        messages.error(request, f"Erro de validação: {e}")
        return redirect('presencas:listar_presencas')
    except Exception as e:
        logger.error(f"Erro ao registrar presença: {str(e)}", exc_info=True)
        messages.error(request, "Ocorreu um erro ao registrar a presença. Por favor, tente novamente.")
        return redirect('presencas:listar_presencas')

@login_required
def editar_presenca(request, presenca_id):
    """Edita uma presença existente."""
    try:
        Presenca = get_models()
        PresencaForm, _, _ = get_forms()
        
        presenca = get_object_or_404(Presenca, id=presenca_id)
        
        if request.method == 'POST':
            form = PresencaForm(request.POST, instance=presenca)
            if form.is_valid():
                form.save()
                messages.success(request, "Presença atualizada com sucesso!")
                return redirect('presencas:listar_presencas')
        else:
            form = PresencaForm(instance=presenca)
        
        context = {
            'form': form,
            'presenca': presenca,
            'titulo': 'Editar Presença'
        }
        
        return render(request, 'presencas/formulario_presenca.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao editar presença: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao editar presença: {str(e)}")
        return redirect('presencas:listar_presencas')

@login_required
def excluir_presenca(request, presenca_id):
    """Exclui uma presença."""
    try:
        Presenca = get_models()
        presenca = get_object_or_404(Presenca, id=presenca_id)
        
        if request.method == 'POST':
            presenca.delete()
            messages.success(request, "Presença excluída com sucesso!")
            return redirect('presencas:listar_presencas')
        
        context = {
            'presenca': presenca
        }
        
        return render(request, 'presencas/excluir_presenca.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao excluir presença: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao excluir presença: {str(e)}")
        return redirect('presencas:listar_presencas')

@login_required
def registrar_presencas_multiplas(request):
    """Registra múltiplas presenças de uma vez."""
    try:
        _, PresencaMultiplaForm, _ = get_forms()
        
        if request.method == 'POST':
            form = PresencaMultiplaForm(request.POST)
            if form.is_valid():
                # Os dados serão processados via API JavaScript
                messages.success(request, "Formulário válido. Prossiga com o registro de presenças.")
                
                # Redirecionar para a página de seleção de alunos
                return redirect('presencas:selecionar_alunos_presencas', 
                               data=form.cleaned_data['data'].strftime('%Y-%m-%d'),
                               turmas=','.join(str(t.id) for t in form.cleaned_data['turmas']),
                               atividades=','.join(str(a.id) for a in form.cleaned_data['atividades']))
        else:
            form = PresencaMultiplaForm()
        
        # Obter turmas ativas
        Turma = get_turma_model()
        turmas = Turma.objects.filter(status='A')
        
        # Obter atividades
        Atividade = get_atividade_model()
        atividades = Atividade.objects.all()
        
        context = {
            'form': form,
            'turmas': turmas,
            'atividades': atividades
        }
        
        return render(request, 'presencas/formulario_presencas_multiplas_passo1.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao registrar presenças múltiplas: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao registrar presenças múltiplas: {str(e)}")
        return redirect('presencas:listar_presencas')

@login_required
def selecionar_alunos_presencas(request, data, turmas, atividades):
    """Seleciona alunos para registro de presenças múltiplas."""
    try:
        # Converter parâmetros
        data_obj = datetime.strptime(data, '%Y-%m-%d').date()
        turmas_ids = [int(id) for id in turmas.split(',')]
        atividades_ids = [int(id) for id in atividades.split(',')]
        
        # Obter turmas
        Turma = get_turma_model()
        turmas_objs = Turma.objects.filter(id__in=turmas_ids)
        
        # Obter atividades
        Atividade = get_atividade_model()
        atividades_objs = Atividade.objects.filter(id__in=atividades_ids)
        
        # Obter alunos matriculados nas turmas
        Matricula = import_module("matriculas.models").Matricula
        matriculas = Matricula.objects.filter(turma__in=turmas_objs, status='A').select_related('aluno')
        
        # Obter alunos únicos
        alunos = []
        alunos_ids = set()
        
        for matricula in matriculas:
            if matricula.aluno.cpf not in alunos_ids:
                alunos.append(matricula.aluno)
                alunos_ids.add(matricula.aluno.cpf)
        
        # Verificar presenças existentes
        Presenca = get_models()
        presencas_existentes = Presenca.objects.filter(
            aluno__in=alunos,
            atividade__in=atividades_objs,
            data=data_obj
        )
        
        # Criar dicionário de presenças existentes para fácil acesso
        presencas_dict = {}
        for presenca in presencas_existentes:
            key = f"{presenca.aluno.cpf}_{presenca.atividade.id}"
            presencas_dict[key] = presenca
        
        context = {
            'data': data,
            'data_formatada': data_obj.strftime('%d/%m/%Y'),
            'turmas': turmas_objs,
            'atividades': atividades_objs,
            'alunos': alunos,
            'presencas_dict': presencas_dict
        }
        
        return render(request, 'presencas/formulario_presencas_multiplas_passo2.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao selecionar alunos para presenças: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao selecionar alunos: {str(e)}")
        return redirect('presencas:registrar_presencas_multiplas')

@login_required
def registrar_presencas_multiplas_form(request):
    """Formulário para registrar presenças múltiplas."""
    try:
        # Obter parâmetros da URL
        data_str = request.GET.get('data')
        turmas_ids = request.GET.get('turmas', '').split(',')
        atividades_ids = request.GET.get('atividades', '').split(',')
        
        if not data_str or not turmas_ids or not atividades_ids:
            messages.error(request, "Parâmetros inválidos. Por favor, tente novamente.")
            return redirect('presencas:registrar_presencas_multiplas')
        
        # Converter para data
        try:
            data = timezone.datetime.strptime(data_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Formato de data inválido.")
            return redirect('presencas:registrar_presencas_multiplas')
        
        # Obter modelos
        Turma = get_turma_model()
        Atividade = get_atividade_model()
        
        # Obter turmas e atividades
        turmas = Turma.objects.filter(id__in=turmas_ids)
        atividades = Atividade.objects.filter(id__in=atividades_ids)
        
        if not turmas or not atividades:
            messages.error(request, "Turmas ou atividades não encontradas.")
            return redirect('presencas:registrar_presencas_multiplas')
        
        context = {
            'data': data,
            'turmas': turmas,
            'atividades': atividades,
        }
        
        return render(request, 'presencas/formulario_presencas_multiplas.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao exibir formulário múltiplo: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao exibir formulário múltiplo: {str(e)}")
        return redirect('presencas:registrar_presencas_multiplas')

@login_required
def exportar_presencas_csv(request):
    """Exporta presenças para um arquivo CSV."""
    try:
        Presenca = get_models()
        _, _, FiltroPresencaForm = get_forms()
        
        # Aplicar filtros
        filtro_form = FiltroPresencaForm(request.GET)
        presencas = Presenca.objects.all().select_related('aluno', 'atividade')
        
        if filtro_form.is_valid():
            # Aplicar os mesmos filtros da listagem
            aluno = filtro_form.cleaned_data.get('aluno')
            if aluno:
                presencas = presencas.filter(aluno=aluno)
            
            atividade = filtro_form.cleaned_data.get('atividade')
            if atividade:
                presencas = presencas.filter(atividade=atividade)
            
            data_inicio = filtro_form.cleaned_data.get('data_inicio')
            if data_inicio:
                presencas = presencas.filter(data__gte=data_inicio)
            
            data_fim = filtro_form.cleaned_data.get('data_fim')
            if data_fim:
                presencas = presencas.filter(data__lte=data_fim)
            
            situacao = filtro_form.cleaned_data.get('situacao')
            if situacao:
                presencas = presencas.filter(situacao=situacao)
        
        # Ordenar
        presencas = presencas.order_by('-data', 'aluno__nome')
        
        # Criar resposta CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="presencas.csv"'
        
        # Escrever cabeçalho e dados
        writer = csv.writer(response)
        writer.writerow(['CPF', 'Aluno', 'Atividade', 'Data', 'Situação', 'Justificativa'])
        
        for presenca in presencas:
            writer.writerow([
                presenca.aluno.cpf,
                presenca.aluno.nome,
                presenca.atividade.titulo,
                presenca.data.strftime('%d/%m/%Y'),
                dict(Presenca.SITUACAO_CHOICES).get(presenca.situacao, presenca.situacao),
                presenca.justificativa or ''
            ])
        
        return response
    
    except Exception as e:
        logger.error(f"Erro ao exportar presenças: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao exportar presenças: {str(e)}")
        return redirect('presencas:listar_presencas')

@login_required
def detalhar_presenca(request, presenca_id):
    """
    Exibe os detalhes de um registro de presença.
    """
    Presenca = get_presenca_model()
    presenca = get_object_or_404(Presenca, id=presenca_id)
    
    return render(request, 'presencas/detalhar_presenca.html', {'presenca': presenca})

@login_required
def registrar_presenca_multipla(request):
    """Registra presença para múltiplos alunos de uma vez."""
    try:
        # Obter modelos dinamicamente
        AtividadeAcademica = get_model_dynamically("atividades", "AtividadeAcademica")
        Turma = get_model_dynamically("turmas", "Turma")
        Presenca = get_model_dynamically("presencas", "Presenca")
        
        if request.method == "POST":
            atividade_id = request.POST.get('atividade')
            data = request.POST.get('data')
            presentes = request.POST.getlist('presentes')
            justificativas = {}
            
            # Coletar justificativas para alunos ausentes
            for key, value in request.POST.items():
                if key.startswith('justificativa_'):
                    aluno_id = key.replace('justificativa_', '')
                    justificativas[aluno_id] = value
            
            if not atividade_id or not data:
                messages.error(request, "Atividade e data são obrigatórios.")
                return redirect('presencas:registrar_presenca_multipla')
            
            atividade = get_object_or_404(AtividadeAcademica, id=atividade_id)
            
            # Obter alunos para registro
            alunos = obter_alunos_para_registro_presenca(atividade_id, data)
            
            # Registrar presença para cada aluno
            registros_criados = 0
            registros_atualizados = 0
            
            for aluno_info in alunos:
                aluno_cpf = aluno_info['cpf']
                presente = aluno_cpf in presentes
                justificativa = justificativas.get(aluno_cpf, '')
                
                # Verificar se já existe registro para este aluno/atividade/data
                presenca_existente = aluno_info.get('presenca')
                
                if presenca_existente:
                    # Atualizar registro existente
                    presenca_existente.presente = presente
                    presenca_existente.justificativa = justificativa if not presente else ""
                    presenca_existente.registrado_por = request.user
                    presenca_existente.save()
                    registros_atualizados += 1
                else:
                    # Criar novo registro
                    Aluno = get_model_dynamically("alunos", "Aluno")
                    aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
                    
                    Presenca.objects.create(
                        aluno=aluno,
                        atividade=atividade,
                        data=data,
                        presente=presente,
                        justificativa=justificativa if not presente else "",
                        registrado_por=request.user
                    )
                    registros_criados += 1
            
            messages.success(
                request, 
                f"Registro em massa concluído! {registros_criados} novos registros criados e {registros_atualizados} atualizados."
            )
            return redirect('presencas:listar_presencas')
        
        # Para o método GET, exibir o formulário
        atividade_id = request.GET.get('atividade')
        data = request.GET.get('data', timezone.now().date().isoformat())
        
        # Obter alunos se atividade foi especificada
        alunos = []
        if atividade_id:
            alunos = obter_alunos_para_registro_presenca(atividade_id, data)
        
        atividades = AtividadeAcademica.objects.filter(
            status__in=['agendada', 'em_andamento']
        ).order_by('-data_inicio')
        
        turmas = Turma.objects.filter(status='A').order_by('nome')
        
        context = {
            'atividades': atividades,
            'turmas': turmas,
            'alunos': alunos,
            'data_hoje': data
        }
        
        return render(request, 'presencas/registrar_presenca_multipla.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao registrar presença múltipla: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao registrar presenças: {str(e)}")
        return redirect('presencas:listar_presencas')

@login_required
def obter_alunos_por_turmas(request):
    """
    API para obter alunos das turmas selecionadas.
    """
    if request.method == 'GET':
        turmas_ids = request.GET.getlist('turmas[]')
        data = request.GET.get('data')
        atividades_ids = request.GET.getlist('atividades[]')
        
        if not turmas_ids:
            return JsonResponse({'error': 'Nenhuma turma selecionada'}, status=400)
        
        # Obter alunos das turmas selecionadas
        Aluno = get_aluno_model()
        Turma = get_turma_model()
        Presenca = get_presenca_model()
        
        try:
            turmas = Turma.objects.filter(id__in=turmas_ids)
            alunos = Aluno.objects.filter(turmas__in=turmas).distinct()
            
            # Formatar dados dos alunos
            alunos_data = []
            for aluno in alunos:
                # Verificar se já existem registros de presença para este aluno nas atividades selecionadas
                situacoes = {}
                justificativas = {}
                
                if data and atividades_ids:
                    for atividade_id in atividades_ids:
                        try:
                            presenca = Presenca.objects.get(
                                aluno=aluno,
                                atividade_id=atividade_id,
                                data=data
                            )
                            situacoes[atividade_id] = presenca.situacao
                            justificativas[atividade_id] = presenca.justificativa or ''
                        except Presenca.DoesNotExist:
                            situacoes[atividade_id] = 'PRESENTE'  # Padrão
                            justificativas[atividade_id] = ''
                
                alunos_data.append({
                    'id': aluno.cpf,
                    'nome': aluno.nome,
                    'numero_iniciatico': aluno.numero_iniciatico or 'N/A',
                    'turmas': [t.nome for t in aluno.turmas.all()],
                    'situacoes': situacoes,
                    'justificativas': justificativas,
                })
            
            return JsonResponse({'alunos': alunos_data})
        except Exception as e:
            logger.error(f"Erro ao obter alunos por turmas: {str(e)}")
            return JsonResponse({'error': f"Erro ao obter alunos: {str(e)}"}, status=500)
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@login_required
def obter_atividades_por_data(request):
    """
    API para obter atividades disponíveis para uma data específica.
    """
    if request.method == 'GET':
        data = request.GET.get('data')
        
        if not data:
            return JsonResponse({'error': 'Data não fornecida'}, status=400)
        
        try:
            data_obj = timezone.datetime.strptime(data, '%Y-%m-%d').date()
            
            # Obter atividades para a data
            Atividade = get_atividade_model()
            atividades = Atividade.objects.filter(data=data_obj)
            
            # Formatar dados das atividades
            atividades_data = []
            for atividade in atividades:
                atividades_data.append({
                    'id': atividade.id,
                    'titulo': atividade.titulo,
                    'tipo': atividade.get_tipo_display() if hasattr(atividade, 'get_tipo_display') else 'Não especificado',
                    'turmas': [t.nome for t in atividade.turmas.all()] if hasattr(atividade, 'turmas') else [],
                })
            
            return JsonResponse({'atividades': atividades_data})
        except Exception as e:
            logger.error(f"Erro ao obter atividades por data: {str(e)}")
            return JsonResponse({'error': f"Erro ao obter atividades: {str(e)}"}, status=500)
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@login_required
def registrar_presenca_em_massa(request):
    """Registra presença para múltiplos alunos de uma vez."""
    try:
        Atividade = get_model_dynamically("atividades", "AtividadeAcademica")
        Turma = get_model_dynamically("turmas", "Turma")
        Matricula = get_model_dynamically("matriculas", "Matricula")
        Presenca = get_model_dynamically("presencas", "Presenca")
        
        if request.method == "POST":
            atividade_id = request.POST.get('atividade')
            data = request.POST.get('data')
            presentes = request.POST.getlist('presentes')
            justificativas = {}
            
            # Coletar justificativas para alunos ausentes
            for key, value in request.POST.items():
                if key.startswith('justificativa_'):
                    aluno_id = key.replace('justificativa_', '')
                    justificativas[aluno_id] = value
            
            if not atividade_id or not data:
                messages.error(request, "Atividade e data são obrigatórios.")
                return redirect('presencas:registrar_presenca_em_massa')
            
            atividade = get_object_or_404(Atividade, id=atividade_id)
            
            # Obter todos os alunos matriculados nas turmas da atividade
            matriculas = Matricula.objects.filter(turma__in=atividade.turmas.all(), status='A')
            
            # Registrar presença para cada aluno
            registros_criados = 0
            registros_atualizados = 0
            
            for matricula in matriculas:
                aluno = matricula.aluno
                presente = aluno.cpf in presentes
                justificativa = justificativas.get(aluno.cpf, '')
                
                # Verificar se já existe registro para este aluno/atividade/data
                presenca_existente = Presenca.objects.filter(
                    aluno=aluno,
                    atividade=atividade,
                    data=data
                ).first()
                
                if presenca_existente:
                    # Atualizar registro existente
                    presenca_existente.presente = presente
                    presenca_existente.justificativa = justificativa if not presente else ""
                    presenca_existente.registrado_por = request.user
                    presenca_existente.save()
                    registros_atualizados += 1
                else:
                    # Criar novo registro
                    Presenca.objects.create(
                        aluno=aluno,
                        atividade=atividade,
                        data=data,
                        presente=presente,
                        justificativa=justificativa if not presente else "",
                        registrado_por=request.user
                    )
                    registros_criados += 1
            
            messages.success(
                request, 
                f"Registro em massa concluído! {registros_criados} novos registros criados e {registros_atualizados} atualizados."
            )
            return redirect('presencas:listar_presencas')
        
        # Para o método GET, exibir o formulário
        atividades = Atividade.objects.filter(status__in=['agendada', 'em_andamento']).order_by('-data_inicio')
        turmas = Turma.objects.filter(status='A').order_by('nome')
        
        context = {
            'atividades': atividades,
            'turmas': turmas,
            'data_hoje': timezone.now().date().isoformat()
        }
        
        return render(request, 'presencas/registrar_presenca_em_massa.html', context)
    
    except ValidationError as e:
        messages.error(request, f"Erro de validação: {e}")
        return redirect('presencas:listar_presencas')
    except Exception as e:
        logger.error(f"Erro ao registrar presença em massa: {str(e)}", exc_info=True)
        messages.error(request, "Ocorreu um erro ao registrar as presenças. Por favor, tente novamente.")
        return redirect('presencas:listar_presencas')

@login_required
def api_atividades_por_turma(request, turma_id):
    """API para obter atividades de uma turma específica."""
    try:
        # Obter modelos dinamicamente
        Turma = get_model_dynamically("turmas", "Turma")
        AtividadeAcademica = get_model_dynamically("atividades", "AtividadeAcademica")
        
        # Obter a turma
        turma = get_object_or_404(Turma, id=turma_id)
        
        # Obter atividades da turma
        atividades = AtividadeAcademica.objects.filter(
            turmas=turma,
            status__in=['agendada', 'em_andamento']
        ).order_by('-data_inicio')
        
        # Formatar dados para retorno
        atividades_data = []
        for atividade in atividades:
            atividades_data.append({
                'id': atividade.id,
                'nome': atividade.nome,
                'data': atividade.data_inicio.strftime('%d/%m/%Y'),
                'status': atividade.get_status_display()
            })
        
        return JsonResponse({
            'success': True,
            'atividades': atividades_data
        })
    except Exception as e:
        logger.error(f"Erro ao obter atividades por turma: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def relatorio_presencas(request):
    """Gera um relatório detalhado de presenças."""
    try:
        # Obter modelos dinamicamente
        Presenca = get_model_dynamically("presencas", "Presenca")
        Aluno = get_model_dynamically("alunos", "Aluno")
        Turma = get_model_dynamically("turmas", "Turma")
        
        # Obter parâmetros de filtro
        aluno_id = request.GET.get('aluno')
        turma_id = request.GET.get('turma')
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        
        # Construir query base
        presencas = Presenca.objects.all().select_related('aluno', 'atividade')
        
        # Aplicar filtros
        if aluno_id:
            presencas = presencas.filter(aluno__cpf=aluno_id)
        
        if turma_id:
            presencas = presencas.filter(atividade__turmas__id=turma_id)
        
        if data_inicio:
            presencas = presencas.filter(data__gte=data_inicio)
        
        if data_fim:
            presencas = presencas.filter(data__lte=data_fim)
        
        # Calcular estatísticas
        from django.db.models import Count, Case, When, IntegerField, Sum, F
        
        total = presencas.count()
        presentes = presencas.filter(presente=True).count()
        ausentes = total - presentes
        
        # Calcular taxa de presença
        taxa_presenca = (presentes / total * 100) if total > 0 else 0
        
        # Agrupar por aluno
        alunos_stats = presencas.values('aluno__nome', 'aluno__cpf').annotate(
            total=Count('id'),
            presentes=Sum(Case(
                When(presente=True, then=1),
                default=0,
                output_field=IntegerField()
            ))
        ).order_by('-presentes')
        
        # Calcular percentual para cada aluno
        for aluno in alunos_stats:
            aluno['percentual'] = (aluno['presentes'] / aluno['total'] * 100) if aluno['total'] > 0 else 0
            aluno['ausentes'] = aluno['total'] - aluno['presentes']
        
        # Agrupar por turma
        turmas_stats = presencas.values('atividade__turmas__nome').annotate(
            total=Count('id'),
            presentes=Sum(Case(
                When(presente=True, then=1),
                default=0,
                output_field=IntegerField()
            ))
        ).order_by('-presentes')
        
        # Calcular percentual para cada turma
        for turma in turmas_stats:
            turma['percentual'] = (turma['presentes'] / turma['total'] * 100) if turma['total'] > 0 else 0
            turma['ausentes'] = turma['total'] - turma['presentes']
        
        # Agrupar por data
        datas_stats = presencas.values('data').annotate(
            total=Count('id'),
            presentes=Sum(Case(
                When(presente=True, then=1),
                default=0,
                output_field=IntegerField()
            ))
        ).order_by('-data')
        
        # Calcular percentual para cada data
        for data in datas_stats:
            data['percentual'] = (data['presentes'] / data['total'] * 100) if data['total'] > 0 else 0
            data['ausentes'] = data['total'] - data['presentes']
        
        # Obter dados para filtros
        alunos = Aluno.objects.all().order_by('nome')
        turmas = Turma.objects.filter(status='A').order_by('nome')
        
        # Preparar dados para gráficos
        import json
        
        # Dados para gráfico de presença por aluno
        alunos_labels = [a['aluno__nome'] for a in alunos_stats[:10]]  # Top 10 alunos
        alunos_presenca = [a['percentual'] for a in alunos_stats[:10]]
        
        # Dados para gráfico de presença por turma
        turmas_labels = [t['atividade__turmas__nome'] for t in turmas_stats]
        turmas_presenca = [t['percentual'] for t in turmas_stats]
        
        # Dados para gráfico de presença por data
        datas_labels = [d['data'].strftime('%d/%m/%Y') for d in datas_stats]
        datas_presenca = [d['percentual'] for d in datas_stats]
        
        context = {
            'total': total,
            'presentes': presentes,
            'ausentes': ausentes,
            'taxa_presenca': taxa_presenca,
            'alunos_stats': alunos_stats,
            'turmas_stats': turmas_stats,
            'datas_stats': datas_stats,
            'alunos': alunos,
            'turmas': turmas,
            'filtros': {
                'aluno': aluno_id,
                'turma': turma_id,
                'data_inicio': data_inicio,
                'data_fim': data_fim,
            },
            # Dados para gráficos
            'alunos_labels': json.dumps(alunos_labels),
            'alunos_presenca': json.dumps(alunos_presenca),
            'turmas_labels': json.dumps(turmas_labels),
            'turmas_presenca': json.dumps(turmas_presenca),
            'datas_labels': json.dumps(datas_labels),
            'datas_presenca': json.dumps(datas_presenca),
        }
        
        return render(request, 'presencas/relatorio_presencas.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao gerar relatório de presenças: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao gerar relatório: {str(e)}")
        return redirect('presencas:listar_presencas')

@login_required
def filtrar_presencas(request):
    """Exibe o formulário de filtro avançado de presenças."""
    try:
        # Obter modelos dinamicamente
        Aluno = get_model_dynamically("alunos", "Aluno")
        Turma = get_model_dynamically("turmas", "Turma")
        AtividadeAcademica = get_model_dynamically("atividades", "AtividadeAcademica")
        
        # Obter dados para filtros
        alunos = Aluno.objects.all().order_by('nome')
        turmas = Turma.objects.filter(status='A').order_by('nome')
        atividades = AtividadeAcademica.objects.all().order_by('-data_inicio')
        
        context = {
            'alunos': alunos,
            'turmas': turmas,
            'atividades': atividades,
        }
        
        return render(request, 'presencas/filtro_presencas.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao exibir filtro de presenças: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao carregar filtros: {str(e)}")
        return redirect('presencas:listar_presencas')
