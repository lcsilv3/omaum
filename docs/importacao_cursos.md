# Importação da Tabela de Cursos

Este guia descreve o fluxo oficial para manter a tabela `Curso` sincronizada com a planilha mestre fornecida pela diretoria acadêmica. O processo pode ser realizado via script de linha de comando ou pela interface web administrativa.

## Pré-requisitos

- Aplicar as migrações (`python manage.py migrate cursos` ou `docker compose -f docker/docker-compose.yml exec omaum-web python manage.py migrate cursos`).
- Garantir que a planilha oficial esteja atualizada na pasta `docs/` (recomendado `Planilha de Cursos.csv` ou `Planilha de Cursos.xlsx`).
- Instalar a dependência `openpyxl` caso vá trabalhar com arquivos `.xlsx`.

## Estrutura da planilha

| Coluna           | Obrigatório | Descrição                                                                 |
| ---------------- | ----------- | ------------------------------------------------------------------------- |
| Nome             | Sim         | Nome do curso. Usado como chave principal quando o identificador não é informado. |
| Descricao        | Não         | Texto livre com a descrição do curso.                                     |
| Ativo            | Não         | Indica status do curso (`1`, `0`, `sim`, `nao`, `true`, `false`, etc.).    |
| Codigo / ID      | Não         | Identificador numérico do curso. Quando informado, prioriza a atualização pelo ID. |

Linhas sem `Nome` e sem `Codigo/ID` são ignoradas. Valores em branco são preservados conforme informados na planilha.

## Execução via script CLI

```bash
python scripts/manutencao/sincronizar_cursos.py
```

O script procura automaticamente `docs/Planilha de Cursos.csv` ou `docs/Planilha de Cursos.xlsx`. Ao final, é exibido um resumo com registros processados, criados, atualizados, reativados e desativados, além de avisos relevantes.

### Argumentos opcionais

- `--arquivo <caminho>`: utiliza um arquivo específico de cursos.
- `--manter-existentes`: evita desativar cursos que não estejam presentes na planilha.

Exemplo apontando para arquivo fora do repositório:

```bash
python scripts/manutencao/sincronizar_cursos.py --arquivo "C:/tmp/cursos.xlsx"
```

### Execução no container Docker

```bash
docker compose -f docker/docker-compose.yml exec omaum-web python scripts/manutencao/sincronizar_cursos.py
```

Adicione `--manter-existentes` quando quiser apenas inserir/atualizar dados sem inativar cursos ausentes.

## Importação pela interface web

A página `Cursos > Importar Cursos` aceita arquivos CSV ou XLSX com o mesmo cabeçalho descrito acima. A interface utiliza a mesma camada de serviço do script, porém **não** desativa cursos que estejam ausentes na planilha enviada (comportamento ideal para cargas incrementais).

Após enviar o arquivo, serão exibidos avisos sobre linhas ignoradas ou inconsistências detectadas. Revise os alertas antes de replicar o procedimento em produção.

## Boas práticas

1. Valide a planilha em ambiente de homologação antes de aplicar em produção.
2. Mantenha um backup (`python manage.py dumpdata cursos.Curso > cursos_backup.json`) antes de cargas massivas.
3. Documente no changelog interno a data da carga, origem do arquivo e usuário responsável.
4. Utilize o argumento `--manter-existentes` quando a planilha for parcial e não representar o catálogo completo de cursos.
