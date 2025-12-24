#!/usr/bin/env python
"""
Teste de integração: simula o envio do formulário POST com dados de presença
"""
import os
import sys
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from turmas.models import Turma
from presencas.models import RegistroPresenca
from atividades.models import Atividade

# ===== 1. PREPARAR DADOS =====
print("=" * 80)
print("🔍 ETAPA 1: Preparar dados de teste")
print("=" * 80)

turma = Turma.objects.get(id=32)
print(f"✅ Turma: {turma.nome} (ID: {turma.id})")

matriculas = turma.matriculas.filter(status='A')
print(f"👥 Matrículas ativas: {matriculas.count()}")

atividades = Atividade.objects.filter(turmas=turma)
print(f"📌 Atividades: {atividades.count()}")

# ===== 2. SIMULAR FORMULÁRIO POST =====
print("\n" + "=" * 80)
print("🌐 ETAPA 2: Simular envio do formulário POST")
print("=" * 80)

# Dados do formulário (como seriam enviados pelo formulário HTML)
form_data = {
    'csrfmiddlewaretoken': '',  # Será preenchido pelo cliente
}

# Selecionar primeira atividade e dia de teste
atividade = atividades.first()
dia_teste = 6
ano = 2025
mes = 12

# Adicionar presenças para cada aluno
for matricula in matriculas:
    cpf_aluno = matricula.aluno.cpf
    campo_presenca = f"presenca_{atividade.id}_{dia_teste}_{cpf_aluno}"
    form_data[campo_presenca] = "1"  # 1 = presente, 0 = ausente
    print(f"📝 Adicionado campo: {campo_presenca} = 1 (Presente)")

# Adicionar observação para o dia
campo_obs = f"obs_{atividade.id}_{dia_teste}"
form_data[campo_obs] = "Registro via teste automático"
print(f"📝 Adicionado campo: {campo_obs}")

# ===== 3. CONTAR ANTES =====
print("\n" + "=" * 80)
print("📊 ETAPA 3: Contagem ANTES de submeter")
print("=" * 80)

presencas_antes = RegistroPresenca.objects.filter(turma=turma).count()
print(f"Total de RegistroPresenca: {presencas_antes}")

# ===== 4. SUBMETER FORMULÁRIO =====
print("\n" + "=" * 80)
print("📤 ETAPA 4: Submeter formulário POST")
print("=" * 80)

# Criar cliente Django para testes
client = Client()

# Preparar URL POST
url_post = '/presencas/registrar-presenca-dias-atividades/'

print(f"URL: POST {url_post}")
print(f"Dados do formulário: {form_data}")

# Nota: Este teste não funcionará sem autenticação e sem estar em uma sessão Django válida
# O código abaixo é para ilustrar o processo

print("""
⚠️  AVISO: Este teste de POST não pode ser executado sem:
1. Autenticação de usuário
2. Session Django com dados de turma/ano/mês
3. CSRF token válido

Para testar o fluxo real, use a interface web ou Selenium.
""")

# ===== 5. RESUMO =====
print("\n" + "=" * 80)
print("✅ Teste de estrutura concluído!")
print("=" * 80)
print("""
Formato esperado dos campos do formulário:
  presenca_{atividade_id}_{dia}_{cpf_aluno}=1 (ou 0)
  justificativa_{atividade_id}_{dia}_{cpf_aluno}=texto (opcional)
  obs_{atividade_id}_{dia}=texto (opcional)

Exemplo para dia 6, atividade 46, aluno com CPF 12345678901:
  presenca_46_6_12345678901=1
  obs_46_6=Observação para o dia
""")
