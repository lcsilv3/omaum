from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from importlib import import_module
from django.core.exceptions import ValidationError
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


def get_models():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_forms():
    """Obtém o formulário AlunoForm dinamicamente."""
    alunos_forms = import_module("alunos.forms")
    return getattr(alunos_forms, "AlunoForm")


def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


@login_required
def listar_alunos(request):
    """Lista todos os alunos cadastrados."""
    try:
        Aluno = get_models()
        # Obter parâmetros de busca e filtro
        query = request.GET.get("q", "")
        curso_id = request.GET.get("curso", "")
        # Filtrar alunos
        alunos = Aluno.objects.all()
        if query:
            alunos = alunos.filter(
                Q(nome__icontains=query)
                | Q(cpf__icontains=query)
                | Q(email__icontains=query)
                | Q(numero_iniciatico__icontains=query)
            )
        # Filtro por curso (corrigido)
        codigo_curso = request.GET.get("codigo_curso", "")
        if codigo_curso:
            try:
                Matricula = import_module("matriculas.models").Matricula
                alunos_cpfs = (
                    Matricula.objects.filter(
                        turma__curso__codigo_curso=codigo_curso
                    )
                    .values_list("aluno__cpf", flat=True)
                    .distinct()
                )
                alunos = alunos.filter(cpf__in=alunos_cpfs)
            except (ImportError, AttributeError) as e:
                logger.error(f"Erro ao filtrar por curso: {e}")
        
        # Para cada aluno, buscar os cursos em que está matriculado
        alunos_com_cursos = []
        for aluno in alunos:
            try:
                # Importar o modelo Matricula dinamicamente
                Matricula = import_module("matriculas.models").Matricula
                # Buscar matrículas do aluno
                matriculas = Matricula.objects.filter(aluno=aluno)
                # Extrair nomes dos cursos
                cursos = [m.turma.curso.nome for m in matriculas]
                # Adicionar informação de cursos ao aluno
                aluno.cursos = cursos
            except Exception as e:
                aluno.cursos = []
                print(f"Erro ao buscar cursos do aluno {aluno.nome}: {e}")
            alunos_com_cursos.append(aluno)
        
        # Paginação
        paginator = Paginator(alunos_com_cursos, 10)  # 10 alunos por página
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        # Obter cursos para o filtro
        try:
            Curso = import_module("cursos.models").Curso
            cursos = Curso.objects.all()
        except Exception as e:
            cursos = []
            print(f"Erro ao buscar cursos: {e}")
        
        # Adicionar contagem total de alunos ao contexto
        total_alunos = alunos.count()
        
        context = {
            "alunos": page_obj,
            "page_obj": page_obj,
            "query": query,
            "cursos": cursos,
            "codigo_curso_selecionado": codigo_curso,
            "total_alunos": total_alunos,  # Adicionando contagem total
        }
        return render(request, "alunos/listar_alunos.html", context)
    except Exception as e:
        # Logar o erro para facilitar a depuração
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erro ao listar alunos: {str(e)}", exc_info=True)
        
        # Em vez de mostrar a mensagem de erro, apenas retornamos uma lista vazia
        return render(
            request,
            "alunos/listar_alunos.html",
            {
                "alunos": [],
                "page_obj": None,
                "query": "",
                "cursos": [],
                "curso_selecionado": "",
                "error_message": f"Erro ao listar alunos: {str(e)}",
                "total_alunos": 0,  # Garantir que a contagem seja zero em caso de erro
            },
        )


@login_required
def criar_aluno(request):
    """Cria um novo aluno."""
    AlunoForm = get_forms()
    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                aluno = form.save()
                messages.success(request, "Aluno cadastrado com sucesso!")
                return redirect("alunos:detalhar_aluno", cpf=aluno.cpf)
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
            except Exception as e:
                messages.error(request, f"Erro ao cadastrar aluno: {str(e)}")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = AlunoForm()
    return render(
        request, "alunos/formulario_aluno.html", {"form": form, "aluno": None}
    )

