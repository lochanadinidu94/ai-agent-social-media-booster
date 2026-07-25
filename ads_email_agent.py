"""Ads & Email Agent.

Generates a paid ads starter kit (Google Search + Meta) and a 5-email
welcome/nurture sequence from the client brief.

Usage:
    python ads_email_agent.py            # ads + email
    python ads_email_agent.py ads        # ads only
    python ads_email_agent.py email      # email only
"""
import logging
import sys
from typing import Literal

from common import ask_claude, get_client, load_brief, save

logger = logging.getLogger(__name__)

ADS_SYSTEM = """You are a performance marketing lead at a digital agency.
Produce a launch-ready paid ads kit in Markdown:

## Google Search campaign
- 2 ad groups aligned to the client's goals, each with: 5-8 exact/phrase keywords,
  8 headlines (max 30 chars each — count carefully), 4 descriptions (max 90 chars each),
  and negative keyword suggestions.
## Meta (Facebook/Instagram) campaign
- 2 audience definitions (interests, location radius, age) with reasoning
- 3 ad variants each: primary text (with hook first line), headline, description,
  and a concrete creative brief the owner can shoot on a phone
## Landing & tracking notes
- Which page each ad should land on and why; conversion events to set up
## Suggested starting budget split and what results to expect honestly
Never promise specific ROAS or costs-per-lead. Respect brief constraints.
Include compliance notes for regulatory requirements."""

EMAIL_SYSTEM = """You are an email marketing specialist at a digital agency.
Write a 5-email welcome/nurture sequence in Markdown. For each email:
subject line + preview text + full body (150-250 words) + CTA + send timing.
Sequence arc: welcome/deliver promise -> value/education -> social proof ->
objection handling -> offer. Brand voice from the brief. No spam-trigger
words in subjects. Respect brief constraints.
Include copy tips and A/B test suggestions for each email."""


def validate_mode(mode: str) -> Literal["ads", "email", "both"]:
    """Validate and normalize mode argument."""
    mode = mode.lower().strip()
    valid_modes = {"ads", "email", "both"}
    if mode not in valid_modes:
        logger.warning(f"Invalid mode '{mode}', using 'both'")
        return "both"
    return mode  # type: ignore


def main():
    """Generate ads and/or email assets."""
    mode = validate_mode(sys.argv[1] if len(sys.argv) > 1 else "both")
    
    print(f"\n🎯 Ads & Email Asset Generator")
    print(f"{'=' * 50}")
    print(f"Mode: {mode}\n")
    
    try:
        brief = load_brief()
        client = get_client()

        if mode in ("ads", "both"):
            print("🚀 Generating Google Ads + Meta campaigns...")
            ads = ask_claude(
                client,
                ADS_SYSTEM,
                f"CLIENT BRIEF:\n{brief}\n\nCreate the paid ads kit now. "
                "Ensure all keywords are relevant and budgets are realistic.",
                max_tokens=12000,
            )
            save("ads_kit.md", ads)

        if mode in ("email", "both"):
            print("✉️ Generating 5-email welcome sequence...")
            emails = ask_claude(
                client,
                EMAIL_SYSTEM,
                f"CLIENT BRIEF:\n{brief}\n\nWrite the 5-email sequence now. "
                "Make sure each email has clear value and calls-to-action.",
                max_tokens=12000,
            )
            save("email_sequence.md", emails)

        print("\n✅ Assets generated successfully!")
        print("💡 Next: Review before launching — you are the quality gate.")
        print("   • Check compliance with local regulations")
        print("   • Verify brand voice consistency")
        print("   • Test email rendering across clients")
        
    except Exception as e:
        logger.error(f"Failed to generate assets: {e}")
        sys.exit(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
