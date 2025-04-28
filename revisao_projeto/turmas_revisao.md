# Revisão da Funcionalidade: turmas

## Arquivos forms.py:


### Arquivo: turmas\forms.py

python
from django import forms
from importlib import import_module

# Adicionar esta função para obter o modelo Aluno dinamicamente
def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

# Adicionar esta função para obter o modelo Turma dinamicamente
def get_turma_model():
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

# Adicionar esta função para obter o modelo Curso dinamicamente
def get_curso_model():
    cursos_module = import_module("cursos.models")
    return getattr(cursos_module, "Curso")

class TurmaForm(forms.ModelForm):
    class Meta:
        model = get_turma_model()
        fields = [
            "nome", "curso", "vagas", "status", "data_inicio", "data_fim",
            "instrutor", "instrutor_auxiliar", "auxiliar_instrucao",
            "dias_semana", "local", "horario", "descricao"
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "curso": forms.Select(attrs={"class": "form-select"}),
            "vagas": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "data_inicio": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "data_fim": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "instrutor": forms.Select(attrs={"class": "form-control"}),
            "instrutor_auxiliar": forms.Select(attrs={"class": "form-control"}),
            "auxiliar_instrucao": forms.Select(attrs={"class": "form-control"}),
            "dias_semana": forms.TextInput(attrs={"class": "form-control"}),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "horario": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        labels = {
            "nome": "Nome da Turma",
            "curso": "Curso",
            "vagas": "Número de Vagas",
            "status": "Status",
            "data_inicio": "Data de Início",
            "data_fim": "Data de Término",
            "instrutor": "Instrutor Principal",
            "instrutor_auxiliar": "Instrutor Auxiliar",
            "auxiliar_instrucao": "Auxiliar de Instrução",
            "dias_semana": "Dias da Semana",
            "local": "Local",
            "horario": "Horário",
            "descricao": "Descrição",
        }
        help_texts = {
            "nome": "Digite um nome descritivo para a turma.",
            "vagas": "Quantidade máxima de alunos na turma.",
            "status": "Situação atual da turma.",
            "data_inicio": "Data prevista para início do curso.",
            "data_fim": "Data prevista para término do curso.",
            "dias_semana": "Exemplo: 'Segunda, Quarta e Sexta' ou 'Terças e Quintas'.",
            "horario": "Exemplo: '19h às 21h'.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar apenas alunos ativos para os campos de instrutor
        aluno_model = get_aluno_model()
        alunos_ativos = aluno_model.objects.filter(situacao="ATIVO")
        
        self.fields["instrutor"].queryset = alunos_ativos
        self.fields["instrutor_auxiliar"].queryset = alunos_ativos
        self.fields["auxiliar_instrucao"].queryset = alunos_ativos
        
        # Tornar os campos de instrutor auxiliar e auxiliar de instrução opcionais
        self.fields["instrutor_auxiliar"].required = False
        self.fields["auxiliar_instrucao"].required = False
        
        # Melhorias para garantir que as datas apareçam corretamente na edição
        if self.instance and self.instance.pk:
            if self.instance.data_inicio:
                # Garantir que a data esteja no formato correto para o campo de entrada
                self.initial['data_inicio'] = self.instance.data_inicio.strftime('%Y-%m-%d')
            
            if self.instance.data_fim:
                # Garantir que a data esteja no formato correto para o campo de entrada
                self.initial['data_fim'] = self.instance.data_fim.strftime('%Y-%m-%d')

    def clean(self):
        """Validação adicional dos campos do formulário."""
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get("data_inicio")
        data_fim = cleaned_data.get("data_fim")
        
        # Validar que a data de início seja hoje ou no futuro
        if data_inicio and data_inicio < timezone.localdate():
            self.add_error(
                "data_inicio", 
                "A data de início não pode ser anterior à data atual."
            )
        
        # Validar que a data de término seja depois da data de início
        if data_inicio and data_fim and data_fim < data_inicio:
            self.add_error(
                "data_fim", 
                "A data de término deve ser posterior à data de início."
            )
        
        # Validar que o instrutor principal não seja também instrutor auxiliar ou auxiliar de instrução
        instrutor = cleaned_data.get("instrutor")
        instrutor_auxiliar = cleaned_data.get("instrutor_auxiliar")
        auxiliar_instrucao = cleaned_data.get("auxiliar_instrucao")
        
        if instrutor and instrutor_auxiliar and instrutor == instrutor_auxiliar:
            self.add_error(
                "instrutor_auxiliar", 
                "O instrutor auxiliar não pode ser o mesmo que o instrutor principal."
            )
        
        if instrutor and auxiliar_instrucao and instrutor == auxiliar_instrucao:
            self.add_error(
                "auxiliar_instrucao", 
                "O auxiliar de instrução não pode ser o mesmo que o instrutor principal."
            )
        
        # Validar que instrutor auxiliar e auxiliar de instrução não sejam a mesma pessoa
        if instrutor_auxiliar and auxiliar_instrucao and instrutor_auxiliar == auxiliar_instrucao:
            self.add_error(
                "auxiliar_instrucao", 
                "O auxiliar de instrução não pode ser o mesmo que o instrutor auxiliar."
            )
        
        # Verificar se há vagas e se o número é positivo
        vagas = cleaned_data.get("vagas")
        if vagas is not None and vagas <= 0:
            self.add_error("vagas", "O número de vagas deve ser maior que zero.")
        
        return cleaned_data



## Arquivos views.py:


### Arquivo: turmas\views.py

python
"""
Views para o módulo de Turmas.

Padrão de Nomenclatura:
- Parâmetros de ID em URLs: Usamos o formato 'modelo_id' (ex: turma_id, aluno_id) 
  para maior clareza e para evitar ambiguidades em views que manipulam múltiplos modelos.
- Nos templates, continuamos passando o atributo 'id' do objeto (ex: turma.id), 
  mas nas views e URLs usamos nomes mais descritivos.
"""

from django.db.models import Q
from django.http import HttpResponse
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from django.core.paginator import Paginator
from importlib import import_module

# Importar a função utilitária centralizada
from core.utils import get_model_dynamically

def get_model(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    from importlib import import_module
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)

def get_aluno_model():
    return get_model_dynamically("alunos", "Aluno")

def get_turma_model():
    return get_model_dynamically("turmas", "Turma")

def get_curso_model():
    """Obtém o modelo Curso dinamicamente."""
    return get_model_dynamically("cursos", "Curso")

def get_matricula_model():
    """Obtém o modelo Matricula dinamicamente."""
    return get_model_dynamically("matriculas", "Matricula")

def get_atividade_academica_model():
    """Obtém o modelo AtividadeAcademica dinamicamente."""
    return get_model_dynamically("atividades", "AtividadeAcademica")

def get_frequencia_model():
    """Obtém o modelo Frequencia dinamicamente."""
    return get_model_dynamically("frequencias", "Frequencia")

def get_turma_form():
    """Obtém o formulário TurmaForm dinamicamente."""
    from importlib import import_module
    try:
        forms_module = import_module("turmas.forms")
        return getattr(forms_module, "TurmaForm")
    except (ImportError, AttributeError) as e:
        print(f"Erro ao importar TurmaForm: {e}")
        # Fallback para o formulário da core, se existir
        try:
            core_forms = import_module("core.forms")
            return getattr(core_forms, "TurmaForm")
        except (ImportError, AttributeError) as e:
            print(f"Erro ao importar TurmaForm da core: {e}")
            return None

@login_required
def listar_turmas(request):
    """Lista todas as turmas cadastradas."""
    try:
        # Alterar estas linhas para usar get_model_dynamically em vez de get_model
        Turma = get_model_dynamically("turmas", "Turma")
        Curso = get_model_dynamically("cursos", "Curso")
        
        # Obter parâmetros de busca e filtro
        query = request.GET.get("q", "")
        curso_id = request.GET.get("curso", "")
        
        # Filtrar turmas
        turmas = Turma.objects.all().select_related('curso', 'instrutor')
        
        if query:
            turmas = turmas.filter(
                Q(nome__icontains=query) |
                Q(curso__nome__icontains=query) |
                Q(instrutor__nome__icontains=query)
            )
        
        if curso_id:
            turmas = turmas.filter(curso__codigo_curso=curso_id)
        
        # Ordenar turmas por status, nome do curso e nome da turma
        turmas = turmas.order_by('status', 'curso__nome', 'nome')
        
        # Paginação
        paginator = Paginator(turmas, 10)  # 10 turmas por página
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        # Obter cursos para o filtro
        cursos = Curso.objects.all().order_by('nome')
        
        context = {
            "turmas": page_obj,
            "page_obj": page_obj,
            "query": query,
            "cursos": cursos,
            "curso_selecionado": curso_id,
            "total_turmas": turmas.count(),
        }
        
        return render(request, "turmas/listar_turmas.html", context)
    except Exception as e:
        # Em vez de mostrar a mensagem de erro, apenas retornamos uma lista vazia
        return render(
            request,
            "turmas/listar_turmas.html",
            {
                "turmas": [],
                "page_obj": None,
                "query": "",
                "cursos": [],
                "curso_selecionado": "",
                "error_message": f"Erro ao listar turmas: {str(e)}",
            },
        )

@login_required
def criar_turma(request):
    """Cria uma nova turma."""
    # Obter o formulário dinamicamente
    TurmaForm = get_turma_form()
    
    # Verificar se o formulário foi encontrado
    if TurmaForm is None:
        messages.error(request, "Erro ao carregar o formulário de turma. Contate o administrador.")
        return redirect("turmas:listar_turmas")
    
    if request.method == "POST":
        form = TurmaForm(request.POST)
        if form.is_valid():
            turma = form.save()
            messages.success(request, "Turma criada com sucesso!")
            return redirect("turmas:detalhar_turma", turma_id=turma.id)
    else:
        form = TurmaForm()
    
    # Obter todos os alunos ativos para o contexto
    try:
        Aluno = get_aluno_model()
        alunos = Aluno.objects.filter(situacao="ATIVO")
    except (ImportError, AttributeError):
        alunos = []
    
    # Certifique-se de que os cursos estão sendo carregados
    try:
        Curso = get_curso_model()
        cursos = Curso.objects.all().order_by('codigo_curso')
    except (ImportError, AttributeError):
        cursos = []
    
    return render(
        request,
        "turmas/criar_turma.html",
        {
            "form": form,
            "alunos": alunos,
            "cursos": cursos,
        },
    )

@login_required
def detalhar_turma(request, turma_id):
    """Exibe os detalhes de uma turma."""
    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=turma_id)
    # Verificar pendências na instrutoria
    tem_pendencia_instrutoria = (
        not turma.instrutor
        or not turma.instrutor_auxiliar
        or not turma.auxiliar_instrucao
    )
    # Calcular informações de matrículas
    alunos_matriculados_count = (
        turma.matriculas.filter(status="A").count()
        if hasattr(turma, "matriculas")
        else 0
    )
    vagas_disponiveis = turma.vagas - alunos_matriculados_count
    # Obter matrículas ativas
    matriculas = (
        turma.matriculas.filter(status="A")
        if hasattr(turma, "matriculas")
        else []
    )
    context = {
        "turma": turma,
        "matriculas": matriculas,
        "alunos_matriculados_count": alunos_matriculados_count,
        "vagas_disponiveis": vagas_disponiveis,
        "tem_pendencia_instrutoria": tem_pendencia_instrutoria,
    }
    return render(request, "turmas/detalhar_turma.html", context)

@login_required
def editar_turma(request, turma_id):
    """Edita uma turma existente."""
    # Obter o formulário dinamicamente
    TurmaForm = get_turma_form()
    
    # Verificar se o formulário foi encontrado
    if TurmaForm is None:
        messages.error(request, "Erro ao carregar o formulário de turma. Contate o administrador.")
        return redirect("turmas:listar_turmas")
    
    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=turma_id)
    if request.method == "POST":
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, "Turma atualizada com sucesso!")
            return redirect("turmas:detalhar_turma", turma_id=turma.id)
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = TurmaForm(instance=turma)
    # Obter todos os alunos ativos para o formulário
    try:
        Aluno = get_aluno_model()
        alunos = Aluno.objects.filter(situacao="ATIVO")
    except (ImportError, AttributeError):
        alunos = []
    return render(
        request,
        "turmas/editar_turma.html",
        {
            "form": form,
            "turma": turma,
            "alunos": alunos,  # Passar todos os alunos ativos para o template
        },
    )

@login_required
def excluir_turma(request, turma_id):
    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=turma_id)
    if request.method == "POST":
        turma.delete()
        messages.success(request, "Turma excluída com sucesso!")
        return redirect("turmas:listar_turmas")
    return render(request, "turmas/excluir_turma.html", {"turma": turma})

