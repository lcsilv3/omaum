from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from importlib import import_module
from django.core.exceptions import ValidationError
from django.utils import timezone
import logging
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)

def get_models():
    """Obtém os modelos dinamicamente."""
    try:
        alunos_module = import_module("alunos.models")
        return getattr(alunos_module, "Aluno")
    except (ImportError, AttributeError):
        return None

def get_forms():
    """Obtém os formulários dinamicamente."""
    try:
        alunos_forms = import_module("alunos.forms")
        return getattr(alunos_forms, "AlunoForm")
    except (ImportError, AttributeError):
        return None

@login_required
def pagina_inicial(request):
    """Exibe a página inicial do sistema (versão compacta). Para voltar ao layout antigo, altere para 'home.html'."""
    try:
        # Obter estatísticas para o dashboard
        Aluno = get_models()
        total_alunos = Aluno.objects.count() if Aluno else 0
        alunos_ativos = Aluno.objects.filter(situacao="ATIVO").count() if Aluno else 0
        try:
            Curso = import_module("cursos.models").Curso
            total_cursos = Curso.objects.count()
        except (ImportError, AttributeError):
            total_cursos = 0
        try:
            Atividade = import_module("atividades.models").Atividade
            atividades_recentes = Atividade.objects.count()
        except (ImportError, AttributeError):
            atividades_recentes = 0
        context = {
            "total_alunos": total_alunos,
            "alunos_ativos": alunos_ativos,
            "total_cursos": total_cursos,
            "atividades_recentes": atividades_recentes,
        }
        # NOVO: renderizar home_compact.html
        return render(request, "home_compact.html", context)
    except Exception as e:
        logger.error(f"Erro na página inicial: {str(e)}", exc_info=True)
        messages.error(request, f"Ocorreu um erro ao carregar a página inicial: {str(e)}")
        return render(request, "home_compact.html", {"error": str(e)})

