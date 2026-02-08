import { api } from "@/lib/api/endpoints";

export const employeeService = {
  list: api.employees.list,
  get: api.employees.get,
  create: api.employees.create,
  update: api.employees.update,
  delete: api.employees.delete,
};
