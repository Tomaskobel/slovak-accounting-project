"""Supabase storage operations for law documents and sections."""

import logging
from datetime import datetime, date
from typing import Optional

from scraper.config import get_supabase
from scraper.parser import SectionRecord, build_full_text

logger = logging.getLogger(__name__)

BATCH_SIZE = 100


def store_document(
    law_id: str,
    law_title: str,
    collection: str,
    effective_from: date,
    effective_to: Optional[date],
    source_url: str,
    raw_html: str,
) -> str:
    """Store or update a law document record.

    Returns:
        The UUID of the stored document.
    """
    sb = get_supabase()
    now = datetime.utcnow().isoformat()

    data = {
        "law_id": law_id,
        "law_title": law_title,
        "collection": collection,
        "effective_from": effective_from.isoformat(),
        "effective_to": effective_to.isoformat() if effective_to else None,
        "source_url": source_url,
        "raw_html": raw_html,
        "html_size_bytes": len(raw_html.encode("utf-8")),
        "fetch_status": "fetched",
        "fetched_at": now,
    }

    # Upsert on (law_id, effective_from)
    result = (
        sb.table("law_documents")
        .upsert(data, on_conflict="law_id,effective_from")
        .execute()
    )

    if not result.data:
        raise RuntimeError(
            f"Upsert for {law_id} (effective {effective_from}) returned no data. "
            "Check Supabase RLS policies and table schema."
        )
    doc_id = result.data[0]["id"]
    logger.info("Stored document %s (effective %s) → %s", law_id, effective_from, doc_id)
    return doc_id


def clear_sections(document_id: str) -> int:
    """Delete all sections for a document (before re-parsing).

    Returns:
        Number of deleted rows.
    """
    sb = get_supabase()
    result = (
        sb.table("law_sections")
        .delete()
        .eq("document_id", document_id)
        .execute()
    )
    count = len(result.data) if result.data else 0
    logger.info("Cleared %d sections for document %s", count, document_id)
    return count


def store_sections(
    document_id: str,
    law_id: str,
    effective_from: date,
    records: list[SectionRecord],
) -> int:
    """Store parsed sections into Supabase.

    Uses a two-pass approach:
    1. Insert all records without parent_id (to get UUIDs)
    2. Update parent_id references

    Returns:
        Number of stored sections.
    """
    sb = get_supabase()

    # Build full_text for each record
    full_texts = build_full_text(records)

    # --- Pass 1: Insert all records without parent_id ---
    element_id_to_uuid: dict[str, str] = {}
    total_inserted = 0

    for i in range(0, len(records), BATCH_SIZE):
        batch = records[i:i + BATCH_SIZE]
        rows = []
        for r in batch:
            row = {
                "document_id": document_id,
                "law_id": law_id,
                "effective_from": effective_from.isoformat(),
                "section_type": r.section_type,
                "section_number": r.section_number,
                "element_id": r.element_id,
                "title": r.title,
                "text_content": r.text_content,
                "full_text": full_texts.get(r.element_id, r.text_content),
                "raw_html": r.raw_html,
                "depth": r.depth,
                "sort_order": r.sort_order,
                "has_pdf_attachment": r.has_pdf_attachment,
                "pdf_url": r.pdf_url,
                # parent_id set in pass 2
            }
            rows.append(row)

        result = sb.table("law_sections").insert(rows).execute()

        for row_data in result.data:
            eid = row_data.get("element_id")
            if eid:
                element_id_to_uuid[eid] = row_data["id"]

        total_inserted += len(result.data)
        logger.info("Inserted batch %d-%d (%d rows)", i, i + len(batch), len(result.data))

    # --- Pass 2: Update parent_id references ---
    updates = 0
    for r in records:
        if r.parent_element_id and r.parent_element_id in element_id_to_uuid:
            child_uuid = element_id_to_uuid.get(r.element_id)
            parent_uuid = element_id_to_uuid[r.parent_element_id]
            if child_uuid:
                sb.table("law_sections").update(
                    {"parent_id": parent_uuid}
                ).eq("id", child_uuid).execute()
                updates += 1

    logger.info(
        "Stored %d sections for %s (effective %s), %d parent refs updated",
        total_inserted, law_id, effective_from, updates,
    )

    # Update document with section count and parsed timestamp
    sb.table("law_documents").update({
        "section_count": total_inserted,
        "fetch_status": "parsed",
        "parsed_at": datetime.utcnow().isoformat(),
    }).eq("id", document_id).execute()

    return total_inserted