@login_required
def listar_alunos_turma(request, turma_id):
    """Lista todos os alunos matriculados em uma turma específica."""
    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=turma_id)
    
    # Obter alunos matriculados na turma
    try:
        Matricula = get_matricula_model()
        matriculas = Matricula.objects.filter(turma=turma, status="A").select_related('aluno')
        alunos = [matricula.aluno for matricula in matriculas]
    except (ImportError, AttributeError):
        # Fallback caso o modelo Matricula não esteja disponível
        alunos = []
    
    return render(
        request,
        "turmas/listar_alunos_turma.html",
        {
            "turma": turma,
            "alunos": alunos,
        },
    )

@login_required
def matricular_aluno(request, turma_id):
    """Matricula um aluno na turma."""
    Turma = get_model("turmas", "Turma")
    Aluno = get_model("alunos", "Aluno")
    Matricula = get_model("matriculas", "Matricula")
    
    turma = get_object_or_404(Turma, id=turma_id)
    
    if request.method == "POST":
        aluno_cpf = request.POST.get("aluno")
        if not aluno_cpf:
            messages.error(request, "Selecione um aluno para matricular.")
            return redirect("turmas:matricular_aluno", turma_id=turma_id)
        
        aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
        
        # Verificar se já existe matrícula
        if Matricula.objects.filter(aluno=aluno, turma=turma).exists():
            messages.warning(
                request,
                f"O aluno {aluno.nome} já está matriculado nesta turma."
            )
            return redirect("turmas:detalhar_turma", turma_id=turma_id)
        
        # Verificar se há vagas disponíveis
        if turma.vagas_disponiveis <= 0:
            messages.error(
                request,
                "Não há vagas disponíveis nesta turma."
            )
            return redirect("turmas:detalhar_turma", turma_id=turma_id)
        
        try:
            matricula = Matricula(
                aluno=aluno,
                turma=turma,
                data_matricula=timezone.now().date(),
                ativa=True,
                status="A",  # Ativa
            )
            matricula.save()
            messages.success(
                request,
                f"Aluno {aluno.nome} matriculado com sucesso na turma {turma.nome}."
            )
        except Exception as e:
            messages.error(request, f"Erro ao matricular aluno: {str(e)}")
        
        return redirect("turmas:detalhar_turma", turma_id=turma_id)
    
    # Para requisições GET, exibir formulário de matrícula
    alunos = Aluno.objects.filter(situacao="ATIVO")
    return render(
        request,
        "turmas/matricular_aluno.html",
        {"turma": turma, "alunos": alunos}
    )

@login_required
def remover_aluno_turma(request, turma_id, aluno_id):
    """Remove um aluno de uma turma."""
    Turma = get_turma_model()
    Aluno = get_aluno_model()
    
    turma = get_object_or_404(Turma, id=turma_id)
    aluno = get_object_or_404(Aluno, cpf=aluno_id)
    
    try:
        Matricula = get_matricula_model()
        # Verificar se o aluno está matriculado na turma
        matricula = get_object_or_404(Matricula, aluno=aluno, turma=turma, status="A")
        
        if request.method == "POST":
            # Cancelar a matrícula
            matricula.status = "C"  # Cancelada
            matricula.save()
            
            messages.success(
                request,
                f"Aluno {aluno.nome} removido da turma {turma.nome} com sucesso."
            )
            return redirect("turmas:detalhar_turma", turma_id=turma_id)
        
        return render(
            request,
            "turmas/confirmar_remocao_aluno.html",
            {"turma": turma, "aluno": aluno},
        )
    except (ImportError, AttributeError) as e:
        messages.error(request, f"Erro ao acessar o modelo de matrículas: {str(e)}")
        return redirect("turmas:detalhar_turma", turma_id=turma_id)

@login_required
def atualizar_instrutores(request, turma_id):
    """Atualiza os instrutores de uma turma."""
    Turma = get_turma_model()
    Aluno = get_aluno_model()
    
    turma = get_object_or_404(Turma, id=turma_id)
    
    if request.method == "POST":
        instrutor_cpf = request.POST.get("instrutor")
        instrutor_auxiliar_cpf = request.POST.get("instrutor_auxiliar")
        auxiliar_instrucao_cpf = request.POST.get("auxiliar_instrucao")
        
        # Atualizar instrutor principal
        if instrutor_cpf:
            instrutor = get_object_or_404(Aluno, cpf=instrutor_cpf)
            turma.instrutor = instrutor
        
        # Atualizar instrutor auxiliar
        if instrutor_auxiliar_cpf:
            instrutor_auxiliar = get_object_or_404(Aluno, cpf=instrutor_auxiliar_cpf)
            turma.instrutor_auxiliar = instrutor_auxiliar
        
        # Atualizar auxiliar de instrução
        if auxiliar_instrucao_cpf:
            auxiliar_instrucao = get_object_or_404(Aluno, cpf=auxiliar_instrucao_cpf)
            turma.auxiliar_instrucao = auxiliar_instrucao
        
        turma.save()
        messages.success(request, "Instrutores atualizados com sucesso!")
        return redirect("turmas:detalhar_turma", turma_id=turma_id)
    
    # Obter alunos elegíveis para serem instrutores
    try:
        alunos_elegiveis = Aluno.objects.filter(situacao="ATIVO")
    except (ImportError, AttributeError):
        alunos_elegiveis = []
    
    return render(
        request,
        "turmas/atualizar_instrutores.html",
        {
            "turma": turma,
            "alunos_elegiveis": alunos_elegiveis,
        },
    )

@login_required
def remover_instrutor(request, turma_id, tipo):
    """Remove um instrutor de uma turma."""
    Turma = get_turma_model()
    
    turma = get_object_or_404(Turma, id=turma_id)
    
    if request.method == "POST":
        if tipo == "principal":
            instrutor_nome = turma.instrutor.nome if turma.instrutor else "Não definido"
            turma.instrutor = None
            messages.success(request, f"Instrutor principal {instrutor_nome} removido com sucesso.")
        elif tipo == "auxiliar":
            instrutor_nome = turma.instrutor_auxiliar.nome if turma.instrutor_auxiliar else "Não definido"
            turma.instrutor_auxiliar = None
            messages.success(request, f"Instrutor auxiliar {instrutor_nome} removido com sucesso.")
        elif tipo == "auxiliar_instrucao":
            instrutor_nome = turma.auxiliar_instrucao.nome if turma.auxiliar_instrucao else "Não definido"
            turma.auxiliar_instrucao = None
            messages.success(request, f"Auxiliar de instrução {instrutor_nome} removido com sucesso.")
        
        turma.save()
        return redirect("turmas:detalhar_turma", turma_id=turma_id)
    
    # Determinar qual instrutor será removido
    instrutor_a_remover = None
    titulo = ""
    if tipo == "principal" and turma.instrutor:
        instrutor_a_remover = turma.instrutor
        titulo = "Remover Instrutor Principal"
    elif tipo == "auxiliar" and turma.instrutor_auxiliar:
        instrutor_a_remover = turma.instrutor_auxiliar
        titulo = "Remover Instrutor Auxiliar"
    elif tipo == "auxiliar_instrucao" and turma.auxiliar_instrucao:
        instrutor_a_remover = turma.auxiliar_instrucao
        titulo = "Remover Auxiliar de Instrução"
    
    if not instrutor_a_remover:
        messages.warning(request, "Não há instrutor para remover.")
        return redirect("turmas:detalhar_turma", turma_id=turma_id)
    
    return render(
        request,
        "turmas/confirmar_remocao_instrutor.html",
        {
            "turma": turma,
            "instrutor": instrutor_a_remover,
            "tipo": tipo,
            "titulo": titulo,
        },
    )

@login_required
def listar_atividades_turma(request, turma_id):
    """Lista todas as atividades de uma turma."""
    Turma = get_turma_model()
    
    turma = get_object_or_404(Turma, id=turma_id)
    
    try:
        AtividadeAcademica = get_atividade_academica_model()
        atividades = AtividadeAcademica.objects.filter(turma=turma).order_by('-data_inicio')
    except (ImportError, AttributeError):
        atividades = []
    
    return render(
        request,
        "turmas/listar_atividades_turma.html",
        {
            "turma": turma,
            "atividades": atividades,
        },
    )

@login_required
def adicionar_atividade_turma(request, turma_id):
    """Adiciona uma atividade a uma turma."""
    Turma = get_turma_model()
    
    turma = get_object_or_404(Turma, id=turma_id)
    
    try:
        # Importar o formulário AtividadeAcademicaForm dinamicamente
        from importlib import import_module
        forms_module = import_module("atividades.forms")
        AtividadeAcademicaForm = getattr(forms_module, "AtividadeAcademicaForm")
        
        if request.method == "POST":
            form = AtividadeAcademicaForm(request.POST)
            if form.is_valid():
                atividade = form.save(commit=False)
                atividade.turma = turma
                atividade.save()
                messages.success(request, "Atividade adicionada com sucesso!")
                return redirect("turmas:listar_atividades_turma", turma_id=turma_id)
        else:
            # Pré-selecionar a turma no formulário
            form = AtividadeAcademicaForm(initial={"turma": turma})
        
        return render(
            request,
            "turmas/adicionar_atividade_turma.html",
            {
                "turma": turma,
                "form": form,
            },
        )
    except (ImportError, AttributeError) as e:
        messages.error(request, f"Erro ao carregar o formulário de atividade: {str(e)}")
        return redirect("turmas:detalhar_turma", turma_id=turma_id)

@login_required
def registrar_frequencia_turma(request, turma_id):
    """Registra a frequência dos alunos em uma atividade da turma."""
    Turma = get_turma_model()
    
    turma = get_object_or_404(Turma, id=turma_id)
    
    try:
        # Obter matrículas ativas
        Matricula = get_matricula_model()
        matriculas = Matricula.objects.filter(turma=turma, status="A").select_related('aluno')
        alunos = [matricula.aluno for matricula in matriculas]
        
        # Obter atividades da turma
        AtividadeAcademica = get_atividade_academica_model()
        atividades = AtividadeAcademica.objects.filter(turma=turma).order_by('-data_inicio')
        
        if request.method == "POST":
            atividade_id = request.POST.get("atividade")
            if not atividade_id:
                messages.error(request, "Selecione uma atividade para registrar a frequência.")
                return redirect("turmas:registrar_frequencia_turma", turma_id=turma_id)
            
            atividade = get_object_or_404(AtividadeAcademica, id=atividade_id)
            presentes = request.POST.getlist("presentes")
            
            # Obter modelo de Frequencia
            Frequencia = get_frequencia_model()
            
            # Registrar frequência para cada aluno
            for aluno in alunos:
                presente = aluno.cpf in presentes
                justificativa = request.POST.get(f"justificativa_{aluno.cpf}", "")
                
                # Verificar se já existe registro para este aluno nesta atividade
                frequencia, created = Frequencia.objects.update_or_create(
                    aluno=aluno,
                    atividade=atividade,
                    defaults={
                        'presente': presente,
                        'justificativa': justificativa if not presente else "",
                    }
                )
            
            messages.success(request, "Frequência registrada com sucesso!")
            return redirect("turmas:detalhar_turma", turma_id=turma_id)
        
        return render(
            request,
            "turmas/registrar_frequencia_turma.html",
            {
                "turma": turma,
                "alunos": alunos,
                "atividades": atividades,
            },
        )
    
    except (ImportError, AttributeError) as e:
        messages.error(request, f"Erro ao registrar frequência: {str(e)}")
        return redirect("turmas:detalhar_turma", turma_id=turma_id)

@login_required
def relatorio_frequencia_turma(request, turma_id):
    """Gera um relatório de frequência para uma turma específica."""
    Turma = get_turma_model()
    
    turma = get_object_or_404(Turma, id=turma_id)
    
    try:
        # Obter matrículas ativas
        Matricula = get_matricula_model()
        matriculas = Matricula.objects.filter(turma=turma, status="A").select_related('aluno')
        alunos = [matricula.aluno for matricula in matriculas]
        
        # Obter frequências
        Frequencia = get_frequencia_model()
        
        # Obter datas das atividades da turma
        AtividadeAcademica = get_atividade_academica_model()
        atividades = AtividadeAcademica.objects.filter(turma=turma).order_by('data_inicio')
        datas_atividades = [atividade.data_inicio.date() for atividade in atividades]
        
        # Preparar dados para o relatório
        dados_frequencia = []
        for aluno in alunos:
            frequencias_aluno = Frequencia.objects.filter(
                aluno=aluno,
                atividade__turma=turma
            )
            
            # Calcular estatísticas
            total_presencas = frequencias_aluno.filter(presente=True).count()
            total_atividades = atividades.count()
            
            if total_atividades > 0:
                percentual_presenca = (total_presencas / total_atividades) * 100
            else:
                percentual_presenca = 0
            
            dados_frequencia.append({
                'aluno': aluno,
                'total_presencas': total_presencas,
                'total_atividades': total_atividades,
                'percentual_presenca': percentual_presenca,
                'frequencias': frequencias_aluno
            })
        
        context = {
            'turma': turma,
            'alunos': alunos,
            'datas_atividades': datas_atividades,
            'dados_frequencia': dados_frequencia,
        }
        
        return render(request, 'turmas/relatorio_frequencia_turma.html', context)
    
    except (ImportError, AttributeError) as e:
        messages.error(request, f"Erro ao gerar relatório de frequência: {str(e)}")
        return redirect("turmas:detalhar_turma", turma_id=turma_id)

