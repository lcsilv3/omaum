# Importação de Tipos e Códigos Iniciáticos

Este guia descreve o fluxo oficial para manter as tabelas `TipoCodigo` e `Codigo` sincronizadas com as planilhas-mestre disponibilizadas pela secretaria iniciática. O processo foi unificado no script `scripts/manutencao/limpar_e_importar_codigos.py`.

## Pré-requisitos

- Aplicar as migrações mais recentes (`python manage.py migrate alunos` ou `docker compose -f docker/docker-compose.yml exec omaum-web python manage.py migrate alunos`).
- Garantir que as planilhas oficiais estejam atualizadas na pasta `docs/`:
  - `Planilha Tipos de Códigos` (CSV ou XLSX).
  - `Planilha de Códigos` (CSV ou XLSX).
- Instalar a dependência `openpyxl` caso vá utilizar arquivos `.xlsx`.

## Formato das planilhas

### Planilha de Tipos

| Coluna | Descrição |
| --- | --- |
| A | Identificador numérico do tipo (inteiro, corresponde ao campo `id`). |
| B | Nome do tipo (obrigatório). |
| C | Descrição opcional. |

Linhas sem identificador ou nome são ignoradas. Tipos não presentes na planilha são automaticamente inativados no banco.

### Planilha de Códigos

| Coluna | Descrição |
| --- | --- |
| A | Número sequencial (ignorado pelo script; pode ficar vazio). |
| B | Identificador numérico do tipo (`tipo_id`). |
| C | Nome do tipo informado na planilha (usado para checagem de divergências). |
| D | Nome do código (obrigatório). |
| E | Descrição opcional do código. |

Se o `tipo_id` não existir entre os tipos previamente importados, o código é ignorado e um aviso é emitido. Códigos ausentes na planilha são marcados como inativos.

## Execução básica

```bash
python scripts/manutencao/limpar_e_importar_codigos.py
```

O script procura automaticamente as planilhas na pasta `docs/`. O resumo exibido ao final mostra quantos registros foram criados, atualizados, reativados, desativados e eventuais avisos/divergências.

## Argumentos opcionais

- `--apenas-tipos`: importa somente a planilha de tipos, sem tocar nos códigos.
- `--tipos-arquivo <caminho>`: utiliza um arquivo específico para os tipos.
- `--codigos-arquivo <caminho>`: utiliza um arquivo específico para os códigos.

Exemplo com caminhos customizados:

```bash
python scripts/manutencao/limpar_e_importar_codigos.py \
  --tipos-arquivo "C:/tmp/tipos.xlsx" \
  --codigos-arquivo "C:/tmp/codigos.csv"
```

## Fluxo recomendado

1. Aplicar as migrações (`python manage.py migrate alunos`).
2. Conferir se as planilhas oficiais estão atualizadas.
3. Executar o script de sincronização.
4. Revisar o resumo impresso (avisos e divergências).
5. Validar em ambiente de homologação antes de replicar a produção.

Seguindo esses passos, garantimos que a camada iniciática permaneça consistente e preparada para ativações/inativações controladas diretamente das planilhas oficiais.
