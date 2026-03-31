"""
MEDGRAPH CLI.

Commands:
    python -m medgraph.cli seed     — Seed database with built-in + optional external data
    python -m medgraph.cli serve    — Start FastAPI server
    python -m medgraph.cli analyze  — Analyze drug interactions from CLI
    python -m medgraph.cli enrich   — Run AI agents to enrich the knowledge graph

Usage:
    python -m medgraph.cli seed
    python -m medgraph.cli seed --include-openfda
    python -m medgraph.cli serve
    python -m medgraph.cli serve --host 0.0.0.0 --port 8080
    python -m medgraph.cli analyze Warfarin Aspirin Clopidogrel
    python -m medgraph.cli enrich --all
    python -m medgraph.cli enrich --agent fda
    python -m medgraph.cli enrich --agent labels
    python -m medgraph.cli enrich --agent severity
"""

from __future__ import annotations

import sys
import json
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

console = Console()


@click.group()
def cli() -> None:
    """MEDGRAPH — Drug Interaction Cascade Analyzer."""
    pass


@cli.command()
@click.option(
    "--db",
    default="data/medgraph.db",
    help="Path to SQLite database file",
    show_default=True,
)
@click.option(
    "--include-openfda",
    is_flag=True,
    default=False,
    help="Also fetch adverse events from OpenFDA API (requires internet, ~10 min)",
)
@click.option(
    "--drugbank-dir",
    default="data/drugbank",
    help="Directory containing DrugBank CSV files (optional)",
    show_default=True,
)
def seed(db: str, include_openfda: bool, drugbank_dir: str) -> None:
    """
    Seed the MEDGRAPH database with drug data.

    By default, uses built-in seed data (works offline).
    Add --include-openfda to enrich with FDA adverse event data.
    Add DrugBank CSVs to data/drugbank/ for 2700+ drugs.
    """
    from medgraph.data.seed import DataSeeder
    from medgraph.graph.store import GraphStore

    db_path = Path(db)
    store = GraphStore(db_path)
    seeder = DataSeeder(
        store=store,
        db_path=db_path,
        drugbank_cache_dir=Path(drugbank_dir),
        skip_openfda=not include_openfda,
    )
    seeder.run()


@cli.command()
@click.option("--host", default="127.0.0.1", help="Host to bind", show_default=True)
@click.option("--port", default=8000, help="Port to bind", show_default=True)
@click.option("--reload", is_flag=True, default=False, help="Enable auto-reload (dev mode)")
@click.option("--workers", default=1, help="Number of worker processes", show_default=True)
def serve(host: str, port: int, reload: bool, workers: int) -> None:
    """Start the MEDGRAPH FastAPI server."""
    import uvicorn

    console.print(
        Panel(
            f"[bold blue]MEDGRAPH[/] API Server\n"
            f"Listening on [cyan]http://{host}:{port}[/]\n"
            f"Docs: [cyan]http://{host}:{port}/docs[/]\n"
            f"\n[dim]DISCLAIMER: For research use only. Not medical advice.[/]",
            expand=False,
        )
    )
    uvicorn.run(
        "medgraph.api.server:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers if not reload else 1,
    )


