import { api } from "@/lib/api/endpoints";

export const roleService = {
  list: api.roles.list,
  get: api.roles.get,
  create: api.roles.create,
  update: api.roles.update,
  delete: api.roles.delete,
};