@login_required
def exportar_turmas(request):
    """Exporta os dados das turmas para um arquivo CSV."""
    try:
        import csv
        from django.http import HttpResponse
        from django.utils import timezone
        
        Turma = get_turma_model()
        turmas = Turma.objects.all()
        
        # Criar resposta HTTP com cabeçalho para download de arquivo CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="turmas_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        # Criar escritor CSV
        writer = csv.writer(response)
        
        # Escrever cabeçalho
        writer.writerow([
            'ID', 'Nome', 'Curso', 'Status', 'Vagas',
            'Data Início', 'Data Fim', 'Instrutor',
            'Instrutor Auxiliar', 'Auxiliar de Instrução',
            'Dias da Semana', 'Local', 'Horário'
        ])
        
        # Escrever dados das turmas
        for turma in turmas:
            writer.writerow([
                turma.id,
                turma.nome,
                turma.curso.nome if turma.curso else 'N/A',
                turma.get_status_display(),
                turma.vagas,
                turma.data_inicio.strftime('%d/%m/%Y') if turma.data_inicio else 'N/A',
                turma.data_fim.strftime('%d/%m/%Y') if turma.data_fim else 'N/A',
                turma.instrutor.nome if turma.instrutor else 'N/A',
                turma.instrutor_auxiliar.nome if turma.instrutor_auxiliar else 'N/A',
                turma.auxiliar_instrucao.nome if turma.auxiliar_instrucao else 'N/A',
                turma.dias_semana,
                turma.local,
                turma.horario
            ])
        
        return response
    
    except Exception as e:
        messages.error(request, f"Erro ao exportar turmas: {str(e)}")
        return redirect("turmas:listar_turmas")

@login_required
def relatorio_turmas(request):
    """Gera um relatório com estatísticas sobre as turmas."""
    try:
        Turma = get_turma_model()
        
        # Estatísticas gerais
        total_turmas = Turma.objects.count()
        turmas_ativas = Turma.objects.filter(status='A').count()
        turmas_concluidas = Turma.objects.filter(status='C').count()
        turmas_canceladas = Turma.objects.filter(status='X').count()
        
        # Turmas por curso
        Curso = get_curso_model()
        cursos = Curso.objects.all()
        
        turmas_por_curso = []
        for curso in cursos:
            count = Turma.objects.filter(curso=curso).count()
            if count > 0:
                turmas_por_curso.append({
                    'curso': curso,
                    'count': count,
                    'percentage': (count / total_turmas * 100) if total_turmas > 0 else 0
                })
        
        # Turmas por instrutor
        Aluno = get_aluno_model()
        instrutores = Aluno.objects.filter(
            Q(turma_instrutor__isnull=False) |
            Q(turma_instrutor_auxiliar__isnull=False) |
            Q(turma_auxiliar_instrucao__isnull=False)
        ).distinct()
        
        turmas_por_instrutor = []
        for instrutor in instrutores:
            count_principal = Turma.objects.filter(instrutor=instrutor).count()
            count_auxiliar = Turma.objects.filter(instrutor_auxiliar=instrutor).count()
            count_aux_instrucao = Turma.objects.filter(auxiliar_instrucao=instrutor).count()
            
            if count_principal > 0 or count_auxiliar > 0 or count_aux_instrucao > 0:
                turmas_por_instrutor.append({
                    'instrutor': instrutor,
                    'count_principal': count_principal,
                    'count_auxiliar': count_auxiliar,
                    'count_aux_instrucao': count_aux_instrucao,
                    'total': count_principal + count_auxiliar + count_aux_instrucao
                })
        
        # Ordenar por total de turmas
        turmas_por_instrutor.sort(key=lambda x: x['total'], reverse=True)
        
        context = {
            'total_turmas': total_turmas,
            'turmas_ativas': turmas_ativas,
            'turmas_concluidas': turmas_concluidas,
            'turmas_canceladas': turmas_canceladas,
            'turmas_por_curso': turmas_por_curso,
            'turmas_por_instrutor': turmas_por_instrutor
        }
        
        return render(request, 'turmas/relatorio_turmas.html', context)
    
    except Exception as e:
        messages.error(request, f"Erro ao gerar relatório de turmas: {str(e)}")
        return redirect("turmas:listar_turmas")

@login_required
def dashboard_turmas(request):
    """Exibe um dashboard com informações e estatísticas sobre as turmas."""
    try:
        Turma = get_turma_model()
        
        # Estatísticas gerais
        total_turmas = Turma.objects.count()
        turmas_ativas = Turma.objects.filter(status='A').count()
        turmas_concluidas = Turma.objects.filter(status='C').count()
        turmas_canceladas = Turma.objects.filter(status='X').count()
        
        # Turmas recentes
        turmas_recentes = Turma.objects.order_by('-data_inicio')[:5]
        
        # Turmas com mais alunos
        Matricula = get_matricula_model()
        
        turmas_com_contagem = []
        for turma in Turma.objects.filter(status='A'):
            count = Matricula.objects.filter(turma=turma, status='A').count()
            turmas_com_contagem.append({
                'turma': turma,
                'alunos_count': count,
                'vagas_disponiveis': turma.vagas - count if turma.vagas > count else 0
            })
        
        # Ordenar por número de alunos
        turmas_com_contagem.sort(key=lambda x: x['alunos_count'], reverse=True)
        turmas_populares = turmas_com_contagem[:5]
        
        # Turmas por curso (para gráfico)
        Curso = get_curso_model()
        cursos = Curso.objects.all()
        
        dados_grafico = {
            'labels': [],
            'data': []
        }
        
        for curso in cursos:
            count = Turma.objects.filter(curso=curso).count()
            if count > 0:
                dados_grafico['labels'].append(curso.nome)
                dados_grafico['data'].append(count)
        
        context = {
            'total_turmas': total_turmas,
            'turmas_ativas': turmas_ativas,
            'turmas_concluidas': turmas_concluidas,
            'turmas_canceladas': turmas_canceladas,
            'turmas_recentes': turmas_recentes,
            'turmas_populares': turmas_populares,
            'dados_grafico': dados_grafico
        }
        
        return render(request, 'turmas/dashboard_turmas.html', context)
    
    except Exception as e:
        messages.error(request, f"Erro ao carregar dashboard de turmas: {str(e)}")
        return redirect("turmas:listar_turmas")


## Arquivos urls.py:


### Arquivo: turmas\urls.py

python
"""
Configuração de URLs para o módulo de Turmas.

Padrão de Nomenclatura:
- Usamos 'turma_id' como nome do parâmetro nas URLs para identificar o ID da turma
- Para URLs que envolvem múltiplos modelos, usamos nomes específicos para cada ID
  (ex: 'turma_id', 'aluno_cpf')

Exemplos:
- path('<int:turma_id>/', views.detalhar_turma, name='detalhar_turma')
- path('<int:turma_id>/cancelar-matricula/<str:aluno_cpf>/', views.cancelar_matricula, name='cancelar_matricula')
"""
from django.urls import path
from . import views

app_name = "turmas"

urlpatterns = [
    # URLs existentes
    path("", views.listar_turmas, name="listar_turmas"),
    path("criar/", views.criar_turma, name="criar_turma"),
    path("<int:turma_id>/", views.detalhar_turma, name="detalhar_turma"),
    path("<int:turma_id>/editar/", views.editar_turma, name="editar_turma"),
    path("<int:turma_id>/excluir/", views.excluir_turma, name="excluir_turma"),
    
    # URLs para gerenciamento de alunos na turma
    path("<int:turma_id>/alunos/", views.listar_alunos_turma, name="listar_alunos_turma"),
    path("<int:turma_id>/matricular/", views.matricular_aluno, name="matricular_aluno"),
    path("<int:turma_id>/remover-aluno/<str:aluno_id>/", views.remover_aluno_turma, name="remover_aluno_turma"),
    
    # URLs para gerenciamento de instrutores
    path("<int:turma_id>/instrutores/", views.atualizar_instrutores, name="atualizar_instrutores"),
    path("<int:turma_id>/remover-instrutor/<str:tipo>/", views.remover_instrutor, name="remover_instrutor"),
    
    # URLs para gerenciamento de atividades
    path("<int:turma_id>/atividades/", views.listar_atividades_turma, name="listar_atividades_turma"),
    path("<int:turma_id>/adicionar-atividade/", views.adicionar_atividade_turma, name="adicionar_atividade_turma"),
    
    # URLs para frequência
    path("<int:turma_id>/registrar-frequencia/", views.registrar_frequencia_turma, name="registrar_frequencia_turma"),
    path("<int:turma_id>/relatorio-frequencia/", views.relatorio_frequencia_turma, name="relatorio_frequencia_turma"),
    
    # URLs para exportação e relatórios
    path("exportar/", views.exportar_turmas, name="exportar_turmas"),
    path("relatorio/", views.relatorio_turmas, name="relatorio_turmas"),
    path("dashboard/", views.dashboard_turmas, name="dashboard_turmas"),
]



## Arquivos models.py:


### Arquivo: turmas\models.py

python
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Turma(models.Model):
    """
    Modelo para representar uma turma no sistema OMAUM.
    """
    STATUS_CHOICES = [
        ("A", "Ativa"),
        ("I", "Inativa"),
        ("C", "Cancelada"),
        ("F", "Finalizada"),
    ]

    # Informações básicas
    nome = models.CharField(max_length=100, verbose_name="Nome da Turma")
    curso = models.ForeignKey(
        "cursos.Curso",
        on_delete=models.CASCADE,
        verbose_name="Curso",
        related_name="turmas",
    )
    descricao = models.TextField(
        blank=True, null=True, verbose_name="Descrição"
    )

    # Datas
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_fim = models.DateField(verbose_name="Data de Fim")

    # Informações de agendamento
    dias_semana = models.CharField(max_length=100, blank=True, null=True, verbose_name="Dias da Semana")
    horario = models.CharField(max_length=100, blank=True, null=True, verbose_name="Horário")
    local = models.CharField(max_length=200, blank=True, null=True, verbose_name="Local")

    # Capacidade e status
    vagas = models.PositiveIntegerField(
        default=20,
        validators=[MinValueValidator(1)],
        verbose_name="Número de Vagas",
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default="A",
        verbose_name="Status",
    )

    # Instrutores
    instrutor = models.ForeignKey(
        "alunos.Aluno",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="turmas_como_instrutor",
        verbose_name="Instrutor Principal",
    )
    instrutor_auxiliar = models.ForeignKey(
        "alunos.Aluno",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="turmas_como_instrutor_auxiliar",
        verbose_name="Instrutor Auxiliar",
    )
    auxiliar_instrucao = models.ForeignKey(
        "alunos.Aluno",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="turmas_como_auxiliar_instrucao",
        verbose_name="Auxiliar de Instrução",
    )

    # Campos de alerta para instrutores
    alerta_instrutor = models.BooleanField(
        default=False, verbose_name="Alerta de Instrutor"
    )
    alerta_mensagem = models.TextField(
        blank=True, null=True, verbose_name="Mensagem de Alerta"
    )

    # Metadados
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Criado em"
    )
    updated_at = models.DateTimeField(
        default=timezone.now, verbose_name="Atualizado em"
    )

    def __str__(self):
        return f"{self.nome} - {self.curso.nome}"

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"
        ordering = ["-data_inicio"]

    @property
    def vagas_disponiveis(self):
        """Retorna o número de vagas disponíveis na turma."""
        vagas_ocupadas = self.matriculas.filter(status="A").count()
        return self.vagas - vagas_ocupadas

    @property
    def esta_ativa(self):
        """Verifica se a turma está ativa."""
        return self.status == "A"

    @property
    def esta_em_andamento(self):
        """Verifica se a turma está em andamento (começou mas não terminou)."""
        hoje = timezone.now().date()
        return self.data_inicio <= hoje <= self.data_fim and self.status == "A"

    def clean(self):
        super().clean()
        # Verificar se já existe uma turma com o mesmo nome (ignorando case)
        if self.nome:
            turmas_existentes = Turma.objects.filter(nome__iexact=self.nome)
            # Excluir a própria instância se estiver editando
            if self.pk:
                turmas_existentes = turmas_existentes.exclude(pk=self.pk)
            if turmas_existentes.exists():
                raise ValidationError(
                    {
                        "nome": "Já existe uma turma com este nome. "
                        "Por favor, escolha um nome diferente."
                    }
                )
        if self.data_fim < self.data_inicio:
            raise ValidationError(
                _("A data de fim não pode ser anterior à data de início.")
            )

    @classmethod
    def get_by_codigo(cls, codigo_turma):
        """Método auxiliar para buscar turma por código."""
        try:
            # Use o campo id em vez de codigo
            return Turma.objects.get(id=codigo_turma)
            
            # Ou use o campo nome
            # return Turma.objects.get(nome=codigo_turma)
        except Turma.DoesNotExist:
            return None


