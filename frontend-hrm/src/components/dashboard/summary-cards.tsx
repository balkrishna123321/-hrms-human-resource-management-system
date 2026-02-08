"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Users, ClipboardList, CheckCircle, XCircle } from "lucide-react";
import type { DashboardSummary } from "@/lib/types/api";

export function SummaryCards({ data }: { data: DashboardSummary }) {
  const cards = [
    {
      title: "Total Employees",
      value: data.total_employees,
      icon: Users,
      desc: "Active employees",
    },
    {
      title: "Attendance Records",
      value: data.total_attendance_records,
      icon: ClipboardList,
      desc: "Total marked",
    },
    {
      title: "Present",
      value: data.present_count,
      icon: CheckCircle,
      desc: "Present days",
    },
    {
      title: "Absent",
      value: data.absent_count,
      icon: XCircle,
      desc: "Absent days",
    },
  ];

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {cards.map((c, i) => (
        <Card
          key={c.title}
          className="transition-all duration-300 hover:shadow-md animate-in fade-in-50 slide-in-from-bottom-4"
          style={{ animationDelay: `${i * 50}ms`, animationFillMode: "backwards" }}
        >
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{c.title}</CardTitle>
            <c.icon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold tabular-nums">{c.value}</div>
            <p className="text-xs text-muted-foreground">{c.desc}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
