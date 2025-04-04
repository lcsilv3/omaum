from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from importlib import import_module
from django.core.exceptions import ValidationError

def get_models():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module('alunos.models')
    return getattr(alunos_module, 'Aluno')

def get_forms():
    """Obtém o formulário AlunoForm dinamicamente."""
    alunos_forms = import_module('alunos.forms')
    return getattr(alunos_forms, 'AlunoForm')

@login_required
def listar_alunos(request):
    """Lista todos os alunos cadastrados."""
    try:
        Aluno = get_models()
        
        # Obter parâmetros de busca e filtro
        query = request.GET.get('q', '')
        
        # Filtrar alunos
        alunos = Aluno.objects.all()
        
        if query:
            alunos = alunos.filter(
                Q(nome__icontains=query) | 
                Q(cpf__icontains=query) | 
                Q(email__icontains=query) |
                Q(numero_iniciatico__icontains=query)
            )
        
        # Paginação
        paginator = Paginator(alunos, 10)  # 10 alunos por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Obter cursos para o filtro
        try:
            Curso = import_module('cursos.models').Curso
            cursos = Curso.objects.all()
        except:
            cursos = []
        
        context = {
            'alunos': page_obj,
            'page_obj': page_obj,
            'query': query,
            'cursos': cursos,
            'curso_selecionado': request.GET.get('curso', ''),
        }
        
        return render(request, 'alunos/listar_alunos.html', context)
    except Exception as e:
        # Em vez de mostrar a mensagem de erro, apenas retornamos uma lista vazia
        return render(request, 'alunos/listar_alunos.html', {
            'alunos': [],
            'page_obj': None,
            'query': '',
            'cursos': [],
            'curso_selecionado': '',
        })

@login_required
def criar_aluno(request):
    """Cria um novo aluno."""
    AlunoForm = get_forms()
    
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                aluno = form.save()
                messages.success(request, 'Aluno cadastrado com sucesso!')
                return redirect('alunos:detalhar_aluno', cpf=aluno.cpf)
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
            except Exception as e:
                messages.error(request, f'Erro ao cadastrar aluno: {str(e)}')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = AlunoForm()
    
    return render(request, 'alunos/formulario_aluno.html', {'form': form, 'aluno': None})

@login_required
def detalhar_aluno(request, cpf):
    """Exibe os detalhes de um aluno."""
    Aluno = get_models()
    aluno = get_object_or_404(Aluno, cpf=cpf)
    return render(request, 'alunos/detalhar_aluno.html', {'aluno': aluno})

@login_required
def editar_aluno(request, cpf):
    """Edita um aluno existente."""
    Aluno = get_models()
    AlunoForm = get_forms()
    
    aluno = get_object_or_404(Aluno, cpf=cpf)
    
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES, instance=aluno)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Aluno atualizado com sucesso!')
                return redirect('alunos:detalhar_aluno', cpf=aluno.cpf)
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
            except Exception as e:
                messages.error(request, f'Erro ao atualizar aluno: {str(e)}')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = AlunoForm(instance=aluno)
    
    return render(request, 'alunos/formulario_aluno.html', {'form': form, 'aluno': aluno})

@login_required
def excluir_aluno(request, cpf):
    """Exclui um aluno."""
    Aluno = get_models()
    aluno = get_object_or_404(Aluno, cpf=cpf)
    
    if request.method == 'POST':
        try:
            aluno.delete()
            messages.success(request, 'Aluno excluído com sucesso!')
            return redirect('alunos:listar_alunos')
        except Exception as e:
            messages.error(request, f'Erro ao excluir aluno: {str(e)}')
            return redirect('alunos:detalhar_aluno', cpf=aluno.cpf)
    
    return render(request, 'alunos/excluir_aluno.html', {'aluno': aluno})

@login_required
def dashboard(request):
    """Exibe o dashboard de alunos com estatísticas."""
    try:
        Aluno = get_models()
        total_alunos = Aluno.objects.count()
        
        # Contagem por sexo
        total_masculino = Aluno.objects.filter(sexo='M').count()
        total_feminino = Aluno.objects.filter(sexo='F').count()
        total_outros = Aluno.objects.filter(sexo='O').count()
        
        # Alunos recentes
        alunos_recentes = Aluno.objects.order_by('-created_at')[:5]
        
        context = {
            'total_alunos': total_alunos,
            'total_masculino': total_masculino,
            'total_feminino': total_feminino,
            'total_outros': total_outros,
            'alunos_recentes': alunos_recentes,
        }
        
        return render(request, 'alunos/dashboard.html', context)
    except Exception as e:
        messages.error(request, f"Erro ao carregar dashboard: {str(e)}")
        return redirect('alunos:listar_alunos')

