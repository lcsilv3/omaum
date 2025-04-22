# Revisão da Funcionalidade: alunos

## Arquivos forms.py:


### Arquivo: alunos\forms.py

python
from django import forms
from django.core.validators import RegexValidator
from importlib import import_module


def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


class AlunoForm(forms.ModelForm):
    """
    Formulário para criação e edição de alunos.
    """

    # Validadores personalizados
    cpf_validator = RegexValidator(
        r"^\d{11}$", "O CPF deve conter exatamente 11 dígitos numéricos."
    )

    # Campos com validação adicional
    cpf = forms.CharField(
        validators=[cpf_validator],
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Somente números"}
        ),
    )

    class Meta:
        model = get_aluno_model()
        fields = [
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
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "data_nascimento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "hora_nascimento": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "foto": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "sexo": forms.Select(attrs={"class": "form-control"}),
            "situacao": forms.Select(attrs={"class": "form-control"}),
            "numero_iniciatico": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "nome_iniciatico": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "nacionalidade": forms.TextInput(
                attrs={"class": "form-control", "value": "Brasileira"}
            ),
            "naturalidade": forms.TextInput(attrs={"class": "form-control"}),
            "rua": forms.TextInput(attrs={"class": "form-control"}),
            "numero_imovel": forms.TextInput(attrs={"class": "form-control"}),
            "complemento": forms.TextInput(attrs={"class": "form-control"}),
            "bairro": forms.TextInput(attrs={"class": "form-control"}),
            "cidade": forms.TextInput(attrs={"class": "form-control"}),
            "estado": forms.TextInput(attrs={"class": "form-control"}),
            "cep": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Somente números",
                }
            ),
            "nome_primeiro_contato": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "celular_primeiro_contato": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "tipo_relacionamento_primeiro_contato": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "nome_segundo_contato": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "celular_segundo_contato": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "tipo_relacionamento_segundo_contato": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "tipo_sanguineo": forms.TextInput(attrs={"class": "form-control"}),
            "fator_rh": forms.Select(attrs={"class": "form-control"}),
            "alergias": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "condicoes_medicas_gerais": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "convenio_medico": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "hospital": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "cpf": "CPF",
            "nome": "Nome Completo",
            "data_nascimento": "Data de Nascimento",
            "hora_nascimento": "Hora de Nascimento",
            "email": "E-mail",
            "foto": "Foto",
            "sexo": "Sexo",
            "situacao": "Situação",
            "numero_iniciatico": "Número Iniciático",
            "nome_iniciatico": "Nome Iniciático",
            "nacionalidade": "Nacionalidade",
            "naturalidade": "Naturalidade",
            "rua": "Rua",
            "numero_imovel": "Número",
            "complemento": "Complemento",
            "bairro": "Bairro",
            "cidade": "Cidade",
            "estado": "Estado",
            "cep": "CEP",
            "nome_primeiro_contato": "Nome do Primeiro Contato",
            "celular_primeiro_contato": "Celular do Primeiro Contato",
            "tipo_relacionamento_primeiro_contato": "Relacionamento",
            "nome_segundo_contato": "Nome do Segundo Contato",
            "celular_segundo_contato": "Celular do Segundo Contato",
            "tipo_relacionamento_segundo_contato": "Relacionamento",
            "tipo_sanguineo": "Tipo Sanguíneo",
            "fator_rh": "Fator RH",
            "alergias": "Alergias",
            "condicoes_medicas_gerais": "Condições Médicas",
            "convenio_medico": "Convênio Médico",
            "hospital": "Hospital de Preferência",
        }
        help_texts = {
            "cpf": "Digite apenas os 11 números do CPF, sem pontos ou traços.",
            "data_nascimento": "Formato: DD/MM/AAAA",
            "hora_nascimento": "Formato: HH:MM",
            "situacao": "Selecione a situação atual do aluno.",
            "numero_iniciatico": "Número único de identificação do iniciado.",
            "cep": "Digite apenas os 8 números do CEP, sem hífen.",
            "tipo_sanguineo": "Ex: A, B, AB, O",
            "fator_rh": "Positivo (+) ou Negativo (-)",
            "alergias": "Liste todas as alergias conhecidas. Deixe em branco se não houver.",
            "condicoes_medicas_gerais": "Descreva condições médicas relevantes. Deixe em branco se não houver.",
        }

    def clean_cpf(self):
        """Validação personalizada para o campo CPF."""
        cpf = self.cleaned_data.get("cpf")
        if cpf:
            # Remove caracteres não numéricos
            cpf = "".join(filter(str.isdigit, cpf))

            # Verifica se tem 11 dígitos
            if len(cpf) != 11:
                raise forms.ValidationError(
                    "O CPF deve conter exatamente 11 dígitos."
                )

            # Aqui você poderia adicionar uma validação mais complexa do CPF
            # como verificar os dígitos verificadores

        return cpf

    def clean_nome(self):
        """Validação personalizada para o campo nome."""
        nome = self.cleaned_data.get("nome")
        if nome:
            # Capitaliza a primeira letra de cada palavra
            nome = " ".join(word.capitalize() for word in nome.split())
        return nome

    def clean_email(self):
        """Validação personalizada para o campo email."""
        email = self.cleaned_data.get("email")
        if email:
            email = email.lower()  # Converte para minúsculas

            # Verifica se o email já existe (exceto para o próprio registro em
            # caso de edição)
            Aluno = get_aluno_model()
            instance = getattr(self, "instance", None)
            if instance and instance.pk:
                if (
                    Aluno.objects.filter(email=email)
                    .exclude(pk=instance.pk)
                    .exists()
                ):
                    raise forms.ValidationError(
                        "Este e-mail já está em uso por outro aluno."
                    )
            else:
                if Aluno.objects.filter(email=email).exists():
                    raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    def clean_cep(self):
        """Validação personalizada para o campo CEP."""
        cep = self.cleaned_data.get("cep")
        if cep:
            # Remove caracteres não numéricos
            cep = "".join(filter(str.isdigit, cep))

            # Verifica se tem 8 dígitos
            if len(cep) != 8:
                raise forms.ValidationError(
                    "O CEP deve conter exatamente 8 dígitos."
                )
        return cep

    def clean_situacao(self):
        """Validação personalizada para o campo situacao."""
        situacao = self.cleaned_data.get("situacao")
        situacao_anterior = None

        # Verificar se é uma edição e se a situação mudou
        if self.instance and self.instance.pk:
            situacao_anterior = self.instance.situacao

            # Se a situação mudou de "ATIVO" para outra coisa, verificar se o
            # aluno é instrutor em alguma turma
            if situacao_anterior == "ATIVO" and situacao != "ATIVO":
                from importlib import import_module

                try:
                    # Importar o modelo Turma dinamicamente
                    turmas_module = import_module("turmas.models")
                    Turma = getattr(turmas_module, "Turma")

                    # Verificar se o aluno é instrutor em alguma turma ativa
                    turmas_como_instrutor = Turma.objects.filter(
                        instrutor=self.instance, status="A"
                    ).count()

                    turmas_como_instrutor_auxiliar = Turma.objects.filter(
                        instrutor_auxiliar=self.instance, status="A"
                    ).count()

                    turmas_como_auxiliar_instrucao = Turma.objects.filter(
                        auxiliar_instrucao=self.instance, status="A"
                    ).count()

                    total_turmas = (
                        turmas_como_instrutor
                        + turmas_como_instrutor_auxiliar
                        + turmas_como_auxiliar_instrucao
                    )

                    if total_turmas > 0:
                        # Não vamos lançar erro aqui, apenas registrar para
                        # mostrar alerta na view
                        self.aluno_e_instrutor = True
                        self.total_turmas_como_instrutor = total_turmas
                except (ImportError, AttributeError):
                    pass

        return situacao

    def clean(self):
        """Validação global do formulário."""
        cleaned_data = super().clean()

        # Verifica se pelo menos um contato de emergência foi fornecido
        nome_primeiro_contato = cleaned_data.get("nome_primeiro_contato")
        celular_primeiro_contato = cleaned_data.get("celular_primeiro_contato")

        if not nome_primeiro_contato or not celular_primeiro_contato:
            self.add_error(
                "nome_primeiro_contato",
                "É necessário fornecer pelo menos um contato de emergência.",
            )
            self.add_error(
                "celular_primeiro_contato",
                "É necessário fornecer pelo menos um contato de emergência.",
            )

        return cleaned_data



