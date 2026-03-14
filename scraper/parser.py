"""HTML parser for slov-lex.sk legal texts.

Parses the structured HTML into a hierarchical list of SectionRecord objects.
Based on the actual DOM structure of static.slov-lex.sk pages:

    div.paragraf.Skupina#paragraf-{N}
        div.paragrafOznacenie#paragraf-{N}.oznacenie  → "§ N"
        div.paragrafNadpis#paragraf-{N}.nadpis        → section title
        div.odsek.Skupina#paragraf-{N}.odsek-{M}
            div.odsekOznacenie  → "(M)"
            div.text            → actual text
            div.pismeno.Skupina#...pismeno-{x}
                div.pismenoOznacenie → "x)"
                div.text             → actual text
                div.bod.Skupina#...bod-{Y} (if exists inside pismeno)

    div.priloha.Skupina#prilohy.priloha-{slug}
        div.prilohaOznacenie → annex title

    div.poznamka.Skupina#poznamky.poznamka-{ref}
        div.poznamkaOznacenie → footnote reference
        div.text              → footnote text
"""

import logging
from dataclasses import dataclass, field
from typing import Optional

from bs4 import BeautifulSoup, Tag

logger = logging.getLogger(__name__)


@dataclass
class SectionRecord:
    """A parsed section from the law HTML."""
    section_type: str       # 'skupinaParagrafov', 'paragraf', 'odsek', 'pismeno', 'bod', 'priloha', 'poznamka'
    section_number: str     # e.g., "1", "2", "a", "1.", slug for annexes
    element_id: str         # Original HTML id attribute
    title: Optional[str]    # Section title (if exists)
    text_content: str       # Text of THIS section only (not children)
    raw_html: str           # Raw HTML of this section
    depth: int              # 0=top, 1=odsek, 2=pismeno, 3=bod
    sort_order: int         # Position within the document
    parent_element_id: Optional[str] = None  # Parent's element_id
    has_pdf_attachment: bool = False
    pdf_url: Optional[str] = None
    children: list["SectionRecord"] = field(default_factory=list)


def _get_text(tag: Tag, class_name: str) -> str:
    """Extract text from a child div with the given class."""
    child = tag.find("div", class_=class_name, recursive=False)
    if child is None:
        return ""
    return child.get_text(strip=True)


def _get_text_div(tag: Tag) -> str:
    """Extract text from the direct 'text' class div."""
    text_div = tag.find("div", class_="text", recursive=False)
    if text_div is None:
        return ""
    return text_div.get_text(separator=" ", strip=True)


def _get_element_id(tag: Tag) -> str:
    """Get the id attribute of a tag, or empty string."""
    value = tag.get("id", "")
    if isinstance(value, list):
        return value[0] if value else ""
    return value or ""


def _extract_number_from_id(element_id: str, prefix: str) -> str:
    """Extract the section number from an element id.

    Example: "paragraf-2.odsek-1.pismeno-a" with prefix "pismeno-" → "a"
    """
    if not element_id:
        return ""
    parts = element_id.split(".")
    for part in reversed(parts):
        if part.startswith(prefix):
            return part[len(prefix):]
    return element_id


def _find_content_start(soup: BeautifulSoup) -> Optional[Tag]:
    """Find the start of the actual law content (after the table of contents).

    The content section has elements with proper id attributes like
    'paragraf-1', while the TOC section has elements without id attributes.
    """
    # Look for the first paragraf with an actual id
    first_paragraf = soup.find("div", class_="paragraf", id=True)
    if first_paragraf and first_paragraf.parent:
        return first_paragraf.parent
    return None


