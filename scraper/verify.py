"""Completeness verification for scraped law data."""

import logging
from typing import Optional

from scraper.config import get_supabase

logger = logging.getLogger(__name__)


def verify_law(law_id: str, effective_from: Optional[str] = None) -> dict:
    """Run completeness checks on stored law data.

    Args:
        law_id: Law identifier (e.g., "222/2004").
        effective_from: Optional date filter (YYYY-MM-DD format).

    Returns:
        Dict with verification results.
    """
    sb = get_supabase()
    report: dict = {"law_id": law_id, "status": "ok", "issues": []}

    # --- Check document exists ---
    query = sb.table("law_documents").select("*").eq("law_id", law_id)
    if effective_from:
        query = query.eq("effective_from", effective_from)
    docs = query.execute()

    if not docs.data:
        report["status"] = "error"
        report["issues"].append(f"No document found for {law_id}")
        return report

    doc = docs.data[0]
    doc_id = doc["id"]
    report["document_id"] = doc_id
    report["effective_from"] = doc["effective_from"]
    report["fetch_status"] = doc["fetch_status"]
    report["html_size_bytes"] = doc["html_size_bytes"]
    report["stored_section_count"] = doc["section_count"]

    # --- Count sections by type (paginate past Supabase 1000-row default) ---
    all_sections: list[dict] = []
    page_size = 1000
    offset = 0
    while True:
        page = (
            sb.table("law_sections")
            .select("section_type, text_content, parent_id, element_id")
            .eq("document_id", doc_id)
            .range(offset, offset + page_size - 1)
            .execute()
        )
        all_sections.extend(page.data)
        if len(page.data) < page_size:
            break
        offset += page_size

    sections_data = all_sections

    type_counts: dict[str, int] = {}
    empty_text = 0
    total_text_chars = 0

    for s in sections_data:
        stype = s["section_type"]
        type_counts[stype] = type_counts.get(stype, 0) + 1

        text = s.get("text_content", "")
        if not text or not text.strip():
            empty_text += 1
        else:
            total_text_chars += len(text)

    report["section_counts"] = type_counts
    report["total_sections"] = len(sections_data)
    report["total_text_chars"] = total_text_chars
    report["empty_text_sections"] = empty_text

    # --- Check expected counts ---
    paragraf_count = type_counts.get("paragraf", 0)
    expected_counts = {
        "222/2004": {"paragraf_min": 80, "paragraf_max": 200},
        "431/2002": {"paragraf_min": 30, "paragraf_max": 120},
    }

    if law_id in expected_counts:
        exp = expected_counts[law_id]
        if paragraf_count < exp["paragraf_min"]:
            report["issues"].append(
                f"Too few paragraphs: {paragraf_count} (expected >= {exp['paragraf_min']})"
            )
        if paragraf_count > exp["paragraf_max"]:
            report["issues"].append(
                f"Too many paragraphs: {paragraf_count} (expected <= {exp['paragraf_max']})"
            )

    # --- Check text/HTML ratio ---
    html_size = doc.get("html_size_bytes", 0)
    if html_size > 0:
        ratio = total_text_chars / html_size
        report["text_to_html_ratio"] = round(ratio, 3)
        if ratio < 0.05:
            report["issues"].append(
                f"Very low text/HTML ratio: {ratio:.3f} (expected > 0.05)"
            )

    # --- Check for empty text ---
    if empty_text > len(sections_data) * 0.3:
        report["issues"].append(
            f"High proportion of empty text: {empty_text}/{len(sections_data)}"
        )

    if report["issues"]:
        report["status"] = "warning"

    return report


def print_report(report: dict) -> None:
    """Print a human-readable verification report."""
    print(f"\n{'='*60}")
    print(f"Verification Report: {report['law_id']}")
    print(f"{'='*60}")
    print(f"Status: {report['status'].upper()}")

    if "effective_from" in report:
        print(f"Effective from: {report['effective_from']}")
    if "html_size_bytes" in report:
        print(f"HTML size: {report['html_size_bytes']:,} bytes")
    if "total_sections" in report:
        print(f"Total sections: {report['total_sections']}")
    if "total_text_chars" in report:
        print(f"Total text characters: {report['total_text_chars']:,}")
    if "text_to_html_ratio" in report:
        print(f"Text/HTML ratio: {report['text_to_html_ratio']}")

    if "section_counts" in report:
        print(f"\nSection counts:")
        for stype, count in sorted(report["section_counts"].items()):
            print(f"  {stype}: {count}")

    if "empty_text_sections" in report:
        print(f"\nEmpty text sections: {report['empty_text_sections']}")

    if report.get("issues"):
        print(f"\nIssues ({len(report['issues'])}):")
        for issue in report["issues"]:
            print(f"  ⚠ {issue}")
    else:
        print(f"\nNo issues found.")

    print(f"{'='*60}\n")
