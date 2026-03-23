"""CSV report generator for MEDGRAPH drug interaction analysis."""

from __future__ import annotations

import csv
import io


def generate_report_csv(check_result: dict) -> str:
    """
    Generate a CSV report of drug interactions from check results.

    Each row represents one interaction. Cascade and evidence details
    are flattened into summary columns.

    Args:
        check_result: Dict matching CheckResponse schema.

    Returns:
        CSV string with headers.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(
        [
            "Drug A",
            "Drug B",
            "Severity",
            "Risk Score",
            "Description",
            "Mechanism",
            "Cascade Count",
            "Cascade Summary",
            "FAERS Cases",
            "Overall Risk",
            "Overall Score",
        ]
    )

    overall_risk = check_result.get("overall_risk", "")
    overall_score = check_result.get("overall_score", 0.0)

    for ix in check_result.get("interactions", []):
        cascades = ix.get("cascade_paths", [])
        cascade_summary = "; ".join(
            cp.get("description", "") for cp in cascades if cp.get("description")
        )

        evidence = ix.get("evidence", [])
        total_cases = sum(e.get("case_count", 0) or 0 for e in evidence)

        writer.writerow(
            [
                ix.get("drug_a", {}).get("name", ""),
                ix.get("drug_b", {}).get("name", ""),
                ix.get("severity", ""),
                f"{ix.get('risk_score', 0.0):.1f}",
                ix.get("description", ""),
                ix.get("mechanism", "") or "",
                len(cascades),
                cascade_summary,
                total_cases,
                overall_risk,
                f"{overall_score:.1f}",
            ]
        )

    return output.getvalue()
