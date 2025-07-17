"""
Script de migração para transferir dados dos modelos antigos para o novo sistema JSONField.
Este script irá:
1. Migrar dados de TipoCodigo -> Codigo -> RegistroHistorico para o JSONField historico_iniciatico
2. Consolidar informações iniciáticas em campos diretos do Aluno
3. Preservar todos os dados históricos existentes
"""

import json
import os
import sys
from datetime import datetime

# Configuração do Django
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')

import django
django.setup()

from django.db import transaction
from alunos.models import Aluno, TipoCodigo, Codigo, RegistroHistorico


def migrar_dados_iniciaticos():
    """
    Migra dados do sistema antigo (4 tabelas) para o novo sistema (JSONField).
    """
    print("=== INICIANDO MIGRAÇÃO DE DADOS INICIÁTICOS ===")
    print(f"Timestamp: {datetime.now()}")
    
    total_alunos = Aluno.objects.count()
    migrados = 0
    erros = 0
    
    print(f"\nTotal de alunos para migrar: {total_alunos}")
    
    for aluno in Aluno.objects.all():
        try:
            with transaction.atomic():
                # Obter todos os registros históricos do aluno
                registros = RegistroHistorico.objects.filter(aluno=aluno).select_related(
                    'codigo', 'codigo__tipo_codigo'
                ).order_by('data_os')
                
                historico_eventos = []
                
                # Processar cada registro histórico
                for registro in registros:
                    evento = {
                        'id': len(historico_eventos) + 1,
                        'tipo': registro.codigo.tipo_codigo.nome if registro.codigo and registro.codigo.tipo_codigo else 'INDEFINIDO',
                        'descricao': registro.codigo.nome if registro.codigo else 'Sem descrição',
                        'data': registro.data_os.isoformat() if registro.data_os else None,
                        'observacoes': registro.observacoes or '',
                        'numero_iniciatico': registro.numero_iniciatico or '',
                        'nome_iniciatico': registro.nome_iniciatico or '',
                        'ordem_servico': registro.ordem_servico or '',
                        'migrado_de': f'RegistroHistorico ID: {registro.id}',
                        'data_criacao': datetime.now().isoformat()
                    }
                    historico_eventos.append(evento)
                
                # Atualizar campos do aluno
                aluno.historico_iniciatico = historico_eventos
                
                # Definir dados iniciáticos baseados no histórico
                if historico_eventos:
                    ultimo_evento = max(historico_eventos, key=lambda x: x['data'] or '1900-01-01')
                    
                    # Definir grau atual baseado no último evento
                    if ultimo_evento.get('nome_iniciatico'):
                        aluno.grau_atual = ultimo_evento['nome_iniciatico']
                    elif ultimo_evento.get('descricao'):
                        aluno.grau_atual = ultimo_evento['descricao']
                    else:
                        aluno.grau_atual = 'A definir'
                    
                    # Definir número e nome iniciático
                    if ultimo_evento.get('numero_iniciatico'):
                        aluno.numero_iniciatico = ultimo_evento['numero_iniciatico']
                    if ultimo_evento.get('nome_iniciatico'):
                        aluno.nome_iniciatico = ultimo_evento['nome_iniciatico']
                    
                    # Definir data de iniciação (primeiro evento de iniciação)
                    eventos_iniciacao = [e for e in historico_eventos if 'INICIAÇÃO' in e['tipo'].upper()]
                    if eventos_iniciacao:
                        primeiro_evento = min(eventos_iniciacao, key=lambda x: x['data'] or '9999-12-31')
                        if primeiro_evento['data']:
                            aluno.data_iniciacao = datetime.fromisoformat(primeiro_evento['data']).date()
                    
                    # Definir situação iniciática
                    tipos_evento = [e['tipo'].upper() for e in historico_eventos]
                    if any('PUNIÇÃO' in t or 'SUSPENSÃO' in t for t in tipos_evento):
                        aluno.situacao_iniciatica = 'SUSPENSA'
                    elif any('INICIAÇÃO' in t for t in tipos_evento):
                        aluno.situacao_iniciatica = 'ATIVA'
                    else:
                        aluno.situacao_iniciatica = 'INDEFINIDA'
                else:
                    # Aluno sem histórico
                    aluno.situacao_iniciatica = 'INDEFINIDA'
                    aluno.grau_atual = 'A definir'
                
                # Salvar aluno
                aluno.save()
                migrados += 1
                
                print(f"✓ Migrado: {aluno.nome} - {len(historico_eventos)} eventos")
                
        except Exception as e:
            erros += 1
            print(f"✗ Erro ao migrar {aluno.nome}: {str(e)}")
    
    print(f"\n=== RESUMO DA MIGRAÇÃO ===")
    print(f"Total de alunos: {total_alunos}")
    print(f"Migrados com sucesso: {migrados}")
    print(f"Erros: {erros}")
    print(f"Taxa de sucesso: {(migrados/total_alunos)*100:.1f}%")
    
    return migrados, erros


