import { api } from "@/lib/api/endpoints";

export const departmentService = {
  list: api.departments.list,
  get: api.departments.get,
  create: api.departments.create,
  update: api.departments.update,
  delete: api.departments.delete,
};