## Arquivos de Template:


### Arquivo: turmas\templates\turmas\adicionar_aluno.html

html
{% extends 'base.html' %}

{% block title %}Adicionar Aluno à Turma{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Adicionar Aluno à Turma: {{ turma.nome }}</h1>
        <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Voltar para Turma</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">Selecione um Aluno</h5>
        </div>
        <div class="card-body">
            {% if alunos %}
                <form method="post" class="mb-4">
                    {% csrf_token %}
                    
                    <div class="mb-3">
                        <label for="id_aluno" class="form-label">Aluno</label>
                        <select name="aluno" id="id_aluno" class="form-select" required>
                            <option value="">Selecione um aluno</option>
                            {% for aluno in alunos %}
                                <option value="{{ aluno.cpf }}">{{ aluno.nome }} (CPF: {{ aluno.cpf }})</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="d-flex justify-content-between">
                        <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Cancelar</a>
                        <button type="submit" class="btn btn-primary">Adicionar Aluno</button>
                    </div>
                </form>
                
                <div class="mt-3">
                    <p><strong>Informações da Turma:</strong></p>
                    <ul>
                        <li><strong>Nome:</strong> {{ turma.nome }}</li>
                        <li><strong>Curso:</strong> {{ turma.curso }}</li>
                        <li><strong>Vagas Disponíveis:</strong> {{ turma.vagas_disponiveis }}</li>
                        <li><strong>Status:</strong> {{ turma.get_status_display }}</li>
                    </ul>
                </div>
            {% else %}
                <div class="alert alert-info">
                    <p>Não há alunos disponíveis para matricular nesta turma.</p>
                    <p>Possíveis razões:</p>
                    <ul>
                        <li>Todos os alunos já estão matriculados nesta turma</li>
                        <li>Não há alunos cadastrados no sistema</li>
                    </ul>
                </div>
                <a href="{% url 'alunos:criar_aluno' %}" class="btn btn-primary">Cadastrar Novo Aluno</a>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Add select2 for better search experience if available
        if (typeof $.fn.select2 !== 'undefined') {
            $('#id_aluno').select2({
                placeholder: 'Selecione um aluno',
                width: '100%'
            });
        }
    });
</script>
{% endblock %}




### Arquivo: turmas\templates\turmas\cancelar_matricula.html

html
{% extends 'base.html' %}

{% block title %}Cancelar Matrícula{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Cancelar Matrícula</h1>
    
    <div class="alert alert-warning">
        <p>Você está prestes a cancelar a matrícula do aluno <strong>{{ matricula.aluno.nome }}</strong> na turma <strong>{{ matricula.turma.nome }}</strong>.</p>
        <p>Esta ação não pode ser desfeita. Deseja continuar?</p>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <button type="submit" class="btn btn-danger">Confirmar Cancelamento</button>
        <a href="{{ return_url }}" class="btn btn-secondary">Voltar</a>
    </form>
</div>
{% endblock %}




### Arquivo: turmas\templates\turmas\confirmar_cancelamento_matricula.html

html
{% extends 'base.html' %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card">
        <div class="card-header bg-danger text-white">
            <h4>Confirmar Cancelamento de Matrícula</h4>
        </div>
        <div class="card-body">
            <p class="lead">Você tem certeza que deseja cancelar a matrícula do aluno <strong>{{ aluno.nome }}</strong> na turma <strong>{{ turma.nome }}</strong>?</p>
            <p>Esta ação não poderá ser desfeita.</p>
            
            <div class="mt-4">
                <form method="post">
                    {% csrf_token %}
                    <div class="d-flex justify-content-between">
                        <a href="{% url 'turmas:listar_alunos_matriculados' turma.id %}" class="btn btn-secondary">Cancelar</a>
                        <button type="submit" class="btn btn-danger">Confirmar Cancelamento</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    
    <a href="javascript:history.back()" class="btn btn-secondary mt-3">Voltar</a>
</div>
{% endblock %}




### Arquivo: turmas\templates\turmas\criar_turma.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Nova Turma{% endblock %}

{% block extra_css %}
<style>
    /* Ocultar os selects originais */
    #id_instrutor, #id_instrutor_auxiliar, #id_auxiliar_instrucao {
        display: none;
    }
    
    /* Estilo para os resultados da busca */
    .list-group-item-action {
        cursor: pointer;
    }
    
    /* Estilo para o contêiner de instrutor selecionado */
    .selected-instrutor {
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
</style>
{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Nova Turma</h1>
        <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Voltar para a lista</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header bg-primary text-white">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.curso %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.vagas %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.status %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.dias_semana %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.data_inicio %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.data_fim %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.horario %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header bg-success text-white">
                <h5>Instrutores</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <!-- Instrutor Principal -->
                    <div class="col-md-4 mb-3">
                        <label for="search-instrutor" class="form-label">Instrutor Principal</label>
                        <input type="text" id="search-instrutor" class="form-control" placeholder="Digite parte do CPF, nome ou número iniciático..." autocomplete="off">
                        <div id="search-results-instrutor" class="list-group mt-2" style="display: none"></div>
                        <div id="selected-instrutor-container" class="p-3 border rounded mt-2 d-none">
                            <div id="selected-instrutor-info">
                                Nenhum instrutor selecionado
                            </div>
                        </div>
                        <div id="instrutor-error" class="alert alert-warning mt-2 d-none"></div>
                        <!-- Campo original oculto via CSS -->
                        {{ form.instrutor }}
                    </div>
                    
                    <!-- Instrutor Auxiliar -->
                    <div class="col-md-4 mb-3">
                        <label for="search-instrutor-auxiliar" class="form-label">Instrutor Auxiliar</label>
                        <input type="text" id="search-instrutor-auxiliar" class="form-control" placeholder="Digite parte do CPF, nome ou número iniciático..." autocomplete="off">
                        <div id="search-results-instrutor-auxiliar" class="list-group mt-2" style="display: none;"></div>
                        <div id="selected-instrutor-auxiliar-container" class="p-3 border rounded mt-2 d-none">
                            <div id="selected-instrutor-auxiliar-info">
                                Nenhum instrutor auxiliar selecionado
                            </div>
                        </div>
                        <div id="instrutor-auxiliar-error" class="alert alert-warning mt-2 d-none"></div>
                        <!-- Campo original oculto via CSS -->
                        {{ form.instrutor_auxiliar }}
                    </div>
                    
                    <!-- Auxiliar de Instrução -->
                    <div class="col-md-4 mb-3">
                        <label for="search-auxiliar-instrucao" class="form-label">Auxiliar de Instrução</label>
                        <input type="text" id="search-auxiliar-instrucao" class="form-control" placeholder="Digite parte do CPF, nome ou número iniciático..." autocomplete="off">
                        <div id="search-results-auxiliar-instrucao" class="list-group mt-2" style="display: none;"></div>
                        <div id="selected-auxiliar-instrucao-container" class="p-3 border rounded mt-2 d-none">
                            <div id="selected-auxiliar-instrucao-info">
                                Nenhum auxiliar de instrução selecionado
                            </div>
                        </div>
                        <div id="auxiliar-instrucao-error" class="alert alert-warning mt-2 d-none"></div>
                        <!-- Campo original oculto via CSS -->
                        {{ form.auxiliar_instrucao }}
                    </div>
                </div>
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> Você pode selecionar qualquer aluno como instrutor.
                    O sistema verificará a elegibilidade e mostrará um aviso caso o aluno não atenda aos requisitos.
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Criar Turma</button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/instrutor_search.js' %}"></script>
{% endblock %}




### Arquivo: turmas\templates\turmas\dashboard.html

html
{% extends 'base.html' %}

{% block title %}Dashboard de Turmas{% endblock %}

{% block extra_css %}
<style>
    .card-dashboard {
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s;
    }
    
    .card-dashboard:hover {
        transform: translateY(-5px);
    }
    
    .stat-card {
        border-left: 4px solid;
        border-radius: 4px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: white;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    .stat-card-primary {
        border-left-color: #4e73df;
    }
    
    .stat-card-success {
        border-left-color: #1cc88a;
    }
    
    .stat-card-info {
        border-left-color: #36b9cc;
    }
    
    .stat-card-warning {
        border-left-color: #f6c23e;
    }
    
    .stat-card-danger {
        border-left-color: #e74a3b;
    }
    
    .stat-card-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #5a5c69;
    }
    
    .stat-card-label {
        font-size: 0.8rem;
        color: #858796;
        text-transform: uppercase;
        font-weight: 600;
    }
    
    .stat-card-icon {
        font-size: 2rem;
        opacity: 0.3;
        color: #dddfeb;
    }
    
    .progress-sm {
        height: 8px;
    }
</style>
{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex flex-wrap justify-content-between align-items-center mb-3">
        <h1 class="mb-3 mb-md-0">Dashboard de Turmas</h1>
        
        <div class="btn-group">
            <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'turmas:relatorio_turmas' %}" class="btn btn-warning">
                <i class="fas fa-chart-bar"></i> Relatório Detalhado
            </a>
        </div>
    </div>
    
    <!-- Cards de Estatísticas -->
    <div class="row mb-4">
        <div class="col-xl-3 col-md-6">
            <div class="stat-card stat-card-primary">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <div class="stat-card-value">{{ total_turmas }}</div>
                        <div class="stat-card-label">Total de Turmas</div>
                    </div>
                    <div class="stat-card-icon">
                        <i class="fas fa-chalkboard-teacher"></i>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-xl-3 col-md-6">
            <div class="stat-card stat-card-success">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <div class="stat-card-value">{{ turmas_ativas }}</div>
                        <div class="stat-card-label">Turmas Ativas</div>
                    </div>
                    <div class="stat-card-icon">
                        <i class="fas fa-check-circle"></i>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-xl-3 col-md-6">
            <div class="stat-card stat-card-info">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <div class="stat-card-value">{{ turmas_planejadas }}</div>
                        <div class="stat-card-label">Turmas Planejadas</div>
                    </div>
                    <div class="stat-card-icon">
                        <i class="fas fa-calendar-alt"></i>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-xl-3 col-md-6">
            <div class="stat-card stat-card-warning">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <div class="stat-card-value">{{ turmas_concluidas }}</div>
                        <div class="stat-card-label">Turmas Concluídas</div>
                    </div>
                    <div class="stat-card-icon">
                        <i class="fas fa-flag-checkered"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Gráficos -->
    <div class="row mb-4">
        <!-- Gráfico de Status -->
        <div class="col-lg-6 mb-4">
            <div class="card card-dashboard">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">Distribuição por Status</h6>
                </div>
                <div class="card-body">
                    <div class="chart-pie">
                        <canvas id="statusChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Gráfico de Cursos -->
        <div class="col-lg-6 mb-4">
            <div class="card card-dashboard">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">Turmas por Curso</h6>
                </div>
                <div class="card-body">
                    <div class="chart-bar">
                        <canvas id="cursosChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Turmas Recentes e Turmas com Vagas -->
    <div class="row">
        <!-- Turmas Recentes -->
        <div class="col-lg-6 mb-4">
            <div class="card card-dashboard">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">Turmas Recentes</h6>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th>Nome</th>
                                    <th>Curso</th>
                                    <th>Status</th>
                                    <th>Ações</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for turma in turmas_recentes %}
                                <tr>
                                    <td>{{ turma.nome }}</td>
                                    <td>{{ turma.curso.nome }}</td>
                                    <td>
                                        {% if turma.status == 'ATIVA' %}
                                            <span class="badge bg-success">Ativa</span>
                                        {% elif turma.status == 'PLANEJADA' %}
                                            <span class="badge bg-info">Planejada</span>
                                        {% elif turma.status == 'CONCLUIDA' %}
                                            <span class="badge bg-secondary">Concluída</span>
                                        {% elif turma.status == 'CANCELADA' %}
                                            <span class="badge bg-danger">Cancelada</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i>
                                        </a>
                                    </td>
                                </tr>
                                {% empty %}
                                <tr>
                                    <td colspan="4" class="text-center">Nenhuma turma encontrada</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Turmas com Vagas -->
        <div class="col-lg-6 mb-4">
            <div class="card card-dashboard">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">Turmas com Vagas Disponíveis</h6>
                </div>
                <div class="card-body">
                    {% if turmas_com_vagas %}
                        {% for item in turmas_com_vagas %}
                            <h4 class="small font-weight-bold">
                                {{ item.turma.nome }} 
                                <span class="float-end">{{ item.vagas_disponiveis }} vagas</span>
                            </h4>
                            <div class="progress mb-4">
                                <div class="progress-bar bg-success" role="progressbar" style="width: {{ item.percentual_ocupacao }}%"
                                    aria-valuenow="{{ item.percentual_ocupacao }}" aria-valuemin="0" aria-valuemax="100">
                                </div>
                            </div>
                        {% endfor %}
                    {% else %}
                        <p class="text-center">Nenhuma turma com vagas disponíveis</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Dados para o gráfico de status
        const statusData = {
            labels: [{% for item in dados_status %}'{{ item.status }}'{% if not forloop.last %}, {% endif %}{% endfor %}],
            datasets: [{
                data: [{% for item in dados_status %}{{ item.quantidade }}{% if not forloop.last %}, {% endif %}{% endfor %}],
                backgroundColor: [{% for item in dados_status %}'{{ item.cor }}'{% if not forloop.last %}, {% endif %}{% endfor %}],
                hoverBackgroundColor: [{% for item in dados_status %}'{{ item.cor }}'{% if not forloop.last %}, {% endif %}{% endfor %}],
                hoverBorderColor: "rgba(234, 236, 244, 1)",
            }]
        };
        
        // Configuração do gráfico de status
        const statusConfig = {
            type: 'doughnut',
            data: statusData,
            options: {
                maintainAspectRatio: false,
                tooltips: {
                    backgroundColor: "rgb(255,255,255)",
                    bodyFontColor: "#858796",
                    borderColor: '#dddfeb',
                    borderWidth: 1,
                    xPadding: 15,
                    yPadding: 15,
                    displayColors: false,
                    caretPadding: 10,
                },
                legend: {
                    display: true,
                    position: 'bottom'
                },
                cutoutPercentage: 70,
            },
        };
        
        // Renderizar gráfico de status
        const statusChart = new Chart(
            document.getElementById('statusChart'),
            statusConfig
        );
        
        // Dados para o gráfico de cursos
        const cursosData = {
            labels: [{% for item in dados_cursos %}'{{ item.curso }}'{% if not forloop.last %}, {% endif %}{% endfor %}],
            datasets: [{
                label: "Turmas",
                backgroundColor: [{% for item in dados_cursos %}'{{ item.cor }}'{% if not forloop.last %}, {% endif %}{% endfor %}],
                hoverBackgroundColor: [{% for item in dados_cursos %}'{{ item.cor }}'{% if not forloop.last %}, {% endif %}{% endfor %}],
                data: [{% for item in dados_cursos %}{{ item.quantidade }}{% if not forloop.last %}, {% endif %}{% endfor %}],
            }]
        };
        
        // Configuração do gráfico de cursos
        const cursosConfig = {
            type: 'bar',
            data: cursosData,
            options: {
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        left: 10,
                        right: 25,
                        top: 25,
                        bottom: 0
                    }
                },
                scales: {
                    xAxes: [{
                        gridLines: {
                            display: false,
                            drawBorder: false
                        },
                        ticks: {
                            maxTicksLimit: 6
                        },
                        maxBarThickness: 25,
                    }],
                    yAxes: [{
                        ticks: {
                            min: 0,
                            maxTicksLimit: 5,
                            padding: 10,
                        },
                        gridLines: {
                            color: "rgb(234, 236, 244)",
                            zeroLineColor: "rgb(234, 236, 244)",
                            drawBorder: false,
                            borderDash: [2],
                            zeroLineBorderDash: [2]
                        }
                    }],
                },
                legend: {
                    display: false
                },
                tooltips: {
                    titleMarginBottom: 10,
                    titleFontColor: '#6e707e',
                    titleFontSize: 14,
                    backgroundColor: "rgb(255,255,255)",
                    bodyFontColor: "#858796",
                    borderColor: '#dddfeb',
                    borderWidth: 1,
                    xPadding: 15,
                    yPadding: 15,
                    displayColors: false,
                    caretPadding: 10,
                },
            }
        };
        
        // Renderizar gráfico de cursos
        const cursosChart = new Chart(
            document.getElementById('cursosChart'),
            cursosConfig
        );
    });
