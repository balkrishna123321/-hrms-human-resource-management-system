"use client";

import { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Plus } from "lucide-react";
import { api } from "@/lib/api/endpoints";
import type { DepartmentResponse } from "@/lib/types/api";
import { toast } from "sonner";

interface AddEmployeeDialogProps {
  onSuccess: () => void;
}

const initialForm = {
  employee_id: "",
  full_name: "",
  email: "",
  phone: "",
  department: "",
  department_id: undefined as number | undefined,
  designation: "",
  date_of_joining: "",
  address: "",
  emergency_contact_name: "",
  emergency_contact_phone: "",
  date_of_birth: "",
  employee_type: "full_time" as const,
};

export function AddEmployeeDialog({ onSuccess }: AddEmployeeDialogProps) {
  const [open, setOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [form, setForm] = useState(initialForm);
  const [departments, setDepartments] = useState<DepartmentResponse[]>([]);

  useEffect(() => {
    if (open) {
      api.departments
        .list({ per_page: 100 })
        .then((res) => setDepartments(res.data))
        .catch(() => {});
    }
  }, [open]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await api.employees.create({
        employee_id: form.employee_id,
        full_name: form.full_name,
        email: form.email,
        phone: form.phone || undefined,
        department: form.department || undefined,
        department_id: form.department_id,
        designation: form.designation || undefined,
        date_of_joining: form.date_of_joining || undefined,
        address: form.address || undefined,
        emergency_contact_name: form.emergency_contact_name || undefined,
        emergency_contact_phone: form.emergency_contact_phone || undefined,
        date_of_birth: form.date_of_birth || undefined,
        employee_type: form.employee_type,
      });
      setForm(initialForm);
      setOpen(false);
      onSuccess();
      toast.success("Employee created");
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Failed to create employee";
      toast.error(message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Add Employee
        </Button>
      </DialogTrigger>
      <DialogContent className="max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Add Employee</DialogTitle>
          <DialogDescription>
            Create a new employee record. Employee ID and email must be unique. You can link a department or enter a department name.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="employee_id">Employee ID *</Label>
              <Input
                id="employee_id"
                value={form.employee_id}
                onChange={(e) => setForm((p) => ({ ...p, employee_id: e.target.value }))}
                placeholder="EMP001"
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="designation">Designation</Label>
              <Input
                id="designation"
                value={form.designation}
                onChange={(e) => setForm((p) => ({ ...p, designation: e.target.value }))}
                placeholder="Software Engineer"
              />
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="full_name">Full Name *</Label>
            <Input
              id="full_name"
              value={form.full_name}
              onChange={(e) => setForm((p) => ({ ...p, full_name: e.target.value }))}
              placeholder="John Doe"
              required
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email *</Label>
              <Input
                id="email"
                type="email"
                value={form.email}
                onChange={(e) => setForm((p) => ({ ...p, email: e.target.value }))}
                placeholder="john@company.com"
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="phone">Phone</Label>
              <Input
                id="phone"
                value={form.phone}
                onChange={(e) => setForm((p) => ({ ...p, phone: e.target.value }))}
                placeholder="+1 234 567 8900"
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Department (link)</Label>
              <Select
                value={form.department_id != null ? String(form.department_id) : "none"}
                onValueChange={(v) =>
                  setForm((p) => ({
                    ...p,
                    department_id: v === "none" ? undefined : Number(v),
                    department: v === "none" ? p.department : departments.find((d) => d.id === Number(v))?.name ?? p.department,
                  }))
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select department" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="none">None</SelectItem>
                  {departments.map((d) => (
                    <SelectItem key={d.id} value={String(d.id)}>
                      {d.code} – {d.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="department">Department (name, if not linked)</Label>
              <Input
                id="department"
                value={form.department}
                onChange={(e) => setForm((p) => ({ ...p, department: e.target.value }))}
                placeholder="Engineering"
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="date_of_joining">Date of Joining</Label>
              <Input
                id="date_of_joining"
                type="date"
                value={form.date_of_joining}
                onChange={(e) => setForm((p) => ({ ...p, date_of_joining: e.target.value }))}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="date_of_birth">Date of Birth</Label>
              <Input
                id="date_of_birth"
                type="date"
                value={form.date_of_birth}
                onChange={(e) => setForm((p) => ({ ...p, date_of_birth: e.target.value }))}
              />
            </div>
          </div>
          <div className="space-y-2">
            <Label>Employment Type</Label>
            <Select
              value={form.employee_type}
              onValueChange={(v) => setForm((p) => ({ ...p, employee_type: v as typeof form.employee_type }))}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="full_time">Full Time</SelectItem>
                <SelectItem value="contract">Contract</SelectItem>
                <SelectItem value="intern">Intern</SelectItem>
                <SelectItem value="part_time">Part Time</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="address">Address</Label>
            <Input
              id="address"
              value={form.address}
              onChange={(e) => setForm((p) => ({ ...p, address: e.target.value }))}
              placeholder="City, Country"
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="emergency_contact_name">Emergency Contact Name</Label>
              <Input
                id="emergency_contact_name"
                value={form.emergency_contact_name}
                onChange={(e) => setForm((p) => ({ ...p, emergency_contact_name: e.target.value }))}
                placeholder="Jane Doe"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="emergency_contact_phone">Emergency Contact Phone</Label>
              <Input
                id="emergency_contact_phone"
                value={form.emergency_contact_phone}
                onChange={(e) => setForm((p) => ({ ...p, emergency_contact_phone: e.target.value }))}
                placeholder="+1 234 567 8901"
              />
            </div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={submitting}>
              {submitting ? "Creating..." : "Create"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
