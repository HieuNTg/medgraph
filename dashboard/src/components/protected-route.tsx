import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "@/lib/auth-context";
import type { ReactNode } from "react";

interface ProtectedRouteProps {
  children: ReactNode;
  /** When true (default), redirect unauthenticated users to /login */
  requireAuth?: boolean;
  /** Redirect authenticated users away (e.g. login page). Default false */
  redirectAuthenticated?: boolean;
}

/**
 * Centralized auth guard component.
 * Wrap any route element with <ProtectedRoute> to enforce authentication.
 */
export function ProtectedRoute({
  children,
  requireAuth = true,
  redirectAuthenticated = false,
}: ProtectedRouteProps) {
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  if (requireAuth && !isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (redirectAuthenticated && isAuthenticated) {
    const from = (location.state as { from?: Location } | null)?.from?.pathname ?? "/";
    return <Navigate to={from} replace />;
  }

  return <>{children}</>;
}
