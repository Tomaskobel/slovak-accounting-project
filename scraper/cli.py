"""CLI entry point for the legal text scraper.

Usage:
    python -m scraper fetch 222/2004 --date 20250401
    python -m scraper fetch-all
    python -m scraper parse 222/2004 --date 20250401
    python -m scraper verify 222/2004
    python -m scraper history 222/2004 --date 20250401
    python -m scraper pipeline 222/2004 --date 20250401  # fetch + parse + verify
    python -m scraper pipeline-all                        # all laws, all dates
"""

import argparse
import logging
import sys
from datetime import date as date_type

from scraper.config import LAWS, build_url
from scraper.fetcher import fetch_law
from scraper.parser import parse_html, parse_history
from scraper.store import store_document, clear_sections, store_sections
from scraper.verify import verify_law, print_report

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def _parse_effective_date(date_str: str) -> date_type:
    """Convert YYYYMMDD string to date object."""
    if len(date_str) != 8 or not date_str.isdigit():
        raise ValueError(
            f"Invalid date format: '{date_str}'. Expected YYYYMMDD (e.g., 20250401)."
        )
    return date_type(
        year=int(date_str[:4]),
        month=int(date_str[4:6]),
        day=int(date_str[6:8]),
    )


def cmd_fetch(args: argparse.Namespace) -> None:
    """Fetch raw HTML and store in Supabase."""
    law = LAWS.get(args.law_id)
    if not law:
        print(f"Unknown law_id: {args.law_id}. Available: {list(LAWS.keys())}")
        sys.exit(1)

    date = args.date or law.target_dates[0]
    raw_html = fetch_law(law, date)

    effective_from = _parse_effective_date(date)
    source_url = build_url(law, date)

    doc_id = store_document(
        law_id=law.law_id,
        law_title=law.title,
        collection=law.collection,
        effective_from=effective_from,
        effective_to=None,
        source_url=source_url,
        raw_html=raw_html,
    )
    print(f"Stored {law.law_id} (effective {effective_from}) → document {doc_id}")
    print(f"HTML size: {len(raw_html.encode('utf-8')):,} bytes")


def cmd_fetch_all(args: argparse.Namespace) -> None:
    """Fetch all configured laws."""
    import time
    from scraper.config import POLITENESS_DELAY

    first = True
    for law in LAWS.values():
        for date in law.target_dates:
            if not first:
                logger.info("Politeness delay: %.1f seconds", POLITENESS_DELAY)
                time.sleep(POLITENESS_DELAY)
            first = False

            raw_html = fetch_law(law, date)
            effective_from = _parse_effective_date(date)
            source_url = build_url(law, date)

            doc_id = store_document(
                law_id=law.law_id,
                law_title=law.title,
                collection=law.collection,
                effective_from=effective_from,
                effective_to=None,
                source_url=source_url,
                raw_html=raw_html,
            )
            print(f"Stored {law.law_id} (effective {effective_from}) → {doc_id}")


def cmd_parse(args: argparse.Namespace) -> None:
    """Parse stored HTML into sections."""
    from scraper.config import get_supabase

    sb = get_supabase()
    law_id = args.law_id

    # Find the document
    query = sb.table("law_documents").select("id, raw_html, effective_from").eq("law_id", law_id)
    if args.date:
        effective = _parse_effective_date(args.date)
        query = query.eq("effective_from", effective.isoformat())
    docs = query.execute()

    if not docs.data:
        print(f"No stored document found for {law_id}. Run 'fetch' first.")
        sys.exit(1)

    doc = docs.data[0]
    doc_id = doc["id"]
    raw_html = doc["raw_html"]
    effective_from = date_type.fromisoformat(doc["effective_from"])

    if not raw_html:
        print(f"Document {doc_id} has no raw_html. Fetch may have failed.")
        sys.exit(1)

    # Clear existing sections
    clear_sections(doc_id)

    # Parse
    records = parse_html(raw_html, law_id)
    print(f"Parsed {len(records)} sections from {law_id}")

    # Store
    stored = store_sections(doc_id, law_id, effective_from, records)
    print(f"Stored {stored} sections for {law_id} (effective {effective_from})")


def cmd_verify(args: argparse.Namespace) -> None:
    """Run verification checks."""
    effective = None
    if args.date:
        effective = _parse_effective_date(args.date).isoformat()

    report = verify_law(args.law_id, effective)
    print_report(report)


