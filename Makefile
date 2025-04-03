PROJECT_NAME=order-app
COMPOSE_DEV=docker compose -f docker-compose.yaml -f docker-compose.override.yaml -p $(PROJECT_NAME)
COMPOSE_PROD=docker compose -f docker-compose.yaml -p $(PROJECT_NAME)


sync:
	uv sync

build_dev: ## Builds the Docker images for development
	$(COMPOSE_DEV) build db
	$(COMPOSE_DEV) build backend
	$(COMPOSE_DEV) build redis
	$(COMPOSE_DEV) build migrate


run_dev: build_dev ## Starts the application in development mode with live reload
	$(COMPOSE_DEV) up -d

check_backend: ## Checks if the container backend is running
	@if docker ps --filter "name=backend" --format "{{.Names}}" | grep -q "^backend$$"; then \
		echo "The container 'backend' is running."; \
	else \
		echo "The container 'backend' is not running. Run \"make run_dev\" first"; \
		exit 1; \
	fi

migrate: check_backend
	@name=$(if $(word 2,$(MAKECMDGOALS)),$(word 2,$(MAKECMDGOALS)),update); \
	docker exec -it backend uv run -- alembic -c ../alembic.ini revision -m "$$name" --autogenerate

upgrade: check_backend
	docker exec -it backend uv run -- alembic -c ../alembic.ini upgrade head

downgrade: check_backend
	docker exec -it backend uv run -- alembic -c ../alembic.ini downgrade head

down: ## Stops all running containers
	$(COMPOSE_DEV) down

clean_db: ## Removes the database container and its associated volume
	@docker compose stop db || true
	@docker compose rm -f db || true
	@docker volume rm $$(docker volume ls -q --filter name=${PWD##*/}_postgres_data) || true

clean_all: clean_db ## Completely removes all containers, volumes, images, and orphaned services
	$(COMPOSE_DEV) down -v --rmi all --remove-orphans || true
	@docker volume prune -f || true

logs: ## Displays logs for the specified service
	$(COMPOSE_DEV) logs -f $(filter-out $@,$(MAKECMDGOALS))

test: check_backend ## Run tests
	docker exec -it backend uv run pytest

help: ## Lists all available Makefile commands with their descriptions
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

%:
	@: