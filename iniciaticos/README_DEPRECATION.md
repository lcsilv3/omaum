# Depreciação do App `iniciaticos`

Este app serviu como camada de transição durante a extração/isolamento dos modelos iniciáticos (`TipoCodigo`, `Codigo`).

## Estado Atual
- Fonte de verdade dos modelos: `alunos.models.TipoCodigo` e `alunos.models.Codigo`.
- `iniciaticos.models` apenas reexporta essas classes (não declara novos `models.Model`).
- Admin legado removido (arquivo `iniciaticos/admin.py` neutro) para evitar `AlreadyRegistered`.
- Serviços e utilitários já priorizam `alunos`.

## Próximos Passos Recomendados
1. Remover importações diretas de `iniciaticos.models` nos módulos restantes.
2. Buscar por `from iniciaticos` e substituir por `from alunos`.
3. Excluir este app do `INSTALLED_APPS` após confirmar ausência de dependências (tests e produção).
4. Criar migration de limpeza (opcional) apenas se houver artefatos residuais.

## Racional
A dupla declaração anterior provocava conflitos (`models.E028`) e dificultava manutenção. A reexportação mantém compatibilidade enquanto código legado é atualizado gradualmente.

## Checklist de Remoção
- [x] Zero usos de `iniciaticos.` em código de produção.
- [x] Zero usos em testes.
- [ ] Deploy realizado sem o app (staging) com smoke tests verdes.
- [x] App removido de `INSTALLED_APPS` nesta branch (`refatoracao-alunos-performance`).

---
Gerado automaticamente como parte da fase de limpeza pós-refatoração.
