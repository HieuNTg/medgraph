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
from typing import Optional

from medgraph.graph.models import Drug, DrugEnzymeRelation, Interaction

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
