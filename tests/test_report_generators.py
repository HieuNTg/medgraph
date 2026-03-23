"""
Tests for JSON and CSV report generators.

Covers: structure, field presence, edge cases (empty data, special chars).
"""

from __future__ import annotations

import csv
import io
import json

import pytest

from medgraph.reports.json_generator import generate_report_json
from medgraph.reports.csv_generator import generate_report_csv


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

SAMPLE_CHECK_RESULT = {
    "drugs": [
        {
            "id": "DB00001",
            "name": "Warfarin",
            "brand_names": ["Coumadin"],
            "drug_class": "Anticoagulant",
            "enzyme_relations": [
                {"enzyme_name": "CYP2C9", "relation_type": "metabolized_by", "strength": "strong"},
            ],
        },
        {
            "id": "DB00002",
            "name": "Fluoxetine",
            "brand_names": ["Prozac"],
            "drug_class": "SSRI",
            "enzyme_relations": [
                {"enzyme_name": "CYP2D6", "relation_type": "inhibits", "strength": "strong"},
            ],
        },
    ],
    "interactions": [
        {
            "drug_a": {"id": "DB00001", "name": "Warfarin"},
            "drug_b": {"id": "DB00002", "name": "Fluoxetine"},
            "severity": "major",
            "risk_score": 72.5,
            "description": "Increased bleeding risk",
            "mechanism": "CYP2C9 inhibition",
            "cascade_paths": [
                {
                    "description": "Fluoxetine inhibits CYP2C9, reducing Warfarin metabolism",
                    "net_severity": "major",
                    "steps": [
                        {
                            "source": "Fluoxetine",
                            "target": "CYP2C9",
                            "relation": "inhibits",
                            "effect": "reduced enzyme activity",
                        },
                    ],
                },
            ],
            "evidence": [
                {
                    "source": "faers",
                    "description": "FAERS: Hemorrhage",
                    "case_count": 150,
                    "url": None,
                },
            ],
        },
    ],
    "overall_risk": "major",
    "overall_score": 72.5,
    "drug_count": 2,
    "interaction_count": 1,
    "timestamp": "2026-03-23T12:00:00+00:00",
    "disclaimer": "For informational purposes only.",
}


@pytest.fixture
def check_result() -> dict:
    return SAMPLE_CHECK_RESULT.copy()


EMPTY_CHECK_RESULT = {
    "drugs": [],
    "interactions": [],
    "overall_risk": "minor",
    "overall_score": 0.0,
    "drug_count": 0,
    "interaction_count": 0,
    "timestamp": "2026-03-23T12:00:00+00:00",
    "disclaimer": "Disclaimer text.",
}


# ---------------------------------------------------------------------------
# JSON Generator Tests
# ---------------------------------------------------------------------------


class TestJSONGenerator:
    def test_generates_valid_json(self, check_result: dict) -> None:
        result = generate_report_json(check_result)
        parsed = json.loads(result)
        assert isinstance(parsed, dict)

    def test_report_format_version(self, check_result: dict) -> None:
        parsed = json.loads(generate_report_json(check_result))
        assert parsed["report_format"] == "medgraph-json-v1"

    def test_summary_fields(self, check_result: dict) -> None:
        parsed = json.loads(generate_report_json(check_result))
        summary = parsed["summary"]
        assert summary["drug_count"] == 2
        assert summary["interaction_count"] == 1
        assert summary["overall_risk"] == "major"
        assert summary["overall_score"] == 72.5

    def test_drugs_extracted(self, check_result: dict) -> None:
        parsed = json.loads(generate_report_json(check_result))
        assert len(parsed["drugs"]) == 2
        drug = parsed["drugs"][0]
        assert drug["name"] == "Warfarin"
        assert drug["brand_names"] == ["Coumadin"]
        assert len(drug["enzyme_relations"]) == 1

    def test_interactions_extracted(self, check_result: dict) -> None:
        parsed = json.loads(generate_report_json(check_result))
        assert len(parsed["interactions"]) == 1
        ix = parsed["interactions"][0]
        assert ix["drug_a"] == "Warfarin"
        assert ix["drug_b"] == "Fluoxetine"
        assert ix["severity"] == "major"
        assert ix["risk_score"] == 72.5

    def test_cascade_paths_included(self, check_result: dict) -> None:
        parsed = json.loads(generate_report_json(check_result))
        ix = parsed["interactions"][0]
        assert len(ix["cascade_paths"]) == 1
        cp = ix["cascade_paths"][0]
        assert len(cp["steps"]) == 1

    def test_evidence_included(self, check_result: dict) -> None:
        parsed = json.loads(generate_report_json(check_result))
        ix = parsed["interactions"][0]
        assert len(ix["evidence"]) == 1
        assert ix["evidence"][0]["case_count"] == 150

    def test_pretty_false_no_indent(self, check_result: dict) -> None:
        result = generate_report_json(check_result, pretty=False)
        assert "\n" not in result.strip()

    def test_pretty_true_has_indent(self, check_result: dict) -> None:
        result = generate_report_json(check_result, pretty=True)
        assert "\n" in result

    def test_empty_result(self) -> None:
        parsed = json.loads(generate_report_json(EMPTY_CHECK_RESULT))
        assert parsed["summary"]["drug_count"] == 0
        assert parsed["drugs"] == []
        assert parsed["interactions"] == []

    def test_generated_at_present(self, check_result: dict) -> None:
        parsed = json.loads(generate_report_json(check_result))
        assert "generated_at" in parsed

    def test_disclaimer_preserved(self, check_result: dict) -> None:
        parsed = json.loads(generate_report_json(check_result))
        assert parsed["disclaimer"] == "For informational purposes only."


