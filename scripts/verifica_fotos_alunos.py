from alunos.models import Aluno

print("Alunos com campo de foto preenchido:")
for aluno in Aluno.objects.filter(situacao="a").exclude(foto=""):
    print(f"ID: {aluno.id} | Nome: {aluno.nome} | Foto: {aluno.foto}")
    # Verifica se o arquivo existe fisicamente
    import os
    from django.conf import settings

    caminho = os.path.join(settings.MEDIA_ROOT, str(aluno.foto))
    print(f"  Caminho físico: {caminho} | Existe: {os.path.exists(caminho)}")