## Arquivos views.py:


### Arquivo: alunos\views.py

python
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
        # Adicionar filtro por curso
        if curso_id:
            try:
                # Importar o modelo Matricula dinamicamente
                Matricula = import_module("matriculas.models").Matricula
                # Filtrar alunos matriculados no curso especificado
                alunos_ids = (
                    Matricula.objects.filter(
                        turma__curso__codigo_curso=curso_id
                    )
                    .values_list("aluno__cpf", flat=True)
                    .distinct()
                )
                alunos = alunos.filter(cpf__in=alunos_ids)
            except (ImportError, AttributeError) as e:
                # Log do erro, mas continuar sem o filtro de curso
                print(f"Erro ao filtrar por curso: {e}")
        # Paginação
        paginator = Paginator(alunos, 10)  # 10 alunos por página
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        # Obter cursos para o filtro
        try:
            Curso = import_module("cursos.models").Curso
            cursos = Curso.objects.all()
        except:
            cursos = []
        context = {
            "alunos": page_obj,
            "page_obj": page_obj,
            "query": query,
            "cursos": cursos,
            "curso_selecionado": curso_id,
        }
        return render(request, "alunos/listar_alunos.html", context)
    except Exception as e:
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
    return render(
        request,
        "alunos/detalhar_aluno.html",
        {
            "aluno": aluno,
            "turmas_como_instrutor": turmas_como_instrutor,
            "turmas_como_instrutor_auxiliar": turmas_como_instrutor_auxiliar,
            "turmas_como_auxiliar_instrucao": turmas_como_auxiliar_instrucao,
        },
    )