def parse_html(raw_html: str, law_id: str) -> list[SectionRecord]:
    """Parse slov-lex.sk HTML into hierarchical section records.

    Args:
        raw_html: Complete HTML page content.
        law_id: Law identifier (e.g., "222/2004") for logging.

    Returns:
        Flat list of SectionRecord objects with parent_element_id references.
    """
    soup = BeautifulSoup(raw_html, "html.parser")
    records: list[SectionRecord] = []
    sort_counter = 0

    # --- Parse skupinaParagrafov (paragraph groups / chapters) ---
    for group in soup.find_all("div", class_="skupinaParagrafov", id=True):
        element_id = _get_element_id(group)
        title = _get_text(group, "skupinaParagrafovOznacenie")

        sort_counter += 1
        records.append(SectionRecord(
            section_type="skupinaParagrafov",
            section_number=_extract_number_from_id(element_id, "skupinaParagrafov-"),
            element_id=element_id,
            title=title,
            text_content=title,
            raw_html=str(group)[:5000],  # Truncate raw HTML for groups (they contain everything)
            depth=0,
            sort_order=sort_counter,
            parent_element_id=None,
        ))

    # --- Parse paragraf sections (§) ---
    for paragraf in soup.find_all("div", class_="paragraf", id=True):
        p_id = _get_element_id(paragraf)
        if not p_id.startswith("paragraf-"):
            continue

        p_number = _extract_number_from_id(p_id, "paragraf-")
        p_title = _get_text(paragraf, "paragrafNadpis")
        p_text = _get_text_div(paragraf)

        # Find parent skupinaParagrafov
        parent_group = paragraf.find_parent("div", class_="skupinaParagrafov", id=True)
        parent_id = _get_element_id(parent_group) if parent_group else None

        sort_counter += 1
        p_record = SectionRecord(
            section_type="paragraf",
            section_number=p_number,
            element_id=p_id,
            title=p_title if p_title else None,
            text_content=p_text,
            raw_html=str(paragraf)[:10000],
            depth=0,
            sort_order=sort_counter,
            parent_element_id=parent_id,
        )
        records.append(p_record)

        # --- Parse odsek (subsections) within this paragraf ---
        for odsek in paragraf.find_all("div", class_="odsek", id=True, recursive=False):
            o_id = _get_element_id(odsek)
            o_number = _extract_number_from_id(o_id, "odsek-")
            o_text = _get_text_div(odsek)

            sort_counter += 1
            o_record = SectionRecord(
                section_type="odsek",
                section_number=o_number,
                element_id=o_id,
                title=None,
                text_content=o_text,
                raw_html=str(odsek)[:10000],
                depth=1,
                sort_order=sort_counter,
                parent_element_id=p_id,
            )
            records.append(o_record)

            # --- Parse pismeno (letters) within this odsek ---
            for pismeno in odsek.find_all("div", class_="pismeno", id=True, recursive=False):
                pi_id = _get_element_id(pismeno)
                pi_number = _extract_number_from_id(pi_id, "pismeno-")
                pi_text = _get_text_div(pismeno)

                sort_counter += 1
                pi_record = SectionRecord(
                    section_type="pismeno",
                    section_number=pi_number,
                    element_id=pi_id,
                    title=None,
                    text_content=pi_text,
                    raw_html=str(pismeno)[:5000],
                    depth=2,
                    sort_order=sort_counter,
                    parent_element_id=o_id,
                )
                records.append(pi_record)

                # --- Parse bod (points) within this pismeno ---
                for bod in pismeno.find_all("div", class_="bod", id=True, recursive=False):
                    b_id = _get_element_id(bod)
                    b_number = _extract_number_from_id(b_id, "bod-")
                    b_text = _get_text_div(bod)

                    sort_counter += 1
                    records.append(SectionRecord(
                        section_type="bod",
                        section_number=b_number,
                        element_id=b_id,
                        title=None,
                        text_content=b_text,
                        raw_html=str(bod)[:5000],
                        depth=3,
                        sort_order=sort_counter,
                        parent_element_id=pi_id,
                    ))

            # --- Parse bod directly under odsek (without pismeno wrapper) ---
            for bod in odsek.find_all("div", class_="bod", id=True, recursive=False):
                b_id = _get_element_id(bod)
                b_number = _extract_number_from_id(b_id, "bod-")
                b_text = _get_text_div(bod)

                sort_counter += 1
                records.append(SectionRecord(
                    section_type="bod",
                    section_number=b_number,
                    element_id=b_id,
                    title=None,
                    text_content=b_text,
                    raw_html=str(bod)[:5000],
                    depth=2,
                    sort_order=sort_counter,
                    parent_element_id=o_id,
                ))

    # --- Parse prílohy (annexes) ---
    for priloha in soup.find_all("div", class_="priloha", id=True):
        pr_id = _get_element_id(priloha)
        pr_title = _get_text(priloha, "prilohaOznacenie")
        pr_number = _extract_number_from_id(pr_id, "priloha-")
        pr_text = priloha.get_text(separator=" ", strip=True)

        # Check for PDF attachments
        pdf_link = priloha.find("a", class_="predpis-pdf-priloha")
        has_pdf = pdf_link is not None
        pdf_href = pdf_link.get("href") if pdf_link else None
        pdf_url = pdf_href[0] if isinstance(pdf_href, list) else pdf_href

        sort_counter += 1
        records.append(SectionRecord(
            section_type="priloha",
            section_number=pr_number,
            element_id=pr_id,
            title=pr_title if pr_title else None,
            text_content=pr_text[:50000],  # Annexes can be large
            raw_html=str(priloha)[:50000],
            depth=0,
            sort_order=sort_counter,
            parent_element_id=None,
            has_pdf_attachment=has_pdf,
            pdf_url=pdf_url,
        ))

    # --- Parse poznámky (footnotes) ---
    for poznamka in soup.find_all("div", class_="poznamka", id=True):
        pz_id = _get_element_id(poznamka)
        pz_number = _extract_number_from_id(pz_id, "poznamka-")
        pz_title = _get_text(poznamka, "poznamkaOznacenie")
        pz_text = _get_text_div(poznamka)

        sort_counter += 1
        records.append(SectionRecord(
            section_type="poznamka",
            section_number=pz_number,
            element_id=pz_id,
            title=pz_title if pz_title else None,
            text_content=pz_text,
            raw_html=str(poznamka)[:5000],
            depth=0,
            sort_order=sort_counter,
            parent_element_id=None,
        ))

    logger.info(
        "Parsed %s: %d total records", law_id, len(records),
    )

    # Log counts by type
    type_counts: dict[str, int] = {}
    for r in records:
        type_counts[r.section_type] = type_counts.get(r.section_type, 0) + 1
    for stype, count in sorted(type_counts.items()):
        logger.info("  %s: %d", stype, count)

    return records


