"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api/endpoints";
import type { EmployeeListResponse } from "@/lib/types/api";
import { toast } from "sonner";

export function MarkAttendanceForm({ onSuccess }: { onSuccess: () => void }) {
  const [employees, setEmployees] = useState<EmployeeListResponse[]>([]);
  const [employeeId, setEmployeeId] = useState<string>("");
  const [date, setDate] = useState(() => new Date().toISOString().slice(0, 10));
  const [status, setStatus] = useState<"present" | "absent">("present");
  const [notes, setNotes] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [loadingEmployees, setLoadingEmployees] = useState(true);

  useEffect(() => {
    api.employees
      .list({ per_page: 500 })
      .then((res) => setEmployees(res.data))
      .catch(() => toast.error("Failed to load employees"))
      .finally(() => setLoadingEmployees(false));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!employeeId) {
      toast.error("Select an employee");
      return;
    }
    setSubmitting(true);
    try {
      await api.attendance.mark(Number(employeeId), { date, status, notes: notes || null });
      toast.success("Attendance marked");
      setNotes("");
      onSuccess();
    } catch (err: unknown) {
      toast.error(err instanceof Error ? err.message : "Failed to mark attendance");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Mark Attendance</CardTitle>
        <CardDescription>Select employee, date, and status (Present/Absent)</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="flex flex-wrap items-end gap-4">
          <div className="min-w-[200px] space-y-2">
            <Label>Employee</Label>
            <Select
              value={employeeId}
              onValueChange={setEmployeeId}
              disabled={loadingEmployees}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select employee" />
              </SelectTrigger>
              <SelectContent>
                {employees.map((e) => (
                  <SelectItem key={e.id} value={String(e.id)}>
                    {e.employee_id} – {e.full_name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <Label>Date</Label>
            <Input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              required
            />
          </div>
          <div className="min-w-[120px] space-y-2">
            <Label>Status</Label>
            <Select value={status} onValueChange={(v) => setStatus(v as "present" | "absent")}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="present">Present</SelectItem>
                <SelectItem value="absent">Absent</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="min-w-[180px] space-y-2">
            <Label>Notes (optional)</Label>
            <Input
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Optional notes"
            />
          </div>
          <Button type="submit" disabled={submitting}>
            {submitting ? "Saving..." : "Mark Attendance"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