@login_required
def editar_aluno(request, cpf):
    """Edita um aluno existente."""
    Aluno = get_models()
    AlunoForm = get_forms()
    aluno = get_object_or_404(Aluno, cpf=cpf)
    situacao_anterior = aluno.situacao
    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES, instance=aluno)
        # Verificar se o formulário é válido
        if form.is_valid():
            try:
                # Verificar se a situação mudou de "ATIVO" para outra
                nova_situacao = form.cleaned_data.get("situacao")
                # Se a situação mudou e o aluno é instrutor em alguma turma
                if (
                    situacao_anterior == "ATIVO"
                    and nova_situacao != "ATIVO"
                    and hasattr(form, "aluno_e_instrutor")
                ):
                    # Verificar se o usuário confirmou a remoção da instrutoria
                    if (
                        request.POST.get("confirmar_remocao_instrutoria")
                        != "1"
                    ):
                        # Redirecionar para a página de confirmação
                        return redirect(
                            "alunos:confirmar_remocao_instrutoria",
                            cpf=aluno.cpf,
                            nova_situacao=nova_situacao,
                        )
                    # Se confirmou, atualizar as turmas
                    from importlib import import_module
                    try:
                        # Importar o modelo Turma dinamicamente
                        turmas_module = import_module("turmas.models")
                        Turma = getattr(turmas_module, "Turma")
                        # Buscar turmas onde o aluno é instrutor
                        turmas_instrutor = Turma.objects.filter(
                            instrutor=aluno, status="A"
                        )
                        turmas_instrutor_auxiliar = Turma.objects.filter(
                            instrutor_auxiliar=aluno, status="A"
                        )
                        turmas_auxiliar_instrucao = Turma.objects.filter(
                            auxiliar_instrucao=aluno, status="A"
                        )
                        # Atualizar as turmas
                        for turma in turmas_instrutor:
                            turma.instrutor = None
                            turma.alerta_instrutor = True
                            turma.alerta_mensagem = f"O instrutor {aluno.nome} foi removido devido à mudança de situação para '{aluno.get_situacao_display()}'."
                            turma.save()
                        for turma in turmas_instrutor_auxiliar:
                            turma.instrutor_auxiliar = None
                            turma.alerta_instrutor = True
                            turma.alerta_mensagem = f"O instrutor auxiliar {aluno.nome} foi removido devido à mudança de situação para '{aluno.get_situacao_display()}'."
                            turma.save()
                        for turma in turmas_auxiliar_instrucao:
                            turma.auxiliar_instrucao = None
                            turma.alerta_instrutor = True
                            turma.alerta_mensagem = f"O auxiliar de instrução {aluno.nome} foi removido devido à mudança de situação para '{aluno.get_situacao_display()}'."
                            turma.save()
                    except (ImportError, AttributeError):
                        pass
                # Salvar o aluno
                form.save()
                messages.success(request, "Aluno atualizado com sucesso!")
                return redirect("alunos:detalhar_aluno", cpf=aluno.cpf)
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
            except Exception as e:
                messages.error(request, f"Erro ao atualizar aluno: {str(e)}")
        else:
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
        writer.writerow(
            [
                "CPF",
                "Nome",
                "Email",
                "Data de Nascimento",
                "Sexo",
                "Número Iniciático",
            ]
        )
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
        Aluno = get_aluno_model()  # Use a função existente para obter o modelo
        # Buscar alunos por nome, CPF ou número iniciático
        alunos = Aluno.objects.filter(
            Q(nome__icontains=query)
            | Q(cpf__icontains=query)
            | Q(numero_iniciatico__icontains=query)
        )[
            :10
        ]  # Limitar a 10 resultados
        # Formatar resultados
        results = []
        for aluno in alunos:
            results.append(
                {
                    "cpf": aluno.cpf,
                    "nome": aluno.nome,
                    "numero_iniciatico": aluno.numero_iniciatico or "N/A",
                    "foto": (
                        aluno.foto.url
                        if hasattr(aluno, "foto") and aluno.foto
                        else None
                    ),
                }
            )
        return JsonResponse(results, safe=False)
    except Exception as e:
        logger.error(f"Error in search_alunos: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def confirmar_remocao_instrutoria(request, cpf, nova_situacao):
    """Confirma a remoção da instrutoria de um aluno."""
    Aluno = get_models()
    aluno = get_object_or_404(Aluno, cpf=cpf)
    # Importar os modelos necessários
    from importlib import import_module
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
                )
                for atribuicao in atribuicoes:
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
        Aluno = get_aluno_model()
        # Buscar apenas alunos ativos
        alunos = Aluno.objects.filter(situacao="ATIVO")
        # Filtrar alunos que podem ser instrutores
        alunos_elegiveis = []
        for aluno in alunos:
            if aluno.pode_ser_instrutor:
                alunos_elegiveis.append(
                    {
                        "cpf": aluno.cpf,
                        "nome": aluno.nome,
                        "numero_iniciatico": aluno.numero_iniciatico or "N/A",
                        "foto": (
                            aluno.foto.url
                            if hasattr(aluno, "foto") and aluno.foto
                            else None
                        ),
                    }
                )
        # Se não houver alunos elegíveis, adicionar um log de aviso
        if not alunos_elegiveis:
            logger.warning(
                "Nenhum aluno elegível para ser instrutor. Usando todos os alunos ativos."
            )
            # Temporariamente, retornar todos os alunos ativos
            for aluno in alunos:
                alunos_elegiveis.append(
                    {
                        "cpf": aluno.cpf,
                        "nome": aluno.nome,
                        "numero_iniciatico": aluno.numero_iniciatico or "N/A",
                        "foto": (
                            aluno.foto.url
                            if hasattr(aluno, "foto") and aluno.foto
                            else None
                        ),
                    }
                )
        logger.info(f"Alunos elegíveis para instrutores: {len(alunos_elegiveis)}")
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
        # Configurar logging
        logger.info(f"Verificando elegibilidade do instrutor com CPF: {cpf}")
        
        Aluno = get_aluno_model()
        aluno = get_object_or_404(Aluno, cpf=cpf)
        logger.info(f"Aluno encontrado: {aluno.nome}, situação: {aluno.situacao}")
        
        # Verificar se o aluno está ativo
        if aluno.situacao != "ATIVO":
            logger.warning(f"Aluno {aluno.nome} não está ativo. Situação: {aluno.situacao}")
            return JsonResponse(
                {
                    "elegivel": False,
                    "motivo": f"O aluno não está ativo. Situação atual: {aluno.get_situacao_display()}",
                }
            )
        
        # Verificar se o aluno pode ser instrutor
        logger.info(f"Verificando método pode_ser_instrutor para {aluno.nome}")
        if not hasattr(aluno, 'pode_ser_instrutor'):
            logger.error(f"Método pode_ser_instrutor não encontrado para o aluno {aluno.nome}")
            return JsonResponse(
                {
                    "elegivel": False,
                    "motivo": "Erro na verificação: o método 'pode_ser_instrutor' não existe.",
                }
            )
        
        # Tentar executar o método pode_ser_instrutor com tratamento de erro
        try:
            pode_ser_instrutor = aluno.pode_ser_instrutor
            logger.info(f"Resultado de pode_ser_instrutor para {aluno.nome}: {pode_ser_instrutor}")
            
            if not pode_ser_instrutor:
                # Verificar matrículas em cursos pré-iniciáticos diretamente para mensagem mais específica
                from importlib import import_module
                matriculas_module = import_module("matriculas.models")
                Matricula = getattr(matriculas_module, "Matricula")
                
                matriculas_pre_iniciatico = Matricula.objects.filter(
                    aluno=aluno, turma__curso__nome__icontains="Pré-iniciático"
                )
                
                if matriculas_pre_iniciatico.exists():
                    cursos = ", ".join([f"{m.turma.curso.nome}" for m in matriculas_pre_iniciatico])
                    logger.warning(f"Aluno {aluno.nome} está matriculado em cursos pré-iniciáticos: {cursos}")
                    return JsonResponse(
                        {
                            "elegivel": False,
                            "motivo": f"O aluno está matriculado em cursos pré-iniciáticos: {cursos}",
                        }
                    )
                else:
                    logger.warning(f"Aluno {aluno.nome} não atende a outros requisitos para ser instrutor")
                    return JsonResponse(
                        {
                            "elegivel": False,
                            "motivo": "O aluno não atende aos requisitos para ser instrutor.",
                        }
                    )
        except Exception as method_error:
            import traceback
            logger.error(f"Erro ao executar método pode_ser_instrutor: {str(method_error)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return JsonResponse(
                {
                    "elegivel": False,
                    "motivo": f"Erro ao verificar requisitos de instrutor: {str(method_error)}",
                }
            )
        
        logger.info(f"Aluno {aluno.nome} é elegível para ser instrutor")
        return JsonResponse({"elegivel": True})
    except Exception as e:
        import traceback
        error_msg = str(e)
        stack_trace = traceback.format_exc()
        logger.error(f"Erro ao verificar elegibilidade: {error_msg}")
        logger.error(f"Traceback: {stack_trace}")
        return JsonResponse(
            {"elegivel": False, "motivo": f"Erro na busca: {error_msg}"},
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
                        # Verificar matrículas em cursos pré-iniciáticos
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


## Arquivos urls.py:


### Arquivo: alunos\urls.py

python
from django.urls import path
from . import views

app_name = "alunos"

urlpatterns = [
    path("", views.listar_alunos, name="listar_alunos"),
    path("criar/", views.criar_aluno, name="criar_aluno"),
    path("<str:cpf>/detalhes/", views.detalhar_aluno, name="detalhar_aluno"),
    path("<str:cpf>/editar/", views.editar_aluno, name="editar_aluno"),
    path("<str:cpf>/excluir/", views.excluir_aluno, name="excluir_aluno"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("exportar/", views.exportar_alunos, name="exportar_alunos"),
    path("importar/", views.importar_alunos, name="importar_alunos"),
    path("relatorio/", views.relatorio_alunos, name="relatorio_alunos"),
    path("search/", views.search_alunos, name="search_alunos"),
    path(
        "<str:cpf>/confirmar-remocao-instrutoria/<str:nova_situacao>/",
        views.confirmar_remocao_instrutoria,
        name="confirmar_remocao_instrutoria",
    ),
    path(
        "api/search-instrutores/",
        views.search_instrutores,
        name="search_instrutores",
    ),
    path("api/get-aluno/<str:cpf>/", views.get_aluno, name="get_aluno"),
    # Adicione esta linha para o novo endpoint
    path(
        "api/verificar-elegibilidade-instrutor/<str:cpf>/",
        views.verificar_elegibilidade_instrutor,
        name="verificar_elegibilidade_instrutor",
    ),
    path(
        "diagnostico-instrutores/",
        views.diagnostico_instrutores,
        name="diagnostico_instrutores",
    ),]


## Arquivos models.py:


### Arquivo: alunos\models.py

python
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Aluno(models.Model):
    # Opções para o campo sexo
    SEXO_CHOICES = [
        ("M", "Masculino"),
        ("F", "Feminino"),
        ("O", "Outro"),
    ]

    # Opções para o campo fator_rh
    FATOR_RH_CHOICES = [
        ("+", "Positivo"),
        ("-", "Negativo"),
    ]

    # Opções para o campo situacao
    SITUACAO_CHOICES = [
        ("ATIVO", "Ativo"),
        ("AFASTADO", "Afastado"),
        ("ESPECIAIS", "Especiais"),
        ("EXCLUIDO", "Excluído"),
        ("FALECIDO", "Falecido"),
        ("LOI", "LOI"),
    ]

    # Validadores
    cpf_validator = RegexValidator(
        regex=r"^\d{11}$", message=_("CPF deve conter 11 dígitos numéricos")
    )

    celular_validator = RegexValidator(
        regex=r"^\d{10,11}$", message=_("Número de celular inválido")
    )

    # Campos do modelo
    cpf = models.CharField(
        max_length=11,
        primary_key=True,
        validators=[cpf_validator],
        verbose_name=_("CPF"),
    )
    nome = models.CharField(max_length=100, verbose_name=_("Nome Completo"))
    data_nascimento = models.DateField(verbose_name=_("Data de Nascimento"))
    hora_nascimento = models.TimeField(
        null=True, blank=True, verbose_name=_("Hora de Nascimento")
    )
    email = models.EmailField(unique=True, verbose_name=_("E-mail"))
    foto = models.ImageField(
        upload_to="alunos/fotos/",
        null=True,
        blank=True,
        verbose_name=_("Foto"),
    )
    sexo = models.CharField(
        max_length=1, choices=SEXO_CHOICES, default="M", verbose_name=_("Sexo")
    )

    # Novo campo situacao
    situacao = models.CharField(
        max_length=10,
        choices=SITUACAO_CHOICES,
        default="ATIVO",
        verbose_name=_("Situação"),
    )

    # Dados iniciáticos - Tornando estes campos nullable
    numero_iniciatico = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Número Iniciático"),
    )
    nome_iniciatico = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("Nome Iniciático"),
    )

    # Nacionalidade e naturalidade
    nacionalidade = models.CharField(
        max_length=50, default="Brasileira", verbose_name=_("Nacionalidade")
    )
    naturalidade = models.CharField(
        max_length=50, verbose_name=_("Naturalidade")
    )

    # Endereço
    rua = models.CharField(max_length=100, verbose_name=_("Rua"))
    numero_imovel = models.CharField(max_length=10, verbose_name=_("Número"))
    complemento = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_("Complemento")
    )
    bairro = models.CharField(max_length=50, verbose_name=_("Bairro"))
    cidade = models.CharField(max_length=50, verbose_name=_("Cidade"))
    estado = models.CharField(max_length=2, verbose_name=_("Estado"))
    cep = models.CharField(max_length=8, verbose_name=_("CEP"))

    # Contatos de emergência
    nome_primeiro_contato = models.CharField(
        max_length=100, verbose_name=_("Nome do Primeiro Contato")
    )
    celular_primeiro_contato = models.CharField(
        max_length=11,
        validators=[celular_validator],
        verbose_name=_("Celular do Primeiro Contato"),
    )
    tipo_relacionamento_primeiro_contato = models.CharField(
        max_length=50,
        verbose_name=_("Tipo de Relacionamento do Primeiro Contato"),
    )

    nome_segundo_contato = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Nome do Segundo Contato"),
    )
    celular_segundo_contato = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        validators=[celular_validator],
        verbose_name=_("Celular do Segundo Contato"),
    )
    tipo_relacionamento_segundo_contato = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("Tipo de Relacionamento do Segundo Contato"),
    )

    # Informações médicas
    tipo_sanguineo = models.CharField(
        max_length=3, verbose_name=_("Tipo Sanguíneo")
    )
    fator_rh = models.CharField(
        max_length=1, choices=FATOR_RH_CHOICES, verbose_name=_("Fator RH")
    )
    alergias = models.TextField(
        blank=True, null=True, verbose_name=_("Alergias")
    )
    condicoes_medicas_gerais = models.TextField(
        blank=True, null=True, verbose_name=_("Condições Médicas Gerais")
    )
    convenio_medico = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Convênio Médico"),
    )
    hospital = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Hospital de Preferência"),
    )

    # Metadados - Definindo um valor padrão para created_at
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name=_("Criado em")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Atualizado em")
    )

    def __str__(self):
        return self.nome

    @property
    def esta_ativo(self):
        """Verifica se o aluno está ativo."""
        return self.situacao == "ATIVO"

    @property
    def pode_ser_instrutor(self):
        """Verifica se o aluno pode ser instrutor."""
        from importlib import import_module
        from django.db.models import Q

        # Verificar se o aluno está ativo
        if not self.esta_ativo:
            return False

        try:
            # Importar o modelo Matricula dinamicamente
            matriculas_module = import_module("matriculas.models")
            Matricula = getattr(matriculas_module, "Matricula")

            # Verificar se o aluno está matriculado em algum curso que não seja "Pré-iniciático"
            matriculas = Matricula.objects.filter(
                aluno=self, turma__curso__nome__icontains="Pré-iniciático"
            )

            # Se não tiver matrículas em cursos "Pré-iniciático", pode ser instrutor
            return not matriculas.exists()
        except (ImportError, AttributeError):
            # Se houver erro na importação, retorna False por segurança
            return False

    def clean(self):
        """Validação personalizada para o modelo."""
        super().clean()
    class Meta:
        verbose_name = _("Aluno")
        verbose_name_plural = _("Alunos")
        ordering = ["nome"]



