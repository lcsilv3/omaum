## App iniciaticos (Transição)

Este app concentra modelos de domínio iniciático (TipoCodigo, Codigo) antes residentes em `alunos.models`.

Estratégia de transição:
1. `db_table` preservado (`alunos_tipocodigo`, `alunos_codigo`) para evitar migração de dados imediata.
2. Próxima etapa: mover referências diretas em código para importar destes modelos.
3. `RegistroHistorico` permanece em `alunos` temporariamente; poderá migrar depois com mesma técnica (`db_table`).
4. Serviços centralizados em `alunos.services` já suportam busca dos modelos extraídos se presentes.

Checklist futuro:
- [ ] Substituir imports de `TipoCodigo` / `Codigo` em views/forms para o novo app.
- [ ] Adicionar testes de regressão cruzados.
- [ ] Criar endpoints REST específicos.
- [ ] Transferir `RegistroHistorico` (fase posterior).

Manter este arquivo atualizado durante a migração.
