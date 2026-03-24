import { Shield, ShieldCheck, ShieldAlert } from "lucide-react";

interface ConfidenceIndicatorProps {
  score: number;
  level: string;
  factors: string[];
}

export function ConfidenceIndicator({
  score,
  level,
  factors: _factors,
}: ConfidenceIndicatorProps) {
  const config =
    (
      {
        high: {
          icon: ShieldCheck,
          color: "text-green-600 dark:text-green-400",
          bg: "bg-green-100 dark:bg-green-900/30",
          label: "High Confidence",
        },
        moderate: {
          icon: Shield,
          color: "text-yellow-600 dark:text-yellow-400",
          bg: "bg-yellow-100 dark:bg-yellow-900/30",
          label: "Moderate Confidence",
        },
        low: {
          icon: ShieldAlert,
          color: "text-red-600 dark:text-red-400",
          bg: "bg-red-100 dark:bg-red-900/30",
          label: "Low Confidence",
        },
      } as Record<
        string,
        {
          icon: typeof Shield;
          color: string;
          bg: string;
          label: string;
        }
      >
    )[level] ?? {
      icon: Shield,
      color: "text-gray-600",
      bg: "bg-gray-100",
      label: "Unknown",
    };

  const Icon = config.icon;

  return (
    <div
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ${config.bg} ${config.color}`}
    >
      <Icon className="h-3.5 w-3.5" />
      <span>{config.label}</span>
      <span className="opacity-70">({score}%)</span>
    </div>
  );
}
