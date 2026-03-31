"""
DrugBank data parser for MEDGRAPH.

DrugBank Open Data requires free registration. This module provides:
1. A parser for downloaded DrugBank CSV files (when available)
2. Falls back to built-in seed_data if DrugBank files are not present

DrugBank Open Data: https://go.drugbank.com/releases/latest#open-data
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from medgraph.graph.models import Drug, DrugEnzymeRelation, Interaction

if TYPE_CHECKING:
    from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)

# Severity keyword mapping from description text
_SEVERITY_KEYWORDS = {
    "critical": ["contraindicated", "life-threatening", "fatal", "avoid"],
    "major": ["serious", "significant", "severe", "major", "substantial"],
    "moderate": ["moderate", "caution", "monitor", "careful", "adjust"],
    "minor": ["minor", "mild", "minimal", "slight"],
}

# Map DrugBank enzyme names to standardized CYP IDs
_ENZYME_ID_MAP: dict[str, str] = {
    "CYP3A4": "CYP3A4",
    "Cytochrome P450 3A4": "CYP3A4",
    "CYP3A5": "CYP3A4",  # Group with 3A4
    "CYP2D6": "CYP2D6",
    "Cytochrome P450 2D6": "CYP2D6",
    "CYP2C9": "CYP2C9",
    "Cytochrome P450 2C9": "CYP2C9",
    "CYP2C19": "CYP2C19",
    "Cytochrome P450 2C19": "CYP2C19",
    "CYP1A2": "CYP1A2",
    "Cytochrome P450 1A2": "CYP1A2",
    "CYP2B6": "CYP2B6",
    "Cytochrome P450 2B6": "CYP2B6",
    "P-glycoprotein": "PGLYCO",
    "P-glycoprotein 1": "PGLYCO",
    "MDR1": "PGLYCO",
    "ABCB1": "PGLYCO",
}


def classify_severity(description: str) -> str:
    """
    Classify interaction severity from description text using keyword matching.

    Returns: "critical" | "major" | "moderate" | "minor"
    """
    text = description.lower()
    for severity, keywords in _SEVERITY_KEYWORDS.items():
        if any(k in text for k in keywords):
            return severity
    return "minor"


def normalize_enzyme_id(enzyme_name: str) -> Optional[str]:
    """Map an enzyme name string to a standardized enzyme ID, or None if unknown."""
    return _ENZYME_ID_MAP.get(enzyme_name)


class DrugBankParser:
    """
    Parser for DrugBank Open Data CSV files.

    Usage:
        parser = DrugBankParser(cache_dir=Path("data/drugbank"))
        drugs = parser.parse_drugs()
        interactions = parser.parse_interactions()
        relations = parser.parse_enzyme_relations()

    If DrugBank files are not present, methods return empty lists and log a warning.
    The seed.py orchestrator supplements with built-in seed_data.
    """

    VOCAB_FILENAME = "drugbank_vocabulary.csv"
    INTERACTIONS_FILENAME = "drug-drug-interactions.csv"
    ENZYMES_FILENAME = "drug-enzymes.csv"

    def __init__(self, cache_dir: Path = Path("data/drugbank")) -> None:
        self.cache_dir = Path(cache_dir)

    def is_available(self) -> bool:
        """Check if DrugBank CSV files are present."""
        return (self.cache_dir / self.VOCAB_FILENAME).exists() or (
            self.cache_dir / self.INTERACTIONS_FILENAME
        ).exists()

    def parse_drugs(self) -> list[Drug]:
        """
        Parse drug vocabulary CSV.

        Expected columns: DrugBank ID, Accession Numbers, Common name,
        CAS, UNII, Synonyms, Standard InChI Key
        """
        path = self.cache_dir / self.VOCAB_FILENAME
        if not path.exists():
            logger.warning(
                f"DrugBank vocabulary not found at {path}. "
                "Run: download DrugBank open data to data/drugbank/"
            )
            return []

        drugs: list[Drug] = []
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    drug_id = row.get("DrugBank ID", "").strip()
                    name = row.get("Common name", "").strip()
                    if not drug_id or not name:
                        continue
                    synonyms_raw = row.get("Synonyms", "")
                    brand_names = [s.strip() for s in synonyms_raw.split("|") if s.strip()]
                    drugs.append(
                        Drug(
                            id=drug_id,
                            name=name,
                            brand_names=brand_names[:10],  # cap at 10
                            description="",
                            drug_class=None,
                            rxnorm_cui=None,
                        )
                    )
        except Exception as e:
            logger.error(f"Error parsing DrugBank vocabulary: {e}")

        logger.info(f"Parsed {len(drugs)} drugs from DrugBank vocabulary")
        return drugs

    def parse_interactions(self) -> list[Interaction]:
        """
        Parse drug-drug interactions CSV.

        Expected columns: Drug1 DrugBank ID, Drug1 Name, Drug2 DrugBank ID,
        Drug2 Name, Description
        """
        path = self.cache_dir / self.INTERACTIONS_FILENAME
        if not path.exists():
            logger.warning(f"DrugBank interactions not found at {path}.")
            return []

        interactions: list[Interaction] = []
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    drug_a = row.get("Drug1 DrugBank ID", "").strip()
                    drug_b = row.get("Drug2 DrugBank ID", "").strip()
                    desc = row.get("Description", "").strip()
                    if not drug_a or not drug_b:
                        continue
                    severity = classify_severity(desc)
                    interactions.append(
                        Interaction(
                            id=f"DB-INT-{drug_a}-{drug_b}",
                            drug_a_id=drug_a,
                            drug_b_id=drug_b,
                            severity=severity,
                            description=desc,
                            mechanism=None,
                            source="drugbank",
                            evidence_count=0,
                        )
                    )
        except Exception as e:
            logger.error(f"Error parsing DrugBank interactions: {e}")

        logger.info(f"Parsed {len(interactions)} interactions from DrugBank")
        return interactions

    def parse_enzyme_relations(self) -> list[DrugEnzymeRelation]:
        """
        Parse drug-enzyme relations CSV.

        Expected columns: DrugBank ID, Drug Name, UniProt ID, Protein Name,
        Gene Name, Action, Pharmacological Action
        """
        path = self.cache_dir / self.ENZYMES_FILENAME
        if not path.exists():
            logger.warning(f"DrugBank enzyme relations not found at {path}.")
            return []

        relations: list[DrugEnzymeRelation] = []
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    drug_id = row.get("DrugBank ID", "").strip()
                    protein_name = row.get("Protein Name", "").strip()
                    gene = row.get("Gene Name", "").strip()
                    action = row.get("Action", "").strip().lower()

                    if not drug_id:
                        continue

                    # Try to map enzyme name
                    enzyme_id = normalize_enzyme_id(protein_name) or normalize_enzyme_id(gene)
                    if not enzyme_id:
                        continue  # Not a CYP450 or recognized enzyme

                    # Map action to relation_type
                    if "inhibit" in action:
                        relation_type = "inhibits"
                        strength = "strong" if "strong" in action else "moderate"
                    elif "induc" in action:
                        relation_type = "induces"
                        strength = "strong" if "strong" in action else "moderate"
                    elif "substrate" in action or "metaboli" in action:
                        relation_type = "metabolized_by"
                        strength = "moderate"
                    else:
                        continue  # Skip unknown action types

                    relations.append(
                        DrugEnzymeRelation(
                            drug_id=drug_id,
                            enzyme_id=enzyme_id,
                            relation_type=relation_type,
                            strength=strength,
                        )
                    )
        except Exception as e:
            logger.error(f"Error parsing DrugBank enzyme relations: {e}")

        logger.info(f"Parsed {len(relations)} enzyme relations from DrugBank")
        return relations


# ---------------------------------------------------------------------------
# Full import with batch inserts, progress reporting, and duplicate detection
# ---------------------------------------------------------------------------

_DRUG_CLASS_KEYWORDS: dict[str, list[str]] = {
    "anticoagulant": ["warfarin", "heparin", "apixaban", "rivaroxaban", "dabigatran"],
    "antiplatelet": ["aspirin", "clopidogrel", "ticagrelor", "prasugrel"],
    "antidepressant": ["fluoxetine", "sertraline", "paroxetine", "escitalopram", "venlafaxine"],
    "antihypertensive": ["lisinopril", "enalapril", "amlodipine", "metoprolol", "atenolol"],
    "antibiotic": ["amoxicillin", "ciprofloxacin", "azithromycin", "doxycycline", "metronidazole"],
    "statin": ["simvastatin", "atorvastatin", "rosuvastatin", "pravastatin", "lovastatin"],
    "opioid": ["morphine", "oxycodone", "hydrocodone", "fentanyl", "codeine"],
    "antifungal": ["fluconazole", "itraconazole", "ketoconazole", "voriconazole"],
    "antiviral": ["ritonavir", "lopinavir", "atazanavir", "efavirenz", "tenofovir"],
    "nsaid": ["ibuprofen", "naproxen", "celecoxib", "diclofenac", "indomethacin"],
}


def _infer_drug_class(name: str) -> Optional[str]:
    """Infer a basic drug class from the drug name using keyword matching."""
    lower = name.lower()
    for cls, keywords in _DRUG_CLASS_KEYWORDS.items():
        if any(k in lower for k in keywords):
            return cls
    return None


def import_drugbank_full(
    store: "GraphStore",
    csv_path: Path,
    batch_size: int = 1000,
    show_progress: bool = True,
) -> dict[str, int]:
    """
    Import full DrugBank open dataset CSV into the graph store.

    Handles ~2,700 drugs with batch inserts and duplicate detection.

    Args:
        store: GraphStore instance to insert into.
        csv_path: Path to DrugBank vocabulary CSV (drugbank_vocabulary.csv).
        batch_size: Records per transaction (default 1000).
        show_progress: Show rich progress bar (default True).

    Returns:
        dict with keys: inserted, skipped, errors
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"DrugBank CSV not found: {csv_path}")

    # Try importing rich.progress — fall back gracefully if unavailable
    try:
        from rich.progress import (
            BarColumn,
            Progress,
            SpinnerColumn,
            TaskProgressColumn,
            TextColumn,
            TimeElapsedColumn,
        )

        _rich_available = True
    except ImportError:
        _rich_available = False

    # Collect existing drug names for duplicate detection
    with store._connect() as conn:
        existing_names: set[str] = {
            row[0].lower() for row in conn.execute("SELECT name FROM drugs").fetchall()
        }

    stats = {"inserted": 0, "skipped": 0, "errors": 0}
    batch: list[Drug] = []

    def _flush_batch(batch: list[Drug]) -> None:
        """Insert a batch of drugs in a single transaction."""
        with store._connect() as conn:
            for drug in batch:
                try:
                    conn.execute(
                        """INSERT OR IGNORE INTO drugs
                           (id, name, brand_names, description, drug_class,
                            rxnorm_cui, category, atc_code, last_updated)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            drug.id,
                            drug.name,
                            __import__("json").dumps(drug.brand_names or []),
                            drug.description or "",
                            drug.drug_class,
                            drug.rxnorm_cui,
                            drug.category if hasattr(drug, "category") else None,
                            None,
                            __import__("datetime")
                            .datetime.now(__import__("datetime").timezone.utc)
                            .isoformat(),
                        ),
                    )
                    stats["inserted"] += 1
                except Exception as exc:
                    logger.debug("Batch insert error for drug %s: %s", drug.id, exc)
                    stats["errors"] += 1

    def _process_rows(rows: list[dict]) -> None:
        nonlocal batch
        for row in rows:
            drug_id = row.get("DrugBank ID", "").strip()
            name = row.get("Common name", "").strip()
            if not drug_id or not name:
                stats["errors"] += 1
                continue
            if name.lower() in existing_names:
                stats["skipped"] += 1
                continue
            existing_names.add(name.lower())

            synonyms_raw = row.get("Synonyms", "")
            brand_names = [s.strip() for s in synonyms_raw.split("|") if s.strip()][:10]
            inferred_class = _infer_drug_class(name)

            batch.append(
                Drug(
                    id=drug_id,
                    name=name,
                    brand_names=brand_names,
                    description="",
                    drug_class=inferred_class,
                    rxnorm_cui=None,
                )
            )
            if len(batch) >= batch_size:
                _flush_batch(batch)
                batch = []

    # Count rows for progress bar
    with open(csv_path, newline="", encoding="utf-8") as f:
        total_rows = sum(1 for _ in f) - 1  # subtract header

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)

    if show_progress and _rich_available:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
        ) as progress:
            task = progress.add_task(
                f"[cyan]Importing DrugBank ({csv_path.name})…", total=total_rows
            )
            chunk_size = batch_size
            for i in range(0, len(all_rows), chunk_size):
                chunk = all_rows[i : i + chunk_size]
                _process_rows(chunk)
                progress.advance(task, len(chunk))
    else:
        _process_rows(all_rows)

    # Flush remaining
    if batch:
        _flush_batch(batch)

    logger.info(
        "DrugBank import complete: inserted=%d skipped=%d errors=%d",
        stats["inserted"],
        stats["skipped"],
        stats["errors"],
    )
    return stats
