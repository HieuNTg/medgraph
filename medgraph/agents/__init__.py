"""
MEDGRAPH AI Agent Layer — internal infrastructure agents.

These agents run as background jobs to enrich the knowledge graph
with real data from external sources. They are NOT user-facing.

Agents:
    FDAEnrichmentAgent  — Fetches FAERS adverse event data from OpenFDA API
    LabelParserAgent    — Extracts interaction warnings from FDA drug labels
    SeverityAgent       — Re-classifies interaction severity using NLP patterns
"""

from medgraph.agents.fda_enrichment_agent import FDAEnrichmentAgent
from medgraph.agents.label_parser_agent import LabelParserAgent
from medgraph.agents.severity_agent import SeverityAgent

__all__ = ["FDAEnrichmentAgent", "LabelParserAgent", "SeverityAgent"]
