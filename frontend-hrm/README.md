# HRMS Lite – Frontend

Next.js (App Router) frontend for HRMS Lite: dashboard, employee management, and attendance with dark/light theme and Shadcn UI.

## Tech Stack

- **Next.js 16** (App Router), **React 19**, **TypeScript**
- **Tailwind CSS 4**, **Shadcn UI**, **next-themes** (dark/light)
- **pnpm**

## Project Structure

```
frontend-hrm/
├── src/
│   ├── app/
│   │   ├── layout.tsx           # Root layout (Theme + Auth providers)
│   │   ├── page.tsx             # Redirect to /dashboard
│   │   ├── (auth)/login/        # Login page
│   │   └── (dashboard)/          # Protected routes
│   │       ├── layout.tsx       # Sidebar + header
│   │       ├── dashboard/       # Dashboard summary
│   │       ├── employees/       # List, add, delete; [id] detail page
│   │       ├── departments/    # List, add, delete departments
│   │       └── attendance/      # Mark attendance, list with filters
│   ├── components/
│   │   ├── ui/                  # Shadcn components
│   │   ├── providers/           # Theme, Auth
│   │   ├── layout/              # AppSidebar, AppHeader
│   │   ├── dashboard/            # SummaryCards, DepartmentList
│   │   ├── employees/           # EmployeeTable, AddEmployeeDialog
│   │   └── attendance/          # AttendanceTable, MarkAttendanceForm
│   └── lib/
│       ├── api/                 # client (fetch + refresh), endpoints
│       ├── types/               # API response types
│       └── utils.ts
├── Dockerfile
├── Makefile
└── README.md
```

## Features

- **Auth**: Login with email/password, JWT access + refresh token, auto-refresh on 401
- **Dashboard**: Summary cards (employees, attendance, present/absent), department list
- **Login guidance**: First-time users see default admin credentials on the login page (seeded by backend)
- **Employees**: List (paginated), add (extended form), delete, **detail page** (profile + attendance summary)
- **Departments**: List, add, delete departments
- **Attendance**: Mark attendance (employee, date, status), list with filters (date range, status)
- **UI**: Dark/light/system theme toggle, responsive layout, loading/empty/error states

## Default credentials (development & demo)

The backend seeds a default administrator. Use these to sign in:

- **Email**: `admin@hrms.local`
- **Password**: `admin123`

These are shown on the login page so new users can access the app without extra setup.

## Run Locally

### Prerequisites

- Node 20+, pnpm
- Backend running (e.g. `http://localhost:8000`)

### Commands

```bash
pnpm install
cp .env.local.example .env.local   # set NEXT_PUBLIC_API_URL if needed
pnpm dev
```

Open http://localhost:3000. Default admin: `admin@hrms.local` / `admin123`.

## Environment

- `NEXT_PUBLIC_API_URL` – Backend API base URL (default: `http://localhost:8000`)

## Run with Docker

Build and run (standalone output):

```bash
pnpm build
docker build -t hrms-frontend .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://backend:8000 hrms-frontend
```

Use the same network as the backend when using docker-compose.
