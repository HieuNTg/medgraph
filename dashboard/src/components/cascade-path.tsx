import { motion } from "framer-motion";
import type { CascadePath as CascadePathType } from "@/lib/types";

interface CascadePathProps {
  path: CascadePathType;
}

const RELATION_COLORS: Record<string, string> = {
  inhibits: "text-red-600 dark:text-red-400",
  induces: "text-green-600 dark:text-green-400",
  metabolized_by: "text-blue-600 dark:text-blue-400",
  metabolizes: "text-blue-600 dark:text-blue-400",
  default: "text-[var(--muted-foreground)]",
};

const RELATION_BG: Record<string, string> = {
  inhibits: "bg-red-50 border-red-200 dark:bg-red-950 dark:border-red-800",
  induces: "bg-green-50 border-green-200 dark:bg-green-950 dark:border-green-800",
  metabolized_by: "bg-blue-50 border-blue-200 dark:bg-blue-950 dark:border-blue-800",
  metabolizes: "bg-blue-50 border-blue-200 dark:bg-blue-950 dark:border-blue-800",
  default: "bg-[var(--card)] border-[var(--border)]",
};

function getRelationColor(relation: string) {
  const key = relation.toLowerCase().replace(/\s+/g, "_");
  return RELATION_COLORS[key] ?? RELATION_COLORS.default;
}

function getRelationBg(relation: string) {
  const key = relation.toLowerCase().replace(/\s+/g, "_");
  return RELATION_BG[key] ?? RELATION_BG.default;
}

export function CascadePath({ path }: CascadePathProps) {
  return (
    <div className="space-y-3">
      {/* Flow diagram */}
      <div className="flex flex-wrap items-center gap-2">
        {path.steps.map((step, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="flex items-center gap-2"
          >
            {/* Source node */}
            {index === 0 && (
              <div className="rounded-md border border-[var(--border)] bg-[var(--background)] px-3 py-1.5 text-sm font-medium shadow-sm">
                {step.source}
              </div>
            )}

            {/* Arrow + relation label */}
            <div className="flex flex-col items-center gap-0.5">
              <span
                className={`text-xs font-medium ${getRelationColor(step.relation)}`}
              >
                {step.relation}
              </span>
              <div className="flex items-center gap-1">
                <div className="h-0.5 w-8 bg-[var(--border)]" />
                <div className="h-0 w-0 border-t-4 border-b-4 border-l-6 border-t-transparent border-b-transparent border-l-[var(--muted-foreground)]" />
              </div>
              {step.effect && (
                <span className="text-xs text-[var(--muted-foreground)]">
                  {step.effect}
                </span>
              )}
            </div>

            {/* Target node */}
            <div
              className={`rounded-md border px-3 py-1.5 text-sm font-medium shadow-sm ${getRelationBg(step.relation)}`}
            >
              {step.target}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Description */}
      {path.description && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: path.steps.length * 0.1 }}
          className="text-sm text-[var(--muted-foreground)] leading-relaxed"
        >
          {path.description}
        </motion.p>
      )}
    </div>
  );
}
