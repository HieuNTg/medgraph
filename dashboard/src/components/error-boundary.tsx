import { Component, type ErrorInfo, type ReactNode } from "react";
import { AlertOctagon, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  retryKey: number;
}

/**
 * React error boundary — catches render errors in child tree,
 * shows fallback UI instead of crashing the entire app.
 * Does NOT expose stack traces to users (security requirement).
 */
export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null, retryKey: 0 };
  }

  static getDerivedStateFromError(error: Error): Partial<ErrorBoundaryState> {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    // Log to console for debugging — never expose to user UI
    console.error("[ErrorBoundary] Caught error:", error, errorInfo);
  }

  handleRetry = (): void => {
    this.setState((prev) => ({ hasError: false, error: null, retryKey: prev.retryKey + 1 }));
  };

  render(): ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="flex items-center justify-center min-h-[40vh] p-6">
          <Card className="max-w-md w-full">
            <CardContent className="flex flex-col items-center gap-4 pt-6 text-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/20">
                <AlertOctagon className="h-8 w-8 text-red-600 dark:text-red-400" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-[var(--foreground)]">
                  Something went wrong
                </h2>
                <p className="mt-2 text-sm text-[var(--muted-foreground)]">
                  An unexpected error occurred. Please try again or refresh the page.
                </p>
              </div>
              <div className="flex gap-3">
                <Button onClick={this.handleRetry} variant="outline" className="gap-2">
                  <RefreshCw className="h-4 w-4" />
                  Try Again
                </Button>
                <Button onClick={() => window.location.reload()}>
                  Refresh Page
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      );
    }

    return <span key={this.state.retryKey}>{this.props.children}</span>;
  }
}
