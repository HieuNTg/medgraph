import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { ArrowLeft, Pill, Loader2, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { MedicalDisclaimer } from "@/components/medical-disclaimer";
import { getDrug } from "@/lib/api";

const RELATION_LABELS: Record<string, string> = {
  metabolized_by: "Metabolized by",
  inhibits: "Inhibits",
  induces: "Induces",
};

const STRENGTH_VARIANT: Record<string, "default" | "secondary" | "outline"> = {
  strong: "default",
  moderate: "secondary",
  weak: "outline",
};

export function DrugInfoPage() {
  const { id } = useParams<{ id: string }>();
  const {
    data: drug,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["drug", id],
    queryFn: () => getDrug(id!),
    enabled: !!id,
  });

  if (isLoading) {
    return (
      <div className="flex min-h-[400px] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-[var(--muted-foreground)]" />
      </div>
    );
  }

  if (error || !drug) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8 space-y-6">
        <div className="flex items-start gap-3 rounded-lg border border-red-200 bg-red-50 p-4 text-red-800">
          <AlertCircle className="mt-0.5 h-4 w-4" />
          <p className="text-sm">
            {error instanceof Error ? error.message : "Drug not found."}
          </p>
        </div>
        <Button asChild variant="outline">
          <Link to="/checker">
            <ArrowLeft className="h-4 w-4" />
            Back to Checker
          </Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8 space-y-8">
      {/* Back */}
      <Button asChild variant="ghost" size="sm">
        <Link to="/checker" className="flex items-center gap-2">
          <ArrowLeft className="h-4 w-4" />
          Back to Checker
        </Link>
      </Button>

      {/* Header */}
      <div className="flex items-center gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-50 dark:bg-blue-950">
          <Pill className="h-6 w-6 text-[var(--primary)]" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-[var(--foreground)]">
            {drug.name}
          </h1>
          {drug.drug_class && (
            <p className="text-sm text-[var(--muted-foreground)]">
              {drug.drug_class}
            </p>
          )}
        </div>
      </div>

      {/* Brand names */}
      {drug.brand_names.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Brand Names</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {drug.brand_names.map((name) => (
                <Badge key={name} variant="secondary">
                  {name}
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Enzyme relations */}
      {drug.enzyme_relations.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Enzyme Relationships</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="divide-y divide-[var(--border)]">
              {drug.enzyme_relations.map((rel, i) => (
                <div
                  key={i}
                  className="flex items-center justify-between py-3 first:pt-0 last:pb-0"
                >
                  <div>
                    <p className="font-medium text-sm text-[var(--foreground)]">
                      {rel.enzyme_name}
                    </p>
                    <p className="text-xs text-[var(--muted-foreground)]">
                      {RELATION_LABELS[rel.relation_type] ?? rel.relation_type}
                    </p>
                  </div>
                  <Badge variant={STRENGTH_VARIANT[rel.strength] ?? "outline"}>
                    {rel.strength}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* CTA */}
      <div className="rounded-lg border border-[var(--border)] bg-[var(--card)] p-4">
        <p className="text-sm text-[var(--muted-foreground)] mb-3">
          Want to check interactions for {drug.name}?
        </p>
        <Button asChild>
          <Link to="/checker">Check Interactions with {drug.name}</Link>
        </Button>
      </div>

      <MedicalDisclaimer />
    </div>
  );
}
