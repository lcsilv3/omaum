import os
import sys
import django
import random
import requests
from django.core.files.base import ContentFile
from django.db.models import Q

# --- Configuração do Ambiente Django ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()
# ----------------------------------------

from alunos.models import Aluno

# Lista de URLs de fotos aleatórias
FOTOS_MASCULINAS = [f"https://randomuser.me/api/portraits/men/{i}.jpg" for i in range(1, 51)]
FOTOS_FEMININAS = [f"https://randomuser.me/api/portraits/women/{i}.jpg" for i in range(1, 51)]

def preencher_fotos():
    """Preenche a foto para alunos ativos que não têm uma."""
    # Filtra alunos ativos que tem o campo foto nulo ou vazio
    alunos_sem_foto = Aluno.objects.filter(Q(foto__isnull=True) | Q(foto=''), ativo=True)
    
    if not alunos_sem_foto.exists():
        print("Todos os alunos ativos já possuem fotos.")
        return

    print(f"Encontrados {alunos_sem_foto.count()} alunos ativos sem foto. Iniciando o preenchimento...")

    for aluno in alunos_sem_foto:
        if aluno.sexo == 'F':
            url = random.choice(FOTOS_FEMININAS)
        else:
            url = random.choice(FOTOS_MASCULINAS)
        
        try:
            # Baixa a imagem
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Garante que o download foi bem-sucedido

            # Cria um nome de arquivo único
            nome_arquivo = f"aluno_{aluno.id}_{random.randint(1000, 9999)}.jpg"
            
            # Salva o arquivo usando o sistema de arquivos do Django
            aluno.foto.save(nome_arquivo, ContentFile(response.content), save=True)
            
            print(f"Aluno {aluno.id} - {aluno.nome}: Foto atribuída com sucesso.")

        except requests.RequestException as e:
            print(f"Erro de rede ao baixar foto para {aluno.nome}: {e}")
        except Exception as e:
            print(f"Erro inesperado ao processar {aluno.nome}: {e}")

if __name__ == "__main__":
    preencher_fotos()
