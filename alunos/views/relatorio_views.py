"""
Views relacionadas a relatórios e exportação de dados.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, F
from django.db.models.functions import ExtractYear
from django.utils import timezone
from django.http import HttpResponse
import csv
import logging
from io import TextIOWrapper

from alunos.utils import get_aluno_model

logger = logging.getLogger(__name__)

@login_required
def painel(request):
    """Exibe o painel de alunos com estatísticas."""
    try:
        Aluno = get_aluno_model()
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
        return render(request, "alunos/painel.html", context)
    except Exception as e:
        messages.error(request, f"Erro ao carregar painel: {str(e)}")
        logger.error(f"Erro ao carregar painel: {str(e)}")
        return redirect("alunos:listar_alunos")

@login_required
def exportar_alunos(request):
    """Exporta os dados dos alunos para um arquivo CSV."""
    try:
        Aluno = get_aluno_model()
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
        logger.error(f"Erro ao exportar alunos: {str(e)}")
        return redirect("alunos:listar_alunos")

@login_required
def importar_alunos(request):
    """Importa alunos de um arquivo CSV."""
    if request.method == "POST" and request.FILES.get("csv_file"):
        try:
            Aluno = get_aluno_model()
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
            logger.error(f"Erro ao importar alunos: {str(e)}")
    return render(request, "alunos/importar_alunos.html")

@login_required
def relatorio_alunos(request):
    """Exibe um relatório com estatísticas sobre os alunos."""
    try:
        Aluno = get_aluno_model()
        total_alunos = Aluno.objects.count()
        total_masculino = Aluno.objects.filter(sexo="M").count()
        total_feminino = Aluno.objects.filter(sexo="F").count()
        total_outros = Aluno.objects.filter(sexo="O").count()
        
        # Calcular idade média
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
        logger.error(f"Erro ao gerar relatório: {str(e)}")
        return redirect("alunos:listar_alunos")