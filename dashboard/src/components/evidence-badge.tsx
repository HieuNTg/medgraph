import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface EvidenceBadgeConfig {
  label: string;
  className: string;
  title: string;
}

const EVIDENCE_CONFIG: Record<string, EvidenceBadgeConfig> = {
  A: {
    label: "FDA Label",
    className:
      "border-transparent bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400",
    title: "Evidence from FDA-approved drug label",
  },
  B: {
    label: "Clinical Trial",
    className:
      "border-transparent bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400",
    title: "Evidence from clinical trial data",
  },
  C: {
    label: "Case Report",
    className:
      "border-transparent bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400",
    title: "Evidence from case report(s)",
  },
  D: {
    label: "Theoretical",
    className:
      "border-transparent bg-gray-100 text-gray-700 dark:bg-gray-800/50 dark:text-gray-400",
    title: "Theoretically predicted interaction",
  },
};

interface EvidenceBadgeProps {
  level: string;
  className?: string;
}

export function EvidenceBadge({ level, className }: EvidenceBadgeProps) {
  const code = level.trim().toUpperCase();
  const config = EVIDENCE_CONFIG[code];

  if (!config) {
    // Render unknown levels as a neutral outline badge
    return (
      <Badge
        className={cn(
          "border border-current text-xs font-medium",
          className
        )}
        title={level}
      >
        {level}
      </Badge>
    );
  }

  return (
    <Badge
      className={cn("text-xs font-medium", config.className, className)}
      title={config.title}
    >
      {code} · {config.label}
    </Badge>
  );
}
