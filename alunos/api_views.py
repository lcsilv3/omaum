"""Views dedicadas a endpoints de API do aplicativo Alunos."""

import csv
import json
import logging
import traceback
from datetime import date, datetime, timedelta
from io import BytesIO

from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
from django.views.decorators.http import require_GET, require_http_methods
from importlib import import_module
from rest_framework import viewsets

from .models import Aluno, RegistroHistorico
from .serializers import AlunoSerializer
from .services import HistoricoService, HistoricoValidationError, InstrutorService

try:
    import xlwt
except ImportError:  # pragma: no cover - dependência opcional
    xlwt = None

logger = logging.getLogger(__name__)


def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


@require_GET
def search_alunos(request):
    """API para buscar alunos por nome, CPF ou número iniciático."""

    query = request.GET.get("q", "").strip()
    if len(query) < 2:
        return JsonResponse([], safe=False)

    AlunoModel = get_aluno_model()
    alunos = AlunoModel.objects.filter(nome__icontains=query)[:10]

    resultados = []
    for aluno in alunos:
        resultados.append(
            {
                "cpf": aluno.cpf,
                "nome": aluno.nome,
                "email": aluno.email or "N/A",
                "foto": aluno.foto.url if getattr(aluno, "foto", None) else None,
            }
        )

    return JsonResponse(resultados, safe=False)


@login_required
def search_instrutores(request):
    """Busca alunos elegíveis para assumirem papel de instrutor."""

    try:
        query = request.GET.get("q", "").strip()
        AlunoModel = get_aluno_model()
        alunos = AlunoModel.objects.filter(situacao="ATIVO")

        if query and len(query) >= 2:
            alunos = alunos.filter(Q(nome__icontains=query) | Q(cpf__icontains=query))

        alunos = alunos[:10]

        resultados = []
        for aluno in alunos:
            resultados.append(
                {
                    "cpf": aluno.cpf,
                    "nome": aluno.nome,
                    "foto": aluno.foto.url if getattr(aluno, "foto", None) else None,
                    "situacao": aluno.get_situacao_display()
                    if hasattr(aluno, "get_situacao_display")
                    else "",
                    "situacao_codigo": aluno.situacao,
                    "esta_ativo": getattr(aluno, "esta_ativo", False),
                    "elegivel": getattr(aluno, "pode_ser_instrutor", True),
                }
            )

        logger.info(
            "Busca de instrutores por '%s' retornou %s resultados",
            query,
            len(resultados),
        )
        return JsonResponse(resultados, safe=False)
    except Exception as exc:  # pragma: no cover - proteção adicional
        logger.error("Erro em search_instrutores: %s", exc)
        return JsonResponse({"error": str(exc)}, status=500)


@login_required
def get_aluno(request, cpf):
    """Retorna dados resumidos de um aluno específico."""

    try:
        AlunoModel = get_aluno_model()
        aluno = get_object_or_404(AlunoModel, cpf=cpf)
        return JsonResponse(
            {
                "success": True,
                "aluno": {
                    "cpf": aluno.cpf,
                    "nome": aluno.nome,
                    "foto": aluno.foto.url if getattr(aluno, "foto", None) else None,
                },
            }
        )
    except Exception as exc:  # pragma: no cover - caminho excepcional
        return JsonResponse({"success": False, "error": str(exc)}, status=404)


@login_required
def get_aluno_detalhes(request, cpf):
    """Exibe informações adicionais e vínculos de um aluno."""

    AlunoModel = get_aluno_model()

    try:
        aluno = AlunoModel.objects.get(cpf=cpf)

        turmas_como_instrutor = False
        try:
            Turma = import_module("turmas.models").Turma
            turmas_como_instrutor = Turma.objects.filter(
                Q(instrutor=aluno)
                | Q(instrutor_auxiliar=aluno)
                | Q(auxiliar_instrucao=aluno)
            ).exists()
        except Exception as exc:  # pragma: no cover - dependência externa
            logger.error("Erro ao verificar turmas como instrutor: %s", exc)

        turmas_matriculado = []
        try:
            Matricula = import_module("matriculas.models").Matricula
            matriculas = Matricula.objects.filter(aluno=aluno, status="A")
            turmas_matriculado = [
                {
                    "id": matricula.turma.id,
                    "nome": matricula.turma.nome,
                    "curso": matricula.turma.curso.nome
                    if matricula.turma and matricula.turma.curso
                    else "Sem curso",
                }
                for matricula in matriculas
            ]
        except Exception as exc:  # pragma: no cover - dependência externa
            logger.error("Erro ao buscar matrículas: %s", exc)

        resposta = JsonResponse(
            {
                "success": True,
                "e_instrutor": turmas_como_instrutor,
                "turmas": turmas_matriculado,
                "pode_ser_instrutor": getattr(aluno, "pode_ser_instrutor", False),
            }
        )
        return resposta
    except AlunoModel.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Aluno não encontrado"}, status=404
        )
    except Exception as exc:  # pragma: no cover - caminho excepcional
        logger.error("Erro ao obter detalhes do aluno: %s", exc, exc_info=True)
        return JsonResponse({"success": False, "error": str(exc)}, status=500)


