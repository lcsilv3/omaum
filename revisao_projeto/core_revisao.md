# Revisão da Funcionalidade: core

## Arquivos forms.py:


### Arquivo: core\forms.py

python
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Importar a função utilitária centralizada
from .utils import get_model_dynamically

# Substituir a função get_model pela função utilitária centralizada
get_model = get_model_dynamically


class AlunoForm(forms.ModelForm):
    class Meta:
        model = get_model("alunos", "Aluno")
        fields = (
            "cpf",
            "nome",
            "data_nascimento",
            "hora_nascimento",
            "email",
            "foto",
            "sexo",
            "situacao",
            "numero_iniciatico",
            "nome_iniciatico",
            "nacionalidade",
            "naturalidade",
            "rua",
            "numero_imovel",
            "complemento",
            "bairro",
            "cidade",
            "estado",
            "cep",
            "nome_primeiro_contato",
            "celular_primeiro_contato",
            "tipo_relacionamento_primeiro_contato",
            "nome_segundo_contato",
            "celular_segundo_contato",
            "tipo_relacionamento_segundo_contato",
            "tipo_sanguineo",
            "fator_rh",
            "alergias",
            "condicoes_medicas_gerais",
            "convenio_medico",
            "hospital",
        )
        widgets = {
            "data_nascimento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "hora_nascimento": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
        }


class CursoForm(forms.ModelForm):
    class Meta:
        model = get_model("cursos", "Curso")
        fields = ("codigo_curso", "nome", "descricao", "duracao")
        widgets = {
            "codigo_curso": forms.NumberInput(
                attrs={"class": "form-control", "min": "1"}
            ),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "duracao": forms.NumberInput(
                attrs={"class": "form-control", "min": "1"}
            ),
        }


