"""SEO Audit Agent.

Crawls up to 10 pages of a website, then produces a client-ready SEO audit:
technical issues, on-page findings, keyword opportunities, and a 90-day plan.

Usage:
    python seo_audit_agent.py https://clientsite.com.au
"""
import logging
import re
import sys
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from common import ask_claude, get_client, load_brief, save, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

MAX_PAGES = 10
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AIAuditAgent/2.0)"}

SYSTEM = """You are a senior technical SEO consultant at a digital agency.
You write audits that are specific, prioritized, and actionable — never generic.
Every finding must reference actual evidence from the crawl data provided.
Write in clear Australian English. Format as Markdown with these sections:
1. Executive summary (3-4 sentences, plain language for the business owner)
2. Technical SEO findings (prioritized: critical / important / minor)
3. On-page findings per page (titles, metas, headings, content gaps)
4. Keyword opportunities (based on the business, location and audience in the brief)
5. 90-day action plan (week-by-week, what and why)
Do not invent data you were not given. If something could not be checked
(e.g. page speed, backlinks), list it under "Requires further tooling".
Include compliance notes and mobile-friendly recommendations."""


def crawl_page(url: str) -> Dict[str, Any]:
    """
    Crawl a single page and extract SEO-relevant data.
    
    Args:
        url: Full URL to crawl
        
    Returns:
        Dictionary containing page metadata and SEO data
    """
    try:
        logger.debug(f"Crawling: {url}")
        r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
    except requests.Timeout:
        logger.warning(f"Timeout: {url}")
        return {"url": url, "error": "Timeout (>30s)"}
    except requests.HTTPError as e:
        logger.warning(f"HTTP error: {url} - {e.response.status_code}")
        return {"url": url, "error": f"HTTP {e.response.status_code}", "status": e.response.status_code}
    except requests.RequestException as e:
        logger.warning(f"Request error: {url} - {e}")
        return {"url": url, "error": str(e)}
    
    try:
        soup = BeautifulSoup(r.text, "html.parser")
        
        title = soup.title.string.strip() if soup.title and soup.title.string else None
        desc = soup.find("meta", attrs={"name": "description"})
        imgs = soup.find_all("img")
        text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
        
        # Check for mobile-friendly meta tag
        viewport = soup.find("meta", attrs={"name": "viewport"})
        
        # Check for structured data
        has_schema = bool(soup.find("script", attrs={"type": "application/ld+json"}))
        
        internal_links = set()
        for a in soup.find_all("a", href=True):
            link = urljoin(url, a["href"])
            if urlparse(link).netloc == urlparse(url).netloc:
                internal_links.add(link)
        
        page_data = {
            "url": url,
            "status": r.status_code,
            "title": title,
            "title_length": len(title) if title else 0,
            "meta_description": desc.get("content", "").strip() if desc else None,
            "meta_description_length": len(desc.get("content", "")) if desc else 0,
            "h1": [h.get_text(strip=True) for h in soup.find_all("h1")],
            "h2": [h.get_text(strip=True) for h in soup.find_all("h2")][:10],
            "word_count": len(text.split()),
            "images_total": len(imgs),
            "images_missing_alt": sum(1 for i in imgs if not i.get("alt")),
            "canonical": (soup.find("link", rel="canonical") or {}).get("href"),
            "has_viewport": bool(viewport),
            "has_schema": has_schema,
            "content_sample": text[:1500],
            "internal_links": len(internal_links),
        }
        
        logger.info(f"✓ Crawled: {url} ({r.status_code}, {page_data['word_count']} words)")
        return page_data
        
    except Exception as e:
        logger.error(f"Parse error for {url}: {e}")
        return {"url": url, "error": f"Parse error: {str(e)}"}


def crawl_site(start_url: str) -> List[Dict[str, Any]]:
    """
    Crawl a website up to MAX_PAGES pages.
    
    Args:
        start_url: Starting URL for crawl
        
    Returns:
        List of page data dictionaries
    """
    seen = set()
    queue = [start_url]
    pages = []
    
    print(f"🔍 Crawling site (max {MAX_PAGES} pages)...")
    
    while queue and len(pages) < MAX_PAGES:
        url = queue.pop(0).split("#")[0].rstrip("/")
        
        if url in seen:
            continue
        
        seen.add(url)
        page = crawl_page(url)
        pages.append(page)
        
        # Only queue more links if crawl was successful
        if "error" not in page:
            for link in page.get("internal_links", []):
                clean_link = link.split("#")[0].rstrip("/")
                if clean_link not in seen and len(pages) < MAX_PAGES:
                    queue.append(clean_link)
    
    logger.info(f"Crawl complete: {len(pages)} pages")
    return pages


def validate_url(url: str) -> str:
    """Validate and normalize URL."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        urlparse(url)
        return url
    except Exception:
        raise ValueError(f"Invalid URL: {url}")


def main():
    """Generate SEO audit."""
    if len(sys.argv) < 2:
        print("\n📊 SEO Audit Generator")
        print(f"{'=' * 50}")
        print("Usage: python seo_audit_agent.py https://clientsite.com.au\n")
        sys.exit(1)
    
    url = sys.argv[1]
    
    print(f"\n📊 SEO Audit Generator")
    print(f"{'=' * 50}")
    
    try:
        url = validate_url(url)
        print(f"Target: {url}\n")
        
        brief = load_brief()
        client = get_client()

        pages = crawl_site(url)
        
        if not pages:
            sys.exit("❌ No pages crawled successfully")
        
        print("\n🤖 Analyzing with Claude...")
        audit = ask_claude(
            client,
            SYSTEM,
            f"CLIENT BRIEF:\n{brief}\n\nCRAWL DATA ({len(pages)} pages):\n{pages}",
            max_tokens=16000,
        )
        save("seo_audit.md", audit)
        print("\n✅ Audit complete!")
        print("💡 Next: Review, add strategy notes, then send to client.")
        
    except ValueError as e:
        logger.error(f"Invalid URL: {e}")
        sys.exit(f"❌ Invalid URL: {e}")
    except Exception as e:
        logger.error(f"Audit failed: {e}")
        sys.exit(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
