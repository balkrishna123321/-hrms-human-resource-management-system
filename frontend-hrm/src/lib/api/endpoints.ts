/** API endpoint functions using the api client */

import {
  apiGet,
  apiPost,
  apiPatch,
  apiDelete,
} from "./client";
import type {
  APIResponse,
  PaginatedResponse,
  TokenPair,
  UserResponse,
  EmployeeResponse,
  EmployeeListResponse,
  DepartmentResponse,
  AttendanceResponse,
  AttendanceWithEmployeeResponse,
  DashboardSummary,
  DepartmentSummary,
  PermissionResponse,
  RoleWithPermissionsResponse,
  LeaveTypeResponse,
  LeaveBalanceResponse,
  LeaveRequestResponse,
  HolidayResponse,
  CalendarLogsResponse,
} from "@/lib/types/api";

const auth = {
  login: (email: string, password: string) =>
    apiPost<APIResponse<TokenPair>>("/api/v1/auth/login", { email, password }, { skipAuth: true }),

  refresh: (refresh_token: string) =>
    apiPost<APIResponse<TokenPair>>("/api/v1/auth/refresh", { refresh_token }, { skipAuth: true }),

  me: () => apiGet<APIResponse<UserResponse>>("/api/v1/auth/me"),
};

const employees = {
  list: (params?: {
    page?: number;
    per_page?: number;
    department?: string;
    department_id?: number;
    is_active?: boolean;
  }) => {
    const sp = new URLSearchParams();
    if (params?.page != null) sp.set("page", String(params.page));
    if (params?.per_page != null) sp.set("per_page", String(params.per_page));
    if (params?.department) sp.set("department", params.department);
    if (params?.department_id != null) sp.set("department_id", String(params.department_id));
    if (params?.is_active != null) sp.set("is_active", String(params.is_active));
    const q = sp.toString();
    return apiGet<PaginatedResponse<EmployeeListResponse>>(
      `/api/v1/employees${q ? `?${q}` : ""}`
    );
  },

  get: (id: number) =>
    apiGet<APIResponse<EmployeeResponse>>(`/api/v1/employees/${id}`),

  create: (body: Partial<{
    employee_id: string;
    full_name: string;
    email: string;
    phone: string;
    department: string;
    department_id: number;
    designation: string;
    date_of_joining: string;
    manager_id: number;
    address: string;
    emergency_contact_name: string;
    emergency_contact_phone: string;
    date_of_birth: string;
    gender: string;
    employee_type: string;
  }>) => apiPost<APIResponse<EmployeeResponse>>("/api/v1/employees", body),

  update: (id: number, body: Partial<EmployeeResponse>) =>
    apiPatch<APIResponse<EmployeeResponse>>(`/api/v1/employees/${id}`, body),

  delete: (id: number) => apiDelete(`/api/v1/employees/${id}`),
};

const departments = {
  list: (params?: { page?: number; per_page?: number }) => {
    const sp = new URLSearchParams();
    if (params?.page != null) sp.set("page", String(params.page));
    if (params?.per_page != null) sp.set("per_page", String(params.per_page));
    const q = sp.toString();
    return apiGet<PaginatedResponse<DepartmentResponse>>(
      `/api/v1/departments${q ? `?${q}` : ""}`
    );
  },

  get: (id: number) =>
    apiGet<APIResponse<DepartmentResponse>>(`/api/v1/departments/${id}`),

  create: (body: { name: string; code: string; description?: string | null }) =>
    apiPost<APIResponse<DepartmentResponse>>("/api/v1/departments", body),

  update: (id: number, body: Partial<{ name: string; code: string; description?: string | null }>) =>
    apiPatch<APIResponse<DepartmentResponse>>(`/api/v1/departments/${id}`, body),

  delete: (id: number) => apiDelete(`/api/v1/departments/${id}`),
};

