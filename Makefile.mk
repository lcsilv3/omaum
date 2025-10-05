# Makefile para automação do projeto OmAum
.PHONY: help build up down logs shell test check backup restore migrate makemigrations createsuperuser collectstatic build-prod up-prod down-prod logs-prod backup-prod clean clean-all stats ps install reset

COMPOSE_FILE = docker/docker-compose.yml
COMPOSE_FILE_PROD = docker/docker-compose.prod.yml
PROJECT_NAME = omaum

help:
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Constrói as imagens Docker
	docker-compose -f $(COMPOSE_FILE) build

up: ## Sobe o ambiente de desenvolvimento
	@echo "🚀 Subindo o ambiente de desenvolvimento..."
	@docker-compose -f $(COMPOSE_FILE) up -d
	@echo "⏳ Aguardando a estabilização dos serviços (aprox. 15 segundos)..."
	@sleep 15
	@echo "🔍 Verificando o status da aplicação..."
	@if [ -z "$$(docker-compose -f $(COMPOSE_FILE) ps -q omaum-web)" ] || [ "$$(docker-compose -f $(COMPOSE_FILE) ps -q omaum-web | xargs docker inspect -f '{{.State.Status}}')" != "running" ]; then \
		echo "\n\033[31m❌ ERRO: A aplicação não conseguiu iniciar corretamente.\033[0m"; \
		echo "   Por favor, informe ao administrador e envie o resultado do seguinte comando:"; \
		echo "   \033[33mmake logs\033[0m\n"; \
	else \
		echo "\n\033[32m✅ Sucesso! O ambiente está no ar.\033[0m"; \
		echo "   Acesse a aplicação em: \033[36mhttp://localhost:8000\033[0m\n"; \
	fi

down: ## Para o ambiente de desenvolvimento
	docker-compose -f $(COMPOSE_FILE) down

logs: ## Mostra os logs dos containers
	docker-compose -f $(COMPOSE_FILE) logs -f

shell: ## Acessa o shell do container Django
	docker-compose -f $(COMPOSE_FILE) exec omaum-web bash

test: ## Executa os testes
	docker-compose -f $(COMPOSE_FILE) exec omaum-web python manage.py test

check: ## Verifica o projeto em busca de erros sem iniciar o servidor
	@echo "🔍 Verificando a integridade do projeto Django..."
	@docker-compose -f $(COMPOSE_FILE) run --rm omaum-web python manage.py check

migrate: ## Executa migrações
	docker-compose -f $(COMPOSE_FILE) exec omaum-web python manage.py migrate

makemigrations: ## Cria novas migrações
	docker-compose -f $(COMPOSE_FILE) exec omaum-web python manage.py makemigrations

createsuperuser: ## Cria um superusuário interativamente
	docker-compose -f $(COMPOSE_FILE) exec omaum-web python manage.py createsuperuser

collectstatic: ## Coleta arquivos estáticos
	docker-compose -f $(COMPOSE_FILE) exec omaum-web python manage.py collectstatic --noinput

build-prod: ## Constrói imagens para produção
	docker-compose -f $(COMPOSE_FILE_PROD) build

up-prod: ## Sobe ambiente de produção
	docker-compose -f $(COMPOSE_FILE_PROD) up -d

down-prod: ## Para ambiente de produção
	docker-compose -f $(COMPOSE_FILE_PROD) down

logs-prod: ## Logs do ambiente de produção
	docker-compose -f $(COMPOSE_FILE_PROD) logs -f

backup: ## Cria backup do banco de dados
	docker-compose -f $(COMPOSE_FILE) exec omaum-db pg_dump -U omaum_user omaum_dev > backup_$(shell date +%Y%m%d_%H%M%S).sql

backup-prod: ## Cria backup do banco de produção
	docker-compose -f $(COMPOSE_FILE_PROD) exec omaum-db pg_dump -U $(POSTGRES_USER) $(POSTGRES_DB) > backup_prod_$(shell date +%Y%m%d_%H%M%S).sql

restore: ## Restaura backup (uso: make restore FILE=backup.sql)
	docker-compose -f $(COMPOSE_FILE) exec -T omaum-db psql -U omaum_user omaum_dev < $(FILE)

clean: ## Remove containers, volumes e imagens não utilizados
	docker system prune -f
	docker volume prune -f

clean-all: ## Remove TUDO (cuidado!)
	docker-compose -f $(COMPOSE_FILE) down -v --rmi all
	docker system prune -af

stats: ## Mostra estatísticas dos containers
	docker stats

ps: ## Lista containers em execução
	docker-compose -f $(COMPOSE_FILE) ps

install: ## Instalação inicial do projeto
	cp docker/env/.env.example docker/env/.env.development
	make build
	make up
	sleep 10
	make migrate
	make collectstatic
	@echo "Projeto instalado! Acesse http://localhost:8000"

reset: ## Reset completo do ambiente de desenvolvimento
	make down
	docker volume rm omaum_db_data omaum_redis_data || true
	make up
	sleep 10
	make migrate
	make collectstatic