# ---------------------------------------------------------------------------
# CSV Generator Tests
# ---------------------------------------------------------------------------


class TestCSVGenerator:
    def _parse_csv(self, csv_str: str) -> list[list[str]]:
        reader = csv.reader(io.StringIO(csv_str))
        return list(reader)

    def test_generates_valid_csv(self, check_result: dict) -> None:
        result = generate_report_csv(check_result)
        rows = self._parse_csv(result)
        assert len(rows) >= 2  # header + at least 1 data row

    def test_header_columns(self, check_result: dict) -> None:
        rows = self._parse_csv(generate_report_csv(check_result))
        header = rows[0]
        assert "Drug A" in header
        assert "Drug B" in header
        assert "Severity" in header
        assert "Risk Score" in header
        assert "Overall Risk" in header

    def test_interaction_row(self, check_result: dict) -> None:
        rows = self._parse_csv(generate_report_csv(check_result))
        data = rows[1]
        assert data[0] == "Warfarin"  # Drug A
        assert data[1] == "Fluoxetine"  # Drug B
        assert data[2] == "major"  # Severity
        assert data[3] == "72.5"  # Risk Score

    def test_cascade_count_column(self, check_result: dict) -> None:
        rows = self._parse_csv(generate_report_csv(check_result))
        header = rows[0]
        cascade_idx = header.index("Cascade Count")
        assert rows[1][cascade_idx] == "1"

    def test_evidence_count_summed(self, check_result: dict) -> None:
        rows = self._parse_csv(generate_report_csv(check_result))
        header = rows[0]
        ev_idx = header.index("FAERS Cases")
        assert rows[1][ev_idx] == "150"

    def test_empty_result_only_header(self) -> None:
        rows = self._parse_csv(generate_report_csv(EMPTY_CHECK_RESULT))
        assert len(rows) == 1  # header only

    def test_special_chars_in_description(self) -> None:
        """Commas and quotes in description must not break CSV."""
        result = {
            **EMPTY_CHECK_RESULT,
            "interactions": [
                {
                    "drug_a": {"name": "Drug, A"},
                    "drug_b": {"name": 'Drug "B"'},
                    "severity": "minor",
                    "risk_score": 10.0,
                    "description": 'Contains "quotes" and, commas',
                    "mechanism": None,
                    "cascade_paths": [],
                    "evidence": [],
                },
            ],
        }
        rows = self._parse_csv(generate_report_csv(result))
        assert len(rows) == 2
        assert rows[1][0] == "Drug, A"
        assert rows[1][1] == 'Drug "B"'

    def test_overall_risk_in_every_row(self, check_result: dict) -> None:
        rows = self._parse_csv(generate_report_csv(check_result))
        header = rows[0]
        risk_idx = header.index("Overall Risk")
        for row in rows[1:]:
            assert row[risk_idx] == "major"
