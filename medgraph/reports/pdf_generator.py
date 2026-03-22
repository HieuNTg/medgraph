"""PDF report generator for MEDGRAPH drug interaction analysis."""

from __future__ import annotations

import base64
import io
from datetime import datetime, timezone
from typing import Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


# Severity color mapping
SEVERITY_COLORS = {
    "critical": colors.HexColor("#DC2626"),
    "major": colors.HexColor("#EA580C"),
    "moderate": colors.HexColor("#CA8A04"),
    "minor": colors.HexColor("#16A34A"),
}

SEVERITY_BG = {
    "critical": colors.HexColor("#FEE2E2"),
    "major": colors.HexColor("#FFEDD5"),
    "moderate": colors.HexColor("#FEF9C3"),
    "minor": colors.HexColor("#DCFCE7"),
}


def generate_report_pdf(
    check_result: dict,
    graph_png_b64: Optional[str] = None,
) -> bytes:
    """
    Generate a PDF report from a drug interaction check result.

    Args:
        check_result: Dict matching CheckResponse schema
        graph_png_b64: Optional base64-encoded PNG of the interaction graph

    Returns:
        PDF file contents as bytes
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontSize=18,
        spaceAfter=6,
        textColor=colors.HexColor("#1E293B"),
    )
    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=12,
    )
    section_style = ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading2"],
        fontSize=13,
        spaceBefore=16,
        spaceAfter=8,
        textColor=colors.HexColor("#1E293B"),
    )
    body_style = ParagraphStyle(
        "BodyText",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
    )
    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["Normal"],
        fontSize=7,
        textColor=colors.HexColor("#94A3B8"),
        spaceBefore=20,
        leading=10,
    )

    story = []

    timestamp = check_result.get("timestamp", datetime.now(timezone.utc).isoformat())
    overall_risk = check_result.get("overall_risk", "minor")
    overall_score = check_result.get("overall_score", 0.0)
    drugs = check_result.get("drugs", [])
    interactions = check_result.get("interactions", [])
    disclaimer = check_result.get("disclaimer", "")

    # --- HEADER ---
    story.append(Paragraph("MEDGRAPH Drug Interaction Report", title_style))
    story.append(
        Paragraph(
            f"Generated: {timestamp[:19].replace('T', ' ')} UTC &nbsp;|&nbsp; "
            f"Overall Risk: <b>{overall_risk.upper()}</b> &nbsp;|&nbsp; "
            f"Score: {overall_score:.1f}/100",
            subtitle_style,
        )
    )
    story.append(Spacer(1, 4 * mm))

    # --- RISK SUMMARY BAR ---
    risk_color = SEVERITY_COLORS.get(overall_risk, colors.grey)
    risk_bg = SEVERITY_BG.get(overall_risk, colors.lightgrey)
    risk_data = [
        [
            Paragraph(
                f"<b>Overall Risk Level: {overall_risk.upper()}</b>",
                ParagraphStyle("risk", parent=body_style, textColor=risk_color, fontSize=11),
            ),
            Paragraph(
                f"<b>{len(interactions)}</b> interaction(s) found across <b>{len(drugs)}</b> medication(s)",
                ParagraphStyle("risk2", parent=body_style, fontSize=9),
            ),
        ]
    ]
    risk_table = Table(risk_data, colWidths=[160, 300])
    risk_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), risk_bg),
                ("BOX", (0, 0), (-1, -1), 1, risk_color),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(risk_table)
    story.append(Spacer(1, 6 * mm))

    # --- MEDICATIONS TABLE ---
    story.append(Paragraph("Medications Analyzed", section_style))

    med_header = ["Drug Name", "Class", "Brand Names", "CYP450 Enzymes"]
    med_data = [med_header]
    for drug in drugs:
        enzymes = ", ".join(
            f"{r.get('enzyme_name', '')} ({r.get('relation_type', '')})"
            for r in drug.get("enzyme_relations", [])[:3]
        )
        if len(drug.get("enzyme_relations", [])) > 3:
            enzymes += f" +{len(drug['enzyme_relations']) - 3} more"

        med_data.append(
            [
                Paragraph(f"<b>{drug.get('name', '')}</b>", body_style),
                drug.get("drug_class", "—") or "—",
                ", ".join(drug.get("brand_names", [])[:3]) or "—",
                enzymes or "—",
            ]
        )

    col_widths = [100, 100, 120, 160]
    med_table = Table(med_data, colWidths=col_widths, repeatRows=1)
    med_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E293B")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 8),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("ALIGN", (0, 0), (-1, 0), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(med_table)

    # --- INTERACTIONS TABLE ---
    if interactions:
        story.append(Paragraph("Drug-Drug Interactions", section_style))

        int_header = ["Drug A", "Drug B", "Severity", "Score", "Mechanism"]
        int_data = [int_header]

        # Sort by severity
        severity_order = {"critical": 0, "major": 1, "moderate": 2, "minor": 3}
        sorted_interactions = sorted(
            interactions,
            key=lambda x: severity_order.get(x.get("severity", "minor"), 99),
        )

        for ix in sorted_interactions:
            sev = ix.get("severity", "minor")
            sev_color = SEVERITY_COLORS.get(sev, colors.grey)

            int_data.append(
                [
                    ix.get("drug_a", {}).get("name", ""),
                    ix.get("drug_b", {}).get("name", ""),
                    Paragraph(
                        f"<b>{sev.upper()}</b>",
                        ParagraphStyle("sev", parent=body_style, textColor=sev_color, fontSize=8),
                    ),
                    f"{ix.get('risk_score', 0):.0f}",
                    Paragraph(
                        ix.get("mechanism", ix.get("description", "")) or "—",
                        ParagraphStyle("mech", parent=body_style, fontSize=7, leading=9),
                    ),
                ]
            )

        int_col_widths = [80, 80, 60, 40, 220]
        int_table = Table(int_data, colWidths=int_col_widths, repeatRows=1)

        # Build table style
        table_style_commands = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E293B")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 8),
            ("FONTSIZE", (0, 1), (-1, -1), 8),
            ("ALIGN", (3, 0), (3, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]

        # Color-code rows by severity
        for row_idx, ix in enumerate(sorted_interactions, start=1):
            sev = ix.get("severity", "minor")
            bg = SEVERITY_BG.get(sev, colors.white)
            table_style_commands.append(("BACKGROUND", (0, row_idx), (-1, row_idx), bg))

        int_table.setStyle(TableStyle(table_style_commands))
        story.append(int_table)

    # --- INTERACTION DETAILS ---
    if interactions:
        story.append(Spacer(1, 4 * mm))
        story.append(Paragraph("Interaction Details", section_style))

        for ix in sorted_interactions:
            sev = ix.get("severity", "minor")
            sev_color = SEVERITY_COLORS.get(sev, colors.grey)
            drug_a = ix.get("drug_a", {}).get("name", "")
            drug_b = ix.get("drug_b", {}).get("name", "")

            # Interaction header
            story.append(
                Paragraph(
                    f"<b>{drug_a} + {drug_b}</b> — "
                    f"<font color='{sev_color}'>{sev.upper()}</font> "
                    f"(score: {ix.get('risk_score', 0):.0f})",
                    ParagraphStyle(
                        "ixhead", parent=body_style, fontSize=10, spaceBefore=8, spaceAfter=4
                    ),
                )
            )

            desc = ix.get("description", "")
            if desc:
                story.append(Paragraph(desc, body_style))

            mech = ix.get("mechanism", "")
            if mech:
                story.append(
                    Paragraph(
                        f"<i>Mechanism: {mech}</i>",
                        ParagraphStyle(
                            "mech_detail",
                            parent=body_style,
                            fontSize=8,
                            textColor=colors.HexColor("#475569"),
                        ),
                    )
                )

            # Cascade paths
            cascades = ix.get("cascade_paths", [])
            if cascades:
                for cp in cascades[:2]:  # limit to 2 cascade paths
                    path_desc = cp.get("description", "")
                    if path_desc:
                        story.append(
                            Paragraph(
                                f"Cascade: {path_desc}",
                                ParagraphStyle(
                                    "cascade",
                                    parent=body_style,
                                    fontSize=8,
                                    leftIndent=12,
                                    textColor=colors.HexColor("#7C3AED"),
                                ),
                            )
                        )

            story.append(Spacer(1, 2 * mm))

    # --- GRAPH IMAGE ---
    if graph_png_b64:
        story.append(PageBreak())
        story.append(Paragraph("Interaction Network Visualization", section_style))
        try:
            img_data = base64.b64decode(graph_png_b64)
            img = Image(io.BytesIO(img_data))
            # Scale to fit page width (A4 - margins = ~180mm)
            max_width = 170 * mm
            max_height = 120 * mm
            img_width = img.drawWidth
            img_height = img.drawHeight
            if img_width > 0 and img_height > 0:
                ratio = min(max_width / img_width, max_height / img_height)
                img.drawWidth = img_width * ratio
                img.drawHeight = img_height * ratio
            story.append(img)
            story.append(
                Paragraph(
                    "Blue circles = drugs, amber rectangles = enzymes. "
                    "Edge colors indicate severity (red = critical, orange = major, yellow = moderate).",
                    ParagraphStyle(
                        "caption",
                        parent=body_style,
                        fontSize=7,
                        textColor=colors.HexColor("#94A3B8"),
                        spaceBefore=4,
                    ),
                )
            )
        except Exception:
            story.append(Paragraph("[Graph image could not be rendered]", body_style))

    # --- DISCLAIMER ---
    story.append(Spacer(1, 8 * mm))
    story.append(
        Paragraph(
            f"<b>DISCLAIMER:</b> {disclaimer}",
            disclaimer_style,
        )
    )
    story.append(
        Paragraph(
            "Data sources: DrugBank, OpenFDA FAERS, RxNorm, FDA Drug Labels. "
            "This report was generated by MEDGRAPH — an open-source drug interaction cascade analyzer.",
            disclaimer_style,
        )
    )

    doc.build(story)
    return buffer.getvalue()
