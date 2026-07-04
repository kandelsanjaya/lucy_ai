"""
KANDEL AI - Web Search Fallback
Designed by Kandel Sanjaya
"""
import requests
from config.settings import settings


def web_search(query: str, max_results: int = 5):
    """Returns list of {title, url, snippet, best}. Tries Tavily first if key present,
    otherwise falls back to DuckDuckGo (no API key needed). The first result returned
    is treated as the best/most relevant link."""
    results = []

    if settings.TAVILY_API_KEY:
        try:
            r = requests.post(
                "https://api.tavily.com/search",
                json={"api_key": settings.TAVILY_API_KEY, "query": query, "max_results": max_results},
                timeout=10,
            )
            data = r.json()
            results = [
                {"title": item.get("title", ""), "url": item.get("url", ""), "snippet": item.get("content", "")}
                for item in data.get("results", [])
            ]
        except Exception:
            results = []  # fall through to DuckDuckGo

    if not results:
        try:
            from ddgs import DDGS
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=max_results):
                    results.append({"title": r.get("title", ""), "url": r.get("href", ""), "snippet": r.get("body", "")})
        except Exception as e:
            return [{"title": "Web search unavailable", "url": "", "snippet": str(e), "best": True}]

    for i, r in enumerate(results):
        r["best"] = (i == 0)
    return results
