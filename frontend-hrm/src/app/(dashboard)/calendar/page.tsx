"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api/endpoints";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import type { CalendarLogsResponse } from "@/lib/types/api";
import { formatDate, formatTime } from "@/utilities/format";

export default function CalendarPage() {
  const today = new Date();
  const [fromDate, setFromDate] = useState(today.toISOString().slice(0, 10));
  const [toDate, setToDate] = useState(today.toISOString().slice(0, 10));
  const [data, setData] = useState<CalendarLogsResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchLogs = () => {
    setLoading(true);
    api.calendar
      .getLogs(fromDate, toDate)
      .then((res) => res.data && setData(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchLogs();
  }, [fromDate, toDate]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Calendar & Attendance Logs</h1>
        <p className="text-muted-foreground">View who logged in/out, working hours, holidays, and leave for a date range.</p>
      </div>
      <div className="flex flex-wrap items-end gap-4">
        <div className="space-y-2">
          <Label>From date</Label>
          <Input type="date" value={fromDate} onChange={(e) => setFromDate(e.target.value)} />
        </div>
        <div className="space-y-2">
          <Label>To date</Label>
          <Input type="date" value={toDate} onChange={(e) => setToDate(e.target.value)} />
        </div>
        <button
          type="button"
          onClick={fetchLogs}
          className="rounded-md bg-primary px-4 py-2 text-sm text-primary-foreground hover:bg-primary/90"
        >
          Refresh
        </button>
      </div>
      {loading && <p className="text-muted-foreground">Loading...</p>}
      {data && !loading && (
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Attendance Logs</CardTitle>
              <p className="text-sm text-muted-foreground">Check-in/out and work hours</p>
            </CardHeader>
            <CardContent>
              {data.attendance_logs.length === 0 ? (
                <p className="text-muted-foreground">No attendance records in this range.</p>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Date</TableHead>
                      <TableHead>Employee</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Check-in</TableHead>
                      <TableHead>Check-out</TableHead>
                      <TableHead>Hours</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {data.attendance_logs.map((a) => (
                      <TableRow key={a.id}>
                        <TableCell>{formatDate(a.date)}</TableCell>
                        <TableCell className="font-medium">{a.employee_name ?? a.employee_employee_id ?? a.employee_id}</TableCell>
                        <TableCell><Badge variant="secondary">{a.status}</Badge></TableCell>
                        <TableCell>{formatTime(a.check_in_time)}</TableCell>
                        <TableCell>{formatTime(a.check_out_time)}</TableCell>
                        <TableCell>{a.work_hours != null ? `${a.work_hours}h` : "—"}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Holidays & Leave</CardTitle>
              <p className="text-sm text-muted-foreground">Holidays and approved leave in range</p>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Holidays</p>
                  {data.holidays.length === 0 ? <p className="text-sm">None</p> : (
                    <ul className="list-inside list-disc text-sm">
                      {data.holidays.map((h) => (
                        <li key={h.id}>{h.name} – {formatDate(h.date)}</li>
                      ))}
                    </ul>
                  )}
                </div>
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Approved Leave</p>
                  {data.leave.length === 0 ? <p className="text-sm">None</p> : (
                    <ul className="list-inside list-disc text-sm">
                      {data.leave.map((l) => (
                        <li key={l.id}>Employee #{l.employee_id} – {formatDate(l.from_date)} to {formatDate(l.to_date)}</li>
                      ))}
                    </ul>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
