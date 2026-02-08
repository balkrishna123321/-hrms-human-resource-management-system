# Contributing to HRMS Lite Frontend

Thank you for your interest in contributing. This document provides guidelines and setup steps.

## Development setup

1. **Prerequisites**: Node 20+, pnpm. Backend API running (e.g. `http://localhost:8000`).

2. **Clone and install**:
   ```bash
   cd frontend-hrm
   pnpm install
   cp .env.local.example .env.local
   ```

3. **Run the app**:
   ```bash
   pnpm dev
   ```
   Or use the Makefile: `make dev`.

   Open http://localhost:3000.

## Default login (for development)

The backend seeds a default administrator. Use these credentials to sign in:

- **Email**: `admin@hrms.local`
- **Password**: `admin123`

This is documented on the login page so new users and reviewers can access the app without separate setup.

## Project structure

- `src/app/` – Next.js App Router: (auth)/login, (dashboard)/dashboard, employees, departments, attendance.
- `src/components/` – UI (Shadcn), providers, layout, dashboard, employees, attendance.
- `src/lib/api/` – API client (auth, refresh), endpoints (auth, employees, departments, attendance, dashboard).
- `src/lib/types/` – API response and pagination types.

## Code style

- Use **ESLint** (and project config): `pnpm lint`.
- TypeScript strict; prefer typed API responses and props.

## Building for production

- `pnpm build` – Next.js production build (standalone output for Docker).
- Docker: image is built via root `docker-compose` using `frontend-hrm/Dockerfile`.