def cmd_history(args: argparse.Namespace) -> None:
    """Show version history from stored HTML."""
    from scraper.config import get_supabase

    sb = get_supabase()
    query = sb.table("law_documents").select("raw_html, effective_from").eq("law_id", args.law_id)
    if args.date:
        effective = _parse_effective_date(args.date)
        query = query.eq("effective_from", effective.isoformat())
    docs = query.execute()

    if not docs.data:
        print(f"No stored document found for {args.law_id}.")
        sys.exit(1)

    raw_html = docs.data[0]["raw_html"]
    history = parse_history(raw_html)
    print(f"\nVersion history for {args.law_id} ({len(history)} versions):\n")
    for h in history:
        amendment = f" (novela: {h['amendment']})" if h["amendment"] else ""
        print(f"  {h['effective_from']} → {h['effective_to'] or 'current'}{amendment}")


def cmd_pipeline(args: argparse.Namespace) -> None:
    """Full pipeline: fetch → parse → verify."""
    law = LAWS.get(args.law_id)
    if not law:
        print(f"Unknown law_id: {args.law_id}. Available: {list(LAWS.keys())}")
        sys.exit(1)

    date = args.date or law.target_dates[0]

    print(f"\n--- Step 1: Fetch {law.law_id} (date {date}) ---")
    raw_html = fetch_law(law, date)
    effective_from = _parse_effective_date(date)
    source_url = build_url(law, date)

    doc_id = store_document(
        law_id=law.law_id,
        law_title=law.title,
        collection=law.collection,
        effective_from=effective_from,
        effective_to=None,
        source_url=source_url,
        raw_html=raw_html,
    )
    print(f"  Stored → {doc_id} ({len(raw_html.encode('utf-8')):,} bytes)")

    print(f"\n--- Step 2: Parse ---")
    records = parse_html(raw_html, law.law_id)
    print(f"  Parsed {len(records)} sections")

    clear_sections(doc_id)
    stored = store_sections(doc_id, law.law_id, effective_from, records)
    print(f"  Stored {stored} sections")

    print(f"\n--- Step 3: Verify ---")
    report = verify_law(law.law_id, effective_from.isoformat())
    print_report(report)


def cmd_parse_pdf(args: argparse.Namespace) -> None:
    """Parse a local PDF file into sections and store in Supabase."""
    from scraper.config import get_supabase
    from scraper.pdf_parser import extract_text_from_pdf, parse_postupy_uctovania, parse_kv_dph_guidelines
    from scraper.parser import build_full_text

    pdf_path = args.pdf_path
    doc_type = args.type
    effective_from = _parse_effective_date(args.date)

    # Extract text from PDF
    print(f"\n--- Step 1: Extract text from {pdf_path} ---")
    raw_text = extract_text_from_pdf(pdf_path)
    print(f"  Extracted {len(raw_text):,} characters")

    # Parse into sections
    print(f"\n--- Step 2: Parse ({doc_type}) ---")
    if doc_type == "postupy":
        law_id = "23054/2002-92"
        law_title = "Opatrenie MF SR — Postupy účtovania pre podnikateľov (podvojné účtovníctvo)"
        records = parse_postupy_uctovania(raw_text)
    elif doc_type == "kv-dph":
        law_id = "KV-DPH"
        law_title = "Metodický pokyn Finančnej správy SR ku kontrolnému výkazu DPH"
        records = parse_kv_dph_guidelines(raw_text)
    else:
        print(f"Unknown document type: {doc_type}. Use 'postupy' or 'kv-dph'.")
        sys.exit(1)

    print(f"  Parsed {len(records)} sections")

    # Store in Supabase
    print(f"\n--- Step 3: Store in Supabase ---")
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    doc_id = store_document(
        law_id=law_id,
        law_title=law_title,
        collection="PDF",
        effective_from=effective_from,
        effective_to=None,
        source_url=args.source_url or f"file://{pdf_path}",
        raw_html=raw_text,  # Store extracted text in raw_html field
    )
    print(f"  Stored document → {doc_id}")

    clear_sections(doc_id)
    stored = store_sections(doc_id, law_id, effective_from, records)
    print(f"  Stored {stored} sections")

    # Verify
    print(f"\n--- Step 4: Verify ---")
    report = verify_law(law_id, effective_from.isoformat())
    print_report(report)


