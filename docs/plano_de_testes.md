# Plano de Testes do Sistema OMAUM

## Introdução

Este documento descreve o plano de testes para o sistema OMAUM, incluindo testes unitários, de integração, E2E, de desempenho e de segurança para todos os módulos do sistema.

## Objetivos

- Garantir a qualidade do código e a corretude das funcionalidades
- Identificar e corrigir bugs antes da implantação
- Assegurar que o sistema atende aos requisitos funcionais e não-funcionais
- Verificar a segurança e o desempenho do sistema

## Escopo

O plano de testes abrange os seguintes módulos do sistema:

1. Alunos
2. Turmas
3. Atividades
4. Frequências
5. Notas
6. Pagamentos
7. Matriculas

## Tipos de Testes

### Testes Unitários

Os testes unitários verificam o funcionamento isolado de componentes individuais do sistema, como modelos, formulários e funções auxiliares.

**Arquivos de Teste:**
- `tests/alunos/test_models.py`
- `tests/alunos/test_forms.py`
- `tests/turmas/test_models.py`
- `tests/turmas/test_forms.py`
- `tests/atividades/test_models.py`
- `tests/atividades/test_forms.py`
- `tests/frequencias/test_models.py`
- `tests/frequencias/test_forms.py`
- `tests/notas/test_models.py`
- `tests/notas/test_forms.py`
- `tests/pagamentos/test_models.py`
- `tests/pagamentos/test_forms.py`
- `tests/matriculas/test_models.py`
- `tests/matriculas/test_forms.py`

### Testes de Integração

Os testes de integração verificam a interação entre diferentes componentes do sistema, como views, modelos e templates.

**Arquivos de Teste:**
- `tests/alunos/test_views.py`
- `tests/turmas/test_views.py`
- `tests/atividades/test_views.py`
- `tests/frequencias/test_views.py`
- `tests/notas/test_views.py`
- `tests/pagamentos/test_views.py`
- `tests/matriculas/test_views.py`

### Testes E2E (End-to-End)

Os testes E2E simulam a interação do usuário com o sistema, verificando fluxos completos de uso.

**Arquivos de Teste:**
- `tests/e2e/test_alunos.py`
- `tests/e2e/test_turmas.py`
- `tests/e2e/test_atividades.py`
- `tests/e2e/test_frequencias.py`
- `tests/e2e/test_notas.py`
- `tests/e2e/test_pagamentos.py`
- `tests/e2e/test_matriculas.py`

### Testes de Desempenho

Os testes de desempenho verificam o tempo de resposta e a eficiência do sistema sob diferentes cargas.

**Arquivos de Teste:**
- `tests/performance/test_performance.py`

### Testes de Segurança

Os testes de segurança verificam a proteção do sistema contra ameaças como acesso não autorizado, injeção SQL e XSS.

**Arquivos de Teste:**
- `tests/security/test_security.py`

## Ambiente de Testes

### Requisitos de Software

- Python 3.8+
- Django 3.2+
- Selenium 4.0+
- ChromeDriver (para testes E2E)
- Pytest 7.0+

### Configuração do Ambiente

1. Instalar as dependências:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Configurar o banco de dados de teste:
   ```bash
   python manage.py migrate --settings=config.settings.test
   ```

3. Instalar o ChromeDriver para testes E2E:
   ```bash
   # Linux
   apt-get install chromium-chromedriver
   
   # macOS
   brew install --cask chromedriver
   
   # Windows
   # Baixar o ChromeDriver do site oficial e adicionar ao PATH
   ```

## Execução dos Testes

### Executar Todos os Testes

```bash
python manage.py test --settings=config.settings.test
```

### Executar Testes por Módulo

```bash
python manage.py test tests.alunos --settings=config.settings.test
python manage.py test tests.turmas --settings=config.settings.test
python manage.py test tests.atividades --settings=config.settings.test
# etc.
```

### Executar Testes por Tipo

```bash
python manage.py test tests.e2e --settings=config.settings.test
python manage.py test tests.performance --settings=config.settings.test
python manage.py test tests.security --settings=config.settings.test
```

## Relatórios de Testes

Os relatórios de testes são gerados automaticamente após a execução dos testes e incluem:

- Número total de testes executados
- Número de testes bem-sucedidos e falhos
- Tempo de execução de cada teste
- Detalhes dos erros encontrados

## Manutenção do Plano de Testes

Este plano de testes deve ser revisado e atualizado regularmente, especialmente quando:

- Novas funcionalidades são adicionadas ao sistema
- Bugs significativos são encontrados e corrigidos
- Mudanças na arquitetura ou design do sistema são implementadas

## Responsabilidades

- Desenvolvedores: Escrever e manter os testes unitários e de integração
- QA: Escrever e manter os testes E2E, de desempenho e de segurança
- Líder Técnico: Revisar e aprovar o plano de testes
- Todos: Executar os testes antes de enviar código para revisão

## Conclusão

Este plano de testes fornece uma abordagem abrangente para garantir a qualidade do sistema OMAUM. Seguindo este plano, a equipe pode identificar e corrigir problemas precocemente no ciclo de desenvolvimento, resultando em um produto final mais robusto e confiável.
```python

## Passo 11: Script de Automação para Execução dos Testes

```python:scripts/run_tests.py
#!/usr/bin/env python
"""
Script para automatizar a execução dos testes do sistema OMAUM.
"""

import os
import sys
import argparse
import subprocess
import time
import datetime

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Execute testes do sistema OMAUM.')
    parser.add_argument('--module', '-m', help='Módulo específico para testar (ex: alunos, turmas)')
    parser.add_argument('--type', '-t', help='Tipo de teste (unit, integration, e2e, performance, security)')
    parser.add_argument('--all', '-a', action='store_true', help='Executar todos os testes')
    parser.add_argument('--coverage', '-c', action='store_true', help='Gerar relatório de cobertura')
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo verboso')
    parser.add_argument('--output', '-o', help='Arquivo de saída para o relatório')
    
    return parser.parse_args()

def run_tests(module=None, test_type=None, coverage=False, verbose=False):
    """Execute the tests based on the provided parameters."""
    command = ['python', 'manage.py', 'test', '--settings=config.settings.test']
    
    if module and test_type:
        command.append(f'tests.{module}.test_{test_type}')
    elif module:
        command.append(f'tests.{module}')
    elif test_type:
        if test_type == 'unit':
            # Executar todos os testes unitários
            modules = ['alunos', 'turmas', 'atividades', 'frequencias', 'notas', 'pagamentos', 'matriculas']
            test_modules = [f'tests.{m}.test_models tests.{m}.test_forms' for m in modules]
            command.append(' '.join(test_modules))
        elif test_type == 'integration':
            # Executar todos os testes de integração
            modules = ['alunos', 'turmas', 'atividades', 'frequencias', 'notas', 'pagamentos', 'matriculas']
            test_modules = [f'tests.{m}.test_views' for m in modules]
            command.append(' '.join(test_modules))
        elif test_type == 'e2e':
            command.append('tests.e2e')
        elif test_type == 'performance':
            command.append('tests.performance')
        elif test_type == 'security':
            command.append('tests.security')
```