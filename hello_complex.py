"""
A "complex" Hello World implementation demonstrating:
- typed signatures
- sync and async variants
- retries with exponential backoff
- simple i18n (en/es/fr)
- optional HTML-escaping and styling
- structured return value and logging

This file was added by an automated assistant.
"""

import asyncio
import html
import logging
import random
import time
from typing import Dict, Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


I18N: Dict[str, str] = {
    "en": "Hello, {name}!",
    "es": "¡Hola, {name}!",
    "fr": "Bonjour, {name}!",
}


def _apply_style(text: str, style: str) -> str:
    if style == "upper":
        return text.upper()
    if style == "lower":
        return text.lower()
    if style == "title":
        return text.title()
    # ANSI green as default "fancy"
    if style == "fancy":
        return f"\033[92m{text}\033[0m"
    return text


def _safe_text(text: str, html_safe: bool) -> str:
    return html.escape(text) if html_safe else text


def _build_message(name: str, locale: str, html_safe: bool, style: str) -> str:
    template = I18N.get(locale, I18N["en"])
    raw = template.format(name=name)
    raw = _safe_text(raw, html_safe)
    return _apply_style(raw, style)


def retry(max_attempts: int = 3, base_delay: float = 0.1):
    """Simple retry decorator with exponential backoff and jitter."""

    def decorator(fn):
        def wrapper(*args, **kwargs):
            attempt = 0
            while True:
                try:
                    attempt += 1
                    return fn(*args, **kwargs)
                except Exception as exc:
                    if attempt >= max_attempts:
                        logger.exception("All retry attempts failed")
                        raise
                    sleep_for = base_delay * (2 ** (attempt - 1)) * (1 + random.random() * 0.1)
                    logger.warning(
                        "Attempt %d failed: %s — retrying in %.2fs", attempt, exc, sleep_for
                    )
                    time.sleep(sleep_for)

        return wrapper

    return decorator


@retry(max_attempts=4, base_delay=0.05)
def complex_hello_world(
    name: Optional[str] = None,
    locale: str = "en",
    style: str = "plain",
    html_safe: bool = False,
    pause: float = 0.0,
) -> Dict[str, object]:
    """
    Synchronous complex hello-world.

    Returns a dict with:
    - message: rendered greeting string
    - meta: details about inputs and timestamp
    """
    if not name:
        raise ValueError("name is required")

    if pause:
        # Simulate work or intermittent failure
        if random.random() < 0.15:
            raise RuntimeError("transient failure while preparing greeting")
        time.sleep(pause)

    message = _build_message(name, locale, html_safe, style)
    result = {
        "message": message,
        "meta": {"locale": locale, "style": style, "html_safe": html_safe, "timestamp": time.time()},
    }
    logger.info("Generated greeting for %s: %s", name, message)
    return result


async def async_complex_hello_world(
    name: Optional[str] = None,
    locale: str = "en",
    style: str = "plain",
    html_safe: bool = False,
    pause: float = 0.0,
) -> Dict[str, object]:
    """
    Async variant (awaitable). Uses similar behavior but compatible with asyncio.
    """
    if not name:
        raise ValueError("name is required")

    # Simulate async work
    if pause:
        # occasional transient error
        if random.random() < 0.12:
            raise RuntimeError("async transient failure")
        await asyncio.sleep(pause)

    message = _build_message(name, locale, html_safe, style)
    result = {
        "message": message,
        "meta": {"locale": locale, "style": style, "html_safe": html_safe, "timestamp": time.time()},
    }
    logger.info("Generated async greeting for %s: %s", name, message)
    return result


# Small demonstration when run as script
if __name__ == "__main__":
    print(complex_hello_world("World", style="fancy")["message"])
    # demo async
    print(asyncio.run(async_complex_hello_world("Async World", locale="es", style="title"))["message"])