@cli.command()
@click.argument("drug_names", nargs=-1, required=True)
@click.option("--db", default="data/medgraph.db", help="Database path", show_default=True)
@click.option("--json-output", is_flag=True, default=False, help="Output raw JSON")
def analyze(drug_names: tuple[str, ...], db: str, json_output: bool) -> None:
    """
    Analyze drug interactions from the command line.

    Example: python -m medgraph.cli analyze Warfarin Aspirin Clopidogrel
    """
    from medgraph.engine.analyzer import CascadeAnalyzer
    from medgraph.graph.builder import GraphBuilder
    from medgraph.graph.store import GraphStore

    db_path = Path(db)
    if not db_path.exists():
        console.print(
            f"[red]Database not found:[/] {db_path}\n"
            "Run [bold]python -m medgraph.cli seed[/] first."
        )
        sys.exit(1)

    store = GraphStore(db_path)
    builder = GraphBuilder()

    with console.status("Building knowledge graph..."):
        graph = builder.build(store)

    analyzer = CascadeAnalyzer()

    with console.status(f"Analyzing {len(drug_names)} drugs..."):
        report = analyzer.analyze_by_names(list(drug_names), graph, store)

    if json_output:
        print(json.dumps(report.model_dump(), indent=2))
        return

    # Pretty print
    console.print()
    console.print(
        Panel(
            f"[bold]MEDGRAPH Drug Interaction Report[/]\n"
            f"Drugs: {', '.join(d.name for d in report.drugs)}\n"
            f"Overall Risk: [bold red]{report.overall_risk.upper()}[/]  "
            f"Score: {report.overall_score:.1f}/100\n"
            f"Interactions found: {report.interaction_count}  "
            f"Cascade paths: {report.cascade_count}",
            expand=False,
        )
    )

    for result in report.interactions:
        if result.risk_score == 0 and not result.cascade_paths:
            continue  # Skip no-interaction pairs

        severity_color = {
            "critical": "red",
            "major": "orange3",
            "moderate": "yellow",
            "minor": "blue",
        }.get(result.severity, "white")

        console.print(
            f"\n[bold]{result.drug_a.name}[/] + [bold]{result.drug_b.name}[/]  "
            f"[{severity_color}]{result.severity.upper()}[/]  "
            f"Score: {result.risk_score:.1f}"
        )

        if result.direct_interaction:
            console.print(f"  [dim]Direct:[/] {result.direct_interaction.description[:120]}...")

        for path in result.cascade_paths[:3]:
            console.print(f"  [dim]Cascade:[/] {path.description}")

    console.print(f"\n[dim]{report.disclaimer}[/]")


@cli.command()
@click.option("--db", default="data/medgraph.db", help="Database path", show_default=True)
@click.option(
    "--agent",
    type=click.Choice(["fda", "labels", "severity", "all"]),
    default="all",
    help="Which agent to run",
    show_default=True,
)
@click.option("--max-items", default=50, help="Max items per agent", show_default=True)
def enrich(db: str, agent: str, max_items: int) -> None:
    """
    Run AI agents to enrich the knowledge graph with external data.

    Agents:
        fda      — Fetch FAERS adverse event data from OpenFDA API
        labels   — Extract interaction warnings from FDA drug labels
        severity — Re-classify severity using NLP pattern analysis
        all      — Run all agents in sequence

    Requires internet for FDA/labels agents. Severity agent works offline.
    """
    from medgraph.agents import FDAEnrichmentAgent, LabelParserAgent, SeverityAgent
    from medgraph.graph.store import GraphStore

    db_path = Path(db)
    if not db_path.exists():
        console.print(
            f"[red]Database not found:[/] {db_path}\n"
            "Run [bold]python -m medgraph.cli seed[/] first."
        )
        sys.exit(1)

    store = GraphStore(db_path)
    counts_before = store.get_counts()

    console.print(
        Panel(
            f"[bold blue]MEDGRAPH[/] AI Agent Enrichment\n"
            f"Agent: [cyan]{agent}[/]  Max items: [cyan]{max_items}[/]\n"
            f"DB: {db_path} ({counts_before['drugs']} drugs, "
            f"{counts_before['interactions']} interactions)\n"
            f"\n[dim]Agents enrich the knowledge graph with real FDA data.[/]",
            expand=False,
        )
    )

    agents_to_run = []
    if agent in ("fda", "all"):
        agents_to_run.append(("FDA Enrichment", FDAEnrichmentAgent(store, max_pairs=max_items)))
    if agent in ("labels", "all"):
        agents_to_run.append(("Label Parser", LabelParserAgent(store, max_drugs=max_items)))
    if agent in ("severity", "all"):
        agents_to_run.append(("Severity Classifier", SeverityAgent(store)))

    for name, agent_instance in agents_to_run:
        console.print(f"\n[bold]Running {name} agent...[/]")
        result = agent_instance.run()

        status_color = "green" if result.success else "red"
        console.print(f"  [{status_color}]{result.summary()}[/]")
        if result.errors:
            for err in result.errors[:5]:
                console.print(f"  [red]  Error: {err}[/]")

    counts_after = store.get_counts()
    console.print(
        f"\n[bold green]Enrichment complete![/]\n"
        f"  Interactions: {counts_before['interactions']} -> {counts_after['interactions']}\n"
        f"  Adverse events: {counts_before['adverse_events']} -> {counts_after['adverse_events']}"
    )