</script>
{% endblock %}



### Arquivo: turmas\templates\turmas\dashboard_turmas.html

html
{% extends 'base.html' %}

{% block title %}Dashboard de Turmas{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Dashboard de Turmas</h1>
        <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Voltar para Lista</a>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <h5 class="card-title">Total de Turmas</h5>
                    <p class="card-text display-4">{{ total_turmas }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center bg-success text-white">
                <div class="card-body">
                    <h5 class="card-title">Turmas Ativas</h5>
                    <p class="card-text display-4">{{ turmas_ativas }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center bg-info text-white">
                <div class="card-body">
                    <h5 class="card-title">Turmas Concluídas</h5>
                    <p class="card-text display-4">{{ turmas_concluidas }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center bg-danger text-white">
                <div class="card-body">
                    <h5 class="card-title">Turmas Canceladas</h5>
                    <p class="card-text display-4">{{ turmas_canceladas }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">Turmas Recentes</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Nome</th>
                                    <th>Curso</th>
                                    <th>Data de Início</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for turma in turmas_recentes %}
                                    <tr>
                                        <td>
                                            <a href="{% url 'turmas:detalhar_turma' turma.id %}">{{ turma.nome }}</a>
                                        </td>
                                        <td>{{ turma.curso.nome }}</td>
                                        <td>{{ turma.data_inicio|date:"d/m/Y" }}</td>
                                        <td>
                                            <span class="badge {% if turma.status == 'A' %}bg-success{% elif turma.status == 'C' %}bg-info{% else %}bg-danger{% endif %}">
                                                {{ turma.get_status_display }}
                                            </span>
                                        </td>
                                    </tr>
                                {% empty %}
                                    <tr>
                                        <td colspan="4" class="text-center">Nenhuma turma encontrada</td>
                                    </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">Turmas Mais Populares</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Nome</th>
                                    <th>Curso</th>
                                    <th>Alunos</th>
                                    <th>Vagas Disponíveis</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for item in turmas_populares %}
                                    <tr>
                                        <td>
                                            <a href="{% url 'turmas:detalhar_turma' item.turma.id %}">{{ item.turma.nome }}</a>
                                        </td>
                                        <td>{{ item.turma.curso.nome }}</td>
                                        <td>{{ item.alunos_count }}</td>
                                        <td>{{ item.vagas_disponiveis }}</td>
                                    </tr>
                                {% empty %}
                                    <tr>
                                        <td colspan="4" class="text-center">Nenhuma turma encontrada</td>
                                    </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-12">
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">Distribuição de Turmas por Curso</h5>
                </div>
                <div class="card-body">
                    <canvas id="turmasPorCursoChart" height="300"></canvas>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        var ctx = document.getElementById('turmasPorCursoChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: {{ dados_grafico.labels|safe }},
                datasets: [{
                    label: 'Número de Turmas',
                    data: {{ dados_grafico.data|safe }},
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    });
</script>
{% endblock %}



### Arquivo: turmas\templates\turmas\detalhar_turma.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Detalhes da Turma: {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Cabeçalho com título e botões de ação -->
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Detalhes da Turma: {{ turma.nome }}</h1>
        <div>
            <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary me-2">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'turmas:editar_turma' turma.id %}" class="btn btn-warning me-2">
                <i class="fas fa-edit"></i> Editar
            </a>
            {% if not matriculas %}
                <a href="{% url 'turmas:excluir_turma' turma.id %}" class="btn btn-danger">
                    <i class="fas fa-trash"></i> Excluir
                </a>
            {% endif %}
        </div>
    </div>
    
    {% if tem_pendencia_instrutoria %}
    <div class="alert alert-danger text-center mb-4 blink">
        <h5 class="mb-0"><strong>Pendência na Instrutoria</strong></h5>
    </div>
    {% endif %}
    
    <!-- Card de informações da turma com layout em colunas -->
    <div class="card mb-4 border-primary">
        <div class="card-header bg-primary text-white">
            <h5 class="card-title mb-0">Informações da Turma</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <!-- Coluna 1 -->
                <div class="col-md-4">
                    <div class="mb-3">
                        <h6 class="text-muted">Curso</h6>
                        <p class="fs-5">{{ turma.curso }}</p>
                    </div>
                    <div class="mb-3">
                        <h6 class="text-muted">Status</h6>
                        <p>
                            {% if turma.status == 'A' %}
                                <span class="badge bg-success">{{ turma.get_status_display }}</span>
                            {% elif turma.status == 'I' %}
                                <span class="badge bg-warning">{{ turma.get_status_display }}</span>
                            {% else %}
                                <span class="badge bg-secondary">{{ turma.get_status_display }}</span>
                            {% endif %}
                        </p>
                    </div>
                </div>
                
                <!-- Coluna 2 -->
                <div class="col-md-4">
                    <div class="mb-3">
                        <h6 class="text-muted">Data de Início</h6>
                        <p>{{ turma.data_inicio|date:"d/m/Y" }}</p>
                    </div>
                    <div class="mb-3">
                        <h6 class="text-muted">Data de Término</h6>
                        <p>{{ turma.data_fim|date:"d/m/Y"|default:"Não definida" }}</p>
                    </div>
                    <div class="mb-3">
                        <h6 class="text-muted">Local</h6>
                        <p>{{ turma.local|default:"Não informado" }}</p>
                    </div>
                </div>
                
                <!-- Coluna 3 - Estatísticas -->
                <div class="col-md-4">
                    <div class="card bg-light">
                        <div class="card-body text-center">
                            <h6 class="text-muted">Ocupação</h6>
                            <div class="d-flex justify-content-around mb-2">
                                <div>
                                    <h3 class="mb-0">{{ alunos_matriculados_count }}</h3>
                                    <small class="text-muted">Matriculados</small>
                                </div>
                                <div>
                                    <h3 class="mb-0">{{ turma.vagas }}</h3>
                                    <small class="text-muted">Total</small>
                                </div>
                                <div>
                                    <h3 class="mb-0">{{ vagas_disponiveis }}</h3>
                                    <small class="text-muted">Disponíveis</small>
                                </div>
                            </div>
                            
                            <!-- Barra de progresso -->
                            <div class="progress" style="height: 10px;">
                                <div class="progress-bar bg-primary" role="progressbar"
                                     style="width: {% widthratio alunos_matriculados_count turma.vagas 100 %}%;"
                                     aria-valuenow="{{ alunos_matriculados_count }}"
                                     aria-valuemin="0"
                                     aria-valuemax="{{ turma.vagas }}">
                                </div>
                            </div>
                            <small class="text-muted">{% widthratio alunos_matriculados_count turma.vagas 100 %}% ocupado</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Linha para Dias da Semana e Horário -->
            <div class="row mt-3">
                <div class="col-md-6">
                    <h6 class="text-muted">Dias da Semana</h6>
                    <p>{{ turma.dias_semana|default:"Não informado" }}</p>
                </div>
                <div class="col-md-6">
                    <h6 class="text-muted">Horário</h6>
                    <p>{{ turma.horario|default:"Não informado" }}</p>
                </div>
            </div>
            
            <!-- Descrição em linha separada -->
            {% if turma.descricao %}
            <div class="row mt-3">
                <div class="col-12">
                    <h6 class="text-muted">Descrição</h6>
                    <p>{{ turma.descricao }}</p>
                </div>
            </div>
            {% endif %}
        </div>
    </div>
    
    <!-- Card de instrutores -->
    <div class="card mb-4 border-success">
        <div class="card-header bg-success text-white">
            <h5 class="card-title mb-0">Instrutoria</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <!-- Instrutor Principal -->
                <div class="col-md-4">
                    <div class="card h-100">
                        <div class="card-header bg-light">
                            <h6 class="mb-0">Instrutor Principal</h6>
                        </div>
                        <div class="card-body text-center">
                            {% if turma.instrutor %}
                                <div class="mb-3">
                                    {% if turma.instrutor.foto %}
                                        <img src="{{ turma.instrutor.foto.url }}" alt="Foto de {{ turma.instrutor.nome }}"
                                             class="rounded-circle" style="width: 100px; height: 100px; object-fit: cover;">
                                    {% else %}
                                        <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center mx-auto"
                                             style="width: 100px; height: 100px; font-size: 36px;">
                                            {{ turma.instrutor.nome|first|upper }}
                                        </div>
                                    {% endif %}
                                </div>
                                <h5>{{ turma.instrutor.nome }}</h5>
                                <p class="text-muted">{{ turma.instrutor.numero_iniciatico|default:"" }}</p>
                                <a href="{% url 'alunos:detalhar_aluno' turma.instrutor.cpf %}" class="btn btn-sm btn-primary">
                                    Ver Perfil
                                </a>
                            {% else %}
                                <div class="text-muted py-4">
                                    <i class="fas fa-user-slash fa-3x mb-3"></i>
                                    <p>Nenhum instrutor designado</p>
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
                
                <!-- Instrutor Auxiliar -->
                <div class="col-md-4">
                    <div class="card h-100">
                        <div class="card-header bg-light">
                            <h6 class="mb-0">Instrutor Auxiliar</h6>
                        </div>
                        <div class="card-body text-center">
                            {% if turma.instrutor_auxiliar %}
                                <div class="mb-3">
                                    {% if turma.instrutor_auxiliar.foto %}
                                        <img src="{{ turma.instrutor_auxiliar.foto.url }}" alt="Foto de {{ turma.instrutor_auxiliar.nome }}"
                                             class="rounded-circle" style="width: 100px; height: 100px; object-fit: cover;">
                                    {% else %}
                                        <div class="rounded-circle bg-info text-white d-flex align-items-center justify-content-center mx-auto"
                                             style="width: 100px; height: 100px; font-size: 36px;">
                                            {{ turma.instrutor_auxiliar.nome|first|upper }}
                                        </div>
                                    {% endif %}
                                </div>
                                <h5>{{ turma.instrutor_auxiliar.nome }}</h5>
                                <p class="text-muted">{{ turma.instrutor_auxiliar.numero_iniciatico|default:"" }}</p>
                                <a href="{% url 'alunos:detalhar_aluno' turma.instrutor_auxiliar.cpf %}" class="btn btn-sm btn-info">
                                    Ver Perfil
                                </a>
                            {% else %}
                                <div class="text-muted py-4">
                                    <i class="fas fa-user-slash fa-3x mb-3"></i>
                                    <p>Nenhum instrutor designado</p>
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
                
                <!-- Auxiliar de Instrução -->
                <div class="col-md-4">
                    <div class="card h-100">
                        <div class="card-header bg-light">
                            <h6 class="mb-0">Auxiliar de Instrução</h6>
                        </div>
                        <div class="card-body text-center">
                            {% if turma.auxiliar_instrucao %}
                                <div class="mb-3">
                                    {% if turma.auxiliar_instrucao.foto %}
                                        <img src="{{ turma.auxiliar_instrucao.foto.url }}" alt="Foto de {{ turma.auxiliar_instrucao.nome }}"
                                             class="rounded-circle" style="width: 100px; height: 100px; object-fit: cover;">
                                    {% else %}
                                        <div class="rounded-circle bg-success text-white d-flex align-items-center justify-content-center mx-auto"
                                             style="width: 100px; height: 100px; font-size: 36px;">
                                            {{ turma.auxiliar_instrucao.nome|first|upper }}
                                        </div>
                                    {% endif %}
                                </div>
                                <h5>{{ turma.auxiliar_instrucao.nome }}</h5>
                                <p class="text-muted">{{ turma.auxiliar_instrucao.numero_iniciatico|default:"" }}</p>
                                <a href="{% url 'alunos:detalhar_aluno' turma.auxiliar_instrucao.cpf %}" class="btn btn-sm btn-success">
                                    Ver Perfil
                                </a>
                            {% else %}
                                <div class="text-muted py-4">
                                    <i class="fas fa-user-slash fa-3x mb-3"></i>
                                    <p>Nenhum auxiliar designado</p>
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Card de alunos matriculados -->
    <div class="card mb-4 border-primary">
        <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Alunos Matriculados</h5>
            <a href="{% url 'turmas:matricular_aluno' turma.id %}" class="btn btn-light">
                <i class="fas fa-user-plus"></i> Matricular Aluno
            </a>
        </div>
        <div class="card-body">
            {% if matriculas %}
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead class="table-light">
                            <tr>
                                <th>Nome</th>
                                <th>CPF</th>
                                <th>Nº Iniciático</th>
                                <th class="text-end">Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for matricula in matriculas %}
                            <tr>
                                <td>
                                    <div class="d-flex align-items-center">
                                        <div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center me-2"
                                             style="width: 32px; height: 32px; font-size: 14px;">
                                            {{ matricula.aluno.nome|first|upper }}
                                        </div>
                                        {{ matricula.aluno.nome }}
                                    </div>
                                </td>
                                <td>{{ matricula.aluno.cpf }}</td>
                                <td>{{ matricula.aluno.numero_iniciatico|default:"N/A" }}</td>
                                <td class="text-end">
                                    <a href="{% url 'alunos:detalhar_aluno' matricula.aluno.cpf %}" class="btn btn-sm btn-info">
                                        <i class="fas fa-eye"></i> Ver
                                    </a>
                                    <a href="{% url 'matriculas:cancelar_matricula_por_turma_aluno' turma.id matricula.aluno.cpf %}"
                                       class="btn btn-sm btn-danger"
                                       onclick="return confirm('Tem certeza que deseja cancelar esta matrícula?');">
                                        <i class="fas fa-times"></i> Cancelar
                                    </a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i> Nenhum aluno matriculado nesta turma.
                </div>
                <a href="{% url 'turmas:matricular_aluno' turma.id %}" class="btn btn-primary">
                    <i class="fas fa-user-plus"></i> Matricular Primeiro Aluno
                </a>
            {% endif %}
        </div>
        {% if matriculas %}
        <div class="card-footer text-muted">
            <small>Total: {{ alunos_matriculados_count }} aluno(s)</small>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}

{% block extra_css %}
<style>
    .bg-gradient-primary {
        background: linear-gradient(to right, #0d6efd, #0a58ca);
    }
    .bg-primary.bg-opacity-10 {
        background-color: rgba(13, 110, 253, 0.1) !important;
    }
    .bg-success.bg-opacity-10 {
        background-color: rgba(25, 135, 84, 0.1) !important;
    }
    .bg-info.bg-opacity-10 {
        background-color: rgba(13, 202, 240, 0.1) !important;
    }
    .rounded-circle {
        border-radius: 50% !important;
    }
    .progress {
        overflow: hidden;
        background-color: #e9ecef;
    }
    .card {
        transition: all 0.3s ease;
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 .5rem 1rem rgba(0,0,0,.15) !important;
    }
    .blink {
        animation: blinker 1s linear infinite;
    }
    @keyframes blinker {
        50% { opacity: 0.5; }
    }
</style>
{% endblock %}

{% block extra_js %}
<script>
    // Adicione aqui qualquer JavaScript específico para esta página
</script>
{% endblock %}




### Arquivo: turmas\templates\turmas\editar_turma.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Editar Turma{% endblock %}

{% block extra_css %}
<style>
    /* Ocultar os selects originais */
    #id_instrutor, #id_instrutor_auxiliar, #id_auxiliar_instrucao {
        display: none;
    }
    
    /* Estilo para os resultados da busca */
    .list-group-item-action {
        cursor: pointer;
    }
    
    /* Estilo para o contêiner de instrutor selecionado */
    .selected-instrutor {
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
</style>
{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Editar Turma: {{ turma.nome }}</h1>
        <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Voltar para a lista</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <!-- Seção de Informações Básicas -->
        <div class="card mb-4">
            <div class="card-header bg-primary text-white">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.curso %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.vagas %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.status %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.dias_semana %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.data_inicio %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.data_fim %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.horario %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Seção de Instrutores -->
        <div class="card mb-4">
            <div class="card-header bg-success text-white">
                <h5>Instrutores</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <!-- Instrutor Principal -->
                    <div class="col-md-4 mb-3">
                        <label for="search-instrutor" class="form-label">Instrutor Principal</label>
                        <input type="text" id="search-instrutor" class="form-control" placeholder="Digite parte do CPF, nome ou número iniciático..." autocomplete="off">
                        <div id="search-results-instrutor" class="list-group mt-2" style="display: none"></div>
                        <div id="selected-instrutor-container" class="p-3 border rounded mt-2 d-none">
                            <div id="selected-instrutor-info">
                                Nenhum instrutor selecionado
                            </div>
                        </div>
                        <div id="instrutor-error" class="alert alert-warning mt-2 d-none"></div>
                        <!-- Campo original oculto via CSS -->
                        {{ form.instrutor }}
                    </div>
                    
                    <!-- Instrutor Auxiliar -->
                    <div class="col-md-4 mb-3">
                        <label for="search-instrutor-auxiliar" class="form-label">Instrutor Auxiliar</label>
                        <input type="text" id="search-instrutor-auxiliar" class="form-control" placeholder="Digite parte do CPF, nome ou número iniciático..." autocomplete="off">
                        <div id="search-results-instrutor-auxiliar" class="list-group mt-2" style="display: none;"></div>
                        <div id="selected-instrutor-auxiliar-container" class="p-3 border rounded mt-2 d-none">
                            <div id="selected-instrutor-auxiliar-info">
                                Nenhum instrutor auxiliar selecionado
                            </div>
                        </div>
                        <div id="instrutor-auxiliar-error" class="alert alert-warning mt-2 d-none"></div>
                        <!-- Campo original oculto via CSS -->
                        {{ form.instrutor_auxiliar }}
                    </div>
                    
                    <!-- Auxiliar de Instrução -->
                    <div class="col-md-4 mb-3">
                        <label for="search-auxiliar-instrucao" class="form-label">Auxiliar de Instrução</label>
                        <input type="text" id="search-auxiliar-instrucao" class="form-control" placeholder="Digite parte do CPF, nome ou número iniciático..." autocomplete="off">
                        <div id="search-results-auxiliar-instrucao" class="list-group mt-2" style="display: none;"></div>
                        <div id="selected-auxiliar-instrucao-container" class="p-3 border rounded mt-2 d-none">
                            <div id="selected-auxiliar-instrucao-info">
                                Nenhum auxiliar de instrução selecionado
                            </div>
                        </div>
                        <div id="auxiliar-instrucao-error" class="alert alert-warning mt-2 d-none"></div>
                        <!-- Campo original oculto via CSS -->
                        {{ form.auxiliar_instrucao }}
                    </div>
                </div>
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> Você pode selecionar qualquer aluno como instrutor.
                    O sistema verificará a elegibilidade e mostrará um aviso caso o aluno não atenda aos requisitos.
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Atualizar Turma</button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/instrutor_search.js' %}"></script>
{% endblock %}




### Arquivo: turmas\templates\turmas\excluir_turma.html

html
{% extends 'base.html' %}

{% block title %}Excluir Turma: {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Turma: {{ turma.nome }}</h1>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    <div class="alert alert-danger">
        <p>Você tem certeza que deseja excluir esta turma?</p>
        <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
    </div>

    <form method="post">
        {% csrf_token %}
        <div class="mt-4">
            <button type="submit" class="btn btn-danger">Confirmar Exclusão</button>
            <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Cancelar</a>
        </div>    </form>
</div>
{% endblock %}





### Arquivo: turmas\templates\turmas\formulario_instrutoria.html

html
<div class="card mb-4">
    <div class="card-header bg-success text-white">
        <h5 class="mb-0">Instrutoria</h5>
    </div>
    <div class="card-body">
        <div class="row">
            <!-- Instrutor Principal -->
            <div class="col-md-4 mb-3">
                <label for="search-instrutor" class="form-label">Instrutor Principal</label>
                <input type="text" id="search-instrutor" class="form-control" 
                       placeholder="Digite parte do CPF, nome ou número iniciático..." 
                       autocomplete="off"
                       value="{{ turma.instrutor.nome|default:'' }}">
                <div id="search-results-instrutor" class="list-group mt-2" style="display: none;"></div>
                <div id="selected-instrutor-container" class="p-3 border rounded mt-2 {% if not turma.instrutor %}d-none{% endif %}">
                    <div id="selected-instrutor-info">
                        {% if turma.instrutor %}
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <strong>{{ turma.instrutor.nome }}</strong><br>
                                    CPF: {{ turma.instrutor.cpf }}<br>
                                    {% if turma.instrutor.numero_iniciatico %}
                                        Número Iniciático: {{ turma.instrutor.numero_iniciatico }}
                                    {% endif %}
                                </div>
                                <button type="button" class="btn btn-sm btn-outline-danger" id="remove-id_instrutor">
                                    <i class="fas fa-times"></i> Remover
                                </button>
                            </div>
                        {% else %}
                            Nenhum instrutor selecionado
                        {% endif %}
                    </div>
                </div>
                <div class="alert alert-danger mt-2 d-none"></div>
                <select name="instrutor" class="form-control d-none" id="id_instrutor">
                    <option value="">---------</option>
                    {% if turma.instrutor %}
                        <option value="{{ turma.instrutor.cpf }}" selected>{{ turma.instrutor.nome }}</option>
                    {% endif %}
                </select>
            </div>
            
            <!-- Instrutor Auxiliar -->
            <div class="col-md-4 mb-3">
                <label for="search-instrutor-auxiliar" class="form-label">Instrutor Auxiliar</label>
                <input type="text" id="search-instrutor-auxiliar" class="form-control" 
                       placeholder="Digite parte do CPF, nome ou número iniciático..." 
                       autocomplete="off"
                       value="{{ turma.instrutor_auxiliar.nome|default:'' }}">
                <div id="search-results-instrutor-auxiliar" class="list-group mt-2" style="display: none;"></div>
                <div id="selected-instrutor-auxiliar-container" class="p-3 border rounded mt-2 {% if not turma.instrutor_auxiliar %}d-none{% endif %}">
                    <div id="selected-instrutor-auxiliar-info">
                        {% if turma.instrutor_auxiliar %}
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <strong>{{ turma.instrutor_auxiliar.nome }}</strong><br>
                                    CPF: {{ turma.instrutor_auxiliar.cpf }}<br>
                                    {% if turma.instrutor_auxiliar.numero_iniciatico %}
                                        Número Iniciático: {{ turma.instrutor_auxiliar.numero_iniciatico }}
                                    {% endif %}
                                </div>
                                <button type="button" class="btn btn-sm btn-outline-danger" id="remove-id_instrutor_auxiliar">
                                    <i class="fas fa-times"></i> Remover
                                </button>
                            </div>
                        {% else %}
                            Nenhum instrutor auxiliar selecionado
                        {% endif %}
                    </div>
                </div>
                <div class="alert alert-danger mt-2 d-none"></div>
                <select name="instrutor_auxiliar" class="form-control d-none" id="id_instrutor_auxiliar">
                    <option value="">---------</option>
                    {% if turma.instrutor_auxiliar %}
                        <option value="{{ turma.instrutor_auxiliar.cpf }}" selected>{{ turma.instrutor_auxiliar.nome }}</option>
                    {% endif %}
                </select>
            </div>
            
            <!-- Auxiliar de Instrução -->
            <div class="col-md-4 mb-3">
                <label for="search-auxiliar-instrucao" class="form-label">Auxiliar de Instrução</label>
                <input type="text" id="search-auxiliar-instrucao" class="form-control" 
                       placeholder="Digite parte do CPF, nome ou número iniciático..." 
                       autocomplete="off"
                       value="{{ turma.auxiliar_instrucao.nome|default:'' }}">
                <div id="search-results-auxiliar-instrucao" class="list-group mt-2" style="display: none;"></div>
                <div id="selected-auxiliar-instrucao-container" class="p-3 border rounded mt-2 {% if not turma.auxiliar_instrucao %}d-none{% endif %}">
                    <div id="selected-auxiliar-instrucao-info">
                        {% if turma.auxiliar_instrucao %}
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <strong>{{ turma.auxiliar_instrucao.nome }}</strong><br>
                                    CPF: {{ turma.auxiliar_instrucao.cpf }}<br>
                                    {% if turma.auxiliar_instrucao.numero_iniciatico %}
                                        Número Iniciático: {{ turma.auxiliar_instrucao.numero_iniciatico }}
                                    {% endif %}
                                </div>
                                <button type="button" class="btn btn-sm btn-outline-danger" id="remove-id_auxiliar_instrucao">
                                    <i class="fas fa-times"></i> Remover
                                </button>
                            </div>
                        {% else %}
                            Nenhum auxiliar de instrução selecionado
                        {% endif %}
                    </div>
                </div>
                <div class="alert alert-danger mt-2 d-none"></div>
                <select name="auxiliar_instrucao" class="form-control d-none" id="id_auxiliar_instrucao">
                    <option value="">---------</option>
                    {% if turma.auxiliar_instrucao %}
                        <option value="{{ turma.auxiliar_instrucao.cpf }}" selected>{{ turma.auxiliar_instrucao.nome }}</option>
                    {% endif %}
                </select>
            </div>
        </div>
    </div>
</div>



### Arquivo: turmas\templates\turmas\listar_alunos_matriculados.html

html
{% extends 'base.html' %}

{% block title %}Alunos Matriculados - {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Alunos Matriculados - {{ turma.nome }}</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary me-2">Detalhes da Turma</a>
            <a href="{% url 'turmas:matricular_aluno' turma.id %}" class="btn btn-primary">Adicionar Aluno</a>        </div>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card">
        <div class="card-header bg-light">
            <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Total de Alunos: {{ total_alunos }}</h5>
                <div>
                    <form method="get" class="d-flex">
                        <input type="text" name="q" class="form-control me-2" placeholder="Buscar aluno..." value="{{ query }}">
                        <button type="submit" class="btn btn-outline-primary">Buscar</button>
                    </form>
                </div>
            </div>
        </div>
        <div class="card-body">
            {% if alunos %}
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead class="table-light">
                            <tr>
                                <th>Nome</th>
                                <th>CPF</th>
                                <th>Email</th>
                                <th>Data de Matrícula</th>
                                <th>Status</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for matricula in matriculas %}
                                <tr>
                                    <td>
                                        <div class="d-flex align-items-center">
                                            {% if matricula.aluno.foto %}
                                                <img src="{{ matricula.aluno.foto.url }}" alt="Foto de {{ matricula.aluno.nome }}" 
                                                     class="rounded-circle me-2" width="40" height="40" 
                                                     style="object-fit: cover;">
                                            {% else %}
                                                <div class="rounded-circle bg-secondary me-2 d-flex align-items-center justify-content-center" 
                                                     style="width: 40px; height: 40px; color: white;">
                                                    {{ matricula.aluno.nome|first|upper }}
                                                </div>
                                            {% endif %}
                                            {{ matricula.aluno.nome }}
                                        </div>
                                    </td>
                                    <td>{{ matricula.aluno.cpf }}</td>
                                    <td>{{ matricula.aluno.email }}</td>
                                    <td>{{ matricula.data_matricula|date:"d/m/Y" }}</td>
                                    <td>
                                        {% if matricula.status == 'A' %}
                                            <span class="badge bg-success">Ativa</span>
                                        {% elif matricula.status == 'C' %}
                                            <span class="badge bg-danger">Cancelada</span>
                                        {% elif matricula.status == 'F' %}
                                            <span class="badge bg-info">Finalizada</span>
                                        {% else %}
                                            <span class="badge bg-secondary">{{ matricula.get_status_display }}</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        <a href="{% url 'alunos:detalhar_aluno' matricula.aluno.cpf %}" class="btn btn-sm btn-info">Detalhes</a>
                                        <a href="{% url 'turmas:remover_aluno_turma' turma.id matricula.aluno.cpf %}" class="btn btn-sm btn-danger">Remover</a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                
                {% if page_obj.has_other_pages %}
                    <nav aria-label="Paginação">
                        <ul class="pagination justify-content-center mt-3">
                            {% if page_obj.has_previous %}
                                <li class="page-item">
                                    <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% if query %}&q={{ query }}{% endif %}">Anterior</a>
                                </li>
                            {% else %}
                                <li class="page-item disabled">
                                    <span class="page-link">Anterior</span>
                                </li>
                            {% endif %}

                            {% for num in page_obj.paginator.page_range %}
                                {% if page_obj.number == num %}
                                    <li class="page-item active">
                                        <span class="page-link">{{ num }}</span>
                                    </li>
                                {% else %}
                                    <li class="page-item">
                                        <a class="page-link" href="?page={{ num }}{% if query %}&q={{ query }}{% endif %}">{{ num }}</a>
                                    </li>
                                {% endif %}
                            {% endfor %}

                            {% if page_obj.has_next %}
                                <li class="page-item">
                                    <a class="page-link" href="?page={{ page_obj.next_page_number }}{% if query %}&q={{ query }}{% endif %}">Próxima</a>
                                </li>
                            {% else %}
                                <li class="page-item disabled">
                                    <span class="page-link">Próxima</span>
                                </li>
                            {% endif %}
                        </ul>
                    </nav>
                {% endif %}
            {% else %}
                <div class="alert alert-info text-center">
                    <p class="mb-0">Nenhum aluno matriculado nesta turma.</p>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: turmas\templates\turmas\listar_turmas.html

html
{% extends 'base.html' %}

{% block title %}Lista de Turmas{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Cabeçalho com título e botões na mesma linha -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Lista de Turmas</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'turmas:criar_turma' %}" class="btn btn-primary">Nova Turma</a>
        </div>
    </div>
    
    <!-- Barra de busca e filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <form method="get" class="row g-3">
                <div class="col-md-6">
                    <input type="text" name="q" class="form-control" placeholder="Buscar por nome, curso ou instrutor..." value="{{ query }}">
                </div>
                <div class="col-md-4">
                    <select name="curso" class="form-select" title="Selecione um curso" aria-label="Selecione um curso">
                        <option value="">Todos os cursos</option>
                        {% for curso in cursos %}
                            <option value="{{ curso.codigo_curso }}" {% if curso.codigo_curso|stringformat:"s" == curso_selecionado %}selected{% endif %}>{{ curso.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn btn-primary w-100">Filtrar</button>
                </div>
            </form>
        </div>
        <div class="card-body">
            {% if error_message %}
            <div class="alert alert-danger">
                {{ error_message }}
            </div>
            {% endif %}
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Curso</th>
                            <th>Nome da Turma</th>
                            <th>Instrutor</th>
                            <th>Status</th>
                            <th>Data Início</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for turma in turmas %}
                            <tr>
                                <td>{{ turma.curso.nome }}</td>
                                <td>{{ turma.nome }}</td>
                                <td>{{ turma.instrutor.nome|default:"Não definido" }}</td>
                                <td>
                                    <span class="badge {% if turma.status == 'A' %}bg-success{% elif turma.status == 'P' %}bg-info{% elif turma.status == 'C' %}bg-secondary{% else %}bg-danger{% endif %}">
                                        {{ turma.get_status_display }}
                                    </span>
                                </td>
                                <td>{{ turma.data_inicio|date:"d/m/Y"|default:"-" }}</td>
                                <td>
                                    <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-sm btn-info" title="Ver detalhes completos da turma">Detalhes</a>
                                    <a href="{% url 'turmas:editar_turma' turma.id %}" class="btn btn-sm btn-warning" title="Editar informações da turma">Editar</a>
                                    <a href="{% url 'turmas:excluir_turma' turma.id %}" class="btn btn-sm btn-danger" title="Excluir esta turma">Excluir</a>
                                </td>
                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="6" class="text-center">
                                    <p class="my-3">Nenhuma turma cadastrada.</p>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer">
            <p class="text-muted mb-0">Total: {{ total_turmas|default:"0" }} turma(s)</p>
            {% if page_obj.has_other_pages %}
                <nav aria-label="Paginação">
                    <ul class="pagination justify-content-center mb-0">
                        {% if page_obj.has_previous %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.previous_page_number }}&q={{ query }}&curso={{ curso_selecionado }}">Anterior</a>
                            </li>
                        {% else %}
                            <li class="page-item disabled">
                                <span class="page-link">Anterior</span>
                            </li>
                        {% endif %}

                        {% for num in page_obj.paginator.page_range %}
                            {% if page_obj.number == num %}
                                <li class="page-item active">
                                    <span class="page-link">{{ num }}</span>
                                </li>
                            {% else %}
                                <li class="page-item">
                                    <a class="page-link" href="?page={{ num }}&q={{ query }}&curso={{ curso_selecionado }}">{{ num }}</a>
                                </li>
                            {% endif %}
                        {% endfor %}

                        {% if page_obj.has_next %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.next_page_number }}&q={{ query }}&curso={{ curso_selecionado }}">Próxima</a>
                            </li>
                        {% else %}
                            <li class="page-item disabled">
                                <span class="page-link">Próxima</span>
                            </li>
                        {% endif %}
                    </ul>
                </nav>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: turmas\templates\turmas\matricular_aluno.html

html
{% extends 'base.html' %}

{% block title %}Matricular Aluno na Turma{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Matricular Aluno na Turma: {{ turma.nome }}</h1>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Turma</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ turma.nome }}</p>
            <p><strong>Curso:</strong> {{ turma.curso.nome }}</p>
            <p><strong>Vagas Disponíveis:</strong> {{ turma.vagas_disponiveis }}</p>
        </div>
    </div>
    
    <form method="post" id="matricula-form">
        {% csrf_token %}
        <div class="mb-3">
            <label for="aluno-search" class="form-label">Buscar Aluno</label>
            <div class="input-group">
                <input type="text" class="form-control" id="aluno-search" placeholder="Digite o nome, CPF ou número iniciático do aluno...">
                <button class="btn btn-outline-secondary" type="button" id="limpar-aluno">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div id="aluno-results" class="list-group mt-2 d-none"></div>
            <div id="aluno-selected" class="mt-2 d-none">
                <div class="card">
                    <div class="card-body d-flex align-items-center">
                        <div id="aluno-avatar" class="me-3">
                            <!-- Avatar do aluno será inserido aqui -->
                        </div>
                        <div>
                            <h5 id="aluno-nome" class="mb-1"></h5>
                            <p id="aluno-info" class="mb-0 text-muted"></p>
                        </div>
                    </div>
                </div>
            </div>
            <input type="hidden" name="aluno" id="aluno-id" required>
        </div>
        
        <div class="d-flex justify-content-between">
            <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Matricular Aluno</button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const alunoSearch = document.getElementById('aluno-search');
        const alunoResults = document.getElementById('aluno-results');
        const alunoSelected = document.getElementById('aluno-selected');
        const alunoId = document.getElementById('aluno-id');
        const alunoNome = document.getElementById('aluno-nome');
        const alunoInfo = document.getElementById('aluno-info');
        const alunoAvatar = document.getElementById('aluno-avatar');
        const limparAluno = document.getElementById('limpar-aluno');
        const form = document.getElementById('matricula-form');
        
        let searchTimeout;
        
        // Função para buscar alunos
        function buscarAlunos(query) {
            if (query.length < 2) {
                alunoResults.classList.add('d-none');
                return;
            }
            
            fetch(`/alunos/search/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    alunoResults.innerHTML = '';
                    
                    if (data.length === 0) {
                        const noResult = document.createElement('div');
                        noResult.className = 'list-group-item';
                        noResult.textContent = 'Nenhum aluno encontrado';
                        alunoResults.appendChild(noResult);
                    } else {
                        data.forEach(aluno => {
                            const item = document.createElement('a');
                            item.href = '#';
                            item.className = 'list-group-item list-group-item-action';
                            item.dataset.id = aluno.cpf;
                            item.dataset.nome = aluno.nome;
                            item.dataset.numero = aluno.numero_iniciatico;
                            item.dataset.foto = aluno.foto || '';
                            
                            // Criar conteúdo do item
                            let avatarHtml = '';
                            if (aluno.foto) {
                                avatarHtml = `<img src="${aluno.foto}" alt="${aluno.nome}" class="rounded-circle me-2" width="32" height="32">`;
                            } else {
                                avatarHtml = `<div class="rounded-circle bg-secondary text-white d-inline-flex align-items-center justify-content-center me-2" style="width: 32px; height: 32px;">${aluno.nome.charAt(0)}</div>`;
                            }
                            
                            item.innerHTML = `
                                ${avatarHtml}
                                <div>
                                    <div class="fw-bold">${aluno.nome}</div>
                                    <small class="text-muted">CPF: ${aluno.cpf} | Nº Iniciático: ${aluno.numero_iniciatico || 'N/A'}</small>
                                </div>
                            `;
                            
                            item.addEventListener('click', function(e) {
                                e.preventDefault();
                                selecionarAluno(this.dataset);
                            });
                            
                            alunoResults.appendChild(item);
                        });
                    }
                    
                    alunoResults.classList.remove('d-none');
                })
                .catch(error => {
                    console.error('Erro ao buscar alunos:', error);
                });
        }
        
        // Função para selecionar um aluno
        function selecionarAluno(dados) {
            alunoId.value = dados.id;
            alunoNome.textContent = dados.nome;
            alunoInfo.textContent = `CPF: ${dados.id} | Nº Iniciático: ${dados.numero || 'N/A'}`;
            
            // Configurar avatar
            if (dados.foto) {
                alunoAvatar.innerHTML = `<img src="${dados.foto}" alt="${dados.nome}" class="rounded-circle" width="48" height="48">`;
            } else {
                alunoAvatar.innerHTML = `<div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center" style="width: 48px; height: 48px; font-size: 20px;">${dados.nome.charAt(0)}</div>`;
            }
            
            // Mostrar seleção e esconder resultados
            alunoSelected.classList.remove('d-none');
            alunoResults.classList.add('d-none');
            alunoSearch.value = '';
        }
        
        // Função para limpar seleção
        function limparSelecao() {
            alunoId.value = '';
            alunoSelected.classList.add('d-none');
            alunoSearch.value = '';
            alunoResults.classList.add('d-none');
        }
        
        // Event listeners
        alunoSearch.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                buscarAlunos(this.value);
            }, 300);
        });
        
        limparAluno.addEventListener('click', limparSelecao);
        
        // Fechar resultados ao clicar fora
        document.addEventListener('click', function(e) {
            if (!alunoSearch.contains(e.target) && !alunoResults.contains(e.target)) {
                alunoResults.classList.add('d-none');
            }
        });
        
        // Validar formulário antes de enviar
        form.addEventListener('submit', function(e) {
            if (!alunoId.value) {
                e.preventDefault();
                alert('Por favor, selecione um aluno para matricular.');
            }
        });
    });
