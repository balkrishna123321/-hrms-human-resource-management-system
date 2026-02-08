"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { DepartmentSummary } from "@/lib/types/api";

export function DepartmentList({ data }: { data: DepartmentSummary }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Departments</CardTitle>
        <p className="text-sm text-muted-foreground">Employee count by department</p>
      </CardHeader>
      <CardContent>
        {data.departments.length === 0 ? (
          <p className="text-sm text-muted-foreground">No departments yet.</p>
        ) : (
          <ul className="space-y-2">
            {data.departments.map((d) => (
              <li
                key={d.name}
                className="flex items-center justify-between rounded-lg border border-border px-3 py-2"
              >
                <span className="font-medium">{d.name}</span>
                <span className="text-muted-foreground">{d.employee_count} employees</span>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}