@cli.command()
@click.option("--db", default="data/medgraph.db", help="Database path", show_default=True)
def expand(db: str) -> None:
    """Expand database with additional drug data (Flockhart CYP450 + DDInter)."""
    from medgraph.data.seed import DataSeeder
    from medgraph.graph.store import GraphStore

    db_path = Path(db)
    store = GraphStore(db_path)
    seeder = DataSeeder(store=store, db_path=db_path)
    seeder.seed_expanded()
    counts = seeder.store.get_counts()
    console.print("[bold green]Database expanded![/]")
    console.print(
        f"  Drugs: [cyan]{counts['drugs']}[/]  "
        f"Interactions: [cyan]{counts['interactions']}[/]  "
        f"Enzyme relations: [cyan]{counts['drug_enzyme_relations']}[/]"
    )


@cli.group()
def db() -> None:
    """Database management commands (migrate, backup, restore)."""
    pass


@db.command()
@click.option(
    "--db-path", "db_path", default="data/medgraph.db", help="Database path", show_default=True
)
@click.option("--revision", default="head", help="Target revision", show_default=True)
def upgrade(db_path: str, revision: str) -> None:
    """Run database migrations up to the target revision."""
    from medgraph.migrations.runner import upgrade as run_upgrade

    console.print(f"[bold blue]MEDGRAPH[/] — running migrations to [cyan]{revision}[/]...")
    run_upgrade(db_path=db_path, revision=revision)
    console.print("[bold green]Migrations applied successfully.[/]")


@db.command()
@click.option(
    "--db-path", "db_path", default="data/medgraph.db", help="Database path", show_default=True
)
@click.option("--revision", default="-1", help="Target revision", show_default=True)
def downgrade(db_path: str, revision: str) -> None:
    """Downgrade database by one revision (or to a specific revision)."""
    from medgraph.migrations.runner import downgrade as run_downgrade

    console.print(f"[bold blue]MEDGRAPH[/] — downgrading to [cyan]{revision}[/]...")
    run_downgrade(db_path=db_path, revision=revision)
    console.print("[bold green]Downgrade complete.[/]")


@db.command()
@click.option(
    "--db-path", "db_path", default="data/medgraph.db", help="Database path", show_default=True
)
def status(db_path: str) -> None:
    """Show current migration revision."""
    from medgraph.migrations.runner import current

    rev = current(db_path=db_path)
    console.print(f"Current migration revision: [cyan]{rev or 'not stamped'}[/]")


@db.command()
@click.option(
    "--db-path", "db_path", default="data/medgraph.db", help="Database path", show_default=True
)
@click.option(
    "--output",
    "-o",
    default=None,
    help="Output file path (default: data/backups/medgraph-<timestamp>.db)",
)
def backup(db_path: str, output: str | None) -> None:
    """Create a backup of the database."""
    from datetime import datetime

    from medgraph.graph.store import GraphStore

    store = GraphStore(Path(db_path))

    if output is None:
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        output = f"data/backups/medgraph-{ts}.db"

    dest = store.backup(output)
    console.print(f"[bold green]Backup created:[/] {dest}")


@db.command()
@click.option(
    "--db-path", "db_path", default="data/medgraph.db", help="Database path", show_default=True
)
@click.argument("backup_file")
def restore(db_path: str, backup_file: str) -> None:
    """Restore the database from a backup file."""
    from medgraph.graph.store import GraphStore

    backup_path = Path(backup_file)
    if not backup_path.exists():
        console.print(f"[red]Backup file not found:[/] {backup_path}")
        sys.exit(1)

    store = GraphStore(Path(db_path))
    store.restore(backup_path)
    console.print(f"[bold green]Database restored from:[/] {backup_path}")


