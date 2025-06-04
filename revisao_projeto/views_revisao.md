# Revisão da Funcionalidade: views

## Arquivos de Views Modulares:


### Arquivo: views\academicas.py

python
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.db.models import Q

from ..forms import AtividadeAcademicaForm, AtividadeAcademicaFiltroForm
from ..utils import get_models

def listar_atividades_academicas(request):
    """
    View para listar atividades acadêmicas com filtros.
    """
    models = get_models()
    AtividadeAcademica = models['AtividadeAcademica']
    
    # Inicializa o formulário de filtro com os dados da requisição
    filtro_form = AtividadeAcademicaFiltroForm(request.GET or None)
    
    # Inicializa o queryset com todas as atividades
    atividades = AtividadeAcademica.objects.all().select_related('curso').prefetch_related('turmas')
    
    # Aplica os filtros se o formulário for válido
    if filtro_form.is_valid():
        # Filtro por texto (nome ou descrição)
        q = filtro_form.cleaned_data.get('q')
        if q:
            atividades = atividades.filter(
                Q(nome__icontains=q) | Q(descricao__icontains=q)
            )
        
        # Filtro por curso
        curso = filtro_form.cleaned_data.get('curso')
        if curso:
            atividades = atividades.filter(curso=curso)
        
        # Filtro por turma
        turma = filtro_form.cleaned_data.get('turma')
        if turma:
            atividades = atividades.filter(turmas=turma)
    
    # Ordena as atividades
    atividades = atividades.order_by('-data_inicio', 'hora_inicio')
    
    context = {
        'atividades': atividades,
        'filtro_form': filtro_form,
    }
    
    # Se for uma requisição AJAX, retorna apenas o HTML da tabela
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string(
            'atividades/academicas/partials/atividades_tabela_body.html',
            context,
            request=request
        )
        return JsonResponse({'html': html})
    
    return render(request, 'atividades/academicas/listar_atividades_academicas.html', context)

def ajax_turmas_por_curso(request):
    """
    View AJAX para obter turmas por curso.
    """
    curso_id = request.GET.get('curso_id')
    models = get_models()
    Turma = models['Turma']
    
    if curso_id:
        turmas = Turma.objects.filter(curso_id=curso_id).order_by('nome')
    else:
        turmas = Turma.objects.all().order_by('nome')
    
    return JsonResponse({
        'turmas': [{'id': turma.id, 'nome': turma.nome} for turma in turmas]
    })

# Remover a função ajax_atividades_filtradas, pois sua funcionalidade 
# foi incorporada na função listar_atividades_academicas



### Arquivo: views\dashboard.py

python
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone

from ..utils import get_models
from .utils import get_turmas_por_curso

def dashboard_atividades(request):
    """
    View para o dashboard de atividades.
    """
    models = get_models()
    AtividadeAcademica = models['AtividadeAcademica']
    Curso = models['Curso']
    
    cursos = Curso.objects.all().order_by('nome')
    
    # Inicializa o contexto com dados básicos
    context = {
        'cursos': cursos,
        'filtros': {
            'curso_id': request.GET.get('curso'),
            'turma_id': request.GET.get('turma'),
            'periodo': request.GET.get('periodo', 'mes')
        }
    }
    
    # Se for uma requisição AJAX, carrega apenas os dados do dashboard
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return ajax_dashboard_conteudo(request)
    
    return render(request, 'atividades/dashboard_atividades.html', context)

def ajax_turmas_por_curso_dashboard(request):
    """
    View AJAX para obter turmas por curso para o dashboard.
    Reutiliza a função utilitária get_turmas_por_curso.
    """
    curso_id = request.GET.get('curso_id')
    models = get_models()
    
    turmas = get_turmas_por_curso(curso_id, models)
    
    return JsonResponse({
        'turmas': [{'id': turma.id, 'nome': turma.nome} for turma in turmas]
    })

