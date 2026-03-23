"""JSON report generator for MEDGRAPH drug interaction analysis."""

from __future__ import annotations

import json
from datetime import datetime, timezone


def generate_report_json(
    check_result: dict,
    pretty: bool = True,
) -> str:
    """
    Generate a structured JSON report from check results.

    Args:
        check_result: Dict matching CheckResponse schema.
        pretty: If True, indent output for readability.

    Returns:
        JSON string of the report.
    """
    report = {
        "report_format": "medgraph-json-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "drug_count": check_result.get("drug_count", 0),
            "interaction_count": check_result.get("interaction_count", 0),
            "overall_risk": check_result.get("overall_risk", "minor"),
            "overall_score": check_result.get("overall_score", 0.0),
        },
        "drugs": _extract_drugs(check_result.get("drugs", [])),
        "interactions": _extract_interactions(check_result.get("interactions", [])),
        "disclaimer": check_result.get("disclaimer", ""),
    }
    indent = 2 if pretty else None
    return json.dumps(report, indent=indent, ensure_ascii=False)


def _extract_drugs(drugs: list[dict]) -> list[dict]:
    """Extract drug data into a clean structure."""
    result = []
    for drug in drugs:
        result.append(
            {
                "id": drug.get("id", ""),
                "name": drug.get("name", ""),
                "brand_names": drug.get("brand_names", []),
                "drug_class": drug.get("drug_class"),
                "enzyme_relations": [
                    {
                        "enzyme": rel.get("enzyme_name", ""),
                        "type": rel.get("relation_type", ""),
                        "strength": rel.get("strength", ""),
                    }
                    for rel in drug.get("enzyme_relations", [])
                ],
            }
        )
    return result


def _extract_interactions(interactions: list[dict]) -> list[dict]:
    """Extract interaction data into a clean structure."""
    result = []
    for ix in interactions:
        entry = {
            "drug_a": ix.get("drug_a", {}).get("name", ""),
            "drug_b": ix.get("drug_b", {}).get("name", ""),
            "severity": ix.get("severity", "minor"),
            "risk_score": ix.get("risk_score", 0.0),
            "description": ix.get("description", ""),
            "mechanism": ix.get("mechanism"),
            "cascade_paths": [
                {
                    "description": cp.get("description", ""),
                    "net_severity": cp.get("net_severity", ""),
                    "steps": [
                        {
                            "source": step.get("source", ""),
                            "target": step.get("target", ""),
                            "relation": step.get("relation", ""),
                            "effect": step.get("effect", ""),
                        }
                        for step in cp.get("steps", [])
                    ],
                }
                for cp in ix.get("cascade_paths", [])
            ],
            "evidence": [
                {
                    "source": ev.get("source", ""),
                    "description": ev.get("description", ""),
                    "case_count": ev.get("case_count"),
                    "url": ev.get("url"),
                }
                for ev in ix.get("evidence", [])
            ],
        }
        result.append(entry)
    return result
