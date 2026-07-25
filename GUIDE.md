# 🎯 Enhanced Features & Best Practices Guide

## Table of Contents
1. [Configuration Management](#configuration-management)
2. [Error Handling & Recovery](#error-handling--recovery)
3. [Logging & Debugging](#logging--debugging)
4. [Performance & Cost](#performance--cost)
5. [Security](#security)
6. [Quality Assurance](#quality-assurance)

---

## Configuration Management

### Environment Variables

All configuration is now managed through `.env` file:

```env
# REQUIRED
ANTHROPIC_API_KEY=sk-ant-...

# OPTIONAL
AGENT_MODEL=claude-3-5-sonnet-20241022
LOG_LEVEL=INFO
MAX_RETRIES=3
REQUEST_TIMEOUT=30
```

### Model Selection

Choose the best model for your use case:

| Model | Speed | Quality | Cost | Best For |
|-------|-------|---------|------|----------|
| `claude-3-5-sonnet-20241022` | Fast | Excellent | $ | Most use cases (default) |
| `claude-3-opus-20250219` | Slower | Best | $$ | Complex analysis, premium output |
| `claude-3-haiku-20250307` | Fastest | Good | $ | Quick drafts, high volume |

```bash
# Use a different model
export AGENT_MODEL=claude-3-opus-20250219
python3 main.py --all https://example.com
```

### Logging Levels

```bash
# DEBUG - Detailed information for troubleshooting
export LOG_LEVEL=DEBUG
python3 social_content_agent.py instagram

# INFO - Normal operation (default)
export LOG_LEVEL=INFO
python3 social_content_agent.py instagram

# WARNING - Only issues and warnings
export LOG_LEVEL=WARNING
python3 social_content_agent.py instagram

# ERROR - Only critical errors
export LOG_LEVEL=ERROR
python3 social_content_agent.py instagram
```

### Custom Retry & Timeout

```bash
# More retries for unreliable networks
export MAX_RETRIES=5

# Longer timeout for large websites
export REQUEST_TIMEOUT=60

python3 seo_audit_agent.py https://large-site.com
```

---

## Error Handling & Recovery

### Automatic Recovery

The system now automatically handles:

✓ **Rate limits (429):** Auto-retries with exponential backoff  
✓ **Network timeouts:** Retries after delay  
✓ **Temporary API errors:** Retries with backoff  
✓ **Invalid client brief:** Clear instructions provided  
✓ **Invalid URLs:** Validation before crawl  
✓ **Missing files:** Detailed guidance  

### Manual Recovery

#### API Key Invalid
```
❌ API error (attempt 1/3): Error code: 401 - API key is invalid

Steps to fix:
1. Go to https://console.anthropic.com/api/keys
2. Create a new API key
3. Edit .env and update ANTHROPIC_API_KEY
4. Try again
```

#### Client Brief Missing
```
❌ No client_brief.md found

Steps to fix:
1. cp client_brief.example.md client_brief.md
2. Edit client_brief.md with your client details
3. Try again
```

#### Website Timeout
```
❌ Timeout (>30s) - increase timeout:
export REQUEST_TIMEOUT=60
python3 seo_audit_agent.py https://example.com
```

---

## Logging & Debugging

### Enable Debug Mode

```bash
# See detailed logs
export LOG_LEVEL=DEBUG
python3 social_content_agent.py instagram

# Output includes:
# - API request/response details
# - Configuration loaded
# - Function entry/exit points
# - Variable states
```

### Save Logs to File

```bash
# Capture all output
python3 social_content_agent.py instagram > run.log 2>&1

# View logs
cat run.log | grep ERROR
```

### Common Log Messages

| Message | Meaning | Action |
|---------|---------|--------|
| `✓ Loaded client brief` | Config OK | None - continue |
| `✓ API call successful` | API working | None - continue |
| `⚠️ Rate limited` | Too many requests | Agent retries automatically |
| `❌ API error` | API issue | Check your key or try again |
| `✗ Crawled: 403` | Page forbidden | Check URL permissions |
| `⚠️ Invalid platforms` | Bad platform name | Check spelling |

---

## Performance & Cost

### Typical Performance

```
SEO Audit (10 pages):  1-2 min  → $0.08-0.15
Social Calendar:        1 min   → $0.05-0.10
Ads + Email Kit:        1-2 min → $0.08-0.15
─────────────────────────────────────
FULL SET:              ~5 min   → <$0.30
```

### Optimize for Speed

```bash
# Use faster model
export AGENT_MODEL=claude-3-haiku-20250307
python3 main.py --all https://example.com
# ~3 min, ~$0.10 cost
```

### Optimize for Quality

```bash
# Use better model
export AGENT_MODEL=claude-3-opus-20250219
python3 main.py --all https://example.com
# ~8 min, ~$0.80 cost
```

### Monitor Costs

1. Go to https://console.anthropic.com/dashboard
2. Check "Usage" section
3. See cost breakdown by model

**Billing:** Charged per 1,000 tokens
- Input: $3 per 1M tokens (Sonnet)
- Output: $15 per 1M tokens (Sonnet)

---

## Security

### API Key Protection

✅ **Good Practice:**
```bash
# Use .env file (git-ignored)
ANTHROPIC_API_KEY=sk-ant-...

# Load from environment
export ANTHROPIC_API_KEY=sk-ant-...

# Use in CI/CD secrets
# (GitHub Actions, GitLab CI, etc.)
```

❌ **Bad Practice:**
```bash
# Never in code
api_key = "sk-ant-..."

# Never in git
git add .env

# Never shared
"Here's my key: sk-ant-..."
```

### File Permissions

```bash
# Restrict .env to owner only
chmod 600 .env

# Verify
ls -l .env
# Should show: -rw-------
```

### Key Rotation

Do this periodically:

1. Generate new key at console.anthropic.com
2. Update `.env` with new key
3. Delete old key from dashboard
4. Test with one agent
5. Proceed normally

### If Key is Compromised

**IMMEDIATELY:**
1. Delete key from console.anthropic.com (prevents charges)
2. Generate new key
3. Update `.env`
4. Test one agent
5. Continue normally

---

## Quality Assurance

### Pre-Delivery Checklist

Before sending outputs to clients:

**Content Quality**
- [ ] Matches client brief (business, audience, goals)
- [ ] Brand voice is consistent
- [ ] No generic filler text
- [ ] All facts are specific to client
- [ ] Recommendations are realistic

**Technical Quality**
- [ ] Formatting is clean (proper Markdown)
- [ ] Links work (for URLs)
- [ ] Tables render correctly
- [ ] No encoding issues
- [ ] File saves successfully

**Compliance**
- [ ] Local regulations mentioned (AU, US, EU, etc.)
- [ ] Required disclaimers included (for financial, health, etc.)
- [ ] Privacy policy links present
- [ ] No false claims or guarantees
- [ ] Terms of service acknowledged

**Process Quality**
- [ ] You reviewed it personally
- [ ] Client brief was accurate
- [ ] You didn't change facts
- [ ] Outputs are reproducible
- [ ] You understand everything in it

### Output Validation

```bash
# Check SEO audit quality
grep -i "critical\|important" deliverables/*seo*.md

# Check for generic text
grep -i "happy\|easy\|simple\|just" deliverables/*social*.md

# Check compliance
grep -i "disclaimer\|restricted\|warning" deliverables/*ads*.md
```

### Client Feedback Loop

1. Send outputs to client
2. Collect feedback
3. Note what worked and what didn't
4. Update client_brief template if needed
5. Improve next time

---

## Troubleshooting Flowchart

```
Something's wrong
    ↓
Check error message
    ├→ "API key is invalid" 
    │    └→ Regenerate key at console.anthropic.com
    ├→ "client_brief.md not found"
    │    └→ cp client_brief.example.md client_brief.md
    ├→ "Rate limited"
    │    └→ Wait a minute, then try again
    ├→ "Timeout"
    │    └→ export REQUEST_TIMEOUT=60
    ├→ "Invalid URL"
    │    └→ Check URL format (must start with http:// or https://)
    └→ Something else?
         └→ Run with DEBUG logging:
            export LOG_LEVEL=DEBUG
            python3 [agent] [args]
```

---

## Advanced Features

### Streaming Output (Planned)

```python
# Future: Show Claude thinking in real-time
for chunk in client.messages.stream(...):
    print(chunk.delta.text, end="", flush=True)
```

### Caching (Planned)

```python
# Cache brief for faster runs
brief = load_brief()
cached_brief = cache.set("brief", brief, ttl=3600)
```

### Parallel Execution (Planned)

```python
# Run all agents in parallel instead of sequential
results = asyncio.gather(
    run_seo(),
    run_social(),
    run_ads_email(),
)
```

---

## Tips & Tricks

### Quick Test Run

```bash
# Test without real data
python3 -c "from common import get_client; print(get_client())"
```

### Dry Run (Preview without saving)

```python
# In any agent, modify to not save:
calendar = ask_claude(...)
print(calendar)  # Instead of save(...)
```

### Batch Processing

```bash
# Create multiple client folders
mkdir -p clients/{client-1,client-2,client-3}
cd clients/client-1
cp ../../client_brief.example.md client_brief.md
# ... edit and run
```

### Keep Delivery Notes

```bash
# Save your notes with deliverables
echo "Status: Reviewed, ready for client
Date: 2025-01-15
Changes: Updated social captions for tone
Reviewed by: John Doe" > deliverables/NOTES.txt
```

---

## Getting Help

1. **Check logs:** `export LOG_LEVEL=DEBUG` to see what's happening
2. **Read error message:** It usually tells you exactly what's wrong
3. **Check configuration:** Verify `.env` is set correctly
4. **Test individually:** Run one agent at a time to isolate issues
5. **Contact support:** https://support.anthropic.com

---

Remember: **You are the quality gate.** Review everything before it reaches a client. The system is powerful but not perfect—your expertise makes it premium.