def registro_usuario(request):
    """Exibe o formulário de registro de usuário."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso! Agora você pode fazer login.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def painel_controle(request):
    """Exibe o painel de controle do sistema."""
    try:
        # Obter estatísticas para o painel de controle
        Aluno = get_models()
        total_alunos = Aluno.objects.count() if Aluno else 0
        alunos_ativos = Aluno.objects.filter(situacao="ATIVO").count() if Aluno else 0
        
        # Tentar importar outros modelos para estatísticas
        try:
            Curso = import_module("cursos.models").Curso
            total_cursos = Curso.objects.count()
        except (ImportError, AttributeError):
            total_cursos = 0
            
        try:
            Turma = import_module("turmas.models").Turma
            total_turmas = Turma.objects.count()
        except (ImportError, AttributeError):
            total_turmas = 0
        
        # Preparar contexto para o template
        context = {
            "total_alunos": total_alunos,
            "alunos_ativos": alunos_ativos,
            "total_cursos": total_cursos,
            "total_turmas": total_turmas,
        }
        
        return render(request, "core/painel_controle.html", context)
    except Exception as e:
        logger.error(f"Erro no painel de controle: {str(e)}", exc_info=True)
        messages.error(request, f"Ocorreu um erro ao carregar o painel de controle: {str(e)}")
        return render(request, "core/painel_controle.html", {"error": str(e)})

@login_required
def perfil(request):
    """Exibe o perfil do usuário logado."""
    return render(request, "core/perfil.html")

@login_required
def configuracoes(request):
    """Exibe as configurações do sistema."""
    return render(request, "core/configuracoes.html")

@login_required
def atualizar_configuracao(request):
    """Atualiza as configurações do sistema."""
    if request.method == 'POST':
        # Processar as configurações enviadas
        try:
            # Obter os dados do formulário
            configuracoes = request.POST.dict()
            
            # Remover o token CSRF
            if 'csrfmiddlewaretoken' in configuracoes:
                del configuracoes['csrfmiddlewaretoken']
            
            # Salvar as configurações (exemplo simplificado)
            for chave, valor in configuracoes.items():
                # Aqui você implementaria a lógica para salvar cada configuração
                # Por exemplo, usando um modelo de Configuração ou similar
                pass
            
            messages.success(request, "Configurações atualizadas com sucesso!")
            return redirect('core:configuracoes')
        except Exception as e:
            logger.error(f"Erro ao atualizar configurações: {str(e)}", exc_info=True)
            messages.error(request, f"Erro ao atualizar configurações: {str(e)}")
    
    # Se não for POST ou se houver erro, redirecionar para a página de configurações
    return redirect('core:configuracoes')

def csrf_check(request):
    """
    Verifica se a proteção CSRF está funcionando corretamente.
    Esta função é usada principalmente para testes e diagnósticos.
    """
    if request.method == 'POST':
        # Se chegou aqui em um POST, significa que o token CSRF foi validado com sucesso
        return JsonResponse({"status": "success", "message": "CSRF check passed"})
    else:
        # Para GET, retorna um formulário simples que fará um POST
        return render(request, "core/csrf_check.html")

@login_required
def dashboard(request):
    """Exibe o dashboard com estatísticas gerais."""
    try:
        # Obter estatísticas para o dashboard
        Aluno = get_models()
        total_alunos = Aluno.objects.count() if Aluno else 0
        alunos_ativos = Aluno.objects.filter(situacao="ATIVO").count() if Aluno else 0
        
        # Tentar importar outros modelos para estatísticas
        try:
            Curso = import_module("cursos.models").Curso
            total_cursos = Curso.objects.count()
            cursos = Curso.objects.all()
            cursos_labels = [curso.nome for curso in cursos]
        except (ImportError, AttributeError):
            total_cursos = 0
            cursos_labels = []
            
        try:
            Matricula = import_module("matriculas.models").Matricula
            alunos_por_curso = []
            for curso in cursos:
                count = Matricula.objects.filter(turma__curso=curso).count()
                alunos_por_curso.append(count)
        except (ImportError, AttributeError):
            alunos_por_curso = [0] * len(cursos_labels)
        
        # Preparar contexto para o template
        context = {
            "total_alunos": total_alunos,
            "alunos_ativos": alunos_ativos,
            "total_cursos": total_cursos,
            "cursos_labels": cursos_labels,
            "alunos_por_curso_data": alunos_por_curso,
        }
        
        return render(request, "core/dashboard.html", context)
    except Exception as e:
        logger.error(f"Erro no dashboard: {str(e)}", exc_info=True)
        messages.error(request, f"Ocorreu um erro ao carregar o dashboard: {str(e)}")
        return render(request, "core/dashboard.html", {"error": str(e)})

@login_required
def busca_global(request):
    """Realiza uma busca global no sistema."""
    query = request.GET.get("q", "")
    resultados = []
    
    if query and len(query) >= 2:
        try:
            # Buscar alunos
            Aluno = get_models()
            if Aluno:
                alunos = Aluno.objects.filter(
                    Q(nome__icontains=query) | 
                    Q(cpf__icontains=query) |
                    Q(email__icontains=query)
                )[:10]
                for aluno in alunos:
                    resultados.append({
                        "tipo": "Aluno",
                        "nome": aluno.nome,
                        "url": f"/alunos/{aluno.cpf}/detalhes/",
                        "descricao": f"CPF: {aluno.cpf}"
                    })
            
            # Buscar cursos
            try:
                Curso = import_module("cursos.models").Curso
                cursos = Curso.objects.filter(nome__icontains=query)[:10]
                for curso in cursos:
                    resultados.append({
                        "tipo": "Curso",
                        "nome": curso.nome,
                        "url": f"/cursos/{curso.codigo_curso}/detalhes/",
                        "descricao": f"Código: {curso.codigo_curso}"
                    })
            except (ImportError, AttributeError):
                pass
            
            # Buscar turmas
            try:
                Turma = import_module("turmas.models").Turma
                turmas = Turma.objects.filter(nome__icontains=query)[:10]
                for turma in turmas:
                    resultados.append({
                        "tipo": "Turma",
                        "nome": turma.nome,
                        "url": f"/turmas/{turma.id}/detalhes/",
                        "descricao": f"Curso: {turma.curso.nome if turma.curso else 'N/A'}"
                    })
            except (ImportError, AttributeError):
                pass
        
        except Exception as e:
            logger.error(f"Erro na busca global: {str(e)}", exc_info=True)
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse(resultados, safe=False)