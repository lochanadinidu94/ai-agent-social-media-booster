# 🚀 AI Agency Marketing Agents

Professional AI-powered marketing automation for digital agencies. Generate client deliverables with Claude:
- **SEO Audits** → Technical analysis + 90-day action plans
- **Social Content** → 30-day calendars for Instagram, Facebook, LinkedIn, TikTok
- **Ads + Email** → Google Ads, Meta campaigns, 5-email sequences

Every output is specific to your client, on-brand, and ready to send.

---

## ⚡ Quick Start (~5 minutes)

### 1. Setup (First Time Only)
```bash
python setup.py
```

This will:
- ✓ Verify Python 3.10+
- ✓ Install dependencies
- ✓ Create `.env` file
- ✓ Guide you through API key setup

### 2. Configure Your API Key
1. Get a free API key: https://console.anthropic.com (Settings → API Keys)
2. Edit `.env` and paste your key:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

### 3. Prepare Client Brief
```bash
cp client_brief.example.md client_brief.md
# Edit client_brief.md with your client details
```

### 4. Run Agents

**Run everything for a client:**
```bash
python main.py --all https://clientsite.com.au
```

**Run individual agents:**
```bash
# SEO audit
python seo_audit_agent.py https://clientsite.com.au

# Social content (choose platforms)
python social_content_agent.py instagram facebook linkedin

# Ads + Email
python ads_email_agent.py          # both
python ads_email_agent.py ads      # ads only
python ads_email_agent.py email    # email only
```

**Orchestrator examples:**
```bash
python main.py --all https://example.com
python main.py --seo https://example.com
python main.py --social instagram linkedin
python main.py --ads
python main.py --email
```

---

## 📁 Project Structure

```
marketingAgents/
├── main.py                        # Master orchestrator
├── setup.py                       # One-time setup
├── common.py                      # Shared utilities & error handling
├── seo_audit_agent.py             # Website crawl → audit
├── social_content_agent.py        # Content calendar generator
├── ads_email_agent.py             # Ads + email sequence generator
├── client_brief.example.md        # Template (copy & customize)
├── client_brief.md                # Your current client (git-ignored)
├── requirements.txt               # Python dependencies
├── .env.example                   # Template (git-safe)
├── .env                           # Your secrets (git-ignored)
└── deliverables/                  # Outputs go here (dated files)
```

---

## 💰 Cost & Performance

| Agent | Time | Cost |
|-------|------|------|
| SEO Audit | 1-2 min | ~$0.08-0.15 |
| Social Calendar | 1 min | ~$0.05-0.10 |
| Ads + Email | 1-2 min | ~$0.08-0.15 |
| **Full Set** | **~5 min** | **<$0.30** |

Uses `claude-3-5-sonnet-20241022` by default. Change via `.env`:
```
AGENT_MODEL=claude-3-opus-20250219  # Higher quality, higher cost
AGENT_MODEL=claude-3-haiku-20250307 # Faster, lower cost
```

---

## 🔑 Configuration

**.env options:**
```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...

# Optional
AGENT_MODEL=claude-3-5-sonnet-20241022    # default
LOG_LEVEL=INFO                             # DEBUG, INFO, WARNING, ERROR
MAX_RETRIES=3                              # API retry attempts
REQUEST_TIMEOUT=30                         # seconds
```

---

## 📊 What Each Agent Does

### SEO Audit Agent
- Crawls up to 10 pages of your client's website
- Checks: titles, meta descriptions, H1/H2 structure, images, mobile-friendliness, schema markup
- Produces: executive summary, technical findings, on-page analysis, keyword opportunities, 90-day plan
- **Output:** `seo_audit.md`

### Social Content Agent
- Generates 30-day content calendar
- Includes: captions, hashtags, visual direction, best posting times, story/reel ideas
- Platforms: Instagram, Facebook, LinkedIn, TikTok, Twitter, YouTube
- Content mix: 40% value, 25% social proof, 20% engagement, 15% promo
- **Output:** `social_calendar.md`

