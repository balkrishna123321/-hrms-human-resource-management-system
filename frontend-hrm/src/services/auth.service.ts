import { api } from "@/lib/api/endpoints";

export const authService = {
  login: (email: string, password: string) => api.auth.login(email, password),
  refresh: (refreshToken: string) => api.auth.refresh(refreshToken),
  me: () => api.auth.me(),
};
