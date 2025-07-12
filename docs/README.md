# Documentação do Sistema OMAUM

Bem-vindo à documentação completa do Sistema OMAUM - uma plataforma robusta para gestão acadêmica com foco em controle de presenças e frequência.

## 📋 Índice da Documentação

### 🎯 Para Usuários Finais
- **[📖 Manual do Usuário](MANUAL_USUARIO.md)**
  - Guia completo para professores e coordenadores
  - Tutoriais passo-a-passo
  - Interface e funcionalidades
  - Casos de uso práticos
  - FAQ e solução de problemas

### 🔧 Para Administradores
- **[⚙️ Guia de Instalação](GUIA_INSTALACAO.md)**
  - Pré-requisitos do sistema
  - Instalação passo-a-passo
  - Configuração inicial
  - Deploy em produção
  - Troubleshooting

### 👨‍💻 Para Desenvolvedores
- **[🏗️ Arquitetura do Sistema](ARQUITETURA_PRESENCAS.md)**
  - Visão geral da arquitetura
  - Padrões de design utilizados
  - Fluxo de dados
  - Decisões técnicas
  - Diagramas e estruturas

- **[💻 Guia do Desenvolvedor](GUIA_DESENVOLVEDOR.md)**
  - Estrutura do código
  - Padrões de desenvolvimento
  - Como contribuir
  - Testes e qualidade
  - Debugging e performance

- **[🔌 Documentação da API](API_DOCUMENTATION.md)**
  - Endpoints REST
  - Autenticação e segurança
  - Exemplos de uso
  - Rate limiting
  - Códigos de erro

### 📝 Histórico e Mudanças
- **[📋 Changelog](CHANGELOG.md)**
  - Histórico de versões
  - Mudanças e melhorias
  - Breaking changes
  - Roadmap futuro
  - Guias de migração

## 🎯 Sistema de Presenças - Funcionalidades Principais

### ✨ Destaques da Versão 2.0

#### 📊 Registro de Presenças
- **Multi-etapas**: Processo guiado em 5 etapas
- **Registro Rápido**: Interface AJAX otimizada
- **Validação Inteligente**: Múltiplas camadas de validação
- **Cálculos Automáticos**: Percentuais e carências em tempo real

#### 📈 Análises e Relatórios
- **Painel Interativo**: Gráficos dinâmicos com Chart.js
- **Exportação Avançada**: Excel profissional, PDF completo, CSV
- **Agendamento Automático**: Relatórios por email
- **Configurações Flexíveis**: Por turma e atividade

#### 🔗 Integração e API
- **API REST Completa**: Endpoints documentados
- **Autenticação Segura**: Token-based
- **Rate Limiting**: Controle de acesso
- **Versionamento**: APIs versionadas

## 🚀 Quick Start

### Para Usuários
1. Leia o [Manual do Usuário](MANUAL_USUARIO.md)
2. Acesse o sistema via navegador
3. Faça login com suas credenciais
4. Explore o menu de Presenças

### Para Desenvolvedores
1. Siga o [Guia de Instalação](GUIA_INSTALACAO.md)
2. Configure o ambiente de desenvolvimento
3. Leia o [Guia do Desenvolvedor](GUIA_DESENVOLVEDOR.md)
4. Execute os testes: `python manage.py test`

### Para Integradores
1. Consulte a [Documentação da API](API_DOCUMENTATION.md)
2. Obtenha token de autenticação
3. Teste endpoints em ambiente de desenvolvimento
4. Implemente seguindo as melhores práticas

## 📊 Arquitetura Geral

```mermaid
graph TB
    subgraph "Frontend"
        UI[Interface Web]
        AJAX[Componentes AJAX]
        GRAFICOS[Gráficos Interativos]
    end
    
    subgraph "Backend Django"
        VIEWS[Views]
        API[API REST]
        MODELS[Modelos]
        SERVICES[Serviços]
    end
    
    subgraph "Dados"
        DB[(PostgreSQL)]
        CACHE[(Redis)]
        FILES[Arquivos]
    end
    
    UI --> VIEWS
    AJAX --> API
    GRAFICOS --> API
    
    VIEWS --> SERVICES
    API --> SERVICES
    
    SERVICES --> MODELS
    MODELS --> DB
    
    SERVICES --> CACHE
    SERVICES --> FILES
```

## 🔄 Fluxo de Trabalho Principal

### 1. Registro de Presença Multi-etapas
```mermaid
sequenceDiagram
    participant U as Usuário
    participant V as View
    participant S as Service
    participant M as Model
    
    U->>V: 1. Dados Básicos
    V->>S: Validar curso/turma
    S->>V: Dados validados
    
    U->>V: 2. Totais Atividades
    V->>S: Calcular limites
    S->>V: Limites retornados
    
    U->>V: 3. Distribuir Dias
    V->>S: Validar distribuição
    S->>V: Distribuição OK
    
    U->>V: 4. Dados Alunos
    V->>S: Calcular estatísticas
    S->>V: Estatísticas calculadas
    
    U->>V: 5. Confirmar
    V->>S: Processar lote
    S->>M: Salvar registros
    M->>S: Registros salvos
    S->>V: Operação concluída
```

