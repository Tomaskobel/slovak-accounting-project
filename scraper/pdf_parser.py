"""PDF parser for Slovak regulatory documents (Postupy účtovania, KV DPH guidelines).

Uses pdfplumber to extract text from PDF files and parse into hierarchical sections
matching the same SectionRecord structure as the HTML parser.
"""

import logging
import re
from pathlib import Path
from typing import Optional

import pdfplumber

from scraper.parser import SectionRecord

logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """Extract full text from a PDF file.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Concatenated text from all pages.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    pages_text: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        logger.info("Opened PDF: %s (%d pages)", pdf_path.name, len(pdf.pages))
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                pages_text.append(text)
            else:
                logger.warning("Page %d has no extractable text", i + 1)

    full_text = "\n\n".join(pages_text)
    logger.info(
        "Extracted %d characters from %d pages",
        len(full_text),
        len(pages_text),
    )
    return full_text


# ---------------------------------------------------------------------------
# Section patterns for Postupy účtovania (Opatrenie MF SR 23054/2002-92)
# ---------------------------------------------------------------------------

# §1, §2, ..., §30f, §31, ..., §88
_PARAGRAF_RE = re.compile(
    r"^§\s*(\d+[a-z]?)\s*$",
    re.MULTILINE,
)

# (1), (2), ..., (15) — subsections (odsek)
_ODSEK_RE = re.compile(
    r"^\((\d+)\)\s",
    re.MULTILINE,
)

# a), b), ..., z) — letters (pismeno)
_PISMENO_RE = re.compile(
    r"^([a-z])\)\s",
    re.MULTILINE,
)


def parse_postupy_uctovania(text: str) -> list[SectionRecord]:
    """Parse Postupy účtovania PDF text into hierarchical sections.

    The document structure is:
    - § (paragraf) — top-level sections
    - (1), (2) — subsections (odsek)
    - a), b) — letters (písmeno)

    Args:
        text: Full text extracted from the PDF.

    Returns:
        List of SectionRecord objects with parent-child relationships.
    """
    records: list[SectionRecord] = []
    sort_order = 0
    seen_eids: dict[str, int] = {}  # Track element_ids to deduplicate

    def _unique_eid(eid: str) -> str:
        """Ensure element_id is unique by appending counter if needed."""
        if eid not in seen_eids:
            seen_eids[eid] = 1
            return eid
        seen_eids[eid] += 1
        return f"{eid}--{seen_eids[eid]}"

    # Split text into paragraf blocks
    paragraf_splits = list(_PARAGRAF_RE.finditer(text))

    if not paragraf_splits:
        logger.warning("No § sections found in text. Returning single record.")
        records.append(SectionRecord(
            section_type="dokument",
            section_number="1",
            element_id="dokument-1",
            title="Postupy účtovania",
            text_content=text,
            raw_html="",
            depth=0,
            sort_order=0,
            parent_element_id=None,
        ))
        return records

    for idx, match in enumerate(paragraf_splits):
        paragraf_num = match.group(1)
        paragraf_start = match.end()
        paragraf_end = (
            paragraf_splits[idx + 1].start()
            if idx + 1 < len(paragraf_splits)
            else len(text)
        )

        paragraf_text = text[paragraf_start:paragraf_end].strip()
        paragraf_eid = _unique_eid(f"paragraf-{paragraf_num}")

        # Extract title (first line after §)
        lines = paragraf_text.split("\n", 1)
        title = lines[0].strip() if lines else None
        body = lines[1].strip() if len(lines) > 1 else ""

        # Check if title looks like a real title (not a subsection start)
        if title and (title.startswith("(1)") or title.startswith("a)")):
            body = paragraf_text
            title = None

        sort_order += 1
        paragraf_record = SectionRecord(
            section_type="paragraf",
            section_number=paragraf_num,
            element_id=paragraf_eid,
            title=title,
            text_content="",  # Text goes into children
            raw_html="",
            depth=0,
            sort_order=sort_order,
            parent_element_id=None,
        )
        records.append(paragraf_record)

        # Parse subsections (odsek) within this paragraf
        odsek_splits = list(_ODSEK_RE.finditer(body))

        if not odsek_splits:
            # No subsections — text belongs to paragraf directly
            paragraf_record.text_content = body
        else:
            # Text before first odsek belongs to paragraf
            pre_odsek = body[:odsek_splits[0].start()].strip()
            if pre_odsek:
                paragraf_record.text_content = pre_odsek

            for ods_idx, ods_match in enumerate(odsek_splits):
                odsek_num = ods_match.group(1)
                odsek_start = ods_match.end()
                odsek_end = (
                    odsek_splits[ods_idx + 1].start()
                    if ods_idx + 1 < len(odsek_splits)
                    else len(body)
                )

                odsek_text = body[odsek_start:odsek_end].strip()
                odsek_eid = _unique_eid(f"{paragraf_eid}.odsek-{odsek_num}")

                sort_order += 1
                odsek_record = SectionRecord(
                    section_type="odsek",
                    section_number=odsek_num,
                    element_id=odsek_eid,
                    title=None,
                    text_content="",
                    raw_html="",
                    depth=1,
                    sort_order=sort_order,
                    parent_element_id=paragraf_eid,
                )
                records.append(odsek_record)

                # Parse letters (pismeno) within this odsek
                pismeno_splits = list(_PISMENO_RE.finditer(odsek_text))

                if not pismeno_splits:
                    odsek_record.text_content = odsek_text
                else:
                    pre_pismeno = odsek_text[:pismeno_splits[0].start()].strip()
                    if pre_pismeno:
                        odsek_record.text_content = pre_pismeno

                    for pis_idx, pis_match in enumerate(pismeno_splits):
                        pis_letter = pis_match.group(1)
                        pis_start = pis_match.end()
                        pis_end = (
                            pismeno_splits[pis_idx + 1].start()
                            if pis_idx + 1 < len(pismeno_splits)
                            else len(odsek_text)
                        )

                        pis_text = odsek_text[pis_start:pis_end].strip()
                        pis_eid = _unique_eid(f"{odsek_eid}.pismeno-{pis_letter}")

                        sort_order += 1
                        records.append(SectionRecord(
                            section_type="pismeno",
                            section_number=pis_letter,
                            element_id=pis_eid,
                            title=None,
                            text_content=pis_text,
                            raw_html="",
                            depth=2,
                            sort_order=sort_order,
                            parent_element_id=odsek_eid,
                        ))

    logger.info(
        "Parsed %d sections from Postupy účtovania (%d §)",
        len(records),
        len(paragraf_splits),
    )
    return records


def parse_kv_dph_guidelines(text: str) -> list[SectionRecord]:
    """Parse KV DPH methodical guidelines PDF text into sections.

    The document structure is section-based (A.1, A.2, B.1, B.2, B.3, C.1, C.2, D.1, D.2).

    Args:
        text: Full text extracted from the PDF.

    Returns:
        List of SectionRecord objects.
    """
    records: list[SectionRecord] = []
    sort_order = 0

    # KV DPH section pattern: "- časť A.1. - description" or "- časť. B.2. – description"
    section_re = re.compile(
        r"-\s*časť\.?\s+([A-D]\.\d)\.?\s*[–—-]+\s*(.+?)$",
        re.MULTILINE | re.IGNORECASE,
    )

    section_splits = list(section_re.finditer(text))

    if not section_splits:
        # Try simpler format: "A.1 — description"
        section_re = re.compile(
            r"^([A-D]\.\d)\s*[–—-]\s*(.+?)$",
            re.MULTILINE,
        )
        section_splits = list(section_re.finditer(text))

    if not section_splits:
        logger.warning("No KV DPH sections found. Returning single record.")
        records.append(SectionRecord(
            section_type="dokument",
            section_number="1",
            element_id="kv-dph-1",
            title="Metodický pokyn ku KV DPH",
            text_content=text,
            raw_html="",
            depth=0,
            sort_order=0,
            parent_element_id=None,
        ))
        return records

    # Add text before first section as intro
    pre_text = text[:section_splits[0].start()].strip()
    if pre_text:
        sort_order += 1
        records.append(SectionRecord(
            section_type="uvod",
            section_number="0",
            element_id="kv-dph-uvod",
            title="Úvod",
            text_content=pre_text,
            raw_html="",
            depth=0,
            sort_order=sort_order,
            parent_element_id=None,
        ))

    for idx, match in enumerate(section_splits):
        section_code = match.group(1)
        section_title = match.group(2).strip()
        section_start = match.end()
        section_end = (
            section_splits[idx + 1].start()
            if idx + 1 < len(section_splits)
            else len(text)
        )

        section_text = text[section_start:section_end].strip()
        section_eid = f"kv-dph-{section_code.replace('.', '-')}"

        sort_order += 1
        records.append(SectionRecord(
            section_type="sekcia_kv",
            section_number=section_code,
            element_id=section_eid,
            title=section_title,
            text_content=section_text,
            raw_html="",
            depth=0,
            sort_order=sort_order,
            parent_element_id=None,
        ))

    logger.info(
        "Parsed %d sections from KV DPH guidelines",
        len(records),
    )
    return records


def fetch_pdf(url: str, save_path: str | Path) -> Path:
    """Download a PDF from a URL.

    Args:
        url: URL to download from.
        save_path: Path to save the PDF.

    Returns:
        Path to the saved PDF.
    """
    import requests
    from scraper.config import USER_AGENT, REQUEST_TIMEOUT

    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    save_path.write_bytes(response.content)
    logger.info("Downloaded PDF: %s (%d bytes)", save_path.name, len(response.content))
    return save_path
