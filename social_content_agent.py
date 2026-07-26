"""Social Content Agent.

Generates a 30-day social media content calendar from the client brief:
post copy, hashtags, image/video direction, and platform variants.

Usage:
    python social_content_agent.py                     # Instagram + Facebook
    python social_content_agent.py instagram linkedin  # choose platforms
"""
import logging
import sys
from typing import List

from common import ask_claude, get_client, load_brief, save

logger = logging.getLogger(__name__)

SYSTEM = """You are the head of social at a digital agency. You create content
calendars that a real business can post without embarrassment: specific to their
business and suburb, on brand voice, varied, and designed for engagement — not
generic filler like "Happy Monday!".

Output a Markdown table with columns:
Day | Platform | Post type | Caption (full, ready to post) | Hashtags | Visual direction

Rules:
- Content mix: ~40% value/education, 25% social proof & behind-the-scenes,
  20% engagement (questions, polls), 15% promotional.
- Captions written in full, in the brand voice from the brief, with hooks in
  the first line. Platform-appropriate length (short for FB, longer ok for IG/LinkedIn).
- Hashtags: mix of local, niche and broad; 5-10 for Instagram, 3-5 elsewhere.
- Visual direction must be shootable by the owner on a phone, or a simple
  Canva graphic — describe it concretely.
- Respect all constraints in the brief.

After the table, add a short "Posting notes" section: best times, and 3 story/reel
ideas for the month. Include estimated engagement targets based on industry benchmarks."""


def validate_platforms(platforms: List[str]) -> List[str]:
    """Validate and normalize platform names."""
    valid = {"instagram", "facebook", "linkedin", "tiktok", "twitter", "youtube"}
    normalized = [p.lower().strip() for p in platforms]
    invalid = [p for p in normalized if p not in valid]
    
    if invalid:
        logger.warning(f"Skipping invalid platforms: {invalid}")
        normalized = [p for p in normalized if p in valid]
    
    if not normalized:
        logger.info("No valid platforms specified, defaulting to instagram, facebook")
        normalized = ["instagram", "facebook"]
    
    return sorted(normalized)


def main():
    """Generate social content calendar."""
    platforms = sys.argv[1:] or ["instagram", "facebook"]
    platforms = validate_platforms(platforms)
    
    print(f"\n📱 Social Content Calendar Generator")
    print(f"{'=' * 50}")
    print(f"Platforms: {', '.join(platforms)}\n")
    
    try:
        brief = load_brief()
        client = get_client()

        print(f"Generating 30-day calendar...")
        calendar = ask_claude(
            client,
            SYSTEM,
            f"CLIENT BRIEF:\n{brief}\n\nPlatforms: {', '.join(platforms)}.\n"
            "Create the 30-day content calendar now. Ensure it's specific, on-brand, "
            "and ready to post.",
            max_tokens=4000,
        )
        save("social_calendar.md", calendar)
        print("\n✅ Calendar ready for review!")
        print("💡 Next: Review, tweak any off-brand content, then load into Buffer/Publer/Meta Business Suite.")
        
    except Exception as e:
        logger.error(f"Failed to generate calendar: {e}")
        sys.exit(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
