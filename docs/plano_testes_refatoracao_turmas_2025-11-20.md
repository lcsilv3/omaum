# Plano de Testes – Refatoração de Encerramento/Exclusão de Turmas

**Data:** 20/11/2025  
**Responsável:** GitHub Copilot (Supervisor de Agentes)  
**Escopo:** módulos `turmas`, `matriculas`, `atividades`, `presencas`, `notas`, `pagamentos`, `core`, `relatorios_presenca`.

---

## 1. Objetivos

1. Garantir que as novas regras de bloqueio total, badges e reabertura funcionem em fluxo completo.
2. Validar regressão dos módulos dependentes (cadastros, matrículas, presenças, notas, pagamentos) diante das mudanças.
3. Certificar que a experiência do usuário esteja alinhada com o conteúdo atualizado do manual.

## 2. Estratégia Geral

- Utilizar **pytest/pytest-django** para cenários unitários e integrações rápidas (`.venv/Scripts/python -m pytest`).
- Executar **`python manage.py test`** direcionando apps específicos quando necessário.
- Manter o watcher Ruff desligado durante a bateria principal para evitar ruído, religando ao final.
- Testes divididos em três ondas para facilitar paralelismo:
  1. **Unitários focados em turmas** (`turmas/tests_encerramento.py`, futuros testes de services/views).
  2. **Módulos dependentes** (`matriculas`, `atividades`, `presencas`, `notas`, `pagamentos`).
  3. **Smoke E2E/Relatórios** para garantir que a UI reflita badges e bloqueios.

## 3. Casos Prioritários

| ID | Descrição | Tipo | Ferramenta |
| --- | --- | --- | --- |
| T-01 | Encerrar turma sem dependências → badge cinza, exclusão permitida | Unitário | pytest (turmas) |
| T-02 | Encerrar turma com dependências → badge vermelha, bloqueio total | Unitário | pytest (turmas) |
| T-03 | Reabrir turma com permissão `pode_reabrir_turma` → desbloqueio registrado | Unitário | pytest (turmas) |
| T-04 | Reabertura negada para usuário sem permissão | Unitário | pytest (turmas) |
| T-05 | Matrículas bloqueadas quando `bloqueio_total=True` | Unitário | pytest (matriculas) |
| T-06 | Registro de presença impedido para turma bloqueada | Unitário | pytest (presencas) |
| T-07 | Lançamento de notas/pagamentos em modo leitura | Unitário | pytest (notas/pagamentos) |
| T-08 | Exclusão direta de turma sem dependências continua funcionando | Unitário | pytest (turmas) |
| T-09 | Logs/auditoria preenchidos no encerramento e na reabertura | Unitário | pytest (turmas services) |
| T-10 | Templates exibem badge correta (snapshot simples) | Integração | Django TestCase |
| T-11 | Endpoints REST/serializers retornam erro HTTP apropriado em bloqueio | Integração | pytest + APIClient |
| T-12 | Smoke UI: fluxo de leitura em turma bloqueada permanece acessível | E2E | selenium/scripts existentes |

## 4. Sequência de Execução

1. **Preparação**
   - Ativar ambiente: `& .\.venv\Scripts\Activate.ps1`.
   - Aplicar migrações: `python manage.py migrate`.
   - Criar fixtures mínimas (turma ativa, encerrada, com vínculos).

2. **Onda 1 – Turmas**
   - `python -m pytest -q turmas/tests_encerramento.py`
   - Adicionar novos testes de service/view conforme necessário (arquivo `turmas/tests/test_bloqueios.py`).

3. **Onda 2 – Apps dependentes (executar em paralelo onde possível)**
   - `python -m pytest -q matriculas/tests` (ou `python manage.py test matriculas`).
   - `python -m pytest -q presencas/tests` (garantir cobertura de APIs).
   - `python -m pytest -q notas/tests` e `python -m pytest -q pagamentos/tests`.
   - `python -m pytest -q atividades/tests` para confirmar travas nos relacionamentos M2M.

4. **Onda 3 – Smoke/Integração**
   - `python scripts/run_smoke_tests.py` (já configurado na workspace).
   - `python manage.py test relatorios_presenca` (verificar filtros e badges nos relatórios).
   - Se necessário, rodar `pytest -q tests/e2e/test_pagamentos.py` para validar UI.

5. **Finalização**
   - Consolidar resultados, registrar falhas e reexecutar apenas o subconjunto afetado.
   - Rodar `ruff`/`black` somente após a bateria para evitar ruído.

## 5. Critérios de Aceite

- 100% dos casos T-01 a T-12 executados com sucesso.
- Nenhum erro em `scripts/run_smoke_tests.py` ou watchers relacionados.
- Logs (`logs/django.log`) sem stack traces relacionados aos novos bloqueios.
- Documentação atualizada (já realizado) alinhada com comportamento observado.

## 6. Observações

- Este plano complementa `docs/regras_encerramento_turmas_2025-11-20.md` e deve ser revisado após a implementação de testes adicionais.
- Manter backup do banco antes de smoke tests E2E.
- Em caso de instabilidade, priorizar rollback parcial para isolar o módulo impactado.
