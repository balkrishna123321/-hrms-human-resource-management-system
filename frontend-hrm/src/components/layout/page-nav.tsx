"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { ChevronLeft, ChevronRight, Home } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useSidebar } from "./sidebar-context";

const pathLabels: Record<string, string> = {
  dashboard: "Dashboard",
  employees: "Employees",
  departments: "Departments",
  attendance: "Attendance",
  calendar: "Calendar",
  "leave-requests": "Leave Requests",
  "leave-balances": "Leave Balances",
  "leave-types": "Leave Types",
  holidays: "Holidays",
  roles: "Roles & Permissions",
};

function getBreadcrumbs(pathname: string): { segment: string; href: string; label: string }[] {
  const parts = pathname.split("/").filter(Boolean);
  const crumbs: { segment: string; href: string; label: string }[] = [];
  let acc = "";
  for (let i = 0; i < parts.length; i++) {
    acc += (acc ? "/" : "") + parts[i];
    const segment = parts[i];
    const label =
      pathLabels[segment] ??
      (segment && !/^\d+$/.test(segment) ? segment.replace(/-/g, " ") : segment);
    crumbs.push({ segment: parts[i], href: "/" + acc, label });
  }
  return crumbs;
}

export function PageNav() {
  const pathname = usePathname();
  const router = useRouter();
  const { setMobileOpen } = useSidebar();

  if (!pathname || pathname === "/login") return null;

  const crumbs = getBreadcrumbs(pathname);
  const canGoBack = crumbs.length > 1 || pathname !== "/dashboard";

  const handleBack = () => {
    setMobileOpen(false);
    if (crumbs.length > 1) {
      router.push(crumbs[crumbs.length - 2].href);
    } else {
      router.push("/dashboard");
    }
  };

  return (
    <div className="mb-4 flex flex-wrap items-center gap-2 text-sm">
      <Button
        variant="ghost"
        size="sm"
        className="gap-1 -ml-2"
        onClick={handleBack}
        style={{ visibility: canGoBack ? "visible" : "hidden" }}
      >
        <ChevronLeft className="h-4 w-4" />
        Back
      </Button>
      <nav className="flex items-center gap-1.5 text-muted-foreground" aria-label="Breadcrumb">
        <Link
          href="/dashboard"
          className="flex items-center gap-1 rounded px-1.5 py-0.5 transition-colors hover:text-foreground"
        >
          <Home className="h-4 w-4" />
          <span className="sr-only md:not-sr-only">Home</span>
        </Link>
        {crumbs.map((c, i) => (
          <span key={c.href} className="flex items-center gap-1.5">
            <ChevronRight className="h-3.5 w-3.5 opacity-50" />
            {i === crumbs.length - 1 ? (
              <span className="font-medium text-foreground capitalize">
                {/^\d+$/.test(c.segment) ? `#${c.segment}` : c.label}
              </span>
            ) : (
              <Link
                href={c.href}
                className="rounded px-1.5 py-0.5 transition-colors hover:text-foreground capitalize"
              >
                {c.label}
              </Link>
            )}
          </span>
        ))}
      </nav>
    </div>
  );
}
