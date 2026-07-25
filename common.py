"""Shared helpers for all agency agents."""
import logging
import os
import sys
from datetime import date
from pathlib import Path
from typing import Optional

from anthropic import Anthropic, APIError, RateLimitError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
MODEL = os.environ.get("AGENT_MODEL", "claude-3-5-sonnet-20241022")
OUTPUT_DIR = Path("deliverables")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", "3"))
REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "30"))

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))


def get_client() -> Anthropic:
    """Initialize and return Anthropic client with error handling."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY not set")
        sys.exit(
            "❌ API key not found.\n\n"
            "1. Get an API key: https://console.anthropic.com (Settings → API Keys)\n"
            "2. Copy .env.example to .env and add your key\n"
            "   export ANTHROPIC_API_KEY='sk-ant-...'\n"
            "3. Or run: python setup.py"
        )
    try:
        client = Anthropic(api_key=api_key, timeout=REQUEST_TIMEOUT)
        logger.debug("Anthropic client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Anthropic client: {e}")
        sys.exit(f"❌ Client initialization failed: {e}")


def load_brief(path: str = "client_brief.md") -> str:
    """Load and validate client brief file."""
    f = Path(path)
    if not f.exists():
        logger.error(f"Brief file not found: {path}")
        sys.exit(
            f"❌ No {path} found.\n\n"
            "Steps:\n"
            f"1. Copy: cp client_brief.example.md {path}\n"
            "2. Edit the file with your client details\n"
            "3. Run again"
        )
    
    content = f.read_text().strip()
    if not content:
        logger.error(f"Brief file is empty: {path}")
        sys.exit(f"❌ {path} is empty. Fill in your client details.")
    
    logger.info(f"Loaded client brief from {path} ({len(content)} bytes)")
    return content


def ask_claude(
    client: Anthropic,
    system: str,
    user: str,
    max_tokens: int = 8000,
    model: Optional[str] = None,
) -> str:
    """
    Query Claude with retry logic and error handling.
    
    Args:
        client: Anthropic client instance
        system: System prompt
        user: User message
        max_tokens: Maximum tokens in response
        model: Model to use (defaults to AGENT_MODEL)
    
    Returns:
        Claude's response text
    """
    model = model or MODEL
    
    for attempt in range(MAX_RETRIES):
        try:
            logger.debug(f"API call (attempt {attempt + 1}/{MAX_RETRIES}): {model}")
            msg = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            
            response_text = "".join(b.text for b in msg.content if b.type == "text")
            logger.info(
                f"✓ API call successful - {msg.usage.input_tokens} input, "
                f"{msg.usage.output_tokens} output tokens"
            )
            return response_text
        
        except RateLimitError as e:
            if attempt < MAX_RETRIES - 1:
                wait_time = 2 ** (attempt + 1)
                logger.warning(f"Rate limited. Retrying in {wait_time}s... ({attempt + 1}/{MAX_RETRIES})")
                import time
                time.sleep(wait_time)
            else:
                logger.error(f"Rate limit exceeded after {MAX_RETRIES} attempts")
                sys.exit(f"❌ Rate limited: {e}")
        
        except APIError as e:
            logger.error(f"API error (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES - 1:
                import time
                time.sleep(2 ** attempt)
            else:
                sys.exit(f"❌ API error after {MAX_RETRIES} attempts: {e}")
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            sys.exit(f"❌ Error: {e}")


def save(name: str, content: str) -> Path:
    """Save output to timestamped file in deliverables directory."""
    try:
        OUTPUT_DIR.mkdir(exist_ok=True)
        timestamp = date.today().isoformat()
        out = OUTPUT_DIR / f"{timestamp}_{name}"
        out.write_text(content)
        logger.info(f"✓ Saved deliverable: {out}")
        print(f"\n✅ Saved: {out}")
        return out
    except Exception as e:
        logger.error(f"Failed to save output: {e}")
        sys.exit(f"❌ Could not save to {OUTPUT_DIR}: {e}")
