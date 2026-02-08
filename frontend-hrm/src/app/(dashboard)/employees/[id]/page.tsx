"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api/endpoints";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import type { EmployeeResponse, AttendanceResponse } from "@/lib/types/api";
import { ArrowLeft } from "lucide-react";

export default function EmployeeDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = Number(params.id);
  const [employee, setEmployee] = useState<EmployeeResponse | null>(null);
  const [attendance, setAttendance] = useState<AttendanceResponse[]>([]);
  const [presentDays, setPresentDays] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (Number.isNaN(id)) {
      setError("Invalid employee ID");
      setLoading(false);
      return;
    }
    Promise.all([
      api.employees.get(id),
      api.attendance.listByEmployee(id, { per_page: 10 }),
      api.attendance.presentDays(id),
    ])
      .then(([empRes, attRes, daysRes]) => {
        if (empRes.data) setEmployee(empRes.data);
        if (attRes.data) setAttendance(attRes.data);
        if (daysRes.data?.present_days != null) setPresentDays(daysRes.data.present_days);
      })
      .catch((err) => setError(err?.message ?? "Failed to load employee"))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className="space-y-6">
        <p className="text-muted-foreground">Loading...</p>
      </div>
    );
  }

  if (error || !employee) {
    return (
      <div className="space-y-6">
        <p className="text-destructive">{error ?? "Employee not found"}</p>
        <Button variant="outline" asChild>
          <Link href="/employees">Back to Employees</Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" asChild>
          <Link href="/employees">
            <ArrowLeft className="h-4 w-4" />
          </Link>
        </Button>
        <div>
          <h1 className="text-2xl font-bold">{employee.full_name}</h1>
          <p className="text-muted-foreground">{employee.employee_id} · {employee.department ?? "—"}</p>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Profile</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm">
            <p><span className="text-muted-foreground">Email:</span> {employee.email}</p>
            {employee.phone && <p><span className="text-muted-foreground">Phone:</span> {employee.phone}</p>}
            {employee.designation && <p><span className="text-muted-foreground">Designation:</span> {employee.designation}</p>}
            {employee.date_of_joining && <p><span className="text-muted-foreground">Date of Joining:</span> {new Date(employee.date_of_joining).toLocaleDateString()}</p>}
            {employee.employee_type && <p><span className="text-muted-foreground">Type:</span> <Badge variant="secondary">{employee.employee_type.replace("_", " ")}</Badge></p>}
            <p><span className="text-muted-foreground">Status:</span> <Badge variant={employee.is_active ? "default" : "secondary"}>{employee.is_active ? "Active" : "Inactive"}</Badge></p>
            {employee.address && <p><span className="text-muted-foreground">Address:</span> {employee.address}</p>}
            {(employee.emergency_contact_name || employee.emergency_contact_phone) && (
              <p><span className="text-muted-foreground">Emergency:</span> {employee.emergency_contact_name ?? "—"} {employee.emergency_contact_phone ? `(${employee.emergency_contact_phone})` : ""}</p>
            )}
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Attendance Summary</CardTitle>
            <p className="text-sm text-muted-foreground">Total present days (all time)</p>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{presentDays ?? "—"}</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent Attendance</CardTitle>
          <p className="text-sm text-muted-foreground">Latest 10 records</p>
        </CardHeader>
        <CardContent>
          {attendance.length === 0 ? (
            <p className="text-muted-foreground">No attendance records yet.</p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Date</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Notes</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {attendance.map((a) => (
                  <TableRow key={a.id}>
                    <TableCell>{new Date(a.date).toLocaleDateString()}</TableCell>
                    <TableCell><Badge variant={a.status === "present" ? "default" : "secondary"}>{a.status}</Badge></TableCell>
                    <TableCell className="text-muted-foreground">{a.notes ?? "—"}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
