"""
Script para remover turmas órfãs (sem curso válido) e todos os registros relacionados nos principais apps do projeto OMAUM.
- Remove: Matrículas, Atividades, Presenças, Notas, Pagamentos relacionados à turma.
- Loga IDs e nomes das turmas removidas.
- Seguro para rodar via shell Django: python manage.py shell < scripts/limpar_turmas_orfas.py
- Agora trata FK, M2M e ausência de campo de forma robusta.
"""
from core.utils import get_model_dynamically
from django.db import transaction
from django.db.models.fields.related import ManyToManyField

Turma = get_model_dynamically("turmas", "Turma")

# Modelos relacionados e seus possíveis campos de relação
relacionamentos = [
    ("matriculas", "Matricula", ["turma"]),
    ("atividades", "AtividadeAcademica", ["turmas", "turma"]),  # M2M ou FK
    ("presencas", "Presenca", ["turma"]),
    ("notas", "Nota", ["turma"]),
    ("pagamentos", "Pagamento", ["turma"]),
]

removidas = []
erros = []

def remover_dependencias(model, turma, campos):
    for campo in campos:
        # Verifica se o campo existe no modelo
        if hasattr(model, campo):
            field = model._meta.get_field(campo)
            try:
                if isinstance(field, ManyToManyField):
                    # Para M2M, remove a turma da relação
                    for obj in model.objects.filter(**{f"{campo}__id": turma.id}):
                        getattr(obj, campo).remove(turma)
                else:
                    # Para FK, deleta os objetos relacionados
                    model.objects.filter(**{campo: turma}).delete()
            except Exception as e:
                erros.append(f"Erro ao remover dependências em {model.__name__}.{campo}: {e}")

with transaction.atomic():
    for turma in Turma.objects.all():
        try:
            _ = turma.curso  # tenta acessar o curso
        except Exception:
            print(f"Removendo turma órfã: {turma.id} - {turma.nome}")
            for app, model_name, campos in relacionamentos:
                try:
                    model = get_model_dynamically(app, model_name)
                    remover_dependencias(model, turma, campos)
                except Exception as e:
                    erros.append(f"Erro ao processar {app}.{model_name}: {e}")
            removidas.append((turma.id, turma.nome))
            try:
                turma.delete()
            except Exception as e:
                erros.append(f"Erro ao deletar turma {turma.id}: {e}")

print(f"Total de turmas órfãs removidas: {len(removidas)}")
for tid, nome in removidas:
    print(f"- {tid}: {nome}")
if erros:
    print("\nOcorreram erros durante a limpeza:")
    for erro in erros:
        print("*", erro)
