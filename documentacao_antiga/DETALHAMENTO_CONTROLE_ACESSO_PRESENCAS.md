# DETALHAMENTO: CONTROLE DE ACESSO E PERMISSÕES GRANULARES

**Data:** 06 de agosto de 2025  
**Contexto:** SEMANA 2 do Plano de Implementação  
**Foco:** Sistema Avançado de Permissões para Presenças  

---

## 🎯 VISÃO GERAL DO SISTEMA

### **📊 MATRIZ COMPLETA DE PERMISSÕES**

| Grupo / Papel | Visualizar | Criar | Editar | Excluir | Auditoria | Admin |
|---------------|------------|-------|--------|---------|-----------|-------|
| **Aluno** | ✅ Próprias | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Monitor** | ✅ Turma | ✅ Turma | ✅ Próprias + Recentes | ❌ | ❌ | ❌ |
| **Professor** | ✅ Turma | ✅ Turma + Lote | ✅ Próprias + Recentes + Lote | ✅ Próprias + Recentes | ✅ Básica | ❌ |
| **Coordenador** | ✅ Todas | ✅ Todas + Lote | ✅ Todas + Além do Prazo + Lote | ✅ Todas + Restaurar | ✅ Completa + Export | ✅ Parcial |
| **Administrador** | ✅ Todas | ✅ Todas + Lote | ✅ Todas + Override Rules + Lote | ✅ Todas + Restaurar | ✅ Completa + Export | ✅ Total |

---

## 🔒 CATEGORIAS DE PERMISSÕES DETALHADAS

### **1. PERMISSÕES DE VISUALIZAÇÃO (5 níveis)**
```python
# Hierarquia de acesso crescente
'can_view_own_presenca'         # Apenas suas próprias presenças
'can_view_turma_presenca'       # Presenças das turmas que leciona
'can_view_any_presenca'         # Todas as presenças do sistema
'can_view_presenca_details'     # Detalhes completos (observações, etc.)
'can_view_audit_trail'          # Histórico de auditoria
```

### **2. PERMISSÕES DE CRIAÇÃO (3 níveis)**
```python
'can_create_presenca_turma'     # Criar para suas turmas
'can_create_presenca_any'       # Criar para qualquer turma
'can_bulk_create_presenca'      # Criação em lote
```

### **3. PERMISSÕES DE EDIÇÃO (5 níveis)**
```python
'can_edit_own_presenca'              # Editar apenas próprios registros
'can_edit_recent_presenca'           # Editar registros recentes (7 dias)
'can_edit_any_presenca'              # Editar qualquer presença
'can_edit_presenca_beyond_deadline'  # Editar após prazo normal
'can_bulk_edit_presenca'             # Edição em lote
```

### **4. PERMISSÕES DE EXCLUSÃO (4 níveis)**
```python
'can_delete_own_presenca'        # Excluir próprios registros
'can_delete_recent_presenca'     # Excluir registros recentes (24h)
'can_delete_any_presenca'        # Excluir qualquer presença
'can_restore_deleted_presenca'   # Restaurar presenças excluídas
```

### **5. PERMISSÕES DE AUDITORIA (3 níveis)**
```python
'can_view_audit_trail'           # Ver histórico básico
'can_view_full_audit_details'    # Ver detalhes completos de auditoria
'can_export_audit_reports'       # Exportar relatórios
```

### **6. PERMISSÕES ADMINISTRATIVAS (3 níveis)**
```python
'can_override_business_rules'    # Ignorar regras de negócio
'can_manage_presenca_settings'   # Gerenciar configurações
'can_access_admin_dashboard'     # Acessar dashboard admin
```

---

## ⏰ REGRAS TEMPORAIS DINÂMICAS

### **📅 JANELAS TEMPORAIS CONFIGURÁVEIS**