@login_required
def detalhar_aluno(request, cpf):
    """Exibe os detalhes de um aluno."""
    Aluno = get_models()
    aluno = get_object_or_404(Aluno, cpf=cpf)
    
    # Buscar turmas onde o aluno é instrutor
    turmas_como_instrutor = []
    turmas_como_instrutor_auxiliar = []
    turmas_como_auxiliar_instrucao = []
    
    if aluno.esta_ativo:
        from importlib import import_module
        try:
            # Importar o modelo Turma dinamicamente
            turmas_module = import_module("turmas.models")
            Turma = getattr(turmas_module, "Turma")
            # Buscar turmas ativas onde o aluno é instrutor
            turmas_como_instrutor = Turma.objects.filter(
                instrutor=aluno, status="A"
            ).select_related("curso")
            turmas_como_instrutor_auxiliar = Turma.objects.filter(
                instrutor_auxiliar=aluno, status="A"
            ).select_related("curso")
            turmas_como_auxiliar_instrucao = Turma.objects.filter(
                auxiliar_instrucao=aluno, status="A"
            ).select_related("curso")
        except (ImportError, AttributeError):
            pass
    
    # Buscar matrículas do aluno
    matriculas = []
    try:
        # Importar o modelo Matricula dinamicamente
        matriculas_module = import_module("matriculas.models")
        Matricula = getattr(matriculas_module, "Matricula")
        # Buscar matrículas do aluno
        matriculas = Matricula.objects.filter(aluno=aluno).select_related("turma__curso")
    except (ImportError, AttributeError):
        pass
    
    # Buscar atividades acadêmicas do aluno
    atividades_academicas = []
    try:
        # Importar o modelo Frequencia dinamicamente
        frequencias_module = import_module("frequencias.models")
        Frequencia = getattr(frequencias_module, "Frequencia")
        # Buscar frequências do aluno
        atividades_academicas = Frequencia.objects.filter(aluno=aluno).select_related("atividade").order_by("-data")
    except (ImportError, AttributeError):
        pass
    
    # Buscar atividades ritualísticas do aluno
    atividades_ritualisticas = []
    try:
        # Importar o modelo AtividadeRitualistica dinamicamente
        atividades_module = import_module("atividades.models")
        AtividadeRitualistica = getattr(atividades_module, "AtividadeRitualistica")
        # Buscar atividades ritualísticas do aluno
        atividades_ritualisticas = AtividadeRitualistica.objects.filter(participantes=aluno).order_by("-data")
    except (ImportError, AttributeError):
        pass
    
    return render(
        request,
        "alunos/detalhar_aluno.html",
        {
            "aluno": aluno,
            "turmas_como_instrutor": turmas_como_instrutor,
            "turmas_como_instrutor_auxiliar": turmas_como_instrutor_auxiliar,
            "turmas_como_auxiliar_instrucao": turmas_como_auxiliar_instrucao,
            "matriculas": matriculas,
            "atividades_academicas": atividades_academicas,
            "atividades_ritualisticas": atividades_ritualisticas,
        },
    )


@login_required
def editar_aluno(request, cpf):
    """Edita um aluno existente."""
    Aluno = get_models()
    AlunoForm = get_forms()
    aluno = get_object_or_404(Aluno, cpf=cpf)
    
    if request.method == "POST":
        logger.debug(f"Recebido POST para editar aluno {cpf}")
        form = AlunoForm(request.POST, request.FILES, instance=aluno)
        if form.is_valid():
            logger.debug("Form é válido, salvando...")
            try:
                aluno_atualizado = form.save()
                logger.debug(f"Aluno salvo com sucesso: {aluno_atualizado.nome_iniciatico}")
                messages.success(request, "Aluno atualizado com sucesso!")
                return redirect("alunos:detalhar_aluno", cpf=aluno_atualizado.cpf)
            except Exception as e:
                logger.error(f"Erro ao salvar aluno: {str(e)}", exc_info=True)
                messages.error(request, f"Erro ao atualizar aluno: {str(e)}")
        else:
            logger.debug(f"Form inválido: {form.errors}")
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = AlunoForm(instance=aluno)
    
    return render(
        request, "alunos/formulario_aluno.html", {"form": form, "aluno": aluno}
    )


