"""
Data seeding orchestrator for MEDGRAPH.

Seeds the SQLite database from built-in data and optionally enriches with
external API data (OpenFDA). Built-in seed data is always applied first,
ensuring the application works without external connectivity.

Usage:
    python -m medgraph.cli seed
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from medgraph.data import seed_data as sd
from medgraph.data.drugbank import DrugBankParser
from medgraph.graph.models import (
    AdverseEvent,
    Drug,
    DrugEnzymeRelation,
    Enzyme,
    Interaction,
)
from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)
console = Console()


class DataSeeder:
    """
    Orchestrates seeding of MEDGRAPH database from available data sources.

    Priority:
    1. Built-in seed_data (always applied) — guaranteed to work offline
    2. DrugBank CSV files (if present in data/drugbank/) — 2700+ drugs
    3. OpenFDA API enrichment (optional, requires internet) — FAERS counts
    """

    def __init__(
        self,
        store: Optional[GraphStore] = None,
        db_path: Path = Path("data/medgraph.db"),
        drugbank_cache_dir: Path = Path("data/drugbank"),
        openfda_cache_dir: Path = Path("data/openfda_cache"),
        skip_openfda: bool = True,
    ) -> None:
        self.store = store or GraphStore(db_path)
        self.drugbank_dir = Path(drugbank_cache_dir)
        self.openfda_dir = Path(openfda_cache_dir)
        self.skip_openfda = skip_openfda

    def run(self) -> dict[str, int]:
        """
        Execute full seed sequence.

        Returns:
            Dict of entity counts after seeding.
        """
        console.print("[bold blue]MEDGRAPH[/] — seeding database...")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
            transient=False,
        ) as progress:
            # Step 1: Built-in seed data (enzymes first, then drugs, then relations)
            task = progress.add_task("Seeding enzymes...", total=None)
            self._seed_enzymes()
            progress.update(task, description="Enzymes seeded", completed=1, total=1)

            task = progress.add_task("Seeding built-in drugs...", total=None)
            self._seed_builtin_drugs()
            progress.update(task, description="Built-in drugs seeded", completed=1, total=1)

            task = progress.add_task("Seeding built-in interactions...", total=None)
            self._seed_builtin_interactions()
            progress.update(task, description="Interactions seeded", completed=1, total=1)

            task = progress.add_task("Seeding drug-enzyme relations...", total=None)
            self._seed_builtin_enzyme_relations()
            progress.update(task, description="Enzyme relations seeded", completed=1, total=1)

            task = progress.add_task("Seeding adverse events...", total=None)
            self._seed_builtin_adverse_events()
            progress.update(task, description="Adverse events seeded", completed=1, total=1)

            # Step 2: Expanded drug data (Flockhart CYP450 + DDInter)
            task = progress.add_task("Seeding expanded drugs...", total=None)
            self._seed_expanded_drugs()
            progress.update(task, description="Expanded drugs seeded", completed=1, total=1)

            task = progress.add_task("Seeding expanded interactions...", total=None)
            self._seed_expanded_interactions()
            progress.update(task, description="Expanded interactions seeded", completed=1, total=1)

            task = progress.add_task("Seeding pharmacogenomics guidelines...", total=None)
            self._seed_pharmacogenomics()
            progress.update(
                task, description="Pharmacogenomics guidelines seeded", completed=1, total=1
            )

            # Step 3: DrugBank data (if available)
            parser = DrugBankParser(self.drugbank_dir)
            if parser.is_available():
                task = progress.add_task("Loading DrugBank data...", total=None)
                self._seed_drugbank(parser, progress, task)
            else:
                console.print(
                    "[dim]DrugBank CSV not found — skipping. "
                    "Place files in data/drugbank/ for 2700+ drugs.[/]"
                )

            # Step 4: OpenFDA enrichment (optional)
            if not self.skip_openfda:
                task = progress.add_task("Enriching with OpenFDA...", total=None)
                self._enrich_openfda()
                progress.update(task, description="OpenFDA enrichment done", completed=1, total=1)

        counts = self.store.get_counts()
        console.print("[bold green]Seeding complete![/]")
        console.print(
            f"  Drugs: [cyan]{counts['drugs']}[/]  "
            f"Enzymes: [cyan]{counts['enzymes']}[/]  "
            f"Interactions: [cyan]{counts['interactions']}[/]  "
            f"Enzyme relations: [cyan]{counts['drug_enzyme_relations']}[/]  "
            f"Adverse events: [cyan]{counts['adverse_events']}[/]"
        )
        return counts

    # -------------------------------------------------------------------------
    # Private seed methods
    # -------------------------------------------------------------------------

    def _seed_enzymes(self) -> None:
        for e in sd.ENZYMES:
            self.store.upsert_enzyme(Enzyme(**e))

    def _seed_builtin_drugs(self) -> None:
        for d in sd.DRUGS:
            self.store.upsert_drug(Drug(**d))

    def _seed_builtin_interactions(self) -> None:
        for i in sd.INTERACTIONS:
            self.store.upsert_interaction(Interaction(**i))

    def _seed_builtin_enzyme_relations(self) -> None:
        for r in sd.DRUG_ENZYME_RELATIONS:
            self.store.upsert_drug_enzyme_relation(DrugEnzymeRelation(**r))

    def _seed_builtin_adverse_events(self) -> None:
        for e in sd.ADVERSE_EVENTS:
            self.store.upsert_adverse_event(AdverseEvent(**e))

    def _seed_expanded_drugs(self) -> None:
        try:
            from medgraph.data.seed_drugs_expanded import DRUGS_EXPANDED

            for d in DRUGS_EXPANDED:
                self.store.upsert_drug(Drug(**d))
        except ImportError:
            logger.debug("seed_drugs_expanded not available — skipping")

    def _seed_expanded_interactions(self) -> None:
        try:
            from medgraph.data.seed_interactions_expanded import (
                INTERACTIONS_EXPANDED,
                DRUG_ENZYME_RELATIONS_EXPANDED,
            )

            for i in INTERACTIONS_EXPANDED:
                self.store.upsert_interaction(Interaction(**i))
            for r in DRUG_ENZYME_RELATIONS_EXPANDED:
                self.store.upsert_drug_enzyme_relation(DrugEnzymeRelation(**r))
        except ImportError:
            logger.debug("seed_interactions_expanded not available — skipping")

    def _seed_pharmacogenomics(self) -> None:
        try:
            from medgraph.data.seed_pharmacogenomics import GENETIC_GUIDELINES
            from medgraph.graph.models import GeneticGuideline

            for g in GENETIC_GUIDELINES:
                self.store.upsert_genetic_guideline(GeneticGuideline(**g))
        except ImportError:
            pass

    def _seed_drugbank(self, parser: DrugBankParser, progress, task) -> None:
        """Seed from DrugBank CSV files."""
        try:
            drugs = parser.parse_drugs()
            progress.update(task, description=f"DrugBank: {len(drugs)} drugs found")
            for drug in drugs:
                self.store.upsert_drug(drug)

            interactions = parser.parse_interactions()
            for interaction in interactions:
                # Only store if both drugs are in our DB
                drug_a = self.store.get_drug_by_id(interaction.drug_a_id)
                drug_b = self.store.get_drug_by_id(interaction.drug_b_id)
                if drug_a and drug_b:
                    self.store.upsert_interaction(interaction)

            relations = parser.parse_enzyme_relations()
            for rel in relations:
                if self.store.get_drug_by_id(rel.drug_id):
                    self.store.upsert_drug_enzyme_relation(rel)

            progress.update(
                task,
                description=(
                    f"DrugBank: {len(drugs)} drugs, "
                    f"{len(interactions)} interactions, "
                    f"{len(relations)} enzyme relations"
                ),
                completed=1,
                total=1,
            )
        except Exception as e:
            logger.error(f"DrugBank seeding failed: {e}")
            progress.update(task, description=f"DrugBank failed: {e}", completed=1, total=1)

    def _enrich_openfda(self) -> None:
        """Optional: Enrich top drugs with FAERS adverse event data."""
        try:
            from medgraph.data.openfda import OpenFDAClient

            client = OpenFDAClient(cache_dir=self.openfda_dir)
            drugs = self.store.get_all_drugs()
            top_drugs = drugs[:50]  # Enrich top 50 drugs

            for drug in top_drugs:
                events = client.search_adverse_events([drug.name])
                for event in events[:5]:  # cap at 5 events per drug
                    self.store.upsert_adverse_event(event)
        except Exception as e:
            logger.warning(f"OpenFDA enrichment failed (non-critical): {e}")
