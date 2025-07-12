# Changelog - Sistema OMAUM

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não Lançado]

### Em Desenvolvimento
- Sistema de notificações em tempo real
- Aplicativo mobile companion
- Integração com sistemas acadêmicos externos

## [2.0.0] - 2024-01-15

### Adicionado
- **Sistema de Presenças Completo**: Implementação completa do módulo de presenças
  - Modelo `PresencaDetalhada` com campos C, P, F, V1, V2
  - Cálculos automáticos de percentuais e carências
  - Configurações personalizáveis por turma/atividade
- **Registro Multi-etapas**: Processo guiado em 5 etapas
  - Dados básicos (curso, turma, período)
  - Totais por atividades
  - Distribuição por dias
  - Dados individuais dos alunos
  - Confirmação e validação
- **Registro Rápido Otimizado**: Interface AJAX para registros pontuais
  - Busca de alunos em tempo real
  - Validação automática de dados
  - Salvamento em lote otimizado
- **Painel de Estatísticas**: Dashboard interativo
  - Gráficos em tempo real (Pizza, Barras, Linha)
  - Indicadores KPI principais
  - Filtros dinâmicos por período/turma
- **Exportação Avançada**: Sistema completo de relatórios
  - Múltiplos formatos (Excel, PDF, CSV)
  - Templates profissionais
  - Agendamento automático de relatórios
  - Envio por email
- **API REST Completa**: Endpoints para integração
  - Autenticação por token
  - Rate limiting
  - Documentação Swagger/ReDoc
  - Versionamento de API
- **Sistema de Configuração**: Flexibilidade total
  - Limites de carência por faixas percentuais
  - Pesos por atividade
  - Configurações específicas por turma

### Melhorado
- **Performance**: Otimização de queries com select_related/prefetch_related
- **Validação**: Sistema robusto de validação em múltiplas camadas
- **Cache**: Implementação estratégica de cache para consultas pesadas
- **Logging**: Sistema detalhado de logs para auditoria
- **UI/UX**: Interface mais responsiva e intuitiva

### Segurança
- Validação rigorosa de inputs
- Prevenção contra SQL injection
- Rate limiting em APIs
- Auditoria completa de operações

## [1.5.0] - 2023-12-01

### Adicionado
- Módulo básico de presenças
- CRUD simples para registros
- Exportação básica em Excel
- Sistema de usuários e permissões

### Melhorado
- Interface administrativa
- Navegação entre módulos
- Performance geral do sistema

### Corrigido
- Bugs na importação de dados
- Problemas de encoding em exportações
- Validações de formulários

## [1.4.0] - 2023-11-01

### Adicionado
- Módulo de Turmas completo
- Gestão de períodos letivos
- Matriculas de alunos em turmas
- Relatórios básicos de turmas

### Melhorado
- Integração entre módulos
- Validações de dados
- Interface de usuário

## [1.3.0] - 2023-10-01

### Adicionado
- Módulo de Atividades
- Tipos de atividades (acadêmica/ritualística)
- Configuração de obrigatoriedade
- Vinculação atividades-turmas

### Melhorado
- Sistema de navegação
- Breadcrumbs
- Mensagens de feedback

## [1.2.0] - 2023-09-01

### Adicionado
- Módulo de Cursos
- Hierarquia de cursos
- Duração e configurações
- Pré-requisitos entre cursos

### Melhorado
- Sistema de templates
- Padronização visual
- Responsividade

## [1.1.0] - 2023-08-01

### Adicionado
- Módulo de Alunos completo
- CRUD de estudantes
- CPF e validações
- Histórico de alterações

### Melhorado
- Sistema de autenticação
- Controle de permissões
- Segurança geral

### Corrigido
- Problemas de migração
- Bugs na listagem
- Validação de CPF

## [1.0.0] - 2023-07-01

### Adicionado
- **Primeira versão estável** do Sistema OMAUM
- Estrutura base do projeto Django
- Sistema de autenticação básico
- Interface administrativa
- Configurações iniciais
- Documentação básica

### Características Principais
- Framework Django 4.2
- Python 3.8+
- SQLite para desenvolvimento
- Interface administrativa Django
- Sistema de logs básico

---

## Guia de Migração

### De v1.x para v2.0

#### Breaking Changes

1. **Modelo de Presenças Reformulado**
   ```python
   # ANTES (v1.x)
   class Presenca(models.Model):
       aluno = models.ForeignKey(Aluno)
       data = models.DateField()
       presente = models.BooleanField()
   
   # DEPOIS (v2.0)
   class PresencaDetalhada(models.Model):
       aluno = models.ForeignKey(Aluno)
       periodo = models.DateField()  # Primeiro dia do mês
       convocacoes = models.PositiveIntegerField()
       presencas = models.PositiveIntegerField()
       faltas = models.PositiveIntegerField()
       # ... novos campos
   ```

