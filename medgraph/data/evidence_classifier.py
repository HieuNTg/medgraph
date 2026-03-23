"""Evidence level classifier for drug-drug interactions.

Levels:
    A — FDA label / official contraindication
    B — Clinical trial or large cohort study
    C — Case report or small study
    D — Theoretical / in-vitro / mechanistic inference
"""

from __future__ import annotations

_SOURCE_TYPE_LEVELS: dict[str, str] = {
    "fda_label": "A",
    "clinical_trial": "B",
    "cohort_study": "B",
    "case_report": "C",
    "case_series": "C",
    "in_vitro": "D",
    "theoretical": "D",
    "animal_study": "D",
}

_MECHANISM_KEYWORDS_A: tuple[str, ...] = (
    "contraindicated",
    "fda label",
    "fda-approved",
    "boxed warning",
    "black box",
    "prescribing information",
)

_MECHANISM_KEYWORDS_B: tuple[str, ...] = (
    "clinical trial",
    "randomized",
    "rct",
    "pharmacokinetic study",
    "pharmacodynamic study",
    "crossover study",
    "pk study",
    "bioavailability study",
)

_MECHANISM_KEYWORDS_C: tuple[str, ...] = (
    "case report",
    "case series",
    "postmarketing",
    "spontaneous report",
    "faers",
    "adverse event report",
)


class EvidenceClassifier:
    def classify_from_source(self, source_type: str) -> str:
        return _SOURCE_TYPE_LEVELS.get(source_type.lower(), "D")

    def classify(self, description: str = "", mechanism: str = "", source: str = "") -> str:
        text = f"{description} {mechanism} {source}".lower()
        for kw in _MECHANISM_KEYWORDS_A:
            if kw in text:
                return "A"
        for kw in _MECHANISM_KEYWORDS_B:
            if kw in text:
                return "B"
        for kw in _MECHANISM_KEYWORDS_C:
            if kw in text:
                return "C"
        return "D"