</script>
{% endblock %}




### Arquivo: turmas\templates\turmas\registrar_frequencia_turma.html

html
{% extends 'base.html' %}

{% block title %}Registrar Frequência - {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Registrar Frequência</h1>
        <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Voltar para Turma</a>
    </div>
    
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">{{ turma.nome }} - {{ turma.curso.nome }}</h5>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="data_atividade" class="form-label">Data da Atividade</label>
                    <input type="date" class="form-control" id="data_atividade" name="data_atividade" required>
                </div>
                
                <div class="mb-3">
                    <label for="atividade" class="form-label">Atividade</label>
                    <select class="form-select" id="atividade" name="atividade" required>
                        <option value="">Selecione uma atividade</option>
                        {% for atividade in atividades %}
                            <option value="{{ atividade.id }}">{{ atividade.nome }} - {{ atividade.data_inicio|date:"d/m/Y" }}</option>
                        {% endfor %}
                    </select>
                </div>
                
                <h5 class="mt-4 mb-3">Lista de Alunos</h5>
                
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Aluno</th>
                                <th>Presente</th>
                                <th>Justificativa (se ausente)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for aluno in alunos %}
                                <tr>
                                    <td>{{ aluno.nome }}</td>
                                    <td>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" name="presentes" value="{{ aluno.cpf }}" id="presente_{{ aluno.cpf }}" checked>
                                            <label class="form-check-label" for="presente_{{ aluno.cpf }}">
                                                Presente
                                            </label>
                                        </div>
                                    </td>
                                    <td>
                                        <textarea class="form-control" name="justificativa_{{ aluno.cpf }}" rows="1" placeholder="Justificativa para ausência"></textarea>
                                    </td>
                                </tr>
                            {% empty %}
                                <tr>
                                    <td colspan="3" class="text-center">Nenhum aluno matriculado nesta turma.</td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                
                <div class="mt-4">
                    <button type="submit" class="btn btn-primary">Registrar Frequência</button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: turmas\templates\turmas\relatorio_frequencia_turma.html

