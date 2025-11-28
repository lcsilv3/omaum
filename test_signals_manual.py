"""
Script para testar manualmente os signals de matrícula.
Execute: python manage.py shell < test_signals_manual.py
"""
from django.utils import timezone
from alunos.models import Aluno, Pais
from turmas.models import Turma
from cursos.models import Curso
from matriculas.models import Matricula

print("\n=== TESTE MANUAL DOS SIGNALS DE MATRÍCULA ===\n")

# Buscar ou criar dados de teste
print("1. Buscando dados de teste...")

try:
    pais = Pais.objects.first()
    if not pais:
        print("   ❌ Nenhum país encontrado no banco")
        exit(1)
    
    aluno = Aluno.objects.first()
    if not aluno:
        print("   ❌ Nenhum aluno encontrado no banco")
        exit(1)
    
    print(f"   ✅ Aluno: {aluno.nome}")
    print(f"   📋 Grau atual ANTES: '{aluno.grau_atual}'")
    
    curso = Curso.objects.first()
    if not curso:
        print("   ❌ Nenhum curso encontrado no banco")
        exit(1)
    
    print(f"   ✅ Curso: {curso.nome}")
    
    turma = Turma.objects.filter(curso=curso, status="A").first()
    if not turma:
        print("   ❌ Nenhuma turma ativa encontrada")
        exit(1)
    
    print(f"   ✅ Turma: {turma.nome}")
    
    # Verificar se já existe matrícula
    matricula_existente = Matricula.objects.filter(
        aluno=aluno,
        turma=turma
    ).first()
    
    if matricula_existente:
        print(f"\n2. Matrícula já existe (ID: {matricula_existente.id})")
        print(f"   Status: {matricula_existente.get_status_display()}")
        print(f"   Ativa: {matricula_existente.ativa}")
    else:
        print("\n2. Criando nova matrícula...")
        matricula = Matricula.objects.create(
            aluno=aluno,
            turma=turma,
            data_matricula=timezone.now().date(),
            ativa=True,
            status="A"
        )
        print(f"   ✅ Matrícula criada (ID: {matricula.id})")
    
    # Recarregar aluno
    aluno.refresh_from_db()
    
    print(f"\n3. Verificando atualização do grau_atual:")
    print(f"   📋 Grau atual DEPOIS: '{aluno.grau_atual}'")
    print(f"   🎯 Curso da turma: '{turma.curso.nome}'")
    
    if aluno.grau_atual == turma.curso.nome:
        print("\n   ✅ SUCESSO! O campo grau_atual foi atualizado corretamente!")
    else:
        print(f"\n   ❌ FALHA! Esperado: '{turma.curso.nome}', Obtido: '{aluno.grau_atual}'")
    
    print(f"\n4. Propriedade grau_atual_automatico: '{aluno.grau_atual_automatico}'")
    
except Exception as e:
    print(f"\n❌ ERRO: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n=== FIM DO TESTE ===\n")
