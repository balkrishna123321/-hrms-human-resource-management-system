"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import type { AttendanceWithEmployeeResponse } from "@/lib/types/api";
import type { PaginationMeta } from "@/lib/types/api";

interface AttendanceTableProps {
  records: AttendanceWithEmployeeResponse[];
  meta: PaginationMeta;
  onPageChange: (page: number) => void;
  loading?: boolean;
}

export function AttendanceTable({
  records,
  meta,
  onPageChange,
  loading,
}: AttendanceTableProps) {
  if (loading) {
    return (
      <div className="rounded-md border border-border">
        <div className="flex items-center justify-center py-12 text-muted-foreground">
          Loading...
        </div>
      </div>
    );
  }

  if (records.length === 0) {
    return (
      <div className="rounded-md border border-border">
        <div className="flex flex-col items-center justify-center py-12 text-center text-muted-foreground">
          <p>No attendance records.</p>
          <p className="text-sm">Mark attendance for employees from the form above.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="rounded-md border border-border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Date</TableHead>
              <TableHead>Employee ID</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Notes</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {records.map((r) => (
              <TableRow key={r.id}>
                <TableCell>{new Date(r.date).toLocaleDateString()}</TableCell>
                <TableCell className="font-mono text-sm">{r.employee_employee_id ?? r.employee_id}</TableCell>
                <TableCell>{r.employee_full_name ?? "—"}</TableCell>
                <TableCell>
                  <Badge variant={r.status === "present" ? "default" : "secondary"}>
                    {r.status === "present" ? "Present" : "Absent"}
                  </Badge>
                </TableCell>
                <TableCell className="max-w-[200px] truncate text-muted-foreground">
                  {r.notes ?? "—"}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      {meta.total_pages > 1 && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            Page {meta.page} of {meta.total_pages} ({meta.total} total)
          </p>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              disabled={!meta.has_prev}
              onClick={() => onPageChange(meta.page - 1)}
            >
              Previous
            </Button>
            <Button
              variant="outline"
              size="sm"
              disabled={!meta.has_next}
              onClick={() => onPageChange(meta.page + 1)}
            >
              Next
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
