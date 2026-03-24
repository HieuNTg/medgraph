import { useState } from "react";
import { Clock, AlertCircle, Plus, X, Calendar } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { getSchedule } from "@/lib/api";
import type { ScheduleResponse } from "@/lib/types";

const FREQUENCY_OPTIONS = [
  { value: 1, label: "1x daily" },
  { value: 2, label: "2x daily" },
  { value: 3, label: "3x daily" },
];

const SLOT_COLORS: Record<string, string> = {
  "08:00": "bg-amber-100 border-amber-300 text-amber-800 dark:bg-amber-900/30 dark:border-amber-700 dark:text-amber-300",
  "12:00": "bg-sky-100 border-sky-300 text-sky-800 dark:bg-sky-900/30 dark:border-sky-700 dark:text-sky-300",
  "18:00": "bg-violet-100 border-violet-300 text-violet-800 dark:bg-violet-900/30 dark:border-violet-700 dark:text-violet-300",
  "22:00": "bg-slate-100 border-slate-300 text-slate-700 dark:bg-slate-800 dark:border-slate-600 dark:text-slate-300",
};

interface DrugEntry {
  name: string;
  frequency: number;
}

export function SchedulePage() {
  const [drugs, setDrugs] = useState<DrugEntry[]>([{ name: "", frequency: 1 }]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ScheduleResponse | null>(null);

  const addDrug = () => {
    if (drugs.length >= 10) return;
    setDrugs((prev) => [...prev, { name: "", frequency: 1 }]);
  };

  const removeDrug = (index: number) => {
    setDrugs((prev) => prev.filter((_, i) => i !== index));
  };

  const updateDrug = (index: number, field: keyof DrugEntry, value: string | number) => {
    setDrugs((prev) =>
      prev.map((d, i) => (i === index ? { ...d, [field]: value } : d))
    );
  };

  const validDrugs = drugs.filter((d) => d.name.trim().length > 0);
  const canSubmit = validDrugs.length >= 1 && !loading;

  const handleSubmit = async () => {
    setError(null);
    setLoading(true);
    setResult(null);
    try {
      const data = await getSchedule(
        validDrugs.map((d) => ({ name: d.name.trim(), frequency: d.frequency }))
      );
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8 space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[var(--primary)]">
            <Calendar className="h-5 w-5 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-[var(--foreground)]">
            Schedule Optimizer
          </h1>
        </div>
        <p className="text-[var(--muted-foreground)]">
          Optimize your medication schedule across 4 daily time slots to minimize interactions.
        </p>
      </div>

      {/* Drug input form */}
      <div className="rounded-xl border border-[var(--border)] bg-[var(--card)] p-6 space-y-4">
        <h2 className="text-sm font-semibold text-[var(--foreground)]">Medications</h2>

        {drugs.map((drug, index) => (
          <div key={index} className="flex items-center gap-3">
            <Input
              value={drug.name}
              onChange={(e) => updateDrug(index, "name", e.target.value)}
              placeholder="Drug name (e.g. Warfarin)"
              aria-label={`Drug ${index + 1} name`}
              className="flex-1"
            />
            <select
              value={drug.frequency}
              onChange={(e) => updateDrug(index, "frequency", Number(e.target.value))}
              aria-label={`Drug ${index + 1} frequency`}
              className="rounded-md border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-sm text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
            >
              {FREQUENCY_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
            {drugs.length > 1 && (
              <button
                type="button"
                onClick={() => removeDrug(index)}
                aria-label={`Remove drug ${index + 1}`}
                className="rounded-full p-1 hover:bg-[var(--accent)] transition-colors"
              >
                <X className="h-4 w-4 text-[var(--muted-foreground)]" />
              </button>
            )}
          </div>
        ))}

        <div className="flex items-center justify-between pt-2">
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={addDrug}
            disabled={drugs.length >= 10}
            className="flex items-center gap-1.5"
          >
            <Plus className="h-4 w-4" />
            Add Drug
          </Button>
          <Button
            onClick={handleSubmit}
            disabled={!canSubmit}
            size="lg"
            className="min-w-[180px]"
          >
            {loading ? (
              <>
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                Optimizing...
              </>
            ) : (
              "Optimize Schedule"
            )}
          </Button>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div
          role="alert"
          className="flex items-start gap-3 rounded-lg border border-red-200 bg-red-50 p-4 text-red-800 dark:border-red-800 dark:bg-red-950 dark:text-red-300"
        >
          <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
          <div className="space-y-1">
            <p className="font-semibold text-sm">Schedule Failed</p>
            <p className="text-sm">{error}</p>
          </div>
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="space-y-6">
          <h2 className="text-lg font-semibold text-[var(--foreground)]">Recommended Schedule</h2>

          {/* Time slot cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {result.slots.map((slot) => {
              const colorClass =
                SLOT_COLORS[slot.time] ??
                "bg-[var(--card)] border-[var(--border)] text-[var(--foreground)]";
              return (
                <div
                  key={slot.time}
                  className={`rounded-xl border p-4 space-y-3 ${colorClass}`}
                >
                  <div className="flex items-center gap-2">
                    <Clock className="h-4 w-4 shrink-0" />
                    <span className="font-semibold text-sm">{slot.label}</span>
                    <span className="text-xs opacity-70">{slot.time}</span>
                  </div>
                  {slot.drugs.length > 0 ? (
                    <div className="flex flex-wrap gap-2">
                      {slot.drugs.map((drug) => (
                        <Badge key={drug} variant="secondary" className="text-xs">
                          {drug}
                        </Badge>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs opacity-60">No medications assigned</p>
                  )}
                </div>
              );
            })}
          </div>

          {/* Warnings */}
          {result.warnings.length > 0 && (
            <div className="rounded-xl border border-amber-200 bg-amber-50 p-4 dark:border-amber-800 dark:bg-amber-950 space-y-2">
              <div className="flex items-center gap-2 text-amber-800 dark:text-amber-300">
                <AlertCircle className="h-4 w-4 shrink-0" />
                <span className="font-semibold text-sm">Scheduling Warnings</span>
              </div>
              <ul className="space-y-1">
                {result.warnings.map((w, i) => (
                  <li key={i} className="text-sm text-amber-700 dark:text-amber-400">
                    {w}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