const attendance = {
  list: (params?: {
    page?: number;
    per_page?: number;
    from_date?: string;
    to_date?: string;
    status?: "present" | "absent";
    department?: string;
  }) => {
    const sp = new URLSearchParams();
    if (params?.page != null) sp.set("page", String(params.page));
    if (params?.per_page != null) sp.set("per_page", String(params.per_page));
    if (params?.from_date) sp.set("from_date", params.from_date);
    if (params?.to_date) sp.set("to_date", params.to_date);
    if (params?.status) sp.set("status", params.status);
    if (params?.department) sp.set("department", params.department);
    const q = sp.toString();
    return apiGet<PaginatedResponse<AttendanceWithEmployeeResponse>>(
      `/api/v1/attendance${q ? `?${q}` : ""}`
    );
  },

  listByEmployee: (
    employeeId: number,
    params?: { page?: number; per_page?: number; from_date?: string; to_date?: string; status?: "present" | "absent" }
  ) => {
    const sp = new URLSearchParams();
    if (params?.page != null) sp.set("page", String(params.page));
    if (params?.per_page != null) sp.set("per_page", String(params.per_page));
    if (params?.from_date) sp.set("from_date", params.from_date);
    if (params?.to_date) sp.set("to_date", params.to_date);
    if (params?.status) sp.set("status", params.status);
    const q = sp.toString();
    return apiGet<PaginatedResponse<AttendanceResponse>>(
      `/api/v1/attendance/employee/${employeeId}${q ? `?${q}` : ""}`
    );
  },

  presentDays: (employeeId: number, from_date?: string, to_date?: string) => {
    const sp = new URLSearchParams();
    if (from_date) sp.set("from_date", from_date);
    if (to_date) sp.set("to_date", to_date);
    const q = sp.toString();
    return apiGet<APIResponse<{ employee_id: number; present_days: number }>>(
      `/api/v1/attendance/employee/${employeeId}/present-days${q ? `?${q}` : ""}`
    );
  },

  mark: (employeeId: number, body: { date: string; status: AttendanceResponse["status"]; notes?: string | null }) =>
    apiPost<APIResponse<AttendanceResponse>>(
      `/api/v1/attendance/employee/${employeeId}`,
      body
    ),

  update: (id: number, body: Partial<{ status: AttendanceResponse["status"]; notes?: string | null }>) =>
    apiPatch<APIResponse<AttendanceResponse>>(`/api/v1/attendance/${id}`, body),

  delete: (id: number) => apiDelete(`/api/v1/attendance/${id}`),
};

const dashboard = {
  summary: (from_date?: string, to_date?: string) => {
    const sp = new URLSearchParams();
    if (from_date) sp.set("from_date", from_date);
    if (to_date) sp.set("to_date", to_date);
    const q = sp.toString();
    return apiGet<APIResponse<DashboardSummary>>(
      `/api/v1/dashboard/summary${q ? `?${q}` : ""}`
    );
  },

  departments: () =>
    apiGet<APIResponse<DepartmentSummary>>("/api/v1/dashboard/departments"),
};

const permissions = {
  list: () => apiGet<APIResponse<PermissionResponse[]>>("/api/v1/permissions"),
  create: (body: { name: string; code: string; description?: string | null }) =>
    apiPost<APIResponse<PermissionResponse>>("/api/v1/permissions", body),
};

const roles = {
  list: (params?: { page?: number; per_page?: number }) => {
    const sp = new URLSearchParams();
    if (params?.page != null) sp.set("page", String(params.page));
    if (params?.per_page != null) sp.set("per_page", String(params.per_page));
    const q = sp.toString();
    return apiGet<PaginatedResponse<RoleWithPermissionsResponse>>(`/api/v1/roles${q ? `?${q}` : ""}`);
  },
  get: (id: number) => apiGet<APIResponse<RoleWithPermissionsResponse>>(`/api/v1/roles/${id}`),
  create: (body: { name: string; code: string; description?: string | null; permission_ids?: number[] }) =>
    apiPost<APIResponse<RoleWithPermissionsResponse>>("/api/v1/roles", body),
  update: (id: number, body: Partial<{ name: string; code: string; description?: string | null; permission_ids?: number[] }>) =>
    apiPatch<APIResponse<RoleWithPermissionsResponse>>(`/api/v1/roles/${id}`, body),
  delete: (id: number) => apiDelete(`/api/v1/roles/${id}`),
};

const leaveTypes = {
  list: (params?: { page?: number; per_page?: number }) => {
    const sp = new URLSearchParams();
    if (params?.page != null) sp.set("page", String(params.page));
    if (params?.per_page != null) sp.set("per_page", String(params.per_page));
    const q = sp.toString();
    return apiGet<PaginatedResponse<LeaveTypeResponse>>(`/api/v1/leave-types${q ? `?${q}` : ""}`);
  },
  get: (id: number) => apiGet<APIResponse<LeaveTypeResponse>>(`/api/v1/leave-types/${id}`),
  create: (body: { name: string; code: string; default_days_per_year?: number; description?: string | null }) =>
    apiPost<APIResponse<LeaveTypeResponse>>("/api/v1/leave-types", body),
  update: (id: number, body: Partial<LeaveTypeResponse>) =>
    apiPatch<APIResponse<LeaveTypeResponse>>(`/api/v1/leave-types/${id}`, body),
  delete: (id: number) => apiDelete(`/api/v1/leave-types/${id}`),
};

