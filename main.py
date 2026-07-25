#!/usr/bin/env python3
"""
Main Orchestrator for AI Agency Agents.

Run one or more agents from a single command:
    python main.py --all              # Run all agents
    python main.py --seo https://example.com
    python main.py --social instagram
    python main.py --ads              # Generate ads only
    python main.py --email            # Generate email only
"""
import argparse
import logging
import subprocess
import sys
from pathlib import Path
from typing import Optional

from common import get_client, load_brief

logger = logging.getLogger(__name__)


def run_command(cmd: list[str]) -> bool:
    """Run a subprocess command and return success status."""
    try:
        logger.info(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e}")
        return False
    except FileNotFoundError:
        logger.error(f"Command not found: {cmd[0]}")
        return False


def run_seo(url: str) -> bool:
    """Run SEO audit agent."""
    print(f"\n{'='*60}")
    print("📊 SEO AUDIT AGENT")
    print(f"{'='*60}")
    return run_command([sys.executable, "seo_audit_agent.py", url])


def run_social(platforms: Optional[list[str]] = None) -> bool:
    """Run social content agent."""
    print(f"\n{'='*60}")
    print("📱 SOCIAL CONTENT AGENT")
    print(f"{'='*60}")
    cmd = [sys.executable, "social_content_agent.py"]
    if platforms:
        cmd.extend(platforms)
    return run_command(cmd)


def run_ads(mode: str = "both") -> bool:
    """Run ads & email agent."""
    print(f"\n{'='*60}")
    print("🎯 ADS & EMAIL AGENT")
    print(f"{'='*60}")
    return run_command([sys.executable, "ads_email_agent.py", mode])


def run_all(url: str, social_platforms: Optional[list[str]] = None) -> bool:
    """Run all agents."""
    print(f"\n{'='*60}")
    print("🚀 RUNNING ALL AGENTS")
    print(f"{'='*60}")
    
    social_platforms = social_platforms or ["instagram", "facebook"]
    
    try:
        brief = load_brief()
        client = get_client()
        print("✓ Configuration verified\n")
    except SystemExit:
        return False
    
    results = {
        "SEO Audit": run_seo(url),
        "Social Content": run_social(social_platforms),
        "Ads & Email": run_ads("both"),
    }
    
    print(f"\n{'='*60}")
    print("📊 RESULTS SUMMARY")
    print(f"{'='*60}")
    for agent_name, success in results.items():
        status = "✓" if success else "✗"
        print(f"{status} {agent_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✅ All agents completed successfully!")
        print(f"📁 Check deliverables/ directory for outputs")
    else:
        print("\n⚠️  Some agents failed. Check logs above.")
    
    return all_passed


def main():
    parser = argparse.ArgumentParser(
        description="AI Agency Marketing Agents Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --all https://example.com
  python main.py --seo https://example.com
  python main.py --social instagram linkedin
  python main.py --ads
  python main.py --email
        """
    )
    
    parser.add_argument(
        "url",
        nargs="?",
        default=None,
        help="Website URL (required for --all and --seo)"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all agents"
    )
    
    parser.add_argument(
        "--seo",
        action="store_true",
        help="Run SEO audit agent"
    )
    
    parser.add_argument(
        "--social",
        nargs="*",
        help="Run social content agent (optionally specify platforms)"
    )
    
    parser.add_argument(
        "--ads",
        action="store_true",
        help="Run ads only"
    )
    
    parser.add_argument(
        "--email",
        action="store_true",
        help="Run email only"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)
    
    # Verify client_brief.md exists
    if not Path("client_brief.md").exists():
        print("❌ client_brief.md not found")
        print("   Copy client_brief.example.md → client_brief.md and fill it in")
        sys.exit(1)
    
    # Route to appropriate agent(s)
    if args.all:
        if not args.url:
            print("❌ URL required for --all mode")
            print("   Usage: python main.py --all https://example.com")
            sys.exit(1)
        success = run_all(args.url)
    
    elif args.seo:
        if not args.url:
            print("❌ URL required for --seo")
            print("   Usage: python main.py --seo https://example.com")
            sys.exit(1)
        success = run_seo(args.url)
    
    elif args.social is not None:
        platforms = args.social if args.social else ["instagram", "facebook"]
        success = run_social(platforms)
    
    elif args.ads:
        success = run_ads("ads")
    
    elif args.email:
        success = run_ads("email")
    
    else:
        print("❌ No agent specified")
        print("\nUsage: python main.py [--all | --seo | --social | --ads | --email] [URL]")
        print("\nExamples:")
        print("  python main.py --all https://example.com")
        print("  python main.py --seo https://example.com")
        print("  python main.py --social instagram facebook")
        print("  python main.py --ads")
        parser.print_help()
        sys.exit(1)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
