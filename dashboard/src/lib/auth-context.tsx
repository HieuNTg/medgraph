import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import type { ReactNode } from "react";
import { setAuthToken, login as apiLogin, register as apiRegister, refreshToken as apiRefresh, getMe } from "./api";
import type { User } from "./types";

const TOKEN_KEY = "medgraph-access-token";
const REFRESH_KEY = "medgraph-refresh-token";

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
        const stored = localStorage.getItem(TOKEN_KEY);
        if (stored) setAuthToken(stored);
      })
      .catch(() => {
        // Cookie auth failed — try localStorage refresh token
        const storedRefresh = localStorage.getItem(REFRESH_KEY);
        if (!storedRefresh) return;

        const stored = localStorage.getItem(TOKEN_KEY);
        if (stored) setAuthToken(stored);

        apiRefresh(storedRefresh)
          .then((res) => {
            localStorage.setItem(TOKEN_KEY, res.access_token);
            localStorage.setItem(REFRESH_KEY, res.refresh_token);
            setAuthToken(res.access_token);
            setUser(res.user);
          })
          .catch(() => {
            localStorage.removeItem(TOKEN_KEY);
            localStorage.removeItem(REFRESH_KEY);
            setAuthToken(null);
          });
      });
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const res = await apiLogin(email, password);
    localStorage.setItem(TOKEN_KEY, res.access_token);
    localStorage.setItem(REFRESH_KEY, res.refresh_token);
    setAuthToken(res.access_token);
    setUser(res.user);
  }, []);

  const register = useCallback(
    async (email: string, password: string, displayName?: string) => {
      const res = await apiRegister(email, password, displayName);
      localStorage.setItem(TOKEN_KEY, res.access_token);
      localStorage.setItem(REFRESH_KEY, res.refresh_token);
      setAuthToken(res.access_token);
      setUser(res.user);
    },
    []
  );

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_KEY);
    setAuthToken(null);
    setUser(null);
  }, []);

  // Proactively refresh token every 10 minutes while authenticated
  useEffect(() => {
    if (!user) return;
    const id = setInterval(() => {
      const storedRefresh = localStorage.getItem(REFRESH_KEY);
      if (!storedRefresh) return;
      apiRefresh(storedRefresh)
        .then((res) => {
          localStorage.setItem(TOKEN_KEY, res.access_token);
          localStorage.setItem(REFRESH_KEY, res.refresh_token);
          setAuthToken(res.access_token);
          setUser(res.user);
        })
        .catch(() => {
          // Silently ignore — will retry next interval; don't force logout
        });
    }, 600_000);
    return () => clearInterval(id);
  }, [user]);

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
