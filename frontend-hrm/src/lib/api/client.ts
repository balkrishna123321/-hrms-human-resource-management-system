/**
 * API client with auth header injection and refresh-on-401.
 * getAccessToken and setTokens are provided by auth context.
 */

const getBaseUrl = () =>
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export type TokenGetter = () => string | null;
export type TokenSetter = (access: string, refresh: string) => void;

let tokenGetter: TokenGetter = () => null;
let tokenSetter: TokenSetter = () => {};

export function setAuthHandlers(getter: TokenGetter, setter: TokenSetter) {
  tokenGetter = getter;
  tokenSetter = setter;
}

async function refreshTokens(refreshToken: string): Promise<{ access_token: string; refresh_token: string } | null> {
  const res = await fetch(`${getBaseUrl()}/api/v1/auth/refresh`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });
  if (!res.ok) return null;
  const json = await res.json();
  if (json?.data?.access_token && json?.data?.refresh_token) {
    return { access_token: json.data.access_token, refresh_token: json.data.refresh_token };
  }
  return null;
}

export interface RequestConfig extends RequestInit {
  skipAuth?: boolean;
  skipRefresh?: boolean;
}

export async function apiRequest<T>(
  path: string,
  config: RequestConfig = {}
): Promise<T> {
  const { skipAuth = false, skipRefresh = false, ...init } = config;
  const url = path.startsWith("http") ? path : `${getBaseUrl()}${path}`;
  const headers = new Headers(init.headers);

  if (!skipAuth) {
    const access = tokenGetter();
    if (access) headers.set("Authorization", `Bearer ${access}`);
  }

  let res = await fetch(url, { ...init, headers });

  if (res.status === 401 && !skipAuth && !skipRefresh) {
    const refresh = typeof window !== "undefined" ? localStorage.getItem("refresh_token") : null;
    if (refresh) {
      const newTokens = await refreshTokens(refresh);
      if (newTokens) {
        tokenSetter(newTokens.access_token, newTokens.refresh_token);
        headers.set("Authorization", `Bearer ${newTokens.access_token}`);
        res = await fetch(url, { ...init, headers });
      }
    }
  }

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    const err = new Error(data?.message || res.statusText || "Request failed");
    (err as Error & { status?: number; data?: unknown }).status = res.status;
    (err as Error & { status?: number; data?: unknown }).data = data;
    throw err;
  }

  return data as T;
}

export function apiGet<T>(path: string, config?: RequestConfig): Promise<T> {
  return apiRequest<T>(path, { ...config, method: "GET" });
}

export function apiPost<T>(path: string, body?: unknown, config?: RequestConfig): Promise<T> {
  return apiRequest<T>(path, {
    ...config,
    method: "POST",
    headers: { "Content-Type": "application/json", ...config?.headers },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
}

export function apiPatch<T>(path: string, body?: unknown, config?: RequestConfig): Promise<T> {
  return apiRequest<T>(path, {
    ...config,
    method: "PATCH",
    headers: { "Content-Type": "application/json", ...config?.headers },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
}

export function apiDelete(path: string, config?: RequestConfig): Promise<void> {
  return apiRequest(path, { ...config, method: "DELETE" });
}
