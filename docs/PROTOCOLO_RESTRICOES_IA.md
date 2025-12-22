# 🚫 PROTOCOLO DE RESTRIÇÕES PARA IA - PROJETO OMAUM

## Status: CRÍTICO ⚠️

**Data:** 21 de dezembro de 2025  
**Situação:** Erros graves foram cometidos na remoção de modelos sem análise adequada.

---

## 🔴 ERRO COMETIDO

A IA removeu imports de `TotalAtividadeMes` e `ObservacaoPresenca` em 5 arquivos **SEM VERIFICAR** que esses modelos ainda estavam sendo usados ativamente em **20+ outros arquivos**.

### Arquivos que foram "corrigidos" mas na verdade quebrados:
1. `presencas/serializers.py` - Removido import (classe ainda precisa dele!)
2. `presencas/repositories.py` - Removido import + deletou `ObservacaoPresencaRepository` (CLASSE ATIVA!)
3. `presencas/views_ext/registro_presenca.py` - Removido import (view usa ObservacaoPresenca em linhas 333, 388, 1160!)
4. `presencas/views_new.py` - Removido imports de AMBOS modelos
5. `presencas/services.py` - Removido imports de AMBOS modelos (get_presenca_models() retorna referências!)

### Funcionalidades QUEBRADAS:
- ❌ Criação de observações de presença em `presencas/views.py` linha 113
- ❌ Criação de observações em `presencas/views_ext/registro_presenca.py` linhas 333, 388, 1160
- ❌ Criação de observações em `presencas/views_new.py` linha 102
- ❌ Registro de totais de atividades em `presencas/views_ext/registro_presenca.py` linha 179
- ❌ Atualização de totais em `presencas/views_new.py` linha 272
- ❌ Repositório de observações em `presencas/repositories.py` linhas 294-320
- ❌ Serialização de observações em `presencas/serializers.py` linhas 10-16
- ❌ Busca de observações em `presencas/services.py` linhas 387-390, 424-426
- ❌ Scripts de debug: `scripts/debug/debug_sessao_completa.py`, `debug_banco_estado.py`
- ❌ Operações em lote: `presencas/bulk_operations.py` linhas 128, 168, 196
- ❌ API Views: `presencas/api_views.py` linha 25
- ❌ Views de registro rápido: `presencas/views/registro_rapido.py` linhas 17, 269

---

## 📋 PROTOCOLO OBRIGATÓRIO PARA QUALQUER ALTERAÇÃO FUTURA

### ✅ ANTES DE FAZER QUALQUER MODIFICAÇÃO, VOCÊ DEVE:

#### 1. PROCURAR TODAS AS REFERÊNCIAS (OBRIGATÓRIO)
```bash
# Se vai remover um modelo, função ou classe:
grep -r "NomeDaClasse\|NomeDaFuncao" --include="*.py" e:\projetos\omaum\
grep -r "from .models import NomeDaClasse" --include="*.py" e:\projetos\omaum\
```

#### 2. CONTAR E DOCUMENTAR AS DEPENDÊNCIAS
- Quantos arquivos importam essa classe?
- Quantos arquivos **USAM** essa classe?
- Qual é a diferença? (Se houver, importações obsoletas podem ser removidas com cuidado)

#### 3. VERIFICAR O CONTEXTO DE NEGÓCIO
- Ler código em torno de **CADA USO** (não apenas o import)
- Entender **POR QUÊ** aquela classe é usada
- Procurar em:
  - Services (`**/services.py`)
  - Views (`**/views.py`, `**/views_*.py`)
  - Serializers (`**/serializers.py`)
  - Repositories (`**/repositories.py`)
  - Testes (`**/test_*.py`)
  - Bulk operations (`**/bulk_operations.py`)
  - API Views (`**/api_views.py`)
  - Scripts de debug (`scripts/debug/*.py`)

#### 4. PROCURAR POR TESTES QUE USAM A CLASSE
```bash
grep -r "NomeDaClasse" --include="test_*.py" e:\projetos\omaum\
grep -r "NomeDaClasse" --include="*test.py" e:\projetos\omaum\
```

#### 5. PROCURAR NO HISTÓRICO DE GIT
```bash
git log --all --oneline -S "NomeDaClasse" -- e:\projetos\omaum\
git log --all -p --grep="NomeDaClasse"
git blame <arquivo> | grep "NomeDaClasse"
```

**Perguntas a responder:**
- Quando foi adicionada? (git log)
- Quando foi modificada pela última vez? (git blame)
- Há commits que mencionam exclusão dela?
- Há PRs ou issues associadas?

#### 6. CONFERIR MIGRAÇÕES DO BANCO
```bash
grep -r "NomeDaClasse\|nome_da_tabela" --include="*.py" presencas/migrations/
```

