<UPDATED_CODE>from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
import csv
import logging
from importlib import import_module
from datetime import datetime
import calendar
from django.utils import timezone
from django.db.models import Count, Case, When, IntegerField, Sum, F
import json

logger = logging.getLogger(__name__)

def get_models():
    """Obtém os modelos FrequenciaMensal e Carencia."""
    frequencias_module = import_module("frequencias.models")
    FrequenciaMensal = getattr(frequencias_module, "FrequenciaMensal")
    Carencia = getattr(frequencias_module, "Carencia")
    return FrequenciaMensal, Carencia

def get_forms():
    """Obtém os formulários relacionados a frequências."""
    frequencias_forms = import_module("frequencias.forms")
    return (
        getattr(frequencias_forms, "FrequenciaMensalForm"),
        getattr(frequencias_forms, "FiltroPainelFrequenciasForm")
    )

def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)

@login_required
def listar_frequencias(request):
    """Lista todas as frequências mensais."""
    try:
        FrequenciaMensal, _ = get_models()
        
        # Aplicar filtros
        frequencias = FrequenciaMensal.objects.all().select_related('turma')
        
        # Filtrar por turma
        turma_id = request.GET.get('turma')
        if turma_id:
            frequencias = frequencias.filter(turma_id=turma_id)
        
        # Filtrar por ano
        ano = request.GET.get('ano')
        if ano:
            frequencias = frequencias.filter(ano=ano)
        
        # Ordenar
        frequencias = frequencias.order_by('-ano', '-mes', 'turma__nome')
        
        # Paginação
        paginator = Paginator(frequencias, 20)  # 20 itens por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Obter turmas para filtro
        Turma = get_turma_model()
        turmas = Turma.objects.filter(status='A')
        
        # Obter anos disponíveis
        anos = FrequenciaMensal.objects.values_list('ano', flat=True).distinct().order_by('-ano')
        
        context = {
            'frequencias': page_obj,
            'page_obj': page_obj,
            'turmas': turmas,
            'anos': anos,
            'turma_selecionada': turma_id,
            'ano_selecionado': ano
        }
        
        return render(request, 'frequencias/listar_frequencias.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao listar frequências: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao listar frequências: {str(e)}")
        return redirect('home')

@login_required
def criar_frequencia_mensal(request):
    """Cria uma nova frequência mensal."""
    try:
        FrequenciaMensalForm, _ = get_forms()
        
        if request.method == 'POST':
            form = FrequenciaMensalForm(request.POST)
            if form.is_valid():
                frequencia = form.save()
                
                # Calcular carências automaticamente
                frequencia.calcular_carencias()
                
                messages.success(request, "Frequência mensal criada com sucesso!")
                return redirect('frequencias:detalhar_frequencia_mensal', frequencia_id=frequencia.id)
        else:
            form = FrequenciaMensalForm()
        
        context = {
            'form': form,
            'titulo': 'Criar Frequência Mensal'
        }
        
        return render(request, 'frequencias/formulario_frequencia_mensal.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao criar frequência mensal: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao criar frequência mensal: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def editar_frequencia_mensal(request, frequencia_id):
    """Edita uma frequência mensal existente."""
    try:
        FrequenciaMensal, _ = get_models()
        FrequenciaMensalForm, _ = get_forms()
        
        frequencia = get_object_or_404(FrequenciaMensal, id=frequencia_id)
        
        if request.method == 'POST':
            form = FrequenciaMensalForm(request.POST, instance=frequencia)
            if form.is_valid():
                frequencia = form.save()
                
                # Recalcular carências se necessário
                if 'recalcular' in request.POST:
                    frequencia.calcular_carencias()
                    messages.success(request, "Frequência mensal atualizada e carências recalculadas!")
                else:
                    messages.success(request, "Frequência mensal atualizada com sucesso!")
                
                return redirect('frequencias:detalhar_frequencia_mensal', frequencia_id=frequencia.id)
        else:
            form = FrequenciaMensalForm(instance=frequencia)
        
        context = {
            'form': form,
            'frequencia': frequencia,
            'titulo': 'Editar Frequência Mensal'
        }
        
        return render(request, 'frequencias/formulario_frequencia_mensal.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao editar frequência mensal: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao editar frequência mensal: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def excluir_frequencia_mensal(request, frequencia_id):
    """Exclui uma frequência mensal."""
    try:
        FrequenciaMensal, _ = get_models()
        frequencia = get_object_or_404(FrequenciaMensal, id=frequencia_id)
        
        if request.method == 'POST':
            frequencia.delete()
            messages.success(request, "Frequência mensal excluída com sucesso!")
            return redirect('frequencias:listar_frequencias')
        
        context = {
            'frequencia': frequencia
        }
        
        return render(request, 'frequencias/excluir_frequencia_mensal.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao excluir frequência mensal: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao excluir frequência mensal: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def detalhar_frequencia_mensal(request, frequencia_id):
    """Exibe os detalhes de uma frequência mensal."""
    try:
        FrequenciaMensal, Carencia = get_models()
        frequencia = get_object_or_404(FrequenciaMensal, id=frequencia_id)
        
        # Obter carências
        carencias = Carencia.objects.filter(frequencia_mensal=frequencia).select_related('aluno')
        
        # Ordenar carências
        carencias = carencias.order_by('liberado', 'aluno__nome')
        
        # Preparar dados para gráfico
        alunos_labels = []
        percentuais_presenca = []
        
        for carencia in carencias:
            alunos_labels.append(carencia.aluno.nome)
            percentuais_presenca.append(float(carencia.percentual_presenca))
        
        # Calcular total de alunos
        total_alunos = carencias.count()
        
        context = {
            'frequencia': frequencia,
            'carencias': carencias,
            'total_alunos': total_alunos,
            'alunos_labels': json.dumps(alunos_labels),
            'percentuais_presenca': json.dumps(percentuais_presenca)
        }
        
        return render(request, 'frequencias/detalhar_frequencia_mensal.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao detalhar frequência mensal: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao detalhar frequência mensal: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def recalcular_carencias(request, frequencia_id):
    """Recalcula as carências de uma frequência mensal."""
    try:
        FrequenciaMensal, _ = get_models()
        frequencia = get_object_or_404(FrequenciaMensal, id=frequencia_id)
        
        # Recalcular carências
        frequencia.calcular_carencias()
        
        messages.success(request, "Carências recalculadas com sucesso!")
        return redirect('frequencias:detalhar_frequencia_mensal', frequencia_id=frequencia.id)
    
    except Exception as e:
        logger.error(f"Erro ao recalcular carências: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao recalcular carências: {str(e)}")
        return redirect('frequencias:detalhar_frequencia_mensal', frequencia_id=frequencia_id)

@login_required
def editar_carencia(request, carencia_id):
    """Edita uma carência específica."""
    try:
        _, Carencia = get_models()
        carencia = get_object_or_404(Carencia, id=carencia_id)
        
        if request.method == 'POST':
            # Atualizar campos da carência
            liberado = request.POST.get('liberado') == 'on'
            observacoes = request.POST.get('observacoes', '')
            
            carencia.liberado = liberado
            carencia.observacoes = observacoes
            carencia.save()
            
            messages.success(request, "Carência atualizada com sucesso!")
            return redirect('frequencias:detalhar_frequencia_mensal', frequencia_id=carencia.frequencia_mensal.id)
        
        context = {
            'carencia': carencia
        }
        
        return render(request, 'frequencias/editar_carencia.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao editar carência: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao editar carência: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def exportar_frequencia_csv(request, frequencia_id):
    """Exporta os dados de uma frequência mensal para CSV."""
    try:
        FrequenciaMensal, Carencia = get_models()
        frequencia = get_object_or_404(FrequenciaMensal, id=frequencia_id)
        
        # Obter carências
        carencias = Carencia.objects.filter(frequencia_mensal=frequencia).select_related('aluno')
        
        # Criar resposta CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="frequencia_{frequencia.turma.nome}_{frequencia.get_mes_display()}_{frequencia.ano}.csv"'
        
        # Escrever cabeçalho e dados
        writer = csv.writer(response)
        writer.writerow(['CPF', 'Aluno', 'Presenças', 'Total Atividades', 'Percentual', 'Carências', 'Liberado', 'Observações'])
        
        for carencia in carencias:
            writer.writerow([
                carencia.aluno.cpf,
                carencia.aluno.nome,
                carencia.total_presencas,
                carencia.total_atividades,
                f"{carencia.percentual_presenca:.2f}",
                carencia.numero_carencias,
                'Sim' if carencia.liberado else 'Não',
                carencia.observacoes or ''
            ])
        
        return response
    
    except Exception as e:
        logger.error(f"Erro ao exportar frequência: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao exportar frequência: {str(e)}")
        return redirect('frequencias:detalhar_frequencia_mensal', frequencia_id=frequencia_id)

@login_required
def painel_frequencias(request):
    """Exibe um painel de frequências para uma turma."""
    try:
        _, FiltroPainelFrequenciasForm = get_forms()
        
        if request.method == 'POST':
            form = FiltroPainelFrequenciasForm(request.POST)
            if form.is_valid():
                # Redirecionar para a página do painel com os parâmetros
                return redirect('frequencias:visualizar_painel_frequencias', 
                               turma_id=form.cleaned_data['turma'].id,
                               mes_inicio=form.cleaned_data['mes_inicio'],
                               ano_inicio=form.cleaned_data['ano_inicio'],
                               mes_fim=form.cleaned_data['mes_fim'],
                               ano_fim=form.cleaned_data['ano_fim'])
        else:
            form = FiltroPainelFrequenciasForm()
        
        context = {
            'form': form
        }
        
        return render(request, 'frequencias/painel_frequencias_form.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao acessar painel de frequências: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao acessar painel de frequências: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def visualizar_painel_frequencias(request, turma_id, mes_inicio, ano_inicio, mes_fim, ano_fim):
    """Visualiza o painel de frequências para uma turma em um período."""
    try:
        FrequenciaMensal, _ = get_models()
        Turma = get_turma_model()
        
        # Obter turma
        turma = get_object_or_404(Turma, id=turma_id)
        
        # Converter parâmetros para inteiros
        mes_inicio = int(mes_inicio)
        ano_inicio = int(ano_inicio)
        mes_fim = int(mes_fim)
        ano_fim = int(ano_fim)
        
        # Calcular período em meses
        data_inicio = ano_inicio * 12 + mes_inicio
        data_fim = ano_fim * 12 + mes_fim
        
        # Obter frequências no período
        frequencias = FrequenciaMensal.objects.filter(
            turma=turma
        ).select_related('turma')
        
        # Filtrar pelo período
        frequencias_filtradas = [
            f for f in frequencias
            if data_inicio <= (f.ano * 12 + f.mes) <= data_fim
        ]
        
        # Ordenar por ano e mês
        frequencias_filtradas.sort(key=lambda x: (x.ano, x.mes))
        
        context = {
            'turma': turma,
            'mes_inicio': mes_inicio,
            'ano_inicio': ano_inicio,
            'mes_fim': mes_fim,
            'ano_fim': ano_fim,
            'frequencias': frequencias_filtradas
        }
        
        return render(request, 'frequencias/visualizar_painel_frequencias.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao visualizar painel de frequências: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao visualizar painel de frequências: {str(e)}")
        return redirect('frequencias:painel_frequencias')

@login_required
def relatorio_frequencias(request):
    """Exibe um relatório de frequências."""
    try:
        FrequenciaMensal, Carencia = get_models()
        
        # Estatísticas gerais
        total_frequencias = FrequenciaMensal.objects.count()
        
        # Obter total de alunos com carência
        total_carencias = Carencia.objects.count()
        total_liberados = Carencia.objects.filter(liberado=True).count()
        total_nao_liberados = total_carencias - total_liberados
        
        # Percentuais
        percentual_liberados = (total_liberados / total_carencias * 100) if total_carencias > 0 else 0
        percentual_nao_liberados = (total_nao_liberados / total_carencias * 100) if total_carencias > 0 else 0
        
        # Frequências por mês
        from django.db.models import Count
        from django.db.models.functions import TruncMonth
        
        # Agrupar por mês e ano
        frequencias_por_mes = FrequenciaMensal.objects.values('mes', 'ano').annotate(
            total=Count('id')
        ).order_by('ano', 'mes')
        
        # Formatar dados para gráficos
        meses = []
        dados_frequencias = []
        
        for item in frequencias_por_mes:
            mes_nome = dict(FrequenciaMensal.MES_CHOICES).get(item['mes'])
            meses.append(f"{mes_nome}/{item['ano']}")
            dados_frequencias.append(item['total'])
        
        context = {
            'total_frequencias': total_frequencias,
            'total_carencias': total_carencias,
            'total_liberados': total_liberados,
            'total_nao_liberados': total_nao_liberados,
            'percentual_liberados': percentual_liberados,
            'percentual_nao_liberados': percentual_nao_liberados,
            'meses': meses,
            'dados_frequencias': dados_frequencias
        }
        
        return render(request, 'frequencias/relatorio_frequencias.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao gerar relatório de frequências: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao gerar relatório: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def dashboard(request):
    """Exibe um dashboard com estatísticas de frequência."""
    try:
        FrequenciaMensal, Carencia = get_models()
        
        # Obter parâmetros de filtro
        periodo = request.GET.get('periodo')
        curso_id = request.GET.get('curso')
        turma_id = request.GET.get('turma')
        
        # Construir query base
        frequencias = FrequenciaMensal.objects.all().select_related('turma')
        carencias = Carencia.objects.all().select_related('frequencia_mensal', 'aluno')
        
        # Aplicar filtros
        if periodo:
            ano, mes = periodo.split('-')
            frequencias = frequencias.filter(ano=ano, mes=mes)
            carencias = carencias.filter(frequencia_mensal__ano=ano, frequencia_mensal__mes=mes)
        
        if curso_id:
            frequencias = frequencias.filter(turma__curso__codigo_curso=curso_id)
            carencias = carencias.filter(frequencia_mensal__turma__curso__codigo_curso=curso_id)
        
        if turma_id:
            frequencias = frequencias.filter(turma__id=turma_id)
            carencias = carencias.filter(frequencia_mensal__turma__id=turma_id)
        
        # Calcular estatísticas
        total_alunos = carencias.values('aluno').distinct().count()
        alunos_regulares = carencias.filter(percentual_presenca__gte=75).values('aluno').distinct().count()
        alunos_carencia = carencias.filter(percentual_presenca__lt=75).values('aluno').distinct().count()
        
        # Calcular média de frequência
        from django.db.models import Avg
        media_frequencia = carencias.aggregate(Avg('percentual_presenca'))['percentual_presenca__avg'] or 0
        
        # Obter turmas com menor frequência
        turmas_menor_frequencia = []
        turmas_ids = frequencias.values_list('turma__id', flat=True).distinct()
        
        for turma_id in turmas_ids:
            carencias_turma = carencias.filter(frequencia_mensal__turma__id=turma_id)
            if carencias_turma.exists():
                media_turma = carencias_turma.aggregate(Avg('percentual_presenca'))['percentual_presenca__avg'] or 0
                alunos_carencia_turma = carencias_turma.filter(percentual_presenca__lt=75).count()
                total_alunos_turma = carencias_turma.count()
                
                # Obter informações da turma
                turma = get_turma_model().objects.get(id=turma_id)
                
                # Obter período (mês/ano) da frequência mais recente
                ultima_frequencia = frequencias.filter(turma__id=turma_id).order_by('-ano', '-mes').first()
                
                turmas_menor_frequencia.append({
                    'id': turma_id,
                    'nome': turma.nome,
                    'curso': turma.curso,
                    'media_frequencia': media_turma,
                    'alunos_carencia': alunos_carencia_turma,
                    'total_alunos': total_alunos_turma,
                    'periodo_mes': ultima_frequencia.get_mes_display() if ultima_frequencia else '',
                    'periodo_ano': ultima_frequencia.ano if ultima_frequencia else ''
                })
        
        # Ordenar turmas por média de frequência (ascendente)
        turmas_menor_frequencia.sort(key=lambda x: x['media_frequencia'])
        
        # Limitar a 5 turmas
        turmas_menor_frequencia = turmas_menor_frequencia[:5]
        
        # Obter alunos com menor frequência
        alunos_menor_frequencia = []
        alunos_ids = carencias.filter(percentual_presenca__lt=75).values_list('aluno__cpf', flat=True).distinct()
        
        for aluno_id in alunos_ids:
            carencia_aluno = carencias.filter(aluno__cpf=aluno_id).order_by('percentual_presenca').first()
            if carencia_aluno:
                alunos_menor_frequencia.append({
                    'cpf': aluno_id,
                    'nome': carencia_aluno.aluno.nome,
                    'email': carencia_aluno.aluno.email,
                    'foto': carencia_aluno.aluno.foto.url if carencia_aluno.aluno.foto else None,
                    'turma': carencia_aluno.frequencia_mensal.turma.nome,
                    'curso': carencia_aluno.frequencia_mensal.turma.curso.nome,
                    'percentual_presenca': carencia_aluno.percentual_presenca,
                    'periodo_mes': carencia_aluno.frequencia_mensal.get_mes_display(),
                    'periodo_ano': carencia_aluno.frequencia_mensal.ano,
                    'carencia_id': carencia_aluno.id,
                    'status_carencia': carencia_aluno.status if hasattr(carencia_aluno, 'status') else 'PENDENTE'
                })
        
        # Ordenar alunos por percentual de presença (ascendente)
        alunos_menor_frequencia.sort(key=lambda x: x['percentual_presenca'])
        
        # Limitar a 10 alunos
        alunos_menor_frequencia = alunos_menor_frequencia[:10]
        
        # Dados para gráficos
        # 1. Frequência por curso
        cursos_labels = []
        frequencia_por_curso = []
        
        Curso = get_model_dynamically("cursos", "Curso")
        cursos = Curso.objects.all()
        
        for curso in cursos:
            carencias_curso = carencias.filter(frequencia_mensal__turma__curso=curso)
            if carencias_curso.exists():
                media_curso = carencias_curso.aggregate(Avg('percentual_presenca'))['percentual_presenca__avg'] or 0
                cursos_labels.append(curso.nome)
                frequencia_por_curso.append(float(media_curso))
        
        # 2. Evolução da frequência por período
        periodos_labels = []
        evolucao_frequencia = []
        
        # Obter últimos 6 meses
        from datetime import datetime, timedelta
        
        hoje = datetime.now()
        for i in range(5, -1, -1):
            data = hoje - timedelta(days=30 * i)
            mes = data.month
            ano = data.year
            
            # Obter frequências do mês
            carencias_periodo = carencias.filter(frequencia_mensal__mes=mes, frequencia_mensal__ano=ano)
            if carencias_periodo.exists():
                media_periodo = carencias_periodo.aggregate(Avg('percentual_presenca'))['percentual_presenca__avg'] or 0
                mes_nome = dict(FrequenciaMensal.MES_CHOICES).get(mes)
                periodos_labels.append(f"{mes_nome}/{ano}")
                evolucao_frequencia.append(float(media_periodo))
            else:
                mes_nome = dict(FrequenciaMensal.MES_CHOICES).get(mes)
                periodos_labels.append(f"{mes_nome}/{ano}")
                evolucao_frequencia.append(0)
        
        # Obter dados para filtros
        anos = FrequenciaMensal.objects.values_list('ano', flat=True).distinct().order_by('-ano')
        meses = FrequenciaMensal.MES_CHOICES
        
        # Obter contagem por status
        status_counts = {}
        for status, _ in FrequenciaMensal.objects.model.STATUS_CHOICES:
            count = FrequenciaMensal.objects.filter(status=status).count()
            status_counts[status] = count
        
        # Obter contagem por tipo
        academicas_por_tipo = {}
        for tipo, _ in FrequenciaMensal.objects.model.TIPO_CHOICES:
            count = FrequenciaMensal.objects.filter(tipo_atividade=tipo).count()
            academicas_por_tipo[tipo] = count
        
        context = {
            'estatisticas': {
                'total_alunos': total_alunos,
                'alunos_regulares': alunos_regulares,
                'alunos_carencia': alunos_carencia,
                'media_frequencia': media_frequencia
            },
            'turmas_menor_frequencia': turmas_menor_frequencia,
            'alunos_menor_frequencia': alunos_menor_frequencia,
            'cursos_labels': json.dumps(cursos_labels),
            'frequencia_por_curso': json.dumps(frequencia_por_curso),
            'periodos_labels': json.dumps(periodos_labels),
            'evolucao_frequencia': json.dumps(evolucao_frequencia),
            'filtros': {
                'periodo': periodo,
                'curso': curso_id,
                'turma': turma_id
            },
            'anos': anos,
            'meses': meses,
            'cursos': cursos,
            'turmas': get_turma_model().objects.filter(status='A'),
            'status_counts': status_counts,
            'academicas_por_tipo': academicas_por_tipo
        }
        
        return render(request, 'frequencias/dashboard.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao exibir dashboard: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao exibir dashboard: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def historico_frequencia(request, aluno_cpf):
    """Exibe o histórico de frequência de um aluno."""
    try:
        FrequenciaMensal, Carencia = get_models()
        Aluno = get_model_dynamically("alunos", "Aluno")
        
        # Obter aluno
        aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
        
        # Obter parâmetros de filtro
        curso_id = request.GET.get('curso')
        turma_id = request.GET.get('turma')
        periodo = request.GET.get('periodo')
        
        # Construir query base
        carencias = Carencia.objects.filter(aluno=aluno).select_related('frequencia_mensal', 'frequencia_mensal__turma')
        
        # Aplicar filtros
        if curso_id:
            carencias = carencias.filter(frequencia_mensal__turma__curso__codigo_curso=curso_id)
        
        if turma_id:
            carencias = carencias.filter(frequencia_mensal__turma__id=turma_id)
        
        if periodo:
            ano, mes = periodo.split('-')
            carencias = carencias.filter(frequencia_mensal__ano=ano, frequencia_mensal__mes=mes)
        
        # Ordenar por período (mais recente primeiro)
        carencias = carencias.order_by('-frequencia_mensal__ano', '-frequencia_mensal__mes')
        
        # Paginação
        paginator = Paginator(carencias, 10)  # 10 itens por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Calcular média geral de frequência
        from django.db.models import Avg
        media_geral = carencias.aggregate(Avg('percentual_presenca'))['percentual_presenca__avg'] or 0
        
        # Dados para gráfico de evolução
        periodos_labels = []
        percentuais_presenca = []
        
        # Limitar a 12 períodos mais recentes
        for carencia in carencias[:12]:
            periodo_label = f"{carencia.frequencia_mensal.get_mes_display()}/{carencia.frequencia_mensal.ano}"
            periodos_labels.append(periodo_label)
            percentuais_presenca.append(float(carencia.percentual_presenca))
        
        # Inverter para ordem cronológica
        periodos_labels.reverse()
        percentuais_presenca.reverse()
        
        # Obter dados para filtros
        Curso = get_model_dynamically("cursos", "Curso")
        cursos = Curso.objects.all()
        
        Turma = get_turma_model()
        turmas = Turma.objects.filter(matriculas__aluno=aluno).distinct()
        
        anos = FrequenciaMensal.objects.filter(carencia__aluno=aluno).values_list('ano', flat=True).distinct().order_by('-ano')
        meses = FrequenciaMensal.MES_CHOICES
        
        context = {
            'aluno': aluno,
            'registros': page_obj,
            'total_registros': carencias.count(),
            'media_geral': media_geral,
            'carencias': carencias.filter(percentual_presenca__lt=75),
            'periodos_labels': json.dumps(periodos_labels),
            'percentuais_presenca': json.dumps(percentuais_presenca),
            'filtros': {
                'curso': curso_id,
                'turma': turma_id,
                'periodo': periodo
            },
            'cursos': cursos,
            'turmas': turmas,
            'anos': anos,
            'meses': meses
        }
        
        return render(request, 'frequencias/historico_frequencia.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao exibir histórico de frequência: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao exibir histórico de frequência: {str(e)}")
        return redirect('alunos:detalhar_aluno', cpf=aluno_cpf)

@login_required
def exportar_historico(request, aluno_cpf):
    """Exporta o histórico de frequência de um aluno para CSV."""
    try:
        _, Carencia = get_models()
        Aluno = get_model_dynamically("alunos", "Aluno")
        
        # Obter aluno
        aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
        
        # Obter carências
        carencias = Carencia.objects.filter(aluno=aluno).select_related('frequencia_mensal', 'frequencia_mensal__turma')
        
        # Criar resposta CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="historico_frequencia_{aluno.nome}.csv"'
        
        # Escrever cabeçalho e dados
        writer = csv.writer(response)
        writer.writerow(['Curso', 'Turma', 'Período', 'Presenças', 'Faltas', 'Total Aulas', 'Percentual', 'Status'])
        
        for carencia in carencias:
            writer.writerow([
                carencia.frequencia_mensal.turma.curso.nome,
                carencia.frequencia_mensal.turma.nome,
                f"{carencia.frequencia_mensal.get_mes_display()}/{carencia.frequencia_mensal.ano}",
                carencia.total_presencas,
                carencia.total_atividades - carencia.total_presencas,
                carencia.total_atividades,
                f"{carencia.percentual_presenca:.2f}",
                'Regular' if carencia.percentual_presenca >= 75 else 'Carência'
            ])
        
        return response
    
    except Exception as e:
        logger.error(f"Erro ao exportar histórico: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao exportar histórico: {str(e)}")
        return redirect('frequencias:historico_frequencia', aluno_cpf=aluno_cpf)

@login_required
def iniciar_acompanhamento(request, carencia_id):
    """Inicia o acompanhamento de uma carência."""
    try:
        _, Carencia = get_models()
        carencia = get_object_or_404(Carencia, id=carencia_id)
        
        if request.method == 'POST':
            # Atualizar status da carência
            carencia.status = 'EM_ACOMPANHAMENTO'
            carencia.data_acompanhamento = timezone.now()
            carencia.acompanhado_por = request.user
            carencia.observacoes = request.POST.get('observacoes', '')
            carencia.prazo_resolucao = request.POST.get('prazo_resolucao')
            carencia.save()
            
            # Criar notificação se solicitado
            if request.POST.get('criar_notificacao'):
                Notificacao = get_model_dynamically("notificacoes", "Notificacao")
                
                notificacao = Notificacao.objects.create(
                    aluno=carencia.aluno,
                    carencia=carencia,
                    assunto=request.POST.get('assunto'),
                    mensagem=request.POST.get('mensagem'),
                    criado_por=request.user,
                    data_criacao=timezone.now()
                )
                
                # Enviar notificação imediatamente se solicitado
                if request.POST.get('enviar_agora'):
                    notificacao.status = 'ENVIADA'
                    notificacao.data_envio = timezone.now()
                    notificacao.enviado_por = request.user
                    notificacao.save()
                    
                    # Lógica para enviar a notificação (e-mail, SMS, etc.)
                    try:
                        # Implementar envio de notificação
                        pass
                    except Exception as e:
                        logger.error(f"Erro ao enviar notificação: {str(e)}", exc_info=True)
                        messages.warning(request, f"Acompanhamento iniciado, mas houve um erro ao enviar a notificação: {str(e)}")
                        return redirect('frequencias:detalhar_carencia', carencia_id=carencia.id)
            
            messages.success(request, "Acompanhamento iniciado com sucesso!")
            return redirect('frequencias:detalhar_carencia', carencia_id=carencia.id)
        
        context = {
            'carencia': carencia,
            'data_atual': timezone.now().date()
        }
        
        return render(request, 'frequencias/iniciar_acompanhamento.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao iniciar acompanhamento: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao iniciar acompanhamento: {str(e)}")
        return redirect('frequencias:detalhar_carencia', carencia_id=carencia_id)

@login_required
def resolver_carencia(request, carencia_id):
    """Resolve uma carência."""
    try:
        _, Carencia = get_models()
        carencia = get_object_or_404(Carencia, id=carencia_id)
        
        if request.method == 'POST':
            # Atualizar status da carência
            carencia.status = 'RESOLVIDO'
            carencia.data_resolucao = timezone.now()
            carencia.resolvido_por = request.user
            carencia.motivo_resolucao = request.POST.get('motivo_resolucao')
            carencia.observacoes_resolucao = request.POST.get('observacoes_resolucao', '')
            carencia.liberado = True
            carencia.save()
            
            # Processar documentos anexados
            for arquivo in request.FILES.getlist('documentos'):
                Documento = get_model_dynamically("documentos", "Documento")
                
                documento = Documento.objects.create(
                    nome=arquivo.name,
                    arquivo=arquivo,
                    tipo='CARENCIA',
                    aluno=carencia.aluno,
                    uploaded_by=request.user
                )
                
                # Associar documento à carência
                carencia.documentos_resolucao.add(documento)
            
            messages.success(request, "Carência resolvida com sucesso!")
            return redirect('frequencias:detalhar_carencia', carencia_id=carencia.id)
        
        context = {
            'carencia': carencia
        }
        
        return render(request, 'frequencias/resolver_carencia.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao resolver carência: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao resolver carência: {str(e)}")
        return redirect('frequencias:detalhar_carencia', carencia_id=carencia_id)

@login_required
def detalhar_carencia(request, carencia_id):
    """Exibe os detalhes de uma carência."""
    try:
        _, Carencia = get_models()
        carencia = get_object_or_404(Carencia, id=carencia_id)
        
        context = {
            'carencia': carencia
        }
        
        return render(request, 'frequencias/detalhar_carencia.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao detalhar carência: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao detalhar carência: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def criar_notificacao(request, carencia_id):
    """Cria uma notificação para uma carência."""
    try:
        _, Carencia = get_models()
        carencia = get_object_or_404(Carencia, id=carencia_id)
        
        if request.method == 'POST':
            Notificacao = get_model_dynamically("notificacoes", "Notificacao")
            
            notificacao = Notificacao.objects.create(
                aluno=carencia.aluno,
                carencia=carencia,
                assunto=request.POST.get('assunto'),
                mensagem=request.POST.get('mensagem'),
                tipo_notificacao=request.POST.get('tipo_notificacao'),
                prioridade=request.POST.get('prioridade'),
                criado_por=request.user,
                data_criacao=timezone.now()
            )
            
            # Processar anexos
            for arquivo in request.FILES.getlist('anexos'):
                Anexo = get_model_dynamically("notificacoes", "Anexo")
                
                anexo = Anexo.objects.create(
                    notificacao=notificacao,
                    nome=arquivo.name,
                    arquivo=arquivo,
                    uploaded_by=request.user
                )
            
            # Enviar notificação imediatamente se solicitado
            if request.POST.get('enviar_agora'):
                notificacao.status = 'ENVIADA'
                notificacao.data_envio = timezone.now()
                notificacao.enviado_por = request.user
                notificacao.save()
                
                # Lógica para enviar a notificação (e-mail, SMS, etc.)
                try:
                    # Implementar envio de notificação
                    pass
                except Exception as e:
                    logger.error(f"Erro ao enviar notificação: {str(e)}", exc_info=True)
                    messages.warning(request, f"Notificação criada, mas houve um erro ao enviá-la: {str(e)}")
                    return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
            
            messages.success(request, "Notificação criada com sucesso!")
            return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
        
        context = {
            'carencia': carencia
        }
        
        return render(request, 'frequencias/criar_notificacao.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao criar notificação: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao criar notificação: {str(e)}")
        return redirect('frequencias:detalhar_carencia', carencia_id=carencia_id)

@login_required
def detalhar_notificacao(request, notificacao_id):
    """Exibe os detalhes de uma notificação."""
    try:
        Notificacao = get_model_dynamically("notificacoes", "Notificacao")
        notificacao = get_object_or_404(Notificacao, id=notificacao_id)
        
        context = {
            'notificacao': notificacao
        }
        
        return render(request, 'frequencias/detalhar_notificacao.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao detalhar notificação: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao detalhar notificação: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def editar_notificacao(request, notificacao_id):
    """Edita uma notificação."""
    try:
        Notificacao = get_model_dynamically("notificacoes", "Notificacao")
        notificacao = get_object_or_404(Notificacao, id=notificacao_id)
        
        # Verificar se a notificação já foi enviada
        if notificacao.status != 'PENDENTE':
            messages.warning(request, "Esta notificação já foi enviada e não pode ser editada.")
            return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
        
        if request.method == 'POST':
            action = request.POST.get('action', 'salvar')
            
            # Atualizar dados da notificação
            notificacao.assunto = request.POST.get('assunto')
            notificacao.mensagem = request.POST.get('mensagem')
            
            # Processar anexos
            for arquivo in request.FILES.getlist('anexos'):
                Anexo = get_model_dynamically("notificacoes", "Anexo")
                
                anexo = Anexo.objects.create(
                    notificacao=notificacao,
                    nome=arquivo.name,
                    arquivo=arquivo,
                    uploaded_by=request.user
                )
            
            # Remover anexos selecionados
            for anexo_id in request.POST.getlist('remover_anexos'):
                Anexo = get_model_dynamically("notificacoes", "Anexo")
                anexo = get_object_or_404(Anexo, id=anexo_id)
                anexo.delete()
            
            notificacao.save()
            
            # Enviar notificação se solicitado
            if action == 'salvar_enviar':
                notificacao.status = 'ENVIADA'
                notificacao.data_envio = timezone.now()
                notificacao.enviado_por = request.user
                notificacao.save()
                
                # Lógica para enviar a notificação (e-mail, SMS, etc.)
                try:
                    # Implementar envio de notificação
                    pass
                except Exception as e:
                    logger.error(f"Erro ao enviar notificação: {str(e)}", exc_info=True)
                    messages.warning(request, f"Notificação atualizada, mas houve um erro ao enviá-la: {str(e)}")
                    return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
                
                messages.success(request, "Notificação atualizada e enviada com sucesso!")
            else:
                messages.success(request, "Notificação atualizada com sucesso!")
            
            return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
        
        context = {
            'notificacao': notificacao
        }
        
        return render(request, 'frequencias/editar_notificacao.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao editar notificação: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao editar notificação: {str(e)}")
        return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao_id)

@login_required
def enviar_notificacao(request, notificacao_id):
    """Envia uma notificação."""
    try:
        Notificacao = get_model_dynamically("notificacoes", "Notificacao")
        notificacao = get_object_or_404(Notificacao, id=notificacao_id)
        
        # Verificar se a notificação já foi enviada
        if notificacao.status != 'PENDENTE':
            messages.warning(request, "Esta notificação já foi enviada.")
            return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
        
        if request.method == 'POST':
            # Atualizar status da notificação
            notificacao.status = 'ENVIADA'
            notificacao.data_envio = timezone.now()
            notificacao.enviado_por = request.user
            
            # Atualizar status da carência se solicitado
            if request.POST.get('marcar_acompanhamento') and notificacao.carencia and notificacao.carencia.status == 'PENDENTE':
                notificacao.carencia.status = 'EM_ACOMPANHAMENTO'
                notificacao.carencia.data_acompanhamento = timezone.now()
                notificacao.carencia.acompanhado_por = request.user
                notificacao.carencia.save()
            
            notificacao.save()
            
            # Enviar cópia para o usuário se solicitado
            enviar_copia = request.POST.get('enviar_copia')
            
            # Lógica para enviar a notificação (e-mail, SMS, etc.)
            try:
                # Implementar envio de notificação
                pass
            except Exception as e:
                logger.error(f"Erro ao enviar notificação: {str(e)}", exc_info=True)
                messages.warning(request, f"Houve um erro ao enviar a notificação: {str(e)}")
                return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
            
            messages.success(request, "Notificação enviada com sucesso!")
            return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
        
        context = {
            'notificacao': notificacao
        }
        
        return render(request, 'frequencias/enviar_notificacao.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao enviar notificação: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao enviar notificação: {str(e)}")
        return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao_id)

@login_required
def reenviar_notificacao(request, notificacao_id):
    """Reenvia uma notificação."""
    try:
        Notificacao = get_model_dynamically("notificacoes", "Notificacao")
        notificacao = get_object_or_404(Notificacao, id=notificacao_id)
        
        # Verificar se a notificação pode ser reenviada
        if notificacao.status not in ['ENVIADA', 'LIDA']:
            messages.warning(request, "Esta notificação não pode ser reenviada.")
            return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
        
        # Atualizar data de envio
        notificacao.data_envio = timezone.now()
        notificacao.enviado_por = request.user
        notificacao.save()
        
        # Lógica para reenviar a notificação (e-mail, SMS, etc.)
        try:
            # Implementar reenvio de notificação
            pass
        except Exception as e:
            logger.error(f"Erro ao reenviar notificação: {str(e)}", exc_info=True)
            messages.warning(request, f"Houve um erro ao reenviar a notificação: {str(e)}")
            return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
        
        messages.success(request, "Notificação reenviada com sucesso!")
        return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
    
    except Exception as e:
        logger.error(f"Erro ao reenviar notificação: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao reenviar notificação: {str(e)}")
        return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao_id)

@login_required
def responder_aluno(request, notificacao_id):
    """Responde a uma notificação do aluno."""
    try:
        Notificacao = get_model_dynamically("notificacoes", "Notificacao")
        notificacao = get_object_or_404(Notificacao, id=notificacao_id)
        
        # Verificar se a notificação pode ser respondida
        if notificacao.status != 'RESPONDIDA':
            messages.warning(request, "Esta notificação não possui resposta do aluno.")
            return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
        
        if request.method == 'POST':
            # Criar nova notificação como resposta
            nova_notificacao = Notificacao.objects.create(
                aluno=notificacao.aluno,
                carencia=notificacao.carencia,
                assunto=f"RE: {notificacao.assunto}",
                mensagem=request.POST.get('mensagem'),
                tipo_notificacao=notificacao.tipo_notificacao,
                prioridade=notificacao.prioridade,
                criado_por=request.user,
                data_criacao=timezone.now(),
                notificacao_pai=notificacao
            )
            
            # Processar anexos
            for arquivo in request.FILES.getlist('anexos'):
                Anexo = get_model_dynamically("notificacoes", "Anexo")
                
                anexo = Anexo.objects.create(
                    notificacao=nova_notificacao,
                    nome=arquivo.name,
                    arquivo=arquivo,
                    uploaded_by=request.user
                )
            
            # Enviar notificação imediatamente
            nova_notificacao.status = 'ENVIADA'
            nova_notificacao.data_envio = timezone.now()
            nova_notificacao.enviado_por = request.user
            nova_notificacao.save()
            
            # Lógica para enviar a notificação (e-mail, SMS, etc.)
            try:
                # Implementar envio de notificação
                pass
            except Exception as e:
                logger.error(f"Erro ao enviar resposta: {str(e)}", exc_info=True)
                messages.warning(request, f"Resposta criada, mas houve um erro ao enviá-la: {str(e)}")
                return redirect('frequencias:detalhar_notificacao', notificacao_id=nova_notificacao.id)
            
            messages.success(request, "Resposta enviada com sucesso!")
            return redirect('frequencias:detalhar_notificacao', notificacao_id=nova_notificacao.id)
        
        context = {
            'notificacao': notificacao
        }
        
        return render(request, 'frequencias/responder_aluno.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao responder aluno: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao responder aluno: {str(e)}")
        return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao_id)

@login_required
def notificacoes_carencia(request):
    """Lista todas as notificações de carência."""
    try:
        Notificacao = get_model_dynamically("notificacoes", "Notificacao")
        
        # Obter parâmetros de filtro
        status = request.GET.get('status')
        aluno_id = request.GET.get('aluno')
        tipo = request.GET.get('tipo')
        
        # Construir query base
        notificacoes = Notificacao.objects.filter(carencia__isnull=False).select_related('aluno', 'carencia')
        
        # Aplicar filtros
        if status:
            notificacoes = notificacoes.filter(status=status)
        
        if aluno_id:
            notificacoes = notificacoes.filter(aluno__cpf=aluno_id)
        
        if tipo:
            notific