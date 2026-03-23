import { useState, useEffect } from "react";
import { Link, NavLink, Outlet, useNavigate } from "react-router-dom";
import { Pill, Shield, Info, Sun, Moon, Menu, X, BookMarked, History, LogIn, LogOut, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { MedicalDisclaimer } from "@/components/medical-disclaimer";
import { useAuth } from "@/lib/auth-context";

function ThemeToggle() {
  const [dark, setDark] = useState(() => {
    if (typeof window === "undefined") return false;
    const stored = localStorage.getItem("medgraph-theme");
    if (stored) return stored === "dark";
    return document.documentElement.classList.contains("dark");
  });

  useEffect(() => {
    const root = document.documentElement;
    if (dark) {
      root.classList.add("dark");
      root.classList.remove("light");
    } else {
      root.classList.remove("dark");
      root.classList.add("light");
    }
    localStorage.setItem("medgraph-theme", dark ? "dark" : "light");
  }, [dark]);

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setDark((d) => !d)}
      aria-label={dark ? "Switch to light mode" : "Switch to dark mode"}
    >
      {dark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
    </Button>
  );
}

const STATIC_NAV_LINKS = [
  { to: "/", label: "Home", icon: null, end: true },
  { to: "/checker", label: "Check Interactions", icon: Shield },
  { to: "/about", label: "About", icon: Info },
];

const AUTH_NAV_LINKS = [
  { to: "/profiles", label: "Profiles", icon: BookMarked },
  { to: "/history", label: "History", icon: History },
];

export function AppShell() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const navLinkClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
      isActive
        ? "bg-[var(--primary)] text-white"
        : "text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:bg-[var(--accent)]"
    }`;

  const navLinks = isAuthenticated
    ? [...STATIC_NAV_LINKS, ...AUTH_NAV_LINKS]
    : STATIC_NAV_LINKS;

  const handleLogout = () => {
    logout();
    navigate("/");
    setMobileOpen(false);
  };

  return (
    <div className="flex min-h-screen flex-col bg-[var(--background)]">
      {/* Header */}
      <header className="sticky top-0 z-40 border-b border-[var(--border)] bg-[var(--background)]/95 backdrop-blur">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            {/* Logo */}
            <Link
              to="/"
              className="flex items-center gap-2 font-bold text-[var(--foreground)] text-lg"
            >
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[var(--primary)]">
                <Pill className="h-4 w-4 text-white" />
              </div>
              <span>MEDGRAPH</span>
            </Link>

            {/* Desktop nav */}
            <nav className="hidden md:flex items-center gap-1">
              {navLinks.map(({ to, label, end }) => (
                <NavLink key={to} to={to} end={end} className={navLinkClass}>
                  {label}
                </NavLink>
              ))}
            </nav>

            {/* Right: auth + theme + mobile menu */}
            <div className="flex items-center gap-2">
              {isAuthenticated ? (
                <div className="hidden md:flex items-center gap-2">
                  <span className="flex items-center gap-1.5 text-sm text-[var(--muted-foreground)]">
                    <User className="h-3.5 w-3.5" />
                    {user?.display_name ?? user?.email}
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleLogout}
                    className="flex items-center gap-1.5 text-[var(--muted-foreground)]"
                  >
                    <LogOut className="h-3.5 w-3.5" />
                    Logout
                  </Button>
                </div>
              ) : (
                <NavLink
                  to="/login"
                  className="hidden md:flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:bg-[var(--accent)] transition-colors"
                >
                  <LogIn className="h-4 w-4" />
                  Login
                </NavLink>
              )}
              <ThemeToggle />
              <button
                className="md:hidden rounded-md p-2 hover:bg-[var(--accent)] transition-colors"
                onClick={() => setMobileOpen((o) => !o)}
                aria-label="Toggle menu"
              >
                {mobileOpen ? (
                  <X className="h-5 w-5" />
                ) : (
                  <Menu className="h-5 w-5" />
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile menu */}
        {mobileOpen && (
          <div className="md:hidden border-t border-[var(--border)] bg-[var(--background)] px-4 py-3">
            <nav className="flex flex-col gap-1">
              {navLinks.map(({ to, label, icon: Icon, end }) => (
                <NavLink
                  key={to}
                  to={to}
                  end={end}
                  className={navLinkClass}
                  onClick={() => setMobileOpen(false)}
                >
                  {Icon && <Icon className="h-4 w-4" />}
                  {label}
                </NavLink>
              ))}
              {isAuthenticated ? (
                <button
                  type="button"
                  onClick={handleLogout}
                  className="flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:bg-[var(--accent)] transition-colors"
                >
                  <LogOut className="h-4 w-4" />
                  Logout ({user?.display_name ?? user?.email})
                </button>
              ) : (
                <NavLink
                  to="/login"
                  className={navLinkClass}
                  onClick={() => setMobileOpen(false)}
                >
                  <LogIn className="h-4 w-4" />
                  Login
                </NavLink>
              )}
            </nav>
          </div>
        )}
      </header>

      {/* Main */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t border-[var(--border)] bg-[var(--card)]">
        <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8 space-y-4">
          <MedicalDisclaimer />
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-[var(--muted-foreground)]">
            <div className="flex items-center gap-2">
              <Pill className="h-4 w-4" />
              <span>MEDGRAPH - Drug Interaction Cascade Analyzer</span>
            </div>
            <p>
              Data sources: DrugBank · OpenFDA · RxNorm
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
