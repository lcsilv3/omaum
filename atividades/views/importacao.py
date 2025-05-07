from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from io import TextIOWrapper
import csv
import datetime
from importlib import import_module

def get_models():
    """Obtém os modelos AtividadeAcademica e AtividadeRitualistica."""
    atividades_module = import_module("atividades.models")
    AtividadeAcademica = getattr(atividades_module, "AtividadeAcademica")
    AtividadeRitualistica = getattr(atividades_module, "AtividadeRitualistica")
    return AtividadeAcademica, AtividadeRitualistica

def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

def get_aluno_model():
    """Obtém o modelo Aluno."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

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

def parse_date_time(datetime_str):
    """Converte uma string de data e hora para um objeto datetime."""
    if not datetime_str:
        return None
    
    # Tentar diferentes formatos
    formats = ["%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M", "%d-%m-%Y %H:%M", 
               "%d/%m/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d-%m-%Y %H:%M:%S"]
    
    for fmt in formats:
        try:
            return datetime.datetime.strptime(datetime_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Formato de data e hora inválido: {datetime_str}")

@login_required
def importar_atividades(request):
    """Importa atividades a partir de um arquivo CSV."""
    AtividadeAcademica, AtividadeRitualistica = get_models()
    
    if request.method == "POST" and request.FILES.get("csv_file"):
        try:
            # Obter o tipo de atividade a ser importada
            tipo_atividade = request.POST.get("tipo_atividade", "academica")
            
            # Abrir o arquivo CSV
            csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")
            reader = csv.DictReader(csv_file)
            
            count = 0
            errors = []
            
            # Importar atividades acadêmicas
            if tipo_atividade == "academica":
                for row in reader:
                    try:
                        # Criar a atividade acadêmica
                        atividade = AtividadeAcademica(
                            nome=row.get("Nome", "").strip(),
                            descricao=row.get("Descricao", "").strip(),
                            data_inicio=parse_date_time(row.get("Data_Inicio", "")),
                            data_fim=parse_date_time(row.get("Data_Fim", "")) if row.get("Data_Fim") else None,
                            responsavel=row.get("Responsavel", "").strip(),
                            local=row.get("Local", "").strip(),
                            tipo_atividade=row.get("Tipo", "aula").strip().lower(),
                            status=row.get("Status", "agendada").strip().lower()
                        )
                        
                        # Validar e salvar
                        atividade.full_clean()
                        atividade.save()
                        
                        # Adicionar turmas
                        turmas_str = row.get("Turmas", "").strip()
                        if turmas_str:
                            Turma = get_turma_model()
                            turmas_ids = [t.strip() for t in turmas_str.split(",")]
                            for turma_id in turmas_ids:
                                try:
                                    turma = Turma.objects.get(id=turma_id)
                                    atividade.turmas.add(turma)
                                except Turma.DoesNotExist:
                                    errors.append(f"Turma com ID {turma_id} não encontrada para a atividade '{atividade.nome}'")
                        
                        count += 1
                    except Exception as e:
                        errors.append(f"Erro na linha {count+1}: {str(e)}")
            
            # Importar atividades ritualísticas
            elif tipo_atividade == "ritualistica":
                for row in reader:
                    try:
                        # Obter a turma
                        Turma = get_turma_model()
                        turma_id = row.get("Turma", "").strip()
                        try:
                            turma = Turma.objects.get(id=turma_id)
                        except Turma.DoesNotExist:
                            errors.append(f"Turma com ID {turma_id} não encontrada para a atividade '{row.get('Nome', '')}'")
                            continue
                        
                        # Criar a atividade ritualística
                        atividade = AtividadeRitualistica(
                            nome=row.get("Nome", "").strip(),
                            descricao=row.get("Descricao", "").strip(),
                            data=parse_date(row.get("Data", "")),
                            hora_inicio=parse_time(row.get("Hora_Inicio", "")),
                            hora_fim=parse_time(row.get("Hora_Fim", "")),
                            local=row.get("Local", "").strip(),
                            turma=turma
                        )
                        
                        # Validar e salvar
                        atividade.full_clean()
                        atividade.save()
                        
                        # Adicionar participantes
                        participantes_str = row.get("Participantes", "").strip()
                        if participantes_str:
                            Aluno = get_aluno_model()
                            participantes_cpfs = [p.strip() for p in participantes_str.split(",")]
                            for cpf in participantes_cpfs:
                                try:
                                    aluno = Aluno.objects.get(cpf=cpf)
                                    atividade.participantes.add(aluno)
                                except Aluno.DoesNotExist:
                                    errors.append(f"Aluno com CPF {cpf} não encontrado para a atividade '{atividade.nome}'")
                        
                        count += 1
                    except Exception as e:
                        errors.append(f"Erro na linha {count+1}: {str(e)}")
            
            # Exibir mensagens de sucesso/erro
            if errors:
                messages.warning(
                    request,
                    f"{count} atividades importadas com {len(errors)} erros.",
                )
                for error in errors[:5]:  # Mostrar apenas os 5 primeiros erros
                    messages.error(request, error)
                if len(errors) > 5:
                    messages.error(
                        request, f"... e mais {len(errors) - 5} erros."
                    )
            else:
                messages.success(
                    request, f"{count} atividades importadas com sucesso!"
                )
            
            # Redirecionar para a lista de atividades
            if tipo_atividade == "academica":
                return redirect("atividades:listar_atividades_academicas")
            else:
                return redirect("atividades:listar_atividades_ritualisticas")
        
        except Exception as e:
            messages.error(request, f"Erro ao importar atividades: {str(e)}")
    
    return render(request, "atividades/importar_atividades.html")