@login_required
def excluir_aluno(request, cpf):
    """Exclui um aluno."""
    Aluno = get_models()
    aluno = get_object_or_404(Aluno, cpf=cpf)
    if request.method == "POST":
        try:
            aluno.delete()
            messages.success(request, "Aluno excluído com sucesso!")
            return redirect("alunos:listar_alunos")
        except Exception as e:
            messages.error(request, f"Erro ao excluir aluno: {str(e)}")
            return redirect("alunos:detalhar_aluno", cpf=aluno.cpf)
    return render(request, "alunos/excluir_aluno.html", {"aluno": aluno})


@login_required
def dashboard(request):
    """Exibe o dashboard de alunos com estatísticas."""
    try:
        Aluno = get_models()
        total_alunos = Aluno.objects.count()
        # Contagem por sexo
        total_masculino = Aluno.objects.filter(sexo="M").count()
        total_feminino = Aluno.objects.filter(sexo="F").count()
        total_outros = Aluno.objects.filter(sexo="O").count()
        # Alunos recentes
        alunos_recentes = Aluno.objects.order_by("-created_at")[:5]
        context = {
            "total_alunos": total_alunos,
            "total_masculino": total_masculino,
            "total_feminino": total_feminino,
            "total_outros": total_outros,
            "alunos_recentes": alunos_recentes,
        }
        return render(request, "alunos/dashboard.html", context)
    except Exception as e:
        messages.error(request, f"Erro ao carregar dashboard: {str(e)}")
        return redirect("alunos:listar_alunos")


@login_required
def exportar_alunos(request):
    """Exporta os dados dos alunos para um arquivo CSV."""
    try:
        import csv
        from django.http import HttpResponse
        Aluno = get_models()
        alunos = Aluno.objects.all()
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="alunos.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "CPF",
            "Nome",
            "Email",
            "Data de Nascimento",
            "Sexo",
            "Número Iniciático",
        ])
        for aluno in alunos:
            writer.writerow(
                [
                    aluno.cpf,
                    aluno.nome,
                    aluno.email,
                    aluno.data_nascimento,
                    aluno.get_sexo_display(),
                    aluno.numero_iniciatico,
                ]
            )
        return response
    except Exception as e:
        messages.error(request, f"Erro ao exportar alunos: {str(e)}")
        return redirect("alunos:listar_alunos")

@login_required
def importar_alunos(request):
    """Importa alunos de um arquivo CSV."""
    if request.method == "POST" and request.FILES.get("csv_file"):
        try:
            import csv
            from io import TextIOWrapper
            Aluno = get_models()
            csv_file = TextIOWrapper(
                request.FILES["csv_file"].file, encoding="utf-8"
            )
            reader = csv.DictReader(csv_file)
            count = 0
            errors = []
            for row in reader:
                try:
                    # Processar cada linha do CSV
                    Aluno.objects.create(
                        cpf=row.get("CPF", "").strip(),
                        nome=row.get("Nome", "").strip(),
                        email=row.get("Email", "").strip(),
                        data_nascimento=row.get(
                            "Data de Nascimento", ""
                        ).strip(),
                        sexo=row.get("Sexo", "M")[
                            0
                        ].upper(),  # Pega a primeira letra e converte para maiúscula
                        numero_iniciatico=row.get(
                            "Número Iniciático", ""
                        ).strip(),
                        nome_iniciatico=row.get(
                            "Nome Iniciático", row.get("Nome", "")
                        ).strip(),
                        nacionalidade=row.get(
                            "Nacionalidade", "Brasileira"
                        ).strip(),
                        naturalidade=row.get("Naturalidade", "").strip(),
                        rua=row.get("Rua", "").strip(),
                        numero_imovel=row.get("Número", "").strip(),
                        complemento=row.get("Complemento", "").strip(),
                        bairro=row.get("Bairro", "").strip(),
                        cidade=row.get("Cidade", "").strip(),
                        estado=row.get("Estado", "").strip(),
                        cep=row.get("CEP", "").strip(),
                        nome_primeiro_contato=row.get(
                            "Nome do Primeiro Contato", ""
                        ).strip(),
                        celular_primeiro_contato=row.get(
                            "Celular do Primeiro Contato", ""
                        ).strip(),
                        tipo_relacionamento_primeiro_contato=row.get(
                            "Tipo de Relacionamento do Primeiro Contato", ""
                        ).strip(),
                        tipo_sanguineo=row.get("Tipo Sanguíneo", "").strip(),
                        fator_rh=row.get("Fator RH", "+").strip(),
                    )
                    count += 1
                except Exception as e:
                    errors.append(f"Erro na linha {count+1}: {str(e)}")
            if errors:
                messages.warning(
                    request,
                    f"{count} alunos importados com {len(errors)} erros.",
                )
                for error in errors[:5]:  # Mostrar apenas os 5 primeiros erros
                    messages.error(request, error)
                if len(errors) > 5:
                    messages.error(
                        request, f"... e mais {len(errors) - 5} erros."
                    )
            else:
                messages.success(
                    request, f"{count} alunos importados com sucesso!"
                )
            return redirect("alunos:listar_alunos")
        except Exception as e:
            messages.error(request, f"Erro ao importar alunos: {str(e)}")
    return render(request, "alunos/importar_alunos.html")


