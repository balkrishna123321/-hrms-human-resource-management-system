# HRMS Lite - Frontend (Next.js)
# Docker: built via root docker-compose (build context: ., dockerfile: Dockerfile)

.PHONY: dev build install lint docker-build

# Install dependencies
install:
	pnpm install

# Run dev server
dev:
	pnpm dev

# Production build
build:
	pnpm build

# Lint
lint:
	pnpm lint

# Build Docker image (same Dockerfile used by root docker-compose)
docker-build:
	docker build -t hrms-frontend .
