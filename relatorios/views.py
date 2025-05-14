from django.shortcuts import render, get_object_or_404, redirect
from .models import Relatorio
from .forms import RelatorioForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from importlib import import_module
from django.utils import timezone
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)


def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_presenca_model():
    """Obtém o modelo Presenca dinamicamente."""
    try:
        presencas_module = import_module("presencas.models")
        return getattr(presencas_module, "Presenca")
    except (ImportError, AttributeError):
        return None


def get_punicao_model():
    """Obtém o modelo Punicao dinamicamente."""
    try:
        punicoes_module = import_module("punicoes.models")
        return getattr(punicoes_module, "Punicao")
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
def relatorio_punicoes(request):
    """Gera um relatório de punições com filtros."""
    try:
        Punicao = get_punicao_model()
        Aluno = get_aluno_model()
        
        if not Punicao:
            return render(
                request, 
                "relatorios/relatorio_punicoes.html", 
                {"erro": "Módulo de punições não disponível"}
            )
        
        # Obter parâmetros de filtro
        aluno_id = request.GET.get('aluno', '')
        tipo_punicao = request.GET.get('tipo_punicao', '')
        data_inicio = request.GET.get('data_inicio', '')
        data_fim = request.GET.get('data_fim', '')
        
        # Obter todos os alunos para o filtro
        alunos = Aluno.objects.all().order_by('nome')
        
        # Obter todos os tipos de punição para o filtro
        tipos_punicao = Punicao.objects.values_list('tipo_punicao', flat=True).distinct()
        
        # Filtrar punições
        punicoes = Punicao.objects.all().order_by('-data')
        
        if aluno_id:
            punicoes = punicoes.filter(aluno_id=aluno_id)
        
        if tipo_punicao:
            punicoes = punicoes.filter(tipo_punicao=tipo_punicao)
        
        if data_inicio and data_fim:
            punicoes = punicoes.filter(data__range=[data_inicio, data_fim])
        elif data_inicio:
            punicoes = punicoes.filter(data__gte=data_inicio)
        elif data_fim:
            punicoes = punicoes.filter(data__lte=data_fim)
        
        return render(
            request, 
            "relatorios/relatorio_punicoes.html", 
            {
                "punicoes": punicoes,
                "alunos": alunos,
                "tipos_punicao": tipos_punicao,
                "aluno_id": aluno_id,
                "tipo_punicao": tipo_punicao,
                "data_inicio": data_inicio,
                "data_fim": data_fim
            }
        )
    except Exception as e:
        logger.error(f"Erro ao gerar relatório de punições: {str(e)}")
        return render(
            request, 
            "relatorios/relatorio_punicoes.html", 
            {"erro": f"Erro ao gerar relatório: {str(e)}"}
        )


@login_required
def relatorio_alunos_pdf(request):
    """Gera um relatório de alunos em PDF."""
    try:
        # Importar biblioteca para geração de PDF
        from django.template.loader import get_template
        from xhtml2pdf import pisa
        from io import BytesIO
        
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
        from io import BytesIO
        
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
def relatorio_punicoes_pdf(request):
    """Gera um relatório de punições em PDF."""
    try:
        # Importar biblioteca para geração de PDF
        from django.template.loader import get_template
        from xhtml2pdf import pisa
        from io import BytesIO
        
        # Obter os mesmos parâmetros de filtro que na view relatorio_punicoes
        aluno_id = request.GET.get('aluno', '')
        tipo_punicao = request.GET.get('tipo_punicao', '')
        data_inicio = request.GET.get('data_inicio', '')
        data_fim = request.GET.get('data_fim', '')
        
        # Filtrar punições (mesmo código da view relatorio_punicoes)
        Punicao = get_punicao_model()
        Aluno = get_aluno_model()
        
        if not Punicao:
            return HttpResponse('Módulo de punições não disponível', status=404)
        
        punicoes = Punicao.objects.all().order_by('-data')
        
        if aluno_id:
            punicoes = punicoes.filter(aluno_id=aluno_id)
        
        if tipo_punicao:
            punicoes = punicoes.filter(tipo_punicao=tipo_punicao)
        
        if data_inicio and data_fim:
            punicoes = punicoes.filter(data__range=[data_inicio, data_fim])
        elif data_inicio:
            punicoes = punicoes.filter(data__gte=data_inicio)
        elif data_fim:
            punicoes = punicoes.filter(data__lte=data_fim)
        
        # Renderizar o template para HTML
        template = get_template('relatorios/relatorio_punicoes_pdf.html')
        html = template.render({
            'punicoes': punicoes,
            'aluno': Aluno.objects.get(id=aluno_id) if aluno_id else None,
            'tipo_punicao': tipo_punicao,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'data_geracao': timezone.now(),
        })
        
        # Criar resposta HTTP com PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_punicoes.pdf"'
        
        # Gerar PDF
        pdf_status = pisa.CreatePDF(
            html, dest=response)
        
        if pdf_status.err:
            return HttpResponse('Erro ao gerar PDF', status=500)
        
        return response
    except Exception as e:
        logger.error(f"Erro ao gerar PDF de punições: {str(e)}")
        return HttpResponse(f"Erro ao gerar PDF: {str(e)}", status=500)