@login_required
def relatorio_alunos(request):
    """Exibe um relatório com estatísticas sobre os alunos."""
    try:
        Aluno = get_models()
        total_alunos = Aluno.objects.count()
        total_masculino = Aluno.objects.filter(sexo="M").count()
        total_feminino = Aluno.objects.filter(sexo="F").count()
        total_outros = Aluno.objects.filter(sexo="O").count()
        # Calcular idade média
        from django.db.models import Avg, F
        from django.db.models.functions import ExtractYear
        from django.utils import timezone
        current_year = timezone.now().year
        idade_media = (
            Aluno.objects.annotate(
                idade=current_year - ExtractYear("data_nascimento")
            ).aggregate(Avg("idade"))["idade__avg"]
            or 0
        )
        context = {
            "total_alunos": total_alunos,
            "total_masculino": total_masculino,
            "total_feminino": total_feminino,
            "total_outros": total_outros,
            "idade_media": round(idade_media, 1),
        }
        return render(request, "alunos/relatorio_alunos.html", context)
    except Exception as e:
        messages.error(request, f"Erro ao gerar relatório: {str(e)}")
        return redirect("alunos:listar_alunos")

@login_required
def search_alunos(request):
    """API endpoint para buscar alunos."""
    try:
        query = request.GET.get("q", "")
        if len(query) < 2:
            return JsonResponse([], safe=False)
        
        Aluno = get_aluno_model()
        alunos = Aluno.objects.filter(
            Q(nome__icontains=query) |
            Q(cpf__icontains=query) |
            Q(email__icontains=query) |  # <-- Adicione esta linha
            Q(numero_iniciatico__icontains=query)
        )[:10]
        
        results = []
        for aluno in alunos:
            results.append({
                "cpf": aluno.cpf,
                "nome": aluno.nome,
                "email": aluno.email,  # <-- Adicione esta linha
                "numero_iniciatico": aluno.numero_iniciatico or "N/A",
                "foto": aluno.foto.url if hasattr(aluno, "foto") and aluno.foto else None,
                "situacao": aluno.get_situacao_display() if hasattr(aluno, "get_situacao_display") else ""
            })
        
        return JsonResponse(results, safe=False)
    except Exception as e:
        logger.error(f"Error in search_alunos: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

def confirmar_remocao_instrutoria(request, cpf, nova_situacao):
    """Confirma a remoção da instrutoria de um aluno."""
    from django.utils import timezone    from django.shortcuts import get_object_or_404, redirect, render
    from django.contrib import messages
    from importlib import import_module

    Aluno = get_models()
    aluno = get_object_or_404(Aluno, cpf=cpf)
    
    try:
        turmas_module = import_module("turmas.models")
        Turma = getattr(turmas_module, "Turma")
        cargos_module = import_module("cargos.models")
        AtribuicaoCargo = getattr(cargos_module, "AtribuicaoCargo")
        
        # Buscar turmas onde o aluno é instrutor
        turmas_instrutor = Turma.objects.filter(instrutor=aluno, status="A")
        turmas_instrutor_auxiliar = Turma.objects.filter(
            instrutor_auxiliar=aluno, status="A"
        )
        turmas_auxiliar_instrucao = Turma.objects.filter(
            auxiliar_instrucao=aluno, status="A"
        )
        
        # Juntar todas as turmas
        turmas = (
            list(turmas_instrutor)
            + list(turmas_instrutor_auxiliar)
            + list(turmas_auxiliar_instrucao)
        )
        
        # Se não houver turmas, redirecionar para a edição
        if not turmas:
            return redirect("alunos:editar_aluno", cpf=aluno.cpf)
            
        # Se o método for POST, processar a confirmação
        if request.method == "POST":
            # Atualizar a situação do aluno
            aluno.situacao = nova_situacao
            aluno.save()
            
            # Atualizar as turmas e finalizar os cargos administrativos
            for turma in turmas_instrutor:
                turma.instrutor = None
                turma.alerta_instrutor = True
                turma.alerta_mensagem = f"O instrutor {aluno.nome} foi removido devido à mudança de situação para '{aluno.get_situacao_display()}'."
                turma.save()
                # Finalizar os cargos administrativos relacionados
                atribuicoes = AtribuicaoCargo.objects.filter(
                    aluno=aluno,
                    cargo__nome__icontains="Instrutor Principal",
                    data_fim__isnull=True,
                )                for atribuicao in atribuicoes:
                    atribuicao.data_fim = timezone.now().date()
                    atribuicao.save()
                    
            for turma in turmas_instrutor_auxiliar:
                turma.instrutor_auxiliar = None
                turma.alerta_instrutor = True
                turma.alerta_mensagem = f"O instrutor auxiliar {aluno.nome} foi removido devido à mudança de situação para '{aluno.get_situacao_display()}'."
                turma.save()
                # Finalizar os cargos administrativos relacionados
                atribuicoes = AtribuicaoCargo.objects.filter(
                    aluno=aluno,
                    cargo__nome__icontains="Instrutor Auxiliar",
                    data_fim__isnull=True,
                )
                for atribuicao in atribuicoes:
                    atribuicao.data_fim = timezone.now().date()
                    atribuicao.save()
                    
            for turma in turmas_auxiliar_instrucao:
                turma.auxiliar_instrucao = None
                turma.alerta_instrutor = True
                turma.alerta_mensagem = f"O auxiliar de instrução {aluno.nome} foi removido devido à mudança de situação para '{aluno.get_situacao_display()}'."
                turma.save()
                # Finalizar os cargos administrativos relacionados
                atribuicoes = AtribuicaoCargo.objects.filter(
                    aluno=aluno,
                    cargo__nome__icontains="Auxiliar de Instrução",
                    data_fim__isnull=True,
                )
                for atribuicao in atribuicoes:
                    atribuicao.data_fim = timezone.now().date()
                    atribuicao.save()
                    
            messages.success(
                request,
                "Aluno atualizado com sucesso e removido das turmas como instrutor!",
            )
            return redirect("alunos:detalhar_aluno", cpf=aluno.cpf)
            
        # Renderizar a página de confirmação
        return render(
            request,
            "alunos/confirmar_remocao_instrutoria.html",
            {
                "aluno": aluno,
                "nova_situacao": dict(Aluno.SITUACAO_CHOICES).get(
                    nova_situacao
                ),
                "turmas_instrutor": turmas_instrutor,
                "turmas_instrutor_auxiliar": turmas_instrutor_auxiliar,
                "turmas_auxiliar_instrucao": turmas_auxiliar_instrucao,
                "total_turmas": len(turmas),
            },
        )
    except (ImportError, AttributeError) as e:
        messages.error(request, f"Erro ao processar a solicitação: {str(e)}")
        return redirect("alunos:editar_aluno", cpf=aluno.cpf)

@login_required
def search_instrutores(request):
    """API endpoint para buscar alunos elegíveis para serem instrutores."""
    try:
        query = request.GET.get("q", "")
        Aluno = get_aluno_model()
        # Buscar apenas alunos ativos
        alunos = Aluno.objects.filter(situacao="ATIVO")
        
        # Se houver uma consulta, filtrar por ela
        if query and len(query) >= 2:
            alunos = alunos.filter(
                Q(nome__icontains=query)
                | Q(cpf__icontains=query)
                | Q(numero_iniciatico__icontains=query)
            )
        
        # Filtrar alunos que podem ser instrutores
        alunos_elegiveis = []
        for aluno in alunos[:10]:  # Limitar a 10 resultados
            # Verificar se o aluno pode ser instrutor
            pode_ser_instrutor = False
            try:
                pode_ser_instrutor = aluno.pode_ser_instrutor
            except Exception as e:
                logger.error(f"Erro ao verificar elegibilidade do aluno {aluno.nome}: {str(e)}")
            
            alunos_elegiveis.append({
                "cpf": aluno.cpf,
                "nome": aluno.nome,
                "numero_iniciatico": aluno.numero_iniciatico or "N/A",
                "foto": aluno.foto.url if hasattr(aluno, "foto") and aluno.foto else None,
                "situacao": aluno.get_situacao_display(),
                "situacao_codigo": aluno.situacao,
                "esta_ativo": aluno.esta_ativo,
                "elegivel": pode_ser_instrutor
            })
        
        if not alunos_elegiveis:
            logger.warning("Nenhum aluno elegível para ser instrutor. Usando todos os alunos ativos.")
        
        logger.info(f"Alunos elegíveis para instrutores: {len([a for a in alunos_elegiveis if a['elegivel']])}")
        return JsonResponse(alunos_elegiveis, safe=False)
    except Exception as e:
        logger.error(f"Erro em search_instrutores: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def get_aluno(request, cpf):
    """API endpoint para obter dados de um aluno específico."""
    try:
        Aluno = get_aluno_model()
        aluno = get_object_or_404(Aluno, cpf=cpf)
        return JsonResponse(
            {
                "success": True,
                "aluno": {
                    "cpf": aluno.cpf,
                    "nome": aluno.nome,
                    "numero_iniciatico": aluno.numero_iniciatico or "N/A",
                    "foto": (
                        aluno.foto.url
                        if hasattr(aluno, "foto") and aluno.foto
                        else None
                    ),
                },
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=404)


@login_required
@permission_required('alunos.view_aluno', raise_exception=True)
def verificar_elegibilidade_instrutor(request, cpf):
    """API endpoint para verificar se um aluno pode ser instrutor."""
    try:
        Aluno = get_aluno_model()
        aluno = get_object_or_404(Aluno, cpf=cpf)
        
        # Verificar se o aluno está ativo
        if aluno.situacao != "ATIVO":
            return JsonResponse(
                {
                    "elegivel": False,
                    "motivo": f"O aluno não está ativo. Situação atual: {aluno.get_situacao_display()}",
                }
            )
        
        # Verificar se o aluno pode ser instrutor
        if hasattr(aluno, 'pode_ser_instrutor'):
            pode_ser_instrutor = aluno.pode_ser_instrutor
            
            if not pode_ser_instrutor:
                return JsonResponse(
                    {
                        "elegivel": False,
                        "motivo": "O aluno não atende aos requisitos para ser instrutor.",
                    }
                )
        else:
            # Se o método não existir, considerar elegível por padrão
            return JsonResponse({"elegivel": True})
        
        return JsonResponse({"elegivel": True})
    except Exception as e:
        return JsonResponse(
            {"elegivel": False, "motivo": f"Erro na busca: {str(e)}"},
            status=500
        )


@login_required
def diagnostico_instrutores(request):
    """
    Página de diagnóstico para depurar problemas com a seleção de instrutores.
    Mostra informações detalhadas sobre alunos e sua elegibilidade para serem instrutores.
    """
    try:
        Aluno = get_aluno_model()
        # Buscar todos os alunos ativos
        alunos_ativos = Aluno.objects.filter(situacao="ATIVO")
        
        # Coletar informações de diagnóstico para cada aluno
        diagnostico = []
        for aluno in alunos_ativos:
            info = {
                "cpf": aluno.cpf,
                "nome": aluno.nome,
                "numero_iniciatico": aluno.numero_iniciatico or "N/A",
                "situacao": aluno.get_situacao_display(),
                "tem_metodo": hasattr(aluno, 'pode_ser_instrutor'),
            }
            
            # Verificar se o método pode_ser_instrutor existe e executá-lo
            if info["tem_metodo"]:
                try:
                    info["elegivel"] = aluno.pode_ser_instrutor
                    
                    # Se não for elegível, tentar determinar o motivo
                    if not info["elegivel"]:
                        # Verificar matrículas em cursos pré-iniciaticos
                        from importlib import import_module
                        try:
                            matriculas_module = import_module("matriculas.models")
                            Matricula = getattr(matriculas_module, "Matricula")
                            
                            matriculas_pre_iniciatico = Matricula.objects.filter(
                                aluno=aluno, turma__curso__nome__icontains="Pré-iniciático"
                            )
                            
                            if matriculas_pre_iniciatico.exists():
                                cursos = [m.turma.curso.nome for m in matriculas_pre_iniciatico]
                                info["motivo_inelegibilidade"] = f"Matriculado em cursos pré-iniciáticos: {', '.join(cursos)}"
                            else:
                                info["motivo_inelegibilidade"] = "Não atende aos requisitos (motivo desconhecido)"
                        except Exception as e:
                            info["motivo_inelegibilidade"] = f"Erro ao verificar matrículas: {str(e)}"
                except Exception as e:
                    info["erro"] = str(e)
            
            diagnostico.append(info)
        
        return render(
            request,
            "alunos/diagnostico_instrutores.html",
            {
                "diagnostico": diagnostico,
                "total_alunos": len(alunos_ativos),
                "total_elegiveis": sum(1 for info in diagnostico if info.get("elegivel", False)),
            },
        )
    except Exception as e:
        import traceback
        error_msg = str(e)
        stack_trace = traceback.format_exc()
        logger.error(f"Erro na página de diagnóstico: {error_msg}")
        logger.error(f"Traceback: {stack_trace}")
        
        return render(
            request,
            "alunos/erro.html",
            {
                "erro": error_msg,
                "traceback": stack_trace,
            },
        )
@login_required
def get_aluno_detalhes(request, cpf):
    """API endpoint para obter detalhes específicos de um aluno."""
    try:
        Aluno = get_aluno_model()
        aluno = get_object_or_404(Aluno, cpf=cpf)
        
        # Verificar se o aluno é instrutor em alguma turma
        turmas_como_instrutor = False
        try:
            from django.db.models import Q
            turmas_module = import_module("turmas.models")
            Turma = getattr(turmas_module, "Turma")
            turmas_como_instrutor = Turma.objects.filter(
                Q(instrutor=aluno) |
                Q(instrutor_auxiliar=aluno) |
                Q(auxiliar_instrucao=aluno)
            ).exists()
        except Exception as e:
            logger.error(f"Erro ao verificar turmas como instrutor: {str(e)}")
        
        # Obter turmas em que o aluno está matriculado
        turmas_matriculado = []
        try:
            matriculas_module = import_module("matriculas.models")
            Matricula = getattr(matriculas_module, "Matricula")
            matriculas = Matricula.objects.filter(aluno=aluno, status="A")
            turmas_matriculado = [
                {
                    "id": m.turma.id,
                    "nome": m.turma.nome,
                    "curso": m.turma.curso.nome if m.turma.curso else "Sem curso"
                }
                for m in matriculas
            ]
        except Exception as e:
            logger.error(f"Erro ao buscar matrículas: {str(e)}")
        
        return JsonResponse({
            "success": True,
            "e_instrutor": turmas_como_instrutor,
            "turmas": turmas_matriculado,
            "pode_ser_instrutor": getattr(aluno, 'pode_ser_instrutor', False)
        })
    except Exception as e:
        logger.error(f"Erro ao obter detalhes do aluno: {str(e)}", exc_info=True)
        return JsonResponse({"success": False, "error": str(e)}, status=500)