html
{% extends 'base.html' %}

{% block title %}Relatório de Frequência - {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Relatório de Frequência</h1>
        <div>
            <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary me-2">Voltar para Turma</a>
            <button onclick="window.print()" class="btn btn-primary">
                <i class="fas fa-print"></i> Imprimir Relatório
            </button>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">{{ turma.nome }} - {{ turma.curso.nome }}</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Instrutor:</strong> {{ turma.instrutor.nome|default:"Não definido" }}</p>
                    <p><strong>Instrutor Auxiliar:</strong> {{ turma.instrutor_auxiliar.nome|default:"Não definido" }}</p>
                    <p><strong>Auxiliar de Instrução:</strong> {{ turma.auxiliar_instrucao.nome|default:"Não definido" }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Data de Início:</strong> {{ turma.data_inicio|date:"d/m/Y" }}</p>
                    <p><strong>Data de Término:</strong> {{ turma.data_fim|date:"d/m/Y"|default:"Não definida" }}</p>
                    <p><strong>Total de Alunos:</strong> {{ alunos|length }}</p>
                </div>
            </div>
        </div>
    </div>
    
    {% if dados_frequencia %}
        <div class="card mb-4">
            <div class="card-header">
                <h5 class="mb-0">Resumo de Frequência</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Aluno</th>
                                <th>Presenças</th>
                                <th>Total de Atividades</th>
                                <th>Percentual</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for dado in dados_frequencia %}
                                <tr>
                                    <td>{{ dado.aluno.nome }}</td>
                                    <td>{{ dado.total_presencas }}</td>
                                    <td>{{ dado.total_atividades }}</td>
                                    <td>{{ dado.percentual_presenca|floatformat:1 }}%</td>
                                    <td>
                                        {% if dado.percentual_presenca >= 75 %}
                                            <span class="badge bg-success">Aprovado</span>
                                        {% else %}
                                            <span class="badge bg-danger">Reprovado</span>
                                        {% endif %}
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5 class="mb-0">Detalhamento por Atividade</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped table-bordered">
                        <thead>
                            <tr>
                                <th>Aluno</th>
                                {% for data in datas_atividades %}
                                    <th>{{ data|date:"d/m/Y" }}</th>
                                {% endfor %}
                            </tr>
                        </thead>
                        <tbody>
                            {% for dado in dados_frequencia %}
                                <tr>
                                    <td>{{ dado.aluno.nome }}</td>
                                    {% for data in datas_atividades %}
                                        <td class="text-center">
                                            {% for freq in dado.frequencias %}
                                                {% if freq.atividade.data_inicio.date == data %}
                                                    {% if freq.presente %}
                                                        <span class="text-success"><i class="fas fa-check"></i></span>
                                                    {% else %}
                                                        <span class="text-danger"><i class="fas fa-times"></i></span>
                                                    {% endif %}
                                                {% endif %}
                                            {% endfor %}
                                        </td>
                                    {% endfor %}
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    {% else %}
        <div class="alert alert-info">
            <p>Não há dados de frequência disponíveis para esta turma.</p>
        </div>
    {% endif %}
</div>
{% endblock %}



### Arquivo: turmas\templates\turmas\relatorio_turmas.html

html
{% extends 'base.html' %}

{% block title %}Relatório de Turmas{% endblock %}

{% block extra_css %}
<style>
    .card-counter {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        padding: 20px;
        background-color: #fff;
        height: 100%;
        border-radius: 5px;
        transition: .3s linear all;
    }
    
    .card-counter.primary {
        background-color: #007bff;
        color: #FFF;
    }
    
    .card-counter.success {
        background-color: #28a745;
        color: #FFF;
    }
    
    .card-counter.info {
        background-color: #17a2b8;
        color: #FFF;
    }
    
    .card-counter.warning {
        background-color: #ffc107;
        color: #FFF;
    }
    
    .card-counter.danger {
        background-color: #dc3545;
        color: #FFF;
    }
    
    .card-counter i {
        font-size: 4em;
        opacity: 0.3;
    }
    
    .card-counter .count-numbers {
        position: absolute;
        right: 35px;
        top: 20px;
        font-size: 32px;
        display: block;
    }
    
    .card-counter .count-name {
        position: absolute;
        right: 35px;
        top: 65px;
        font-style: italic;
        text-transform: capitalize;
        opacity: 0.7;
        display: block;
    }
    
    .progress-bar-container {
        height: 25px;
        margin-bottom: 10px;
    }
    
    .progress-bar-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
    }