| Ação | Janela Padrão | Quem Pode Alterar | Override |
|------|---------------|-------------------|----------|
| **Criação** | Sem limite | Professor+ | - |
| **Edição Normal** | 7 dias | Criador | `can_edit_recent_presenca` |
| **Edição Estendida** | 30 dias | Coordenador+ | `can_edit_presenca_beyond_deadline` |
| **Edição Irrestrita** | Sem limite | Admin | `can_edit_any_presenca` |
| **Exclusão Normal** | 24 horas | Criador | `can_delete_recent_presenca` |
| **Exclusão Estendida** | Sem limite | Admin | `can_delete_any_presenca` |

### **🔧 CONFIGURAÇÃO DINÂMICA**
```python
# Modelo PresencaConfiguracao permite ajustar em tempo real:
- dias_limite_edicao: 7 (padrão)
- horas_limite_exclusao: 24 (padrão)
- max_alteracoes_por_dia: 50 (padrão)
- motivo_obrigatorio_edicao: True
- motivo_obrigatorio_exclusao: True
```

---

## 🛡️ SISTEMA DE REGRAS DE NEGÓCIO

### **🎯 ENGINE DE VERIFICAÇÃO CONTEXTUAL**

O `PresencaPermissionEngine` aplica múltiplas regras em sequência:

1. **Verificação de Usuário**
   - Superusuário? → Acesso total
   - Usuário autenticado? → Continua verificação

2. **Verificação de Ownership**
   - É o criador da presença? → Aplica regras de owner
   - Professor da turma? → Aplica regras de professor
   - Coordenador/Admin? → Aplica regras hierárquicas

3. **Verificação Temporal**
   - Dentro da janela normal? → Permite
   - Fora da janela + permissão especial? → Permite
   - Fora da janela + sem permissão? → Nega

4. **Verificação de Status**
   - Presença finalizada? → Verifica override
   - Presença excluída? → Verifica restore
   - Status normal? → Continua

5. **Verificação de Limites**
   - Limite diário de alterações? → Verifica contador
   - Operação em lote? → Verifica permissão específica

### **📊 EXEMPLOS DE VERIFICAÇÃO**

```python
# CENÁRIO 1: Professor tentando editar presença de 10 dias atrás
pode, motivo = PresencaPermissionEngine.pode_alterar_presenca(presenca, professor)
# Resultado: False, "Período de alteração expirado (10 dias). Limite: 7 dias"

# CENÁRIO 2: Coordenador com permissão especial
pode, motivo = PresencaPermissionEngine.pode_alterar_presenca(presenca, coordenador)
# Resultado: True, "Edição após prazo (permissão global)"

# CENÁRIO 3: Aluno tentando ver presença de outro aluno
pode, motivo = PresencaPermissionEngine.pode_visualizar_presenca(presenca, aluno)
# Resultado: False, "Sem permissão para visualizar esta presença"
```

---

## 🎮 CONTROLES DE SEGURANÇA AVANÇADOS

### **🚦 SISTEMA DE LIMITES**

1. **Limite Diário de Alterações**
   - Padrão: 50 alterações por usuário/dia
   - Cache: Redis/Memcached com TTL de 24h
   - Exceção: `can_override_business_rules`

2. **Prevenção de Abuse**
   - Rate limiting por IP
   - Detecção de padrões suspeitos
   - Bloqueio automático temporário

3. **Auditoria Obrigatória**
   - Motivo obrigatório para alterações/exclusões
   - Rastreamento de IP e User-Agent
   - Log detalhado de todas as operações

### **🔍 MONITORAMENTO EM TEMPO REAL**

```python
# Alertas automáticos para:
- Mais de 20 alterações por usuário em 1 hora
- Tentativas de acesso negadas > 10 por usuário
- Alterações em lote sem motivo adequado
- Padrões de acesso fora do horário normal
```

---

## 💻 INTEGRAÇÃO COM INTERFACE

### **🎨 ELEMENTOS VISUAIS DINÂMICOS**

1. **Badges de Permissão**
   ```html
   <!-- Verde: Pode executar -->
   <span class="badge badge-success">✓ Pode editar</span>
   
   <!-- Amarelo: Atenção -->
   <span class="badge badge-warning">⚠ Prazo expirando</span>
   
   <!-- Vermelho: Bloqueado -->
   <span class="badge badge-danger">✗ Sem permissão</span>
   ```