def criar_backup_dados():
    """
    Cria backup dos dados antes da migração.
    """
    print("\n=== CRIANDO BACKUP DOS DADOS ===")
    
    backup_data = {
        'timestamp': datetime.now().isoformat(),
        'alunos': [],
        'tipos_codigo': [],
        'codigos': [],
        'registros_historico': []
    }
    
    # Backup dos alunos
    for aluno in Aluno.objects.all():
        backup_data['alunos'].append({
            'cpf': aluno.cpf,
            'nome': aluno.nome,
            'email': getattr(aluno, 'email', None),
            'numero_iniciatico': getattr(aluno, 'numero_iniciatico', None),
            'nome_iniciatico': getattr(aluno, 'nome_iniciatico', None),
            'ativo': aluno.ativo
        })
    
    # Backup dos tipos de código
    for tipo in TipoCodigo.objects.all():
        backup_data['tipos_codigo'].append({
            'id': tipo.id,
            'nome': tipo.nome,
            'descricao': tipo.descricao
        })
    
    # Backup dos códigos
    for codigo in Codigo.objects.all():
        backup_data['codigos'].append({
            'id': codigo.id,
            'nome': codigo.nome,
            'tipo_codigo_id': codigo.tipo_codigo_id,
            'tipo_codigo_nome': codigo.tipo_codigo.nome if codigo.tipo_codigo else None
        })
    
                # Backup dos registros históricos
        for registro in RegistroHistorico.objects.all():
            backup_data['registros_historico'].append({
                'id': registro.pk,
                'aluno_cpf': registro.aluno.cpf if registro.aluno else None,
                'codigo_id': registro.codigo.pk if registro.codigo else None,
                'data_os': registro.data_os.isoformat() if registro.data_os else None,
                'ordem_servico': getattr(registro, 'ordem_servico', None),
                'numero_iniciatico': getattr(registro, 'numero_iniciatico', None),
                'nome_iniciatico': getattr(registro, 'nome_iniciatico', None),
                'observacoes': getattr(registro, 'observacoes', None)
            })
    
    # Salvar backup
    backup_filename = f'backup_dados_iniciaticos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(backup_filename, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Backup criado: {backup_filename}")
    print(f"  - Alunos: {len(backup_data['alunos'])}")
    print(f"  - Tipos de código: {len(backup_data['tipos_codigo'])}")
    print(f"  - Códigos: {len(backup_data['codigos'])}")
    print(f"  - Registros históricos: {len(backup_data['registros_historico'])}")
    
    return backup_filename


def verificar_integridade_migracao():
    """
    Verifica se a migração foi bem-sucedida.
    """
    print("\n=== VERIFICANDO INTEGRIDADE DA MIGRAÇÃO ===")
    
    alunos_com_historico = 0
    alunos_sem_historico = 0
    total_eventos = 0
    
    for aluno in Aluno.objects.all():
        historico = aluno.obter_historico_ordenado()
        if historico:
            alunos_com_historico += 1
            total_eventos += len(historico)
        else:
            alunos_sem_historico += 1
    
    print(f"✓ Alunos com histórico: {alunos_com_historico}")
    print(f"✓ Alunos sem histórico: {alunos_sem_historico}")
    print(f"✓ Total de eventos migrados: {total_eventos}")
    
    # Verificar se o total de eventos bate com o total de registros antigos
    total_registros_antigos = RegistroHistorico.objects.count()
    print(f"✓ Total de registros antigos: {total_registros_antigos}")
    
    if total_eventos == total_registros_antigos:
        print("✅ MIGRAÇÃO VERIFICADA COM SUCESSO!")
    else:
        print("⚠️  ATENÇÃO: Número de eventos não confere com registros antigos")
    
    return alunos_com_historico, alunos_sem_historico, total_eventos


def main():
    """
    Função principal para executar a migração.
    """
    print("SISTEMA DE MIGRAÇÃO DE DADOS INICIÁTICOS")
    print("=" * 50)
    
    # Criar backup antes da migração
    backup_filename = criar_backup_dados()
    
    # Executar migração
    migrados, erros = migrar_dados_iniciaticos()
    
    # Verificar integridade
    verificar_integridade_migracao()
    
    print(f"\n=== MIGRAÇÃO CONCLUÍDA ===")
    print(f"Backup salvo em: {backup_filename}")
    print(f"Alunos migrados: {migrados}")
    print(f"Erros encontrados: {erros}")
    
    if erros == 0:
        print("✅ MIGRAÇÃO EXECUTADA COM SUCESSO!")
    else:
        print("⚠️  MIGRAÇÃO CONCLUÍDA COM ALGUNS ERROS - VERIFIQUE OS LOGS")


if __name__ == "__main__":
    main()
