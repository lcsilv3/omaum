# 🔍 DEBUG - Sincronização de Dias

## Problema Identificado
- Usuário marca presença no **dia 3**
- Campo de observação aparece para **dia 4**

## Pontos de Investigação

### 1. Interceptador V2 - Nova Lógica
✅ Implementada lógica baseada em `maxDias` ao invés de `diasFaltandoPresenca`
✅ Controla pela quantidade necessária para a atividade
✅ Logs ultra detalhados para diagnóstico

### 2. Possíveis Causas do Dia Errado no Card
1. **Timezone/Data**: Conversão incorreta entre dia selecionado e date object
2. **onDayCreate**: Event handler usando `dayElem.textContent` pode estar pegando dia errado
3. **Flatpickr selectedDates**: Array de datas pode ter offset
4. **Campo de Observação**: `date.getDate()` pode estar retornando dia+1

### 3. Próximos Passos para Debug
1. Recarregar página e testar nova lógica V2
2. Verificar logs do interceptador
3. Verificar se campos de observação são criados corretamente
4. Confirmar sincronização entre dia selecionado e dia salvo

## Melhorias Implementadas

### Interceptador V2
- ✅ Controla por `maxDias` da atividade
- ✅ Conta dias já preenchidos
- ✅ Só fecha modal quando atividade está completa
- ✅ Navega automaticamente para próximo dia pendente
- ✅ Logs detalhados para diagnóstico

### Função diasFaltandoPresenca V2
- ✅ Baseada em `maxDias` ao invés de dias selecionados
- ✅ Retorna dias ainda não preenchidos
- ✅ Logs simplificados e focados

## Teste Sugerido
1. Selecionar 2 dias no calendário (atividade "Trabalho Curador - Terças Feiras")
2. Clicar no primeiro dia
3. Marcar algumas presenças
4. Clicar "Salvar Presenças"
5. Verificar se modal permanece aberto
6. Verificar se navega para próximo dia
7. Verificar se campos de observação mostram dias corretos

## Status
🔄 Aguardando teste da nova implementação V2
