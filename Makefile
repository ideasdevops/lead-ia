.PHONY: build up down logs shell test clean

# Variables
DOCKER_COMPOSE = docker-compose
PROJECT_NAME = lead-ia

# Build de la imagen
build:
	$(DOCKER_COMPOSE) build

# Iniciar servicios
up:
	$(DOCKER_COMPOSE) up -d

# Detener servicios
down:
	$(DOCKER_COMPOSE) down

# Ver logs
logs:
	$(DOCKER_COMPOSE) logs -f

# Shell en el contenedor
shell:
	$(DOCKER_COMPOSE) exec app bash

# Ejecutar tests
test:
	$(DOCKER_COMPOSE) exec app python -m pytest

# Limpiar (detener y eliminar volúmenes)
clean:
	$(DOCKER_COMPOSE) down -v

# Rebuild completo
rebuild: clean build up

# Inicializar base de datos
init-db:
	$(DOCKER_COMPOSE) exec app /app/init-db.sh

# Ver estado de supervisor
supervisor-status:
	$(DOCKER_COMPOSE) exec app supervisorctl status

# Reiniciar servicios
restart:
	$(DOCKER_COMPOSE) restart