@cli.command("import-drugbank")
@click.argument("csv_path")
@click.option("--db", default="data/medgraph.db", help="Database path", show_default=True)
@click.option("--batch-size", default=1000, help="Records per transaction", show_default=True)
def import_drugbank(csv_path: str, db: str, batch_size: int) -> None:
    """
    Import full DrugBank open dataset CSV into the database.

    Supports ~2,700 drugs with batch inserts, progress reporting,
    brand name extraction, drug class categorization, and duplicate detection.

    CSV_PATH: Path to DrugBank vocabulary CSV (drugbank_vocabulary.csv).
    """
    from medgraph.data.drugbank import import_drugbank_full
    from medgraph.graph.store import GraphStore

    db_path = Path(db)
    store = GraphStore(db_path)
    counts_before = store.get_counts()

    console.print(
        Panel(
            f"[bold blue]MEDGRAPH[/] DrugBank Full Import\n"
            f"CSV: [cyan]{csv_path}[/]\n"
            f"Batch size: [cyan]{batch_size}[/]  "
            f"Current drugs: [cyan]{counts_before['drugs']}[/]",
            expand=False,
        )
    )

    try:
        stats = import_drugbank_full(
            store=store,
            csv_path=Path(csv_path),
            batch_size=batch_size,
            show_progress=True,
        )
    except FileNotFoundError as exc:
        console.print(f"[red]Error:[/] {exc}")
        sys.exit(1)

    counts_after = store.get_counts()
    console.print(
        f"\n[bold green]Import complete![/]\n"
        f"  Inserted: [cyan]{stats['inserted']}[/]\n"
        f"  Skipped (duplicates): [cyan]{stats['skipped']}[/]\n"
        f"  Errors: [cyan]{stats['errors']}[/]\n"
        f"  Total drugs now: [cyan]{counts_after['drugs']}[/]"
    )


@cli.command("refresh")
@click.option("--db", default="data/medgraph.db", help="Database path", show_default=True)
@click.option(
    "--schedule",
    type=click.Choice(["weekly", "daily"]),
    default=None,
    help="Run on a schedule, skipping if data is fresh",
)
@click.option(
    "--sources",
    default=None,
    help="Comma-separated sources to refresh (drugbank,openfda)",
)
@click.option(
    "--force",
    is_flag=True,
    default=False,
    help="Force refresh even if data is fresh",
)
@click.option(
    "--history",
    is_flag=True,
    default=False,
    help="Show recent refresh history instead of running a refresh",
)
@click.option(
    "--limit",
    default=20,
    help="Number of history entries to show (used with --history)",
    show_default=True,
)
def refresh(
    db: str,
    schedule: str | None,
    sources: str | None,
    force: bool,
    history: bool,
    limit: int,
) -> None:
    """
    Run data refresh from external sources, or view refresh history.

    Examples:
        python -m medgraph.cli refresh
        python -m medgraph.cli refresh --sources openfda --force
        python -m medgraph.cli refresh --history
        python -m medgraph.cli refresh --schedule weekly
    """
    import asyncio

    from medgraph.data.refresh_pipeline import DataRefreshPipeline
    from medgraph.data.refresh_service import RefreshService
    from medgraph.graph.store import GraphStore

    db_path = Path(db)
    if not db_path.exists():
        console.print(
            f"[red]Database not found:[/] {db_path}\n"
            "Run [bold]python -m medgraph.cli seed[/] first."
        )
        sys.exit(1)

    store = GraphStore(db_path)

    # -- History mode -------------------------------------------------------
    if history:
        svc = RefreshService(store)
        rows = store.get_refresh_history(limit=limit)
        if not rows:
            console.print("[dim]No refresh history found.[/]")
            return
        console.print(
            Panel(
                f"[bold blue]MEDGRAPH[/] Refresh History (last {len(rows)} entries)",
                expand=False,
            )
        )
        for row in rows:
            status_color = "green" if row["status"] == "completed" else "red"
            console.print(
                f"  [{status_color}]{row['status'].upper()}[/]  "
                f"source={row['source']}  "
                f"records={row['records_updated']}  "
                f"at={row['created_at']}"
            )
        return

    # -- Incremental refresh (via RefreshService) ---------------------------
    source_list = [s.strip() for s in sources.split(",")] if sources else None

    if schedule:
        # Use legacy pipeline for scheduled / freshness-aware refresh
        pipeline = DataRefreshPipeline(store)
        console.print(f"[bold blue]MEDGRAPH[/] Scheduled refresh — [cyan]{schedule}[/]")
        result = pipeline.schedule_refresh(sources=source_list, schedule=schedule, force=force)
        if result is None:
            freshness = pipeline.get_freshness()
            console.print(
                f"[dim]Skipped — data is fresh. "
                f"Last updated: {freshness.get('last_updated', 'unknown')}[/]"
            )
            return
        status_color = "green" if result.success else "red"
        console.print(
            f"\n[bold {status_color}]Refresh {'complete' if result.success else 'failed'}![/]\n"
            f"  Sources attempted: {', '.join(result.sources_attempted)}\n"
            f"  Succeeded: {', '.join(result.sources_succeeded) or 'none'}\n"
            f"  Failed: {', '.join(result.sources_failed) or 'none'}\n"
            f"  Records updated: [cyan]{result.records_updated}[/]"
        )
        if result.errors:
            for src, err in result.errors.items():
                console.print(f"  [red]  {src}: {err}[/]")
        return

    # Default: incremental refresh via RefreshService
    console.print("[bold blue]MEDGRAPH[/] Running incremental FAERS refresh…")
    svc = RefreshService(store)

    with console.status("Querying OpenFDA FAERS…"):
        job = asyncio.run(svc.trigger_refresh(sources=source_list, force=force))

    status_color = "green" if job.status == "completed" else "red"
    console.print(
        f"\n[bold {status_color}]Refresh {job.status}![/]\n"
        f"  Job ID: [dim]{job.job_id}[/]\n"
        f"  Sources attempted: {', '.join(job.sources_attempted)}\n"
        f"  Succeeded: {', '.join(job.sources_succeeded) or 'none'}\n"
        f"  Failed: {', '.join(job.sources_failed) or 'none'}\n"
        f"  Records updated: [cyan]{job.records_updated}[/]"
    )
    if job.errors:
        for src, err in job.errors.items():
            console.print(f"  [red]  {src}: {err}[/]")


