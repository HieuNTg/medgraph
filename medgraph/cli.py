"""
MEDGRAPH CLI.

Commands:
    python -m medgraph.cli seed     — Seed database with built-in + optional external data
    python -m medgraph.cli serve    — Start FastAPI server

Usage:
    python -m medgraph.cli seed
    python -m medgraph.cli seed --include-openfda
    python -m medgraph.cli serve
    python -m medgraph.cli serve --host 0.0.0.0 --port 8080
    python -m medgraph.cli analyze Warfarin Aspirin Clopidogrel
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


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
