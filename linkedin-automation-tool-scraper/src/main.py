import argparse
import csv
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# Ensure that the src directory is on sys.path so that imports work
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from utils.logger import setup_logging, get_logger  # type: ignore
from utils.cookie_manager import load_cookie_from_env  # type: ignore
from modules.navigator_scraper import NavigatorScraper  # type: ignore
from modules.connection_sender import ConnectionSender  # type: ignore
from modules.message_dispatcher import MessageDispatcher  # type: ignore

def load_settings() -> Dict[str, Any]:
    """
    Load settings from the JSON configuration file.
    """
    config_path = CURRENT_DIR / "config" / "settings.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)

def load_input_profiles(csv_path: Path, logger: logging.Logger) -> List[Dict[str, str]]:
    """
    Load input profiles from CSV into a list of dicts.
    """
    if not csv_path.exists():
        logger.error("Input CSV not found at %s", csv_path)
        raise FileNotFoundError(f"Input CSV not found at {csv_path}")

    profiles: List[Dict[str, str]] = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip blank lines
            if not any(value.strip() for value in row.values() if isinstance(value, str)):
                continue
            profiles.append(row)

    logger.info("Loaded %d profiles from %s", len(profiles), csv_path)
    return profiles

def persist_results(results: List[Dict[str, Any]], output_path: Path, logger: logging.Logger) -> None:
    """
    Write enriched profile data to JSON file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    logger.info("Wrote %d records to %s", len(results), output_path)

def build_message(template: str, profile: Dict[str, Any]) -> str:
    """
    Render a message template using profile fields with sensible fallbacks.
    """
    full_name = profile.get("full_name") or "there"
    first_name = full_name.split()[0]
    context = {
        "full_name": full_name,
        "first_name": first_name,
        "headline": profile.get("headline") or "",
        "company": profile.get("company") or "",
        "location": profile.get("location") or "",
    }
    try:
        return template.format(**context).strip()
    except Exception:
        # Fallback to a very simple message if template variables are invalid
        return f"Hi {first_name}, I'd love to connect with you on LinkedIn."

def run(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="LinkedIn Sales Navigator automation tool (offline-safe runner)."
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to settings.json (defaults to src/config/settings.json)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without performing connection/message operations (simulated only).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of profiles to process.",
    )

    args = parser.parse_args(argv)

    # Load settings
    settings = load_settings() if args.config is None else json.loads(Path(args.config).read_text(encoding="utf-8"))

    log_level = settings.get("logging", {}).get("level", "INFO")
    setup_logging(level=log_level)
    logger = get_logger("main")

    logger.info("Starting LinkedIn automation run (dry_run=%s)", args.dry_run)

    # Load cookies from environment
    cookie_env_var = settings.get("linkedin", {}).get("cookie_env_var", "LINKEDIN_SALES_NAV_COOKIE")
    try:
        cookies = load_cookie_from_env(cookie_env_var)
    except RuntimeError as exc:
        logger.error("Cookie loading failed: %s", exc)
        return 1

    # Resolve data paths
    data_settings = settings.get("data", {})
    input_csv_path = Path(data_settings.get("input_profiles_path", CURRENT_DIR.parent / "data" / "input_profiles.csv"))
    output_json_path = Path(
        data_settings.get("output_results_path", CURRENT_DIR.parent / "data" / "output_results.json")
    )

    # Load profiles
    try:
        profiles = load_input_profiles(input_csv_path, logger)
    except FileNotFoundError as exc:
        logger.error("%s", exc)
        return 1

    if args.limit is not None:
        profiles = profiles[: args.limit]
        logger.info("Processing first %d profiles due to --limit", len(profiles))

    scraper = NavigatorScraper(
        logger=get_logger("NavigatorScraper"),
        settings=settings.get("scraper", {}),
    )
    connection_sender = ConnectionSender(
        logger=get_logger("ConnectionSender"),
        automation_settings=settings.get("automation", {}),
        dry_run=args.dry_run,
    )
    message_dispatcher = MessageDispatcher(
        logger=get_logger("MessageDispatcher"),
        automation_settings=settings.get("automation", {}),
        dry_run=args.dry_run,
    )

    results: List[Dict[str, Any]] = []
    message_template_default = settings.get("automation", {}).get(
        "message_template",
        "Hi {first_name}, I came across your profile and would love to connect.",
    )

    for idx, row in enumerate(profiles, start=1):
        profile_url = (row.get("profile_url") or "").strip()
        if not profile_url:
            logger.warning("Skipping row %d: missing profile_url", idx)
            continue

        logger.info("Processing profile %d: %s", idx, profile_url)

        try:
            # Step 1: Scrape/enrich profile
            scraped_profile = scraper.enrich_profile(row, cookies=cookies)

            # Step 2: Send connection request
            connection_status = connection_sender.send_connection(
                profile_url=profile_url,
                full_name=scraped_profile.get("full_name"),
                cookies=cookies,
            )

            # Step 3: Send message, if applicable
            row_message_template = row.get("custom_message") or message_template_default
            message_text = build_message(row_message_template, scraped_profile)
            message_status = message_dispatcher.send_message(
                profile_url=profile_url,
                message_text=message_text,
                connection_status=connection_status,
                cookies=cookies,
            )

            record = {
                "profile_url": profile_url,
                "full_name": scraped_profile.get("full_name"),
                "headline": scraped_profile.get("headline"),
                "company": scraped_profile.get("company"),
                "location": scraped_profile.get("location"),
                "connection_status": connection_status,
                "message_status": message_status,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
            results.append(record)

        except Exception as exc:
            logger.exception("Error processing profile %s: %s", profile_url, exc)
            results.append(
                {
                    "profile_url": profile_url,
                    "full_name": row.get("full_name") or None,
                    "headline": row.get("headline") or None,
                    "company": row.get("company") or None,
                    "location": row.get("location") or None,
                    "connection_status": "Error",
                    "message_status": "Error",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                }
            )

    persist_results(results, output_json_path, logger)

    logger.info("Run complete. Processed %d profiles.", len(results))
    return 0

if __name__ == "__main__":
    os._exit(run())