@cli.command("enrich-pubmed")
@click.option("--db", default="data/medgraph.db", help="Database path", show_default=True)
@click.option(
    "--max-pairs",
    default=20,
    help="Maximum interaction pairs to enrich",
    show_default=True,
)
@click.option(
    "--max-results",
    default=5,
    help="Max PubMed articles per drug pair",
    show_default=True,
)
def enrich_pubmed(db: str, max_pairs: int, max_results: int) -> None:
    """
    Enrich drug interactions with PubMed literature evidence.

    Searches NCBI PubMed for published evidence on drug-drug interactions
    and stores the top articles as evidence sources in the database.

    Rate-limited to <3 requests/second (NCBI free tier).
    """
    from medgraph.data.pubmed_agent import PubMedAgent, enrich_interaction
    from medgraph.graph.store import GraphStore

    db_path = Path(db)
    if not db_path.exists():
        console.print(
            f"[red]Database not found:[/] {db_path}\n"
            "Run [bold]python -m medgraph.cli seed[/] first."
        )
        sys.exit(1)

    store = GraphStore(db_path)
    agent = PubMedAgent(max_results=max_results)

    # Get top interactions to enrich
    with store._connect() as conn:
        rows = conn.execute(
            "SELECT id, drug_a_id, drug_b_id FROM interactions "
            "ORDER BY evidence_count ASC LIMIT ?",
            (max_pairs,),
        ).fetchall()

    if not rows:
        console.print("[yellow]No interactions found to enrich.[/]")
        return

    console.print(
        Panel(
            f"[bold blue]MEDGRAPH[/] PubMed Literature Enrichment\n"
            f"Enriching [cyan]{len(rows)}[/] interaction pairs\n"
            f"Max articles per pair: [cyan]{max_results}[/]\n"
            f"\n[dim]Rate-limited to ~3 req/sec. This may take a few minutes.[/]",
            expand=False,
        )
    )

    total_articles = 0
    for i, row in enumerate(rows, 1):
        _, drug_a_id, drug_b_id = row[0], row[1], row[2]
        console.print(f"  [{i}/{len(rows)}] Enriching {drug_a_id} + {drug_b_id}…", end=" ")
        articles = enrich_interaction(store, drug_a_id, drug_b_id, agent=agent)
        console.print(f"[green]{len(articles)} articles[/]")
        total_articles += len(articles)

    console.print(
        f"\n[bold green]PubMed enrichment complete![/]\n"
        f"  Total articles found: [cyan]{total_articles}[/]"
    )


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