## Arquivos de Template:


### Arquivo: alunos\templates\alunos\confirmar_remocao_instrutoria.html

html
{% extends 'base.html' %}

{% block title %}Confirmar Remoção de Instrutoria{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card border-danger">
        <div class="card-header bg-danger text-white">
            <h4 class="mb-0">Atenção: Remoção de Instrutoria</h4>
        </div>
        <div class="card-body">
            <div class="alert alert-warning">
                <h5>O aluno <strong>{{ aluno.nome }}</strong> é instrutor em {{ total_turmas }} turma(s) ativa(s).</h5>
                <p>Ao alterar a situação para <strong>{{ nova_situacao }}</strong>, o aluno será removido automaticamente como instrutor dessas turmas.</p>
            </div>
            
            {% if turmas_instrutor %}
            <h5 class="mt-4">Turmas onde é Instrutor Principal:</h5>
            <ul class="list-group mb-3">
                {% for turma in turmas_instrutor %}
                <li class="list-group-item">
                    <strong>{{ turma.nome }}</strong> - {{ turma.curso }}
                </li>
                {% endfor %}
            </ul>
            {% endif %}
            
            {% if turmas_instrutor_auxiliar %}
            <h5 class="mt-4">Turmas onde é Instrutor Auxiliar:</h5>
            <ul class="list-group mb-3">
                {% for turma in turmas_instrutor_auxiliar %}
                <li class="list-group-item">
                    <strong>{{ turma.nome }}</strong> - {{ turma.curso }}
                </li>
                {% endfor %}
            </ul>
            {% endif %}
            
            {% if turmas_auxiliar_instrucao %}
            <h5 class="mt-4">Turmas onde é Auxiliar de Instrução:</h5>
            <ul class="list-group mb-3">
                {% for turma in turmas_auxiliar_instrucao %}
                <li class="list-group-item">
                    <strong>{{ turma.nome }}</strong> - {{ turma.curso }}
                </li>
                {% endfor %}
            </ul>
            {% endif %}
            
            <form method="post" class="mt-4">
                {% csrf_token %}
                <div class="d-flex justify-content-between">
                    <a href="{% url 'alunos:editar_aluno' aluno.cpf %}" class="btn btn-secondary">Cancelar</a>
                    <button type="submit" class="btn btn-danger">
                        Confirmar Alteração e Remover Instrutoria
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: alunos\templates\alunos\criar_aluno.html

html
{% extends 'base.html' %}

{% block title %}Criar Novo Aluno{% endblock %}

{% block content %}
<div class="container mt-4">
  <h1>Criar Novo Aluno</h1>
  
  <form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    
    {% for field in form %}
      <div class="form-group">
        <label for="{{ field.id_for_label }}">{{ field.label }}</label>
        {{ field }}
        {% if field.help_text %}
          <small class="form-text text-muted">{{ field.help_text }}</small>
        {% endif %}
        {% for error in field.errors %}
          <div class="alert alert-danger">{{ error }}</div>
        {% endfor %}
      </div>
    {% endfor %}
    
    <button type="submit" class="btn btn-primary">Salvar</button>
    <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}



