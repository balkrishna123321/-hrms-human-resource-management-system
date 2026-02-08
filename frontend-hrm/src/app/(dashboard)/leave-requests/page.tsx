"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api/endpoints";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { LeaveRequestResponse } from "@/lib/types/api";
import { formatDate } from "@/utilities/format";
import { toast } from "sonner";

export default function LeaveRequestsPage() {
  const [requests, setRequests] = useState<LeaveRequestResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState<string>("");

  const fetchRequests = () => {
    setLoading(true);
    api.leaveRequests
      .list({ per_page: 50, status: statusFilter || undefined })
      .then((res) => setRequests(res.data))
      .catch(() => toast.error("Failed to load leave requests"))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchRequests();
  }, [statusFilter]);

  const handleApprove = async (id: number) => {
    try {
      await api.leaveRequests.update(id, { status: "approved" });
      toast.success("Leave approved");
      fetchRequests();
    } catch {
      toast.error("Failed to approve");
    }
  };

  const handleReject = async (id: number) => {
    try {
      await api.leaveRequests.update(id, { status: "rejected" });
      toast.success("Leave rejected");
      fetchRequests();
    } catch {
      toast.error("Failed to reject");
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold">Leave Requests</h1>
          <p className="text-muted-foreground">View and approve or reject leave applications.</p>
        </div>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="h-9 rounded-md border border-input bg-transparent px-3 text-sm"
        >
          <option value="">All statuses</option>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
          <option value="cancelled">Cancelled</option>
        </select>
      </div>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Employee</TableHead>
              <TableHead>Leave Type</TableHead>
              <TableHead>From</TableHead>
              <TableHead>To</TableHead>
              <TableHead>Days</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              <TableRow><TableCell colSpan={7} className="text-center py-8 text-muted-foreground">Loading...</TableCell></TableRow>
            ) : requests.length === 0 ? (
              <TableRow><TableCell colSpan={7} className="text-center py-8 text-muted-foreground">No leave requests.</TableCell></TableRow>
            ) : (
              requests.map((r) => (
                <TableRow key={r.id}>
                  <TableCell className="font-medium">{r.employee_name ?? `#${r.employee_id}`}</TableCell>
                  <TableCell>{r.leave_type_name ?? `#${r.leave_type_id}`}</TableCell>
                  <TableCell>{formatDate(r.from_date)}</TableCell>
                  <TableCell>{formatDate(r.to_date)}</TableCell>
                  <TableCell>{r.total_days ?? "—"}</TableCell>
                  <TableCell>
                    <Badge variant={r.status === "approved" ? "default" : r.status === "rejected" ? "destructive" : "secondary"}>{r.status}</Badge>
                  </TableCell>
                  <TableCell>
                    {r.status === "pending" && (
                      <div className="flex gap-2">
                        <Button size="sm" variant="outline" onClick={() => handleApprove(r.id)}>Approve</Button>
                        <Button size="sm" variant="destructive" onClick={() => handleReject(r.id)}>Reject</Button>
                      </div>
                    )}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
