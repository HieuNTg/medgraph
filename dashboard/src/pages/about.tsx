import { Shield, Database, GitBranch, AlertTriangle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { MedicalDisclaimer } from "@/components/medical-disclaimer";

const DATA_SOURCES = [
  {
    name: "DrugBank",
    description:
      "Comprehensive drug and drug target database with enzyme interaction data.",
    url: "https://go.drugbank.com",
  },
  {
    name: "OpenFDA",
    description:
      "FDA adverse event reporting system (FAERS) with real-world case counts.",
    url: "https://open.fda.gov",
  },
  {
    name: "RxNorm",
    description:
      "NLM's normalized clinical drug nomenclature for consistent drug identification.",
    url: "https://www.nlm.nih.gov/research/umls/rxnorm/",
  },
];

export function AboutPage() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6 lg:px-8 space-y-12">
      {/* Header */}
      <div className="space-y-4">
        <h1 className="text-3xl font-bold text-[var(--foreground)]">
          About MEDGRAPH
        </h1>
        <p className="text-lg text-[var(--muted-foreground)] leading-relaxed">
          MEDGRAPH uses knowledge graph technology and enzyme cascade analysis
          to detect drug interaction risks that conventional checkers miss.
        </p>
      </div>

      {/* Methodology */}
      <section className="space-y-6">
        <h2 className="text-xl font-semibold text-[var(--foreground)] flex items-center gap-2">
          <GitBranch className="h-5 w-5 text-[var(--primary)]" />
          Methodology
        </h2>
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Knowledge Graph</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-[var(--muted-foreground)] leading-relaxed">
                Drug interactions are modeled as a directed graph where nodes
                represent drugs and enzymes, and edges represent metabolic
                relationships (metabolized_by, inhibits, induces). This enables
                detection of indirect interactions through shared enzyme pathways.
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Cascade Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-[var(--muted-foreground)] leading-relaxed">
                The cascade engine traverses the graph to find multi-hop
                pathways. For example: Drug A inhibits CYP3A4, which normally
                metabolizes Drug B — causing Drug B levels to rise dangerously.
                These indirect interactions are often missed by simple
                pairwise checkers.
              </p>
            </CardContent>
          </Card>
        </div>
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Risk Scoring</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-[var(--muted-foreground)] leading-relaxed">
              Each interaction receives a risk score based on: enzyme inhibition
              strength (strong/moderate/weak), number of affected pathways,
              FDA adverse event case counts, and clinical literature evidence.
              Scores are normalized to 0–1 and mapped to severity levels:
              Critical, Major, Moderate, or Minor.
            </p>
          </CardContent>
        </Card>
      </section>

      {/* Data sources */}
      <section className="space-y-6">
        <h2 className="text-xl font-semibold text-[var(--foreground)] flex items-center gap-2">
          <Database className="h-5 w-5 text-[var(--primary)]" />
          Data Sources
        </h2>
        <div className="grid gap-4 md:grid-cols-3">
          {DATA_SOURCES.map(({ name, description, url }) => (
            <Card key={name}>
              <CardHeader>
                <CardTitle className="text-base">
                  <a
                    href={url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-[var(--primary)] hover:underline"
                  >
                    {name}
                  </a>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-[var(--muted-foreground)] leading-relaxed">
                  {description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Limitations */}
      <section className="space-y-4">
        <h2 className="text-xl font-semibold text-[var(--foreground)] flex items-center gap-2">
          <AlertTriangle className="h-5 w-5 text-amber-500" />
          Limitations
        </h2>
        <Card className="border-amber-200 dark:border-amber-800">
          <CardContent className="pt-6">
            <ul className="space-y-3 text-sm text-[var(--muted-foreground)]">
              <li className="flex gap-2">
                <span className="text-amber-500 shrink-0">·</span>
                Drug interaction databases are not complete — unknown
                interactions may exist.
              </li>
              <li className="flex gap-2">
                <span className="text-amber-500 shrink-0">·</span>
                Individual patient factors (genetics, kidney/liver function, age)
                significantly affect interaction severity and are not modeled.
              </li>
              <li className="flex gap-2">
                <span className="text-amber-500 shrink-0">·</span>
                Risk scores are estimates based on population data, not
                personalized predictions.
              </li>
              <li className="flex gap-2">
                <span className="text-amber-500 shrink-0">·</span>
                This tool does not account for dosage, route of administration,
                or timing of medications.
              </li>
              <li className="flex gap-2">
                <span className="text-amber-500 shrink-0">·</span>
                Database may not reflect the most recent clinical findings.
              </li>
            </ul>
          </CardContent>
        </Card>
      </section>

      {/* Full disclaimer */}
      <section className="space-y-4">
        <h2 className="text-xl font-semibold text-[var(--foreground)] flex items-center gap-2">
          <Shield className="h-5 w-5 text-[var(--primary)]" />
          Medical Disclaimer
        </h2>
        <MedicalDisclaimer full />
      </section>

      {/* GitHub */}
      <section>
        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-[var(--muted-foreground)]">
              MEDGRAPH is an open-source project.{" "}
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-[var(--primary)] hover:underline"
              >
                View source on GitHub
              </a>
            </p>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