### Arquivo: alunos\templates\alunos\dashboard.html

html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container mt-4">
    <h1 class="mb-4">Dashboard de Alunos</h1>

    <div class="row">
        <!-- Cartão de Total de Alunos -->
        <div class="col-md-3 mb-4">
            <div class="card text-white bg-primary">
                <div class="card-body">
                    <h5 class="card-title">Total de Alunos</h5>
                    <p class="card-text display-4">{{ total_alunos }}</p>
                </div>
            </div>
        </div>

        <!-- Cartão de Alunos Ativos -->
        <div class="col-md-3 mb-4">
            <div class="card text-white bg-success">
                <div class="card-body">
                    <h5 class="card-title">Alunos Ativos</h5>
                    <p class="card-text display-4">{{ alunos_ativos }}</p>
                </div>
            </div>
        </div>

        <!-- Cartão de Alunos por Curso -->
        <div class="col-md-3 mb-4">
            <div class="card text-white bg-info">
                <div class="card-body">
                    <h5 class="card-title">Cursos</h5>
                    <p class="card-text display-4">{{ total_cursos }}</p>
                </div>
            </div>
        </div>

        <!-- Cartão de Atividades Recentes -->
        <div class="col-md-3 mb-4">
            <div class="card text-white white-warning">
                <div class="card-body">
                    <h5 class="card-title">Atividades Recentes</h5>
                    <p class="card-text display-4">{{ atividades_recentes }}</p>
                </div>
            </div>
        </div>
    </div>

    <div class="row mt-4">
        <!-- Gráfico de Alunos por Curso -->
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Alunos por Curso</h5>
                    <canvas id="alunosPorCursoChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Lista de Alunos Recentes -->
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Alunos Recentemente Adicionados</h5>
                    <ul class="list-group">
                        {% for aluno in alunos_recentes %}
                            <li class="list-group-item">
                                {{ aluno.nome }}
                                <a href="{% url 'alunos:detalhes' aluno.cpf %}" class="btn btn-sm btn-info float-right">Detalhes</a>
                            </li>
                        {% empty %}
                            <li class="list-group-item">Nenhum aluno recente.</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <div class="row mt-4">
        <!-- Ações Rápidas -->
        <div class="col-md-12">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Ações Rápidas</h5>
                    <a href="{% url 'alunos:cadastrar' %}" class="btn btn-primary mr-2">Cadastrar Novo Aluno</a>
                    <a href="{% url 'alunos:listar' %}" class="btn btn-secondary mr-2">Listar Todos os Alunos</a>
                    <a href="{% url 'alunos:exportar' %}" class="btn btn-success mr-2">Exportar Dados</a>
                    <a href="{% url 'alunos:importar' %}" class="btn btn-info">Importar Dados</a>
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
    var ctx = document.getElementById('alunosPorCursoChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: JSON.parse('{{ cursos_labels|safe }}'),
            datasets: [{
                label: 'Número de Alunos',
                data: JSON.parse('{{ alunos_por_curso_data|safe }}'),
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
</script>
{% endblock %}




### Arquivo: alunos\templates\alunos\detalhar_aluno.html

html
{% extends 'base.html' %}

{% block title %}Detalhes do Aluno: {{ aluno.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Detalhes do Aluno</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'alunos:editar_aluno' aluno.cpf %}" class="btn btn-warning me-2">Editar</a>
            <a href="{% url 'alunos:excluir_aluno' aluno.cpf %}" class="btn btn-danger">Excluir</a>
        </div>
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
            <h5>Dados Pessoais</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-8">
                    <div class="row">
                        <div class="col-md-6">
                            <p><strong>CPF:</strong> {{ aluno.cpf }}</p>
                            <p><strong>Nome:</strong> {{ aluno.nome }}</p>
                            <p><strong>Data de Nascimento:</strong> {{ aluno.data_nascimento|date:"d/m/Y" }}</p>
                            <p><strong>Hora de Nascimento:</strong> {{ aluno.hora_nascimento|time:"H:i" }}</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Email:</strong> {{ aluno.email }}</p>
                            <p><strong>Sexo:</strong> {{ aluno.get_sexo_display }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <!-- Moldura tracejada azul brilhante sem cabeçalho -->
                    <div class="border rounded p-3 text-center" 
                         style="border-style: dashed !important; 
                                border-color: #007bff !important; 
                                border-width: 2px !important;
                                height: 200px; 
                                display: flex; 
                                align-items: center; 
                                justify-content: center;">
                        {% if aluno.foto %}
                            <img src="{{ aluno.foto.url }}" alt="Foto de {{ aluno.nome }}" 
                                 class="img-fluid rounded" 
                                 style="max-width: 120px; max-height: 160px; object-fit: cover;">
                        {% else %}
                            <div class="text-muted">Sem foto</div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    {% if aluno.esta_ativo %}
    <div class="card mb-4">
        <div class="card-header">
            <h5>Instrutoria</h5>
        </div>
        <div class="card-body">
            {% if turmas_como_instrutor or turmas_como_instrutor_auxiliar or turmas_como_auxiliar_instrucao %}
                <div class="row">
                    {% if turmas_como_instrutor %}
                    <div class="col-md-4">
                        <h6 class="border-bottom pb-2">Como Instrutor Principal</h6>
                        <ul class="list-group">
                            {% for turma in turmas_como_instrutor %}
                            <li class="list-group-item">
                                <a href="{% url 'turmas:detalhar_turma' turma.id %}">{{ turma.nome }}</a>
                                <span class="badge bg-primary float-end">{{ turma.curso }}</span>
                            </li>
                            {% endfor %}
                        </ul>
                    </div>
                    {% endif %}
                    
                    {% if turmas_como_instrutor_auxiliar %}
                    <div class="col-md-4">
                        <h6 class="border-bottom pb-2">Como Instrutor Auxiliar</h6>
                        <ul class="list-group">
                            {% for turma in turmas_como_instrutor_auxiliar %}
                            <li class="list-group-item">
                                <a href="{% url 'turmas:detalhar_turma' turma.id %}">{{ turma.nome }}</a>
                                <span class="badge bg-info float-end">{{ turma.curso }}</span>
                            </li>
                            {% endfor %}
                        </ul>
                    </div>
                    {% endif %}
                    
                    {% if turmas_como_auxiliar_instrucao %}
                    <div class="col-md-4">
                        <h6 class="border-bottom pb-2">Como Auxiliar de Instrução</h6>
                        <ul class="list-group">
                            {% for turma in turmas_como_auxiliar_instrucao %}
                            <li class="list-group-item">
                                <a href="{% url 'turmas:detalhar_turma' turma.id %}">{{ turma.nome }}</a>
                                <span class="badge bg-success float-end">{{ turma.curso }}</span>
                            </li>
                            {% endfor %}
                        </ul>
                    </div>
                    {% endif %}
                </div>
            {% else %}
                <p class="text-muted">Este aluno não é instrutor em nenhuma turma ativa.</p>
            {% endif %}
        </div>
    </div>
    {% endif %}
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Dados Iniciáticos</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Número Iniciático:</strong> {{ aluno.numero_iniciatico }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Nome Iniciático:</strong> {{ aluno.nome_iniciatico }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Nacionalidade e Naturalidade</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Nacionalidade:</strong> {{ aluno.nacionalidade }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Naturalidade:</strong> {{ aluno.naturalidade }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Endereço</h5>
        </div>
        <div class="card-body">
            <p><strong>Endereço Completo:</strong> {{ aluno.rua }}, {{ aluno.numero_imovel }}
                {% if aluno.complemento %}, {{ aluno.complemento }}{% endif %}
                - {{ aluno.bairro }}, {{ aluno.cidade }}/{{ aluno.estado }} - CEP: {{ aluno.cep }}</p>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Contatos de Emergência</h5>
        </div>
        <div class="card-body">
            <h6>Primeiro Contato</h6>
            <p><strong>Nome:</strong> {{ aluno.nome_primeiro_contato }}</p>
            <p><strong>Celular:</strong> {{ aluno.celular_primeiro_contato }}</p>
            <p><strong>Relacionamento:</strong> {{ aluno.tipo_relacionamento_primeiro_contato }}</p>
            
            {% if aluno.nome_segundo_contato %}
                <h6 class="mt-3">Segundo Contato</h6>
                <p><strong>Nome:</strong> {{ aluno.nome_segundo_contato }}</p>
                <p><strong>Celular:</strong> {{ aluno.celular_segundo_contato }}</p>
                <p><strong>Relacionamento:</strong> {{ aluno.tipo_relacionamento_segundo_contato }}</p>
            {% endif %}
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações Médicas</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-3">
                    <p><strong>Tipo Sanguíneo:</strong> {{ aluno.tipo_sanguineo }}</p>
                </div>
                <div class="col-md-3">
                    <p><strong>Fator RH:</strong> {{ aluno.get_fator_rh_display }}</p>
                </div>
                <div class="col-md-3">
                    <p><strong>Convênio Médico:</strong> {{ aluno.convenio_medico|default:"Não informado" }}</p>
                </div>
                <div class="col-md-3">
                    <p><strong>Hospital:</strong> {{ aluno.hospital|default:"Não informado" }}</p>
                </div>
            </div>
            
            <div class="row mt-3">
                <div class="col-md-6">
                    <p><strong>Alergias:</strong> {{ aluno.alergias|default:"Nenhuma" }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Condições Médicas:</strong> {{ aluno.condicoes_medicas_gerais|default:"Nenhuma" }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="d-flex justify-content-between mb-5">
        <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-secondary">Voltar para a lista</a>
        <div>
            <a href="{% url 'alunos:editar_aluno' aluno.cpf %}" class="btn btn-warning me-2">Editar</a>
            <a href="{% url 'alunos:excluir_aluno' aluno.cpf %}" class="btn btn-danger">Excluir</a>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: alunos\templates\alunos\diagnostico_instrutores.html

html
{% extends 'base.html' %}

{% block title %}Diagnóstico de Elegibilidade de Instrutores{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Diagnóstico de Elegibilidade de Instrutores</h1>
    
    <div class="alert alert-info">
        <p>Esta página mostra o diagnóstico de elegibilidade de todos os alunos ativos para serem instrutores.</p>
        <p>Total de alunos: {{ total_alunos }}</p>
        <p>Alunos elegíveis: {{ total_elegiveis }} ({{ total_elegiveis|floatformat:1 }}%)</p>
        <p>Alunos inelegíveis: {{ total_inelegiveis }} ({{ total_inelegiveis|floatformat:1 }}%)</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Filtros</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <div class="form-check form-switch">
                        <input class="form-check-input" type="checkbox" id="mostrar-elegiveis" checked>
                        <label class="form-check-label" for="mostrar-elegiveis">Mostrar alunos elegíveis</label>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-check form-switch">
                        <input class="form-check-input" type="checkbox" id="mostrar-inelegiveis" checked>
                        <label class="form-check-label" for="mostrar-inelegiveis">Mostrar alunos inelegíveis</label>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="table-responsive">
        <table class="table table-striped" id="tabela-diagnostico">
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>CPF</th>
                    <th>Nº Iniciático</th>
                    <th>Situação</th>
                    <th>Elegível</th>
                    <th>Motivo</th>
                </tr>
            </thead>
            <tbody>
                {% for item in alunos_diagnostico %}
                <tr class="{% if item.pode_ser_instrutor %}elegivel{% else %}inelegivel{% endif %}">
                    <td>{{ item.aluno.nome }}</td>
                    <td>{{ item.aluno.cpf }}</td>
                    <td>{{ item.aluno.numero_iniciatico|default:"N/A" }}</td>
                    <td>{{ item.aluno.get_situacao_display }}</td>
                    <td>
                        {% if item.pode_ser_instrutor %}
                            <span class="badge bg-success">Sim</span>
                        {% else %}
                            <span class="badge bg-danger">Não</span>
                        {% endif %}
                    </td>
                    <td>
                        {% if item.motivo %}
                            {{ item.motivo }}
                            {% if item.cursos_pre_iniciatico %}
                                <br>
                                <small>Cursos: {{ item.cursos_pre_iniciatico|join:", " }}</small>
                            {% endif %}
                        {% else %}
                            -
                        {% endif %}
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="6" class="text-center">Nenhum aluno encontrado.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        const mostrarElegiveisCheckbox = document.getElementById('mostrar-elegiveis');
        const mostrarInelegiveisCheckbox = document.getElementById('mostrar-inelegiveis');
        const tabela = document.getElementById('tabela-diagnostico');
        
        function atualizarVisibilidade() {
            const mostrarElegiveis = mostrarElegiveisCheckbox.checked;
            const mostrarInelegiveis = mostrarInelegiveisCheckbox.checked;
            
            const linhasElegiveis = tabela.querySelectorAll('tbody tr.elegivel');
            const linhasInelegiveis = tabela.querySelectorAll('tbody tr.inelegivel');
            
            linhasElegiveis.forEach(linha => {
                linha.style.display = mostrarElegiveis ? '' : 'none';
            });
            
            linhasInelegiveis.forEach(linha => {
                linha.style.display = mostrarInelegiveis ? '' : 'none';
            });
        }
        
        mostrarElegiveisCheckbox.addEventListener('change', atualizarVisibilidade);
        mostrarInelegiveisCheckbox.addEventListener('change', atualizarVisibilidade);
        
        // Inicializar
        atualizarVisibilidade();
    });
</script>
{% endblock %}



### Arquivo: alunos\templates\alunos\editar_aluno.html

html
{% extends 'base.html' %}

{% block title %}Editar Aluno: {{ aluno.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Aluno: {{ aluno.nome }}</h1>
    
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        
        {% for field in form %}
            <div class="form-group mb-3">
                <label for="{{ field.id_for_label }}">{{ field.label }}</label>
                {{ field }}
                {% if field.help_text %}
                    <small class="form-text text-muted">{{ field.help_text }}</small>
                {% endif %}
                {% for error in field.errors %}
                    <div class="alert alert-danger">{{ error }}</div>
                {% endfor %}
            </div>
        {% endfor %}
        
        <div class="mt-4">
            <button type="submit" class="btn btn-primary">Salvar Alterações</button>
            <a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>
            <a href="{% url 'alunos:detalhar_aluno' aluno.cpf %}" class="btn btn-info">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}



### Arquivo: alunos\templates\alunos\excluir_aluno.html

html
{% extends 'base.html' %}

{% block title %}Excluir Aluno: {{ aluno.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
  <h1>Excluir Aluno: {{ aluno.nome }}</h1>
    
  <div class="alert alert-danger">
      <p>Você tem certeza que deseja excluir o aluno "{{ aluno.nome }}"?</p>
      <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
  </div>
    
  <form method="post">
      {% csrf_token %}
      <button type="submit" class="btn btn-danger">Confirmar Exclusão</button>
      <a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>
      <a href="{% url 'alunos:detalhar_aluno' aluno.cpf %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}




### Arquivo: alunos\templates\alunos\formulario_aluno.html

html
{% extends 'base.html' %}

{% block title %}{% if aluno.id %}Editar{% else %}Novo{% endif %} Aluno{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{% if aluno.id %}Editar{% else %}Novo{% endif %} Aluno</h1>
        <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-secondary">Voltar para a lista</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Dados Pessoais</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <div class="row">
                            <div class="col-md-6">
                                {% include 'includes/form_field.html' with field=form.cpf %}
                                {% include 'includes/form_field.html' with field=form.nome %}
                                {% include 'includes/form_field.html' with field=form.data_nascimento %}
                                {% include 'includes/form_field.html' with field=form.hora_nascimento %}
                            </div>
                            <div class="col-md-6">
                                {% include 'includes/form_field.html' with field=form.email %}
                                {% include 'includes/form_field.html' with field=form.sexo %}
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <!-- Moldura tracejada azul brilhante sem cabeçalho -->
                        <div class="border rounded p-3 mb-3 text-center" 
                             style="border-style: dashed !important; 
                                    border-color: #007bff !important; 
                                    border-width: 2px !important;
                                    height: 200px; 
                                    display: flex; 
                                    align-items: center; 
                                    justify-content: center;">
                            {% if aluno.foto %}
                                <img src="{{ aluno.foto.url }}" alt="Foto de {{ aluno.nome }}" 
                                     class="img-fluid rounded" 
                                     style="max-width: 120px; max-height: 160px; object-fit: cover;">
                            {% else %}
                                <div class="text-muted">Sem foto</div>
                            {% endif %}
                        </div>
                        
                        <!-- Campo de upload separado da moldura -->
                        <div class="form-group">
                            {{ form.foto }}
                            {% if form.foto.help_text %}
                                <small class="form-text text-muted">{{ form.foto.help_text }}</small>
                            {% endif %}
                            {% for error in form.foto.errors %}
                                <div class="alert alert-danger">{{ error }}</div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Dados Iniciáticos</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.numero_iniciatico %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome_iniciatico %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Nacionalidade e Naturalidade</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nacionalidade %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.naturalidade %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Endereço</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        {% include 'includes/form_field.html' with field=form.rua %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.numero_imovel %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.complemento %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.bairro %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.cep %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-8">
                        {% include 'includes/form_field.html' with field=form.cidade %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.estado %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Contatos de Emergência</h5>
            </div>
            <div class="card-body">
                <h6>Primeiro Contato</h6>
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.nome_primeiro_contato %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.celular_primeiro_contato %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.tipo_relacionamento_primeiro_contato %}
                    </div>
                </div>
                
                <h6 class="mt-3">Segundo Contato</h6>
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.nome_segundo_contato %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.celular_segundo_contato %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.tipo_relacionamento_segundo_contato %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações Médicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.tipo_sanguineo %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.fator_rh %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.convenio_medico %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.hospital %}
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.alergias %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.condicoes_medicas_gerais %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">
                {% if aluno.id %}Atualizar{% else %}Cadastrar{% endif %} Aluno
            </button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
    // Script para pré-visualização da imagem quando o usuário seleciona uma foto
    document.addEventListener('DOMContentLoaded', function() {
        const fotoInput = document.getElementById('{{ form.foto.id_for_label }}');
        if (fotoInput) {
            fotoInput.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    const preview = document.createElement('img');
                    preview.className = 'img-fluid mt-2 rounded';
                    preview.style.maxHeight = '200px';
                    
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        preview.src = e.target.result;
                    }
                    
                    reader.readAsDataURL(this.files[0]);
                    
                    // Remove qualquer preview anterior
                    const previewContainer = fotoInput.parentNode;
                    const existingPreview = previewContainer.querySelector('img');
                    if (existingPreview) {
                        previewContainer.removeChild(existingPreview);
                    }
                    
                    // Adiciona o novo preview
                    previewContainer.appendChild(preview);
                }
            });
        }
    });
</script>
{% endblock %}




### Arquivo: alunos\templates\alunos\importar_alunos.html

html
{% extends 'base.html' %}

{% block title %}Importar Alunos{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Importar Alunos</h1>
    
    <div class="card">
        <div class="card-body">
            <p class="mb-3">Faça upload de um arquivo CSV contendo os dados dos alunos.</p>
            
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                <div class="mb-3">
                    <label for="csv_file" class="form-label">Arquivo CSV</label>
                    <input type="file" name="csv_file" id="csv_file" class="form-control" accept=".csv" required>
                    <div class="form-text">O arquivo deve ter cabeçalhos: CPF, Nome, Email, etc.</div>
                </div>
                
                <div class="d-flex">
                    <button type="submit" class="btn btn-primary me-2">Importar</button>
                    <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
    
    <div class="mt-3">
        <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-link">Voltar para a lista de alunos</a>
    </div>
</div>
{% endblock %}



### Arquivo: alunos\templates\alunos\listar_alunos.html

html
{% extends 'base.html' %}

{% block title %}Lista de Alunos{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Cabeçalho com título e botões na mesma linha -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Lista de Alunos</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'alunos:criar_aluno' %}" class="btn btn-primary">Novo Aluno</a>
            <a href="{% url 'alunos:exportar_alunos' %}" class="btn btn-success">Exportar CSV</a>
            <a href="{% url 'alunos:importar_alunos' %}" class="btn btn-info">Importar CSV</a>
            <a href="{% url 'alunos:relatorio_alunos' %}" class="btn btn-warning">Relatório</a>
            <a href="{% url 'alunos:dashboard' %}" class="btn btn-dark">Dashboard</a>
            <a href="{% url 'alunos:diagnostico_instrutores' %}" class="btn btn-info">Diagnóstico de Instrutores</a>
        </div>
    </div>
    
    <!-- Barra de busca e filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <form method="get" class="row g-3">
                <div class="col-md-6">
                    <input type="text" name="q" class="form-control" placeholder="Buscar por nome, CPF ou email..." value="{{ query }}">
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
                            <th>Nome</th>
                            <th>CPF</th>
                            <th>Nº Iniciático</th>
                            <th>Email</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for aluno in alunos %}
                            <tr>
                                <td>
                                    <div class="d-flex align-items-center">
                                        {% if aluno.foto %}
                                            <img src="{{ aluno.foto.url }}" alt="Foto de {{ aluno.nome }}" 
                                                 class="rounded-circle me-2" width="40" height="40" 
                                                 style="object-fit: cover;">
                                        {% else %}
                                            <div class="rounded-circle bg-secondary me-2 d-flex align-items-center justify-content-center" 
                                                 style="width: 40px; height: 40px; color: white;">
                                                {{ aluno.nome|first|upper }}
                                            </div>
                                        {% endif %}
                                        {{ aluno.nome }}
                                    </div>
                                </td>
                                <td>{{ aluno.cpf }}</td>
                                <td>{{ aluno.numero_iniciatico|default:"N/A" }}</td>
                                <td>{{ aluno.email }}</td>
                                <td>
                                    {% if aluno.cpf %}
                                        <a href="{% url 'alunos:detalhar_aluno' aluno.cpf %}" class="btn btn-sm btn-info">Detalhes</a>
                                        <a href="{% url 'alunos:editar_aluno' aluno.cpf %}" class="btn btn-sm btn-warning">Editar</a>
                                        <a href="{% url 'alunos:excluir_aluno' aluno.cpf %}" class="btn btn-sm btn-danger">Excluir</a>
                                    {% else %}
                                        <span class="text-muted">CPF não disponível</span>
                                    {% endif %}
                                </td>
                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="5" class="text-center">
                                    <p class="my-3">Nenhum aluno cadastrado.</p>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer">
            <p class="text-muted mb-0">Total: {{ page_obj.paginator.count|default:"0" }} aluno(s)</p>
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
        </div>    </div>
</div>
{% endblock %}




### Arquivo: alunos\templates\alunos\registro.html

html
{% extends 'base.html' %}

{% block content %}
<h2>Registro</h2>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Registrar</button>
</form>

<a href="javascript:history.back()" class="back-button">Voltar</a>

<style>
    .back-button {
        margin-top: 20px;
        display: inline-block;
        padding: 10px 20px;
        background-color: #f0f0f0;
        border: 1px solid #ccc;
        text-decoration: none;
        color: #333;
        border-radius: 5px;
    }
</style>
{% endblock %}




### Arquivo: alunos\templates\alunos\relatorio_alunos.html

html
{% extends 'base.html' %}

{% block title %}Relatório de Alunos{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Relatório de Alunos</h1>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="card-title">Estatísticas Gerais</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-3">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Total de Alunos</h5>
                            <p class="card-text display-4">{{ total_alunos }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Masculino</h5>
                            <p class="card-text display-4">{{ total_masculino }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Feminino</h5>
                            <p class="card-text display-4">{{ total_feminino }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Outros</h5>
                            <p class="card-text display-4">{{ total_outros }}</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="card mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Idade Média</h5>
                            <p class="card-text display-4">{{ idade_media|floatformat:1 }} anos</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}


