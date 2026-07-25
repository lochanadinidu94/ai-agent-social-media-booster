#!/usr/bin/env python3
"""
Setup script for AI Agency Agents.
Handles environment configuration and dependency installation.
"""
import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Verify Python 3.10+ is installed."""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ required")
        print(f"   You have: {sys.version}")
        sys.exit(1)
    print(f"✓ Python {sys.version.split()[0]}")


def install_dependencies():
    """Install required packages from requirements.txt."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
        print("✓ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Dependency installation failed")
        return False


def setup_env_file():
    """Create .env file from .env.example if needed."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✓ .env file exists")
        return True
    
    if not env_example.exists():
        print("❌ .env.example not found")
        return False
    
    print("\n🔑 Setting up environment...")
    content = env_example.read_text()
    env_file.write_text(content)
    print("✓ Created .env from .env.example")
    
    # Prompt for API key
    print("\n📝 Configure your API key:")
    print("   1. Get an API key: https://console.anthropic.com (Settings → API Keys)")
    print("   2. Edit .env and replace 'sk-ant-your-api-key-here' with your actual key")
    print("   3. Save the file")
    
    return True


def verify_setup():
    """Verify all setup files exist."""
    required_files = [
        "common.py",
        "social_content_agent.py",
        "ads_email_agent.py",
        "seo_audit_agent.py",
        "client_brief.example.md",
        ".env",
        "requirements.txt",
    ]
    
    missing = [f for f in required_files if not Path(f).exists()]
    if missing:
        print(f"⚠️  Missing files: {', '.join(missing)}")
        return False
    
    print("✓ All required files present")
    return True


def main():
    """Run complete setup."""
    print("\n" + "=" * 60)
    print("🚀 AI AGENCY AGENTS - SETUP")
    print("=" * 60)
    
    check_python_version()
    
    if not install_dependencies():
        sys.exit(1)
    
    if not setup_env_file():
        sys.exit(1)
    
    if not verify_setup():
        print("\n⚠️  Setup incomplete. Please verify all files are present.")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ SETUP COMPLETE!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("   1. Edit .env and add your ANTHROPIC_API_KEY")
    print("   2. Copy client_brief.example.md → client_brief.md")
    print("   3. Fill in your client details in client_brief.md")
    print("   4. Run: python main.py [--help]")
    print("\n💡 Or run individual agents:")
    print("   • python seo_audit_agent.py https://example.com")
    print("   • python social_content_agent.py instagram facebook")
    print("   • python ads_email_agent.py")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