class TurmaForm(forms.ModelForm):
    class Meta:
        model = get_model("turmas", "Turma")
        fields = [
            "nome",
            "curso",
            "vagas",
            "status",
            "data_inicio",
            "data_fim",
            "instrutor",
            "instrutor_auxiliar",
            "auxiliar_instrucao",
            "dias_semana",
            "local",
            "horario",
            "descricao",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "curso": forms.Select(attrs={"class": "form-select"}),
            "vagas": forms.NumberInput(
                attrs={"class": "form-control", "min": "1"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "data_inicio": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "data_fim": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "instrutor": forms.Select(attrs={"class": "form-control"}),
            "instrutor_auxiliar": forms.Select(
                attrs={"class": "form-control"}
            ),
            "auxiliar_instrucao": forms.Select(
                attrs={"class": "form-control"}
            ),
            "dias_semana": forms.TextInput(attrs={"class": "form-control"}),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "horario": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }


class AtividadeAcademicaForm(forms.ModelForm):
    class Meta:
        model = get_model("atividades", "AtividadeAcademica")
        fields = [
            "nome",
            "descricao",
            "data_inicio",
            "data_fim",
            "turma",
            "responsavel",
            "local",
            "tipo_atividade",
            "status",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "data_inicio": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "data_fim": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "turma": forms.Select(attrs={"class": "form-control"}),
            "responsavel": forms.TextInput(attrs={"class": "form-control"}),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "tipo_atividade": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class AtividadeRitualisticaForm(forms.ModelForm):
    todos_alunos = forms.BooleanField(
        required=False, label="Incluir todos os alunos da turma", initial=False
    )

    class Meta:
        model = get_model("atividades", "AtividadeRitualistica")
        fields = [
            "nome",
            "descricao",
            "data",
            "hora_inicio",
            "hora_fim",
            "local",
            "turma",
            "participantes",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "data": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "hora_inicio": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "hora_fim": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "turma": forms.Select(attrs={"class": "form-control"}),
            "participantes": forms.SelectMultiple(
                attrs={"class": "form-control"}
            ),
        }


class PresencaForm(forms.ModelForm):
    class Meta:
        model = get_model("presencas", "Presenca")
        fields = ["aluno", "turma", "data", "status"]
        widgets = {
            "data": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class FrequenciaForm(forms.ModelForm):
    class Meta:
        model = get_model("frequencias", "Frequencia")
        fields = ["aluno", "atividade", "data", "presente", "justificativa"]
        widgets = {
            "aluno": forms.Select(attrs={"class": "form-select"}),
            "atividade": forms.Select(attrs={"class": "form-select"}),
            "data": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "presente": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "justificativa": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),
        }


class IniciacaoForm(forms.ModelForm):
    class Meta:
        model = get_model("iniciacoes", "Iniciacao")
        fields = ["aluno", "curso", "data_iniciacao", "grau", "observacoes"]
        widgets = {
            "data_iniciacao": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "aluno": forms.Select(attrs={"class": "form-control"}),
            "curso": forms.Select(attrs={"class": "form-control"}),
            "grau": forms.TextInput(attrs={"class": "form-control"}),
            "observacoes": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
        }


class PunicaoForm(forms.ModelForm):
    class Meta:
        model = get_model("punicoes", "Punicao")
        fields = [
            "aluno",
            "tipo_punicao",
            "data_aplicacao",
            "motivo",
            "observacoes",
        ]
        widgets = {
            "aluno": forms.Select(attrs={"class": "form-control"}),
            "tipo_punicao": forms.Select(attrs={"class": "form-control"}),
            "data_aplicacao": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "motivo": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "observacoes": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }


class CargoAdministrativoForm(forms.ModelForm):
    class Meta:
        model = get_model("cargos", "CargoAdministrativo")
        fields = ["codigo_cargo", "nome", "descricao"]
        widgets = {
            "codigo_cargo": forms.TextInput(attrs={"class": "form-control"}),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }


class RelatorioForm(forms.ModelForm):
    class Meta:
        model = get_model("relatorios", "Relatorio")
        fields = ["titulo", "conteudo"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "conteudo": forms.Textarea(attrs={"class": "form-control"}),
        }


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ConfiguracaoSistemaForm(forms.ModelForm):
    class Meta:
        model = get_model("core", "ConfiguracaoSistema")
        fields = [
            "nome_sistema",
            "versao",
            "manutencao_ativa",
            "mensagem_manutencao",
        ]
        widgets = {
            "nome_sistema": forms.TextInput(attrs={"class": "form-control"}),
            "versao": forms.TextInput(attrs={"class": "form-control"}),
            "manutencao_ativa": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "mensagem_manutencao": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }



## Arquivos views.py:


### Arquivo: core\views.py

python
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
    """Exibe a página inicial do sistema."""
    try:
        # Obter estatísticas para o dashboard
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
            Atividade = import_module("atividades.models").Atividade
            atividades_recentes = Atividade.objects.count()
        except (ImportError, AttributeError):
            atividades_recentes = 0
        
        # Preparar contexto para o template
        context = {
            "total_alunos": total_alunos,
            "alunos_ativos": alunos_ativos,
            "total_cursos": total_cursos,
            "atividades_recentes": atividades_recentes,
        }
        
        return render(request, "home.html", context)
    except Exception as e:
        logger.error(f"Erro na página inicial: {str(e)}", exc_info=True)
        messages.error(request, f"Ocorreu um erro ao carregar a página inicial: {str(e)}")
        return render(request, "home.html", {"error": str(e)})

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


## Arquivos urls.py:


### Arquivo: core\urls.py

python
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "core"

urlpatterns = [
    path("", views.pagina_inicial, name="pagina_inicial"),
    
    # Adicione estas URLs se quiser manter as funcionalidades no template
    path('perfil/', views.perfil, name='perfil'),  # Você precisará criar esta view
    path('alterar-senha/', auth_views.PasswordChangeView.as_view(
        template_name='core/alterar_senha.html',
        success_url='/core/senha-alterada/'
    ), name='alterar_senha'),
    path('senha-alterada/', auth_views.PasswordChangeDoneView.as_view(
        template_name='core/senha_alterada.html'
    ), name='senha_alterada'),
    
    # Se você estiver usando as views de autenticação do Django
    path('sair/', auth_views.LogoutView.as_view(next_page='/'), name='sair'),
    
    path("painel-controle/", views.painel_controle, name="painel_controle"),
    path(
        "atualizar-configuracao/",
        views.atualizar_configuracao,
        name="atualizar_configuracao",
    ),
    path("csrf_check/", views.csrf_check, name="csrf_check"),
    path(
        "dashboard/", views.painel_controle, name="dashboard"
    ),  # Redireciona diretamente para a view
]


## Arquivos models.py:


### Arquivo: core\models.py

python
from django.db import models
from django.utils import timezone


class ConfiguracaoSistema(models.Model):
    """Configurações globais do sistema"""

    nome_sistema = models.CharField(max_length=100, default="OMAUM")
    versao = models.CharField(max_length=20, default="1.0.0")
    data_atualizacao = models.DateTimeField(default=timezone.now)
    manutencao_ativa = models.BooleanField(default=False)
    mensagem_manutencao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome_sistema} v{self.versao}"

    class Meta:
        verbose_name = "Configuração do Sistema"
        verbose_name_plural = "Configurações do Sistema"


class LogAtividade(models.Model):
    """Registro de atividades do sistema"""

    TIPO_CHOICES = [
        ("INFO", "Informação"),
        ("AVISO", "Aviso"),
        ("ERRO", "Erro"),
        ("DEBUG", "Depuração"),
    ]

    usuario = models.CharField(max_length=100)
    acao = models.CharField(max_length=255)
    tipo = models.CharField(
        max_length=10, choices=TIPO_CHOICES, default="INFO"
    )
    data = models.DateTimeField(default=timezone.now)
    detalhes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo}: {self.acao} por {self.usuario}"

    class Meta:
        verbose_name = "Log de Atividade"
        verbose_name_plural = "Logs de Atividades"
        ordering = [
            "-data"
        ]  # Garante que os logs mais recentes apareçam primeiro