@login_required
@permission_required("alunos.view_aluno", raise_exception=True)
def verificar_elegibilidade_endpoint(request, cpf):
    """API endpoint para verificar se um aluno pode ser instrutor."""
    try:
        AlunoModel = get_aluno_model()
        aluno = get_object_or_404(AlunoModel, cpf=cpf)

        if aluno.situacao != "ATIVO":
            return JsonResponse(
                {
                    "elegivel": False,
                    "motivo": (
                        f"O aluno não está ativo. "
                        f"Situação atual: {aluno.get_situacao_display()}"
                    ),
                }
            )

        try:
            resultado = InstrutorService.verificar_elegibilidade_completa(aluno)
            if "elegivel" not in resultado:
                resultado["elegivel"] = bool(resultado)
        except Exception as exc:  # pragma: no cover - serviço opcional
            logger.warning(
                "Falha ao consultar InstrutorService para o CPF %s: %s", cpf, exc
            )
            elegivel = getattr(aluno, "pode_ser_instrutor", True)
            resultado = {
                "elegivel": elegivel,
                "motivo": (
                    "O aluno não atende aos requisitos para ser instrutor."
                    if not elegivel
                    else ""
                ),
            }

        return JsonResponse(resultado)
    except Exception as exc:
        logger.error(
            "Erro ao verificar elegibilidade do aluno %s: %s", cpf, exc, exc_info=True
        )
        return JsonResponse(
            {
                "elegivel": False,
                "motivo": f"Erro na verificação: {str(exc)}",
                "trace": traceback.format_exc(),
            },
            status=500,
        )


class AlunoViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite que os alunos sejam visualizados ou editados.
    """

    queryset = Aluno.objects.all().order_by("nome")
    serializer_class = AlunoSerializer


@login_required
@permission_required("alunos.view_aluno", raise_exception=True)
def listar_historico_aluno_api(request, aluno_id):
    """
    API endpoint para listar o histórico de registros de um aluno, com paginação.
    """
    try:
        aluno = get_object_or_404(Aluno, pk=aluno_id)
        historico_list = HistoricoService.listar(aluno)

        page = request.GET.get("page", 1)
        # Garante que page_size seja inteiro
        page_size = int(request.GET.get("page_size", 25))

        paginator = Paginator(historico_list, page_size)
        try:
            historico_page = paginator.page(page)
        except PageNotAnInteger:
            historico_page = paginator.page(1)
        except EmptyPage:
            historico_page = paginator.page(paginator.num_pages)

        results = []
        for item in historico_page:
            codigo = getattr(item, "codigo", None)
            tipo_codigo = getattr(codigo, "tipo_codigo", None)

            results.append(
                {
                    "id": item.id,
                    "codigo_id": codigo.id if codigo else None,
                    "tipo_codigo": getattr(tipo_codigo, "nome", "N/A") or "N/A",
                    "codigo": getattr(codigo, "nome", None) or "N/A",
                    "descricao": getattr(codigo, "descricao", None) or "",
                    "data_os": item.data_os.isoformat() if item.data_os else None,
                    "ordem_servico": item.ordem_servico or "",
                    "observacoes": item.observacoes or "",
                    "ativo": item.ativo,
                    "created_at": item.created_at.isoformat()
                    if item.created_at
                    else None,
                }
            )

        return JsonResponse(
            {
                "status": "success",
                "results": results,
                "page": historico_page.number,
                "total_pages": paginator.num_pages,
                "count": paginator.count,
            }
        )
    except Exception as e:
        logger.error(
            f"Erro ao listar histórico do aluno {aluno_id}: {e}", exc_info=True
        )
        return JsonResponse(
            {"status": "error", "message": "Erro interno do servidor."}, status=500
        )


@login_required
@permission_required("alunos.add_registrohistorico", raise_exception=True)
@require_http_methods(["POST"])
def criar_historico_aluno_api(request, aluno_id):
    """Cria um novo registro histórico para o aluno informado."""

    aluno = get_object_or_404(Aluno, pk=aluno_id)

    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "status": "error",
                "message": "Payload inválido. Envie JSON bem formatado.",
            },
            status=400,
        )

    data_os_valor = payload.get("data_os")
    data_os = None
    if data_os_valor:
        try:
            data_os = datetime.fromisoformat(str(data_os_valor)).date()
        except ValueError:
            return JsonResponse(
                {
                    "status": "error",
                    "errors": {
                        "data_os": ["Data inválida. Utilize o formato ISO YYYY-MM-DD."]
                    },
                },
                status=400,
            )

    try:
        registro = HistoricoService.criar_evento(
            aluno,
            {
                "codigo_id": payload.get("codigo_id"),
                "data_os": data_os,
                "ordem_servico": payload.get("ordem_servico"),
                "observacoes": payload.get("observacoes"),
            },
        )
    except HistoricoValidationError as exc:
        # HistoricoValidationError pode expor message_dict ou messages
        erros = getattr(exc, "message_dict", None) or {"erros": exc.messages}
        return JsonResponse({"status": "error", "errors": erros}, status=400)
    except Exception as exc:  # pragma: no cover - falhas inesperadas
        logger.error(
            "Erro ao criar registro histórico para aluno %s: %s",
            aluno_id,
            exc,
            exc_info=True,
        )
        return JsonResponse(
            {
                "status": "error",
                "message": "Erro interno ao criar registro histórico.",
            },
            status=500,
        )

    codigo = getattr(registro, "codigo", None)
    tipo_codigo = getattr(codigo, "tipo_codigo", None)

    return JsonResponse(
        {
            "status": "success",
            "tipo_evento": getattr(tipo_codigo, "nome", None),
            "registro": {
                "id": registro.id,
                "codigo_id": codigo.id if codigo else None,
                "codigo_nome": getattr(codigo, "nome", None),
                "descricao": getattr(codigo, "descricao", None),
                "ordem_servico": registro.ordem_servico,
                "data_os": registro.data_os.isoformat() if registro.data_os else None,
                "observacoes": registro.observacoes,
            },
        },
        status=201,
    )


@login_required
@permission_required("alunos.change_registrohistorico", raise_exception=True)
@require_http_methods(["POST"])
def desativar_historico_aluno_api(request, aluno_id, registro_id):
    """Realiza o soft delete de um registro histórico do aluno."""

    aluno = get_object_or_404(Aluno, pk=aluno_id)
    registro = get_object_or_404(RegistroHistorico, pk=registro_id, aluno=aluno)

    motivo = None
    if request.body:
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
            motivo = payload.get("motivo")
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Payload inválido. Envie JSON bem formatado.",
                },
                status=400,
            )

    try:
        HistoricoService.desativar_evento(registro, motivo=motivo, atualizar_cache=True)
    except HistoricoValidationError as exc:
        erros = getattr(exc, "message_dict", None) or {"erros": exc.messages}
        return JsonResponse({"status": "error", "errors": erros}, status=400)
    except Exception as exc:  # pragma: no cover - falhas inesperadas
        logger.error(
            "Erro ao desativar registro histórico %s do aluno %s: %s",
            registro_id,
            aluno_id,
            exc,
            exc_info=True,
        )
        return JsonResponse(
            {
                "status": "error",
                "message": "Erro interno ao desativar registro histórico.",
            },
            status=500,
        )

    registro.refresh_from_db()
    return JsonResponse(
        {
            "status": "success",
            "registro": {
                "id": registro.id,
                "ativo": registro.ativo,
                "observacoes": registro.observacoes,
            },
        }
    )


@login_required
@permission_required("alunos.change_registrohistorico", raise_exception=True)
@require_http_methods(["POST"])
def reativar_historico_aluno_api(request, aluno_id, registro_id):
    """Reativa um registro histórico previamente desativado."""

    aluno = get_object_or_404(Aluno, pk=aluno_id)
    registro = get_object_or_404(RegistroHistorico, pk=registro_id, aluno=aluno)

    try:
        HistoricoService.reativar_evento(registro, atualizar_cache=True)
    except HistoricoValidationError as exc:
        erros = getattr(exc, "message_dict", None) or {"erros": exc.messages}
        return JsonResponse({"status": "error", "errors": erros}, status=400)
    except Exception as exc:  # pragma: no cover - falhas inesperadas
        logger.error(
            "Erro ao reativar registro histórico %s do aluno %s: %s",
            registro_id,
            aluno_id,
            exc,
            exc_info=True,
        )
        return JsonResponse(
            {
                "status": "error",
                "message": "Erro interno ao reativar registro histórico.",
            },
            status=500,
        )

    registro.refresh_from_db()
    return JsonResponse(
        {
            "status": "success",
            "registro": {
                "id": registro.id,
                "ativo": registro.ativo,
                "observacoes": registro.observacoes,
            },
        }
    )


@login_required
@require_GET
def painel_kpis_api(request):
    """Retorna os indicadores principais exibidos no painel de alunos."""

    total_alunos = Aluno.objects.count()
    alunos_ativos_qs = Aluno.objects.filter(situacao="a")
    alunos_ativos = alunos_ativos_qs.count()

    datas_nascimento = list(
        alunos_ativos_qs.filter(data_nascimento__isnull=False).values_list(
            "data_nascimento", flat=True
        )
    )
    if datas_nascimento:
        hoje = date.today()
        idades = [(hoje - data).days // 365 for data in datas_nascimento]
        media_idade = int(sum(idades) / len(idades))
    else:
        media_idade = "-"

    crit = Q(celular_primeiro_contato__isnull=False) & ~Q(celular_primeiro_contato="")
    crit &= Q(rua__isnull=False) & ~Q(rua="")
    crit &= Q(nome_primeiro_contato__isnull=False) & ~Q(nome_primeiro_contato="")
    completos = alunos_ativos_qs.filter(crit).count()

    total_ativos = alunos_ativos or 1
    qualidade = int((completos / total_ativos) * 100)

    return JsonResponse(
        {
            "total_alunos": total_alunos,
            "alunos_ativos": alunos_ativos,
            "media_idade": media_idade,
            "qualidade_dados": qualidade,
        }
    )


@login_required
@require_GET
def painel_graficos_api(request):
    """Agrupa dados para os gráficos do painel (situação e evolução mensal)."""

    situacoes = Aluno.objects.values("situacao").annotate(qtd=Count("id"))
    labels = []
    values = []
    mapa = dict(Aluno._meta.get_field("situacao").choices)
    for situacao in situacoes:
        labels.append(mapa.get(situacao["situacao"], situacao["situacao"]))
        values.append(situacao["qtd"])

    hoje = date.today()
    meses = [
        (hoje - timedelta(days=30 * i)).replace(day=1) for i in reversed(range(12))
    ]
    labels_mes = [mes.strftime("%b/%Y") for mes in meses]
    valores_mes = []
    for mes in meses:
        proximo = (mes + timedelta(days=32)).replace(day=1)
        valores_mes.append(
            Aluno.objects.filter(
                created_at__date__gte=mes, created_at__date__lt=proximo
            ).count()
        )

    return JsonResponse(
        {
            "situacao": {"labels": labels, "values": values},
            "novos_mes": {"labels": labels_mes, "values": valores_mes},
        }
    )


@login_required
@require_GET
def painel_tabela_api(request):
    """Retorna a tabela paginada dinâmica do painel de alunos ou exportações."""

    nome = request.GET.get("nome", "").strip()
    cpf = request.GET.get("cpf", "").strip()
    situacao = request.GET.get("situacao", "").strip()
    export = request.GET.get("export", "").strip()

    try:
        page = int(request.GET.get("page", 1))
    except (TypeError, ValueError):
        page = 1

    alunos_qs = Aluno.objects.all()
    if nome:
        alunos_qs = alunos_qs.filter(nome__icontains=nome)
    if cpf:
        alunos_qs = alunos_qs.filter(cpf__icontains=cpf)
    if situacao:
        alunos_qs = alunos_qs.filter(situacao=situacao)
    alunos_qs = alunos_qs.order_by("-id")

    if export in ["csv", "xls", "pdf"]:
        if export == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="alunos.csv"'
            writer = csv.writer(response)
            writer.writerow(["Nome", "CPF", "Email", "Situação"])
            for aluno in alunos_qs:
                writer.writerow(
                    [
                        smart_str(aluno.nome),
                        smart_str(aluno.cpf),
                        smart_str(aluno.email),
                        dict(Aluno.SITUACAO_CHOICES).get(aluno.situacao, "-"),
                    ]
                )
            return response

        if export == "xls":
            if not xlwt:
                return HttpResponse("Pacote xlwt não instalado.", status=500)
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet("Alunos")
            headers = ["Nome", "CPF", "Email", "Situação"]
            for col, header in enumerate(headers):
                sheet.write(0, col, header)
            for row, aluno in enumerate(alunos_qs, start=1):
                sheet.write(row, 0, smart_str(aluno.nome))
                sheet.write(row, 1, smart_str(aluno.cpf))
                sheet.write(row, 2, smart_str(aluno.email))
                sheet.write(
                    row,
                    3,
                    dict(Aluno.SITUACAO_CHOICES).get(aluno.situacao, "-"),
                )
            output = BytesIO()
            workbook.save(output)
            output.seek(0)
            response = HttpResponse(
                output.getvalue(), content_type="application/vnd.ms-excel"
            )
            response["Content-Disposition"] = 'attachment; filename="alunos.xls"'
            return response

    paginator = Paginator(alunos_qs, 15)
    try:
        alunos_page = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        alunos_page = paginator.page(1)

    html = render_to_string(
        "alunos/_tabela_alunos_parcial.html", {"alunos": alunos_page}, request=request
    )

    paginacao_html = ""
    if alunos_page.paginator.num_pages > 1:
        paginacao_html = '<ul class="pagination justify-content-center pagination-sm" id="paginacao-alunos">'
        for numero in alunos_page.paginator.page_range:
            active = " active" if numero == alunos_page.number else ""
            paginacao_html += f'<li class="page-item{active}"><a href="#" class="page-link" data-page="{numero}">{numero}</a></li>'
        paginacao_html += "</ul>"

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return HttpResponse(html + paginacao_html)

    return HttpResponse(html)


@login_required
@require_GET
def buscar_foto_por_numero_iniciatico(request, numero_iniciatico):
    """
    Busca foto existente no diretório baseada no número iniciático.
    
    Retorna o caminho relativo da foto mais recente encontrada.
    """
    import os
    from django.conf import settings
    from pathlib import Path
    
    # Diretório de fotos
    fotos_dir = Path(settings.MEDIA_ROOT) / 'alunos' / 'fotos'
    
    # Extensões suportadas
    extensoes = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
    
    # Procura por arquivos com o número iniciático
    arquivos_encontrados = []
    
    if fotos_dir.exists():
        for ext in extensoes:
            # Procura exato: numero_iniciatico.ext
            arquivo = fotos_dir / f"{numero_iniciatico}{ext}"
            if arquivo.exists():
                arquivos_encontrados.append(arquivo)
            
            # Procura variações: numero_iniciatico_*.ext
            for variacao in fotos_dir.glob(f"{numero_iniciatico}_*{ext}"):
                arquivos_encontrados.append(variacao)
            
            # Procura: *_numero_iniciatico.ext
            for variacao in fotos_dir.glob(f"*_{numero_iniciatico}{ext}"):
                arquivos_encontrados.append(variacao)
    
    if not arquivos_encontrados:
        return JsonResponse({
            'success': False,
            'message': 'Nenhuma foto encontrada para este número iniciático'
        })
    
    # Ordena por data de modificação (mais recente primeiro)
    arquivos_encontrados.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    arquivo_mais_recente = arquivos_encontrados[0]
    
    # Retorna caminho relativo ao MEDIA_ROOT
    caminho_relativo = arquivo_mais_recente.relative_to(settings.MEDIA_ROOT)
    url_foto = f"{settings.MEDIA_URL}{caminho_relativo}".replace('\\', '/')
    
    return JsonResponse({
        'success': True,
        'foto_url': url_foto,
        'foto_path': str(caminho_relativo).replace('\\', '/'),
        'nome_arquivo': arquivo_mais_recente.name,
        'total_encontradas': len(arquivos_encontrados)
    })
