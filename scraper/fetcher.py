"""HTTP fetcher for slov-lex.sk legal texts with retries and rate limiting."""

import logging
import time
from typing import Optional

import requests

from scraper.config import (
    LawDefinition,
    build_url,
    MAX_RETRIES,
    POLITENESS_DELAY,
    REQUEST_TIMEOUT,
    RETRY_BACKOFF,
    USER_AGENT,
)

logger = logging.getLogger(__name__)


class FetchError(Exception):
    """Raised when fetching a law page fails after all retries."""


def fetch_law(law: LawDefinition, date: str) -> str:
    """Fetch raw HTML for a specific law version from slov-lex.sk.

    Args:
        law: Law definition with URL components.
        date: Effective date in YYYYMMDD format.

    Returns:
        Raw HTML content as string.

    Raises:
        FetchError: If all retries are exhausted.
    """
    url = build_url(law, date)
    logger.info("Fetching %s (effective %s) from %s", law.law_id, date, url)

    last_error: Optional[Exception] = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(
                url,
                timeout=REQUEST_TIMEOUT,
                headers={"User-Agent": USER_AGENT},
            )
            response.raise_for_status()
            response.encoding = "utf-8"

            html = response.text
            size = len(html.encode("utf-8"))
            logger.info(
                "Fetched %s/%s: %d bytes, status %d",
                law.law_id, date, size, response.status_code,
            )
            return html

        except requests.RequestException as e:
            last_error = e
            logger.warning(
                "Attempt %d/%d failed for %s/%s: %s",
                attempt, MAX_RETRIES, law.law_id, date, e,
            )
            if attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF * attempt
                logger.info("Waiting %.1f seconds before retry...", wait)
                time.sleep(wait)

    raise FetchError(
        f"Failed to fetch {law.law_id} (date {date}) after {MAX_RETRIES} "
        f"attempts. Last error: {last_error}"
    )


def fetch_with_delay(law: LawDefinition, dates: list[str]) -> dict[str, str]:
    """Fetch multiple versions of a law with politeness delay between requests.

    Args:
        law: Law definition.
        dates: List of effective dates in YYYYMMDD format.

    Returns:
        Dict mapping date -> raw HTML.
    """
    results: dict[str, str] = {}
    for i, date in enumerate(dates):
        if i > 0:
            logger.info("Politeness delay: %.1f seconds", POLITENESS_DELAY)
            time.sleep(POLITENESS_DELAY)
        results[date] = fetch_law(law, date)
    return results