### Ads & Email Agent
- **Ads:** Google Search campaigns (keywords, headlines, descriptions) + Meta campaigns (audiences, ad variants, creative briefs)
- **Email:** 5-email welcome sequence (subject, preview, body, CTA, timing)
- Includes: landing page recs, budget suggestions, compliance notes, A/B test tips
- **Outputs:** `ads_kit.md`, `email_sequence.md`

---

## ✅ Quality Assurance

**You are the quality gate.** Every output requires:
1. ✓ Brand voice consistency
2. ✓ Compliance with local regulations (see client brief)
3. ✓ Factual accuracy (agents use data you provide)
4. ✓ Realistic recommendations (no fake stats)

**Review checklist before sending to client:**
- [ ] Output matches client brief (business, audience, goals, brand voice)
- [ ] All facts/recommendations backed by actual crawl data (SEO) or brief
- [ ] Compliance disclaimers included (especially for regulated industries)
- [ ] No generic placeholder text
- [ ] Formatting works in your delivery tool (Docs, email, etc.)

---

## 🚨 Troubleshooting

### API Key Issues
```
❌ Set your API key first: export ANTHROPIC_API_KEY=sk-ant-...
```
- Get key: https://console.anthropic.com
- Edit `.env` file and add your key
- Verify key is never committed to git (check `.env` is in `.gitignore`)

### Client Brief Not Found
```
❌ No client_brief.md found
```
- Copy template: `cp client_brief.example.md client_brief.md`
- Fill in your client details
- Run again

### Rate Limit (429)
- Too many API calls too quickly
- Agent will auto-retry with exponential backoff
- Wait a minute then try again

### Timeout (>30s)
- Network issue or very large website
- Check your connection
- Try again with smaller website or fewer pages

### Empty/Generic Output
- Client brief is too vague
- Fill in more specific details (niche, location, competitor analysis)
- Agents produce specific output based on your input

---

## 📋 Client Brief Template

Fill this in for each client (copy from `client_brief.example.md`):

```markdown
# Client Brief

## Business
- Name: [Business name]
- Website: [URL]
- Location: [City, State]
- What they sell: [Product/service description]

## Audience
- Who: [Target demographic]
- Pain points: [Problems they solve]

## Goals
- Primary: [Main objective, with numbers]
- Secondary: [Secondary goals]

## Brand voice
- [Description of tone/style]

## Competitors
- [List 3 competitors]

## Constraints / notes
- [Compliance requirements, platform restrictions, etc.]
```

---

## 🔄 Per-Client Workflow

1. **Create client folder:** `mkdir client-name && cd client-name`
2. **Copy template:** `cp ../client_brief.example.md client_brief.md`
3. **Fill in details:** Edit `client_brief.md`
4. **Run agents:** `python ../main.py --all https://their-website.com`
5. **Review outputs:** Check `deliverables/` files
6. **Customize:** Edit any generated Markdown before sending
7. **Deliver:** Send to client as-is or import into your design tool

---

## 🎯 Next Steps to Build

- **Reporting agent:** Pull GA4/Search Console data, generate monthly reports
- **Blog writer:** Feed SEO audit keywords → generate draft articles
- **Landing page generator:** Create high-converting page copy
- **Competitor tracker:** Monitor competitor websites/social
- **Automation:** Trigger via Zapier/Make from Tally intake forms
- **Dashboard:** Build web UI for non-technical agency staff

---

## 📝 License & Usage

This is a starter project for digital agencies. Use it to:
- Generate deliverables for clients
- Train team members on AI-assisted marketing
- Build custom agents for your workflow

Outputs are your responsibility. Always:
- ✓ Review everything before client delivery
- ✓ Verify facts & recommendations
- ✓ Include compliance disclaimers where needed
- ✓ Customize to client needs

---

## 🆘 Support

- **Python issues?** Make sure you have Python 3.10+ installed
- **API errors?** Check your API key at console.anthropic.com
- **Something broken?** Check the logs in `deliverables/*.log`

---

Built with ❤️ for digital agencies using Claude + Python.

# ai-agent-social-media-booster