def build_full_text(records: list[SectionRecord]) -> dict[str, str]:
    """Build full_text for each record by concatenating its text with all descendants.

    Args:
        records: Flat list of parsed section records.

    Returns:
        Dict mapping element_id -> full concatenated text.
    """
    # Index by element_id
    by_id: dict[str, SectionRecord] = {r.element_id: r for r in records if r.element_id}

    # Build children map
    children_map: dict[str, list[str]] = {}
    for r in records:
        if r.parent_element_id:
            children_map.setdefault(r.parent_element_id, []).append(r.element_id)

    def _collect_text(element_id: str) -> str:
        record = by_id.get(element_id)
        if not record:
            return ""
        parts = [record.text_content] if record.text_content else []
        for child_id in children_map.get(element_id, []):
            child_text = _collect_text(child_id)
            if child_text:
                parts.append(child_text)
        return " ".join(parts)

    return {eid: _collect_text(eid) for eid in by_id}


def parse_history(raw_html: str) -> list[dict[str, str]]:
    """Extract version history from the HTML history table.

    Returns:
        List of dicts with keys: effective_from, effective_to, url, amendment.
    """
    soup = BeautifulSoup(raw_html, "html.parser")
    history: list[dict[str, str]] = []

    for row in soup.find_all("tr", class_="effectivenessHistoryItem"):
        entry = {
            "effective_from": row.get("data-ucinnostod", ""),
            "effective_to": row.get("data-ucinnostdo", ""),
            "url": "",
            "amendment": "",
        }
        # Extract URL from first link
        link = row.find("a")
        if link:
            entry["url"] = link.get("href", "")

        # Extract amendment reference from second link (if exists)
        links = row.find_all("a")
        if len(links) > 1:
            entry["amendment"] = links[1].get_text(strip=True)

        if entry["effective_from"]:  # Skip "vyhlásené znenie" (published version)
            history.append(entry)

    return history
