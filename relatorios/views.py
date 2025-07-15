from django.shortcuts import render, get_object_or_404, redirect
from .models import Relatorio
from .forms import RelatorioForm
from django.contrib.auth.decorators import login_required
from importlib import import_module
from django.utils import timezone
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)


def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

def get_registro_historico_model():
    """Obtém o modelo RegistroHistorico dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "RegistroHistorico")

def get_tipo_codigo_model():
    """Obtém o modelo TipoCodigo dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "TipoCodigo")

def get_codigo_model():
    """Obtém o modelo Codigo dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Codigo")


def get_presenca_model():
    """Obtém o modelo Presenca dinamicamente."""
    try:
        presencas_module = import_module("presencas.models")
        return getattr(presencas_module, "Presenca")
    except (ImportError, AttributeError):
        return None


def get_turma_model():
    """Obtém o modelo Turma dinamicamente."""
    try:
        turmas_module = import_module("turmas.models")
        return getattr(turmas_module, "Turma")
    except (ImportError, AttributeError):
        return None


def get_curso_model():
    """Obtém o modelo Curso dinamicamente."""
    try:
        cursos_module = import_module("cursos.models")
        return getattr(cursos_module, "Curso")
    except (ImportError, AttributeError):
        return None


def get_atividade_academica_model():
    """Obtém o modelo AtividadeAcademica dinamicamente."""
    try:
        atividades_module = import_module("atividades.models")
        return getattr(atividades_module, "AtividadeAcademica")
    except (ImportError, AttributeError):
        return None


@login_required
def listar_relatorios(request):
    """Lista todos os relatórios disponíveis."""
    relatorios = Relatorio.objects.all().order_by('-data_criacao')
    return render(
        request,
        "relatorios/listar_relatorios.html",
        {"relatorios": relatorios},
    )


@login_required
def detalhar_relatorio(request, relatorio_id):
    """Exibe os detalhes de um relatório específico."""
    relatorio = get_object_or_404(Relatorio, id=relatorio_id)
    return render(
        request, "relatorios/detalhar_relatorio.html", {"relatorio": relatorio}
    )


@login_required
def criar_relatorio(request):
    """Cria um novo relatório."""
    if request.method == "POST":
        form = RelatorioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("relatorios:listar_relatorios")
    else:
        form = RelatorioForm()
    return render(request, "relatorios/form_relatorio.html", {"form": form})


@login_required
def editar_relatorio(request, relatorio_id):
    """Edita um relatório existente."""
    relatorio = get_object_or_404(Relatorio, id=relatorio_id)
    if request.method == "POST":
        form = RelatorioForm(request.POST, instance=relatorio)
        if form.is_valid():
            form.save()
            return redirect("relatorios:listar_relatorios")
    else:
        form = RelatorioForm(instance=relatorio)
    return render(request, "relatorios/form_relatorio.html", {"form": form})


@login_required
def excluir_relatorio(request, relatorio_id):
    """Exclui um relatório."""
    relatorio = get_object_or_404(Relatorio, id=relatorio_id)
    if request.method == "POST":
        relatorio.delete()
        return redirect("relatorios:listar_relatorios")
    return render(
        request, "relatorios/confirmar_exclusao.html", {"relatorio": relatorio}
    )


@login_required
def relatorio_alunos(request):
    """Gera um relatório de alunos com filtros."""
    try:
        Aluno = get_aluno_model()
        
        # Obter parâmetros de filtro
        nome = request.GET.get('nome', '')
        data_inicio = request.GET.get('data_inicio', '')
        data_fim = request.GET.get('data_fim', '')
        
        # Filtrar alunos
        alunos = Aluno.objects.all()
        
        if nome:
            alunos = alunos.filter(nome__icontains=nome)
        
        if data_inicio and data_fim:
            alunos = alunos.filter(data_nascimento__range=[data_inicio, data_fim])
        elif data_inicio:
            alunos = alunos.filter(data_nascimento__gte=data_inicio)
        elif data_fim:
            alunos = alunos.filter(data_nascimento__lte=data_fim)
        
        return render(
            request, 
            "relatorios/relatorio_alunos.html", 
            {
                "alunos": alunos,
                "nome": nome,
                "data_inicio": data_inicio,
                "data_fim": data_fim
            }
        )
    except Exception as e:
        logger.error(f"Erro ao gerar relatório de alunos: {str(e)}")
        return render(
            request, 
            "relatorios/relatorio_alunos.html", 
            {"erro": f"Erro ao gerar relatório: {str(e)}"}
        )


@login_required
def relatorio_presencas(request):
    """Gera um relatório de presenças com filtros."""
    try:
        Presenca = get_presenca_model()
        Aluno = get_aluno_model()
        
        if not Presenca:
            return render(
                request, 
                "relatorios/relatorio_presencas.html", 
                {"erro": "Módulo de presenças não disponível"}
            )
        
        # Obter parâmetros de filtro
        aluno_id = request.GET.get('aluno', '')
        data_inicio = request.GET.get('data_inicio', '')
        data_fim = request.GET.get('data_fim', '')
        
        # Obter todos os alunos para o filtro
        alunos = Aluno.objects.all().order_by('nome')
        
        # Filtrar presenças
        presencas = Presenca.objects.all().order_by('-data')
        
        if aluno_id:
            presencas = presencas.filter(aluno_id=aluno_id)
        
        if data_inicio and data_fim:
            presencas = presencas.filter(data__range=[data_inicio, data_fim])
        elif data_inicio:
            presencas = presencas.filter(data__gte=data_inicio)
        elif data_fim:
            presencas = presencas.filter(data__lte=data_fim)
        
        return render(
            request, 
            "relatorios/relatorio_presencas.html", 
            {
                "presencas": presencas,
                "alunos": alunos,
                "aluno_id": aluno_id,
                "data_inicio": data_inicio,
                "data_fim": data_fim
            }
        )
    except Exception as e:
        logger.error(f"Erro ao gerar relatório de presenças: {str(e)}")
        return render(
            request, 
            "relatorios/relatorio_presencas.html", 
            {"erro": f"Erro ao gerar relatório: {str(e)}"}
        )


@login_required
def relatorio_historico(request):
    """Gera um relatório do histórico dos alunos com filtros."""
    RegistroHistorico = get_registro_historico_model()
    Aluno = get_aluno_model()
    TipoCodigo = get_tipo_codigo_model()
    Codigo = get_codigo_model()

    # Obter parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    tipo_codigo_id = request.GET.get('tipo_codigo', '')
    codigo_id = request.GET.get('codigo', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    # Filtrar registros
    registros = RegistroHistorico.objects.select_related('aluno', 'codigo', 'codigo__tipo_codigo').all()

    if aluno_id:
        registros = registros.filter(aluno_id=aluno_id)
    if tipo_codigo_id:
        registros = registros.filter(codigo__tipo_codigo_id=tipo_codigo_id)
    if codigo_id:
        registros = registros.filter(codigo_id=codigo_id)
    if data_inicio:
        registros = registros.filter(data_os__gte=data_inicio)
    if data_fim:
        registros = registros.filter(data_os__lte=data_fim)

    context = {
        'registros': registros.order_by('-data_os'),
        'alunos': Aluno.objects.all().order_by('nome'),
        'tipos_codigo': TipoCodigo.objects.all().order_by('nome'),
        'codigos': Codigo.objects.all().order_by('nome'),
        'aluno_selecionado': aluno_id,
        'tipo_codigo_selecionado': tipo_codigo_id,
        'codigo_selecionado': codigo_id,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    return render(request, "relatorios/relatorio_historico.html", context)


@login_required
def relatorio_alunos_pdf(request):
    """Gera um relatório de alunos em PDF."""
    try:
        # Importar biblioteca para geração de PDF
        from django.template.loader import get_template
        from xhtml2pdf import pisa
        
        # Obter os mesmos parâmetros de filtro que na view relatorio_alunos
        nome = request.GET.get('nome', '')
        data_inicio = request.GET.get('data_inicio', '')
        data_fim = request.GET.get('data_fim', '')
        
        # Filtrar alunos (mesmo código da view relatorio_alunos)
        Aluno = get_aluno_model()
        alunos = Aluno.objects.all()
        
        if nome:
            alunos = alunos.filter(nome__icontains=nome)
        
        if data_inicio and data_fim:
            alunos = alunos.filter(data_nascimento__range=[data_inicio, data_fim])
        elif data_inicio:
            alunos = alunos.filter(data_nascimento__gte=data_inicio)
        elif data_fim:
            alunos = alunos.filter(data_nascimento__lte=data_fim)
        
        # Renderizar o template para HTML
        template = get_template('relatorios/relatorio_alunos_pdf.html')
        html = template.render({
            'alunos': alunos,
            'nome': nome,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'data_geracao': timezone.now(),
        })
        
        # Criar resposta HTTP com PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_alunos.pdf"'
        
        # Gerar PDF
        pdf_status = pisa.CreatePDF(
            html, dest=response)
        
        if pdf_status.err:
            return HttpResponse('Erro ao gerar PDF', status=500)
        
        return response
    except Exception as e:
        logger.error(f"Erro ao gerar PDF de alunos: {str(e)}")
        return HttpResponse(f"Erro ao gerar PDF: {str(e)}", status=500)
@login_required
def relatorio_presencas_pdf(request):
    """Gera um relatório de presenças em PDF."""
    try:
        # Importar biblioteca para geração de PDF
        from django.template.loader import get_template
        from xhtml2pdf import pisa
        
        # Obter os mesmos parâmetros de filtro que na view relatorio_presencas
        aluno_id = request.GET.get('aluno', '')
        data_inicio = request.GET.get('data_inicio', '')
        data_fim = request.GET.get('data_fim', '')
        
        # Filtrar presenças (mesmo código da view relatorio_presencas)
        Presenca = get_presenca_model()
        Aluno = get_aluno_model()
        
        if not Presenca:
            return HttpResponse('Módulo de presenças não disponível', status=404)
        
        presencas = Presenca.objects.all().order_by('-data')
        
        if aluno_id:
            presencas = presencas.filter(aluno_id=aluno_id)
        
        if data_inicio and data_fim:
            presencas = presencas.filter(data__range=[data_inicio, data_fim])
        elif data_inicio:
            presencas = presencas.filter(data__gte=data_inicio)
        elif data_fim:
            presencas = presencas.filter(data__lte=data_fim)
        
        # Renderizar o template para HTML
        template = get_template('relatorios/relatorio_presencas_pdf.html')
        html = template.render({
            'presencas': presencas,
            'aluno': Aluno.objects.get(id=aluno_id) if aluno_id else None,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'data_geracao': timezone.now(),
        })
        
        # Criar resposta HTTP com PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_presencas.pdf"'
        
        # Gerar PDF
        pdf_status = pisa.CreatePDF(
            html, dest=response)
        
        if pdf_status.err:
            return HttpResponse('Erro ao gerar PDF', status=500)
        
        return response
    except Exception as e:
        logger.error(f"Erro ao gerar PDF de presenças: {str(e)}")
        return HttpResponse(f"Erro ao gerar PDF: {str(e)}", status=500)
@login_required
def relatorio_historico_pdf(request):
    """Gera um relatório de histórico em PDF."""
    from django.template.loader import get_template
    from xhtml2pdf import pisa

    RegistroHistorico = get_registro_historico_model()
    Aluno = get_aluno_model()
    TipoCodigo = get_tipo_codigo_model()
    Codigo = get_codigo_model()

    # Obter os mesmos parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    tipo_codigo_id = request.GET.get('tipo_codigo', '')
    codigo_id = request.GET.get('codigo', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    # Filtrar registros (mesma lógica da view HTML)
    registros = RegistroHistorico.objects.select_related('aluno', 'codigo', 'codigo__tipo_codigo').all()

    if aluno_id:
        registros = registros.filter(aluno_id=aluno_id)
    if tipo_codigo_id:
        registros = registros.filter(codigo__tipo_codigo_id=tipo_codigo_id)
    if codigo_id:
        registros = registros.filter(codigo_id=codigo_id)
    if data_inicio:
        registros = registros.filter(data_os__gte=data_inicio)
    if data_fim:
        registros = registros.filter(data_os__lte=data_fim)

    # Renderizar o template para HTML
    template = get_template('relatorios/relatorio_historico_pdf.html')
    context = {
        'registros': registros.order_by('-data_os'),
        'data_geracao': timezone.now(),
        'aluno': Aluno.objects.get(id=aluno_id) if aluno_id else None,
        'tipo_codigo': TipoCodigo.objects.get(id=tipo_codigo_id) if tipo_codigo_id else None,
        'codigo': Codigo.objects.get(id=codigo_id) if codigo_id else None,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    
    try:
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_historico.pdf"'
        pdf_status = pisa.CreatePDF(html, dest=response)
        if pdf_status.err:
            return HttpResponse('Erro ao gerar PDF', status=500)
        return response
    except Exception as e:
        logger.error(f"Erro ao gerar PDF de histórico: {str(e)}")
        return HttpResponse(f"Erro ao gerar PDF: {str(e)}", status=500)


@login_required
def relatorio_turmas(request):
    """Gera um relatório de turmas com filtros."""
    Turma = get_turma_model()
    Curso = get_curso_model()

    if not Turma or not Curso:
        return render(
            request,
            "relatorios/relatorio_turmas.html",
            {"erro": "Modelos de Turma ou Curso não encontrados."},
        )

    # Obter parâmetros de filtro
    curso_id = request.GET.get('curso', '')
    status = request.GET.get('status', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    # Filtrar turmas
    turmas = Turma.objects.select_related('curso').all()

    if curso_id:
        turmas = turmas.filter(curso_id=curso_id)

    if status:
        turmas = turmas.filter(status=status)

    if data_inicio:
        turmas = turmas.filter(data_inicio_ativ__gte=data_inicio)

    if data_fim:
        turmas = turmas.filter(data_termino_atividades__lte=data_fim)

    context = {
        'turmas': turmas.order_by('curso__nome', 'nome'),
        'cursos': Curso.objects.all().order_by('nome'),
        'status_choices': Turma.STATUS_CHOICES,
        'curso_selecionado': curso_id,
        'status_selecionado': status,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    return render(request, "relatorios/relatorio_turmas.html", context)


@login_required
def relatorio_turmas_pdf(request):
    """Gera um relatório de turmas em PDF."""
    from django.template.loader import get_template
    from xhtml2pdf import pisa

    Turma = get_turma_model()
    Curso = get_curso_model()

    if not Turma or not Curso:
        return HttpResponse("Modelos de Turma ou Curso não encontrados.", status=500)

    # Obter os mesmos parâmetros de filtro
    curso_id = request.GET.get('curso', '')
    status = request.GET.get('status', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    # Filtrar turmas (mesma lógica da view HTML)
    turmas = Turma.objects.select_related('curso').all()

    if curso_id:
        turmas = turmas.filter(curso_id=curso_id)
    if status:
        turmas = turmas.filter(status=status)
    if data_inicio:
        turmas = turmas.filter(data_inicio_ativ__gte=data_inicio)
    if data_fim:
        turmas = turmas.filter(data_termino_atividades__lte=data_fim)

    # Renderizar o template para HTML
    template = get_template('relatorios/relatorio_turmas_pdf.html')
    context = {
        'turmas': turmas.order_by('curso__nome', 'nome'),
        'data_geracao': timezone.now(),
        'curso': Curso.objects.get(id=curso_id) if curso_id else None,
        'status': dict(Turma.STATUS_CHOICES).get(status, '') if status else None,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    
    try:
        html = template.render(context)

        # Criar resposta HTTP com PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_turmas.pdf"'

        # Gerar PDF
        pdf_status = pisa.CreatePDF(html, dest=response)

        if pdf_status.err:
            return HttpResponse('Erro ao gerar PDF', status=500)

        return response
    except Exception as e:
        logger.error(f"Erro ao gerar PDF de turmas: {str(e)}")
        return HttpResponse(f"Erro ao gerar PDF: {str(e)}", status=500)

@login_required
def relatorio_atividades(request):
    """Gera um relatório de atividades acadêmicas com filtros."""
    AtividadeAcademica = get_atividade_academica_model()
    Turma = get_turma_model()

    if not AtividadeAcademica or not Turma:
        return render(
            request,
            "relatorios/relatorio_atividades.html",
            {"erro": "Modelos de Atividade ou Turma não encontrados."},
        )

    # Obter parâmetros de filtro
    tipo_atividade = request.GET.get('tipo_atividade', '')
    status = request.GET.get('status', '')
    turma_id = request.GET.get('turma', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    # Filtrar atividades
    atividades = AtividadeAcademica.objects.select_related('curso').prefetch_related('turmas').all()

    if tipo_atividade:
        atividades = atividades.filter(tipo_atividade=tipo_atividade)
    if status:
        atividades = atividades.filter(status=status)
    if turma_id:
        atividades = atividades.filter(turmas__id=turma_id)
    if data_inicio:
        atividades = atividades.filter(data_inicio__gte=data_inicio)
    if data_fim:
        atividades = atividades.filter(data_fim__lte=data_fim)

    context = {
        'atividades': atividades.order_by('-data_inicio'),
        'tipos_atividade': AtividadeAcademica.TIPO_CHOICES,
        'status_choices': AtividadeAcademica.STATUS_CHOICES,
        'turmas': Turma.objects.all().order_by('nome'),
        'tipo_selecionado': tipo_atividade,
        'status_selecionado': status,
        'turma_selecionada': turma_id,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    return render(request, "relatorios/relatorio_atividades.html", context)


@login_required
def relatorio_atividades_pdf(request):
    """Gera um relatório de atividades acadêmicas em PDF."""
    from django.template.loader import get_template
    from xhtml2pdf import pisa

    AtividadeAcademica = get_atividade_academica_model()
    Turma = get_turma_model()

    if not AtividadeAcademica or not Turma:
        return HttpResponse("Modelos não encontrados.", status=500)

    # Obter parâmetros de filtro
    tipo_atividade = request.GET.get('tipo_atividade', '')
    status = request.GET.get('status', '')
    turma_id = request.GET.get('turma', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    # Filtrar atividades
    atividades = AtividadeAcademica.objects.select_related('curso').prefetch_related('turmas').all()

    if tipo_atividade:
        atividades = atividades.filter(tipo_atividade=tipo_atividade)
    if status:
        atividades = atividades.filter(status=status)
    if turma_id:
        atividades = atividades.filter(turmas__id=turma_id)
    if data_inicio:
        atividades = atividades.filter(data_inicio__gte=data_inicio)
    if data_fim:
        atividades = atividades.filter(data_fim__lte=data_fim)

    # Renderizar o template para HTML
    template = get_template('relatorios/relatorio_atividades_pdf.html')
    context = {
        'atividades': atividades.order_by('-data_inicio'),
        'data_geracao': timezone.now(),
        'tipo_selecionado': dict(AtividadeAcademica.TIPO_CHOICES).get(tipo_atividade, ''),
        'status_selecionado': dict(AtividadeAcademica.STATUS_CHOICES).get(status, ''),
        'turma_selecionada': Turma.objects.get(id=turma_id) if turma_id else None,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    html = template.render(context)

    try:
        # Criar resposta HTTP com PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_atividades.pdf"'

        # Gerar PDF
        pdf_status = pisa.CreatePDF(html, dest=response)

        if pdf_status.err:
            return HttpResponse('Erro ao gerar PDF', status=500)

        return response
    except Exception as e:
        logger.error(f"Erro ao gerar PDF de atividades: {str(e)}")
        return HttpResponse(f"Erro ao gerar PDF: {str(e)}", status=500)