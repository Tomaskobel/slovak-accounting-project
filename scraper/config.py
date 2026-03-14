"""Law registry, URL patterns, and Supabase client for scraper."""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv(override=True)

# ---------------------------------------------------------------------------
# Law registry
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LawDefinition:
    """Definition of a law to scrape."""
    law_id: str          # e.g., "222/2004"
    title: str           # Full Slovak title
    collection: str      # ZZ = Zbierka zákonov
    year: int
    number: int
    target_dates: tuple[str, ...]  # YYYYMMDD effective dates to fetch


LAWS: dict[str, LawDefinition] = {
    "222/2004": LawDefinition(
        law_id="222/2004",
        title="Zákon o dani z pridanej hodnoty",
        collection="ZZ",
        year=2004,
        number=222,
        target_dates=("20250401",),
    ),
    "431/2002": LawDefinition(
        law_id="431/2002",
        title="Zákon o účtovníctve",
        collection="ZZ",
        year=2002,
        number=431,
        target_dates=("20260101",),
    ),
}

# ---------------------------------------------------------------------------
# URL patterns
# ---------------------------------------------------------------------------

STATIC_BASE = "https://static.slov-lex.sk/static/SK"


def build_url(law: LawDefinition, date: str) -> str:
    """Build the full URL for a specific law version.

    Args:
        law: Law definition with collection, year, number.
        date: Effective date in YYYYMMDD format.

    Returns:
        Full URL to the static HTML page.
    """
    return (
        f"{STATIC_BASE}/{law.collection}/{law.year}/{law.number}/{date}.html"
    )


# ---------------------------------------------------------------------------
# HTTP settings
# ---------------------------------------------------------------------------

USER_AGENT = "SlovakAccountingProject/1.0 (legal-text-scraper)"
REQUEST_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0  # seconds, multiplied by attempt number
POLITENESS_DELAY = 2.0  # seconds between requests

# ---------------------------------------------------------------------------
# Supabase client
# ---------------------------------------------------------------------------

_supabase_client: Optional[Client] = None


def get_supabase() -> Client:
    """Get or create the Supabase client singleton."""
    global _supabase_client
    if _supabase_client is None:
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        if not url or not key:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_KEY must be set in environment. "
                "Check ~/.zshrc."
            )
        _supabase_client = create_client(url, key)
    return _supabase_client
