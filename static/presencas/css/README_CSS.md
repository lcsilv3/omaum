# CSS Grid System Excel-like - Documentação

## Visão Geral

Este sistema CSS replica exatamente o comportamento e visual do Microsoft Excel para a tabela consolidada de presenças. Foi desenvolvido para oferecer uma experiência de usuário familiar e intuitiva.

## Características Principais

### 🎯 Visual Excel Autêntico
- Cores, bordas e tipografia idênticas ao Excel
- Cabeçalhos sticky com hierarquia visual
- Células editáveis com estados visuais claros
- Sistema de cores baseado em performance

### 📱 Totalmente Responsivo
- Mobile-first approach
- Breakpoints otimizados: 480px, 768px, 1024px
- Colunas adaptáveis conforme tamanho da tela
- Navigation touch-friendly

### ⚡ Performance Otimizada
- CSS Grid + Flexbox híbrido
- GPU acceleration para animações
- Scroll virtual para grandes datasets
- Lazy loading de células visíveis

## Estrutura de Classes

### Classes Principais

#### Container
```css
.consolidado-container
```
Container principal com scroll horizontal e vertical otimizado.

#### Tabela
```css
.consolidado-table
```
Grid principal que organiza toda a estrutura da tabela.

### Colunas Fixas (Sticky)

#### Número do Aluno
```css
.numero-col
```
Primeira coluna fixa, sempre visível durante scroll horizontal.

#### Iniciais
```css
.iniciais-col
```
Segunda coluna fixa com iniciais do nome (oculta em mobile).

#### Nome do Aluno
```css
.aluno-nome
```
Terceira coluna fixa com nome completo do aluno.

#### Turma
```css
.turma-nome
```
Quarta coluna fixa com nome da turma (oculta em mobile pequeno).

### Cabeçalhos

#### Atividades
```css
.atividade-header        /* Cabeçalho principal da atividade */
.atividade-subheader     /* Subcabeçalhos (C, P, F, V1, V2, %) */
```

#### Totais
```css
.totais-header
```
Cabeçalho da seção de totalizações.

### Células Editáveis

#### Base
```css
.celula-editavel         /* Célula base editável */
.celula-editavel:hover   /* Estado hover */
.celula-editavel:focus-within /* Estado de edição ativa */
```

#### Estados de Validação
```css
.celula-editavel.validando  /* Durante validação AJAX */
.celula-editavel.sucesso    /* Após salvamento bem-sucedido */
.celula-editavel.erro       /* Após erro de validação */
```

### Células de Performance

#### Percentuais
```css
.percentual-cell         /* Base para células de percentual */
.percentual-alto         /* 76-100% - Verde */
.percentual-medio        /* 51-75% - Amarelo */
.percentual-baixo        /* 0-50% - Vermelho */
```

### Indicadores Especiais

#### Carências
```css
.cell-carencia
```
Destaca células com carências pendentes (ícone ⚠).

#### Voluntários
```css
.cell-voluntario
```
Destaca atividades voluntárias (ícone ★).

## Variáveis CSS (Custom Properties)

### Cores
```css
:root {
  /* Cores principais */
  --excel-border-color: #d0d7de;
  --excel-header-bg: #f6f8fa;
  --excel-cell-bg: #ffffff;
  --excel-cell-hover: #f3f4f6;
  
  /* Performance */
  --color-performance-high: #dcfce7;
  --color-performance-medium: #fef3c7;
  --color-performance-low: #fee2e2;
  
  /* Especiais */
  --color-carencia: #fecaca;
  --color-voluntario: #e0e7ff;
}
```

### Dimensões
```css
:root {
  --cell-min-width: 60px;
  --cell-height: 36px;
  --header-height: 40px;
  --fixed-column-width: 200px;
  --turma-column-width: 150px;
  --numero-column-width: 50px;
  --iniciais-column-width: 80px;
}
```

### Transições
```css
:root {
  --transition-fast: 0.15s ease;
  --transition-medium: 0.3s ease;
  --transition-slow: 0.5s ease;
}
```

