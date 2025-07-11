from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from io import TextIOWrapper
import csv
import datetime

from atividades.models import Atividade
from turmas.models import Turma
from alunos.models import Aluno

def parse_date(date_str):
    """Converte uma string de data para um objeto date."""
    if not date_str:
        return None
    
    # Tentar diferentes formatos
    formats = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"]
    
    for fmt in formats:
        try:
            return datetime.datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    
    raise ValueError(f"Formato de data inválido: {date_str}")

def parse_time(time_str):
    """Converte uma string de hora para um objeto time."""
    if not time_str:
        return None
    
    # Tentar diferentes formatos
    formats = ["%H:%M", "%H:%M:%S"]
    
    for fmt in formats:
        try:
            return datetime.datetime.strptime(time_str, fmt).time()
        except ValueError:
            continue
    
    raise ValueError(f"Formato de hora inválido: {time_str}")

@login_required
def importar_atividades_academicas(request):
    """Importa atividades a partir de um arquivo CSV."""
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")
        reader = csv.DictReader(csv_file)
        count = 0
        errors = []
        for row in reader:
            try:
                atividade = Atividade(
                    nome=row.get("Nome", "").strip(),
                    descricao=row.get("Descricao", "").strip(),
                    tipo_atividade=row.get("Tipo", "AULA").strip().upper(),
                    data_inicio=parse_date(row.get("Data_Inicio", "")),
                    data_fim=parse_date(row.get("Data_Fim", "")),
                    hora_inicio=parse_time(row.get("Hora_Inicio", "")),
                    hora_fim=parse_time(row.get("Hora_Fim", "")),
                    local=row.get("Local", "").strip(),
                    responsavel=row.get("Responsavel", "").strip(),
                    status=row.get("Status", "PENDENTE").strip().upper(),
                )
                atividade.full_clean()
                atividade.save()
                # Turmas (opcional)
                turmas_str = row.get("Turmas", "").strip()
                if turmas_str:
                    turmas_ids = [t.strip() for t in turmas_str.split(",")]
                    for turma_id in turmas_ids:
                        try:
                            turma = Turma.objects.get(id=turma_id)
                            atividade.turmas.add(turma)
                        except Turma.DoesNotExist:
                            errors.append(f"Turma com ID {turma_id} não encontrada para '{atividade.nome}'")
                count += 1
            except Exception as e:
                errors.append(f"Erro na linha {count+1}: {str(e)}")
        if errors:
            messages.warning(request, f"{count} atividades importadas com {len(errors)} erros.")
            for error in errors[:5]:
                messages.error(request, error)
        else:
            messages.success(request, f"{count} atividades importadas com sucesso!")
        return redirect("atividades:listar_atividades")
    return render(request, "atividades/importar_atividades_academicas.html")

@login_required
def importar_atividades_ritualisticas(request):
    """Importa atividades a partir de um arquivo CSV (mantido para compatibilidade)."""
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")
        reader = csv.DictReader(csv_file)
        count = 0
        errors = []
        for row in reader:
            try:
                atividade = Atividade(
                    nome=row.get("Nome", "").strip(),
                    descricao=row.get("Descricao", "").strip(),
                    data_inicio=parse_date(row.get("Data", "")),
                    data_fim=parse_date(row.get("Data", "")),  # Usar a mesma data para inicio e fim
                    hora_inicio=parse_time(row.get("Hora_Inicio", "")),
                    hora_fim=parse_time(row.get("Hora_Fim", "")),
                    local=row.get("Local", "").strip(),
                    responsavel=row.get("Responsavel", "").strip(),
                    status=row.get("Status", "PENDENTE").strip().upper(),
                )
                atividade.full_clean()
                atividade.save()
                count += 1
            except Exception as e:
                errors.append(f"Erro na linha {count+1}: {str(e)}")
        if errors:
            messages.warning(request, f"{count} atividades importadas com {len(errors)} erros.")
            for error in errors[:5]:
                messages.error(request, error)
        else:
            messages.success(request, f"{count} atividades importadas com sucesso!")
        return redirect("atividades:listar_atividades")
    return render(request, "atividades/importar_atividades.html")