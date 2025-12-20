# Correções Necessárias em Desenvolvimento para Próximo Deploy

**Data de Análise**: 27 de novembro de 2025  
**Ambiente**: Desenvolvimento Local  
**Destino**: Produção (Docker)

---

## 🔴 PROBLEMAS CRÍTICOS IDENTIFICADOS

### 1. **Modelo Turma - Campos Extras em Desenvolvimento**

**Status**: ❌ INCOMPATÍVEL com produção  
**Impacto**: ALTO - Causa falha na importação de fixtures

#### Campos Presentes em Dev mas NÃO em Prod:

| Campo | Tipo | Linha | Ação Necessária |
|-------|------|-------|-----------------|
| `instrutor` | ForeignKey | 86 | ✅ MANTER (adicionar em prod) OU ❌ REMOVER |
| `instrutor_auxiliar` | ForeignKey | 93 | ✅ MANTER (adicionar em prod) OU ❌ REMOVER |
| `auxiliar_instrucao` | ForeignKey | 100 | ✅ MANTER (adicionar em prod) OU ❌ REMOVER |
| `alerta_instrutor` | BooleanField | 109 | ✅ MANTER (adicionar em prod) OU ❌ REMOVER |
| `alerta_mensagem` | TextField | 112 | ✅ MANTER (adicionar em prod) OU ❌ REMOVER |

**Arquivo**: `turmas/models.py`

#### Solução A: Sincronizar Produção (RECOMENDADO se os campos são úteis)

```python
# Criar migração em dev
python manage.py makemigrations turmas -n adiciona_campos_instrutor

# Aplicar em prod
docker exec omaum-web-prod python manage.py migrate turmas

# Commit
git add turmas/migrations/
git commit -m "feat(turmas): adiciona campos de instrutor e alertas"
```

#### Solução B: Remover de Desenvolvimento (se não são necessários)

```python
# Remover campos de turmas/models.py (linhas 86-113)
# Criar migração
python manage.py makemigrations turmas -n remove_campos_instrutor

# Aplicar localmente
python manage.py migrate
```

---

### 2. **Modelo Aluno - Campo situacao_iniciatica com Tipo Incompatível**

**Status**: ⚠️ PARCIALMENTE INCOMPATÍVEL  
**Impacto**: MÉDIO - Dados exportados incorretamente

#### Problema Atual:

```python
# Em desenvolvimento (alunos/models.py linha ~370)
situacao_iniciatica = models.CharField(
    max_length=20,  # ❌ ERRADO: aceita texto completo
    default="a",
    choices=SITUACAO_CHOICES,
    verbose_name=_("Situação Iniciática"),
)
```

**Dados exportados**: `"ATIVO"`, `"INATIVO"`, `"EXONERADO"` (texto completo)  
**Esperado em prod**: `"A"`, `"I"`, `"E"` (1 caractere)

#### Solução:

```python
# Corrigir em alunos/models.py
situacao_iniciatica = models.CharField(
    max_length=1,  # ✅ CORRETO: apenas 1 caractere
    default="I",   # ✅ Maiúscula para diferencial de situacao
    choices=[
        ("A", "Ativo"),
        ("I", "Inativo"),
        ("E", "Exonerado"),
        ("D", "Desligado"),
    ],
    verbose_name=_("Situação Iniciática"),
)

# Criar migração
python manage.py makemigrations alunos -n corrige_tamanho_situacao_iniciatica

# Aplicar
python manage.py migrate
```

---

### 3. **Fixture Export - Inclui Dados Auto-Gerados**

**Status**: ❌ ERRO de processo  
**Impacto**: ALTO - Causa conflitos de chave única

#### Problema:

Comando atual de export inclui `auth.permission` e `contenttypes.contenttype`:

```bash
python manage.py dumpdata --indent 2 -o dev_data.json
```

Resultado: 170 registros extras causando `IntegrityError` na importação.

#### Solução:

```bash
# Sempre excluir estes models no export
python manage.py dumpdata \
    --natural-foreign \
    --natural-primary \
    --indent 2 \
    --exclude sessions \
    --exclude admin.logentry \
    --exclude auth.permission \
    --exclude contenttypes.contenttype \
    -o dev_data_$(date +%Y%m%d_%H%M%S).json
```

**Criar alias/script permanente**: `scripts/exportar_fixtures.sh`

---

## ⚠️ PROBLEMAS DE CONFIGURAÇÃO

### 4. **Inconsistência de Choices entre Modelos**

**Status**: ⚠️ DESIGN inconsistente  
**Impacto**: BAIXO - Confusão entre desenvolvedores

#### Problema:

```python
# Aluno.situacao (linha ~210)
SITUACAO_CHOICES = [
    ("a", "Ativo"),      # ✅ Minúscula
    ("i", "Inativo"),
    ("s", "Suspenso"),
    ("t", "Trancado"),
]

# Aluno.situacao_iniciatica (linha ~370)
# Usa mesma SITUACAO_CHOICES mas deveria ter própria
# Resultado: códigos minúsculos quando deveriam ser MAIÚSCULOS
```

#### Solução:

```python
# Criar choices separadas em alunos/models.py
SITUACAO_ALUNO_CHOICES = [
    ("a", "Ativo"),
    ("i", "Inativo"),
    ("s", "Suspenso"),
    ("t", "Trancado"),
]

SITUACAO_INICIATICA_CHOICES = [
    ("A", "Ativo"),      # ✅ Maiúscula para diferenciação
    ("I", "Inativo"),
    ("E", "Exonerado"),
    ("D", "Desligado"),
]

# Atualizar campos
situacao = models.CharField(
    max_length=1,
    choices=SITUACAO_ALUNO_CHOICES,  # ✅
    default="a",
    verbose_name="Situação do Aluno",
)

situacao_iniciatica = models.CharField(
    max_length=1,                          # ✅ Corrigido
    choices=SITUACAO_INICIATICA_CHOICES,   # ✅
    default="I",
    verbose_name=_("Situação Iniciática"),
)
```

---

## 📋 CHECKLIST DE CORREÇÕES

### Ordem de Execução Recomendada:

#### Fase 1: Correções de Schema (OBRIGATÓRIO)

- [ ] **1.1** Decidir sobre campos extras de Turma (instrutor, alertas)
  - [ ] Opção A: Criar migration em dev + aplicar em prod
  - [ ] Opção B: Remover de dev
  
- [ ] **1.2** Corrigir `situacao_iniciatica.max_length` de 20 → 1
  - [ ] Editar `alunos/models.py`
  - [ ] Criar migration
  - [ ] Aplicar localmente
  - [ ] Testar export/import
  
- [ ] **1.3** Separar SITUACAO_CHOICES em duas constantes
  - [ ] Criar `SITUACAO_ALUNO_CHOICES`
  - [ ] Criar `SITUACAO_INICIATICA_CHOICES`
  - [ ] Atualizar referências nos campos

#### Fase 2: Processos e Scripts (RECOMENDADO)

- [ ] **2.1** Criar script de export padronizado
  - [ ] `scripts/exportar_fixtures.sh`
  - [ ] Documentar no README.md
  
- [ ] **2.2** Validar script `corrigir_fixtures_completo.py`
  - [ ] Já existe ✅
  - [ ] Testar com fixture atual
  
- [ ] **2.3** Adicionar teste de compatibilidade
  - [ ] CI/CD valida campos antes de deploy

#### Fase 3: Documentação (IMPORTANTE)

- [ ] **3.1** Atualizar `AGENT.md` com:
  - [ ] Processo de export correto
  - [ ] Comando de correção de fixtures
  - [ ] Diferenças intencionais Dev vs Prod
  
- [ ] **3.2** Criar `docs/DEPLOY.md` com:
  - [ ] Checklist pré-deploy
  - [ ] Validação de compatibilidade
  - [ ] Rollback procedures

---

## 🎯 AÇÕES IMEDIATAS (HOJE)

### 1. Corrigir situacao_iniciatica (15 min)

