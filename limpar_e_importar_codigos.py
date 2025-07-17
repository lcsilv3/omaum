#!/usr/bin/env python
"""Script para limpar e popular a tabela Codigo."""

import os
import csv
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from alunos.models import Codigo, TipoCodigo


def limpar_tabela():
    """Limpa todos os registros da tabela Codigo."""
    print("🧹 Limpando a tabela Codigo...")
    count = Codigo.objects.count()
    print(f"📊 Registros encontrados: {count}")
    
    if count > 0:
        Codigo.objects.all().delete()
        print("✅ Tabela limpa com sucesso!")
    else:
        print("ℹ️  Tabela já estava vazia.")


def obter_tipos_codigo():
    """Obtém todos os tipos de código disponíveis."""
    print("\n🔍 Verificando tipos de código disponíveis...")
    tipos = {}
    
    for tipo in TipoCodigo.objects.all():
        tipos[tipo.nome] = tipo
        print(f"  • {tipo.nome}: {tipo.descricao}")
    
    return tipos


def importar_csv():
    """Importa dados do arquivo CSV para a tabela Codigo."""
    print("\n📥 Importando dados do CSV...")
    
    csv_file = 'codigos.csv'
    if not os.path.exists(csv_file):
        print(f"❌ Arquivo {csv_file} não encontrado!")
        return False
    
    # Obter tipos de código
    tipos_codigo = obter_tipos_codigo()
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            erros = 0
            
            for row_num, row in enumerate(reader, 1):
                try:
                    # Buscar o tipo de código
                    tipo_nome = row['tipo']
                    
                    if tipo_nome not in tipos_codigo:
                        print(f"⚠️  Linha {row_num}: Tipo '{tipo_nome}' não encontrado!")
                        erros += 1
                        continue
                    
                    # Criar o código
                    codigo = Codigo.objects.create(
                        nome=row['nome'],
                        tipo_codigo=tipos_codigo[tipo_nome],
                        descricao=row['descricao']
                    )
                    
                    if count % 50 == 0:  # Mostrar progresso a cada 50 registros
                        print(f"📊 Processados {count} registros...")
                    
                    count += 1
                    
                except Exception as e:
                    print(f"❌ Erro na linha {row_num}: {e}")
                    erros += 1
            
            print(f"\n📊 Importação concluída:")
            print(f"  • Total de registros importados: {count}")
            print(f"  • Total de erros: {erros}")
            
            return erros == 0
            
    except Exception as e:
        print(f"❌ Erro ao importar CSV: {e}")
        return False


def verificar_dados():
    """Verifica os dados importados."""
    print("\n🔍 Verificando dados importados...")
    codigos = Codigo.objects.all()
    
    if not codigos.exists():
        print("⚠️  Nenhum registro encontrado!")
        return
    
    print(f"📊 Total de registros: {codigos.count()}")
    
    # Agrupar por tipo
    tipos_count = {}
    for codigo in codigos:
        tipo_nome = codigo.tipo_codigo.nome
        if tipo_nome not in tipos_count:
            tipos_count[tipo_nome] = 0
        tipos_count[tipo_nome] += 1
    
    print("\n📋 Registros por tipo:")
    for tipo, count in tipos_count.items():
        print(f"  • {tipo}: {count} códigos")
    
    # Mostrar alguns exemplos
    print("\n📝 Exemplos de registros:")
    for codigo in codigos[:5]:
        print(f"  • {codigo.nome} ({codigo.tipo_codigo.nome}): {codigo.descricao[:50]}...")


def validar_integridade():
    """Valida a integridade dos dados."""
    print("\n🔍 Validando integridade dos dados...")
    
    # Verificar registros duplicados
    codigos_duplicados = Codigo.objects.values('nome').annotate(
        count=models.Count('nome')
    ).filter(count__gt=1)
    
    if codigos_duplicados.exists():
        print("⚠️  Códigos duplicados encontrados:")
        for dup in codigos_duplicados:
            print(f"  • {dup['nome']}: {dup['count']} ocorrências")
    else:
        print("✅ Nenhum código duplicado encontrado!")
    
    # Verificar integridade referencial
    codigos_sem_tipo = Codigo.objects.filter(tipo_codigo__isnull=True)
    if codigos_sem_tipo.exists():
        print(f"⚠️  {codigos_sem_tipo.count()} códigos sem tipo encontrados!")
    else:
        print("✅ Integridade referencial validada!")


if __name__ == "__main__":
    print("🚀 Iniciando processo de limpeza e importação da tabela Codigo")
    print("=" * 70)
    
    # Etapa 1: Limpar tabela
    limpar_tabela()
    
    # Etapa 2: Importar CSV
    if importar_csv():
        # Etapa 3: Verificar dados
        verificar_dados()
        
        # Etapa 4: Validar integridade
        # Importar Count para validação
        from django.db import models
        validar_integridade()
        
        print("\n✅ Processo concluído com sucesso!")
    else:
        print("\n❌ Processo falhou durante a importação!")