2. **URLs Reorganizadas**
   ```python
   # ANTES
   path('presencas/', views.lista)
   
   # DEPOIS
   path('presencas/consolidado/', ConsolidadoView.as_view())
   path('presencas/registro-rapido/', registro_rapido_view)
   ```

3. **API Endpoints Modificados**
   ```bash
   # ANTES
   GET /api/presencas/
   
   # DEPOIS
   GET /api/v1/presencas/
   GET /api/v1/presencas-detalhadas/
   ```

#### Passos para Migração

1. **Backup dos Dados**
   ```bash
   python manage.py dumpdata > backup_v1.json
   ```

2. **Atualizar Dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Executar Migrações**
   ```bash
   python manage.py migrate
   ```

4. **Script de Migração de Dados**
   ```python
   # scripts/migrate_v1_to_v2.py
   from presencas.models import Presenca, PresencaDetalhada
   
   # Converter presenças individuais para modelo detalhado
   # Script completo disponível na documentação
   ```

5. **Validar Migração**
   ```bash
   python manage.py test
   python manage.py check --deploy
   ```

### De v1.5 para v2.0

#### Mudanças Menos Impactantes

1. **Novas Configurações**
   ```python
   # settings.py - Adicionar
   INSTALLED_APPS += ['rest_framework']
   
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework.authentication.TokenAuthentication',
       ],
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.IsAuthenticated',
       ],
   }
   ```

2. **Templates Atualizados**
   - Novos templates em `presencas/templates/`
   - Arquivos CSS/JS atualizados
   - Bootstrap 5 como padrão

3. **URLs Adicionais**
   ```python
   # urls.py - Adicionar
   path('api/', include('presencas.api.urls')),
   ```

#### Script de Migração Automática

```bash
# scripts/migrate_to_v2.sh
#!/bin/bash

echo "Iniciando migração para v2.0..."

# 1. Backup
python manage.py dumpdata > backup_pre_v2.json

# 2. Atualizar código
git checkout v2.0.0

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Migração de dados
python manage.py migrate

# 5. Criar configurações padrão
python manage.py shell < scripts/create_default_configs.py

# 6. Testes
python manage.py test

echo "Migração concluída!"
```

---

## Roadmap Futuro

### v2.1.0 - Planejado para 2024-03-01
- [ ] Notificações push para aplicativo mobile
- [ ] Relatórios com inteligência artificial
- [ ] Integração com Google Calendar
- [ ] Workflow de aprovação de faltas

### v2.2.0 - Planejado para 2024-06-01
- [ ] Sistema de backup automático
- [ ] Auditoria avançada com blockchain
- [ ] Reconhecimento facial para presença
- [ ] Aplicativo mobile nativo

### v3.0.0 - Planejado para 2024-12-01
- [ ] Arquitetura de microserviços
- [ ] Deploy em Kubernetes
- [ ] Machine Learning para predição de faltas
- [ ] API GraphQL

---

## Contribuindo

### Como Reportar Bugs
1. Verifique se o bug já foi reportado nas [Issues](https://github.com/lcsilv3/omaum/issues)
2. Crie uma nova issue com template de bug report
3. Inclua informações detalhadas sobre reprodução
4. Adicione logs e screenshots se aplicável

### Como Sugerir Features
1. Verifique o roadmap atual
2. Crie uma issue com template de feature request
3. Descreva o problema que a feature resolve
4. Proponha uma solução detalhada

### Como Contribuir com Código
1. Fork do repositório
2. Crie branch para sua feature
3. Implemente seguindo as convenções
4. Adicione testes
5. Envie Pull Request

---

## Suporte

### Versões Suportadas

| Versão | Suporte | Fim do Suporte |
|--------|---------|----------------|
| 2.0.x  | ✅ Ativo | TBD |
| 1.5.x  | 🔶 Correções de segurança | 2024-07-01 |
| 1.4.x  | ❌ Não suportada | 2024-01-01 |

### Canais de Suporte
- **Email**: suporte@omaum.edu.br
- **GitHub Issues**: Para bugs e features
- **Slack**: #suporte (convite via email)
- **Documentação**: https://docs.omaum.edu.br

### SLA de Suporte
- **Bugs críticos**: 24 horas
- **Bugs normais**: 72 horas
- **Features**: Conforme roadmap
- **Documentação**: 1 semana
