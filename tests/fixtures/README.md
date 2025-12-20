# Fixtures de Teste

Este diretório contém arquivos JSON com dados de teste para o sistema OMAUM.

## Arquivos

- **dados_teste_gerados.json** - Dados de teste gerados automaticamente
- **dev_data_*.json** - Snapshots de dados do ambiente de desenvolvimento
- **dev_data_corrigido.json** - Dados de desenvolvimento após correções

## Uso

Estes arquivos podem ser usados para popular o banco de dados de teste:

```bash
python manage.py loaddata tests/fixtures/dados_teste_gerados.json
```

## Manutenção

- Não comitar dados sensíveis (senhas, CPFs reais, etc.)
- Manter dados atualizados com as migrações mais recentes
- Documentar estrutura de dados quando fizer mudanças significativas
