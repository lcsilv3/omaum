import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse
from ..utils import get_model_dynamically

logger = logging.getLogger(__name__)

@login_required
def exportar_frequencias(request):
    """Exporta os dados de frequências mensais para um arquivo CSV."""
    try:
        import csv
        
        FrequenciaMensal = get_model_dynamically("frequencias", "FrequenciaMensal")
        frequencias = FrequenciaMensal.objects.all().select_related('turma', 'turma__curso')
        
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="frequencias.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "ID",
            "Turma",
            "Curso",
            "Mês",
            "Ano",
            "Percentual Mínimo",
            "Total de Alunos",
            "Alunos com Carência",
            "Alunos Liberados"
        ])
        
        for freq in frequencias:
            writer.writerow([
                freq.id,
                freq.turma.nome,
                freq.turma.curso.nome if freq.turma.curso else "",
                freq.get_mes_display(),
                freq.ano,
                freq.percentual_minimo,
                freq.total_alunos,
                freq.alunos_com_carencia,
                freq.alunos_liberados
            ])
        
        return response
    except Exception as e:
        messages.error(request, f"Erro ao exportar frequências: {str(e)}")
        return redirect("frequencias:listar_frequencias")

@login_required
def importar_frequencias(request):
    """Importa frequências mensais de um arquivo CSV."""
    if request.method == "POST" and request.FILES.get("csv_file"):
        try:
            import csv
            from io import TextIOWrapper
            
            FrequenciaMensal = get_model_dynamically("frequencias", "FrequenciaMensal")
            Turma = get_model_dynamically("turmas", "Turma")
            
            csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")
            reader = csv.DictReader(csv_file)
            count = 0
            errors = []
            
            for row in reader:
                try:
                    # Buscar turma pelo nome ou ID
                    turma = None
                    turma_nome = row.get("Turma", "").strip()
                    if turma_nome:
                        try:
                            turma = Turma.objects.get(nome=turma_nome)
                        except Turma.DoesNotExist:
                            try:
                                turma = Turma.objects.get(id=turma_nome)
                            except (Turma.DoesNotExist, ValueError):
                                errors.append(f"Turma não encontrada: {turma_nome}")
                                continue
                    else:
                        errors.append("Turma não especificada")
                        continue
                    
                    # Processar mês
                    mes = None
                    mes_nome = row.get("Mês", "").strip()
                    if mes_nome:
                        # Mapear nome do mês para número
                        meses = {
                            "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4,
                            "Maio": 5, "Junho": 6, "Julho": 7, "Agosto": 8,
                            "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
                        }
                        mes = meses.get(mes_nome)
                        if not mes:
                            try:
                                mes = int(mes_nome)
                                if mes < 1 or mes > 12:
                                    errors.append(f"Mês inválido: {mes_nome}")
                                    continue
                            except ValueError:
                                errors.append(f"Mês inválido: {mes_nome}")
                                continue
                    else:
                        errors.append("Mês não especificado")
                        continue
                    
                    # Processar ano
                    ano = None
                    try:
                        ano = int(row.get("Ano", "").strip())
                    except ValueError:
                        errors.append(f"Ano inválido: {row.get('Ano', '')}")
                        continue
                    
                    # Processar percentual mínimo
                    percentual_minimo = 75  # Valor padrão
                    try:
                        if row.get("Percentual Mínimo"):
                            percentual_minimo = int(row.get("Percentual Mínimo"))
                    except ValueError:
                        errors.append(f"Percentual mínimo inválido: {row.get('Percentual Mínimo', '')}")
                        continue
                    
                    # Verificar se já existe uma frequência para esta turma/mês/ano
                    if FrequenciaMensal.objects.filter(turma=turma, mes=mes, ano=ano).exists():
                        errors.append(f"Já existe uma frequência para a turma {turma.nome} no mês {mes}/{ano}")
                        continue
                    
                    # Criar a frequência mensal
                    frequencia = FrequenciaMensal.objects.create(
                        turma=turma,
                        mes=mes,
                        ano=ano,
                        percentual_minimo=percentual_minimo
                    )
                    
                    # Calcular carências
                    frequencia.calcular_carencias()
                    
                    count += 1
                except Exception as e:
                    errors.append(f"Erro na linha {count+1}: {str(e)}")
            
            if errors:
                messages.warning(
                    request,
                    f"{count} frequências importadas com {len(errors)} erros.",
                )
                for error in errors[:5]:  # Mostrar apenas os 5 primeiros erros
                    messages.error(request, error)
                if len(errors) > 5:
                    messages.error(
                        request, f"... e mais {len(errors) - 5} erros."
                    )
            else:
                messages.success(
                    request, f"{count} frequências importadas com sucesso!"
                )
            return redirect("frequencias:listar_frequencias")
        except Exception as e:
            messages.error(request, f"Erro ao importar frequências: {str(e)}")
    
    return render(request, "frequencias/importar_frequencias.html")