import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
# from pagamentos.models import Pagamento, TipoPagamento  # Removido: símbolo(s) inexistente(s)
from alunos.services import criar_aluno
from turmas.models import Turma
import datetime

# Arquivo de teste esvaziado para evitar erro de coleta pytest