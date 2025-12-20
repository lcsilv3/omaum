# Scripts Docker

Scripts utilitários para gerenciamento dos ambientes Docker do projeto OMAUM.

## Scripts Disponíveis

### `iniciar_dev_docker.bat`
Inicia o ambiente de **desenvolvimento** na porta 8001.

```bash
cd docker
..\scripts\docker\iniciar_dev_docker.bat
```

### `iniciar_prod_docker.bat`
Inicia o ambiente de **produção** na porta 8000 (+ Nginx na porta 80).

```bash
cd docker
..\scripts\docker\iniciar_prod_docker.bat
```

### `parar_docker.bat`
Para **AMBOS** os ambientes (dev e prod) simultaneamente.

```bash
..\scripts\docker\parar_docker.bat
```

### `atualizar_docker.bat`
Para, reconstrói as imagens e reinicia o ambiente de **desenvolvimento**.

```bash
cd docker
..\scripts\docker\atualizar_docker.bat
```

### `testar_simultaneo.bat`
Script de diagnóstico para testar se ambos os ambientes podem rodar simultaneamente.

```bash
..\scripts\docker\testar_simultaneo.bat
```

## Documentação Relacionada

- [../docker/EXECUCAO_SIMULTANEA.md](../../docker/EXECUCAO_SIMULTANEA.md) - Guia completo de execução simultânea
- [../docs/architecture/DOCKER_AMBIENTES.md](../../docs/architecture/DOCKER_AMBIENTES.md) - Arquitetura Docker