Se a classe está em uma migração, ela pode estar no banco de dados ainda!

#### 7. CONVERSA COM O USUÁRIO ANTES DE AGIR
**NUNCA remova ou altere:**
- Models
- Classes de serializer/repository
- Imports de vistas
- Funcionalidades de negócio

**SEMPRE peça aprovação:**
> "Encontrei a classe XYZ que precisa ser removida. Ela está sendo usada em [LISTA DE ARQUIVOS]. Encontrei [N] dependências ativas e [N] testes. Sugiro:
> 1. [OPÇÃO A]
> 2. [OPÇÃO B]
> 
> Qual você prefere?"

#### 8. SE REMOVER, CERTIFIQUE-SE:
- ✅ Todas as importações foram removidas
- ✅ Todas as dependências foram tratadas
- ✅ Todos os testes passam
- ✅ Nenhuma funcionalidade foi quebrada
- ✅ O banco foi migrado (se modelo foi removido)

---

## 🔒 REGRAS DE OURO (NÃO NEGOCIA!)

### ❌ VOCÊ NÃO PODE:
1. ❌ Remover um modelo sem verificar todas as views/services/serializers
2. ❌ Remover um import sem verificar se a classe é usada em outra parte do arquivo
3. ❌ Deletar uma classe (Serializer, Repository, etc.) sem saber para quê ela servia
4. ❌ Fazer alterações em modelos sem consultar histórico de git
5. ❌ Modificar código de negócio (presencas, atividades, turmas, etc.) sem aprovação
6. ❌ Restaurar um banco ou fazer reset sem alertar o usuário

### ✅ VOCÊ DEVE:
1. ✅ SEMPRE buscar por todas as referências antes de remover
2. ✅ SEMPRE ler o código que usa a coisa que você quer remover
3. ✅ SEMPRE perguntar ao usuário se não tiver certeza
4. ✅ SEMPRE fazer isso em uma PR separada (com descrição detalhada)
5. ✅ SEMPRE rodar testes antes de commitar
6. ✅ SEMPRE alertar o usuário sobre mudanças em produção

---

## 📊 CHECKLIST PARA REMOÇÃO DE CLASSE/MODELO

Antes de remover QUALQUER coisa, preencha isto:

```
[ ] Busquei todas as referências com grep?
[ ] Contei quantos arquivos usam isso?
[ ] Li o código em cada lugar que usa?
[ ] Procurei em testes?
[ ] Procurei em migrations?
[ ] Verifiquei histórico de git?
[ ] Documentei TUDO num documento?
[ ] Pedi aprovação ao usuário?
[ ] Criei uma PR descrevendo a mudança?
[ ] Rodei testes?
[ ] Nenhuma funcionalidade ficou quebrada?
```

Se qualquer item for ❌, **NÃO FAÇA A REMOÇÃO**.

---

## 🔧 COMO RECUPERAR DO ERRO

O erro cometido foi:
1. Remover imports de modelos sem verificar dependências
2. Remover classes (Repository, Serializer) que ainda eram necessárias

**Para recuperar:**
```bash
# Restaurar os arquivos deletados:
git checkout HEAD -- presencas/serializers.py presencas/repositories.py presencas/views_ext/registro_presenca.py presencas/views_new.py presencas/services.py

# Verificar status:
git status

# Restartar containers:
docker compose -p omaum-dev restart omaum-web
docker compose -p omaum-prod restart omaum-web
```

---

## 📝 APLICAÇÃO IMEDIATA

**ESTA RESTRIÇÃO ENTRA EM VIGOR AGORA.**

Para TODA e QUALQUER alteração de código neste projeto, a IA DEVE:

1. Antes de qualquer `replace_string_in_file` ou `multi_replace_string_in_file`:
   - Fazer uma busca completa por referências
   - Documentar os achados
   - Apresentar ao usuário

2. Antes de remover imports:
   - Verificar se a classe é usada naquele arquivo
   - Procurar em ALL arquivos do projeto

3. Antes de deletar classes:
   - Certeza de 100% que não está sendo usada
   - Procurar testes
   - Procurar em migrations

4. NUNCA fazer alterações de negócio sem aprovação explícita

---

## 📞 CONTATO

Se tiver dúvidas sobre este protocolo, o usuário estará disponível para:
- Esclarecer intenções de mudanças
- Revisar análises antes de aplicação
- Aprovar/rejeitar modificações

---

**Status:** Este documento é vinculante e obrigatório.  
**Revisão:** Será atualizado conforme necessário.  
**Assinado (digitalmente):** Análise de IA realizada em 21 de dezembro de 2025.

