"""
Sync pravidla.py rules to Supabase graph_pravidla table.

Usage:
    python3 -m engine.sync_pravidla          # sync all rules
    python3 -m engine.sync_pravidla --check  # dry-run: show what would change
"""

import argparse
import logging
import os

from dotenv import load_dotenv
from supabase import create_client

from engine.pravidla import VSETKY_PRAVIDLA
from engine.schema import Pravidlo

load_dotenv(override=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def _pravidlo_to_row(p: Pravidlo, graph_version: int = 1) -> dict:
    """Convert a Pravidlo dataclass to a Supabase row dict."""
    podmienky = {
        "smer": p.podmienky.smer.value,
        "typ_plnenia": p.podmienky.typ_plnenia.value if p.podmienky.typ_plnenia else None,
        "krajina_dodavatela": p.podmienky.krajina_dodavatela.value if p.podmienky.krajina_dodavatela else None,
        "platitel_dph_kupujuci": p.podmienky.platitel_dph_kupujuci,
        "platitel_dph_dodavatel": p.podmienky.platitel_dph_dodavatel,
        "forma_uhrady": p.podmienky.forma_uhrady,
        "metoda_zasob": p.podmienky.metoda_zasob,
        "tuzemsky_prenos": p.podmienky.tuzemsky_prenos,
    }

    riadky = [
        {
            "ucet": r.ucet,
            "strana": r.strana.value,
            "vzorec_sumy": r.vzorec_sumy.value,
            "popis": r.popis,
        }
        for r in p.riadky
    ]

    return {
        "pravidlo_id": p.id,
        "nazov": p.nazov,
        "name_en": p.name_en,
        "podmienky": podmienky,
        "riadky": riadky,
        "dph_treatment": p.dph_treatment.value,
        "sadzba_dane_id": p.sadzba_dane_id,
        "kv_dph_sekcia": p.kv_dph_sekcia.value,
        "povinne_vstupy": list(p.povinne_vstupy),
        "pravny_zdroj": p.pravny_zdroj,
        "priorita": p.priorita,
        "platne_od": p.platne_od,
        "platne_do": p.platne_do,
        "krok": p.krok,
        "celkovo_krokov": p.celkovo_krokov,
        "poznamky": p.poznamky,
        "dovera": p.dovera,
        "graph_version": graph_version,
    }


def get_supabase():
    """Create Supabase client."""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set")
    return create_client(url, key)


def sync_rules(dry_run: bool = False, graph_version: int = 1) -> None:
    """Sync all rules from pravidla.py to Supabase."""
    sb = get_supabase()

    # Get existing rules for this version
    existing = sb.table("graph_pravidla").select("pravidlo_id").eq(
        "graph_version", graph_version
    ).execute()
    existing_ids = {r["pravidlo_id"] for r in existing.data}

    local_ids = {p.id for p in VSETKY_PRAVIDLA}

    to_insert = local_ids - existing_ids
    to_update = local_ids & existing_ids
    to_remove = existing_ids - local_ids

    print(f"\nGraph version: {graph_version}")
    print(f"Local rules:    {len(local_ids)}")
    print(f"Existing in DB: {len(existing_ids)}")
    print(f"  → Insert: {len(to_insert)}")
    print(f"  → Update: {len(to_update)}")
    print(f"  → Remove: {len(to_remove)}")

    if dry_run:
        if to_insert:
            print(f"\nWould insert: {sorted(to_insert)}")
        if to_update:
            print(f"Would update: {sorted(to_update)}")
        if to_remove:
            print(f"Would remove: {sorted(to_remove)}")
        return

    # Build rows for upsert
    rows = [_pravidlo_to_row(p, graph_version) for p in VSETKY_PRAVIDLA]

    # Delete removed rules
    if to_remove:
        for rid in to_remove:
            sb.table("graph_pravidla").delete().eq(
                "pravidlo_id", rid
            ).eq("graph_version", graph_version).execute()
            logger.info("Deleted: %s", rid)

    # Upsert all current rules
    sb.table("graph_pravidla").upsert(
        rows, on_conflict="pravidlo_id,graph_version"
    ).execute()
    logger.info("Upserted %d rules (version %d)", len(rows), graph_version)

    # Verify
    count = sb.table("graph_pravidla").select(
        "pravidlo_id", count="exact"
    ).eq("graph_version", graph_version).execute()
    print(f"\nVerification: {count.count} rules in DB (version {graph_version})")


def main():
    parser = argparse.ArgumentParser(description="Sync pravidla to Supabase")
    parser.add_argument("--check", action="store_true", help="Dry run — show what would change")
    parser.add_argument("--version", type=int, default=1, help="Graph version (default: 1)")
    args = parser.parse_args()

    sync_rules(dry_run=args.check, graph_version=args.version)


if __name__ == "__main__":
    main()
