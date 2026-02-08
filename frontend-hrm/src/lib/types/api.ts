/** Generic API response and pagination types matching backend */

export interface APIResponse<T> {
  success: boolean;
  message: string;
  data: T | null;
}

export interface APIErrorResponse {
  success: false;
  message: string;
  error_code?: string;
  details?: { field?: string; message: string; code?: string }[];
  timestamp?: string;
}

export interface PaginationMeta {
  page: number;
  per_page: number;
  total: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface PaginatedResponse<T> {
  success: boolean;
  message: string;
  data: T[];
  meta: PaginationMeta;
}

export interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface UserResponse {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
}

export type EmployeeType = "full_time" | "contract" | "intern" | "part_time";
export type Gender = "male" | "female" | "other" | "prefer_not_to_say";

export interface EmployeeResponse {
  id: number;
  employee_id: string;
  full_name: string;
  email: string;
  phone?: string | null;
  department?: string | null;
  department_id?: number | null;
  designation?: string | null;
  date_of_joining?: string | null;
  manager_id?: number | null;
  address?: string | null;
  emergency_contact_name?: string | null;
  emergency_contact_phone?: string | null;
  date_of_birth?: string | null;
  gender?: Gender | null;
  employee_type?: EmployeeType | null;
  is_active: boolean;
}

export interface EmployeeListResponse extends EmployeeResponse {
  total_present_days?: number;
  department_name?: string | null;
}

export interface DepartmentResponse {
  id: number;
  name: string;
  code: string;
  description?: string | null;
}

export type AttendanceStatus = "present" | "absent" | "half_day" | "on_leave" | "wfh";
export type AttendanceSource = "web" | "manual" | "biometric" | "api";

export interface AttendanceResponse {
  id: number;
  employee_id: number;
  date: string;
  status: AttendanceStatus;
  check_in_time?: string | null;
  check_out_time?: string | null;
  work_hours?: number | null;
  source?: AttendanceSource | null;
  notes?: string | null;
}

export interface AttendanceWithEmployeeResponse extends AttendanceResponse {
  employee_employee_id?: string | null;
  employee_full_name?: string | null;
}

export interface DashboardSummary {
  total_employees: number;
  total_attendance_records: number;
  present_count: number;
  absent_count: number;
  from_date?: string | null;
  to_date?: string | null;
}

export interface DepartmentSummary {
  departments: { name: string; employee_count: number }[];
}

export interface PermissionResponse {
  id: number;
  name: string;
  code: string;
  description?: string | null;
}

export interface RoleResponse {
  id: number;
  name: string;
  code: string;
  description?: string | null;
}

export interface RoleWithPermissionsResponse extends RoleResponse {
  permissions: PermissionResponse[];
}

export interface LeaveTypeResponse {
  id: number;
  name: string;
  code: string;
  default_days_per_year: number;
  description?: string | null;
}

export interface LeaveBalanceResponse {
  id: number;
  employee_id: number;
  leave_type_id: number;
  year: number;
  balance_days: number;
  used_days: number;
  employee_name?: string | null;
  leave_type_name?: string | null;
  available_days?: number;
}

export type LeaveRequestStatus = "pending" | "approved" | "rejected" | "cancelled";

export interface LeaveRequestResponse {
  id: number;
  employee_id: number;
  leave_type_id: number;
  from_date: string;
  to_date: string;
  status: LeaveRequestStatus;
  reason?: string | null;
  approved_by_id?: number | null;
  employee_name?: string | null;
  leave_type_name?: string | null;
  total_days?: number;
}

export interface HolidayResponse {
  id: number;
  name: string;
  date: string;
  year?: number | null;
  description?: string | null;
}

export interface CalendarLogsResponse {
  from_date: string;
  to_date: string;
  attendance_logs: {
    id: number;
    date: string;
    employee_id: number;
    employee_name?: string | null;
    employee_employee_id?: string | null;
    status: string;
    check_in_time?: string | null;
    check_out_time?: string | null;
    work_hours?: number | null;
    notes?: string | null;
  }[];
  holidays: { id: number; name: string; date: string; year?: number | null }[];
  leave: { id: number; employee_id: number; from_date: string; to_date: string; leave_type_id: number }[];
}