## Classes Utilitárias

### Estados Dinâmicos
```css
.excel-frozen      /* Força posição sticky */
.excel-highlight   /* Destaque temporário */
.excel-selected    /* Célula selecionada */
.excel-error       /* Erro de validação */
.excel-warning     /* Aviso */
.excel-success     /* Sucesso */
```

### Indicadores de Estado
```css
.cell-pending      /* Alteração pendente */
.tooltip-excel     /* Tooltip estilizado */
```

## Responsividade

### Desktop (>1024px)
- Todas as colunas visíveis
- Tamanhos padrão
- Hover effects completos

### Tablet (768px - 1024px)
- Colunas ligeiramente reduzidas
- Fonte menor
- Touch-friendly

### Mobile (480px - 768px)
- Coluna "Iniciais" oculta
- Tamanhos reduzidos
- Navigation adaptado

### Mobile Pequeno (<480px)
- Coluna "Turma" também oculta
- Modo mínimo
- Focus em dados essenciais

## Animações e Transições

### Edição de Células
- Hover suave (0.15s)
- Focus destacado
- Estados de validação animados

### Performance Visual
- Scroll suave
- Transições CSS otimizadas
- GPU acceleration ativado

### Estados de Loading
- Spinner animado
- Overlay com blur
- Feedback visual claro

## Acessibilidade

### Navegação por Teclado
- Focus indicators claros
- Tab order lógico
- Controles acessíveis

### Leitores de Tela
- Semântica HTML apropriada
- Labels descritivos
- Estados anunciados

### Preferências do Usuário
- Suporte a prefers-reduced-motion
- Modo escuro opcional
- Alto contraste disponível

## Browser Support

### Suportados
- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

### Features Utilizadas
- CSS Grid
- CSS Custom Properties
- Sticky positioning
- Flexbox

## Performance

### Otimizações
- CSS Grid para layout eficiente
- GPU acceleration para animações
- Scroll virtual para grandes datasets
- Lazy loading de células

### Métricas Alvo
- First Paint: <100ms
- Layout Shift: <0.1
- Smooth scrolling: 60fps

## Customização

### Temas
Para criar um tema customizado, sobrescreva as variáveis CSS:

```css
:root {
  --excel-border-color: #custom-color;
  --excel-header-bg: #custom-bg;
  /* ... outras variáveis */
}
```

### Dimensões
Ajuste as dimensões das colunas conforme necessário:

```css
:root {
  --fixed-column-width: 250px;  /* Nome mais largo */
  --cell-min-width: 80px;       /* Células maiores */
}
```

## Integração com JavaScript

### Classes Dinâmicas
O CSS está preparado para receber classes adicionadas via JavaScript:

```javascript
// Marcar célula como pendente
cell.classList.add('cell-pending');

// Mostrar resultado de validação
cell.classList.add('sucesso');
setTimeout(() => cell.classList.remove('sucesso'), 2000);
```

### Estados de Loading
```javascript
// Mostrar loading
document.querySelector('.loading-overlay').style.display = 'block';

// Esconder loading
document.querySelector('.loading-overlay').style.display = 'none';
```

## Troubleshooting

### Problemas Comuns

#### Colunas não ficam fixas
- Verificar se `position: sticky` é suportado
- Confirmar estrutura HTML correta
- Validar z-index values

#### Performance lenta
- Reduzir número de animações
- Verificar número de células visíveis
- Otimizar consultas DOM

#### Layout quebrado em mobile
- Verificar viewport meta tag
- Validar media queries
- Testar em dispositivos reais

## Manutenção

### Atualizações Recomendadas
- Revisar performance trimestralmente
- Atualizar browser support anualmente
- Testar acessibilidade regularmente

### Monitoring
- Core Web Vitals
- Crash reports
- User feedback

---

**Desenvolvido pelo Agente 8 - CSS Grid System**  
**Data:** Novembro 2024  
**Versão:** 1.0.0
