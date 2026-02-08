"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api/endpoints";
import { SummaryCards } from "@/components/dashboard/summary-cards";
import { DepartmentList } from "@/components/dashboard/department-list";
import type { DashboardSummary, DepartmentSummary } from "@/lib/types/api";

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [departments, setDepartments] = useState<DepartmentSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([api.dashboard.summary(), api.dashboard.departments()])
      .then(([sumRes, depRes]) => {
        if (sumRes.data) setSummary(sumRes.data as DashboardSummary);
        if (depRes.data) setDepartments(depRes.data as DepartmentSummary);
      })
      .catch((err) => setError(err?.message ?? "Failed to load dashboard"))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="space-y-8 animate-in fade-in-50 duration-300">
        <div>
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">Overview of employees and attendance</p>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-28 rounded-lg border bg-card animate-pulse" />
          ))}
        </div>
        <div className="grid gap-6 lg:grid-cols-2">
          <div className="h-64 rounded-lg border bg-card animate-pulse" />
          <div className="h-64 rounded-lg border bg-card animate-pulse" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <p className="text-destructive">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in-50 duration-300">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">Overview of employees and attendance</p>
      </div>
      {summary && <SummaryCards data={summary} />}
      {departments && (
        <div className="grid gap-6 lg:grid-cols-2">
          <DepartmentList data={departments} />
        </div>
      )}
    </div>
  );
}
