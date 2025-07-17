#!/usr/bin/env python
"""
Script para criar dados de teste completos para validar a otimização da seção Dados Iniciáticos.
"""

import os
import django
from datetime import date

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from alunos.models import Aluno, TipoCodigo, Codigo


def criar_dados_teste():
    """Cria dados de teste completos."""
    print("=== Criando dados de teste ===")
    
    # 1. Criar TipoCodigo
    tipo_cargo, _ = TipoCodigo.objects.get_or_create(
        nome="Cargo",
        defaults={"descricao": "Cargos iniciáticos"}
    )
    
    tipo_iniciacao, _ = TipoCodigo.objects.get_or_create(
        nome="Iniciação",
        defaults={"descricao": "Registros de iniciação"}
    )
    
    tipo_punicao, _ = TipoCodigo.objects.get_or_create(
        nome="Punição",
        defaults={"descricao": "Registros disciplinares"}
    )
    
    print(f"Tipos de código criados: {TipoCodigo.objects.count()}")
    
    # 2. Criar Códigos
    codigos_cargo = ["Mestre", "Instrutor", "Aprendiz", "Diácono", "Secretário"]
    for codigo_nome in codigos_cargo:
        Codigo.objects.get_or_create(
            nome=codigo_nome,
            tipo_codigo=tipo_cargo,
            defaults={"descricao": f"Cargo de {codigo_nome}"}
        )
    
    codigos_iniciacao = ["Iniciação", "Elevação", "Exaltação", "Instalação"]
    for codigo_nome in codigos_iniciacao:
        Codigo.objects.get_or_create(
            nome=codigo_nome,
            tipo_codigo=tipo_iniciacao,
            defaults={"descricao": f"Cerimônia de {codigo_nome}"}
        )
    
    codigos_punicao = ["Advertência", "Suspensão", "Exclusão", "Reabilitação"]
    for codigo_nome in codigos_punicao:
        Codigo.objects.get_or_create(
            nome=codigo_nome,
            tipo_codigo=tipo_punicao,
            defaults={"descricao": f"Punição: {codigo_nome}"}
        )
    
    print(f"Códigos criados: {Codigo.objects.count()}")
    
    # 3. Criar ou atualizar aluno
    aluno, created = Aluno.objects.get_or_create(
        cpf="12345678900",
        defaults={
            "nome": "João da Silva",
            "email": "joao@example.com",
            "data_nascimento": date(1990, 1, 1),
            "sexo": "M",
            "situacao": "ATIVO",
            "ativo": True,
            "numero_iniciatico": "123456",
            "nome_iniciatico": "João dos Santos",
            "grau_atual": "Aprendiz",
            "situacao_iniciatica": "INICIADO",
            "historico_iniciatico": []
        }
    )
    
    if created:
        print(f"Aluno criado: {aluno.nome} - CPF: {aluno.cpf}")
    else:
        print(f"Aluno já existe: {aluno.nome} - CPF: {aluno.cpf}")
    
    # 4. Adicionar eventos ao histórico
    if not aluno.historico_iniciatico:
        aluno.adicionar_evento_historico(
            tipo="Iniciação",
            descricao="Iniciação no Grau de Aprendiz",
            data=date(2020, 1, 15),
            observacoes="Primeira iniciação do candidato",
            ordem_servico="OS-001/2020"
        )
        
        aluno.adicionar_evento_historico(
            tipo="Cargo",
            descricao="Nomeação para Diácono",
            data=date(2021, 6, 10),
            observacoes="Cargo exercido com dedicação",
            ordem_servico="OS-025/2021"
        )
        
        print("Eventos adicionados ao histórico")
    
    print("\n=== Dados de teste criados com sucesso ===")
    print(f"Total de alunos: {Aluno.objects.count()}")
    print(f"Total de tipos de código: {TipoCodigo.objects.count()}")
    print(f"Total de códigos: {Codigo.objects.count()}")


if __name__ == "__main__":
    criar_dados_teste()
