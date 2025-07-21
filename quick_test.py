from alunos.models import Aluno
alunos = Aluno.objects.filter(matricula__turma_id=1, situacao='ATIVO').distinct()
print(f'Encontrados {alunos.count()} alunos na turma 1')
for aluno in alunos:
    print(f'- {aluno.nome} (CPF: {aluno.cpf})') 