2. **Indicadores Temporais**
   ```html
   <!-- Contador regressivo -->
   <div class="time-limit">
     <i class="fas fa-clock"></i>
     Pode editar até: <strong>23h 45min</strong>
   </div>
   ```

3. **Tooltips Informativos**
   ```html
   <!-- Explicação do motivo -->
   <button disabled title="Período de edição expirado (7 dias)">
     <i class="fas fa-edit"></i> Editar
   </button>
   ```

### **📱 RESPONSIVIDADE**

- **Desktop**: Todas as informações visíveis
- **Tablet**: Badges compactos + tooltips
- **Mobile**: Ícones + modals para detalhes

---

## 🧪 ESTRATÉGIA DE TESTES

### **🔬 TESTES DE PERMISSÃO**

```python
# Cada combinação usuário + ação + contexto
class TestPermissionMatrix:
    def test_aluno_view_own_presenca(self):
        """Aluno pode ver própria presença"""
    
    def test_aluno_cannot_view_other_presenca(self):
        """Aluno não pode ver presença de outro"""
    
    def test_professor_edit_within_deadline(self):
        """Professor pode editar dentro do prazo"""
    
    def test_professor_cannot_edit_after_deadline(self):
        """Professor não pode editar após prazo"""
    
    # ... 50+ testes cobrindo todas as combinações
```

### **⏱️ TESTES TEMPORAIS**

```python
class TestTemporalRules:
    def test_editing_window_expiration(self):
        """Testa expiração da janela de edição"""
    
    def test_deletion_window_stricter(self):
        """Testa janela mais restrita para exclusão"""
    
    def test_weekend_rules(self):
        """Testa regras especiais para fins de semana"""
```

### **🚀 TESTES DE PERFORMANCE**

```python
class TestPermissionPerformance:
    def test_permission_check_speed(self):
        """Verificação de permissão < 10ms"""
    
    def test_bulk_permission_check(self):
        """Verificação em lote < 100ms para 100 registros"""
    
    def test_cache_effectiveness(self):
        """Cache reduz tempo em 80%+"""
```

---

## 📈 MÉTRICAS E MONITORAMENTO

### **📊 KPIs DO SISTEMA**

1. **Performance**
   - Tempo médio de verificação: < 10ms
   - Taxa de cache hit: > 90%
   - Throughput: > 1000 verificações/segundo

2. **Segurança**
   - Tentativas de acesso negadas: < 1% do total
   - Alterações sem motivo: 0%
   - Violações de limite: < 0.1%

3. **Usabilidade**
   - Feedback claro em 100% das negações
   - Tempo de compreensão de permissões: < 5s
   - Satisfação do usuário: > 90%

### **🔔 ALERTAS AUTOMÁTICOS**

```python
# Configuração de alertas
ALERTS = {
    'high_denied_access': {'threshold': 10, 'window': '1h'},
    'bulk_operations_spike': {'threshold': 5, 'window': '10m'},
    'permission_check_slow': {'threshold': 50, 'unit': 'ms'},
    'cache_miss_high': {'threshold': 20, 'unit': '%'},
}
```

---

## 🎯 BENEFÍCIOS ESPERADOS

### **🔒 SEGURANÇA**
- **Zero** alterações não autorizadas
- **100%** das ações auditadas
- **Detecção** automática de tentativas de abuse

### **⚡ PERFORMANCE**
- **Cache inteligente** reduz verificações desnecessárias
- **Verificação contextual** otimizada
- **Operações em lote** eficientes

### **💡 USABILIDADE**
- **Feedback visual** claro e imediato
- **Explicações** detalhadas para negações
- **Interface adaptativa** baseada em permissões

### **📊 COMPLIANCE**
- **Trilha de auditoria** completa
- **Relatórios** detalhados para gestão
- **Configuração** flexível para diferentes políticas

---

**🎯 PRÓXIMO PASSO:** Implementação da **Semana 2** com foco neste sistema avançado de permissões granulares.
