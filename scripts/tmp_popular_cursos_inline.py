from cursos.models import Curso

cursos = [
    {"nome": "Pré-Iniciático", "descricao": "Pré-Iniciático"},
    {"nome": "1º Grau", "descricao": "1º Grau"},
    {"nome": "2º Grau", "descricao": "2º Grau"},
    {"nome": "3º Grau", "descricao": "3º Grau"},
    {"nome": "4º Grau", "descricao": "4º Grau"},
    {"nome": "5º Grau", "descricao": "5º Grau"},
    {"nome": "Coleginho", "descricao": "Coleginho"},
    {"nome": "Colégio Sacerdotal", "descricao": "Colégio Sacerdotal"},
]

print("Iniciando população de cursos...")
for c in cursos:
    obj, created = Curso.objects.get_or_create(
        nome=c["nome"], defaults={"descricao": c["descricao"], "ativo": True}
    )
    status = "criado" if created else "já existe"
    print(f"Curso '{obj.nome}' {status}")

print(f"\nTotal de cursos no banco: {Curso.objects.count()}")
