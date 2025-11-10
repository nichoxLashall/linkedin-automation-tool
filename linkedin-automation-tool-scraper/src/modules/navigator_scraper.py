import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import urlparse, parse_qs

@dataclass
class ScraperConfig:
    request_timeout: int = 20
    rate_limit_seconds: float = 1.5

class NavigatorScraper:
    """
    Simulated LinkedIn Sales Navigator scraper.

    This implementation is intentionally offline-safe and does not perform any
    network requests to LinkedIn. Instead, it enriches profile records with
    derived values from the URL and optional CSV columns.
    """

    def __init__(self, logger: logging.Logger, settings: Optional[Dict[str, Any]] = None) -> None:
        self.logger = logger
        settings = settings or {}
        self.config = ScraperConfig(
            request_timeout=int(settings.get("request_timeout", 20)),
            rate_limit_seconds=float(settings.get("rate_limit_seconds", 1.5)),
        )

    def _derive_name_from_url(self, profile_url: str) -> str:
        """
        Derive a synthetic full_name from the profile URL if none is provided.
        Example:
            https://www.linkedin.com/sales/lead/1234567890 -> "Lead 1234567890"
        """
        try:
            path_parts = urlparse(profile_url).path.strip("/").split("/")
            if not path_parts:
                return "LinkedIn Member"
            # Last segment is often the numeric ID
            identifier = path_parts[-1]
            if identifier.isdigit():
                return f"Lead {identifier}"
            # Fallback to a capitalized slug
            return identifier.replace("-", " ").title() or "LinkedIn Member"
        except Exception:
            return "LinkedIn Member"

    def _derive_company_from_query(self, profile_url: str, fallback: str | None) -> str | None:
        """
        Attempt to read a company value from any query parameter, or fall back.
        """
        try:
            parsed = urlparse(profile_url)
            query = parse_qs(parsed.query)
            for key in ("company", "org", "cname"):
                if key in query and query[key]:
                    return query[key][0]
        except Exception:
            pass
        return fallback

    def enrich_profile(self, profile_row: Dict[str, Any], cookies: Dict[str, str]) -> Dict[str, Any]:
        """
        Given a CSV row and cookies, return a normalized profile dict.

        This simulates the scraping step: in a real implementation, it would
        perform authenticated HTTP requests using the provided cookies.
        """
        profile_url = (profile_row.get("profile_url") or "").strip()
        if not profile_url:
            raise ValueError("profile_url is required for enrichment")

        self.logger.debug("Enriching profile from URL: %s", profile_url)

        # Respect a minimal rate limit to avoid hammering LinkedIn in real scenarios.
        time.sleep(self.config.rate_limit_seconds)

        full_name = (profile_row.get("full_name") or "").strip()
        if not full_name:
            full_name = self._derive_name_from_url(profile_url)

        headline = (profile_row.get("headline") or "").strip() or None
        company_csv = (profile_row.get("company") or "").strip() or None
        company = self._derive_company_from_query(profile_url, fallback=company_csv)
        location = (profile_row.get("location") or "").strip() or None

        enriched = {
            "profile_url": profile_url,
            "full_name": full_name,
            "headline": headline,
            "company": company,
            "location": location,
        }

        self.logger.info(
            "Enriched profile: full_name=%s, company=%s, location=%s",
            full_name,
            company,
            location,
        )

        return enriched