import { useEffect } from "react";
import { setAuthToken, refreshToken as apiRefresh } from "./api";
import type { User } from "./types";

const TOKEN_KEY = "medgraph-access-token";
const REFRESH_KEY = "medgraph-refresh-token";

export interface TokenPair {
  access_token: string;
  refresh_token: string;
}

export function storeTokens(pair: TokenPair): void {
  localStorage.setItem(TOKEN_KEY, pair.access_token);
  localStorage.setItem(REFRESH_KEY, pair.refresh_token);
  setAuthToken(pair.access_token);
}

export function clearTokens(): void {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_KEY);
  setAuthToken(null);
}

export function getStoredAccessToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function getStoredRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_KEY);
}

/** Fires the proactive 10-minute refresh interval while a user is authenticated. */
export function useTokenRefreshInterval(
  user: User | null,
  onRefresh: (user: User) => void
): void {
  useEffect(() => {
    if (!user) return;
    const id = setInterval(() => {
      const storedRefresh = getStoredRefreshToken();
      if (!storedRefresh) return;
      apiRefresh(storedRefresh)
        .then((res) => {
          storeTokens({ access_token: res.access_token, refresh_token: res.refresh_token });
          onRefresh(res.user);
        })
        .catch(() => {
          // Silently ignore — will retry next interval; don't force logout
        });
    }, 600_000);
    return () => clearInterval(id);
  }, [user, onRefresh]);
}