def ajax_dashboard_conteudo(request):
    """
    View AJAX para obter o conteúdo do dashboard filtrado.
    """
    models = get_models()
    AtividadeAcademica = models['AtividadeAcademica']
    
    # Obtém os filtros
    curso_id = request.GET.get('curso')
    turma_id = request.GET.get('turma')
    periodo = request.GET.get('periodo', 'mes')
    
    # Inicializa o queryset com todas as atividades
    atividades = AtividadeAcademica.objects.all().select_related('curso').prefetch_related('turmas')
    
    # Aplica filtros
    if curso_id:
        atividades = atividades.filter(curso_id=curso_id)
    
    if turma_id:
        atividades = atividades.filter(turmas__id=turma_id)
    
    # Filtra por período
    hoje = timezone.now().date()
    if periodo == 'semana':
        inicio_periodo = hoje - timezone.timedelta(days=hoje.weekday())
        fim_periodo = inicio_periodo + timezone.timedelta(days=6)
    elif periodo == 'mes':
        inicio_periodo = hoje.replace(day=1)
        if hoje.month == 12:
            fim_periodo = hoje.replace(year=hoje.year + 1, month=1, day=1) - timezone.timedelta(days=1)
        else:
            fim_periodo = hoje.replace(month=hoje.month + 1, day=1) - timezone.timedelta(days=1)
    elif periodo == 'trimestre':
        mes_atual = hoje.month
        trimestre_inicio = ((mes_atual - 1) // 3) * 3 + 1
        inicio_periodo = hoje.replace(month=trimestre_inicio, day=1)
        if trimestre_inicio + 2 > 12:
            fim_periodo = hoje.replace(year=hoje.year + 1, month=(trimestre_inicio + 2) % 12 + 1, day=1) - timezone.timedelta(days=1)
        else:
            fim_periodo = hoje.replace(month=trimestre_inicio + 3, day=1) - timezone.timedelta(days=1)
    else:  # ano
        inicio_periodo = hoje.replace(month=1, day=1)
        fim_periodo = hoje.replace(month=12, day=31)
    
    # Filtra atividades no período
    atividades_periodo = atividades.filter(
        Q(data_inicio__range=(inicio_periodo, fim_periodo)) | 
        Q(data_fim__range=(inicio_periodo, fim_periodo))
    )
    
    # Estatísticas para o dashboard
    total_atividades = atividades_periodo.count()
    atividades_por_status = atividades_periodo.values('status').annotate(
        total=Count('id')
    ).order_by('status')
    
    # Atividades por tipo
    atividades_por_tipo = atividades_periodo.values('tipo_atividade').annotate(
        total=Count('id')
    ).order_by('tipo_atividade')
    
    # Próximas atividades
    proximas_atividades = atividades.filter(
        data_inicio__gte=hoje
    ).order_by('data_inicio', 'hora_inicio')[:5]
    
    # Prepara dados para gráficos
    labels_status = [dict(AtividadeAcademica.STATUS_CHOICES).get(item['status']) for item in atividades_por_status]
    dados_status = [item['total'] for item in atividades_por_status]
    
    labels_tipo = [dict(AtividadeAcademica.TIPO_CHOICES).get(item['tipo_atividade']) for item in atividades_por_tipo]
    dados_tipo = [item['total'] for item in atividades_por_tipo]
    
    from django.template.loader import render_to_string
    
    context = {
        'total_atividades': total_atividades,
        'atividades_por_status': atividades_por_status,
        'atividades_por_tipo': atividades_por_tipo,
        'proximas_atividades': proximas_atividades,
        'periodo': {
            'inicio': inicio_periodo,
            'fim': fim_periodo,
            'nome': dict(PERIODO_CHOICES).get(periodo, 'Personalizado')
        },
        'graficos': {
            'status': {
                'labels': labels_status,
                'dados': dados_status
            },
            'tipo': {
                'labels': labels_tipo,
                'dados': dados_tipo
            }
        }
    }
    
    html = render_to_string(
        'atividades/partials/dashboard_conteudo.html',
        context,
        request=request
    )
    
    return JsonResponse({
        'html': html,
        'graficos': context['graficos']
    })

# Constantes para escolha de período
PERIODO_CHOICES = [
    ('semana', 'Semana atual'),
    ('mes', 'Mês atual'),
    ('trimestre', 'Trimestre atual'),
    ('ano', 'Ano atual')
]



### Arquivo: views\relatorios.py

python
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Q

from ..utils import get_models
from .utils import get_turmas_por_curso, aplicar_filtros_atividade
  def relatorio_atividades_curso_turma(request):
      """
      View para relatório de atividades por curso/turma.
      """
      models = get_models()
      AtividadeAcademica = models['AtividadeAcademica']
      Curso = models['Curso']
    
      cursos = Curso.objects.all().order_by('nome')
    
      # Inicializa o queryset com todas as atividades
      atividades = AtividadeAcademica.objects.all().select_related('curso').prefetch_related('turmas')
    
      # Aplica filtros
      curso_id = request.GET.get('curso')
      turma_id = request.GET.get('turma')
      q = request.GET.get('q')
    
      if curso_id:
          atividades = atividades.filter(curso_id=curso_id)
    
      if turma_id:
          atividades = atividades.filter(turmas__id=turma_id)
    
      if q:
          atividades = atividades.filter(
              Q(nome__icontains=q) | Q(descricao__icontains=q)
          )
    
      # Ordena as atividades
      atividades = atividades.order_by('-data_inicio', 'hora_inicio')
    
      # Estatísticas para o relatório
      total_atividades = atividades.count()
      atividades_por_status = atividades.values('status').annotate(
          total=Count('id')
      ).order_by('status')
    
      context = {
          'cursos': cursos,
          'atividades': atividades,
          'total_atividades': total_atividades,
          'atividades_por_status': atividades_por_status,
          'filtros': {
              'curso_id': curso_id,
              'turma_id': turma_id,
              'q': q
          }
      }
    
      # Se for uma requisição AJAX, retorna apenas o HTML do relatório
      if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
          from django.template.loader import render_to_string
          html = render_to_string(
              'atividades/partials/relatorio_atividades_body.html',
              context,
              request=request
          )
          return JsonResponse({'html': html})
    
      return render(request, 'atividades/relatorio_atividades_curso_turma.html', context)


  def ajax_turmas_por_curso_relatorio(request):
      """
      View AJAX para obter turmas por curso para o relatório.
      Reutiliza a função utilitária get_turmas_por_curso.
      """
      curso_id = request.GET.get('curso_id')
      models = get_models()
    
      turmas = get_turmas_por_curso(curso_id, models)
    
      return JsonResponse({
          'turmas': [{'id': turma.id, 'nome': turma.nome} for turma in turmas]
      })


  def ajax_atividades_filtradas_relatorio(request):
      """
      View AJAX para obter atividades filtradas para o relatório.
      """
      # Esta função pode ser removida, pois sua funcionalidade foi incorporada
      # na função relatorio_atividades_curso_turma com suporte a AJAX
      return relatorio_atividades_curso_turma(request)
    # Inicializa o queryset com todas as atividades



### Arquivo: views\ritualisticas.py

python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q

from ..forms import AtividadeRitualisticaForm
from ..utils import get_models
from .utils import aplicar_filtros_atividade, responder_ajax_filtro

def listar_atividades_ritualisticas(request):
    """
    View para listar atividades ritualísticas com filtros.
    """
    models = get_models()
    AtividadeRitualistica = models['AtividadeRitualistica']
    
    # Inicializa o queryset com todas as atividades
    atividades = AtividadeRitualistica.objects.all().prefetch_related('participantes')
    
    # Aplica filtro de busca simples
    q = request.GET.get('q', '')
    if q:
        atividades = atividades.filter(
            Q(nome__icontains=q) | Q(descricao__icontains=q)
        )
    
    # Ordena as atividades
    atividades = atividades.order_by('-data', 'hora_inicio')
    
    context = {
        'atividades': atividades,
        'q': q,
    }
    
    # Se for uma requisição AJAX, retorna apenas o HTML da tabela
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return responder_ajax_filtro(
            request, 
            atividades, 
            'atividades/ritualisticas/partials/atividades_tabela_body.html'
        )
    
    return render(request, 'atividades/ritualisticas/listar_atividades_ritualisticas.html', context)

# Restante das funções para criar, editar, detalhar e excluir atividades ritualísticas...



### Arquivo: views\utils.py

python
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string

def aplicar_filtros_atividade(queryset, filtro_form):
    """
    Função utilitária para aplicar filtros a um queryset de atividades.
    
    Args:
        queryset: O queryset base de atividades
        filtro_form: O formulário de filtro validado
        
    Returns:
        QuerySet: O queryset filtrado
    """
    if filtro_form.is_valid():
        # Filtro por texto (nome ou descrição)
        q = filtro_form.cleaned_data.get('q')
        if q:
            queryset = queryset.filter(
                Q(nome__icontains=q) | Q(descricao__icontains=q)
            )
        
        # Filtro por curso
        curso = filtro_form.cleaned_data.get('curso')
        if curso:
            queryset = queryset.filter(curso=curso)
        
        # Filtro por turma
        turma = filtro_form.cleaned_data.get('turma')
        if turma:
            queryset = queryset.filter(turmas=turma)
    
    return queryset

def get_turmas_por_curso(curso_id, models):
    """
    Função utilitária para obter turmas por curso.
    
    Args:
        curso_id: ID do curso
        models: Dicionário com os modelos necessários
        
    Returns:
        QuerySet: Queryset de turmas filtradas por curso
    """
    Turma = models['Turma']
    
    if curso_id:
        return Turma.objects.filter(curso_id=curso_id).order_by('nome')
    else:
        return Turma.objects.all().order_by('nome')

def responder_ajax_filtro(request, queryset, template_partial, context_extra=None):
    """
    Função utilitária para responder a requisições AJAX de filtro.
    
    Args:
        request: O objeto request
        queryset: O queryset filtrado
        template_partial: O caminho para o template parcial
        context_extra: Contexto adicional para o template (opcional)
        
    Returns:
        JsonResponse: Resposta JSON com o HTML renderizado
    """
    context = {'atividades': queryset}
    if context_extra:
        context.update(context_extra)
    
    html = render_to_string(
        template_partial,
        context,
        request=request
    )
    
    return JsonResponse({'html': html})

