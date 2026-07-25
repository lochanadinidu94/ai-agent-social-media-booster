#!/bin/bash
# Quick Start Script for AI Marketing Agents
# Run this after getting your API key

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  🚀 AI MARKETING AGENTS - QUICK START                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
echo "🔍 Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Install from https://www.python.org/downloads/"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION"

# Setup
echo ""
echo "📦 Running setup..."
python3 setup.py

# Create client brief
echo ""
echo "📋 Setting up client brief..."
if [ ! -f "client_brief.md" ]; then
    cp client_brief.example.md client_brief.md
    echo "✓ Created client_brief.md"
else
    echo "✓ client_brief.md already exists"
fi

# Check .env
echo ""
echo "🔑 Checking API configuration..."
if grep -q "sk-ant-your-api-key-here" .env; then
    echo "❌ API key not set in .env"
    echo ""
    echo "Steps to fix:"
    echo "  1. Go to: https://console.anthropic.com/api/keys"
    echo "  2. Create or copy your API key"
    echo "  3. Edit .env and replace 'sk-ant-your-api-key-here' with your key"
    echo "  4. Run this script again"
    exit 1
else
    echo "✓ API key configured"
fi

# Test
echo ""
echo "🧪 Testing configuration..."
python3 -c "from common import get_client; client = get_client(); print('✓ API client initialized')" || {
    echo "❌ API connection failed"
    echo "   Check your API key in .env"
    exit 1
}

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  ✅ READY TO GO!                                              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Try these commands:"
echo ""
echo "  # Run all agents for ROLLiN' Insurance"
echo "  python3 main.py --all https://rollininsurance.com.au"
echo ""
echo "  # Run individual agents"
echo "  python3 seo_audit_agent.py https://rollininsurance.com.au"
echo "  python3 social_content_agent.py instagram facebook"
echo "  python3 ads_email_agent.py"
echo ""
echo "Output files are saved to: deliverables/"
echo ""