```bash
# Editar alunos/models.py linha ~370
# Alterar max_length=20 para max_length=1

python manage.py makemigrations alunos
python manage.py migrate
python manage.py test alunos
```

### 2. Criar Script de Export Padronizado (10 min)

```bash
# Criar scripts/exportar_fixtures.sh
#!/bin/bash
python manage.py dumpdata \
    --natural-foreign \
    --natural-primary \
    --indent 2 \
    --exclude sessions \
    --exclude admin.logentry \
    --exclude auth.permission \
    --exclude contenttypes.contenttype \
    -o "dev_data_$(date +%Y%m%d_%H%M%S).json"

echo "✅ Fixture exportado com sucesso!"
```

### 3. Decisão sobre Campos de Turma (30 min)

**Perguntar ao usuário**:
- Campos de instrutor são necessários? 
  - Se SIM → criar migration e aplicar em prod
  - Se NÃO → remover de dev

**Campos de alerta são usados?**
- Se SIM → adicionar em prod
- Se NÃO → remover de dev

---

## 📊 IMPACTO DAS CORREÇÕES

| Correção | Tempo Estimado | Impacto | Urgência |
|----------|----------------|---------|----------|
| situacao_iniciatica max_length | 15 min | Alto | 🔴 ALTA |
| Campos extras Turma | 30 min | Alto | 🔴 ALTA |
| Script export padronizado | 10 min | Médio | 🟡 MÉDIA |
| Separar SITUACAO_CHOICES | 20 min | Baixo | 🟢 BAIXA |
| Documentação | 60 min | Médio | 🟡 MÉDIA |

**Total Estimado**: ~2h 15min

---

## 🔄 WORKFLOW CORRETO PARA PRÓXIMO DEPLOY

### 1. Pré-Deploy (Desenvolvimento)

```bash
# 1.1 Garantir que migrations estão sincronizadas
python manage.py makemigrations --check --dry-run

# 1.2 Exportar fixtures com script corrigido
bash scripts/exportar_fixtures.sh

# 1.3 Corrigir fixture automaticamente
python scripts/corrigir_fixtures_completo.py \
    dev_data_YYYYMMDD_HHMMSS.json \
    dev_data_corrigido.json

# 1.4 Validar fixture (dry-run)
python manage.py loaddata --dry-run dev_data_corrigido.json
```

### 2. Deploy (Produção)

```bash
# 2.1 Backup
docker exec omaum-db-prod pg_dump -U postgres -d omaum_db \
    -Fc -f /backups/backup_pre_deploy_$(date +%Y%m%d_%H%M%S).dump

# 2.2 Copiar fixture
docker cp dev_data_corrigido.json omaum-web-prod:/app/

# 2.3 Aplicar migrations (se houver)
docker exec omaum-web-prod python manage.py migrate

# 2.4 Importar dados
docker exec omaum-web-prod python manage.py flush --noinput
docker exec omaum-web-prod python manage.py loaddata dev_data_corrigido.json

# 2.5 Validar
docker exec omaum-web-prod python manage.py check
```

### 3. Pós-Deploy (Validação)

```bash
# 3.1 Verificar contagens
docker exec omaum-web-prod python /app/contar_registros.py

# 3.2 Testar aplicação
curl http://192.168.15.4/admin/
curl http://192.168.15.4/alunos/

# 3.3 Verificar logs
docker logs omaum-web-prod --tail 100
```

---

## 📞 PRÓXIMAS AÇÕES

### Antes de Continuar com Deploy:

1. **DECISÃO NECESSÁRIA**: Campos extras de Turma (instrutor, alertas)
2. **CORREÇÃO OBRIGATÓRIA**: situacao_iniciatica max_length
3. **CRIAR**: Script de export padronizado
4. **TESTAR**: Workflow completo em ambiente local

### Contato:

- **Email**: suporte@omaum.edu.br
- **Documentação**: `scripts/README_CORRIGIR_FIXTURES.md`

---

**Status**: 📋 AGUARDANDO CORREÇÕES  
**Próxima Sincronização**: Após implementar correções acima