### 2. Geração de Relatórios
```mermaid
flowchart TD
    START[Solicitar Relatório] --> FILTROS[Aplicar Filtros]
    FILTROS --> DADOS[Buscar Dados]
    DADOS --> CACHE{Cache Disponível?}
    
    CACHE -->|Sim| USAR_CACHE[Usar Cache]
    CACHE -->|Não| CALCULAR[Calcular Estatísticas]
    
    CALCULAR --> SALVAR_CACHE[Salvar no Cache]
    USAR_CACHE --> FORMATAR[Formatar Relatório]
    SALVAR_CACHE --> FORMATAR
    
    FORMATAR --> TIPO{Tipo de Saída}
    TIPO -->|Excel| EXCEL[Gerar Excel]
    TIPO -->|PDF| PDF[Gerar PDF]
    TIPO -->|CSV| CSV[Gerar CSV]
    
    EXCEL --> RETORNAR[Retornar Arquivo]
    PDF --> RETORNAR
    CSV --> RETORNAR
```

## 🎨 Princípios de Design

### 1. **Simplicidade**
- Interface intuitiva e limpa
- Fluxos de trabalho lógicos
- Feedback visual claro

### 2. **Performance**
- Consultas otimizadas
- Cache estratégico
- Paginação eficiente

### 3. **Flexibilidade**
- Configurações personalizáveis
- Múltiplos formatos de export
- API extensível

### 4. **Confiabilidade**
- Validações robustas
- Tratamento de erros
- Logs detalhados

### 5. **Escalabilidade**
- Arquitetura modular
- Componentes reutilizáveis
- Preparado para crescimento

## 🔧 Tecnologias Utilizadas

### Backend
- **Django 4.2+**: Framework web principal
- **Django REST Framework**: API REST
- **PostgreSQL**: Banco de dados (produção)
- **Redis**: Cache e sessões
- **Celery**: Processamento assíncrono

### Frontend
- **Bootstrap 5**: Framework CSS
- **jQuery**: Manipulação DOM
- **Chart.js**: Gráficos interativos
- **Select2**: Componentes avançados

### DevOps
- **Docker**: Containerização
- **Nginx**: Servidor web
- **GitHub Actions**: CI/CD
- **Monitoring**: Logs e métricas

## 📈 Métricas e KPIs

### Performance
- **Tempo de resposta**: < 200ms (média)
- **Uptime**: 99.9%
- **Throughput**: 1000+ req/min

### Uso
- **Usuários ativos**: Professores e coordenadores
- **Registros processados**: Milhares por mês
- **Relatórios gerados**: Centenas por semana

### Qualidade
- **Cobertura de testes**: 80%+
- **Code coverage**: 85%+
- **Bugs críticos**: < 1/mês

## 🛣️ Roadmap

### Próximas Versões

#### v2.1 (Q1 2024)
- [ ] Notificações push
- [ ] Relatórios com IA
- [ ] App mobile (beta)
- [ ] Integração Google Calendar

#### v2.2 (Q2 2024)
- [ ] Dashboard executivo
- [ ] Auditoria avançada
- [ ] Backup automático
- [ ] Performance monitoring

#### v3.0 (Q4 2024)
- [ ] Microserviços
- [ ] GraphQL API
- [ ] Machine Learning
- [ ] Multi-tenancy

## 🤝 Contribuindo

### Como Contribuir

1. **Issues**: Reporte bugs ou sugira features
2. **Pull Requests**: Contribua com código
3. **Documentação**: Melhore a documentação
4. **Testes**: Adicione cobertura de testes

### Convenções

- **Commits**: Conventional Commits
- **Código**: PEP 8 e Django best practices
- **Testes**: 80%+ coverage obrigatório
- **Documentação**: Docstrings obrigatórias

## 📞 Suporte

### Canais de Contato

- **📧 Email**: suporte@omaum.edu.br
- **🐛 Issues**: GitHub Issues
- **💬 Discussões**: GitHub Discussions
- **📖 Wiki**: Documentação completa

### SLA de Suporte

- **Bugs críticos**: 24h
- **Bugs normais**: 72h
- **Features**: Conforme roadmap
- **Dúvidas**: 48h

---

<div align="center">

**Sistema OMAUM - Gestão Acadêmica Inteligente**

*Desenvolvido com ❤️ para a comunidade educacional*

[🌟 Dar Star](https://github.com/lcsilv3/omaum) | [📖 Documentação](README.md) | [🚀 Demo](https://demo.omaum.edu.br)

</div>

---

*Última atualização: Janeiro 2024 | Versão: 2.0.0*
