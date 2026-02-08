# HRMS Lite - Root Makefile
# Run full stack: make up (uses backend-hrm/Dockerfile + frontend-hrm/Dockerfile via docker-compose)

.PHONY: up down build logs ps clean backend frontend postgres-only

# Start all services (Postgres + Backend + Frontend); each app uses its own Dockerfile
up:
	docker compose up -d

# Start with rebuild (e.g. after code changes; may use cached layers)
up-build:
	docker compose up -d --build

# Rebuild backend from scratch (no cache) and start — use after dependency/code changes
rebuild-backend:
	docker compose build --no-cache backend && docker compose up -d

# Rebuild all images from scratch and start
rebuild:
	docker compose build --no-cache && docker compose up -d

# Stop all services
down:
	docker compose down

# Build all images (uses Dockerfile in backend-hrm and frontend-hrm)
build:
	docker compose build

# View logs (all services)
logs:
	docker compose logs -f

# Backend logs only
logs-backend:
	docker compose logs -f backend

# Frontend logs only
logs-frontend:
	docker compose logs -f frontend

# List running services
ps:
	docker compose ps

# Stop and remove volumes
clean:
	docker compose down -v

# Start only Postgres (for local dev of backend/frontend)
postgres-only:
	docker compose up -d postgres

# Run backend locally (expects Postgres running)
backend:
	cd backend-hrm && $(MAKE) run

# Run frontend locally
frontend:
	cd frontend-hrm && $(MAKE) dev
