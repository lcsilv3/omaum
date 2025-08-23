## Importação de Municípios IBGE

Fluxo implementado:

1. Baixar pacote DTB e gerar CSV (o ano 2024 publica apenas planilhas XLS/ODS; o script converte automaticamente para CSV usando xlrd):
   ```bash
   source .venv/Scripts/activate
   python scripts/baixar_ibge_dtb.py --ano 2024 --dest docs/ibge_municipios.csv
   ```
2. Importar para o banco preenchendo `Cidade.codigo_ibge` e criando cidades ausentes:
   ```bash
   python manage.py importar_municipios_ibge --csv docs/ibge_municipios.csv
   ```

Opções:
* `--limit-uf SP RJ` importa só algumas UFs.
* `--dry-run` simula sem gravar.
* `--replace-names` renomeia cidade se código existir com nome diferente.

Exemplos:
```bash
python manage.py importar_municipios_ibge --limit-uf SP --dry-run
python manage.py importar_municipios_ibge --limit-uf SP RJ
```

Arquivo de download/conversão: `scripts/baixar_ibge_dtb.py` (stdlib + chardet + xlrd para XLS; opcional pandas/odfpy para ODS se um dia precisarmos).

Observações:
* 2024: só há `RELATORIO_DTB_BRASIL_2024_MUNICIPIOS.xls` (e .ods). O script detecta e converte.
* Dependência mínima extra: `xlrd` (adicionada na task de setup). Se falhar, instale manualmente: `pip install xlrd`.
