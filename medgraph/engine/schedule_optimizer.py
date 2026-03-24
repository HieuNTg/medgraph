"""
Medication Schedule Optimizer for MEDGRAPH.

Assigns drug doses to time slots minimizing interaction windows.
Drugs that interact are spaced at least 4 hours apart.

Algorithm: greedy assignment — for each drug, pick the time slot
that is furthest from any conflicting drug already scheduled there.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)

# Available time slots (label → hour in 24h format)
TIME_SLOTS: dict[str, int] = {
    "morning": 8,    # 8:00 AM
    "noon": 12,      # 12:00 PM
    "evening": 18,   # 6:00 PM
    "night": 22,     # 10:00 PM
}

# Minimum hours between interacting drugs
MIN_HOURS_APART = 4


@dataclass
class ScheduledDrug:
    """A drug with its assigned time slot(s)."""

    drug_id: str
    drug_name: str
    time_slots: list[str]  # one per daily dose
    frequency: int  # doses per day (1, 2, or 3)
    interacts_with: list[str] = field(default_factory=list)  # drug_ids


@dataclass
class ScheduleResult:
    """Result of schedule optimization."""

    schedule: dict[str, list[ScheduledDrug]]  # slot_label → drugs at that slot
    warnings: list[str]
    disclaimer: str = (
        "This schedule is generated algorithmically. "
        "Always confirm medication timing with your pharmacist or physician."
    )

    def to_dict(self) -> dict:
        return {
            "schedule": {
                slot: [
                    {
                        "drug_id": d.drug_id,
                        "drug_name": d.drug_name,
                        "frequency": d.frequency,
                    }
                    for d in drugs
                ]
                for slot, drugs in self.schedule.items()
            },
            "warnings": self.warnings,
            "disclaimer": self.disclaimer,
        }


def _hours_between(slot_a: str, slot_b: str) -> int:
    """Return the absolute hour difference between two time slots."""
    return abs(TIME_SLOTS[slot_a] - TIME_SLOTS[slot_b])


def _all_slots_for_frequency(frequency: int) -> list[list[str]]:
    """
    Return valid slot combinations for a given frequency.

    1/day → any single slot
    2/day → pairs at least 8h apart
    3/day → morning + noon + evening
    """
    slot_names = list(TIME_SLOTS.keys())
    if frequency == 1:
        return [[s] for s in slot_names]
    if frequency == 2:
        return [
            [a, b]
            for i, a in enumerate(slot_names)
            for b in slot_names[i + 1:]
            if _hours_between(a, b) >= 8
        ]
    # 3x/day default: morning, noon, evening
    return [["morning", "noon", "evening"]]


class ScheduleOptimizer:
    """
    Greedy medication schedule optimizer.

    Assigns drugs to time slots so that interacting drug pairs are
    separated by at least MIN_HOURS_APART (default 4 hours).
    """

    def __init__(self, store: "GraphStore | None" = None) -> None:
        self._store = store

    def optimize(
        self,
        drugs: list[dict],  # [{"drug_id": str, "drug_name": str, "frequency": int}, ...]
        interactions: list[tuple[str, str]] | None = None,
    ) -> ScheduleResult:
        """
        Compute an optimized medication schedule.

        Args:
            drugs: List of drug dicts with drug_id, drug_name, frequency (1/2/3).
            interactions: Optional list of (drug_a_id, drug_b_id) pairs that interact.
                          If None and store is set, will query the DB.

        Returns:
            ScheduleResult with schedule dict and any warnings.
        """
        if not drugs:
            return ScheduleResult(schedule={slot: [] for slot in TIME_SLOTS}, warnings=[])

        # Resolve interactions from store if not provided
        if interactions is None:
            interactions = self._load_interactions([d["drug_id"] for d in drugs])

        # Build adjacency: drug_id → set of conflicting drug_ids
        conflict_map: dict[str, set[str]] = {d["drug_id"]: set() for d in drugs}
        for a, b in (interactions or []):
            if a in conflict_map:
                conflict_map[a].add(b)
            if b in conflict_map:
                conflict_map[b].add(a)

        # Assignment state: slot → list of drug_ids already assigned there
        slot_assignments: dict[str, list[str]] = {slot: [] for slot in TIME_SLOTS}
        scheduled: list[ScheduledDrug] = []
        warnings: list[str] = []

        # Sort drugs: most interactions first (hardest to place)
        sorted_drugs = sorted(drugs, key=lambda d: -len(conflict_map.get(d["drug_id"], set())))

        for drug_info in sorted_drugs:
            drug_id = drug_info["drug_id"]
            drug_name = drug_info.get("drug_name", drug_id)
            frequency = max(1, min(3, int(drug_info.get("frequency", 1))))

            best_slots = self._find_best_slots(
                drug_id, frequency, conflict_map, slot_assignments
            )

            if best_slots is None:
                # No conflict-free placement possible — use any valid slots and warn
                fallback = _all_slots_for_frequency(frequency)[0]
                best_slots = fallback
                warnings.append(
                    f"Could not fully separate {drug_name} from interacting drugs. "
                    "Manual scheduling review recommended."
                )

            # Record assignment
            for slot in best_slots:
                slot_assignments[slot].append(drug_id)

            scheduled.append(
                ScheduledDrug(
                    drug_id=drug_id,
                    drug_name=drug_name,
                    time_slots=best_slots,
                    frequency=frequency,
                    interacts_with=list(conflict_map.get(drug_id, set())),
                )
            )

        # Build result schedule: slot → drugs
        drug_by_id = {s.drug_id: s for s in scheduled}
        result_schedule: dict[str, list[ScheduledDrug]] = {slot: [] for slot in TIME_SLOTS}
        for sched_drug in scheduled:
            for slot in sched_drug.time_slots:
                result_schedule[slot].append(sched_drug)

        return ScheduleResult(schedule=result_schedule, warnings=warnings)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _find_best_slots(
        self,
        drug_id: str,
        frequency: int,
        conflict_map: dict[str, set[str]],
        slot_assignments: dict[str, list[str]],
    ) -> list[str] | None:
        """
        Find the best slot combination for this drug such that all conflicting
        drugs assigned so far are at least MIN_HOURS_APART.
        """
        conflicting_ids = conflict_map.get(drug_id, set())

        # Get hours already occupied by conflicting drugs
        conflict_hours: set[int] = set()
        for conf_id in conflicting_ids:
            for slot, assigned in slot_assignments.items():
                if conf_id in assigned:
                    conflict_hours.add(TIME_SLOTS[slot])

        # Try each valid combination for this frequency
        candidates = _all_slots_for_frequency(frequency)
        for combo in candidates:
            combo_hours = [TIME_SLOTS[s] for s in combo]
            # Check all slots in combo are far enough from all conflict hours
            if all(
                abs(h - ch) >= MIN_HOURS_APART
                for h in combo_hours
                for ch in conflict_hours
            ):
                return combo

        # No clean separation possible
        return None

    def _load_interactions(self, drug_ids: list[str]) -> list[tuple[str, str]]:
        """Query DB for interactions between the given drugs."""
        if self._store is None:
            return []
        try:
            with self._store._connect() as conn:
                placeholders = ",".join("?" * len(drug_ids))
                rows = conn.execute(
                    f"""SELECT drug_a_id, drug_b_id FROM interactions
                        WHERE drug_a_id IN ({placeholders})
                        AND drug_b_id IN ({placeholders})""",
                    drug_ids + drug_ids,
                ).fetchall()
            return [(row[0], row[1]) for row in rows]
        except Exception as exc:
            logger.warning("Failed to load interactions for schedule: %s", exc)
            return []
