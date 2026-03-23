import { AlertTriangle, RefreshCw, WifiOff } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

interface ErrorDisplayProps {
  /** Error message to show the user (sanitized — no stack traces). */
  message?: string;
  /** Callback to retry the failed operation. */
  onRetry?: () => void;
  /** Whether the error is a network/timeout issue. */
  isNetworkError?: boolean;
}

/**
 * Standardized error display component with retry capability.
 * Shows user-friendly message — never exposes internal details.
 */
export function ErrorDisplay({
  message = "Something went wrong. Please try again.",
  onRetry,
  isNetworkError = false,
}: ErrorDisplayProps) {
  const Icon = isNetworkError ? WifiOff : AlertTriangle;

  return (
    <Card className="max-w-md mx-auto" role="alert">
      <CardContent className="flex flex-col items-center gap-4 pt-6 text-center">
        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-amber-100 dark:bg-amber-900/20">
          <Icon className="h-6 w-6 text-amber-600 dark:text-amber-400" />
        </div>
        <div>
          <p className="text-sm text-[var(--muted-foreground)]">{message}</p>
        </div>
        {onRetry && (
          <Button onClick={onRetry} variant="outline" size="sm" className="gap-2">
            <RefreshCw className="h-4 w-4" />
            Try Again
          </Button>
        )}
      </CardContent>
    </Card>
  );
}
