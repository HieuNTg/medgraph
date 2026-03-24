/**
 * Food Interaction Timeline Component
 *
 * Visual timeline showing drug dosing times alongside food interactions
 * as coloured blocks. Warns when food conflicts with drug timing.
 */

import { useState } from "react";
import { Clock, Utensils, AlertTriangle, Info } from "lucide-react";

// Time slots in the day (label, 24h start, 24h end)
const TIME_SLOTS = [
  { id: "morning", label: "Morning", hour: 8, display: "8:00 AM" },
  { id: "noon", label: "Noon", hour: 12, display: "12:00 PM" },
  { id: "evening", label: "Evening", hour: 18, display: "6:00 PM" },
  { id: "night", label: "Night", hour: 22, display: "10:00 PM" },
] as const;

type TimeSlotId = (typeof TIME_SLOTS)[number]["id"];

export interface Drug {
  id: string;
  name: string;
}

export interface FoodInteraction {
  drug_id: string;
  drug_name: string;
  food_item: string;
  severity: "avoid" | "caution" | "safe";
  description: string;
  timing_note?: string; // e.g. "Take 1h before meals"
}

interface FoodInteractionTimelineProps {
  drugs: Drug[];
  foodInteractions: FoodInteraction[];
}

// Severity → colour classes
const SEVERITY_COLOURS: Record<FoodInteraction["severity"], string> = {
  avoid: "bg-red-500/20 border-red-500 text-red-700 dark:text-red-300",
  caution: "bg-amber-500/20 border-amber-500 text-amber-700 dark:text-amber-300",
  safe: "bg-green-500/20 border-green-500 text-green-700 dark:text-green-300",
};

const SEVERITY_BADGE: Record<FoodInteraction["severity"], string> = {
  avoid: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300",
  caution: "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300",
  safe: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300",
};


interface DoseDot {
  drugName: string;
  slotId: TimeSlotId;
}

/** Single time slot column in the timeline grid */
function TimeSlotColumn({
  slot,
  doses,
  conflicts,
}: {
  slot: (typeof TIME_SLOTS)[number];
  doses: DoseDot[];
  conflicts: FoodInteraction[];
}) {
  const hasConflict = conflicts.some((c) => c.severity === "avoid");
  const hasCaution = conflicts.some((c) => c.severity === "caution");

  return (
    <div className="flex flex-col items-center gap-2 min-w-[80px]">
      {/* Time label */}
      <div className="text-center">
        <div className="text-xs font-semibold text-[var(--foreground)]">{slot.label}</div>
        <div className="text-[10px] text-[var(--muted-foreground)]">{slot.display}</div>
      </div>

      {/* Column bar */}
      <div
        className={`relative w-14 rounded-lg border-2 min-h-[120px] flex flex-col items-center justify-start pt-2 gap-1 ${
          hasConflict
            ? "border-red-400 bg-red-50 dark:bg-red-950/20"
            : hasCaution
              ? "border-amber-400 bg-amber-50 dark:bg-amber-950/20"
              : "border-[var(--border)] bg-[var(--secondary)]"
        }`}
      >
        {/* Drug dose pills */}
        {doses.map((dose, i) => (
          <div
            key={i}
            title={dose.drugName}
            className="w-10 rounded-full bg-[var(--primary)] px-1.5 py-0.5 text-center text-[9px] font-medium text-white truncate"
          >
            {dose.drugName.slice(0, 8)}
          </div>
        ))}

        {/* Warning icon */}
        {(hasConflict || hasCaution) && (
          <div
            className={`absolute -top-2 -right-2 rounded-full p-0.5 ${
              hasConflict ? "bg-red-500" : "bg-amber-500"
            }`}
          >
            <AlertTriangle className="h-3 w-3 text-white" />
          </div>
        )}
      </div>
    </div>
  );
}

