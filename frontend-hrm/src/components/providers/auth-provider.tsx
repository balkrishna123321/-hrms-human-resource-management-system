"use client";

import React, { createContext, useCallback, useContext, useEffect, useState } from "react";
import { setAuthHandlers } from "@/lib/api/client";
import { api } from "@/lib/api/endpoints";
import type { UserResponse } from "@/lib/types/api";

const STORAGE_ACCESS = "access_token";
const STORAGE_REFRESH = "refresh_token";

type AuthState = {
  user: UserResponse | null;
  accessToken: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
};

const AuthContext = createContext<AuthState & {
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  setTokens: (access: string, refresh: string) => void;
} | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserResponse | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const setTokens = useCallback((access: string, refresh: string) => {
    if (typeof window !== "undefined") {
      localStorage.setItem(STORAGE_ACCESS, access);
      localStorage.setItem(STORAGE_REFRESH, refresh);
    }
    setAccessToken(access);
  }, []);

  const getAccessToken = useCallback(() => {
    if (accessToken) return accessToken;
    if (typeof window !== "undefined") return localStorage.getItem(STORAGE_ACCESS);
    return null;
  }, [accessToken]);

  useEffect(() => {
    setAuthHandlers(getAccessToken, setTokens);
  }, [getAccessToken, setTokens]);

  useEffect(() => {
    const refresh = typeof window !== "undefined" ? localStorage.getItem(STORAGE_REFRESH) : null;
    const access = typeof window !== "undefined" ? localStorage.getItem(STORAGE_ACCESS) : null;
    if (!access && !refresh) {
      setIsLoading(false);
      return;
    }
    if (access) setAccessToken(access);
    api.auth
      .me()
      .then((res) => {
        if (res.data) setUser(res.data);
      })
      .catch(() => {
        if (typeof window !== "undefined") {
          localStorage.removeItem(STORAGE_ACCESS);
          localStorage.removeItem(STORAGE_REFRESH);
        }
        setAccessToken(null);
        setUser(null);
      })
      .finally(() => setIsLoading(false));
  }, []);

  const login = useCallback(
    async (email: string, password: string) => {
      const res = await api.auth.login(email, password);
      if (!res.data) throw new Error(res.message || "Login failed");
      const { access_token, refresh_token } = res.data;
      setTokens(access_token, refresh_token);
      const meRes = await api.auth.me();
      if (meRes.data) setUser(meRes.data);
    },
    [setTokens]
  );

  const logout = useCallback(() => {
    if (typeof window !== "undefined") {
      localStorage.removeItem(STORAGE_ACCESS);
      localStorage.removeItem(STORAGE_REFRESH);
    }
    setAccessToken(null);
    setUser(null);
  }, []);

  const value: AuthState & {
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
    setTokens: (access: string, refresh: string) => void;
  } = {
    user,
    accessToken,
    isLoading,
    isAuthenticated: !!user && !!accessToken,
    login,
    logout,
    setTokens,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
