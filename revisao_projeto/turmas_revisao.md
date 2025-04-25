# Revisão da Funcionalidade: turmas

## Arquivos forms.py:


### Arquivo: turmas\forms.py

python
from django import forms
from importlib import import_module
from django.utils import timezone


def get_turma_model():
    """Obtém o modelo Turma dinamicamente para evitar importações circulares."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente para evitar importações circulares."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


class TurmaForm(forms.ModelForm):
    """
    Formulário para criação e edição de turmas.
    """

    class Meta:
        model = get_turma_model()
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
            # Melhoria nos widgets de data para garantir o formato correto
            "data_inicio": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "data_fim": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "instrutor": forms.Select(attrs={"class": "form-select"}),
            "instrutor_auxiliar": forms.Select(
                attrs={"class": "form-select"}
            ),
            "auxiliar_instrucao": forms.Select(
                attrs={"class": "form-select"}
            ),
            "dias_semana": forms.TextInput(attrs={"class": "form-control"}),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "horario": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
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
import csv
import io
import xlsxwriter
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Avg
from django.utils import timezone
from importlib import import_module

from .models import Turma
from cursos.models import Curso
from alunos.models import Aluno
from matriculas.models import Matricula

def get_model(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)


def get_turma_model():
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


@login_required
def listar_turmas(request):
    Turma = get_turma_model()
    turmas = Turma.objects.all()
    # Preparar informações adicionais para cada turma
    turmas_com_info = []
    for turma in turmas:
        # Verificar pendências na instrutoria
        tem_pendencia_instrutoria = (
            not turma.instrutor
            or not turma.instrutor_auxiliar
            or not turma.auxiliar_instrucao
        )
        # Calcular vagas disponíveis
        total_alunos = (
            turma.matriculas.filter(status="A").count()
            if hasattr(turma, "matriculas")
            else 0
        )
        vagas_disponiveis = turma.vagas - total_alunos

        turmas_com_info.append(
            {
                "turma": turma,
                "total_alunos": total_alunos,
                "vagas_disponiveis": vagas_disponiveis,
                "tem_pendencia_instrutoria": tem_pendencia_instrutoria,
            }
        )

    return render(
        request,
        "turmas/listar_turmas.html",
        {"turmas_com_info": turmas_com_info},
    )


@login_required
def criar_turma(request):
    """Cria uma nova turma."""
    if request.method == "POST":
        form = TurmaForm(request.POST)
        if form.is_valid():
            turma = form.save()
            messages.success(request, "Turma criada com sucesso!")
            return redirect("turmas:detalhar_turma", id=turma.id)
    else:
        form = TurmaForm()
    
    # Obter todos os alunos ativos para o contexto
    try:
        Aluno = import_module("alunos.models").Aluno
        alunos = Aluno.objects.filter(situacao="ATIVO")
    except (ImportError, AttributeError):
        alunos = []
    
    # Certifique-se de que os cursos estão sendo carregados
    from cursos.models import Curso
    cursos = Curso.objects.all().order_by('codigo_curso')
    
    # Adicione um log para depuração
    print(f"Carregando {len(cursos)} cursos")
    
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
def detalhar_turma(request, id):
    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=id)
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
def editar_turma(request, id):
    """Edita uma turma existente."""
    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=id)
    if request.method == "POST":
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, "Turma atualizada com sucesso!")
            return redirect("turmas:detalhar_turma", id=turma.id)
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = TurmaForm(instance=turma)
    # Obter todos os alunos ativos para o formulário
    Aluno = get_model("alunos", "Aluno")
    alunos = Aluno.objects.filter(situacao="ATIVO")
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
def excluir_turma(request, id):
    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=id)
    if request.method == "POST":
        turma.delete()
        messages.success(request, "Turma excluída com sucesso!")
        return redirect("turmas:listar_turmas")
    return render(request, "turmas/excluir_turma.html", {"turma": turma})


@login_required
def listar_alunos_matriculados(request, id):
    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=id)
    alunos = turma.alunos.all() if hasattr(turma, "alunos") else []
    return render(
        request,
        "turmas/listar_alunos_matriculados.html",
        {"turma": turma, "alunos": alunos},
    )


@login_required
def matricular_aluno(request, turma_id):
    """Matricula um aluno em uma turma específica."""
    Turma = get_turma_model()
    Aluno = get_aluno_model()
    turma = get_object_or_404(Turma, id=id)
    if request.method == "POST":
        aluno_cpf = request.POST.get("aluno")
        aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
        # Verificar se existe um modelo de Matricula
        try:
            Matricula = import_module("matriculas.models").Matricula
            # Criar uma matrícula em vez de adicionar diretamente à relação many-to-many
            Matricula.objects.create(
                aluno=aluno,
                turma=turma,
                data_matricula=timezone.now().date(),
                status="A",  # Ativa
            )
        except (ImportError, AttributeError):
            # Fallback: adicionar diretamente à relação many-to-many se o modelo Matricula não existir
            if hasattr(turma, "alunos"):
                turma.alunos.add(aluno)
        messages.success(
            request, f"Aluno {aluno.nome} matriculado com sucesso!"
        )
        return redirect("turmas:detalhar_turma", id=turma.id)
    # Obter alunos disponíveis para matrícula
    try:
        # Se existir um modelo de Matricula, excluir alunos já matriculados
        Matricula = import_module("matriculas.models").Matricula
        alunos_matriculados = Matricula.objects.filter(
            turma=turma, status="A"
        ).values_list("aluno__cpf", flat=True)
        alunos_disponiveis = Aluno.objects.exclude(cpf__in=alunos_matriculados)
    except (ImportError, AttributeError):
        # Fallback
        if hasattr(turma, "alunos"):
            alunos_disponiveis = Aluno.objects.exclude(turmas=turma)
        else:
            alunos_disponiveis = Aluno.objects.all()
    # Adicionar informação de vagas disponíveis
    vagas_disponiveis = (
        turma.vagas_disponiveis
        if hasattr(turma, "vagas_disponiveis")
        else turma.vagas
    )
    return render(
        request,
        "turmas/matricular_aluno.html",
        {
            "turma": turma,
            "alunos": alunos_disponiveis,
            "vagas_disponiveis": vagas_disponiveis,
        },
    )


@login_required
def cancelar_matricula(request, turma_id, aluno_cpf):
    """Cancela a matrícula de um aluno em uma turma."""
    Turma = get_turma_model()
    Aluno = get_aluno_model()
    turma = get_object_or_404(Turma, id=turma_id)
    aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
    # Verificar se o aluno está matriculado na turma
    try:
        # Importar o modelo Matricula dinamicamente
        from importlib import import_module

        matriculas_module = import_module("matriculas.models")
        Matricula = getattr(matriculas_module, "Matricula")
        matricula = Matricula.objects.get(aluno=aluno, turma=turma)
        if request.method == "POST":
            # Cancelar a matrícula
            matricula.status = "C"  # Cancelada
            matricula.save()
            messages.success(
                request,
                f"Matrícula do aluno {aluno.nome} na turma {turma.nome} cancelada com sucesso.",
            )
            return redirect("turmas:detalhar_turma", id=turma.id)
        # Se for GET, mostrar página de confirmação
        return render(
            request,
            "turmas/cancelar_matricula.html",
            {"turma": turma, "aluno": aluno},
        )
    except (ImportError, AttributeError) as e:
        messages.error(
            request, f"Erro ao acessar o modelo de matrículas: {str(e)}"
        )
        return redirect("turmas:detalhar_turma", id=turma.id)
    except Matricula.DoesNotExist:
        messages.error(
            request,
            f"O aluno {aluno.nome} não está matriculado na turma {turma.nome}.",
        )
        return redirect("turmas:detalhar_turma", id=turma.id)

@login_required
def exportar_turmas(request):
    """Exporta os dados das turmas para um arquivo CSV ou Excel."""
    formato = request.GET.get('formato', 'csv')
    
    # Filtros
    query = request.GET.get('q', '')
    curso_id = request.GET.get('curso', '')
    status = request.GET.get('status', '')
    
    # Consulta base
    turmas = Turma.objects.all()
    
    # Aplicar filtros
    if query:
        turmas = turmas.filter(
            Q(nome__icontains=query) | 
            Q(instrutor__nome__icontains=query) |
            Q(curso__nome__icontains=query)
        )
    
    if curso_id:
        turmas = turmas.filter(curso__codigo_curso=curso_id)
    
    if status:
        turmas = turmas.filter(status=status)
    
    # Ordenar
    turmas = turmas.order_by('nome')
    
    # Definir nome do arquivo
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    filename = f"turmas_export_{timestamp}"
    
    if formato == 'excel':
        # Exportar para Excel
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        
        # Estilos
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#F0F0F0',
            'border': 1
        })
        
        # Cabeçalhos
        headers = [
            'ID', 'Nome', 'Curso', 'Vagas', 'Status', 'Data Início', 
            'Data Fim', 'Instrutor', 'Instrutor Auxiliar', 'Local', 'Horário'
        ]
        
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)
        
        # Dados
        for row_num, turma in enumerate(turmas, 1):
            worksheet.write(row_num, 0, turma.id)
            worksheet.write(row_num, 1, turma.nome)
            worksheet.write(row_num, 2, turma.curso.nome if turma.curso else '')
            worksheet.write(row_num, 3, turma.vagas)
            worksheet.write(row_num, 4, turma.get_status_display())
            worksheet.write(row_num, 5, turma.data_inicio.strftime('%d/%m/%Y') if turma.data_inicio else '')
            worksheet.write(row_num, 6, turma.data_fim.strftime('%d/%m/%Y') if turma.data_fim else '')
            worksheet.write(row_num, 7, turma.instrutor.nome if turma.instrutor else '')
            worksheet.write(row_num, 8, turma.instrutor_auxiliar.nome if turma.instrutor_auxiliar else '')
            worksheet.write(row_num, 9, turma.local or '')
            worksheet.write(row_num, 10, turma.horario or '')
        
        # Ajustar largura das colunas
        for i, header in enumerate(headers):
            worksheet.set_column(i, i, len(header) + 5)
        
        workbook.close()
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
        return response
    else:
        # Exportar para CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Nome', 'Curso', 'Vagas', 'Status', 'Data Início', 
            'Data Fim', 'Instrutor', 'Instrutor Auxiliar', 'Local', 'Horário'
        ])
        
        for turma in turmas:
            writer.writerow([
                turma.id,
                turma.nome,
                turma.curso.nome if turma.curso else '',
                turma.vagas,
                turma.get_status_display(),
                turma.data_inicio.strftime('%d/%m/%Y') if turma.data_inicio else '',
                turma.data_fim.strftime('%d/%m/%Y') if turma.data_fim else '',
                turma.instrutor.nome if turma.instrutor else '',
                turma.instrutor_auxiliar.nome if turma.instrutor_auxiliar else '',
                turma.local or '',
                turma.horario or ''
            ])
        
        return response

@login_required
def relatorio_turmas(request):
    """Gera relatórios sobre as turmas."""
    # Estatísticas gerais
    total_turmas = Turma.objects.count()
    turmas_ativas = Turma.objects.filter(status='ATIVA').count()
    turmas_planejadas = Turma.objects.filter(status='PLANEJADA').count()
    turmas_concluidas = Turma.objects.filter(status='CONCLUIDA').count()
    turmas_canceladas = Turma.objects.filter(status='CANCELADA').count()
    
    # Estatísticas por curso
    cursos = Curso.objects.all()
    estatisticas_cursos = []
    
    for curso in cursos:
        turmas_curso = Turma.objects.filter(curso=curso)
        total_turmas_curso = turmas_curso.count()
        
        if total_turmas_curso > 0:
            turmas_ativas_curso = turmas_curso.filter(status='ATIVA').count()
            turmas_planejadas_curso = turmas_curso.filter(status='PLANEJADA').count()
            turmas_concluidas_curso = turmas_curso.filter(status='CONCLUIDA').count()
            
            # Calcular média de alunos por turma
            total_alunos = 0
            for turma in turmas_curso:
                total_alunos += Matricula.objects.filter(turma=turma, ativa=True).count()
            
            media_alunos = total_alunos / total_turmas_curso if total_turmas_curso > 0 else 0
            
            estatisticas_cursos.append({
                'curso': curso,
                'total_turmas': total_turmas_curso,
                'turmas_ativas': turmas_ativas_curso,
                'turmas_planejadas': turmas_planejadas_curso,
                'turmas_concluidas': turmas_concluidas_curso,
                'media_alunos': round(media_alunos, 1)
            })
    
    # Turmas com mais alunos
    turmas_populares = Turma.objects.annotate(
        total_alunos=Count('matricula', filter=Q(matricula__ativa=True))
    ).order_by('-total_alunos')[:5]
    
    # Instrutores com mais turmas
    instrutores_ativos = Aluno.objects.filter(
        Q(turma_instrutor__isnull=False) | 
        Q(turma_instrutor_auxiliar__isnull=False)
    ).distinct()
    
    estatisticas_instrutores = []
    for instrutor in instrutores_ativos:
        turmas_como_instrutor = Turma.objects.filter(instrutor=instrutor).count()
        turmas_como_auxiliar = Turma.objects.filter(instrutor_auxiliar=instrutor).count()
        total_turmas_instrutor = turmas_como_instrutor + turmas_como_auxiliar
        
        if total_turmas_instrutor > 0:
            estatisticas_instrutores.append({
                'instrutor': instrutor,
                'turmas_como_instrutor': turmas_como_instrutor,
                'turmas_como_auxiliar': turmas_como_auxiliar,
                'total_turmas': total_turmas_instrutor
            })
    
    estatisticas_instrutores.sort(key=lambda x: x['total_turmas'], reverse=True)
    estatisticas_instrutores = estatisticas_instrutores[:5]
    
    context = {
        'total_turmas': total_turmas,
        'turmas_ativas': turmas_ativas,
        'turmas_planejadas': turmas_planejadas,
        'turmas_concluidas': turmas_concluidas,
        'turmas_canceladas': turmas_canceladas,
        'estatisticas_cursos': estatisticas_cursos,
        'turmas_populares': turmas_populares,
        'estatisticas_instrutores': estatisticas_instrutores
    }
    
    return render(request, 'turmas/relatorio_turmas.html', context)

@login_required
def dashboard_turmas(request):
    """Exibe um dashboard com informações sobre as turmas."""
    # Estatísticas gerais
    total_turmas = Turma.objects.count()
    turmas_ativas = Turma.objects.filter(status='ATIVA').count()
    turmas_planejadas = Turma.objects.filter(status='PLANEJADA').count()
    turmas_concluidas = Turma.objects.filter(status='CONCLUIDA').count()
    turmas_canceladas = Turma.objects.filter(status='CANCELADA').count()
    
    # Dados para gráfico de status
    dados_status = [
        {'status': 'Ativas', 'quantidade': turmas_ativas, 'cor': '#28a745'},
        {'status': 'Planejadas', 'quantidade': turmas_planejadas, 'cor': '#17a2b8'},
        {'status': 'Concluídas', 'quantidade': turmas_concluidas, 'cor': '#6c757d'},
        {'status': 'Canceladas', 'quantidade': turmas_canceladas, 'cor': '#dc3545'}
    ]
    
    # Turmas por curso
    cursos = Curso.objects.all()
    dados_cursos = []
    
    cores_cursos = [
        '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b',
        '#5a5c69', '#858796', '#f8f9fc', '#d1d3e2', '#b7b9cc'
    ]
    
    for i, curso in enumerate(cursos):
        total_turmas_curso = Turma.objects.filter(curso=curso).count()
        if total_turmas_curso > 0:
            dados_cursos.append({
                'curso': curso.nome,
                'quantidade': total_turmas_curso,
                'cor': cores_cursos[i % len(cores_cursos)]
            })
    
    # Turmas recentes
    turmas_recentes = Turma.objects.order_by('-id')[:5]
    
    # Turmas com vagas disponíveis
    turmas_com_vagas = []
    for turma in Turma.objects.filter(status='ATIVA'):
        total_matriculados = Matricula.objects.filter(turma=turma, ativa=True).count()
        vagas_disponiveis = turma.vagas - total_matriculados
        
        if vagas_disponiveis > 0:
            turmas_com_vagas.append({
                'turma': turma,
                'vagas_disponiveis': vagas_disponiveis,
                'percentual_ocupacao': (total_matriculados / turma.vagas) * 100
            })
    
    turmas_com_vagas.sort(key=lambda x: x['vagas_disponiveis'], reverse=True)
    turmas_com_vagas = turmas_com_vagas[:5]
    
    context = {
        'total_turmas': total_turmas,
        'turmas_ativas': turmas_ativas,
        'turmas_planejadas': turmas_planejadas,
        'turmas_concluidas': turmas_concluidas,
        'turmas_canceladas': turmas_canceladas,
        'dados_status': dados_status,
        'dados_cursos': dados_cursos,
        'turmas_recentes': turmas_recentes,
        'turmas_com_vagas': turmas_com_vagas
    }
    
    return render(request, 'turmas/dashboard.html', context)



## Arquivos urls.py:


### Arquivo: turmas\urls.py

python
from django.urls import path
from . import views

app_name = "turmas"

urlpatterns = [
    path("", views.listar_turmas, name="listar_turmas"),
    path("criar/", views.criar_turma, name="criar_turma"),
    path("<int:turma_id>/", views.detalhar_turma, name="detalhar_turma"),
    path("<int:turma_id>/editar/", views.editar_turma, name="editar_turma"),
    path("<int:turma_id>/excluir/", views.excluir_turma, name="excluir_turma"),
    path("<int:turma_id>/alunos/", views.listar_alunos_matriculados, name="listar_alunos_matriculados"),
    path("<int:turma_id>/matricular/", views.matricular_aluno, name="matricular_aluno"),
    path("<int:turma_id>/cancelar-matricula/<str:aluno_cpf>/", views.cancelar_matricula, name="cancelar_matricula"),
    path("exportar/", views.exportar_turmas, name="exportar_turmas"),
    path("relatorio/", views.relatorio_turmas, name="relatorio_turmas"),
    path("dashboard/", views.dashboard_turmas, name="dashboard"),
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
        <p>Você está prestes a cancelar a matrícula do aluno <strong>{{ aluno.nome }}</strong> na turma <strong>{{ turma.nome }}</strong>.</p>
        <p>Esta ação não pode ser desfeita. Deseja continuar?</p>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <button type="submit" class="btn btn-danger">Confirmar Cancelamento</button>
        <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Voltar</a>
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

{% block title %}Criar Nova Turma{% endblock %}

{% block extra_css %}
<style>
    /* Garantir que o dropdown do Select2 seja visível */
    .select2-container--bootstrap4 .select2-dropdown {
        z-index: 9999 !important;
    }
    
    /* Corrigir a altura do select */
    .select2-container .select2-selection--single {
        height: calc(1.5em + 0.75rem + 2px) !important;
    }
    
    /* Garantir que o dropdown apareça acima de outros elementos */
    .select2-container--open {
        z-index: 9999 !important;
    }
    
    /* Remover o tracinho do select e manter só a setinha */
    .select2-selection__placeholder {
        display: none !important;
    }
    
    /* Container de dias da semana - estilo igual ao select2 */
    .dias-semana-select {
        width: 100%;
        border: 1px solid #ced4da;
        border-radius: 0.25rem;
        min-height: 38px;
        padding: 0.375rem 0.75rem;
        background-color: #fff;
        cursor: pointer;
        transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    }
    
    .dias-semana-select:hover {
        border-color: #adb5bd;
    }
    
    .dias-semana-select.focus {
        border-color: #80bdff;
        box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
    }
    
    .dias-semana-container {
        display: none;
        position: absolute;
        width: 100%;
        border: 1px solid #ced4da;
        border-radius: 0.25rem;
        max-height: 200px;
        overflow-y: auto;
        z-index: 9999;
        background-color: #fff;
        box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
    }
    
    .dias-semana-item {
        display: block;
        padding: 0.5rem 1rem;
        width: 100%;
        text-align: left;
        border: none;
        background: none;
        cursor: pointer;
    }
    
    .dias-semana-item:hover {
        background-color: #f8f9fa;
    }
    
    .dias-semana-item.selected {
        background-color: #e9ecef;
        font-weight: bold;
        color: #495057;
    }
    
    .dias-semana-item input {
        margin-right: 8px;
    }
    
    /* Corrigir setas nos containers de escolha */
    .select2-selection__arrow {
        height: 100% !important;
        position: absolute !important;
        right: 1px !important;
        top: 0 !important;
    }
    
    /* Estilo para o dropdown arrow customizado */
    .dropdown-arrow {
        position: absolute;
        right: 8px;
        top: 50%;
        transform: translateY(-50%);
        border-style: solid;
        border-width: 5px 5px 0 5px;
        border-color: #888 transparent transparent transparent;
        pointer-events: none;
    }
    
    /* Estilos para a lista de resultados de busca */
    .list-group-item-action {
        transition: background-color 0.15s ease-in-out;
    }
    
    .list-group-item-action:hover {
        background-color: #f8f9fa;
    }
    
    /* Estilo para container de aluno selecionado */
    #selected-instrutor-container,
    #selected-instrutor-auxiliar-container,
    #selected-auxiliar-instrucao-container {
        background-color: #f8f9fa;
    }
    
    /* IMPORTANTE: Esconder completamente os selects originais */
    #id_instrutor,
    #id_instrutor_auxiliar,
    #id_auxiliar_instrucao {
        display: none !important;
    }
    
    /* Esconder os botões duplicados de limpar seleção */
    #id_instrutor + button,
    #id_instrutor_auxiliar + button,
    #id_auxiliar_instrucao + button,
    #selected-instrutor-container + button,
    #selected-instrutor-auxiliar-container + button,
    #selected-auxiliar-instrucao-container + button {
        display: none !important;
    }
</style>
{% endblock %}

{% block content %}
<div class="container">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Criar Nova Turma</h1>
        <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Voltar</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    {% if form.errors %}
        {% if form.non_field_errors %}
            <div class="alert alert-danger">
                <strong>Erro:</strong>
                <ul>
                    {% for error in form.non_field_errors %}
                        <li>{{ error }}</li>
                    {% endfor %}
                </ul>
            </div>
        {% endif %}
    {% endif %}
    
    <form method="post" id="turma-form">
        {% csrf_token %}
        
        <!-- Informações Básicas - Com fundo primary -->
        <div class="card mb-4 border-primary">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0">Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="id_nome" class="form-label">Nome da Turma</label>
                            <input type="text" name="nome" value="{{ form.nome.value|default:'' }}" class="form-control {% if form.nome.errors %}is-invalid{% endif %}" maxlength="100" required id="id_nome">
                            {% if form.nome.errors %}
                                <div class="invalid-feedback">
                                    {% for error in form.nome.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                            {% if form.nome.help_text %}
                                <small class="form-text text-muted">{{ form.nome.help_text }}</small>
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-md-6">
                        <!-- Campo curso personalizado sem tracinhos -->
                        <div class="mb-3">
                            <label for="id_curso" class="form-label">Curso</label>
                            <select name="curso" id="id_curso" class="form-select curso-select" required>
                                {% for curso in cursos %}
                                    <option value="{{ curso.codigo_curso }}">
                                        {{ curso.codigo_curso }} - {{ curso.nome }}
                                    </option>
                                {% empty %}
                                    <option value="">Nenhum curso disponível</option>
                                {% endfor %}
                            </select>
                            {% if form.curso.help_text %}
                                <small class="form-text text-muted">{{ form.curso.help_text }}</small>
                            {% endif %}
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="{{ form.data_inicio.id_for_label }}" class="form-label">Data de Início</label>
                            <input type="date" name="data_inicio" id="id_data_inicio" class="form-control">
                            {% if form.data_inicio.errors %}
                            <div class="invalid-feedback">
                                {% for error in form.data_inicio.errors %}{{ error }}{% endfor %}
                            </div>
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="{{ form.data_fim.id_for_label }}" class="form-label">Data de Término</label>
                            <input type="date" name="data_fim" id="id_data_fim" class="form-control">
                            {% if form.data_fim.errors %}
                            <div class="invalid-feedback">
                                {% for error in form.data_fim.errors %}{{ error }}{% endfor %}
                            </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-4">
                        <div class="mb-3">
                            <label for="id_vagas" class="form-label">Número de Vagas</label>
                            <input type="number" name="vagas" value="{{ form.vagas.value|default:'30' }}" class="form-control{% if form.vagas.errors %} is-invalid{% endif %}" min="0" required id="id_vagas">
                            {% if form.vagas.errors %}
                                <div class="invalid-feedback">
                                    {% for error in form.vagas.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                            {% if form.vagas.help_text %}
                                <small class="form-text text-muted">{{ form.vagas.help_text }}</small>
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-md-4">
                        <!-- Campo status customizado com valores limitados -->
                        <div class="mb-3">
                            <label for="id_status" class="form-label">Status</label>
                            <select name="status" id="id_status" class="form-select" required>
                                <option value="A" {% if form.status.value == 'A' or not form.status.value %}selected{% endif %}>Ativa</option>
                                <option value="I" {% if form.status.value == 'I' %}selected{% endif %}>Inativa</option>
                                <option value="C" {% if form.status.value == 'C' %}selected{% endif %}>Cancelada</option>
                                <option value="F" {% if form.status.value == 'F' %}selected{% endif %}>Finalizada</option>
                            </select>
                            {% if form.status.help_text %}
                                <small class="form-text text-muted">{{ form.status.help_text }}</small>
                            {% endif %}
                            <!-- Alerta para data fim obrigatória quando Finalizada -->
                            <div id="alerta-data-fim" class="alert alert-warning mt-2" style="display:none;">
                                <i class="fas fa-exclamation-triangle"></i> Quando o status é "Finalizada", a Data de Término é obrigatória.
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
                            <label for="id_local" class="form-label">Local</label>
                            <input type="text" name="local" value="{{ form.local.value|default:'' }}" class="form-control{% if form.local.errors %} is-invalid{% endif %}" maxlength="200" id="id_local">
                            {% if form.local.errors %}
                                <div class="invalid-feedback">
                                    {% for error in form.local.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <!-- Dias da semana estilo select2 -->
                        <div class="mb-3">
                            <label class="form-label">Dias da Semana</label>
                            <input type="hidden" name="dias_semana" id="dias_semana_hidden" value="">
                            
                            <div class="position-relative">
                                <div class="dias-semana-select" id="dias-semana-display">
                                    <span id="dias-semana-texto">
                                        {% if form.dias_semana.value %}
                                            {{ form.dias_semana.value }}
                                        {% else %}
                                            Selecione os dias da semana
                                        {% endif %}
                                    </span>
                                    <span class="dropdown-arrow"></span>
                                </div>
                                
                                <div class="dias-semana-container" id="dias-semana-dropdown" style="display: none;">
                                    <div class="dia-semana-item" data-dia="Segunda">
                                        <input type="checkbox" id="dia_segunda">
                                        Segunda
                                    </div>
                                    <div class="dia-semana-item" data-dia="Terça">
                                        <input type="checkbox" id="dia_terca">
                                        Terça
                                    </div>
                                    <div class="dia-semana-item" data-dia="Quarta">
                                        <input type="checkbox" id="dia_quarta">
                                        Quarta
                                    </div>
                                    <div class="dia-semana-item" data-dia="Quinta">
                                        <input type="checkbox" id="dia_quinta">
                                        Quinta
                                    </div>
                                    <div class="dia-semana-item" data-dia="Sexta">
                                        <input type="checkbox" id="dia_sexta">
                                        Sexta
                                    </div>
                                    <div class="dia-semana-item" data-dia="Sábado">
                                        <input type="checkbox" id="dia_sabado">
                                        Sábado
                                    </div>
                                    <div class="dia-semana-item" data-dia="Domingo">
                                        <input type="checkbox" id="dia_domingo">
                                        Domingo
                                    </div>
                                </div>
                            </div>
                            <small class="form-text text-muted">Selecione os dias da semana em que ocorrerão as aulas</small>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="id_horario" class="form-label">Horário</label>
                            <input type="text" name="horario" value="{{ form.horario.value|default:'' }}" class="form-control{% if form.horario.errors %} is-invalid{% endif %}" maxlength="100" id="id_horario">
                            {% if form.horario.errors %}
                                <div class="invalid-feedback">
                                    {% for error in form.horario.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                            {% if form.horario.help_text %}
                                <small class="form-text text-muted">{{ form.horario.help_text }}</small>
                            {% endif %}
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <div class="mb-3">
                            <label for="id_descricao" class="form-label">Descrição</label>
                            <textarea name="descricao" cols="40" rows="3" class="form-control{% if form.descricao.errors %} is-invalid{% endif %}" id="id_descricao">{{ form.descricao.value|default:'' }}</textarea>
                            {% if form.descricao.errors %}
                                <div class="invalid-feedback">
                                    {% for error in form.descricao.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Seção de Instrutoria -->
        <div class="card mb-4 border-success">
            <div class="card-header bg-success text-white">
                <h5 class="mb-0">Instrutoria</h5>
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
                    O sistema verificará a elegibil
                    <i class="fas fa-info-circle"></i> Você pode selecionar qualquer aluno como instrutor.
                    O sistema verificará a elegibilidade do aluno para a função de instrutor.
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between">
            <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Salvar Turma</button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/modules/instrutor-search.js' %}"></script>
<script src="{% static 'js/turmas/form_fix.js' %}"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Inicializar Select2 para o campo de curso
        $('.curso-select').select2({
            theme: 'bootstrap4',
            placeholder: 'Selecione um curso',
            width: '100%'
        });
        
        // Inicializar componente de dias da semana
        if (typeof DiasSemana !== 'undefined') {
            DiasSemana.init();
            
            // Definir os dias da semana selecionados
            var diasSelecionados = '{{ form.dias_semana.value|default:"" }}';
            if (diasSelecionados) {
                console.log('Definindo dias selecionados: ', diasSelecionados);
                var diasArray = diasSelecionados.split(',').map(function(dia) {
                    return dia.trim();
                });
                
                // Marcar os checkboxes correspondentes
                diasArray.forEach(function(dia) {
                    dia = dia.charAt(0).toUpperCase() + dia.slice(1).toLowerCase();
                    var checkbox = document.getElementById('dia_' + dia.toLowerCase());
                    if (checkbox) {
                        checkbox.checked = true;
                    }
                });
                
                // Atualizar texto visível
                document.getElementById('dias-semana-texto').textContent = diasSelecionados;
            }
        } else {
            console.error('Módulo DiasSemana não encontrado!');
        }
        
        // Inicializar busca de instrutores
        if (typeof InstrutorSearch !== 'undefined') {
            var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            InstrutorSearch.init(csrftoken, false);
        } else {
            console.error('Módulo InstrutorSearch não encontrado!');
        }
        
        // Ocultar botões "Limpar seleção" duplicados gerados pelo JS
        document.querySelectorAll('.btn-limpar-duplicada').forEach(function(btn) {
            btn.style.display = 'none';
        });
        
        // Verificar status e mostrar alerta para data fim obrigatória
        var statusField = document.getElementById('id_status');
        var alertaDataFim = document.getElementById('alerta-data-fim');
        
        if (statusField && alertaDataFim) {
            statusField.addEventListener('change', function() {
                if (this.value === 'F') {
                    alertaDataFim.style.display = 'block';
                } else {
                    alertaDataFim.style.display = 'none';
                }
            });
            
            // Verificar status inicial
            if (statusField.value === 'F') {
                alertaDataFim.style.display = 'block';
            }
        }
    });
</script>
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
                                    <a href="{% url 'turmas:cancelar_matricula' turma.id matricula.aluno.cpf %}"
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

{% block title %}Editar Turma: {{ turma.nome }}{% endblock %}

{% block extra_css %}
<style>
    /* Garantir que o dropdown do Select2 seja visível */
    .select2-container--bootstrap4 .select2-dropdown {
        z-index: 9999 !important;
    }
    
    /* Corrigir a altura do select */
    .select2-container .select2-selection--single {
        height: calc(1.5em + 0.75rem + 2px) !important;
    }
    
    /* Garantir que o dropdown apareça acima de outros elementos */
    .select2-container--open {
        z-index: 9999 !important;
    }
    
    /* Remover o tracinho do select e manter só a setinha */
    .select2-selection__placeholder {
        display: none !important;
    }
    
    /* Container de dias da semana - estilo igual ao select2 */
    .dias-semana-select {
        width: 100%;
        border: 1px solid #ced4da;
        border-radius: 0.25rem;
        min-height: 38px;
        padding: 0.375rem 0.75rem;
        background-color: #fff;
        cursor: pointer;
        transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    }
    
    .dias-semana-select:hover {
        border-color: #adb5bd;
    }
    
    .dias-semana-select.focus {
        border-color: #80bdff;
        box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
    }
    
    .dias-semana-container {
        display: none;
        position: absolute;
        width: 100%;
        border: 1px solid #ced4da;
        border-radius: 0.25rem;
        max-height: 200px;
        overflow-y: auto;
        z-index: 9999;
        background-color: #fff;
        box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
    }
    
    .dias-semana-item {
        display: block;
        padding: 0.5rem 1rem;
        width: 100%;
        text-align: left;
        border: none;
        background: none;
        cursor: pointer;
    }
    
    .dias-semana-item:hover {
        background-color: #f8f9fa;
    }
    
    .dias-semana-item.selected {
        background-color: #e9ecef;
        font-weight: bold;
        color: #495057;
    }
    
    .dias-semana-item input {
        margin-right: 8px;
    }
    
    /* Corrigir setas nos containers de escolha */
    .select2-selection__arrow {
        height: 100% !important;
        position: absolute !important;
        right: 1px !important;
        top: 0 !important;
    }
    
    /* Estilo para o dropdown arrow customizado */
    .dropdown-arrow {
        position: absolute;
        right: 8px;
        top: 50%;
        transform: translateY(-50%);
        border-style: solid;
        border-width: 5px 5px 0 5px;
        border-color: #888 transparent transparent transparent;
        pointer-events: none;
    }
    
    /* Estilos para a lista de resultados de busca */
    .list-group-item-action {
        transition: background-color 0.15s ease-in-out;
    }
    
    .list-group-item-action:hover {
        background-color: #f8f9fa;
    }
    
    /* Estilo para container de aluno selecionado */
    #selected-instrutor-container,
    #selected-instrutor-auxiliar-container,
    #selected-auxiliar-instrucao-container {
        background-color: #f8f9fa;
    }
    
    /* IMPORTANTE: Esconder completamente os selects originais */
    #id_instrutor, 
    #id_instrutor_auxiliar, 
    #id_auxiliar_instrucao {
        display: none !important;
    }
    
    /* Esconder os botões duplicados de limpar seleção */
    #id_instrutor + button, 
    #id_instrutor_auxiliar + button, 
    #id_auxiliar_instrucao + button,
    #selected-instrutor-container + button,
    #selected-instrutor-auxiliar-container + button,
    #selected-auxiliar-instrucao-container + button {
        display: none !important;
    }
</style>
{% endblock %}

{% block content %}
<div class="container">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Editar Turma: {{ turma.nome }}</h1>
        <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Voltar para Detalhes</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    {% if form.errors %}
        {% if form.non_field_errors %}
            <div class="alert alert-danger">
                <strong>Erro:</strong>
                <ul>
                    {% for error in form.non_field_errors %}
                        <li>{{ error }}</li>
                    {% endfor %}
                </ul>
            </div>
        {% endif %}
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        
        <!-- Informações Básicas - Com fundo primary -->
        <div class="card mb-4 border-primary">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0">Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="id_nome" class="form-label">Nome da Turma</label>
                            <input type="text" name="nome" value="{{ form.nome.value|default:'' }}" class="form-control {% if form.nome.errors %}is-invalid{% endif %}" maxlength="100" required id="id_nome">
                            {% if form.nome.errors %}
                                <div class="invalid-feedback">
                                    {% for error in form.nome.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                            {% if form.nome.help_text %}
                                <small class="form-text text-muted">{{ form.nome.help_text }}</small>
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-md-6">
                        <!-- Campo curso personalizado sem tracinhos -->
                        <div class="mb-3">
                            <label for="id_curso" class="form-label">Curso</label>
                            <select name="curso" id="id_curso" class="form-select curso-select" required>
                                {% for choice in form.curso.field.choices %}
                                    {% if choice.0 %}
                                        <option value="{{ choice.0 }}" {% if form.curso.value|stringformat:"s" == choice.0|stringformat:"s" %}selected{% endif %}>
                                            {{ choice.1 }}
                                        </option>
                                    {% endif %}
                                {% endfor %}
                            </select>
                            {% if form.curso.help_text %}
                                <small class="form-text text-muted">{{ form.curso.help_text }}</small>
                            {% endif %}
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="{{ form.data_inicio.id_for_label }}" class="form-label">Data de Início</label>
                            {% if turma.data_inicio %}
                            <input type="date" name="data_inicio" id="id_data_inicio" class="form-control" 
                                   value="{{ turma.data_inicio|date:'Y-m-d' }}">
                            {% else %}
                            <input type="date" name="data_inicio" id="id_data_inicio" class="form-control">
                            {% endif %}
                            {% if form.data_inicio.errors %}
                            <div class="invalid-feedback">
                                {% for error in form.data_inicio.errors %}{{ error }}{% endfor %}
                            </div>
                            {% endif %}
                            <small class="form-text text-muted">Data atual: {{ turma.data_inicio|date:"d/m/Y" }}</small>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="{{ form.data_fim.id_for_label }}" class="form-label">Data de Término</label>
                            {% if turma.data_fim %}
                            <input type="date" name="data_fim" id="id_data_fim" class="form-control" 
                                   value="{{ turma.data_fim|date:'Y-m-d' }}">
                            {% else %}
                            <input type="date" name="data_fim" id="id_data_fim" class="form-control">
                            {% endif %}
                            {% if form.data_fim.errors %}
                            <div class="invalid-feedback">
                                {% for error in form.data_fim.errors %}{{ error }}{% endfor %}
                            </div>
                            {% endif %}
                            <small class="form-text text-muted">Data atual: {% if turma.data_fim %}{{ turma.data_fim|date:"d/m/Y" }}{% else %}Não definida{% endif %}</small>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-4">
                        <div class="mb-3">
                            <label for="id_vagas" class="form-label">Número de Vagas</label>
                            <input type="number" name="vagas" value="{{ form.vagas.value }}" class="form-control{% if form.vagas.errors %} is-invalid{% endif %}" min="0" required id="id_vagas">
                            {% if form.vagas.errors %}
                                <div class="invalid-feedback">
                                    {% for error in form.vagas.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                            {% if form.vagas.help_text %}
                                <small class="form-text text-muted">{{ form.vagas.help_text }}</small>
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-md-4">
                        <!-- Campo status customizado com valores limitados -->
                        <div class="mb-3">
                            <label for="id_status" class="form-label">Status</label>
                            <select name="status" id="id_status" class="form-select" required>
                                <option value="A" {% if form.status.value == 'A' %}selected{% endif %}>Ativa</option>
                                <option value="I" {% if form.status.value == 'I' %}selected{% endif %}>Inativa</option>
                                <option value="C" {% if form.status.value == 'C' %}selected{% endif %}>Cancelada</option>
                                <option value="F" {% if form.status.value == 'F' %}selected{% endif %}>Finalizada</option>
                            </select>
                            {% if form.status.help_text %}
                                <small class="form-text text-muted">{{ form.status.help_text }}</small>
                            {% endif %}
                            <!-- Alerta para data fim obrigatória quando Finalizada -->
                            <div id="alerta-data-fim" class="alert alert-warning mt-2" style="display:none;">
                                <i class="fas fa-exclamation-triangle"></i> Quando o status é "Finalizada", a Data de Término é obrigatória.
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
                            <label for="id_local" class="form-label">Local</label>
                            <input type="text" name="local" value="{{ form.local.value }}" class="form-control{% if form.local.errors %} is-invalid{% endif %}" maxlength="200" id="id_local">
                            {% if form.local.errors %}
                                <div class="invalid-feedback">
                                    {% for error in form.local.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <!-- Dias da semana estilo select2 -->
                        <div class="mb-3">
                            <label class="form-label">Dias da Semana</label>
                            <input type="hidden" name="dias_semana" id="dias_semana_hidden" value="sábado">
                            
                            <div class="position-relative">
                                <div class="dias-semana-select" id="dias-semana-display">
                                    <span id="dias-semana-texto">
                                        {% if form.dias_semana.value %}
                                            {{ form.dias_semana.value }}
                                        {% else %}
                                            Selecione os dias da semana
                                        {% endif %}
                                    </span>
                                    <span class="dropdown-arrow"></span>
                                </div>
                                
                                <div class="dias-semana-container" id="dias-semana-dropdown" style="display: none;">
                                    <div class="dia-semana-item" data-dia="Segunda">
                                        <input type="checkbox" id="dia_segunda">
                                        Segunda
                                    </div>
                                    <div class="dia-semana-item" data-dia="Terça">
                                        <input type="checkbox" id="dia_terca">
                                        Terça
                                    </div>
                                    <div class="dia-semana-item" data-dia="Quarta">
                                        <input type="checkbox" id="dia_quarta">
                                        Quarta
                                    </div>
                                    <div class="dia-semana-item" data-dia="Quinta">
                                        <input type="checkbox" id="dia_quinta">
                                        Quinta
                                    </div>
                                    <div class="dia-semana-item" data-dia="Sexta">
                                        <input type="checkbox" id="dia_sexta">
                                        Sexta
                                    </div>
                                    <div class="dia-semana-item" data-dia="Sábado">
                                        <input type="checkbox" id="dia_sabado">
                                        Sábado
                                    </div>
                                    <div class="dia-semana-item" data-dia="Domingo">
                                        <input type="checkbox" id="dia_domingo">
                                        Domingo
                                    </div>
                                </div>
                            </div>
                            <small class="form-text text-muted">Selecione os dias da semana em que ocorrerão as aulas</small>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="id_horario" class="form-label">Horário</label>
                            <input type="text" name="horario" value="{{ form.horario.value }}" class="form-control{% if form.horario.errors %} is-invalid{% endif %}" maxlength="100" id="id_horario">
                            {% if form.horario.errors %}
                                <div class="invalid-feedback">
                                    {% for error in form.horario.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                            {% if form.horario.help_text %}
                                <small class="form-text text-muted">{{ form.horario.help_text }}</small>
                            {% endif %}
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <div class="mb-3">
                            <label for="id_descricao" class="form-label">Descrição</label>
                            <textarea name="descricao" cols="40" rows="3" class="form-control{% if form.descricao.errors %} is-invalid{% endif %}" id="id_descricao">{{ form.descricao.value }}</textarea>
                            {% if form.descricao.errors %}
                                <div class="invalid-feedback">
                                    {% for error in form.descricao.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Seção de Instrutoria - Agora com a resolução dos problemas de exibição -->
        <div class="card mb-4 border-success">
            <div class="card-header bg-success text-white">
                <h5 class="mb-0">Instrutoria</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <!-- Instrutor Principal -->
                    <div class="col-md-4 mb-3">
                        <label for="search-instrutor" class="form-label">Instrutor Principal</label>
                        <input type="text" id="search-instrutor" class="form-control" placeholder="Digite parte do CPF, nome ou número iniciático..." autocomplete="off"
                               value="{% if turma.instrutor %}{{ turma.instrutor.nome }}{% endif %}">
                        <div id="search-results-instrutor" class="list-group mt-2" style="display: none"></div>
                        <div id="selected-instrutor-container" class="p-3 border rounded mt-2">
                            <div id="selected-instrutor-info">
                                <strong>{{ aluno.nome }}</strong><br>
                                CPF: {{ aluno.cpf }}<br>
                                Número Iniciático: {{ aluno.numero_iniciatico|default:"N/A" }}<br>
                                <span class="badge bg-{{ aluno.situacao_class }}">{{ aluno.get_situacao_display }}</span>
                                <div class="mt-2 small">
                                    <div><strong>Status como instrutor:</strong> <span id="instrutor-status"></span></div>
                                    <div class="mt-1"><strong>Turmas:</strong> <span id="instrutor-turmas"></span></div>
                                </div>
                            </div>
                        </div>
                        <div id="instrutor-error" class="alert alert-warning mt-2 d-none"></div>
                        <!-- Campo original oculto via CSS -->
                        {{ form.instrutor }}
                    </div>
                    
                    <!-- Instrutor Auxiliar -->
                    <div class="col-md-4 mb-3">
                        <label for="search-instrutor-auxiliar" class="form-label">Instrutor Auxiliar</label>
                        <input type="text" id="search-instrutor-auxiliar" class="form-control" placeholder="Digite parte do CPF, nome ou número iniciático..." autocomplete="off"
                               value="{% if turma.instrutor_auxiliar %}{{ turma.instrutor_auxiliar.nome }}{% endif %}">
                        <div id="search-results-instrutor-auxiliar" class="list-group mt-2" style="display: none;"></div>
                        <div id="selected-instrutor-auxiliar-container" class="p-3 border rounded mt-2 {% if not turma.instrutor_auxiliar %}d-none{% endif %}">
                            <div id="selected-instrutor-auxiliar-info">
                                {% if turma.instrutor_auxiliar %}
                                    <strong>{{ turma.instrutor_auxiliar.nome }}</strong><br>
                                    CPF: {{ turma.instrutor_auxiliar.cpf }}<br>
                                    Número Iniciático: {{ turma.instrutor_auxiliar.numero_iniciatico|default:"N/A" }}<br>
                                    <span class="badge bg-{{ turma.instrutor_auxiliar.situacao_class }}">{{ turma.instrutor_auxiliar.get_situacao_display }}</span>
                                    <div class="mt-2 small">
                                        <div><strong>Status como instrutor:</strong> <span id="instrutor-auxiliar-status"></span></div>
                                        <div class="mt-1"><strong>Turmas:</strong> <span id="instrutor-auxiliar-turmas"></span></div>
                                    </div>
                                {% else %}
                                    Nenhum instrutor auxiliar selecionado
                                {% endif %}
                            </div>
                        </div>
                        <div id="instrutor-auxiliar-error" class="alert alert-warning mt-2 d-none"></div>
                        <!-- Campo original oculto via CSS -->
                        {{ form.instrutor_auxiliar }}
                    </div>
                    
                    <!-- Auxiliar de Instrução -->
                    <div class="col-md-4 mb-3">
                        <label for="search-auxiliar-instrucao" class="form-label">Auxiliar de Instrução</label>
                        <input type="text" id="search-auxiliar-instrucao" class="form-control" placeholder="Digite parte do CPF, nome ou número iniciático..." autocomplete="off"
                               value="{% if turma.auxiliar_instrucao %}{{ turma.auxiliar_instrucao.nome }}{% endif %}">
                        <div id="search-results-auxiliar-instrucao" class="list-group mt-2" style="display: none;"></div>
                        <div id="selected-auxiliar-instrucao-container" class="p-3 border rounded mt-2 {% if not turma.auxiliar_instrucao %}d-none{% endif %}">
                            <div id="selected-auxiliar-instrucao-info">
                                {% if turma.auxiliar_instrucao %}
                                    <strong>{{ turma.auxiliar_instrucao.nome }}</strong><br>
                                    CPF: {{ turma.auxiliar_instrucao.cpf }}<br>
                                    Número Iniciático: {{ turma.auxiliar_instrucao.numero_iniciatico|default:"N/A" }}<br>
                                    <span class="badge bg-{{ turma.auxiliar_instrucao.situacao_class }}">{{ turma.auxiliar_instrucao.get_situacao_display }}</span>
                                    <div class="mt-2 small">
                                        <div><strong>Status como instrutor:</strong> <span id="auxiliar-instrucao-status"></span></div>
                                        <div class="mt-1"><strong>Turmas:</strong> <span id="auxiliar-instrucao-turmas"></span></div>
                                    </div>
                                {% else %}
                                    Nenhum auxiliar de instrução selecionado
                                {% endif %}
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
<!-- Adicionando jQuery apenas se não estiver disponível -->
<script>
    if (typeof jQuery === 'undefined') {
        document.write('<script src="https://code.jquery.com/jquery-3.6.0.min.js"><\/script>');
    }
</script>

<!-- Carregando os scripts necessários -->
<script src="{% static 'js/modules/instrutor-search.js' %}"></script>
<script src="{% static 'js/modules/dias-semana.js' %}"></script>
<script>
    // Script local para inicializar os componentes
    document.addEventListener('DOMContentLoaded', function() {
        // Inicializar dias da semana
        if (typeof DiasSemana !== 'undefined') {
            console.log('Inicializando DiasSemana');
            DiasSemana.init();
            
            // Definir os dias da semana selecionados
            var diasSelecionados = '{{ form.dias_semana.value|default:"" }}';
            if (diasSelecionados) {
                console.log('Definindo dias selecionados: ', diasSelecionados);
                var diasArray = diasSelecionados.split(',').map(function(dia) {
                    return dia.trim();
                });
                
                // Marcar os checkboxes correspondentes
                diasArray.forEach(function(dia) {
                    dia = dia.charAt(0).toUpperCase() + dia.slice(1).toLowerCase();
                    var checkbox = document.getElementById('dia_' + dia.toLowerCase());
                    if (checkbox) {
                        checkbox.checked = true;
                    }
                });
                
                // Atualizar texto visível
                document.getElementById('dias-semana-texto').textContent = diasSelecionados;
            }
        } else {
            console.error('Módulo DiasSemana não encontrado!');
        }
        
        // Inicializar busca de instrutores
        if (typeof InstrutorSearch !== 'undefined') {
            var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            InstrutorSearch.init(csrftoken, false);
        } else {
            console.error('Módulo InstrutorSearch não encontrado!');
        }
        
        // Ocultar botões "Limpar seleção" duplicados gerados pelo JS
        document.querySelectorAll('.btn-limpar-duplicada').forEach(function(btn) {
            btn.style.display = 'none';
        });
        
        // Remover validação incorreta da data de início
        var dataInicioField = document.getElementById('id_data_inicio');
        if (dataInicioField) {
            dataInicioField.min = ""; // Remove restrição de data mínima
        }
    });
</script>
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
    <h1>Lista de Turmas</h1>

    <form method="get" class="mb-3">
        <div class="row">
            <div class="col-md-4">
                <input type="text" name="q" class="form-control" placeholder="Buscar turmas..." value="{{ query }}">
            </div>
            <div class="col-md-3">
                <select name="curso" class="form-control">
                    <option value="">Todos os cursos</option>
                    {% for curso in cursos %}
                        <option value="{{ curso.codigo_curso }}" {% if curso.codigo_curso|stringformat:"s" == curso_selecionado %}selected{% endif %}>
                            {{ curso.nome }}
                        </option>
                    {% endfor %}
                </select>
            </div>
            <div class="col-md-3">
                <select name="status" class="form-control">
                    <option value="">Todos os status</option>
                    {% for status_value, status_label in opcoes_status %}
                        <option value="{{ status_value }}" {% if status_value == status_selecionado %}selected{% endif %}>
                            {{ status_label }}
                        </option>
                    {% endfor %}
                </select>
            </div>
            <div class="col-md-2">
                <button type="submit" class="btn btn-primary">Filtrar</button>
            </div>
        </div>
    </form>

    <table class="table table-striped">
        <thead>
            <tr>
                <th>Nome</th>
                <th>Curso</th>
                <th>Data de Início</th>
                <th>Data de Fim</th>
                <th>Status</th>
                <th>Vagas</th>
                <th>Matrículas</th>
                <th>Disponíveis</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody>
            {% for turma_info in turmas_com_info %}
            {% with turma=turma_info.turma %}
            <tr {% if turma.alerta_instrutor %}class="table-warning"{% endif %}>
                <td>
                    {{ turma.nome }}
                    {% if turma_info.tem_pendencia_instrutoria %}
                    <div class="alert alert-danger mt-1 mb-0 p-1 text-center blink">
                        <small><strong>Pendência na Instrutoria</strong></small>
                    </div>
                    {% endif %}
                </td>
                <td>{{ turma.curso }}</td>
                <td>{{ turma.data_inicio|date:"d/m/Y" }}</td>
                <td>{{ turma.data_fim|date:"d/m/Y" }}</td>
                <td>
                    {% if turma.status == 'A' %}
                        <span class="badge bg-success">{{ turma.get_status_display }}</span>
                    {% elif turma.status == 'I' %}
                        <span class="badge bg-warning">{{ turma.get_status_display }}</span>
                    {% else %}
                        <span class="badge bg-secondary">{{ turma.get_status_display }}</span>
                    {% endif %}
                    
                    {% if turma.alerta_instrutor %}
                        <span class="badge bg-danger ms-1" data-bs-toggle="tooltip" title="{{ turma.alerta_mensagem }}">
                            <i class="fas fa-exclamation-triangle"></i>
                        </span>
                    {% endif %}
                </td>
                <td>{{ turma.vagas }}</td>
                <td>{{ turma_info.total_alunos }}</td>
                <td>{{ turma_info.vagas_disponiveis }}</td>
                <td>
                    <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-sm btn-info">Detalhes</a>
                    <a href="{% url 'turmas:editar_turma' turma.id %}" class="btn btn-sm btn-warning">Editar</a>
                    <a href="{% url 'turmas:excluir_turma' turma.id %}" class="btn btn-sm btn-danger">Excluir</a>
                </td>
            </tr>
            {% endwith %}
            {% empty %}            <tr>
                <td colspan="9" class="text-center">Nenhuma turma encontrada.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    {% if turmas.has_other_pages %}
    <nav>
        <ul class="pagination">
            {% if turmas.has_previous %}
                <li class="page-item"><a class="page-link" href="?page={{ turmas.previous_page_number }}">Anterior</a></li>
            {% endif %}

            {% for i in turmas.paginator.page_range %}
                {% if turmas.number == i %}
                    <li class="page-item active"><span class="page-link">{{ i }}</span></li>
                {% else %}
                    <li class="page-item"><a class="page-link" href="?page={{ i }}">{{ i }}</a></li>
                {% endif %}
            {% endfor %}

            {% if turmas.has_next %}
                <li class="page-item"><a class="page-link" href="?page={{ turmas.next_page_number }}">Próxima</a></li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}

    <a href="{% url 'turmas:criar_turma' %}" class="btn btn-primary">Criar Nova Turma</a>
</div>
{% endblock %}
@login_required
def listar_turmas(request):
    Turma = get_turma_model()
    turmas = Turma.objects.all()
    
    # Preparar informações adicionais para cada turma
    turmas_com_info = []
    for turma in turmas:
        # Calcular o número de alunos matriculados
        total_alunos = turma.matriculas.count() if hasattr(turma, 'matriculas') else 0
        
        # Calcular vagas disponíveis
        vagas_disponiveis = turma.vagas - total_alunos
        
        turmas_com_info.append({
            'turma': turma,
            'total_alunos': total_alunos,
            'vagas_disponiveis': vagas_disponiveis
        })
    
    # Obter cursos para o filtro
    try:
        Curso = get_model_class("Curso", "cursos.models")
        cursos = Curso.objects.all()
    except:
        cursos = []
    
    # Opções de status para o filtro
    opcoes_status = Turma.STATUS_CHOICES
    
    context = {
        'turmas_com_info': turmas_com_info,
        'cursos': cursos,
        'opcoes_status': opcoes_status,
        'query': request.GET.get('q', ''),
        'curso_selecionado': request.GET.get('curso', ''),
        'status_selecionado': request.GET.get('status', '')
    }
    
    return render(request, "turmas/listar_turmas.html", context)
def get_model_class(model_name, module_name="turmas.models"):
    """Importa dinamicamente uma classe de modelo para evitar importações circulares."""
    models_module = importlib.import_module(module_name)
    return getattr(models_module, model_name)



### Arquivo: turmas\templates\turmas\matricular_aluno.html

html
{% extends 'base.html' %}
{% load static %}
<!-- Modificar os links para usar turma.id em vez de turma.codigo_turma -->
<a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Voltar para Turma</a>
{% block title %}Matricular Aluno na Turma: {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Matricular Aluno na Turma: {{ turma.nome }}</h1>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Informações da Turma</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome da Turma:</strong> {{ turma.nome }}</p>
            <p><strong>Curso:</strong> {{ turma.curso.nome }}</p>
            <p><strong>Período:</strong> {{ turma.data_inicio|date:"d/m/Y" }} a {{ turma.data_fim|date:"d/m/Y" }}</p>
            <p><strong>Vagas Disponíveis:</strong> {{ vagas_disponiveis }}</p>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">Selecionar Aluno para Matrícula</h5>
        </div>
        <div class="card-body">
            <!-- Search input with autocomplete -->
            <div class="mb-4">
                {% csrf_token %}  <!-- Make sure you have this for AJAX requests -->
                <label for="search-aluno" class="form-label">Buscar Aluno:</label>
                <input type="text" id="search-aluno" class="form-control"
                       placeholder="Digite parte do CPF, nome ou número iniciático..."
                       autocomplete="off">
                <div id="search-results" class="list-group mt-2">
                    <!-- Results will be populated here dynamically -->
                </div>
            </div>
            
            <form method="post" id="matricula-form">
                {% csrf_token %}
                <div class="mb-3">
                    <label for="aluno" class="form-label">Aluno Selecionado:</label>
                    <div id="selected-aluno-container" class="p-3 border rounded mb-2 d-none">
                        <div id="selected-aluno-info">Nenhum aluno selecionado</div>
                    </div>
                    <input type="hidden" name="aluno" id="aluno-id" required>
                </div>
                <button type="submit" class="btn btn-primary" id="submit-btn" disabled>Matricular</button>
                <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Cancelar</a>
            </form>
        </div>
    </div>
    
    <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary mt-3">Voltar para Detalhes da Turma</a>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const searchInput = document.getElementById('search-aluno');
        const searchResults = document.getElementById('search-results');
        const selectedAlunoContainer = document.getElementById('selected-aluno-container');
        const selectedAlunoInfo = document.getElementById('selected-aluno-info');
        const alunoIdField = document.getElementById('aluno-id');
        const submitBtn = document.getElementById('submit-btn');
        
        let searchTimeout;
        
        // Get CSRF token
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        // Add CSRF token to all fetch requests
        const originalFetch = window.fetch;
        window.fetch = function(url, options = {}) {
            if (url.startsWith('/')) {
                options.headers = options.headers || {};
                options.headers['X-CSRFToken'] = csrftoken;
            }
            return originalFetch(url, options);
        };
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            
            const query = this.value.trim();
            
            // Clear results if query is too short
            if (query.length < 2) {
                searchResults.innerHTML = '';
                searchResults.classList.add('d-none');
                return;
            }
            
            // Set a timeout to avoid making too many requests
            searchTimeout = setTimeout(function() {
                // Show loading indicator
                searchResults.innerHTML = '<div class="list-group-item text-muted">Buscando...</div>';
                searchResults.classList.remove('d-none');
                
                fetch(`/alunos/search/?q=${encodeURIComponent(query)}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Erro na requisição');
                        }
                        return response.json();
                    })
                    .then(data => {
                        searchResults.innerHTML = '';
                        
                        if (data.error) {
                            // Handle error response
                            searchResults.innerHTML = `<div class="list-group-item text-danger">${data.error}</div>`;
                            return;
                        }
                        
                        if (data.length === 0) {
                            searchResults.innerHTML = '<div class="list-group-item">Nenhum aluno encontrado</div>';
                            return;
                        }
                        
                        // Display results
                        data.forEach(aluno => {
                            const item = document.createElement('a');
                            item.href = '#';
                            item.className = 'list-group-item list-group-item-action';
                            item.innerHTML = `
                                <div class="d-flex justify-content-between">
                                    <div>${aluno.nome}</div>
                                    <div class="text-muted">
                                        <small>CPF: ${aluno.cpf}</small>
                                        ${aluno.numero_iniciatico !== "N/A" ? `<small class="ms-2">Nº: ${aluno.numero_iniciatico}</small>` : ''}
                                    </div>
                                </div>
                            `;
                            
                            // Add click event to select this aluno
                            item.addEventListener('click', function(e) {
                                e.preventDefault();
                                selectAluno(aluno);
                                searchResults.classList.add('d-none');
                            });
                            
                            searchResults.appendChild(item);
                        });
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        searchResults.innerHTML = '<div class="list-group-item text-danger">Erro ao buscar alunos</div>';
                    });
            }, 300);
        });
        
        // Hide results when clicking outside
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.classList.add('d-none');
            }
        });
        
        // Function to select an aluno
        function selectAluno(aluno) {
            // Update the hidden input with the selected aluno's CPF
            alunoIdField.value = aluno.cpf;
            
            // Update the search input with the selected aluno's name
            searchInput.value = aluno.nome;
            
            // Show the selected aluno info
            selectedAlunoInfo.innerHTML = `
                <strong>${aluno.nome}</strong><br>
                CPF: ${aluno.cpf}<br>
                ${aluno.numero_iniciatico !== "N/A" ? `Número Iniciático: ${aluno.numero_iniciatico}` : ''}
            `;
            
            // Show the container and enable the submit button
            selectedAlunoContainer.classList.remove('d-none');
            submitBtn.disabled = false;
        }
    });
</script>
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
<div class="container-fluid mt-4">
    <div class="d-flex flex-wrap justify-content-between align-items-center mb-3">
        <h1 class="mb-3 mb-md-0">Relatório de Turmas</h1>
        
        <div class="btn-group">
            <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'turmas:exportar_turmas' %}" class="btn btn-success">
                <i class="fas fa-file-export"></i> Exportar CSV
            </a>
            <a href="{% url 'turmas:exportar_turmas' %}?formato=excel" class="btn btn-success">
                <i class="fas fa-file-excel"></i> Exportar Excel
            </a>
        </div>
    </div>
    
    <!-- Resumo Geral -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Resumo Geral</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-4 mb-3">
                            <div class="card-counter primary">
                                <i class="fas fa-chalkboard-teacher"></i>
                                <span class="count-numbers">{{ total_turmas }}</span>
                                <span class="count-name">Total de Turmas</span>
                            </div>
                        </div>
                        
                        <div class="col-md-2 mb-3">
                            <div class="card-counter success">
                                <i class="fas fa-check-circle"></i>
                                <span class="count-numbers">{{ turmas_ativas }}</span>
                                <span class="count-name">Ativas</span>
                            </div>
                        </div>
                        
                        <div class="col-md-2 mb-3">
                            <div class="card-counter info">
                                <i class="fas fa-calendar-alt"></i>
                                <span class="count-numbers">{{ turmas_planejadas }}</span>
                                <span class="count-name">Planejadas</span>
                            </div>
                        </div>
                        
                        <div class="col-md-2 mb-3">
                            <div class="card-counter secondary">
                                <i class="fas fa-flag-checkered"></i>
                                <span class="count-numbers">{{ turmas_concluidas }}</span>
                                <span class="count-name">Concluídas</span>
                            </div>
                        </div>
                        
                        <div class="col-md-2 mb-3">
                            <div class="card-counter danger">
                                <i class="fas fa-ban"></i>
                                <span class="count-numbers">{{ turmas_canceladas }}</span>
                                <span class="count-name">Canceladas</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Estatísticas por Curso -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">Estatísticas por Curso</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Curso</th>
                                    <th>Total de Turmas</th>
                                    <th>Turmas Ativas</th>
                                    <th>Turmas Planejadas</th>
                                    <th>Turmas Concluídas</th>
                                    <th>Média de Alunos</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for estatistica in estatisticas_cursos %}
                                <tr>
                                    <td>{{ estatistica.curso.nome }}</td>
                                    <td>{{ estatistica.total_turmas }}</td>
                                    <td>{{ estatistica.turmas_ativas }}</td>
                                    <td>{{ estatistica.turmas_planejadas }}</td>
                                    <td>{{ estatistica.turmas_concluidas }}</td>
                                    <td>{{ estatistica.media_alunos }}</td>
                                </tr>
                                {% empty %}
                                <tr>
                                    <td colspan="6" class="text-center">Nenhum dado disponível</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Turmas Populares e Instrutores -->
    <div class="row">
        <!-- Turmas com mais alunos -->
        <div class="col-md-6 mb-4">
            <div class="card h-100">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">Turmas com Mais Alunos</h5>
                </div>
                <div class="card-body">
                    {% if turmas_populares %}
                        {% for turma in turmas_populares %}
                            <div class="mb-3">
                                <div class="progress-bar-label">
                                    <span><strong>{{ turma.nome }}</strong> ({{ turma.curso.nome }})</span>
                                    <span>{{ turma.total_alunos }} alunos</span>
                                </div>
                                <div class="progress progress-bar-container">
                                    <div class="progress-bar bg-success" role="progressbar" 
                                         style="width: {{ turma.total_alunos|div:turma.vagas|mul:100 }}%" 
                                         aria-valuenow="{{ turma.total_alunos }}" aria-valuemin="0" 
                                         aria-valuemax="{{ turma.vagas }}">
                                        {{ turma.total_alunos }}/{{ turma.vagas }}
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                    {% else %}
                        <p class="text-center">Nenhuma turma encontrada</p>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <!-- Instrutores com mais turmas -->
        <div class="col-md-6 mb-4">
            <div class="card h-100">
                <div class="card-header bg-warning text-white">
                    <h5 class="mb-0">Instrutores Mais Ativos</h5>
                </div>
                <div class="card-body">
                    {% if estatisticas_instrutores %}
                        {% for estatistica in estatisticas_instrutores %}
                            <div class="mb-3">
                                <div class="progress-bar-label">
                                    <span><strong>{{ estatistica.instrutor.nome }}</strong></span>
                                    <span>{{ estatistica.total_turmas }} turmas</span>
                                </div>
                                <div class="progress progress-bar-container">
                                    <div class="progress-bar bg-warning" role="progressbar" 
                                         style="width: {{ estatistica.turmas_como_instrutor|div:estatistica.total_turmas|mul:100 }}%" 
                                         aria-valuenow="{{ estatistica.turmas_como_instrutor }}" 
                                         aria-valuemin="0" aria-valuemax="{{ estatistica.total_turmas }}">
                                        {{ estatistica.turmas_como_instrutor }} como instrutor
                                    </div>
                                    <div class="progress-bar bg-info" role="progressbar" 
                                         style="width: {{ estatistica.turmas_como_auxiliar|div:estatistica.total_turmas|mul:100 }}%" 
                                         aria-valuenow="{{ estatistica.turmas_como_auxiliar }}" 
                                         aria-valuemin="0" aria-valuemax="{{ estatistica.total_turmas }}">
                                        {{ estatistica.turmas_como_auxiliar }} como auxiliar
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                    {% else %}
                        <p class="text-center">Nenhum instrutor encontrado</p>
                    {% endif %}
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

