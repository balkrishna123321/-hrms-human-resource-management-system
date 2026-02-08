"use client";

import { useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  Users,
  Building2,
  ClipboardList,
  Calendar,
  FileText,
  Scale,
  CalendarDays,
  Gift,
  Shield,
  ChevronDown,
  ChevronRight,
  PanelLeftClose,
  PanelLeft,
  X,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { useSidebar } from "./sidebar-context";

const navGroups = [
  {
    label: "Main",
    items: [{ href: "/dashboard", label: "Dashboard", icon: LayoutDashboard }],
  },
  {
    label: "People",
    items: [
      { href: "/employees", label: "Employees", icon: Users },
      { href: "/departments", label: "Departments", icon: Building2 },
    ],
  },
  {
    label: "Time & Attendance",
    items: [
      { href: "/attendance", label: "Attendance", icon: ClipboardList },
      { href: "/calendar", label: "Calendar & Logs", icon: Calendar },
    ],
  },
  {
    label: "Leave",
    items: [
      { href: "/leave-requests", label: "Leave Requests", icon: FileText },
      { href: "/leave-balances", label: "Leave Balances", icon: Scale },
      { href: "/leave-types", label: "Leave Types", icon: CalendarDays },
    ],
  },
  {
    label: "Settings",
    items: [
      { href: "/holidays", label: "Holidays", icon: Gift },
      { href: "/roles", label: "Roles & Permissions", icon: Shield },
    ],
  },
];

function NavContent({ collapsed }: { collapsed: boolean }) {
  const pathname = usePathname();
  const [openGroups, setOpenGroups] = useState<Record<string, boolean>>({
    Leave: true,
    People: true,
  });

  const toggleGroup = (label: string) => {
    setOpenGroups((p) => ({ ...p, [label]: !p[label] }));
  };

  return (
    <nav className="flex flex-1 flex-col gap-1 p-3">
      {navGroups.map((group) => {
        const isOpen = openGroups[group.label] ?? false;
        const hasSub = group.items.length > 1;

        return (
          <div key={group.label} className="space-y-0.5">
            {collapsed ? (
              group.items.map((item) => {
                const isActive =
                  pathname === item.href || pathname.startsWith(item.href + "/");
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    title={item.label}
                    className={cn(
                      "flex items-center justify-center rounded-lg px-2 py-2.5 text-sm font-medium transition-all duration-200",
                      isActive
                        ? "bg-primary text-primary-foreground"
                        : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                    )}
                  >
                    <item.icon className="h-5 w-5 shrink-0" />
                  </Link>
                );
              })
            ) : (
              <>
                {hasSub && (
                  <button
                    type="button"
                    onClick={() => toggleGroup(group.label)}
                    className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-left text-xs font-medium uppercase tracking-wider text-muted-foreground transition-colors hover:bg-accent/50 hover:text-accent-foreground"
                  >
                    {isOpen ? (
                      <ChevronDown className="h-4 w-4 shrink-0" />
                    ) : (
                      <ChevronRight className="h-4 w-4 shrink-0" />
                    )}
                    <span className="truncate">{group.label}</span>
                  </button>
                )}
                <div
                  className={cn(
                    "grid transition-all duration-200 ease-in-out",
                    hasSub && !collapsed
                      ? isOpen
                        ? "grid-rows-[1fr] opacity-100"
                        : "grid-rows-[0fr] opacity-0"
                      : "grid-rows-[1fr]"
                  )}
                >
                  <div className="overflow-hidden">
                    <div className="space-y-0.5 py-0.5">
                      {group.items.map((item) => {
                        const isActive =
                          pathname === item.href ||
                          pathname.startsWith(item.href + "/");
                        return (
                          <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                              "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-all duration-200",
                              isActive
                                ? "bg-primary text-primary-foreground"
                                : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                            )}
                          >
                            <item.icon className="h-5 w-5 shrink-0" />
                            {!collapsed && (
                              <span className="truncate">{item.label}</span>
                            )}
                          </Link>
                        );
                      })}
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>
        );
      })}
    </nav>
  );
}

export function AppSidebar() {
  const pathname = usePathname();
  const { mobileOpen, setMobileOpen, collapsed, toggleCollapsed } = useSidebar();

  useEffect(() => {
    setMobileOpen(false);
  }, [pathname, setMobileOpen]);

  const sidebarContent = (
    <>
      <div className="flex h-14 shrink-0 items-center justify-between border-b border-sidebar-border px-3 gap-1">
        {collapsed ? (
          <Link
            href="/dashboard"
            className="flex size-9 items-center justify-center rounded-lg hover:bg-accent"
            title="HRMS Lite"
          >
            <LayoutDashboard className="h-5 w-5" />
          </Link>
        ) : (
          <Link href="/dashboard" className="text-base font-semibold truncate">
            HRMS Lite
          </Link>
        )}
        <div className="flex items-center gap-0.5">
          <Button
            variant="ghost"
            size="icon"
            className="hidden md:flex shrink-0"
            onClick={toggleCollapsed}
            title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          >
            {collapsed ? (
              <PanelLeft className="h-5 w-5" />
            ) : (
              <PanelLeftClose className="h-5 w-5" />
            )}
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden shrink-0"
            onClick={() => setMobileOpen(false)}
            title="Close menu"
          >
            <X className="h-5 w-5" />
          </Button>
        </div>
      </div>
      <NavContent collapsed={collapsed} />
    </>
  );

  return (
    <>
      {/* Desktop sidebar */}
      <aside
        className={cn(
          "hidden md:flex h-full flex-col border-r border-sidebar-border bg-card transition-all duration-300 ease-in-out",
          collapsed ? "w-16" : "w-64"
        )}
      >
        {sidebarContent}
      </aside>

      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm md:hidden animate-in fade-in-0 duration-200"
          onClick={() => setMobileOpen(false)}
          onKeyDown={(e) => e.key === "Escape" && setMobileOpen(false)}
          role="button"
          tabIndex={0}
          aria-label="Close menu"
        />
      )}

      {/* Mobile drawer */}
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-50 flex w-72 max-w-[85vw] flex-col border-r border-sidebar-border bg-card shadow-xl transition-transform duration-300 ease-out md:hidden",
          mobileOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        {sidebarContent}
      </aside>
    </>
  );
}
