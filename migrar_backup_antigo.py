"""
Script para migrar backup JSON de schema antigo para novo schema PostgreSQL.
Trata incompatibilidades de campos e conversões necessárias.
"""
import json
import sys
from pathlib import Path


# Mapeamentos de conversão
SITUACAO_ALUNO_MAP = {
    'ATIVO': 'a',
    'INATIVO': 'i',
    'SUSPENSO': 's',
    'ARQUIVADO': 'r',
    'FALECIDO': 'f',
    'EXCLUIDO': 'e',
    'a': 'a',  # já convertido
    'i': 'i',
    's': 's',
    'r': 'r',
    'f': 'f',
    'e': 'e',
}


def limpar_cpf(cpf):
    """Remove caracteres não numéricos e limita a 11 dígitos."""
    if not cpf:
        return ''
    import re
    apenas_numeros = re.sub(r'\D', '', str(cpf))
    return apenas_numeros[:11]


def converter_situacao_aluno(situacao):
    """Converte situação de texto completo para código de 1 caractere."""
    if not situacao:
        return 'a'
    return SITUACAO_ALUNO_MAP.get(situacao.upper() if isinstance(situacao, str) else situacao, 'a')


def migrar_aluno(fields):
    """Migra campos do modelo Aluno antigo para novo."""
    # Converter situacao
    if 'situacao' in fields:
        fields['situacao'] = converter_situacao_aluno(fields['situacao'])
    
    # Limpar CPF
    if 'cpf' in fields:
        fields['cpf'] = limpar_cpf(fields['cpf'])
    
    # Remover campos que não existem mais (se houver)
    campos_remover = []
    for campo in campos_remover:
        fields.pop(campo, None)
    
    return fields


def migrar_turma(fields):
    """Migra campos do modelo Turma antigo para novo."""
    # Campos que existiam no backup mas não existem no modelo atual
    campos_remover = [
        'encerrada_em',
        'encerrada_por',
        'bloqueio_total',
        'bloqueio_ativo_em',
        'bloqueio_ativo_por',
        'justificativa_reabertura',
    ]
    
    for campo in campos_remover:
        fields.pop(campo, None)
    
    return fields


def migrar_codigo(fields):
    """Migra campos do modelo Codigo antigo para novo."""
    # Adicionar campo ativo se não existir (padrão True)
    if 'ativo' not in fields:
        fields['ativo'] = True
    return fields


def migrar_tipocodigo(fields):
    """Migra campos do modelo TipoCodigo antigo para novo."""
    # Adicionar campo ativo se não existir (padrão True)
    if 'ativo' not in fields:
        fields['ativo'] = True
    return fields


def migrar_registro(registro):
    """Migra um registro individual baseado no seu model."""
    model = registro.get('model', '')
    fields = registro.get('fields', {})
    
    # Aplicar migração específica por modelo
    if model == 'alunos.aluno':
        fields = migrar_aluno(fields)
    elif model == 'turmas.turma':
        fields = migrar_turma(fields)
    elif model == 'alunos.codigo':
        fields = migrar_codigo(fields)
    elif model == 'alunos.tipocodigo':
        fields = migrar_tipocodigo(fields)
    
    registro['fields'] = fields
    return registro


def processar_backup(caminho_entrada, caminho_saida, excluir_models=None):
    """
    Processa arquivo de backup aplicando migrações.
    
    Args:
        caminho_entrada: Path do JSON original
        caminho_saida: Path do JSON migrado
        excluir_models: Lista de models a excluir (ex: ['auth.permission'])
    """
    if excluir_models is None:
        excluir_models = ['auth.permission', 'contenttypes.contenttype']
    
    print(f"[*] Lendo backup: {caminho_entrada}")
    with open(caminho_entrada, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    print(f"[*] Total de registros: {len(dados)}")
    
    # Filtrar models excluídos
    dados_filtrados = [
        reg for reg in dados 
        if reg.get('model') not in excluir_models
    ]
    print(f"[*] Após filtrar models: {len(dados_filtrados)}")
    
    # Migrar cada registro
    dados_migrados = []
    erros = []
    
    for i, registro in enumerate(dados_filtrados):
        try:
            registro_migrado = migrar_registro(registro)
            dados_migrados.append(registro_migrado)
        except Exception as e:
            erros.append((i, registro.get('model'), registro.get('pk'), str(e)))
            print(f"[!] Erro ao migrar {registro.get('model')}(pk={registro.get('pk')}): {e}")
    
    print(f"[*] Registros migrados com sucesso: {len(dados_migrados)}")
    
    if erros:
        print(f"\n[!] {len(erros)} erros encontrados:")
        for idx, model, pk, erro in erros[:10]:  # mostrar primeiros 10
            print(f"  - {model}(pk={pk}): {erro}")
    
    # Estatísticas por model
    models_count = {}
    for reg in dados_migrados:
        model = reg.get('model', 'unknown')
        models_count[model] = models_count.get(model, 0) + 1
    
    print("\n[*] Distribuição por model:")
    for model in sorted(models_count.keys()):
        print(f"  {model}: {models_count[model]}")
    
    # Salvar resultado
    print(f"\n[*] Salvando backup migrado: {caminho_saida}")
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(dados_migrados, f, ensure_ascii=False, indent=2)
    
    print(f"[✓] Migração concluída!")
    print(f"    Original: {len(dados)} registros")
    print(f"    Migrado: {len(dados_migrados)} registros")
    print(f"    Erros: {len(erros)}")
    
    return len(dados_migrados), len(erros)


if __name__ == '__main__':
    # Caminhos
    entrada = r"C:\Users\Ordem\OneDrive\10 PROJETOS\dev_data_20251126_090717.json"
    saida = r"C:\projetos\omaum\backup_migrado.json"
    
    # Verificar se arquivo existe
    if not Path(entrada).exists():
        print(f"[!] Arquivo não encontrado: {entrada}")
        sys.exit(1)
    
    # Processar
    total, erros = processar_backup(entrada, saida)
    
    if erros > 0:
        print(f"\n[!] Migração completou com {erros} erros.")
        print(f"[*] Revise os erros acima e ajuste as funções de migração se necessário.")
        sys.exit(1)
    else:
        print(f"\n[✓] Migração bem-sucedida sem erros!")
        print(f"\n[*] Para importar no PostgreSQL:")
        print(f"    docker cp {saida} omaum-web-prod:/app/backup_migrado.json")
        print(f"    docker exec omaum-web-prod python manage.py loaddata /app/backup_migrado.json")
        sys.exit(0)
