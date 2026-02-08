"use client";

import { useEffect, useState, useCallback } from "react";
import { api } from "@/lib/api/endpoints";
import { MarkAttendanceForm } from "@/components/attendance/mark-attendance-form";
import { AttendanceTable } from "@/components/attendance/attendance-table";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import type { AttendanceWithEmployeeResponse, PaginationMeta } from "@/lib/types/api";

export default function AttendancePage() {
  const [records, setRecords] = useState<AttendanceWithEmployeeResponse[]>([]);
  const [meta, setMeta] = useState<PaginationMeta | null>(null);
  const [page, setPage] = useState(1);
  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");
  const [status, setStatus] = useState<"" | "present" | "absent">("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAttendance = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.attendance.list({
        page,
        per_page: 20,
        from_date: fromDate || undefined,
        to_date: toDate || undefined,
        status: status || undefined,
      });
      setRecords(res.data);
      setMeta(res.meta);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load attendance");
    } finally {
      setLoading(false);
    }
  }, [page, fromDate, toDate, status]);

  useEffect(() => {
    fetchAttendance();
  }, [fetchAttendance]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Attendance</h1>
        <p className="text-muted-foreground">Mark and view attendance records</p>
      </div>

      <MarkAttendanceForm onSuccess={fetchAttendance} />

      <div className="flex flex-wrap items-end gap-4 rounded-lg border border-border p-4">
        <div className="space-y-2">
          <Label>From date</Label>
          <Input
            type="date"
            value={fromDate}
            onChange={(e) => setFromDate(e.target.value)}
          />
        </div>
        <div className="space-y-2">
          <Label>To date</Label>
          <Input
            type="date"
            value={toDate}
            onChange={(e) => setToDate(e.target.value)}
          />
        </div>
        <div className="space-y-2">
          <Label>Status</Label>
          <select
            className="flex h-9 w-[120px] rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
            value={status}
            onChange={(e) => setStatus(e.target.value as "" | "present" | "absent")}
          >
            <option value="">All</option>
            <option value="present">Present</option>
            <option value="absent">Absent</option>
          </select>
        </div>
        <button
          type="button"
          className="rounded-md border border-border px-3 py-2 text-sm hover:bg-accent"
          onClick={() => {
            setFromDate("");
            setToDate("");
            setStatus("");
            setPage(1);
          }}
        >
          Clear filters
        </button>
      </div>

      {error && <p className="text-destructive">{error}</p>}

      {!meta && loading && <p className="text-muted-foreground">Loading...</p>}
      {meta && (
        <AttendanceTable
          records={records}
          meta={meta}
          onPageChange={setPage}
          loading={loading}
        />
      )}
    </div>
  );
}
