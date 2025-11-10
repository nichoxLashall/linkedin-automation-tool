import os
from http.cookies import SimpleCookie
from typing import Dict

def parse_cookie_string(cookie_string: str) -> Dict[str, str]:
    """
    Parse a browser-style cookie header string into a simple dict.

    Example input:
        "li_at=abc123; JSESSIONID=xyz; foo=bar"
    """
    cookie = SimpleCookie()
    cookie.load(cookie_string)
    return {key: morsel.value for key, morsel in cookie.items()}

def load_cookie_from_env(env_var: str = "LINKEDIN_SALES_NAV_COOKIE") -> Dict[str, str]:
    """
    Load and parse the Sales Navigator cookie string from an environment variable.

    Raises:
        RuntimeError: if the environment variable is not set or is empty.
    """
    raw = os.getenv(env_var, "").strip()
    if not raw:
        raise RuntimeError(
            f"Environment variable {env_var!r} is not set or is empty. "
            "Export a valid Sales Navigator cookie string before running the tool."
        )
    return parse_cookie_string(raw)