@login_required
def exportar_alunos(request):
    """Exporta os dados dos alunos para um arquivo CSV."""
    try:
        import csv
        from django.http import HttpResponse
        
        Aluno = get_models()
        alunos = Aluno.objects.all()
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="alunos.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['CPF', 'Nome', 'Email', 'Data de Nascimento', 'Sexo', 'Número Iniciático'])
        
        for aluno in alunos:
            writer.writerow([
                aluno.cpf,
                aluno.nome,
                aluno.email,
                aluno.data_nascimento,
                aluno.get_sexo_display(),
                aluno.numero_iniciatico
            ])
        
        return response
    except Exception as e:
        messages.error(request, f"Erro ao exportar alunos: {str(e)}")
        return redirect('alunos:listar_alunos')

@login_required
def importar_alunos(request):
    """Importa alunos de um arquivo CSV."""
    if request.method == 'POST' and request.FILES.get('csv_file'):
        try:
            import csv
            from io import TextIOWrapper
            
            Aluno = get_models()
            csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
            reader = csv.DictReader(csv_file)
            
            count = 0
            errors = []
            
            for row in reader:
                try:
                    # Processar cada linha do CSV
                    Aluno.objects.create(
                        cpf=row.get('CPF', '').strip(),
                        nome=row.get('Nome', '').strip(),
                        email=row.get('Email', '').strip(),
                        data_nascimento=row.get('Data de Nascimento', '').strip(),
                        sexo=row.get('Sexo', 'M')[0].upper(),  # Pega a primeira letra e converte para maiúscula
                        numero_iniciatico=row.get('Número Iniciático', '').strip(),
                        nome_iniciatico=row.get('Nome Iniciático', row.get('Nome', '')).strip(),
                        nacionalidade=row.get('Nacionalidade', 'Brasileira').strip(),
                        naturalidade=row.get('Naturalidade', '').strip(),
                        rua=row.get('Rua', '').strip(),
                        numero_imovel=row.get('Número', '').strip(),
                        complemento=row.get('Complemento', '').strip(),
                        bairro=row.get('Bairro', '').strip(),
                        cidade=row.get('Cidade', '').strip(),
                        estado=row.get('Estado', '').strip(),
                        cep=row.get('CEP', '').strip(),
                        nome_primeiro_contato=row.get('Nome do Primeiro Contato', '').strip(),
                        celular_primeiro_contato=row.get('Celular do Primeiro Contato', '').strip(),
                        tipo_relacionamento_primeiro_contato=row.get('Tipo de Relacionamento do Primeiro Contato', '').strip(),
                        tipo_sanguineo=row.get('Tipo Sanguíneo', '').strip(),
                        fator_rh=row.get('Fator RH', '+').strip(),
                    )
                    count += 1
                except Exception as e:
                    errors.append(f"Erro na linha {count+1}: {str(e)}")
            
            if errors:
                messages.warning(request, f"{count} alunos importados com {len(errors)} erros.")
                for error in errors[:5]:  # Mostrar apenas os 5 primeiros erros
                    messages.error(request, error)
                if len(errors) > 5:
                    messages.error(request, f"... e mais {len(errors) - 5} erros.")
            else:
                messages.success(request, f"{count} alunos importados com sucesso!")
            
            return redirect('alunos:listar_alunos')
        except Exception as e:
            messages.error(request, f"Erro ao importar alunos: {str(e)}")
    
    return render(request, 'alunos/importar_alunos.html')

@login_required
def relatorio_alunos(request):
    """Exibe um relatório com estatísticas sobre os alunos."""
    try:
        Aluno = get_models()
        total_alunos = Aluno.objects.count()
        total_masculino = Aluno.objects.filter(sexo='M').count()
        total_feminino = Aluno.objects.filter(sexo='F').count()
        total_outros = Aluno.objects.filter(sexo='O').count()
        
        # Calcular idade média
        from django.db.models import Avg, F
        from django.db.models.functions import ExtractYear
        from django.utils import timezone
        
        current_year = timezone.now().year
        idade_media = Aluno.objects.annotate(
            idade=current_year - ExtractYear('data_nascimento')
        ).aggregate(Avg('idade'))['idade__avg'] or 0
        
        context = {
            'total_alunos': total_alunos,
            'total_masculino': total_masculino,
            'total_feminino': total_feminino,
            'total_outros': total_outros,
            'idade_media': round(idade_media, 1),
        }
        
        return render(request, 'alunos/relatorio_alunos.html', context)
    except Exception as e:
        messages.error(request, f"Erro ao gerar relatório: {str(e)}")
        return redirect('alunos:listar_alunos')