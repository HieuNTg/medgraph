import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import type { ReactNode } from "react";
import { setAuthToken, login as apiLogin, register as apiRegister, getMe } from "./api";
import type { User } from "./types";
import {
  storeTokens,
  clearTokens,
  getStoredAccessToken,
  getStoredRefreshToken,
  useTokenRefreshInterval,
} from "./use-auth-tokens";

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, displayName?: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  // Restore session — try cookie-based auth first, fall back to localStorage
  useEffect(() => {
    // Try cookie-based session (httpOnly cookies sent automatically)
    getMe()
      .then((userData) => {
        setUser(userData);
        // Sync localStorage token if present (backward compat)
        const stored = getStoredAccessToken();
        if (stored) setAuthToken(stored);
      })
      .catch(() => {
        // Cookie auth failed — try localStorage refresh token
        const storedRefresh = getStoredRefreshToken();
        if (!storedRefresh) return;

        const stored = getStoredAccessToken();
        if (stored) setAuthToken(stored);

        import("./api").then(({ refreshToken: apiRefresh }) =>
          apiRefresh(storedRefresh)
            .then((res) => {
              storeTokens({ access_token: res.access_token, refresh_token: res.refresh_token });
              setUser(res.user);
            })
            .catch(() => {
              clearTokens();
            })
        );
      });
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const res = await apiLogin(email, password);
    storeTokens({ access_token: res.access_token, refresh_token: res.refresh_token });
    setUser(res.user);
  }, []);

  const register = useCallback(
    async (email: string, password: string, displayName?: string) => {
      const res = await apiRegister(email, password, displayName);
      storeTokens({ access_token: res.access_token, refresh_token: res.refresh_token });
      setUser(res.user);
    },
    []
  );

  const logout = useCallback(() => {
    clearTokens();
    setUser(null);
  }, []);

  // Proactively refresh token every 10 minutes while authenticated
  useTokenRefreshInterval(user, setUser);

  const value = useMemo<AuthState>(
    () => ({
      user,
      isAuthenticated: user !== null,
      login,
      register,
      logout,
    }),
    [user, login, register, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}
