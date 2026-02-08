"use client";

import Link from "next/link";
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
import { Trash2 } from "lucide-react";
import type { EmployeeListResponse } from "@/lib/types/api";
import type { PaginationMeta } from "@/lib/types/api";

interface EmployeeTableProps {
  employees: EmployeeListResponse[];
  meta: PaginationMeta;
  onPageChange: (page: number) => void;
  onDelete: (id: number, name: string) => void;
  loading?: boolean;
}

export function EmployeeTable({
  employees,
  meta,
  onPageChange,
  onDelete,
  loading,
}: EmployeeTableProps) {
  if (loading) {
    return (
      <div className="rounded-md border border-border">
        <div className="flex items-center justify-center py-12 text-muted-foreground">
          Loading...
        </div>
      </div>
    );
  }

  if (employees.length === 0) {
    return (
      <div className="rounded-md border border-border">
        <div className="flex flex-col items-center justify-center py-12 text-center text-muted-foreground">
          <p>No employees yet.</p>
          <p className="text-sm">Add your first employee to get started.</p>
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
              <TableHead>Employee ID</TableHead>
              <TableHead>Full Name</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Department</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="w-[80px]">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {employees.map((emp) => (
              <TableRow key={emp.id}>
                <TableCell className="font-mono text-sm">{emp.employee_id}</TableCell>
                <TableCell className="font-medium">
                  <Link href={`/employees/${emp.id}`} className="hover:underline text-primary">
                    {emp.full_name}
                  </Link>
                </TableCell>
                <TableCell>{emp.email}</TableCell>
                <TableCell>{emp.department}</TableCell>
                <TableCell>
                  <Badge variant={emp.is_active ? "default" : "secondary"}>
                    {emp.is_active ? "Active" : "Inactive"}
                  </Badge>
                </TableCell>
                <TableCell>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="text-destructive hover:text-destructive"
                    onClick={() => onDelete(emp.id, emp.full_name)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
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
