/** Application route paths */
export const ROUTES = {
  HOME: "/",
  LOGIN: "/login",
  DASHBOARD: "/dashboard",
  EMPLOYEES: "/employees",
  EMPLOYEE_DETAIL: (id: number) => `/employees/${id}`,
  DEPARTMENTS: "/departments",
  ATTENDANCE: "/attendance",
  ROLES: "/roles",
  PERMISSIONS: "/permissions",
  LEAVE_TYPES: "/leave-types",
  LEAVE_BALANCES: "/leave-balances",
  LEAVE_REQUESTS: "/leave-requests",
  HOLIDAYS: "/holidays",
  CALENDAR: "/calendar",
} as const;
