# Revisão da Funcionalidade: atividades

## Arquivos forms.py:


### Arquivo: atividades\forms.py

python
print("ARQUIVO FORMS.PY CARREGADO")
from django import forms
from importlib import import_module

# resto do c√≥digo...


def get_atividade_academica_model():
    try:
        atividades_module = import_module("atividades.models")
        return getattr(atividades_module, "AtividadeAcademica")
    except (ImportError, AttributeError):
        return None


def get_atividade_ritualistica_model():
    try:
        atividades_module = import_module("atividades.models")
        return getattr(atividades_module, "AtividadeRitualistica")
    except (ImportError, AttributeError):
        return None


class AtividadeAcademicaForm(forms.ModelForm):
    todas_turmas = forms.BooleanField(
        required=False, 
        label="Aplicar a todas as turmas ativas", 
        initial=False
    )
    
    class Meta:
        model = get_atividade_academica_model()
        fields = ["nome", "descricao", "data_inicio", "data_fim", "turmas", "responsavel", 
                  "local", "tipo_atividade", "status"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "data_inicio": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "data_fim": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "turmas": forms.SelectMultiple(attrs={"class": "form-control"}),
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
        model = get_atividade_ritualistica_model()
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


def criar_form_atividade_academica():
    return AtividadeAcademicaForm


def criar_form_atividade_ritualistica():
    return AtividadeRitualisticaForm



## Arquivos views.py:


### Arquivo: atividades\views.py

python
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
import importlib

# Importar a função utilitária centralizada
from core.utils import get_model_dynamically, get_form_dynamically

# Set up logger
logger = logging.getLogger(__name__)

print(
    "ARQUIVO VIEWS.PY CARREGADO:",
    importlib.import_module("django.conf").settings.BASE_DIR,
)


def get_return_url(request, default_url):
    """Obtém a URL de retorno do request ou usa o valor padrão."""
    return_url = request.GET.get("return_url", "")
    # Verificação básica de segurança
    if not return_url or not return_url.startswith("/"):
        return default_url
    return return_url


def get_form_class(form_name):
    """Importa dinamicamente uma classe de formulário para evitar importações circulares."""
    return get_form_dynamically("atividades", form_name)


def get_model_class(model_name, module_name="atividades"):
    """Importa dinamicamente uma classe de modelo para evitar importações circulares."""
    return get_model_dynamically(module_name, model_name)


@login_required
def listar_atividades(request):
    """Página inicial do módulo de atividades."""
    return render(request, "atividades/listar_atividades.html")


@login_required
def listar_atividades_academicas(request):
    """Lista todas as atividades acadêmicas."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    
    # Adicionar suporte para busca e filtros
    query = request.GET.get('q', '')
    turma_id = request.GET.get('turma', '')
    
    atividades = AtividadeAcademica.objects.all().order_by('-data_inicio')
    
    # Aplicar filtros se fornecidos
    if query:
        atividades = atividades.filter(
            nome__icontains=query
        )
    
    if turma_id:
        atividades = atividades.filter(turmas__id=turma_id)
    
    # Paginação
    paginator = Paginator(atividades, 10)  # 10 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Armazenar a URL atual na sessão para uso posterior
    request.session["last_academicas_list_url"] = request.get_full_path()

    # Obter lista de turmas para o filtro
    Turma = get_model_class("Turma", "turmas")
    turmas = Turma.objects.filter(status="A")

    return render(
        request,
        "atividades/listar_atividades_academicas.html",
        {
            "atividades": page_obj,
            "page_obj": page_obj,
            "query": query,
            "turma_selecionada": turma_id,
            "turmas": turmas,
            "return_url": request.path,  # Armazena URL atual para retorno
        },
    )


@login_required
def listar_atividades_ritualisticas(request):
    """Lista todas as atividades ritualísticas."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    
    # Adicionar suporte para busca e filtros
    query = request.GET.get('q', '')
    turma_id = request.GET.get('turma', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    atividades = AtividadeRitualistica.objects.all().order_by('-data')
    
    # Aplicar filtros se fornecidos
    if query:
        atividades = atividades.filter(
            nome__icontains=query
        )
    
    if turma_id:
        atividades = atividades.filter(turma_id=turma_id)
        
    if data_inicio:
        atividades = atividades.filter(data__gte=data_inicio)
        
    if data_fim:
        atividades = atividades.filter(data__lte=data_fim)
    
    # Paginação
    paginator = Paginator(atividades, 10)  # 10 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Armazenar a URL atual na sessão para uso posterior
    request.session["last_ritualisticas_list_url"] = request.get_full_path()

    # Salvar URL referenciadora, exceto se vier do próprio formulário de atividade ritualística
    referer = request.META.get("HTTP_REFERER", "")
    if referer and not any(
        x in referer
        for x in [
            "criar_atividade_ritualistica",
            "editar_atividade_ritualistica",
        ]
    ):
        request.session["atividade_ritualistica_referer"] = referer

    # Usar a URL referenciadora armazenada ou a página inicial como fallback
    previous_url = request.session.get("atividade_ritualistica_referer", "/")
    
    # Obter lista de turmas para o filtro
    Turma = get_model_class("Turma", "turmas")
    turmas = Turma.objects.filter(status="A")

    return render(
        request,
        "atividades/listar_atividades_ritualisticas.html",
        {
            "atividades": page_obj,
            "page_obj": page_obj,
            "query": query,
            "turma_selecionada": turma_id,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "turmas": turmas,
            "previous_url": previous_url,
        },
    )


@login_required
def criar_atividade_academica(request):
    """Função para criar uma nova atividade acadêmica."""
    AtividadeAcademicaForm = get_form_class("AtividadeAcademicaForm")
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )

    if request.method == "POST":
        form = AtividadeAcademicaForm(request.POST)
        if form.is_valid():
            try:
                atividade = form.save(commit=False)
                
                # Verificar se é para todas as turmas
                todas_turmas = form.cleaned_data.get('todas_turmas', False)
                
                # Salvar a atividade primeiro
                atividade.save()
                
                if todas_turmas:
                    # Obter todas as turmas ativas
                    Turma = get_model_class("Turma", "turmas")
                    turmas_ativas = Turma.objects.filter(status="A")
                    
                    # Adicionar todas as turmas ativas
                    atividade.turmas.set(turmas_ativas)
                    
                    # Log para depuração
                    logger.info(f"Atividade {atividade.id} associada a {turmas_ativas.count()} turmas ativas")
                else:
                    # Usar as turmas selecionadas no formulário
                    form.save_m2m()  # Salvar relações ManyToMany
                    
                    # Log para depuração
                    logger.info(f"Atividade {atividade.id} associada a {atividade.turmas.count()} turmas selecionadas")
                
                messages.success(
                    request, "Atividade acadêmica criada com sucesso."
                )
                return redirect(return_url)
            except Exception as e:
                logger.error(f"Erro ao criar atividade acadêmica: {str(e)}", exc_info=True)
                messages.error(request, f"Erro ao criar atividade acadêmica: {str(e)}")
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = AtividadeAcademicaForm()

    return render(
        request,
        "atividades/formulario_atividade_academica.html",
        {"form": form, "return_url": return_url},
    )


@login_required
def editar_atividade_academica(request, pk):
    """Função para editar uma atividade acadêmica existente."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    AtividadeAcademicaForm = get_form_class("AtividadeAcademicaForm")
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )

    if request.method == "POST":
        try:
            form = AtividadeAcademicaForm(request.POST, instance=atividade)
            if form.is_valid():
                atividade = form.save(commit=False)
                
                # Verificar se é para todas as turmas
                todas_turmas = form.cleaned_data.get('todas_turmas', False)
                
                # Salvar a atividade primeiro
                atividade.save()
                
                if todas_turmas:
                    # Obter todas as turmas ativas
                    Turma = get_model_class("Turma", "turmas")
                    turmas_ativas = Turma.objects.filter(status="A")
                    
                    # Adicionar todas as turmas ativas
                    atividade.turmas.set(turmas_ativas)
                    
                    # Log para depuração
                    logger.info(f"Atividade {atividade.id} atualizada com {turmas_ativas.count()} turmas ativas")
                else:
                    # Usar as turmas selecionadas no formulário
                    form.save_m2m()  # Salvar relações ManyToMany
                    
                    # Log para depuração
                    logger.info(f"Atividade {atividade.id} atualizada com {atividade.turmas.count()} turmas selecionadas")
                
                messages.success(
                    request, "Atividade acadêmica atualizada com sucesso."
                )
                return redirect(return_url)
            else:
                messages.error(request, "Corrija os erros no formulário.")
        except Exception as e:
            logger.error(f"Erro ao atualizar atividade acadêmica: {str(e)}", exc_info=True)
            messages.error(
                request,
                f"Erro ao processar formulário de atividade acadêmica: {str(e)}",
            )
    else:
        # Verificar se a atividade está associada a todas as turmas ativas
        Turma = get_model_class("Turma", "turmas")
        turmas_ativas = Turma.objects.filter(status="A")
        todas_turmas_selecionadas = (
            atividade.turmas.count() == turmas_ativas.count() and
            all(turma in atividade.turmas.all() for turma in turmas_ativas)
        )
        
        # Inicializar o formulário com o valor correto para todas_turmas
        form = AtividadeAcademicaForm(
            instance=atividade, 
            initial={'todas_turmas': todas_turmas_selecionadas}
        )

    return render(
        request,
        "atividades/formulario_atividade_academica.html",
        {"form": form, "atividade": atividade, "return_url": return_url},
    )


@login_required
def excluir_atividade_academica(request, pk):
    """Função para excluir uma atividade acadêmica."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )

    if request.method == "POST":
        try:
            nome_atividade = atividade.nome  # Guardar o nome para a mensagem
            atividade.delete()
            messages.success(
                request, f"Atividade acadêmica '{nome_atividade}' excluída com sucesso."
            )
            return redirect(return_url)
        except Exception as e:
            logger.error(f"Erro ao excluir atividade acadêmica: {str(e)}", exc_info=True)
            messages.error(
                request, f"Erro ao excluir atividade acadêmica: {str(e)}"
            )
            return redirect("atividades:listar_atividades_academicas")

    return render(
        request,
        "atividades/confirmar_exclusao_academica.html",
        {"atividade": atividade, "return_url": return_url},
    )


@login_required
def confirmar_exclusao_academica(request, pk):
    """Função para confirmar a exclusão de uma atividade acadêmica."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )

    if request.method == "POST":
        try:
            nome_atividade = atividade.nome  # Guardar o nome para a mensagem
            atividade.delete()
            messages.success(
                request, f"Atividade acadêmica '{nome_atividade}' excluída com sucesso."
            )
            return redirect(return_url)
        except Exception as e:
            logger.error(f"Erro ao excluir atividade acadêmica: {str(e)}", exc_info=True)
            messages.error(
                request, f"Erro ao excluir atividade acadêmica: {str(e)}"
            )
            return redirect("atividades:detalhar_atividade_academica", pk=pk)

    return render(
        request,
        "atividades/confirmar_exclusao_academica.html",
        {"atividade": atividade, "return_url": return_url},
    )


@login_required
def detalhar_atividade_academica(request, pk):
    """Função para mostrar detalhes de uma atividade acadêmica."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )
    
    # Calcular estatísticas sobre as turmas
    total_turmas = atividade.turmas.count()
    turmas_ativas = atividade.turmas.filter(status="A").count()
    
    # Verificar se está associada a todas as turmas ativas do sistema
    Turma = get_model_class("Turma", "turmas")
    total_turmas_ativas_sistema = Turma.objects.filter(status="A").count()
    todas_turmas_ativas = (turmas_ativas == total_turmas_ativas_sistema)

    return render(
        request,
        "atividades/detalhar_atividade_academica.html",
        {
            "atividade": atividade, 
            "return_url": return_url,
            "total_turmas": total_turmas,
            "turmas_ativas": turmas_ativas,
            "todas_turmas_ativas": todas_turmas_ativas
        },
    )


@login_required
def criar_atividade_ritualistica(request):
    """Função para criar uma nova atividade ritualística."""
    AtividadeRitualisticaForm = get_form_class("AtividadeRitualisticaForm")
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    if request.method == "POST":
        try:
            form = AtividadeRitualisticaForm(request.POST)
            if form.is_valid():
                atividade = form.save(commit=False)
                atividade.save()

                # Processar o campo todos_alunos se existir
                if hasattr(form, "cleaned_data") and form.cleaned_data.get(
                    "todos_alunos"
                ):
                    # Obter todos os alunos da turma e adicioná-los à atividade
                    Aluno = get_model_class(
                        "Aluno", module_name="alunos"
                    )
                    alunos_da_turma = Aluno.objects.filter(
                        turmas=atividade.turma
                    )
                    for aluno in alunos_da_turma:
                        atividade.participantes.add(aluno)
                else:
                    # Salvar apenas os participantes selecionados no formulário
                    form.save_m2m()

                messages.success(
                    request, "Atividade ritualística criada com sucesso."
                )
                return redirect(return_url)
            else:
                messages.error(request, "Corrija os erros no formulário.")
        except Exception as e:
            logger.error(f"Erro ao criar atividade ritualística: {str(e)}", exc_info=True)
            messages.error(
                request,
                f"Erro ao processar formulário de atividade ritualística: {str(e)}",
            )
    else:
        form = AtividadeRitualisticaForm()

    return render(
        request,
        "atividades/criar_atividade_ritualistica.html",
        {"form": form, "return_url": return_url},
    )


@login_required
def editar_atividade_ritualistica(request, pk):
    """Função para editar uma atividade ritualística existente."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    AtividadeRitualisticaForm = get_form_class("AtividadeRitualisticaForm")
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    if request.method == "POST":
        try:
            form = AtividadeRitualisticaForm(request.POST, instance=atividade)
            if form.is_valid():
                atividade = form.save(commit=False)
                atividade.save()

                # Processar o campo todos_alunos se existir
                if hasattr(form, "cleaned_data") and form.cleaned_data.get(
                    "todos_alunos"
                ):
                    # Limpar participantes existentes
                    atividade.participantes.clear()
                    # Obter todos os alunos da turma e adicioná-los à atividade
                    Aluno = get_model_class(
                        "Aluno", module_name="alunos"
                    )
                    alunos_da_turma = Aluno.objects.filter(
                        turmas=atividade.turma
                    )
                    for aluno in alunos_da_turma:
                        atividade.participantes.add(aluno)
                else:
                    # Salvar apenas os participantes selecionados no formulário
                    form.save_m2m()

                messages.success(
                    request, "Atividade ritualística atualizada com sucesso."
                )
                return redirect(return_url)
            else:
                messages.error(request, "Corrija os erros no formulário.")
        except Exception as e:
            logger.error(f"Erro ao atualizar atividade ritualística: {str(e)}", exc_info=True)
            messages.error(
                request,
                f"Erro ao processar formulário de atividade ritualística: {str(e)}",
            )
    else:
        form = AtividadeRitualisticaForm(instance=atividade)

    return render(
        request,
        "atividades/editar_atividade_ritualistica.html",
        {"form": form, "atividade": atividade, "return_url": return_url},
    )


@login_required
def excluir_atividade_ritualistica(request, pk):
    """Função para excluir uma atividade ritualística."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    if request.method == "POST":
        try:
            nome_atividade = atividade.nome  # Guardar o nome para a mensagem
            atividade.delete()
            messages.success(
                request, f"Atividade ritualística '{nome_atividade}' excluída com sucesso."
            )
            return redirect(return_url)
        except Exception as e:
            logger.error(f"Erro ao excluir atividade ritualística: {str(e)}", exc_info=True)
            messages.error(
                request, f"Erro ao excluir atividade ritualística: {str(e)}"
            )
            return redirect("atividades:listar_atividades_ritualisticas")

    return render(
        request,
        "atividades/confirmar_exclusao_ritualistica.html",
        {"atividade": atividade, "return_url": return_url},
    )


@login_required
def confirmar_exclusao_ritualistica(request, pk):
    """Função para confirmar a exclusão de uma atividade ritualística."""
    AtividadeRitualistica = get
@login_required
def confirmar_exclusao_ritualistica(request, pk):
    """Função para confirmar a exclusão de uma atividade ritualística."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    if request.method == "POST":
        try:
            nome_atividade = atividade.nome  # Guardar o nome para a mensagem
            atividade.delete()
            messages.success(
                request, f"Atividade ritualística '{nome_atividade}' excluída com sucesso."
            )
            return redirect(return_url)
        except Exception as e:
            logger.error(f"Erro ao excluir atividade ritualística: {str(e)}", exc_info=True)
            messages.error(
                request, f"Erro ao excluir atividade ritualística: {str(e)}"
            )
            return redirect(
                "atividades:detalhar_atividade_ritualistica", pk=pk
            )

    return render(
        request,
        "atividades/confirmar_exclusao_ritualistica.html",
        {"atividade": atividade, "return_url": return_url},
    )


@login_required
def detalhar_atividade_ritualistica(request, pk):
    """Função para mostrar detalhes de uma atividade ritualística."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    # Calcular o total de participantes para exibição
    total_participantes = atividade.participantes.count()
    
    # Verificar se todos os alunos da turma estão participando
    Aluno = get_model_class("Aluno", module_name="alunos")
    total_alunos_turma = Aluno.objects.filter(turmas=atividade.turma).count()
    todos_alunos_participando = (total_participantes == total_alunos_turma) and (total_alunos_turma > 0)

    return render(
        request,
        "atividades/detalhar_atividade_ritualistica.html",
        {
            "atividade": atividade, 
            "return_url": return_url,
            "total_participantes": total_participantes,
            "total_alunos_turma": total_alunos_turma,
            "todos_alunos_participando": todos_alunos_participando
        },
    )


@login_required
def relatorio_atividades(request):
    """Gera um relatório de atividades com base nos filtros aplicados."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    
    # Obter parâmetros de filtro
    tipo = request.GET.get('tipo', 'todas')
    status = request.GET.get('status', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Filtrar atividades acadêmicas
    atividades_academicas = AtividadeAcademica.objects.all()
    
    if status:
        atividades_academicas = atividades_academicas.filter(status=status)
    
    if data_inicio:
        atividades_academicas = atividades_academicas.filter(data_inicio__gte=data_inicio)
    
    if data_fim:
        atividades_academicas = atividades_academicas.filter(data_inicio__lte=data_fim)
    
    # Filtrar atividades ritualísticas
    atividades_ritualisticas = AtividadeRitualistica.objects.all()
    
    if data_inicio:
        atividades_ritualisticas = atividades_ritualisticas.filter(data__gte=data_inicio)
    
    if data_fim:
        atividades_ritualisticas = atividades_ritualisticas.filter(data__lte=data_fim)
    
    # Aplicar filtro por tipo
    if tipo == 'academicas':
        atividades_ritualisticas = AtividadeRitualistica.objects.none()
    elif tipo == 'ritualisticas':
        atividades_academicas = AtividadeAcademica.objects.none()
    
    # Calcular totais
    total_academicas = atividades_academicas.count()
    total_ritualisticas = atividades_ritualisticas.count()
    total_atividades = total_academicas + total_ritualisticas
    
    return render(
        request,
        "atividades/relatorio_atividades.html",
        {
            "atividades_academicas": atividades_academicas,
            "atividades_ritualisticas": atividades_ritualisticas,
            "total_academicas": total_academicas,
            "total_ritualisticas": total_ritualisticas,
            "total_atividades": total_atividades,
            "tipo": tipo,
            "status": status,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
        },
    )


@login_required
def exportar_atividades(request, formato):
    """Exporta as atividades filtradas para o formato especificado."""
    # Obter os mesmos filtros que no relatório
    tipo = request.GET.get('tipo', 'todas')
    status = request.GET.get('status', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Obter atividades filtradas (mesmo código do relatório)
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    
    atividades_academicas = AtividadeAcademica.objects.all()
    if status:
        atividades_academicas = atividades_academicas.filter(status=status)
    if data_inicio:
        atividades_academicas = atividades_academicas.filter(data_inicio__gte=data_inicio)
    if data_fim:
        atividades_academicas = atividades_academicas.filter(data_inicio__lte=data_fim)
    
    atividades_ritualisticas = AtividadeRitualistica.objects.all()
    if data_inicio:
        atividades_ritualisticas = atividades_ritualisticas.filter(data__gte=data_inicio)
    if data_fim:
        atividades_ritualisticas = atividades_ritualisticas.filter(data__lte=data_fim)
    
    if tipo == 'academicas':
        atividades_ritualisticas = AtividadeRitualistica.objects.none()
    elif tipo == 'ritualisticas':
        atividades_academicas = AtividadeAcademica.objects.none()
    
    # Exportar para o formato solicitado
    if formato == 'csv':
        return exportar_atividades_csv(atividades_academicas, atividades_ritualisticas)
    elif formato == 'excel':
        return exportar_atividades_excel(atividades_academicas, atividades_ritualisticas)
    elif formato == 'pdf':
        return exportar_atividades_pdf(atividades_academicas, atividades_ritualisticas)
    else:
        messages.error(request, f"Formato de exportação '{formato}' não suportado.")
        return redirect('atividades:relatorio_atividades')

def exportar_atividades_csv(atividades_academicas, atividades_ritualisticas):
    """Exporta as atividades para CSV."""
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="atividades.csv"'
    
    writer = csv.writer(response)
    
    # Cabeçalho para atividades acadêmicas
    writer.writerow(['Tipo', 'Nome', 'Descrição', 'Data de Início', 'Data de Término', 
                     'Responsável', 'Local', 'Status', 'Tipo de Atividade'])
    
    # Dados das atividades acadêmicas
    for atividade in atividades_academicas:
        writer.writerow([
            'Acadêmica',
            atividade.nome,
            atividade.descricao or '',
            atividade.data_inicio.strftime('%d/%m/%Y'),
            atividade.data_fim.strftime('%d/%m/%Y') if atividade.data_fim else '',
            atividade.responsavel or '',
            atividade.local or '',
            atividade.get_status_display(),
            atividade.get_tipo_atividade_display(),
        ])
    
    # Dados das atividades ritualísticas
    for atividade in atividades_ritualisticas:
        writer.writerow([
            'Ritualística',
            atividade.nome,
            atividade.descricao or '',
            atividade.data.strftime('%d/%m/%Y'),
            '',  # Não tem data_fim
            '',  # Não tem responsável
            atividade.local,
            '',  # Não tem status
            '',  # Não tem tipo_atividade
        ])
    
    return response

def exportar_atividades_excel(atividades_academicas, atividades_ritualisticas):
    """Exporta as atividades para Excel."""
    # Implementação básica usando pandas
    try:
        import pandas as pd
        from django.http import HttpResponse
        from io import BytesIO
        
        # Criar DataFrames para cada tipo de atividade
        dados_academicas = []
        for atividade in atividades_academicas:
            dados_academicas.append({
                'Tipo': 'Acadêmica',
                'Nome': atividade.nome,
                'Descrição': atividade.descricao or '',
                'Data de Início': atividade.data_inicio,
                'Data de Término': atividade.data_fim,
                'Responsável': atividade.responsavel or '',
                'Local': atividade.local or '',
                'Status': atividade.get_status_display(),
                'Tipo de Atividade': atividade.get_tipo_atividade_display(),
            })
        
        dados_ritualisticas = []
        for atividade in atividades_ritualisticas:
            dados_ritualisticas.append({
                'Tipo': 'Ritualística',
                'Nome': atividade.nome,
                'Descrição': atividade.descricao or '',
                'Data': atividade.data,
                'Horário': f"{atividade.hora_inicio} - {atividade.hora_fim}",
                'Local': atividade.local,
                'Turma': atividade.turma.nome,
                'Participantes': atividade.participantes.count(),
            })
        
        # Criar arquivo Excel com múltiplas abas
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            if dados_academicas:
                df_academicas = pd.DataFrame(dados_academicas)
                df_academicas.to_excel(writer, sheet_name='Atividades Acadêmicas', index=False)
            
            if dados_ritualisticas:
                df_ritualisticas = pd.DataFrame(dados_ritualisticas)
                df_ritualisticas.to_excel(writer, sheet_name='Atividades Ritualísticas', index=False)
        
        # Configurar resposta HTTP
        output.seek(0)
        response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="atividades.xlsx"'
        
        return response
    except ImportError:
        # Fallback para CSV se pandas não estiver disponível
        return exportar_atividades_csv(atividades_academicas, atividades_ritualisticas)

def exportar_atividades_pdf(atividades_academicas, atividades_ritualisticas):
    """Exporta as atividades para PDF."""
    # Implementação básica usando reportlab
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from django.http import HttpResponse
        import io
        
        # Configurar buffer e documento
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        subtitle_style = styles['Heading2']
        
        # Título
        elements.append(Paragraph("Relatório de Atividades", title_style))
        elements.append(Spacer(1, 12))
        
        # Atividades Acadêmicas
        if atividades_academicas:
            elements.append(Paragraph("Atividades Acadêmicas", subtitle_style))
            elements.append(Spacer(1, 6))
            
            # Dados para a tabela
            data = [['Nome', 'Tipo', 'Data de Início', 'Status', 'Responsável']]
            
            for atividade in atividades_academicas:
                data.append([
                    atividade.nome,
                    atividade.get_tipo_atividade_display(),
                    atividade.data_inicio.strftime('%d/%m/%Y'),
                    atividade.get_status_display(),
                    atividade.responsavel or 'Não informado',
                ])
            
            # Criar tabela
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 12))
        
        # Atividades Ritualísticas
        if atividades_ritualisticas:
            elements.append(Paragraph("Atividades Ritualísticas", subtitle_style))
            elements.append(Spacer(1, 6))
            
            # Dados para a tabela
            data = [['Nome', 'Data', 'Horário', 'Local', 'Turma', 'Participantes']]
            
            for atividade in atividades_ritualisticas:
                data.append([
                    atividade.nome,
                    atividade.data.strftime('%d/%m/%Y'),
                    f"{atividade.hora_inicio} - {atividade.hora_fim}",
                    atividade.local,
                    atividade.turma.nome,
                    str(atividade.participantes.count()),
                ])
            
            # Criar tabela
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            elements.append(table)
        
        # Gerar PDF
        doc.build(elements)
        
        # Configurar resposta HTTP
        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="atividades.pdf"'
        
        return response
    except ImportError:
        # Fallback para CSV se reportlab não estiver disponível
        return exportar_atividades_csv(atividades_academicas, atividades_ritualisticas)
@login_required
def calendario_atividades(request):
    """Exibe o calendário de atividades."""
    # Obter todas as turmas para o filtro
    Turma = get_model_dynamically("turmas", "Turma")
    turmas = Turma.objects.filter(status='A')  # Apenas turmas ativas
    
    return render(
        request,
        "atividades/calendario_atividades.html",
        {
            "turmas": turmas,
        },
    )

@login_required
def api_eventos_calendario(request):
    """API para fornecer eventos para o calendário."""
    from django.http import JsonResponse
    
    # Obter parâmetros
    start_date = request.GET.get('start', '')
    end_date = request.GET.get('end', '')
    tipo_filtro = request.GET.get('tipo', 'todas')
    turma_filtro = request.GET.get('turma', 'todas')
    mostrar_concluidas = request.GET.get('concluidas', '1') == '1'
    
    # Obter modelos
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    
    eventos = []
    
    # Adicionar atividades acadêmicas
    if tipo_filtro in ['todas', 'academicas']:
        atividades_academicas = AtividadeAcademica.objects.all()
        
        # Aplicar filtro de data
        if start_date:
            atividades_academicas = atividades_academicas.filter(data_inicio__gte=start_date)
        if end_date:
            atividades_academicas = atividades_academicas.filter(data_inicio__lte=end_date)
        
        # Aplicar filtro de turma
        if turma_filtro != 'todas':
            atividades_academicas = atividades_academicas.filter(turma_id=turma_filtro)
        
        # Aplicar filtro de status concluído
        if not mostrar_concluidas:
            atividades_academicas = atividades_academicas.exclude(status='concluida')
        
        # Converter para formato de evento do FullCalendar
        for atividade in atividades_academicas:
            evento = {
                'id': atividade.id,
                'title': atividade.nome,
                'start': atividade.data_inicio.isoformat(),
                'end': atividade.data_fim.isoformat() if atividade.data_fim else None,
                'allDay': True,  # Por padrão, eventos de dia inteiro
                'tipo': 'academica',
                'status': atividade.status,
                'description': atividade.descricao or '',
            }
            eventos.append(evento)
    
    # Adicionar atividades ritualísticas
    if tipo_filtro in ['todas', 'ritualisticas']:
        atividades_ritualisticas = AtividadeRitualistica.objects.all()
        
        # Aplicar filtro de data
        if start_date:
            atividades_ritualisticas = atividades_ritualisticas.filter(data__gte=start_date)
        if end_date:
            atividades_ritualisticas = atividades_ritualisticas.filter(data__lte=end_date)
        
        # Aplicar filtro de turma
        if turma_filtro != 'todas':
            atividades_ritualisticas = atividades_ritualisticas.filter(turma_id=turma_filtro)
        
        # Converter para formato de evento do FullCalendar
        for atividade in atividades_ritualisticas:
            # Combinar data e hora para criar datetime completo
            from datetime import datetime, time
            data = atividade.data
            
            # Converter hora_inicio e hora_fim para objetos time
            hora_inicio = atividade.hora_inicio
            hora_fim = atividade.hora_fim
            
            # Criar datetime para início e fim
            start_datetime = datetime.combine(data, hora_inicio)
            end_datetime = datetime.combine(data, hora_fim)
            
            evento = {
                'id': atividade.id,
                'title': atividade.nome,
                'start': start_datetime.isoformat(),
                'end': end_datetime.isoformat(),
                'allDay': False,  # Eventos ritualísticos têm horário específico
                'tipo': 'ritualistica',
                'description': atividade.descricao or '',
            }
            eventos.append(evento)
    
    return JsonResponse(eventos, safe=False)

@login_required
def api_detalhe_evento(request, evento_id):
    """API para fornecer detalhes de um evento específico."""
    from django.http import JsonResponse
    
    tipo = request.GET.get('tipo', '')
    
    try:
        if tipo == 'academica':
            AtividadeAcademica = get_model_class("AtividadeAcademica")
            atividade = get_object_or_404(AtividadeAcademica, id=evento_id)
            
            # Formatar dados para resposta JSON
            evento = {
                'nome': atividade.nome,
                'descricao': atividade.descricao,
                'data_inicio': atividade.data_inicio.strftime('%d/%m/%Y'),
                'data_fim': atividade.data_fim.strftime('%d/%m/%Y') if atividade.data_fim else None,
                'responsavel': atividade.responsavel,
                'local': atividade.local,
                'tipo': atividade.tipo_atividade,
                'tipo_display': atividade.get_tipo_atividade_display(),
                'status': atividade.status,
                'status_display': atividade.get_status_display(),
                'turma': atividade.turma.nome if atividade.turma else 'Sem turma',
            }
            
            return JsonResponse({'success': True, 'evento': evento})
        
        elif tipo == 'ritualistica':
            AtividadeRitualistica = get_model_class("AtividadeRitualistica")
            atividade = get_object_or_404(AtividadeRitualistica, id=evento_id)
            
            # Formatar dados para resposta JSON
            evento = {
                'nome': atividade.nome,
                'descricao': atividade.descricao,
                'data': atividade.data.strftime('%d/%m/%Y'),
                'hora_inicio': atividade.hora_inicio.strftime('%H:%M'),
                'hora_fim': atividade.hora_fim.strftime('%H:%M'),
                'local': atividade.local,
                'turma': atividade.turma.nome if atividade.turma else 'Sem turma',
                'total_participantes': atividade.participantes.count(),
            }
            
            return JsonResponse({'success': True, 'evento': evento})
        
        else:
            return JsonResponse({'success': False, 'error': 'Tipo de evento inválido'}, status=400)
    
    except Exception as e:
        logger.error(f"Erro ao obter detalhes do evento: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
@login_required
def dashboard_atividades(request):
    """Exibe o dashboard de atividades com estatísticas e gráficos."""
    import json
    from datetime import datetime, timedelta
    from django.db.models import Count
    from django.db.models.functions import TruncMonth
    
    # Obter modelos
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    
    # Estatísticas gerais
    total_academicas = AtividadeAcademica.objects.count()
    total_ritualisticas = AtividadeRitualistica.objects.count()
    total_atividades = total_academicas + total_ritualisticas
    
    # Estatísticas de status (apenas para atividades acadêmicas)
    status_counts = dict(AtividadeAcademica.objects.values('status').annotate(count=Count('status')).values_list('status', 'count'))
    total_agendadas = status_counts.get('agendada', 0)
    
    # Atividades por mês (últimos 6 meses)
    hoje = datetime.now().date()
    seis_meses_atras = hoje - timedelta(days=180)
    
    # Preparar dados para o gráfico de atividades por mês
    academicas_por_mes = AtividadeAcademica.objects.filter(
        data_inicio__gte=seis_meses_atras
    ).annotate(
        mes=TruncMonth('data_inicio')
    ).values('mes').annotate(
        count=Count('id')
    ).order_by('mes')
    
    ritualisticas_por_mes = AtividadeRitualistica.objects.filter(
        data__gte=seis_meses_atras
    ).annotate(
        mes=TruncMonth('data')
    ).values('mes').annotate(
        count=Count('id')
    ).order_by('mes')
    
    # Converter para dicionários para facilitar o acesso
    academicas_dict = {item['mes'].strftime('%Y-%m'): item['count'] for item in academicas_por_mes}
    ritualisticas_dict = {item['mes'].strftime('%Y-%m'): item['count'] for item in ritualisticas_por_mes}
    
    # Gerar lista de meses (últimos 6 meses)
    meses = []
    academicas_counts = []
    ritualisticas_counts = []
    
    for i in range(5, -1, -1):
        mes_data = hoje.replace(day=1) - timedelta(days=i*30)
        mes_str = mes_data.strftime('%Y-%m')
        mes_nome = mes_data.strftime('%b/%Y')
        
        meses.append(mes_nome)
        academicas_counts.append(academicas_dict.get(mes_str, 0))
        ritualisticas_counts.append(ritualisticas_dict.get(mes_str, 0))
    
    # Próximas atividades
    proximas_academicas = AtividadeAcademica.objects.filter(
        data_inicio__gte=hoje
    ).exclude(
        status='cancelada'
    ).order_by('data_inicio')[:5]
    
    proximas_ritualisticas = AtividadeRitualistica.objects.filter(
        data__gte=hoje
    ).order_by('data', 'hora_inicio')[:5]
    
    # Adicionar tipo para facilitar o template
    for atividade in proximas_academicas:
        atividade.tipo = 'academica'
    
    for atividade in proximas_ritualisticas:
        atividade.tipo = 'ritualistica'
    
    # Combinar e ordenar por data
    proximas_atividades = sorted(
        list(proximas_academicas) + list(proximas_ritualisticas),
        key=lambda x: x.data_inicio if hasattr(x, 'data_inicio') else x.data
    )[:5]
    
    # Atividades recentes
    recentes_academicas = AtividadeAcademica.objects.filter(
        data_inicio__lt=hoje
    ).order_by('-data_inicio')[:5]
    
    recentes_ritualisticas = AtividadeRitualistica.objects.filter(
        data__lt=hoje
    ).order_by('-data')[:5]
    
    # Adicionar tipo para facilitar o template
    for atividade in recentes_academicas:
        atividade.tipo = 'academica'
    
    for atividade in recentes_ritualisticas:
        atividade.tipo = 'ritualistica'
    
    # Combinar e ordenar por data (decrescente)
    atividades_recentes = sorted(
        list(recentes_academicas) + list(recentes_ritualisticas),
        key=lambda x: x.data_inicio if hasattr(x, 'data_inicio') else x.data,
        reverse=True
    )[:5]
    
    return render(
        request,
        "atividades/dashboard_atividades.html",
        {
            "total_atividades": total_atividades,
            "total_academicas": total_academicas,
            "total_ritualisticas": total_ritualisticas,
            "total_agendadas": total_agendadas,
            "meses": meses,
            "academicas_counts": academicas_counts,
            "ritualisticas_counts": ritualisticas_counts,
            "proximas_atividades": proximas_atividades,
            "atividades_recentes": atividades_recentes,
        },
    )
@login_required
def copiar_atividade_academica(request, id):
    """Cria uma cópia de uma atividade acadêmica existente."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    AtividadeAcademicaForm = get_form_class("AtividadeAcademicaForm")
    
    # Obter atividade original
    atividade_original = get_object_or_404(AtividadeAcademica, id=id)
    
    if request.method == "POST":
        # Criar formulário com dados do POST
        form = AtividadeAcademicaForm(request.POST)
        
        if form.is_valid():
            # Salvar nova atividade
            nova_atividade = form.save()
            
            # Verificar se deve copiar frequências
            copiar_frequencias = request.POST.get('copiar_frequencias') == 'on'
            
            if copiar_frequencias:
                try:
                    # Importar modelo de Frequencia
                    Frequencia = get_model_dynamically("frequencias", "Frequencia")
                    
                    # Obter frequências da atividade original
                    frequencias_originais = Frequencia.objects.filter(atividade=atividade_original)
                    
                    # Criar novas frequências
                    for freq in frequencias_originais:
                        Frequencia.objects.create(
                            aluno=freq.aluno,
                            atividade=nova_atividade,
                            data=nova_atividade.data_inicio,  # Usar a nova data
                            presente=False,  # Inicialmente todos ausentes
                            justificativa=None
                        )
                    
                    messages.success(
                        request, 
                        f"Atividade copiada com sucesso! {frequencias_originais.count()} registros de frequência foram copiados."
                    )
                except Exception as e:
                    logger.error(f"Erro ao copiar frequências: {str(e)}")
                    messages.warning(
                        request, 
                        f"Atividade copiada, mas ocorreu um erro ao copiar as frequências: {str(e)}"
                    )
            else:
                messages.success(request, "Atividade copiada com sucesso!")
            
            return redirect("atividades:detalhar_atividade_academica", pk=nova_atividade.id)
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        # Pré-preencher formulário com dados da atividade original
        initial_data = {
            'nome': f"Cópia de {atividade_original.nome}",
            'descricao': atividade_original.descricao,
            'tipo_atividade': atividade_original.tipo_atividade,
            'responsavel': atividade_original.responsavel,
            'local': atividade_original.local,
            'turma': atividade_original.turma,
            'status': 'agendada',  # Sempre começa como agendada
        }
        form = AtividadeAcademicaForm(initial=initial_data)
    
    return render(
        request,
        "atividades/copiar_atividade_academica.html",
        {
            "form": form,
            "atividade_original": atividade_original,
        },
    )

@login_required
def copiar_atividade_ritualistica(request, id):
    """Cria uma cópia de uma atividade ritualística existente."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    AtividadeRitualisticaForm = get_form_class("AtividadeRitualisticaForm")
    
    # Obter atividade original
    atividade_original = get_object_or_404(AtividadeRitualistica, id=id)
    
    if request.method == "POST":
        # Criar formulário com dados do POST
        form = AtividadeRitualisticaForm(request.POST)
        
        if form.is_valid():
            # Salvar nova atividade sem os participantes
            nova_atividade = form.save(commit=False)
            nova_atividade.save()
            
            # Verificar se deve copiar participantes
            copiar_participantes = request.POST.get('copiar_participantes') == 'on'
            
            if copiar_participantes:
                # Copiar participantes da atividade original
                for participante in atividade_original.participantes.all():
                    nova_atividade.participantes.add(participante)
                
                messages.success(
                    request, 
                    f"Atividade copiada com sucesso! {atividade_original.participantes.count()} participantes foram copiados."
                )
            else:
                # Salvar apenas os participantes selecionados no formulário
                form.save_m2m()
                messages.success(request, "Atividade copiada com sucesso!")
            
            return redirect("atividades:detalhar_atividade_ritualistica", pk=nova_atividade.id)
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        # Pré-preencher formulário com dados da atividade original
        form = AtividadeRitualisticaForm(instance=atividade_original)
    
    context = {
        "form": form,
        "atividade": atividade_original,
    }
    
    return render(request, "atividades/copiar_atividade_ritualistica.html", context)



## Arquivos urls.py:


### Arquivo: atividades\urls.py

python
from django.urls import path
from . import views

app_name = "atividades"  # Definindo o namespace

urlpatterns = [
    path("", views.listar_atividades, name="listar_atividades"),
    # Atividades Acadêmicas
    path(
        "academicas/",
        views.listar_atividades_academicas,
        name="listar_atividades_academicas",
    ),
    path(
        "academicas/criar/",
        views.criar_atividade_academica,
        name="criar_atividade_academica",
    ),
    path(
        "academicas/editar/<int:pk>/",
        views.editar_atividade_academica,
        name="editar_atividade_academica",
    ),
    path(
        "academicas/excluir/<int:pk>/",
        views.excluir_atividade_academica,
        name="excluir_atividade_academica",
    ),
    path(
        "academicas/detalhar/<int:pk>/",
        views.detalhar_atividade_academica,
        name="detalhar_atividade_academica",
    ),
    path(
        "academicas/confirmar-exclusao/<int:pk>/",
        views.confirmar_exclusao_academica,
        name="confirmar_exclusao_academica",
    ),
    path(
        "academicas/<int:id>/copiar/",
        views.copiar_atividade_academica,
        name="copiar_atividade_academica",
    ),
    # Atividades Ritualísticas
    path(
        "ritualisticas/",
        views.listar_atividades_ritualisticas,
        name="listar_atividades_ritualisticas",
    ),
    path(
        "ritualisticas/criar/",
        views.criar_atividade_ritualistica,
        name="criar_atividade_ritualistica",
    ),
    path(
        "ritualisticas/editar/<int:pk>/",
        views.editar_atividade_ritualistica,
        name="editar_atividade_ritualistica",
    ),
    path(
        "ritualisticas/excluir/<int:pk>/",
        views.excluir_atividade_ritualistica,
        name="excluir_atividade_ritualistica",
    ),
    path(
        "ritualisticas/detalhar/<int:pk>/",
        views.detalhar_atividade_ritualistica,
        name="detalhar_atividade_ritualistica",
    ),
    path(
        "ritualisticas/confirmar-exclusao/<int:pk>/",
        views.confirmar_exclusao_ritualistica,
        name="confirmar_exclusao_ritualistica",
    ),
    path(
        "ritualisticas/<int:id>/copiar/",
        views.copiar_atividade_ritualistica,
        name="copiar_atividade_ritualistica",
    ),
    # Novas funcionalidades
    path("relatorio/", views.relatorio_atividades, name="relatorio_atividades"),
    path("exportar/<str:formato>/", views.exportar_atividades, name="exportar_atividades"),
    path("calendario/", views.calendario_atividades, name="calendario_atividades"),
    path("dashboard/", views.dashboard_atividades, name="dashboard_atividades"),
    # APIs
    path("api/eventos/", views.api_eventos_calendario, name="api_eventos_calendario"),
    path("api/evento/<int:evento_id>/", views.api_detalhe_evento, name="api_detalhe_evento"),
]



## Arquivos models.py:


### Arquivo: atividades\models.py

python
# Adicione o seguinte código temporário para diagnóstico no início do arquivo:

print("CARREGANDO MODELS.PY")
# Imprimir os campos do modelo para diagnóstico
try:
    from django.db import models
    import inspect

    # Carregar o módulo atual
    import sys

    current_module = sys.modules[__name__]

    # Encontrar todas as classes de modelo no módulo
    for name, obj in inspect.getmembers(current_module):
        if (
            inspect.isclass(obj)
            and issubclass(obj, models.Model)
            and obj != models.Model
        ):
            print(f"Modelo: {name}")
            for field in obj._meta.fields:
                print(f"  - {field.name} ({field.__class__.__name__})")
except Exception as e:
    print(f"Erro ao inspecionar modelos: {e}")

from django.db import models
from django.utils import timezone
from importlib import import_module


def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_turma_model():
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


class AtividadeAcademica(models.Model):
    TIPO_CHOICES = (
        ("aula", "Aula"),
        ("palestra", "Palestra"),
        ("workshop", "Workshop"),
        ("seminario", "Seminário"),
        ("outro", "Outro"),
    )

    STATUS_CHOICES = (
        ("agendada", "Agendada"),
        ("em_andamento", "Em Andamento"),
        ("concluida", "Concluída"),
        ("cancelada", "Cancelada"),
    )

    nome = models.CharField(max_length=100)

    @property
    def titulo(self):
        return self.nome

    @titulo.setter
    def titulo(self, value):
        self.nome = value

    descricao = models.TextField(
        blank=True, null=True, verbose_name="Descrição"
    )
    data_inicio = models.DateTimeField(
        default=timezone.now, verbose_name="Data de Início"
    )
    data_fim = models.DateTimeField(
        blank=True, null=True, verbose_name="Data de Término"
    )
    responsavel = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Responsável"
    )
    local = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Local"
    )
    tipo_atividade = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default="aula",
        verbose_name="Tipo de Atividade",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="agendada",
        verbose_name="Status",
    )
    
    # Novo campo para múltiplas turmas
    turmas = models.ManyToManyField(
        "turmas.Turma",
        related_name="atividades_academicas",
        verbose_name="Turmas"
    )

    def __str__(self):
        return self.titulo or self.nome

    class Meta:
        verbose_name = "Atividade Acadêmica"
        verbose_name_plural = "Atividades Acadêmicas"


class AtividadeRitualistica(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")
    descricao = models.TextField(
        blank=True, null=True, verbose_name="Descrição"
    )
    data = models.DateField(verbose_name="Data")
    hora_inicio = models.TimeField(verbose_name="Hora de Início")
    hora_fim = models.TimeField(verbose_name="Hora de Término")
    local = models.CharField(max_length=100, verbose_name="Local")
    turma = models.ForeignKey(
        get_turma_model(), on_delete=models.CASCADE, verbose_name="Turma"
    )
    participantes = models.ManyToManyField(
        get_aluno_model(),
        blank=True,
        verbose_name="Participantes",
        related_name="atividades_ritualisticas",
    )

    def __str__(self):
        return f"{self.nome} - {self.data}"

    class Meta:
        verbose_name = "Atividade Ritualística"
        verbose_name_plural = "Atividades Ritualísticas"
        ordering = ["-data", "hora_inicio"]



## Arquivos de Template:


### Arquivo: atividades\templates\atividades\calendario_atividades.html

html
{% extends 'base.html' %}

{% block title %}Calendário de Atividades{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.min.css">
<style>
    #calendar {
        max-width: 1100px;
        margin: 0 auto;
    }
    
    .fc-event {
        cursor: pointer;
    }
    
    .fc-event-title {
        font-weight: bold;
    }
    
    .fc-event-time {
        font-size: 0.9em;
    }
    
    .academica-event {
        background-color: #0d6efd;
        border-color: #0d6efd;
    }
    
    .ritualistica-event {
        background-color: #17a2b8;
        border-color: #17a2b8;
    }
    
    .agendada-event {
        border-left: 5px solid #ffc107;
    }
    
    .em_andamento-event {
        border-left: 5px solid #0dcaf0;
    }
    
    .concluida-event {
        border-left: 5px solid #198754;
    }
    
    .cancelada-event {
        border-left: 5px solid #dc3545;
        text-decoration: line-through;
        opacity: 0.7;
    }
</style>
{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Calendário de Atividades</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'atividades:dashboard_atividades' %}" class="btn btn-primary me-2">Dashboard</a>
            <div class="btn-group">
                <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-outline-primary">Atividades Acadêmicas</a>
                <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-outline-info">Atividades Ritualísticas</a>
            </div>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Filtros</h5>
                <div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" id="mostrar-concluidas" checked>
                    <label class="form-check-label" for="mostrar-concluidas">Mostrar atividades concluídas</label>
                </div>
            </div>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <div class="mb-3">
                        <label for="filtro-tipo" class="form-label">Tipo de Atividade</label>
                        <select id="filtro-tipo" class="form-select">
                            <option value="todas" selected>Todas</option>
                            <option value="academicas">Acadêmicas</option>
                            <option value="ritualisticas">Ritualísticas</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="mb-3">
                        <label for="filtro-turma" class="form-label">Turma</label>
                        <select id="filtro-turma" class="form-select">
                            <option value="todas" selected>Todas</option>
                            {% for turma in turmas %}
                                <option value="{{ turma.id }}">{{ turma.nome }}</option>
                            {% endfor %}
                        </select>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card">
        <div class="card-body">
            <div id="calendar"></div>
        </div>
    </div>
    
    <!-- Modal para detalhes da atividade -->
    <div class="modal fade" id="atividadeModal" tabindex="-1" aria-labelledby="atividadeModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="atividadeModalLabel">Detalhes da Atividade</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
                </div>
                <div class="modal-body" id="atividadeModalBody">
                    <div class="text-center">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Carregando...</span>
                        </div>
                        <p>Carregando detalhes da atividade...</p>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                    <a href="#" class="btn btn-primary" id="verDetalhesBtn">Ver Detalhes Completos</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/locales-all.min.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Inicializar o calendário
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
            },
            locale: 'pt-br',
            buttonText: {
                today: 'Hoje',
                month: 'Mês',
                week: 'Semana',
                day: 'Dia',
                list: 'Lista'
            },
            events: function(info, successCallback, failureCallback) {
                // Obter filtros
                const tipoFiltro = document.getElementById('filtro-tipo').value;
                const turmaFiltro = document.getElementById('filtro-turma').value;
                const mostrarConcluidas = document.getElementById('mostrar-concluidas').checked;
                
                // Construir URL com parâmetros de filtro
                let url = '{% url "atividades:api_eventos_calendario" %}';
                url += '?start=' + info.startStr + '&end=' + info.endStr;
                url += '&tipo=' + tipoFiltro;
                url += '&turma=' + turmaFiltro;
                url += '&concluidas=' + (mostrarConcluidas ? '1' : '0');
                
                // Fazer requisição AJAX
                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        successCallback(data);
                    })
                    .catch(error => {
                        console.error('Erro ao carregar eventos:', error);
                        failureCallback(error);
                    });
            },
            eventClick: function(info) {
                // Abrir modal com detalhes do evento
                const modal = new bootstrap.Modal(document.getElementById('atividadeModal'));
                const modalBody = document.getElementById('atividadeModalBody');
                const verDetalhesBtn = document.getElementById('verDetalhesBtn');
                
                // Limpar conteúdo anterior e mostrar loader
                modalBody.innerHTML = `
                    <div class="text-center">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Carregando...</span>
                        </div>
                        <p>Carregando detalhes da atividade...</p>
                    </div>
                `;
                
                // Configurar link para detalhes completos
                const eventoId = info.event.id;
                const tipoEvento = info.event.extendedProps.tipo;
                
                if (tipoEvento === 'academica') {
                    verDetalhesBtn.href = '{% url "atividades:detalhar_atividade_academica" 0 %}'.replace('0', eventoId);
                } else {
                    verDetalhesBtn.href = '{% url "atividades:detalhar_atividade_ritualistica" 0 %}'.replace('0', eventoId);
                }
                
                // Carregar detalhes do evento via AJAX
                fetch(`/atividades/api/evento/${eventoId}/?tipo=${tipoEvento}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Renderizar detalhes do evento
                            if (tipoEvento === 'academica') {
                                modalBody.innerHTML = `
                                    <div class="row">
                                        <div class="col-md-6">
                                            <p><strong>Nome:</strong> ${data.evento.nome}</p>
                                            <p><strong>Tipo:</strong> ${data.evento.tipo_display}</p>
                                            <p><strong>Status:</strong> <span class="badge ${getStatusBadgeClass(data.evento.status)}">${data.evento.status_display}</span></p>
                                            <p><strong>Responsável:</strong> ${data.evento.responsavel || 'Não informado'}</p>
                                        </div>
                                        <div class="col-md-6">
                                            <p><strong>Data de Início:</strong> ${data.evento.data_inicio}</p>
                                            <p><strong>Data de Término:</strong> ${data.evento.data_fim || 'Não definida'}</p>
                                            <p><strong>Local:</strong> ${data.evento.local || 'Não informado'}</p>
                                            <p><strong>Turma:</strong> ${data.evento.turma}</p>
                                        </div>
                                    </div>
                                    <hr>
                                    <div>
                                        <h6>Descrição:</h6>
                                        <p>${data.evento.descricao || 'Sem descrição'}</p>
                                    </div>
                                `;
                            } else {
                                modalBody.innerHTML = `
                                    <div class="row">
                                        <div class="col-md-6">
                                            <p><strong>Nome:</strong> ${data.evento.nome}</p>
                                            <p><strong>Data:</strong> ${data.evento.data}</p>
                                            <p><strong>Horário:</strong> ${data.evento.hora_inicio} - ${data.evento.hora_fim}</p>
                                            <p><strong>Local:</strong> ${data.evento.local}</p>
                                        </div>
                                        <div class="col-md-6">
                                            <p><strong>Turma:</strong> ${data.evento.turma}</p>
                                            <p><strong>Total de Participantes:</strong> ${data.evento.total_participantes}</p>
                                        </div>
                                    </div>
                                    <hr>
                                    <div>
                                        <h6>Descrição:</h6>
                                        <p>${data.evento.descricao || 'Sem descrição'}</p>
                                    </div>
                                `;
                            }
                        } else {
                            modalBody.innerHTML = `<div class="alert alert-danger">Erro ao carregar detalhes: ${data.error}</div>`;
                        }
                    })
                    .catch(error => {
                        console.error('Erro ao carregar detalhes do evento:', error);
                        modalBody.innerHTML = `<div class="alert alert-danger">Erro ao carregar detalhes do evento.</div>`;
                    });
                
                modal.show();
            },
            eventClassNames: function(arg) {
                const classes = [];
                
                // Adicionar classe baseada no tipo de atividade
                if (arg.event.extendedProps.tipo === 'academica') {
                    classes.push('academica-event');
                } else {
                    classes.push('ritualistica-event');
                }
                
                // Adicionar classe baseada no status (apenas para atividades acadêmicas)
                if (arg.event.extendedProps.status) {
                    classes.push(arg.event.extendedProps.status + '-event');
                }
                
                return classes;
            }
        });
        
        calendar.render();
        
        // Função auxiliar para obter classe CSS do badge de status
        function getStatusBadgeClass(status) {
            switch (status) {
                case 'agendada': return 'bg-warning';
                case 'em_andamento': return 'bg-info';
                case 'concluida': return 'bg-success';
                case 'cancelada': return 'bg-secondary';
                default: return 'bg-secondary';
            }
        }
        
        // Atualizar calendário quando os filtros mudarem
        document.getElementById('filtro-tipo').addEventListener('change', function() {
            calendar.refetchEvents();
        });
        
        document.getElementById('filtro-turma').addEventListener('change', function() {
            calendar.refetchEvents();
        });
        
        document.getElementById('mostrar-concluidas').addEventListener('change', function() {
            calendar.refetchEvents();
        });
    });
</script>
{% endblock %}



### Arquivo: atividades\templates\atividades\confirmar_copia_academica.html

html
{% extends 'base.html' %}

{% block title %}Copiar Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Copiar Atividade Acadêmica</h1>
    
    <div class="alert alert-info">
        <p>Você está prestes a criar uma cópia da atividade acadêmica <strong>"{{ atividade.nome }}"</strong>.</p>
        <p>A nova atividade terá os mesmos dados da original, mas com o status definido como "Agendada".</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade Original</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ atividade.nome }}</p>
            <p><strong>Descrição:</strong> {{ atividade.descricao|default:"Não informada" }}</p>
            <p><strong>Data de Início:</strong> {{ atividade.data_inicio|date:"d/m/Y H:i" }}</p>
            <p><strong>Data de Término:</strong> {{ atividade.data_fim|date:"d/m/Y H:i"|default:"Não definida" }}</p>
            <p><strong>Responsável:</strong> {{ atividade.responsavel|default:"Não informado" }}</p>
            <p><strong>Local:</strong> {{ atividade.local|default:"Não informado" }}</p>
            <p><strong>Tipo:</strong> {{ atividade.get_tipo_atividade_display }}</p>
            <p><strong>Status:</strong> {{ atividade.get_status_display }}</p>
            <p><strong>Turmas:</strong> 
                {% for turma in atividade.turmas.all %}
                    {{ turma.nome }}{% if not forloop.last %}, {% endif %}
                {% empty %}
                    Nenhuma turma associada
                {% endfor %}
            </p>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <div class="d-flex">
            <button type="submit" class="btn btn-primary me-2">Criar Cópia</button>
            <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\confirmar_copia_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}Copiar Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Copiar Atividade Ritualística</h1>
    
    <div class="alert alert-info">
        <p>Você está prestes a criar uma cópia da atividade ritualística <strong>"{{ atividade.nome }}"</strong>.</p>
        <p>A nova atividade terá os mesmos dados e participantes da original.</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade Original</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ atividade.nome }}</p>
            <p><strong>Descrição:</strong> {{ atividade.descricao|default:"Não informada" }}</p>
            <p><strong>Data:</strong> {{ atividade.data|date:"d/m/Y" }}</p>
            <p><strong>Horário:</strong> {{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</p>
            <p><strong>Local:</strong> {{ atividade.local }}</p>
            <p><strong>Turma:</strong> {{ atividade.turma }}</p>
            <p><strong>Total de Participantes:</strong> {{ atividade.participantes.count }}</p>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <div class="d-flex">
            <button type="submit" class="btn btn-primary me-2">Criar Cópia</button>
            <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\confirmar_exclusao_academica.html

html
{% extends 'base.html' %}

{% block title %}Confirmar Exclusão de Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Confirmar Exclusão</h1>
    
    <div class="alert alert-danger">
        <p>Tem certeza que deseja excluir a atividade acadêmica "{{ atividade.nome }}"?</p>
        <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ atividade.nome }}</p>
            <p><strong>Responsável:</strong> {{ atividade.responsavel|default:"Não informado" }}</p>
            <p><strong>Data de Início:</strong> {{ atividade.data_inicio|date:"d/m/Y H:i" }}</p>
            <p><strong>Data de Término:</strong> {{ atividade.data_fim|date:"d/m/Y H:i"|default:"Não definida" }}</p>
            <p><strong>Local:</strong> {{ atividade.local|default:"Não informado" }}</p>
            <p><strong>Tipo:</strong> {{ atividade.get_tipo_atividade_display }}</p>
            <p><strong>Status:</strong> {{ atividade.get_status_display }}</p>
            <p><strong>Turma:</strong> {{ atividade.turma.nome }}</p>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <!-- Adicionar um campo oculto para a URL de retorno -->
        <input type="hidden" name="return_url" value="{{ return_url }}">
        <button type="submit" class="btn btn-danger">Sim, excluir</button>
        <a href="{{ return_url }}" class="btn btn-secondary">Cancelar</a>
    </form></div>
{% endblock %}




### Arquivo: atividades\templates\atividades\confirmar_exclusao_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}Excluir Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Atividade Ritualística</h1>
    
    <div class="alert alert-danger">
        <p>Tem certeza que deseja excluir a atividade ritualística "{{ atividade.nome }}"?</p>
        <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ atividade.nome }}</p>
            <p><strong>Data:</strong> {{ atividade.data|date:"d/m/Y" }}</p>
            <p><strong>Horário:</strong> {{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</p>
            <p><strong>Local:</strong> {{ atividade.local }}</p>
            <p><strong>Turma:</strong> {{ atividade.turma }}</p>
            <p><strong>Total de Participantes:</strong> {{ atividade.participantes.count }}</p>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <input type="hidden" name="return_url" value="{{ return_url }}">
        <div class="d-flex">
            <button type="submit" class="btn btn-danger me-2">Sim, excluir</button>
            <a href="{{ return_url }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\copiar_atividade_academica.html

html
{% extends 'base.html' %}

{% block title %}Copiar Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Copiar Atividade Acadêmica</h1>
        <a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Atividade Original</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Nome:</strong> {{ atividade_original.nome }}</p>
                    <p><strong>Tipo:</strong> {{ atividade_original.get_tipo_atividade_display }}</p>
                    <p><strong>Responsável:</strong> {{ atividade_original.responsavel|default:"Não informado" }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Data de Início:</strong> {{ atividade_original.data_inicio|date:"d/m/Y" }}</p>
                    <p><strong>Data de Término:</strong> {{ atividade_original.data_fim|date:"d/m/Y"|default:"Não definida" }}</p>
                    <p><strong>Turma:</strong> {{ atividade_original.turma.nome }}</p>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <p><strong>Descrição:</strong></p>
                    <p>{{ atividade_original.descricao|default:"Sem descrição"|linebreaks }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações da Nova Atividade</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.turma %}
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
                        {% include 'includes/form_field.html' with field=form.responsavel %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.tipo_atividade %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.status %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
                <div class="form-check mt-3">
                    <input class="form-check-input" type="checkbox" id="copiar_frequencias" name="copiar_frequencias">
                    <label class="form-check-label" for="copiar_frequencias">
                        Copiar registros de frequência (se aplicável)
                    </label>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="javascript:history.back()" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Criar Cópia</button>
        </div>
    </form>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\copiar_atividade_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}Copiar Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Copiar Atividade Ritualística</h1>
        <a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Atividade Original</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Nome:</strong> {{ atividade_original.nome }}</p>
                    <p><strong>Data:</strong> {{ atividade_original.data|date:"d/m/Y" }}</p>
                    <p><strong>Horário:</strong> {{ atividade_original.hora_inicio }} - {{ atividade_original.hora_fim }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Local:</strong> {{ atividade_original.local }}</p>
                    <p><strong>Turma:</strong> {{ atividade_original.turma.nome }}</p>
                    <p><strong>Participantes:</strong> {{ atividade_original.participantes.count }}</p>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <p><strong>Descrição:</strong></p>
                    <p>{{ atividade_original.descricao|default:"Sem descrição"|linebreaks }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações da Nova Atividade</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.data %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_inicio %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_fim %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
                <div class="form-check mt-3">
                    <input class="form-check-input" type="checkbox" id="copiar_participantes" name="copiar_participantes" checked>
                    <label class="form-check-label" for="copiar_participantes">
                        Copiar lista de participantes da atividade original
                    </label>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="javascript:history.back()" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Criar Cópia</button>
        </div>
    </form>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\criar_atividade_academica.html

html
{% extends 'base.html' %}

{% block title %}Criar Nova Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Criar Nova Atividade Acadêmica</h1>
        <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">Voltar para a lista</a>
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
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=<form action="" class="nome"></form> %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.responsavel %}
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
            <div class="card-header">
                <h5>Data e Local</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_inicio %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_fim %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Classificação</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.tipo_atividade %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.status %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Criar Atividade</button>
        </div>
    </form>
</div>
{% endblock %}
<div class="d-flex justify-content-between mb-5">
    <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">Voltar para a lista</a>
    <button type="submit" class="btn btn-primary">Criar Atividade</button>
</div>



### Arquivo: atividades\templates\atividades\criar_atividade_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}Criar Nova Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Criar Nova Atividade Ritualística</h1>
        <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-secondary">Voltar para a lista</a>
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
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
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
            <div class="card-header">
                <h5>Data e Horário</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.data %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_inicio %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_fim %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Turma e Participantes</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.todos_alunos %}
                        <small class="form-text text-muted">Marque esta opção para incluir automaticamente todos os alunos da turma.</small>
                    </div>
                </div>
                
                <div class="row mt-3" id="participantes-container">
                    <div class="col-md-12">
                        <label for="{{ form.participantes.id_for_label }}">{{ form.participantes.label }}</label>
                        <div class="border p-3 rounded">
                            {{ form.participantes }}
                        </div>
                        {% if form.participantes.errors %}
                            <div class="text-danger">
                                {{ form.participantes.errors }}
                            </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Criar Atividade</button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const todosAlunosCheckbox = document.getElementById('{{ form.todos_alunos.id_for_label }}');
        const participantesContainer = document.getElementById('participantes-container');
        
        function toggleParticipantes() {
            if (todosAlunosCheckbox.checked) {
                participantesContainer.style.display = 'none';
            } else {
                participantesContainer.style.display = 'block';
            }
        }
        
        // Inicializar
        toggleParticipantes();
        
        // Adicionar listener para mudanças
        todosAlunosCheckbox.addEventListener('change', toggleParticipantes);
    });
</script>
{% endblock %}




### Arquivo: atividades\templates\atividades\dashboard.html

html
{% extends 'base.html' %}

{% block title %}Dashboard de Atividades{% endblock %}

{% block extra_css %}
<style>
    .stat-card {
        transition: transform 0.3s;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
    }
    
    .chart-container {
        position: relative;
        height: 300px;
        margin-bottom: 20px;
    }
</style>
{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Dashboard de Atividades</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'atividades:calendario_atividades' %}" class="btn btn-primary me-2">Calendário</a>
            <a href="{% url 'atividades:relatorio_atividades' %}" class="btn btn-info">Relatórios</a>
        </div>
    </div>
    
    <!-- Estatísticas Gerais -->
    <div class="row mb-4">
        <div class="col-md-4 mb-3">
            <div class="card stat-card h-100 border-primary">
                <div class="card-body text-center">
                    <h5 class="card-title">Total de Atividades</h5>
                    <p class="display-4">{{ total_academicas|add:total_ritualisticas }}</p>
                    <div class="d-flex justify-content-around mt-3">
                        <div>
                            <span class="badge bg-primary">Acadêmicas</span>
                            <h5>{{ total_academicas }}</h5>
                        </div>
                        <div>
                            <span class="badge bg-info">Ritualísticas</span>
                            <h5>{{ total_ritualisticas }}</h5>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-4 mb-3">
            <div class="card stat-card h-100 border-success">
                <div class="card-body">
                    <h5 class="card-title text-center">Atividades por Status</h5>
                    <div class="mt-3">
                        <div class="d-flex justify-content-between mb-2">
                            <span>Agendadas</span>
                            <span class="badge bg-warning">{{ academicas_por_status.agendada|default:"0" }}</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar bg-warning" role="progressbar" 
                                 style="width: {% widthratio academicas_por_status.agendada|default:0 total_academicas 100 %}%" 
                                 aria-valuenow="{{ academicas_por_status.agendada|default:0 }}" 
                                 aria-valuemin="0" aria-valuemax="{{ total_academicas }}"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-2">
                            <span>Em Andamento</span>
                            <span class="badge bg-info">{{ academicas_por_status.em_andamento|default:"0" }}</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar bg-info" role="progressbar" 
                                 style="width: {% widthratio academicas_por_status.em_andamento|default:0 total_academicas 100 %}%" 
                                 aria-valuenow="{{ academicas_por_status.em_andamento|default:0 }}" 
                                 aria-valuemin="0" aria-valuemax="{{ total_academicas }}"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-2">
                            <span>Concluídas</span>
                            <span class="badge bg-success">{{ academicas_por_status.concluida|default:"0" }}</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar bg-success" role="progressbar" 
                                 style="width: {% widthratio academicas_por_status.concluida|default:0 total_academicas 100 %}%" 
                                 aria-valuenow="{{ academicas_por_status.concluida|default:0 }}" 
                                 aria-valuemin="0" aria-valuemax="{{ total_academicas }}"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-2">
                            <span>Canceladas</span>
                            <span class="badge bg-danger">{{ academicas_por_status.cancelada|default:"0" }}</span>
                        </div>
                        <div class="progress">
                            <div class="progress-bar bg-danger" role="progressbar" 
                                 style="width: {% widthratio academicas_por_status.cancelada|default:0 total_academicas 100 %}%" 
                                 aria-valuenow="{{ academicas_por_status.cancelada|default:0 }}" 
                                 aria-valuemin="0" aria-valuemax="{{ total_academicas }}"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-4 mb-3">
            <div class="card stat-card h-100 border-info">
                <div class="card-body">
                    <h5 class="card-title text-center">Atividades por Tipo</h5>
                    <div class="mt-3">
                        <div class="d-flex justify-content-between mb-2">
                            <span>Aulas</span>
                            <span class="badge bg-primary">{{ academicas_por_tipo.aula|default:"0" }}</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar bg-primary" role="progressbar" 
                                 style="width: {% widthratio academicas_por_tipo.aula|default:0 total_academicas 100 %}%" 
                                 aria-valuenow="{{ academicas_por_tipo.aula|default:0 }}" 
                                 aria-valuemin="0" aria-valuemax="{{ total_academicas }}"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-2">
                            <span>Palestras</span>
                            <span class="badge bg-success">{{ academicas_por_tipo.palestra|default:"0" }}</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar bg-success" role="progressbar" 
                                 style="width: {% widthratio academicas_por_tipo.palestra|default:0 total_academicas 100 %}%" 
                                 aria-valuenow="{{ academicas_por_tipo.palestra|default:0 }}" 
                                 aria-valuemin="0" aria-valuemax="{{ total_academicas }}"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-2">
                            <span>Workshops</span>
                            <span class="badge bg-warning">{{ academicas_por_tipo.workshop|default:"0" }}</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar bg-warning" role="progressbar" 
                                 style="width: {% widthratio academicas_por_tipo.workshop|default:0 total_academicas 100 %}%" 
                                 aria-valuenow="{{ academicas_por_tipo.workshop|default:0 }}" 
                                 aria-valuemin="0" aria-valuemax="{{ total_academicas }}"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-2">
                            <span>Seminários</span>
                            <span class="badge bg-info">{{ academicas_por_tipo.seminario|default:"0" }}</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar bg-info" role="progressbar" 
                                 style="width: {% widthratio academicas_por_tipo.seminario|default:0 total_academicas 100 %}%" 
                                 aria-valuenow="{{ academicas_por_tipo.seminario|default:0 }}" 
                                 aria-valuemin="0" aria-valuemax="{{ total_academicas }}"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-2">
                            <span>Outros</span>
                            <span class="badge bg-secondary">{{ academicas_por_tipo.outro|default:"0" }}</span>
                        </div>
                        <div class="progress">
                            <div class="progress-bar bg-secondary" role="progressbar" 
                                 style="width: {% widthratio academicas_por_tipo.outro|default:0 total_academicas 100 %}%" 
                                 aria-valuenow="{{ academicas_por_tipo.outro|default:0 }}" 
                                 aria-valuemin="0" aria-valuemax="{{ total_academicas }}"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Gráfico de Atividades por Mês -->
    <div class="card mb-4">
        <div class="card-header">
            <h5>Atividades por Mês (Últimos 6 Meses)</h5>
        </div>
        <div class="card-body">
            <div class="chart-container">
                <canvas id="atividadesPorMesChart"></canvas>
            </div>
        </div>
    </div>
    
    <!-- Atividades Recentes -->
    <div class="row">
        <div class="col-md-6 mb-4">
            <div class="card h-100">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Atividades Acadêmicas Recentes</h5>
                </div>
                <div class="card-body">
                    <div class="list-group">
                        {% for atividade in atividades_academicas_recentes %}
                            <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="list-group-item list-group-item-action">
                                <div class="d-flex w-100 justify-content-between">
                                    <h6 class="mb-1">{{ atividade.nome }}</h6>
                                    <small>{{ atividade.data_inicio|date:"d/m/Y" }}</small>
                                </div>
                                <p class="mb-1">{{ atividade.descricao|truncatechars:100 }}</p>
                                <small>
                                    <span class="badge {% if atividade.status == 'agendada' %}bg-warning{% elif atividade.status == 'em_andamento' %}bg-info{% elif atividade.status == 'concluida' %}bg-success{% else %}bg-secondary{% endif %}">
                                        {{ atividade.get_status_display }}
                                    </span>
                                    <span class="badge bg-primary">{{ atividade.get_tipo_atividade_display }}</span>
                                </small>
                            </a>
                        {% empty %}
                            <div class="list-group-item">
                                <p class="mb-0 text-muted">Nenhuma atividade acadêmica recente.</p>
                            </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-6 mb-4">
            <div class="card h-100">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">Atividades Ritualísticas Recentes</h5>
                </div>
                <div class="card-body">
                    <div class="list-group">
                        {% for atividade in atividades_ritualisticas_recentes %}
                            <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="list-group-item list-group-item-action">
                                <div class="d-flex w-100 justify-content-between">
                                    <h6 class="mb-1">{{ atividade.nome }}</h6>
                                    <small>{{ atividade.data|date:"d/m/Y" }}</small>
                                </div>
                                <p class="mb-1">{{ atividade.descricao|truncatechars:100 }}</p>
                                <small>
                                    <span class="badge bg-info">{{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</span>
                                    <span class="badge bg-secondary">{{ atividade.local }}</span>
                                </small>
                            </a>
                        {% empty %}
                            <div class="list-group-item">
                                <p class="mb-0 text-muted">Nenhuma atividade ritualística recente.</p>
                            </div>
                        {% endfor %}
                    </div>
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
        // Dados para o gráfico de atividades por mês
        var ctx = document.getElementById('atividadesPorMesChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: {{ meses|safe }},
                datasets: [
                    {
                        label: 'Atividades Acadêmicas',
                        data: {{ dados_academicas }},
                        backgroundColor: 'rgba(13, 110, 253, 0.7)',
                        borderColor: 'rgba(13, 110, 253, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Atividades Ritualísticas',
                        data: {{ dados_ritualisticas }},
                        backgroundColor: 'rgba(23, 162, 184, 0.7)',
                        borderColor: 'rgba(23, 162, 184, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Atividades por Mês'
                    }
                }
            }
        });
    });
</script>
{% endblock %}



### Arquivo: atividades\templates\atividades\dashboard_atividades.html

html
{% extends 'base.html' %}

{% block title %}Dashboard de Atividades{% endblock %}

{% block extra_css %}
<style>
    .stat-card {
        transition: transform 0.3s;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
    }
    
    .chart-container {
        position: relative;
        height: 300px;
        margin-bottom: 20px;
    }
    
    .activity-item {
        border-left: 4px solid #dee2e6;
        padding-left: 15px;
        margin-bottom: 15px;
        position: relative;
    }
    
    .activity-item.academica {
        border-left-color: #0d6efd;
    }
    
    .activity-item.ritualistica {
        border-left-color: #17a2b8;
    }
    
    .activity-item .date {
        font-size: 0.85rem;
        color: #6c757d;
    }
    
    .activity-item .title {
        font-weight: 600;
        margin: 5px 0;
    }
    
    .activity-item .status {
        position: absolute;
        top: 0;
        right: 0;
    }
</style>
{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Dashboard de Atividades</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'atividades:calendario_atividades' %}" class="btn btn-primary me-2">Calendário</a>
            <a href="{% url 'atividades:relatorio_atividades' %}" class="btn btn-success">Relatório</a>
        </div>
    </div>
    
    <!-- Cards de estatísticas -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card stat-card bg-primary text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Total de Atividades</h5>
                    <p class="display-4">{{ total_atividades }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card stat-card bg-success text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Atividades Acadêmicas</h5>
                    <p class="display-4">{{ total_academicas }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card stat-card bg-info text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Atividades Ritualísticas</h5>
                    <p class="display-4">{{ total_ritualisticas }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card stat-card bg-warning text-dark">
                <div class="card-body text-center">
                    <h5 class="card-title">Atividades Agendadas</h5>
                    <p class="display-4">{{ total_agendadas }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Gráficos -->
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5>Atividades por Tipo</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="tipoAtividadesChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5>Atividades por Status</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="statusAtividadesChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-12">
            <div class="card">
                <div class="card-header">
                    <h5>Atividades por Mês</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="atividadesPorMesChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Próximas atividades e atividades recentes -->
    <div class="row">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5>Próximas Atividades</h5>
                </div>
                <div class="card-body">
                    {% if proximas_atividades %}
                        {% for atividade in proximas_atividades %}
                            <div class="activity-item {% if atividade.tipo == 'academica' %}academica{% else %}ritualistica{% endif %}">
                                <div class="date">
                                    {% if atividade.tipo == 'academica' %}
                                        {{ atividade.data_inicio|date:"d/m/Y" }}
                                    {% else %}
                                        {{ atividade.data|date:"d/m/Y" }} ({{ atividade.hora_inicio }} - {{ atividade.hora_fim }})
                                    {% endif %}
                                </div>
                                <div class="title">{{ atividade.nome }}</div>
                                <div class="details">
                                    {% if atividade.tipo == 'academica' %}
                                        <span class="badge bg-primary">Acadêmica</span>
                                        <span class="badge {% if atividade.status == 'agendada' %}bg-warning{% elif atividade.status == 'em_andamento' %}bg-info{% elif atividade.status == 'concluida' %}bg-success{% else %}bg-secondary{% endif %}">
                                            {{ atividade.get_status_display }}
                                        </span>
                                    {% else %}
                                        <span class="badge bg-info">Ritualística</span>
                                    {% endif %}
                                </div>
                                <div class="mt-2">
                                    {% if atividade.tipo == 'academica' %}
                                        <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-sm btn-outline-primary">Ver Detalhes</a>
                                    {% else %}
                                        <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-sm btn-outline-info">Ver Detalhes</a>
                                    {% endif %}
                                </div>
                            </div>
                        {% endfor %}
                    {% else %}
                        <p class="text-muted">Não há atividades agendadas para os próximos dias.</p>
                    {% endif %}
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5>Atividades Recentes</h5>
                </div>
                <div class="card-body">
                    {% if atividades_recentes %}
                        {% for atividade in atividades_recentes %}
                            <div class="activity-item {% if atividade.tipo == 'academica' %}academica{% else %}ritualistica{% endif %}">
                                <div class="date">
                                    {% if atividade.tipo == 'academica' %}
                                        {{ atividade.data_inicio|date:"d/m/Y" }}
                                    {% else %}
                                        {{ atividade.data|date:"d/m/Y" }} ({{ atividade.hora_inicio }} - {{ atividade.hora_fim }})
                                    {% endif %}
                                </div>
                                <div class="title">{{ atividade.nome }}</div>
                                <div class="details">
                                    {% if atividade.tipo == 'academica' %}
                                        <span class="badge bg-primary">Acadêmica</span>
                                        <span class="badge {% if atividade.status == 'agendada' %}bg-warning{% elif atividade.status == 'em_andamento' %}bg-info{% elif atividade.status == 'concluida' %}bg-success{% else %}bg-secondary{% endif %}">
                                            {{ atividade.get_status_display }}
                                        </span>
                                    {% else %}
                                        <span class="badge bg-info">Ritualística</span>
                                    {% endif %}
                                </div>
                                <div class="mt-2">
                                    {% if atividade.tipo == 'academica' %}
                                        <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-sm btn-outline-primary">Ver Detalhes</a>
                                    {% else %}
                                        <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-sm btn-outline-info">Ver Detalhes</a>
                                    {% endif %}
                                </div>
                            </div>
                        {% endfor %}
                    {% else %}
                        <p class="text-muted">Não há atividades recentes.</p>
                    {% endif %}
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
        // Gráfico de atividades por tipo
        var tipoCtx = document.getElementById('tipoAtividadesChart').getContext('2d');
        var tipoChart = new Chart(tipoCtx, {
            type: 'pie',
            data: {
                labels: ['Acadêmicas', 'Ritualísticas'],
                datasets: [{
                    data: [{{ total_academicas }}, {{ total_ritualisticas }}],
                    backgroundColor: [
                        'rgba(13, 110, 253, 0.8)',
                        'rgba(23, 162, 184, 0.8)'
                    ],
                    borderColor: [
                        'rgba(13, 110, 253, 1)',
                        'rgba(23, 162, 184, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Distribuição por Tipo de Atividade'
                    }
                }
            }
        });
        
        // Gráfico de atividades por status
        var statusCtx = document.getElementById('statusAtividadesChart').getContext('2d');
        var statusChart = new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: ['Agendadas', 'Em Andamento', 'Concluídas', 'Canceladas'],
                datasets: [{
                    data: [
                        {{ status_counts.agendada|default:0 }}, 
                        {{ status_counts.em_andamento|default:0 }}, 
                        {{ status_counts.concluida|default:0 }}, 
                        {{ status_counts.cancelada|default:0 }}
                    ],
                    backgroundColor: [
                        'rgba(255, 193, 7, 0.8)',
                        'rgba(13, 202, 240, 0.8)',
                        'rgba(25, 135, 84, 0.8)',
                        'rgba(220, 53, 69, 0.8)'
                    ],
                    borderColor: [
                        'rgba(255, 193, 7, 1)',
                        'rgba(13, 202, 240, 1)',
                        'rgba(25, 135, 84, 1)',
                        'rgba(220, 53, 69, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Distribuição por Status'
                    }
                }
            }
        });
        
        // Gráfico de atividades por mês
        var mesCtx = document.getElementById('atividadesPorMesChart').getContext('2d');
        var mesChart = new Chart(mesCtx, {
            type: 'bar',
            data: {
                labels: {{ meses|safe }},
                datasets: [
                    {
                        label: 'Atividades Acadêmicas',
                        data: {{ academicas_por_mes|safe }},
                        backgroundColor: 'rgba(13, 110, 253, 0.5)',
                        borderColor: 'rgba(13, 110, 253, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Atividades Ritualísticas',
                        data: {{ ritualisticas_por_mes|safe }},
                        backgroundColor: 'rgba(23, 162, 184, 0.5)',
                        borderColor: 'rgba(23, 162, 184, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Atividades por Mês'
                    }
                }
            }
        });
    });
</script>
{% endblock %}



### Arquivo: atividades\templates\atividades\detalhar_atividade_academica.html

html
{% extends 'base.html' %}

{% block title %}Detalhes da Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Detalhes da Atividade Acadêmica</h1>
    
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">{{ atividade.nome }}</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Descrição:</strong> {{ atividade.descricao|default:"Não informada" }}</p>
                    <p><strong>Data de Início:</strong> {{ atividade.data_inicio|date:"d/m/Y H:i" }}</p>
                    <p><strong>Data de Término:</strong> {{ atividade.data_fim|date:"d/m/Y H:i"|default:"Não definida" }}</p>
                    <p><strong>Responsável:</strong> {{ atividade.responsavel|default:"Não informado" }}</p>
                    <p><strong>Local:</strong> {{ atividade.local|default:"Não informado" }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Tipo:</strong> {{ atividade.get_tipo_atividade_display }}</p>
                    <p><strong>Status:</strong> {{ atividade.get_status_display }}</p>
                    
                    <!-- Mostrar todas as turmas associadas -->
                    <p><strong>Turmas:</strong></p>
                    <ul class="list-group">
                        {% for turma in atividade.turmas.all %}
                            <li class="list-group-item">
                                <a href="{% url 'turmas:detalhar_turma' turma.id %}">{{ turma.nome }}</a>
                                {% if turma.curso %}
                                    - {{ turma.curso.nome }}
                                {% endif %}
                            </li>
                        {% empty %}
                            <li class="list-group-item">Nenhuma turma associada</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
            
            <div class="mt-3">
                <a href="{% url 'atividades:editar_atividade_academica' atividade.pk %}?return_url={{ request.path|urlencode }}" class="btn btn-primary">Editar</a>
                <a href="{% url 'atividades:confirmar_exclusao_academica' atividade.pk %}?return_url={{ request.path|urlencode }}" class="btn btn-danger">Excluir</a>
                <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">Voltar para Lista</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: atividades\templates\atividades\detalhar_atividade_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}Detalhes da Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{{ atividade.nome }}</h1>
        <div>
            <a href="{{ return_url }}" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-secondary me-2">Lista de Atividades</a>
            <a href="{% url 'atividades:editar_atividade_ritualistica' atividade.id %}?return_url={{ request.path|urlencode }}" class="btn btn-warning me-2">Editar</a>
            <a href="{% url 'atividades:confirmar_exclusao_ritualistica' atividade.id %}?return_url={{ request.path|urlencode }}" class="btn btn-danger">Excluir</a>
        </div>
    </div>    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="row">
        <div class="col-md-8">
            <div class="card mb-4">
                <div class="card-header">
                    <h5>Informações Básicas</h5>
                </div>
                <div class="card-body">
                    <p><strong>Descrição:</strong> {{ atividade.descricao|default:"Não informada" }}</p>
                    <p><strong>Data:</strong> {{ atividade.data|date:"d/m/Y" }}</p>
                    <p><strong>Horário:</strong> {{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</p>
                    <p><strong>Local:</strong> {{ atividade.local }}</p>
                    <p><strong>Turma:</strong> {{ atividade.turma }}</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="card mb-4">
                <div class="card-header">
                    <h5>Estatísticas</h5>
                </div>
                <div class="card-body">
                    <p><strong>Total de Participantes:</strong> {{ total_participantes }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Participantes</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>Número Iniciático</th>
                            <th>Email</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for aluno in atividade.participantes.all %}
                            <tr>
                                <td>{{ aluno.nome }}</td>
                                <td>{{ aluno.numero_iniciatico|default:"N/A" }}</td>
                                <td>{{ aluno.email }}</td>
                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="3" class="text-center">
                                    <p class="my-3">Nenhum participante cadastrado para esta atividade.</p>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: atividades\templates\atividades\editar_atividade_academica.html

html
{% extends 'base.html' %}

{% block title %}Editar Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Editar Atividade Acadêmica</h1>
        <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-secondary">Voltar para detalhes</a>
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
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.responsavel %}
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
            <div class="card-header">
                <h5>Data e Local</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_inicio %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_fim %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Classificação</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.tipo_atividade %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.status %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Atualizar Atividade</button>
        </div>
    </form>
</div>
{% endblock %}




### Arquivo: atividades\templates\atividades\editar_atividade_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}Editar Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Editar Atividade Ritualística</h1>
        <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-secondary">Voltar para detalhes</a>
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
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
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
            <div class="card-header">
                <h5>Data e Horário</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.data %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_inicio %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_fim %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Turma e Participantes</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.todos_alunos %}
                        <small class="form-text text-muted">Marque esta opção para incluir automaticamente todos os alunos da turma.</small>
                    </div>
                </div>
                
                <div class="row mt-3" id="participantes-container">
                    <div class="col-md-12">
                        <label for="{{ form.participantes.id_for_label }}">{{ form.participantes.label }}</label>
                        <div class="border p-3 rounded">
                            {{ form.participantes }}
                        </div>
                        {% if form.participantes.errors %}
                            <div class="text-danger">
                                {{ form.participantes.errors }}
                            </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Atualizar Atividade</button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const todosAlunosCheckbox = document.getElementById('{{ form.todos_alunos.id_for_label }}');
        const participantesContainer = document.getElementById('participantes-container');
        
        function toggleParticipantes() {
            if (todosAlunosCheckbox.checked) {
                participantesContainer.style.display = 'none';
            } else {
                participantesContainer.style.display = 'block';
            }
        }
        
        // Inicializar
        toggleParticipantes();
        
        // Adicionar listener para mudanças
        todosAlunosCheckbox.addEventListener('change', toggleParticipantes);
    });
</script>
{% endblock %}




### Arquivo: atividades\templates\atividades\excluir_atividade_academica.html

html
{% extends 'base.html' %}

{% block title %}Excluir Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Atividade Acadêmica</h1>
    
    <div class="alert alert-danger">
        <p>Tem certeza que deseja excluir a atividade acadêmica "{{ atividade.nome }}"?</p>
        <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ atividade.nome }}</p>
            <p><strong>Responsável:</strong> {{ atividade.responsavel|default:"Não informado" }}</p>
            <p><strong>Data de Início:</strong> {{ atividade.data_inicio|date:"d/m/Y H:i" }}</p>
            <p><strong>Data de Término:</strong> {{ atividade.data_fim|date:"d/m/Y H:i"|default:"Não definida" }}</p>
            <p><strong>Local:</strong> {{ atividade.local|default:"Não informado" }}</p>
            <p><strong>Tipo:</strong> {{ atividade.get_tipo_atividade_display }}</p>
            <p><strong>Status:</strong> {{ atividade.get_status_display }}</p>
            <p><strong>Turma:</strong> {{ atividade.turma }}</p>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <div class="d-flex">
            <button type="submit" class="btn btn-danger me-2">Sim, excluir</button>
            <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}




### Arquivo: atividades\templates\atividades\excluir_atividade_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}Excluir Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Atividade Ritualística</h1>
    
    <div class="alert alert-danger">
        <p>Tem certeza que deseja excluir a atividade ritualística "{{ atividade.nome }}"?</p>
        <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ atividade.nome }}</p>
            <p><strong>Data:</strong> {{ atividade.data|date:"d/m/Y" }}</p>
            <p><strong>Horário:</strong> {{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</p>
            <p><strong>Local:</strong> {{ atividade.local }}</p>
            <p><strong>Turma:</strong> {{ atividade.turma }}</p>
            <p><strong>Total de Participantes:</strong> {{ atividade.participantes.count }}</p>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <div class="d-flex">
            <button type="submit" class="btn btn-danger me-2">Sim, excluir</button>
            <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}




### Arquivo: atividades\templates\atividades\formulario_atividade_academica.html

html
{% extends 'base.html' %}
{% block title %}{% if form.instance.pk %}Editar{% else %}Nova{% endif %} Atividade Acadêmica{% endblock %}
{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{% if form.instance.pk %}Editar{% else %}Nova{% endif %} Atividade Acadêmica</h1>
        <a href="{{ return_url }}" class="btn btn-secondary me-2">Voltar</a>
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
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.responsavel %}
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
            <div class="card-header">
                <h5>Data e Local</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_inicio %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_fim %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Nova seção para Turmas -->
        <div class="card mb-4">
            <div class="card-header">
                <h5>Turmas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.turmas %}
                    </div>
                </div>
                <div class="row mt-2">
                    <div class="col-md-12">
                        <div class="form-check">
                            {{ form.todas_turmas }}
                            <label class="form-check-label" for="{{ form.todas_turmas.id_for_label }}">
                                {{ form.todas_turmas.label }}
                            </label>
                            <small class="form-text text-muted">
                                Marque esta opção para aplicar esta atividade a todas as turmas ativas automaticamente.
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Classificação</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.tipo_atividade %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.status %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <!-- Use a URL de retorno fornecida pela view -->
            <a href="{{ return_url }}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">
                {% if atividade %}Atualizar{% else %}Criar{% endif %} Atividade
            </button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const todasTurmasCheckbox = document.getElementById('{{ form.todas_turmas.id_for_label }}');
        const turmasSelect = document.getElementById('{{ form.turmas.id_for_label }}');
        
        function toggleTurmasField() {
            if (todasTurmasCheckbox.checked) {
                turmasSelect.disabled = true;
                // Adicionar uma mensagem informativa
                if (!document.getElementById('turmas-info')) {
                    const infoDiv = document.createElement('div');
                    infoDiv.id = 'turmas-info';
                    infoDiv.className = 'alert alert-info mt-2';
                    infoDiv.textContent = 'Todas as turmas ativas serão incluídas automaticamente.';
                    turmasSelect.parentNode.appendChild(infoDiv);
                }
            } else {
                turmasSelect.disabled = false;
                // Remover a mensagem informativa se existir
                const infoDiv = document.getElementById('turmas-info');
                if (infoDiv) {
                    infoDiv.remove();
                }
            }
        }
        
        // Inicializar
        toggleTurmasField();
        
        // Adicionar listener para mudanças
        todasTurmasCheckbox.addEventListener('change', toggleTurmasField);
        
        // Inicializar Select2 para o campo de turmas
        if (typeof $.fn.select2 === 'function') {
            $(turmasSelect).select2({
                theme: 'bootstrap4',
                placeholder: 'Selecione as turmas',
                allowClear: true,
                width: '100%'
            });
        }
    });
</script>
{% endblock %}




### Arquivo: atividades\templates\atividades\formulario_atividade_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}{% if atividade %}Editar{% else %}Nova{% endif %} Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{% if atividade %}Editar{% else %}Nova{% endif %} Atividade Ritualística</h1>
        <a href="{{ return_url }}" class="btn btn-secondary">Voltar para a lista</a>
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
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
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
            <div class="card-header">
                <h5>Data e Horário</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.data %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_inicio %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_fim %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Turma e Participantes</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.participantes %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{{ return_url }}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">
                {% if atividade %}Atualizar{% else %}Criar{% endif %} Atividade
            </button>
        </div>
    </form>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\index.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Atividades - OMAUM{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Atividades</h1>
        <a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>
    </div>
    
    <div class="row">
        <div class="col-md-6 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">Atividades Acadêmicas</h5>
                    <p class="card-text">Gerenciamento de atividades relacionadas ao ensino e aprendizagem.</p>
                    <p class="card-text text-muted">Aulas, workshops, palestras, seminários e outras atividades educacionais.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-primary">Gerenciar Atividades Acadêmicas</a>
                </div>
            </div>
        </div>
        
        <div class="col-md-6 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">Atividades Ritualísticas</h5>
                    <p class="card-text">Gerenciamento de atividades relacionadas a rituais e cerimônias.</p>
                    <p class="card-text text-muted">Cerimônias, rituais, meditações coletivas e outras práticas espirituais.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-primary">Gerenciar Atividades Ritualísticas</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: atividades\templates\atividades\listar_atividades.html

html
{% extends 'base.html' %}
{% load static %}

{% block title %}Atividades - OMAUM{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Atividades</h1>
        <a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>
    </div>
    
    <div class="row">
        <div class="col-md-6 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">Atividades Acadêmicas</h5>
                    <p class="card-text">Gerenciamento de atividades relacionadas ao ensino e aprendizagem.</p>
                    <p class="card-text text-muted">Aulas, workshops, palestras, seminários e outras atividades educacionais.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-primary">Gerenciar Atividades Acadêmicas</a>
                </div>
            </div>
        </div>
        
        <div class="col-md-6 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">Atividades Ritualísticas</h5>
                    <p class="card-text">Gerenciamento de atividades relacionadas a rituais e cerimônias.</p>
                    <p class="card-text text-muted">Cerimônias, rituais, meditações coletivas e outras práticas espirituais.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-primary">Gerenciar Atividades Ritualísticas</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\listar_atividades_academicas.html

html
{% extends 'base.html' %}

{% block title %}Lista de Atividades Acadêmicas{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Cabeçalho com título e botões na mesma linha -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Lista de Atividades Acadêmicas</h1>
        <div>
            <a href="{% url 'core:pagina_inicial' %}" class="btn btn-secondary me-2">Página Inicial</a>
            
            <!-- Botão para criar nova atividade acadêmica com URL de retorno -->
            <a href="{% url 'atividades:criar_atividade_academica' %}?return_url={{ request.path|urlencode }}" class="btn btn-primary">
                Nova Atividade Acadêmica
            </a>
        </div>
    </div>    
    <!-- Barra de busca e filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <form method="get" class="row g-3">
                <div class="col-md-6">
                    <input type="text" name="q" class="form-control" placeholder="Buscar por título, descrição ou responsável..." value="{{ query }}">
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn btn-primary w-100">Filtrar</button>
                </div>
            </form>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Título</th>
                            <th>Responsável</th>
                            <th>Data de Início</th>
                            <th>Status</th>
                            <th>Turmas</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for atividade in atividades %}
                            <tr>
                                <td>{{ atividade.nome }}</td>
                                <td>{{ atividade.responsavel|default:"Não informado" }}</td>
                                <td>{{ atividade.data_inicio|date:"d/m/Y" }}</td>
                                <td>
                                    <span class="badge {% if atividade.status == 'agendada' %}bg-warning{% elif atividade.status == 'em_andamento' %}bg-info{% elif atividade.status == 'concluida' %}bg-success{% else %}bg-secondary{% endif %}">
                                        {{ atividade.get_status_display }}
                                    </span>
                                </td>
                                <td>
                                    {% if atividade.turmas.count > 3 %}
                                        {{ atividade.turmas.count }} turmas
                                    {% else %}
                                        {% for turma in atividade.turmas.all %}
                                            {{ turma.nome }}{% if not forloop.last %}, {% endif %}
                                        {% empty %}
                                            Nenhuma turma
                                        {% endfor %}
                                    {% endif %}
                                </td>
                                <td>
                                    <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-sm btn-info" title="Ver detalhes completos da atividade">Detalhes</a>
                                    <a href="{% url 'atividades:editar_atividade_academica' atividade.id %}" class="btn btn-sm btn-warning" title="Editar informações da atividade">Editar</a>
                                    <a href="{% url 'atividades:excluir_atividade_academica' atividade.id %}" class="btn btn-sm btn-danger" title="Excluir esta atividade">Excluir</a>
                                </td>
                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="5" class="text-center">
                                    <p class="my-3">Nenhuma atividade acadêmica cadastrada.</p>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer">
            <p class="text-muted mb-0">Total: {{ atividades.count|default:"0" }} atividade(s)</p>
            {% if page_obj.has_other_pages %}
                <nav aria-label="Paginação">
                    <ul class="pagination justify-content-center mb-0">
                        {% if page_obj.has_previous %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.previous_page_number }}&q={{ query }}">Anterior</a>
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
                                    <a class="page-link" href="?page={{ num }}&q={{ query }}">{{ num }}</a>
                                </li>
                            {% endif %}
                        {% endfor %}

                        {% if page_obj.has_next %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.next_page_number }}&q={{ query }}">Próxima</a>
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




### Arquivo: atividades\templates\atividades\listar_atividades_ritualisticas.html

html
{% extends 'base.html' %}

{% block title %}Lista de Atividades Ritualísticas{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Cabeçalho com título e botões na mesma linha -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Lista de Atividades Ritualísticas</h1>
        <div>
            <a href="{% url 'core:pagina_inicial' %}" class="btn btn-secondary me-2">Página Inicial</a>
            <!-- Botão para criar nova atividade ritualística -->
            <a href="{% url 'atividades:criar_atividade_ritualistica' %}?return_url={{ request.path|urlencode }}" class="btn btn-primary">
                Nova Atividade Ritualística
            </a>
        </div>
    </div>    
    <!-- Barra de busca e filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <form method="get" class="row g-3">
                <div class="col-md-6">
                    <input type="text" name="q" class="form-control" placeholder="Buscar por nome, descrição ou local..." value="{{ query }}">
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn btn-primary w-100">Filtrar</button>
                </div>
            </form>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>Data</th>
                            <th>Horário</th>
                            <th>Local</th>
                            <th>Turma</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for atividade in atividades %}
                            <tr>
                                <td>{{ atividade.nome }}</td>
                                <td>{{ atividade.data|date:"d/m/Y" }}</td>
                                <td>{{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</td>
                                <td>{{ atividade.local }}</td>
                                <td>{{ atividade.turma }}</td>
                                <td>
                                    <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-sm btn-info" title="Ver detalhes completos da atividade">Detalhes</a>
                                    <a href="{% url 'atividades:editar_atividade_ritualistica' atividade.id %}" class="btn btn-sm btn-warning" title="Editar informações da atividade">Editar</a>
                                    <a href="{% url 'atividades:excluir_atividade_ritualistica' atividade.id %}" class="btn btn-sm btn-danger" title="Excluir esta atividade">Excluir</a>
                                </td>
                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="6" class="text-center">
                                    <p class="my-3">Nenhuma atividade ritualística cadastrada.</p>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer">
            <p class="text-muted mb-0">Total: {{ atividades.count|default:"0" }} atividade(s)</p>
            {% if page_obj.has_other_pages %}
                <nav aria-label="Paginação">
                    <ul class="pagination justify-content-center mb-0">
                        {% if page_obj.has_previous %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.previous_page_number }}&q={{ query }}">Anterior</a>
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
                                    <a class="page-link" href="?page={{ num }}&q={{ query }}">{{ num }}</a>
                                </li>
                            {% endif %}
                        {% endfor %}

                        {% if page_obj.has_next %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.next_page_number }}&q={{ query }}">Próxima</a>
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




### Arquivo: atividades\templates\atividades\registrar_frequencia.html

html
{% extends 'base.html' %}

{% block title %}Registrar Frequência - {{ atividade.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Registrar Frequência</h1>
        <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-secondary">Voltar</a>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Nome:</strong> {{ atividade.nome }}</p>
                    <p><strong>Tipo:</strong> {{ atividade.get_tipo_atividade_display }}</p>
                    <p><strong>Status:</strong> {{ atividade.get_status_display }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Data de Início:</strong> {{ atividade.data_inicio|date:"d/m/Y" }}</p>
                    <p><strong>Data de Término:</strong> {{ atividade.data_fim|date:"d/m/Y"|default:"Não definida" }}</p>
                    <p><strong>Responsável:</strong> {{ atividade.responsavel|default:"Não informado" }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        
        <div class="card mb-4">
            <div class="card-header">
                <div class="d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">Lista de Presença</h5>
                    <div>
                        <div class="form-group mb-0">
                            <label for="data" class="me-2">Data:</label>
                            <input type="date" id="data" name="data" class="form-control d-inline-block" style="width: auto;" value="{{ data_hoje }}" required>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card-body">
                {% if alunos %}
                    <div class="mb-3">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="marcar-todos" checked>
                            <label class="form-check-label" for="marcar-todos">
                                Marcar/Desmarcar Todos
                            </label>
                        </div>
                    </div>
                    
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th style="width: 50px;">#</th>
                                    <th>Aluno</th>
                                    <th style="width: 120px;">Presente</th>
                                    <th>Justificativa (se ausente)</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for aluno in alunos %}
                                <tr>
                                    <td>{{ forloop.counter }}</td>
                                    <td>
                                        <div class="d-flex align-items-center">
                                            {% if aluno.foto %}
                                                <img src="{{ aluno.foto.url }}" alt="Foto de {{ aluno.nome }}" 
                                                     class="rounded-circle me-2" width="30" height="30" 
                                                     style="object-fit: cover;">
                                            {% else %}
                                                <div class="rounded-circle bg-secondary me-2 d-flex align-items-center justify-content-center" 
                                                     style="width: 30px; height: 30px; color: white;">
                                                    {{ aluno.nome|first|upper }}
                                                </div>
                                            {% endif %}
                                            <div>
                                                <div>{{ aluno.nome }}</div>
                                                <small class="text-muted">{{ aluno.numero_iniciatico|default:"Sem número iniciático" }}</small>
                                            </div>
                                        </div>
                                    </td>
                                    <td>
                                        <div class="form-check">
                                            <input class="form-check-input presenca-checkbox" type="checkbox" name="presentes" value="{{ aluno.cpf }}" id="presente_{{ aluno.cpf }}" checked>
                                            <label class="form-check-label" for="presente_{{ aluno.cpf }}">
                                                Presente
                                            </label>
                                        </div>
                                    </td>
                                    <td>
                                        <textarea class="form-control justificativa-field" name="justificativa_{{ aluno.cpf }}" rows="1" placeholder="Justificativa para ausência" disabled></textarea>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                {% else %}
                    <div class="alert alert-warning">
                        <p>Não há alunos matriculados nas turmas associadas a esta atividade.</p>
                    </div>
                {% endif %}
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-secondary">Cancelar</a>
            {% if alunos %}
                <button type="submit" class="btn btn-primary">Registrar Frequência</button>
            {% endif %}
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Função para alternar o estado de habilitação do campo de justificativa
        function toggleJustificativa(checkbox) {
            const row = checkbox.closest('tr');
            const justificativa = row.querySelector('.justificativa-field');
            
            if (checkbox.checked) {
                justificativa.disabled = true;
                justificativa.value = '';
            } else {
                justificativa.disabled = false;
            }
        }
        
        // Adicionar evento para cada checkbox de presença
        const checkboxes = document.querySelectorAll('.presenca-checkbox');
        checkboxes.forEach(function(checkbox) {
            checkbox.addEventListener('change', function() {
                toggleJustificativa(this);
            });
            
            // Inicializar o estado
            toggleJustificativa(checkbox);
        });
        
        // Marcar/Desmarcar todos
        const marcarTodos = document.getElementById('marcar-todos');
        marcarTodos.addEventListener('change', function() {
            checkboxes.forEach(function(checkbox) {
                checkbox.checked = marcarTodos.checked;
                toggleJustificativa(checkbox);
            });
        });
    });
</script>
{% endblock %}



### Arquivo: atividades\templates\atividades\relatorio_atividades.html

html
{% extends 'base.html' %}

{% block title %}Relatório de Atividades{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Relatório de Atividades</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'atividades:dashboard_atividades' %}" class="btn btn-primary">Dashboard</a>
        </div>
    </div>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-3">
                    <label for="tipo" class="form-label">Tipo de Atividade</label>
                    <select name="tipo" id="tipo" class="form-select">
                        <option value="todas" {% if tipo == 'todas' %}selected{% endif %}>Todas</option>
                        <option value="academicas" {% if tipo == 'academicas' %}selected{% endif %}>Acadêmicas</option>
                        <option value="ritualisticas" {% if tipo == 'ritualisticas' %}selected{% endif %}>Ritualísticas</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="status" class="form-label">Status</label>
                    <select name="status" id="status" class="form-select">
                        <option value="">Todos</option>
                        <option value="agendada" {% if status == 'agendada' %}selected{% endif %}>Agendada</option>
                        <option value="em_andamento" {% if status == 'em_andamento' %}selected{% endif %}>Em Andamento</option>
                        <option value="concluida" {% if status == 'concluida' %}selected{% endif %}>Concluída</option>
                        <option value="cancelada" {% if status == 'cancelada' %}selected{% endif %}>Cancelada</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="data_inicio" class="form-label">Data Início</label>
                    <input type="date" name="data_inicio" id="data_inicio" class="form-control" value="{{ data_inicio }}">
                </div>
                <div class="col-md-3">
                    <label for="data_fim" class="form-label">Data Fim</label>
                    <input type="date" name="data_fim" id="data_fim" class="form-control" value="{{ data_fim }}">
                </div>
                <div class="col-md-12 d-flex justify-content-end">
                    <button type="submit" class="btn btn-primary me-2">Filtrar</button>
                    <a href="{% url 'atividades:relatorio_atividades' %}" class="btn btn-secondary">Limpar Filtros</a>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Botões de exportação -->
    <div class="mb-4">
        <a href="{% url 'atividades:exportar_atividades' 'pdf' %}?{{ request.GET.urlencode }}" class="btn btn-danger me-2">
            <i class="fas fa-file-pdf"></i> Exportar PDF
        </a>
        <a href="{% url 'atividades:exportar_atividades' 'excel' %}?{{ request.GET.urlencode }}" class="btn btn-success me-2">
            <i class="fas fa-file-excel"></i> Exportar Excel
        </a>
        <a href="{% url 'atividades:exportar_atividades' 'csv' %}?{{ request.GET.urlencode }}" class="btn btn-info">
            <i class="fas fa-file-csv"></i> Exportar CSV
        </a>
    </div>
    
    <!-- Resumo -->
    <div class="row mb-4">
        <div class="col-md-4">
            <div class="card bg-light">
                <div class="card-body text-center">
                    <h5 class="card-title">Total de Atividades</h5>
                    <p class="display-4">{{ total_atividades }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card bg-primary text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Atividades Acadêmicas</h5>
                    <p class="display-4">{{ total_academicas }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card bg-info text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Atividades Ritualísticas</h5>
                    <p class="display-4">{{ total_ritualisticas }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Tabela de resultados -->
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">Resultados</h5>
        </div>
        <div class="card-body">
            <ul class="nav nav-tabs mb-3" id="myTab" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="academicas-tab" data-bs-toggle="tab" data-bs-target="#academicas" type="button" role="tab" aria-controls="academicas" aria-selected="true">
                        Atividades Acadêmicas
                    </button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="ritualisticas-tab" data-bs-toggle="tab" data-bs-target="#ritualisticas" type="button" role="tab" aria-controls="ritualisticas" aria-selected="false">
                        Atividades Ritualísticas
                    </button>
                </li>
            </ul>
            <div class="tab-content" id="myTabContent">
                <!-- Atividades Acadêmicas -->
                <div class="tab-pane fade show active" id="academicas" role="tabpanel" aria-labelledby="academicas-tab">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Nome</th>
                                    <th>Tipo</th>
                                    <th>Data de Início</th>
                                    <th>Status</th>
                                    <th>Responsável</th>
                                    <th>Turmas</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for atividade in atividades_academicas %}
                                <tr>
                                    <td>
                                        <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}">
                                            {{ atividade.nome }}
                                        </a>
                                    </td>
                                    <td>{{ atividade.get_tipo_atividade_display }}</td>
                                    <td>{{ atividade.data_inicio|date:"d/m/Y" }}</td>
                                    <td>
                                        <span class="badge {% if atividade.status == 'agendada' %}bg-warning{% elif atividade.status == 'em_andamento' %}bg-info{% elif atividade.status == 'concluida' %}bg-success{% else %}bg-secondary{% endif %}">
                                            {{ atividade.get_status_display }}
                                        </span>
                                    </td>
                                    <td>{{ atividade.responsavel|default:"Não informado" }}</td>
                                    <td>
                                        {% for turma in atividade.turmas.all %}
                                            <span class="badge bg-primary">{{ turma.nome }}</span>
                                        {% empty %}
                                            <span class="text-muted">Nenhuma turma</span>
                                        {% endfor %}
                                    </td>
                                </tr>
                                {% empty %}
                                <tr>
                                    <td colspan="6" class="text-center">Nenhuma atividade acadêmica encontrada.</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <!-- Atividades Ritualísticas -->
                <div class="tab-pane fade" id="ritualisticas" role="tabpanel" aria-labelledby="ritualisticas-tab">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Nome</th>
                                    <th>Data</th>
                                    <th>Horário</th>
                                    <th>Local</th>
                                    <th>Turma</th>
                                    <th>Participantes</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for atividade in atividades_ritualisticas %}
                                <tr>
                                    <td>
                                        <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}">
                                            {{ atividade.nome }}
                                        </a>
                                    </td>
                                    <td>{{ atividade.data|date:"d/m/Y" }}</td>
                                    <td>{{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</td>
                                    <td>{{ atividade.local }}</td>
                                    <td>{{ atividade.turma.nome }}</td>
                                    <td>{{ atividade.participantes.count }}</td>
                                </tr>
                                {% empty %}
                                <tr>
                                    <td colspan="6" class="text-center">Nenhuma atividade ritualística encontrada.</td>
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



### Arquivo: atividades\templates\atividades\visualizar_frequencia.html

html
{% extends 'base.html' %}

{% block title %}Frequência - {{ atividade.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Frequência: {{ atividade.nome }}</h1>
        <div>
            <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'atividades:registrar_frequencia_atividade' atividade.id %}" class="btn btn-primary">Registrar Nova Frequência</a>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Selecionar Data</h5>
                <div>
                    <form method="get" class="d-flex align-items-center">
                        <label for="data" class="me-2">Data:</label>
                        <select name="data" id="data" class="form-select" style="width: auto;" onchange="this.form.submit()">
                            <option value="">Selecione uma data</option>
                            {% for data in datas_disponiveis %}
                                <option value="{{ data|date:'Y-m-d' }}" {% if data|date:'Y-m-d' == data_selecionada|date:'Y-m-d' %}selected{% endif %}>
                                    {{ data|date:"d/m/Y" }}
                                </option>
                            {% endfor %}
                        </select>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
    {% if data_selecionada %}
        <!-- Estatísticas -->
        <div class="row mb-4">
            <div class="col-md-4">
                <div class="card text-white bg-primary">
                    <div class="card-body text-center">
                        <h5 class="card-title">Total de Alunos</h5>
                        <p class="display-4">{{ total_registros }}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card text-white bg-success">
                    <div class="card-body text-center">
                        <h5 class="card-title">Presentes</h5>
                        <p class="display-4">{{ presentes }}</p>
                        <p>{{ taxa_presenca|floatformat:1 }}%</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card text-white bg-danger">
                    <div class="card-body text-center">
                        <h5 class="card-title">Ausentes</h5>
                        <p class="display-4">{{ ausentes }}</p>
                        <p>{{ 100|subtract:taxa_presenca|floatformat:1 }}%</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Gráfico -->
        <div class="card mb-4">
            <div class="card-header">
                <h5>Gráfico de Frequência</h5>
            </div>
            <div class="card-body">
                <canvas id="frequenciaChart" height="200"></canvas>
            </div>
        </div>
        
        <!-- Lista de Alunos -->
        <div class="card">
            <div class="card-header">
                <h5>Lista de Frequência - {{ data_selecionada|date:"d/m/Y" }}</h5>
            </div>
            <div class="card-body">
                {% if frequencias %}
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th style="width: 50px;">#</th>
                                    <th>Aluno</th>
                                    <th style="width: 120px;">Status</th>
                                    <th>Justificativa</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for frequencia in frequencias %}
                                <tr>
                                    <td>{{ forloop.counter }}</td>
                                    <td>
                                        <div class="d-flex align-items-center">
                                            {% if frequencia.aluno.foto %}
                                                <img src="{{ frequencia.aluno.foto.url }}" alt="Foto de {{ frequencia.aluno.nome }}" 
                                                     class="rounded-circle me-2" width="30" height="30" 
                                                     style="object-fit: cover;">
                                            {% else %}
                                                <div class="rounded-circle bg-secondary me-2 d-flex align-items-center justify-content-center" 
                                                     style="width: 30px; height: 30px; color: white;">
                                                    {{ frequencia.aluno.nome|first|upper }}
                                                </div>
                                            {% endif %}
                                            <div>
                                                <div>{{ frequencia.aluno.nome }}</div>
                                                <small class="text-muted">{{ frequencia.aluno.numero_iniciatico|default:"Sem número iniciático" }}</small>
                                            </div>
                                        </div>
                                    </td>
                                    <td>
                                        {% if frequencia.presente %}
                                            <span class="badge bg-success">Presente</span>
                                        {% else %}
                                            <span class="badge bg-danger">Ausente</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        {% if not frequencia.presente %}
                                            {{ frequencia.justificativa|default:"Sem justificativa" }}
                                        {% else %}
                                            -
                                        {% endif %}
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                {% else %}
                    <div class="alert alert-info">
                        <p>Não há registros de frequência para esta data.</p>
                    </div>
                {% endif %}
            </div>
        </div>
    {% else %}
        <div class="alert alert-info">
            <p>Selecione uma data para visualizar os registros de frequência.</p>
        </div>
    {% endif %}
</div>
{% endblock %}

{% block extra_js %}
{% if data_selecionada %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        var ctx = document.getElementById('frequenciaChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Presentes', 'Ausentes'],
                datasets: [{
                    data: [{{ presentes }}, {{ ausentes }}],
                    backgroundColor: [
                        'rgba(40, 167, 69, 0.8)',
                        'rgba(220, 53, 69, 0.8)'
                    ],
                    borderColor: [
                        'rgba(40, 167, 69, 1)',
                        'rgba(220, 53, 69, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Distribuição de Frequência'
                    }
                }
            }
        });
    });
</script>
{% endif %}
{% endblock %}