</style>
{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Relatório de Turmas</h1>
        <div>
            <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary me-2">Voltar para Lista</a>
            <button onclick="window.print()" class="btn btn-primary">
                <i class="fas fa-print"></i> Imprimir Relatório
            </button>
        </div>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <h5 class="card-title">Total de Turmas</h5>
                    <p class="card-text display-4">{{ total_turmas }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center bg-success text-white">
                <div class="card-body">
                    <h5 class="card-title">Turmas Ativas</h5>
                    <p class="card-text display-4">{{ turmas_ativas }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center bg-info text-white">
                <div class="card-body">
                    <h5 class="card-title">Turmas Concluídas</h5>
                    <p class="card-text display-4">{{ turmas_concluidas }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center bg-danger text-white">
                <div class="card-body">
                    <h5 class="card-title">Turmas Canceladas</h5>
                    <p class="card-text display-4">{{ turmas_canceladas }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">Turmas por Curso</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Curso</th>
                                    <th>Quantidade</th>
                                    <th>Percentual</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for item in turmas_por_curso %}
                                    <tr>
                                        <td>{{ item.curso.nome }}</td>
                                        <td>{{ item.count }}</td>
                                        <td>{{ item.percentage|floatformat:1 }}%</td>
                                    </tr>
                                {% empty %}
                                    <tr>
                                        <td colspan="3" class="text-center">Nenhum dado disponível</td>
                                    </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">Turmas por Instrutor</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Instrutor</th>
                                    <th>Principal</th>
                                    <th>Auxiliar</th>
                                    <th>Aux. Instrução</th>
                                    <th>Total</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for item in turmas_por_instrutor %}
                                    <tr>
                                        <td>{{ item.instrutor.nome }}</td>
                                        <td>{{ item.count_principal }}</td>
                                        <td>{{ item.count_auxiliar }}</td>
                                        <td>{{ item.count_aux_instrucao }}</td>
                                        <td>{{ item.total }}</td>
                                    </tr>
                                {% empty %}
                                    <tr>
                                        <td colspan="5" class="text-center">Nenhum dado disponível</td>
                                    </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    // Filtros personalizados para os cálculos nas barras de progresso
    function div(a, b) {
        return a / b;
    }
    
    function mul(a, b) {
        return a * b;
    }
</script>
{% endblock %}



### Arquivo: turmas\templates\turmas\turma_form.html

html
{% extends 'base.html' %}

{% block content %}
  <h1>Criar Turma</h1>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Criar</button>
  </form>
{% endblock %}