const leaveBalances = {
  list: (params?: { page?: number; per_page?: number; employee_id?: number; year?: number }) => {
    const sp = new URLSearchParams();
    if (params?.page != null) sp.set("page", String(params.page));
    if (params?.per_page != null) sp.set("per_page", String(params.per_page));
    if (params?.employee_id != null) sp.set("employee_id", String(params.employee_id));
    if (params?.year != null) sp.set("year", String(params.year));
    const q = sp.toString();
    return apiGet<PaginatedResponse<LeaveBalanceResponse>>(`/api/v1/leave-balances${q ? `?${q}` : ""}`);
  },
  getByEmployee: (employeeId: number, year: number) =>
    apiGet<APIResponse<LeaveBalanceResponse[]>>(`/api/v1/leave-balances/employee/${employeeId}?year=${year}`),
  create: (body: { employee_id: number; leave_type_id: number; year: number; balance_days?: number; used_days?: number }) =>
    apiPost<APIResponse<LeaveBalanceResponse>>("/api/v1/leave-balances", body),
  update: (id: number, body: { balance_days?: number; used_days?: number }) =>
    apiPatch<APIResponse<LeaveBalanceResponse>>(`/api/v1/leave-balances/${id}`, body),
};

const leaveRequests = {
  list: (params?: { page?: number; per_page?: number; employee_id?: number; status?: string; from_date?: string; to_date?: string }) => {
    const sp = new URLSearchParams();
    if (params?.page != null) sp.set("page", String(params.page));
    if (params?.per_page != null) sp.set("per_page", String(params.per_page));
    if (params?.employee_id != null) sp.set("employee_id", String(params.employee_id));
    if (params?.status) sp.set("status", params.status);
    if (params?.from_date) sp.set("from_date", params.from_date);
    if (params?.to_date) sp.set("to_date", params.to_date);
    const q = sp.toString();
    return apiGet<PaginatedResponse<LeaveRequestResponse>>(`/api/v1/leave-requests${q ? `?${q}` : ""}`);
  },
  get: (id: number) => apiGet<APIResponse<LeaveRequestResponse>>(`/api/v1/leave-requests/${id}`),
  create: (employeeId: number, body: { leave_type_id: number; from_date: string; to_date: string; reason?: string | null }) =>
    apiPost<APIResponse<LeaveRequestResponse>>(`/api/v1/leave-requests/employee/${employeeId}`, body),
  update: (id: number, body: { status?: string; reason?: string | null }) =>
    apiPatch<APIResponse<LeaveRequestResponse>>(`/api/v1/leave-requests/${id}`, body),
};

const holidays = {
  list: (params?: { page?: number; per_page?: number; year?: number; from_date?: string; to_date?: string }) => {
    const sp = new URLSearchParams();
    if (params?.page != null) sp.set("page", String(params.page));
    if (params?.per_page != null) sp.set("per_page", String(params.per_page));
    if (params?.year != null) sp.set("year", String(params.year));
    if (params?.from_date) sp.set("from_date", params.from_date);
    if (params?.to_date) sp.set("to_date", params.to_date);
    const q = sp.toString();
    return apiGet<PaginatedResponse<HolidayResponse>>(`/api/v1/holidays${q ? `?${q}` : ""}`);
  },
  get: (id: number) => apiGet<APIResponse<HolidayResponse>>(`/api/v1/holidays/${id}`),
  create: (body: { name: string; date: string; year?: number | null; description?: string | null }) =>
    apiPost<APIResponse<HolidayResponse>>("/api/v1/holidays", body),
  update: (id: number, body: Partial<HolidayResponse>) =>
    apiPatch<APIResponse<HolidayResponse>>(`/api/v1/holidays/${id}`, body),
  delete: (id: number) => apiDelete(`/api/v1/holidays/${id}`),
};

const calendar = {
  getLogs: (from_date: string, to_date: string) =>
    apiGet<APIResponse<CalendarLogsResponse>>(`/api/v1/calendar/logs?from_date=${from_date}&to_date=${to_date}`),
};

export const api = {
  auth,
  employees,
  departments,
  attendance,
  dashboard,
  permissions,
  roles,
  leaveTypes,
  leaveBalances,
  leaveRequests,
  holidays,
  calendar,
};
