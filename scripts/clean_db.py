import os
import sys
import django

# Configuração do ambiente Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from alunos.models import Aluno, RegistroHistorico
from turmas.models import Turma
from atividades.models import Atividade
from notas.models import Nota
from presencas.models import Presenca
from pagamentos.models import Pagamento
from matriculas.models import Matricula

print("Iniciando limpeza do banco de dados de teste (dados transacionais)...")

# A ordem é importante para evitar erros de restrição de chave estrangeira
# Cursos, Códigos e Tipos de Código não são apagados para preservar dados base.
Matricula.objects.all().delete()
Presenca.objects.all().delete()
Nota.objects.all().delete()
Pagamento.objects.all().delete()
RegistroHistorico.objects.all().delete()
Atividade.objects.all().delete()
Aluno.objects.all().delete()
Turma.objects.all().delete()

print("Limpeza de dados transacionais concluída.")
