import os
import random
import urllib.request
from alunos.models import Aluno
from django.conf import settings

# Lista de URLs de fotos aleatórias (pode ser expandida)
FOTOS = [
    "https://randomuser.me/api/portraits/men/1.jpg",
    "https://randomuser.me/api/portraits/women/2.jpg",
    "https://randomuser.me/api/portraits/men/3.jpg",
    "https://randomuser.me/api/portraits/women/4.jpg",
    "https://randomuser.me/api/portraits/men/5.jpg",
    "https://randomuser.me/api/portraits/women/6.jpg",
    "https://randomuser.me/api/portraits/men/7.jpg",
    "https://randomuser.me/api/portraits/women/8.jpg",
]

media_dir = settings.MEDIA_ROOT
subdir = "fotos_alunos"
os.makedirs(os.path.join(media_dir, subdir), exist_ok=True)

alunos = Aluno.objects.filter(ativo=True)
for aluno in alunos:
    url = random.choice(FOTOS)
    ext = url.split(".")[-1]
    nome_arquivo = f"aluno_{aluno.id}.{ext}"
    caminho_arquivo = os.path.join(subdir, nome_arquivo)
    caminho_fisico = os.path.join(media_dir, caminho_arquivo)
    try:
        urllib.request.urlretrieve(url, caminho_fisico)
        aluno.foto = caminho_arquivo
        aluno.save()
        print(f"Aluno {aluno.id} - {aluno.nome}: Foto atribuída ({url})")
    except Exception as e:
        print(f"Erro ao baixar foto para {aluno.nome}: {e}")