export function FoodInteractionTimeline({
  drugs,
  foodInteractions,
}: FoodInteractionTimelineProps) {
  // Default: spread drugs evenly across time slots
  const [doseTimes, setDoseTimes] = useState<Record<string, TimeSlotId>>(() => {
    const defaults: Record<string, TimeSlotId> = {};
    drugs.forEach((drug, i) => {
      const slots: TimeSlotId[] = ["morning", "noon", "evening", "night"];
      defaults[drug.id] = slots[i % slots.length];
    });
    return defaults;
  });

  if (foodInteractions.length === 0) return null;

  const handleSlotChange = (drugId: string, slot: TimeSlotId) => {
    setDoseTimes((prev) => ({ ...prev, [drugId]: slot }));
  };

  // Build conflicts per time slot
  const conflictsBySlot = TIME_SLOTS.reduce<Record<TimeSlotId, FoodInteraction[]>>(
    (acc, slot) => {
      acc[slot.id] = [];
      return acc;
    },
    {} as Record<TimeSlotId, FoodInteraction[]>
  );

  foodInteractions.forEach((fi) => {
    const assignedSlot = doseTimes[fi.drug_id];
    if (assignedSlot && fi.severity !== "safe") {
      conflictsBySlot[assignedSlot].push(fi);
    }
  });

  // Build doses per slot
  const dosesBySlot = TIME_SLOTS.reduce<Record<TimeSlotId, DoseDot[]>>(
    (acc, slot) => {
      acc[slot.id] = [];
      return acc;
    },
    {} as Record<TimeSlotId, DoseDot[]>
  );

  drugs.forEach((drug) => {
    const slot = doseTimes[drug.id];
    if (slot) {
      dosesBySlot[slot].push({ drugName: drug.name, slotId: slot });
    }
  });

  const avoidInteractions = foodInteractions.filter((fi) => fi.severity === "avoid");
  const cautionInteractions = foodInteractions.filter((fi) => fi.severity === "caution");

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="flex items-center gap-2">
        <Utensils className="h-4 w-4 text-[var(--primary)]" />
        <h3 className="font-semibold text-sm text-[var(--foreground)]">
          Food Interaction Timeline
        </h3>
      </div>

      {/* Dosing time assignment */}
      <div className="rounded-lg border border-[var(--border)] bg-[var(--card)] p-4 space-y-3">
        <p className="text-xs text-[var(--muted-foreground)] flex items-center gap-1">
          <Clock className="h-3.5 w-3.5" />
          Assign dosing times to see food-timing conflicts:
        </p>
        <div className="space-y-2">
          {drugs.map((drug) => (
            <div key={drug.id} className="flex items-center justify-between gap-3">
              <span className="text-sm text-[var(--foreground)] font-medium min-w-[120px] truncate">
                {drug.name}
              </span>
              <div className="flex gap-1.5 flex-wrap">
                {TIME_SLOTS.map((slot) => (
                  <button
                    key={slot.id}
                    type="button"
                    onClick={() => handleSlotChange(drug.id, slot.id)}
                    className={`rounded px-2 py-0.5 text-xs border transition-colors ${
                      doseTimes[drug.id] === slot.id
                        ? "bg-[var(--primary)] text-white border-[var(--primary)]"
                        : "border-[var(--border)] text-[var(--muted-foreground)] hover:bg-[var(--accent)]"
                    }`}
                  >
                    {slot.label}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Timeline grid */}
      <div className="overflow-x-auto">
        <div className="flex gap-4 min-w-max pb-2">
          {TIME_SLOTS.map((slot) => (
            <TimeSlotColumn
              key={slot.id}
              slot={slot}
              doses={dosesBySlot[slot.id]}
              conflicts={conflictsBySlot[slot.id]}
            />
          ))}
        </div>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap items-center gap-3 text-xs">
        <span className="text-[var(--muted-foreground)] font-medium">Legend:</span>
        <span className="flex items-center gap-1 rounded-full border border-red-400 bg-red-50 px-2 py-0.5 text-red-700 dark:bg-red-950/20 dark:text-red-300">
          <AlertTriangle className="h-3 w-3" /> Avoid
        </span>
        <span className="flex items-center gap-1 rounded-full border border-amber-400 bg-amber-50 px-2 py-0.5 text-amber-700 dark:bg-amber-950/20 dark:text-amber-300">
          <AlertTriangle className="h-3 w-3" /> Caution
        </span>
        <span className="flex items-center gap-1 rounded-full border border-green-400 bg-green-50 px-2 py-0.5 text-green-700 dark:bg-green-950/20 dark:text-green-300">
          <Info className="h-3 w-3" /> Safe
        </span>
      </div>

      {/* Interaction details */}
      {(avoidInteractions.length > 0 || cautionInteractions.length > 0) && (
        <div className="space-y-2">
          {avoidInteractions.map((fi, i) => (
            <div
              key={i}
              className={`rounded-lg border p-3 ${SEVERITY_COLOURS["avoid"]}`}
            >
              <div className="flex items-start gap-2">
                <span className={`mt-0.5 rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide ${SEVERITY_BADGE["avoid"]}`}>
                  Avoid
                </span>
                <div className="space-y-0.5">
                  <p className="text-xs font-semibold">
                    {fi.drug_name} + {fi.food_item}
                  </p>
                  <p className="text-xs">{fi.description}</p>
                  {fi.timing_note && (
                    <p className="text-[10px] text-[var(--muted-foreground)] italic">
                      {fi.timing_note}
                    </p>
                  )}
                </div>
              </div>
            </div>
          ))}
          {cautionInteractions.map((fi, i) => (
            <div
              key={i}
              className={`rounded-lg border p-3 ${SEVERITY_COLOURS["caution"]}`}
            >
              <div className="flex items-start gap-2">
                <span className={`mt-0.5 rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide ${SEVERITY_BADGE["caution"]}`}>
                  Caution
                </span>
                <div className="space-y-0.5">
                  <p className="text-xs font-semibold">
                    {fi.drug_name} + {fi.food_item}
                  </p>
                  <p className="text-xs">{fi.description}</p>
                  {fi.timing_note && (
                    <p className="text-[10px] text-[var(--muted-foreground)] italic">
                      {fi.timing_note}
                    </p>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
