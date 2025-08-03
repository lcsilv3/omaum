# CORREÇÃO: Botão de Convocação Não Aparece no Modal

## 📊 DIAGNÓSTICO DO PROBLEMA

### Sintomas Reportados
- Botão de convocação não aparece na listagem de alunos dentro do modal
- Atividade "Trabalho Curador - Terças Feiras" tem convocação ativa (visível no cabeçalho)
- HTML do modal mostra "Atividade com convocação" mas não exibe botões individuais de convocação

### Análise do Código
Ao analisar o HTML renderizado, observei que:
1. O cabeçalho do modal mostra corretamente "Atividade com convocação"
2. A lista de alunos não exibe os botões de convocação individual
3. A lógica no template HTML está correta: `if (PresencaApp.atividadeAtualConvocada)`

### Causa Raiz Identificada
**A variável `PresencaApp.atividadeAtualConvocada` não estava sendo definida corretamente na função `abrirModalPresencaComInterceptador`**

A função no arquivo `registrar_presenca_dias_atividades.js` estava:
- Definindo `window.PresencaApp.atividadeAtual = atividadeId`
- Definindo `window.PresencaApp.diaAtual = dia`
- **MAS NÃO estava definindo `window.PresencaApp.atividadeAtualConvocada`**

Resultado: A condição `if (PresencaApp.atividadeAtualConvocada)` no template sempre retornava `false`, impedindo a criação dos botões de convocação.

## 🛠️ CORREÇÃO IMPLEMENTADA

### Código Adicionado
```javascript
// 🔑 DEFINE SE A ATIVIDADE É CONVOCADA (ESSENCIAL PARA EXIBIR BOTÃO DE CONVOCAÇÃO)
window.PresencaApp.atividadeAtualConvocada = window.PresencaApp.atividadesConvocadas && 
                                             window.PresencaApp.atividadesConvocadas[atividadeId] === true;

console.log('🔑 [MODAL-V2] atividadeAtual:', atividadeId);
console.log('🔑 [MODAL-V2] diaAtual:', dia);
console.log('🔑 [MODAL-V2] atividadeAtualConvocada:', window.PresencaApp.atividadeAtualConvocada);
console.log('🔑 [MODAL-V2] atividadesConvocadas:', window.PresencaApp.atividadesConvocadas);
```

### Modificação na Lógica do Cabeçalho
```javascript
// Segunda linha: "Atividade com convocação" apenas se houver convocação
const temConvocacao = window.PresencaApp.atividadeAtualConvocada; // Usa a variável definida
```

## 🎯 FLUXO ESPERADO APÓS CORREÇÃO

### Cenário: Atividade com Convocação
1. **Usuário clica em dia selecionado da atividade "Trabalho Curador"**
2. **Modal abre com função `abrirModalPresencaComInterceptador`**:
   - Define `atividadeAtual = 3`
   - Define `diaAtual = "04"`
   - **Define `atividadeAtualConvocada = true`** (correção aplicada)
3. **Cabeçalho do modal exibe**: "Atividade com convocação"
4. **Função `preencherListaAlunos` executa**:
   - Verifica `if (PresencaApp.atividadeAtualConvocada)` → **agora retorna `true`**
   - **Cria botões de "Convocado"/"Não Convocado" para cada aluno**
5. **Usuário vê**:
   - Lista de alunos com botões de presença (Presente/Ausente)
   - **Botões de convocação (azul "Convocado" / cinza "Não Convocado")**
   - Campos de justificativa para ausentes

### Logs Esperados
```
🔑 [MODAL-V2] atividadeAtual: 3
🔑 [MODAL-V2] diaAtual: 04
🔑 [MODAL-V2] atividadeAtualConvocada: true
🔑 [MODAL-V2] atividadesConvocadas: {1: false, 2: false, 3: true}
🏷️ [MODAL-V2] Título atualizado: Trabalho Curador - Terças Feiras (04/08/2025)
🏷️ [MODAL-V2] Convocação: SIM
```

## 📋 TESTE RECOMENDADO

1. **Recarregue a página** para aplicar o JS corrigido
2. **Selecione dias 3 e 4** na atividade "Trabalho Curador - Terças Feiras"
3. **Clique no dia 3 ou 4** (azul selecionado) para abrir o modal
4. **Verifique se aparecem**:
   - Nome do aluno
   - Botão "Convocado" (azul) ou "Não Convocado" (cinza)
   - Botão "Presente"/"Ausente"
   - Campo de justificativa (se ausente)
5. **Teste a funcionalidade**: clique no botão "Convocado" para alternar para "Não Convocado"

## 🔧 ARQUIVO MODIFICADO

- `static/js/presencas/registrar_presenca_dias_atividades.js`
  - Adicionada definição de `window.PresencaApp.atividadeAtualConvocada`
  - Adicionados logs de debug para rastreamento
  - Corrigida referência à variável no cabeçalho do modal

## ✅ RESULTADO ESPERADO

Agora os botões de convocação devem aparecer corretamente para atividades com convocação, permitindo ao usuário marcar individualmente quais alunos foram convocados ou não para a atividade específica.
