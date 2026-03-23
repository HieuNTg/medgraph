import { Card, CardContent, CardHeader } from "@/components/ui/card";

/** Reusable skeleton pulse block. */
function Pulse({ className = "" }: { className?: string }) {
  return (
    <div
      className={`animate-pulse rounded bg-[var(--muted)] ${className}`}
      aria-hidden="true"
    />
  );
}

/** Skeleton for drug search results list. */
export function SearchResultsSkeleton() {
  return (
    <div className="space-y-2" role="status">
      {Array.from({ length: 4 }).map((_, i) => (
        <div key={i} className="flex items-center gap-3 px-4 py-3">
          <Pulse className="h-4 w-4 shrink-0 rounded-full" />
          <div className="flex-1 space-y-1.5">
            <Pulse className="h-4 w-32" />
            <Pulse className="h-3 w-48" />
          </div>
        </div>
      ))}
      <span className="sr-only">Loading search results...</span>
    </div>
  );
}

/** Skeleton for the analysis results page. */
export function AnalysisSkeleton() {
  return (
    <div className="space-y-6" role="status">
      {/* Risk summary skeleton */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-4">
            <Pulse className="h-16 w-16 rounded-full" />
            <div className="space-y-2">
              <Pulse className="h-6 w-48" />
              <Pulse className="h-4 w-64" />
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Interaction cards skeleton */}
      {Array.from({ length: 3 }).map((_, i) => (
        <Card key={i}>
          <CardContent className="pt-6 space-y-3">
            <div className="flex items-center gap-3">
              <Pulse className="h-5 w-24" />
              <Pulse className="h-5 w-5 rounded-full" />
              <Pulse className="h-5 w-24" />
              <Pulse className="ml-auto h-6 w-20 rounded-full" />
            </div>
            <Pulse className="h-4 w-full" />
            <Pulse className="h-4 w-3/4" />
          </CardContent>
        </Card>
      ))}
      <span className="sr-only">Loading analysis results...</span>
    </div>
  );
}
