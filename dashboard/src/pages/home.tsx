import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { Shield, Network, FileSearch, ArrowRight, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { getStats } from "@/lib/api";

const FEATURES = [
  {
    icon: FileSearch,
    title: "Real FDA Data",
    description:
      "Powered by OpenFDA, DrugBank, and RxNorm — the same databases used by medical professionals.",
  },
  {
    icon: Network,
    title: "Cascade Analysis",
    description:
      "Detects multi-drug enzyme pathway conflicts that simple interaction checkers miss entirely.",
  },
  {
    icon: Shield,
    title: "Evidence Trail",
    description:
      "Every interaction includes FDA adverse event case counts and source citations for full transparency.",
  },
];

const HOW_IT_WORKS = [
  {
    step: "1",
    title: "Enter Your Medications",
    description: "Type the names of your medications and select them from our database.",
  },
  {
    step: "2",
    title: "Analyze Cascade Pathways",
    description:
      "Our engine maps enzyme pathways (CYP450, etc.) to detect cascading interaction risks.",
  },
  {
    step: "3",
    title: "Review Your Report",
    description:
      "Get a detailed report with severity ratings, mechanisms, and evidence for each interaction.",
  },
];

export function HomePage() {
  const { data: stats, isLoading } = useQuery({
    queryKey: ["stats"],
    queryFn: getStats,
    staleTime: 10 * 60 * 1000,
  });

  return (
    <div className="space-y-20 py-12">
      {/* Hero */}
      <section className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 text-center space-y-8">
        <div className="space-y-4">
          <div className="inline-flex items-center gap-2 rounded-full border border-blue-200 bg-blue-50 px-4 py-1.5 text-sm text-blue-700 dark:border-blue-800 dark:bg-blue-950 dark:text-blue-300">
            <Shield className="h-4 w-4" />
            Evidence-Based Drug Interaction Analysis
          </div>
          <h1 className="text-4xl font-bold tracking-tight text-[var(--foreground)] sm:text-5xl lg:text-6xl">
            Know Your Drug Interactions
            <br />
            <span className="text-[var(--primary)]">Before They Harm You</span>
          </h1>
          <p className="mx-auto max-w-2xl text-lg text-[var(--muted-foreground)] leading-relaxed">
            Cascade analysis detects multi-drug enzyme pathway risks that simple
            checkers miss. Built on FDA data, designed for clarity.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Button asChild size="lg" className="min-w-[200px]">
            <Link to="/checker">
              Check Your Medications
              <ArrowRight className="h-4 w-4" />
            </Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link to="/about">How It Works</Link>
          </Button>
        </div>

        {/* Stats */}
        {(isLoading || stats) && (
          <div className="flex items-center justify-center gap-8 text-sm text-[var(--muted-foreground)]">
            {isLoading ? (
              <div className="flex items-center gap-2">
                <Loader2 className="h-4 w-4 animate-spin" />
                Loading database stats...
              </div>
            ) : stats ? (
              <>
                <div className="text-center">
                  <div className="text-2xl font-bold text-[var(--foreground)]">
                    {stats.drug_count.toLocaleString()}
                  </div>
                  <div>Drugs</div>
                </div>
                <div className="h-8 w-px bg-[var(--border)]" />
                <div className="text-center">
                  <div className="text-2xl font-bold text-[var(--foreground)]">
                    {stats.interaction_count.toLocaleString()}
                  </div>
                  <div>Known Interactions</div>
                </div>
                <div className="h-8 w-px bg-[var(--border)]" />
                <div className="text-center">
                  <div className="text-2xl font-bold text-[var(--foreground)]">
                    {stats.enzyme_count.toLocaleString()}
                  </div>
                  <div>Enzyme Pathways</div>
                </div>
              </>
            ) : null}
          </div>
        )}
      </section>

      {/* Feature cards */}
      <section className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <div className="grid gap-6 md:grid-cols-3">
          {FEATURES.map(({ icon: Icon, title, description }) => (
            <Card key={title} className="text-center">
              <CardHeader className="items-center">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-50 dark:bg-blue-950">
                  <Icon className="h-6 w-6 text-[var(--primary)]" />
                </div>
                <CardTitle>{title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-sm leading-relaxed">
                  {description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <div className="text-center space-y-3 mb-10">
          <h2 className="text-2xl font-bold text-[var(--foreground)]">
            How MEDGRAPH Works
          </h2>
          <p className="text-[var(--muted-foreground)]">
            Three steps to a comprehensive drug interaction report
          </p>
        </div>
        <div className="grid gap-8 md:grid-cols-3">
          {HOW_IT_WORKS.map(({ step, title, description }) => (
            <div key={step} className="flex gap-4">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[var(--primary)] text-white font-bold">
                {step}
              </div>
              <div className="space-y-1">
                <h3 className="font-semibold text-[var(--foreground)]">{title}</h3>
                <p className="text-sm text-[var(--muted-foreground)] leading-relaxed">
                  {description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <div className="rounded-xl bg-[var(--primary)] p-10 text-center text-white space-y-4">
          <h2 className="text-2xl font-bold">
            Ready to check your medications?
          </h2>
          <p className="text-blue-100">
            Free, fast, and evidence-based — no sign-up required.
          </p>
          <Button asChild variant="outline" size="lg" className="bg-white text-[var(--primary)] hover:bg-blue-50 border-white">
            <Link to="/checker">
              Start Checking Now
              <ArrowRight className="h-4 w-4" />
            </Link>
          </Button>
        </div>
      </section>

    </div>
  );
}