def cmd_fetch_pdf(args: argparse.Namespace) -> None:
    """Download a PDF from URL and run parse-pdf pipeline."""
    from scraper.pdf_parser import fetch_pdf
    from pathlib import Path

    url = args.url
    doc_type = args.type
    effective_from = _parse_effective_date(args.date)

    # Download PDF
    pdf_dir = Path("scraper/pdfs")
    pdf_dir.mkdir(exist_ok=True)
    filename = f"{doc_type}_{args.date}.pdf"
    pdf_path = pdf_dir / filename

    print(f"\n--- Downloading PDF from {url} ---")
    fetch_pdf(url, pdf_path)
    print(f"  Saved to {pdf_path}")

    # Set up args for parse_pdf
    args.pdf_path = str(pdf_path)
    args.source_url = url
    cmd_parse_pdf(args)


def cmd_pipeline_all(args: argparse.Namespace) -> None:
    """Run full pipeline for all configured laws."""
    import time
    from scraper.config import POLITENESS_DELAY

    first = True
    for law in LAWS.values():
        for date in law.target_dates:
            if not first:
                time.sleep(POLITENESS_DELAY)
            first = False

            print(f"\n{'#'*60}")
            print(f"# Pipeline: {law.law_id} (date {date})")
            print(f"{'#'*60}")

            # Temporarily set args for pipeline
            args.law_id = law.law_id
            args.date = date
            cmd_pipeline(args)


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Scraper pre slovenské právne predpisy zo slov-lex.sk",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # fetch
    p_fetch = subparsers.add_parser("fetch", help="Fetch raw HTML from slov-lex.sk")
    p_fetch.add_argument("law_id", help="Law ID (e.g., 222/2004)")
    p_fetch.add_argument("--date", help="Effective date YYYYMMDD")
    p_fetch.set_defaults(func=cmd_fetch)

    # fetch-all
    p_fetch_all = subparsers.add_parser("fetch-all", help="Fetch all configured laws")
    p_fetch_all.set_defaults(func=cmd_fetch_all)

    # parse
    p_parse = subparsers.add_parser("parse", help="Parse stored HTML into sections")
    p_parse.add_argument("law_id", help="Law ID")
    p_parse.add_argument("--date", help="Effective date YYYYMMDD")
    p_parse.set_defaults(func=cmd_parse)

    # verify
    p_verify = subparsers.add_parser("verify", help="Verify completeness")
    p_verify.add_argument("law_id", help="Law ID")
    p_verify.add_argument("--date", help="Effective date YYYYMMDD")
    p_verify.set_defaults(func=cmd_verify)

    # history
    p_history = subparsers.add_parser("history", help="Show version history")
    p_history.add_argument("law_id", help="Law ID")
    p_history.add_argument("--date", help="Effective date YYYYMMDD")
    p_history.set_defaults(func=cmd_history)

    # pipeline
    p_pipeline = subparsers.add_parser("pipeline", help="Full pipeline: fetch → parse → verify")
    p_pipeline.add_argument("law_id", help="Law ID")
    p_pipeline.add_argument("--date", help="Effective date YYYYMMDD")
    p_pipeline.set_defaults(func=cmd_pipeline)

    # parse-pdf
    p_parse_pdf = subparsers.add_parser("parse-pdf", help="Parse a local PDF into sections")
    p_parse_pdf.add_argument("pdf_path", help="Path to PDF file")
    p_parse_pdf.add_argument("--type", required=True, choices=["postupy", "kv-dph"],
                             help="Document type: postupy or kv-dph")
    p_parse_pdf.add_argument("--date", required=True, help="Effective date YYYYMMDD")
    p_parse_pdf.add_argument("--source-url", help="Original source URL")
    p_parse_pdf.set_defaults(func=cmd_parse_pdf)

    # fetch-pdf
    p_fetch_pdf = subparsers.add_parser("fetch-pdf", help="Download PDF and parse")
    p_fetch_pdf.add_argument("url", help="URL to download PDF from")
    p_fetch_pdf.add_argument("--type", required=True, choices=["postupy", "kv-dph"],
                             help="Document type: postupy or kv-dph")
    p_fetch_pdf.add_argument("--date", required=True, help="Effective date YYYYMMDD")
    p_fetch_pdf.set_defaults(func=cmd_fetch_pdf)

    # pipeline-all
    p_pipeline_all = subparsers.add_parser("pipeline-all", help="Full pipeline for all laws")
    p_pipeline_all.set_defaults(func=cmd_pipeline_all)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
