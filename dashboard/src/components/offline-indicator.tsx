// Online/offline status indicator component.
// Shows a colored dot + status text; when offline, displays last sync time.

import { useState, useEffect } from "react";
import { offlineStore } from "@/lib/offline-store";

export function OfflineIndicator() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [lastSync, setLastSync] = useState<string | null>(null);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  // Load last sync time when going offline
  useEffect(() => {
    if (!isOnline) {
      offlineStore
        .getLastSync()
        .then(setLastSync)
        .catch(() => setLastSync(null));
    }
  }, [isOnline]);

  if (isOnline) {
    return (
      <div
        className="flex items-center gap-1.5 text-xs text-[var(--muted-foreground)]"
        role="status"
        aria-label="Connection status: online"
      >
        <span
          className="h-2 w-2 rounded-full bg-green-500"
          aria-hidden="true"
        />
        <span>Online</span>
      </div>
    );
  }

  return (
    <div
      className="flex items-center gap-1.5 text-xs text-amber-500"
      role="status"
      aria-label="Connection status: offline"
    >
      <span
        className="h-2 w-2 rounded-full bg-red-500"
        aria-hidden="true"
      />
      <span>
        Offline
        {lastSync ? ` · Last synced: ${formatRelativeTime(lastSync)}` : ""}
      </span>
    </div>
  );
}

function formatRelativeTime(isoString: string): string {
  const date = new Date(isoString);
  if (isNaN(date.getTime())) return isoString;

  const diffMs = Date.now() - date.getTime();
  const diffMin = Math.floor(diffMs / 60_000);
  const diffHr = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHr / 24);

  if (diffMin < 1) return "just now";
  if (diffMin < 60) return `${diffMin}m ago`;
  if (diffHr < 24) return `${diffHr}h ago`;
  return `${diffDay}d ago`;
}
