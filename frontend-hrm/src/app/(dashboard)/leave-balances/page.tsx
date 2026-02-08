"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api/endpoints";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { LeaveBalanceResponse } from "@/lib/types/api";
import { formatDays } from "@/utilities/format";

export default function LeaveBalancesPage() {
  const [balances, setBalances] = useState<LeaveBalanceResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [year, setYear] = useState(new Date().getFullYear());

  useEffect(() => {
    api.leaveBalances
      .list({ per_page: 100, year })
      .then((res) => setBalances(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [year]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold">Leave Balances</h1>
          <p className="text-muted-foreground">View leave balance and used days per employee per year.</p>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-sm text-muted-foreground">Year:</label>
          <input
            type="number"
            min={2000}
            max={2100}
            value={year}
            onChange={(e) => setYear(Number(e.target.value))}
            className="h-9 w-24 rounded-md border border-input bg-transparent px-3 text-sm"
          />
        </div>
      </div>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Employee</TableHead>
              <TableHead>Leave Type</TableHead>
              <TableHead>Year</TableHead>
              <TableHead>Balance</TableHead>
              <TableHead>Used</TableHead>
              <TableHead>Available</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              <TableRow><TableCell colSpan={6} className="text-center py-8 text-muted-foreground">Loading...</TableCell></TableRow>
            ) : balances.length === 0 ? (
              <TableRow><TableCell colSpan={6} className="text-center py-8 text-muted-foreground">No leave balances for this year.</TableCell></TableRow>
            ) : (
              balances.map((b) => (
                <TableRow key={b.id}>
                  <TableCell className="font-medium">{b.employee_name ?? `Employee #${b.employee_id}`}</TableCell>
                  <TableCell>{b.leave_type_name ?? `Type #${b.leave_type_id}`}</TableCell>
                  <TableCell>{b.year}</TableCell>
                  <TableCell>{formatDays(b.balance_days)}</TableCell>
                  <TableCell>{formatDays(b.used_days)}</TableCell>
                  <TableCell>{formatDays((b.available_days ?? b.balance_days - b.used_days))}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
