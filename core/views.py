from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.db.models import Q
from importlib import import_module
import logging
from django.contrib.auth.forms import UserCreationForm

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
    # Verificar se o usuário tem permissão (é staff)
    if not request.user.is_staff:
        messages.error(request, "Você não tem permissão para acessar o painel de controle.")
        return redirect('core:pagina_inicial')
    
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
    # Verificar se o usuário tem permissão (é staff)
    if not request.user.is_staff:
        messages.error(request, "Você não tem permissão para acessar as configurações.")
        return redirect('core:pagina_inicial')
    
    # Obter configuração atual
    from .utils import garantir_configuracao_sistema
    config = garantir_configuracao_sistema()
    
    if request.method == 'POST':
        # Processar as configurações enviadas
        try:
            # Atualizar os campos da configuração
            config.nome_sistema = request.POST.get('nome_sistema', config.nome_sistema)
            config.versao = request.POST.get('versao', config.versao)
            config.manutencao_ativa = 'manutencao_ativa' in request.POST
            config.mensagem_manutencao = request.POST.get('mensagem_manutencao', config.mensagem_manutencao)
            config.save()
            
            messages.success(request, "Configurações atualizadas com sucesso!")
            return redirect('core:painel_controle')
        except Exception as e:
            logger.error(f"Erro ao atualizar configurações: {str(e)}", exc_info=True)
            messages.error(request, f"Erro ao atualizar configurações: {str(e)}")
    
    # Para GET, mostrar o formulário de atualização
    return render(request, 'core/atualizar_configuracao.html', {'config': config})

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


class CustomLoginView(LoginView):
    """View customizada para login com sistema de logs."""
    
    template_name = 'core/login.html'
    
    def form_valid(self, form):
        """Processa o login válido e registra no log."""
        response = super().form_valid(form)
        
        # Registrar no log após o login ser bem-sucedido
        try:
            from .utils import registrar_log
            registrar_log(self.request, "Login realizado com sucesso", "INFO")
        except Exception as e:
            logger.error(f"Erro ao registrar log de login: {str(e)}")
        
        return response
    
    def form_invalid(self, form):
        """Processa o login inválido e registra no log."""
        response = super().form_invalid(form)
        
        # Registrar tentativa de login inválido
        try:
            from .utils import registrar_log
            registrar_log(self.request, "Tentativa de login inválida", "AVISO")
        except Exception as e:
            logger.error(f"Erro ao registrar log de login inválido: {str(e)}")
        
        return response