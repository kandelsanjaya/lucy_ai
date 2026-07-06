import streamlit as st
from utils.icons import icon
from utils.helpers import chat_completion


def render(user):
    st.markdown(f"<div class='sub-heading' style='font-size:1.2rem;'>{icon('websearch', 20)} Web Search</div>",
                unsafe_allow_html=True)
    st.caption("Search the live web and get a summarized, cited answer. "
               "Plug in a search API key (e.g. Tavily, SerpAPI, Bing) in `utils/helpers.py` for real results.")

    query = st.text_input("Search the web", placeholder="e.g. Latest developments in quantum computing")
    if st.button("🔍 Search", type="primary") and query:
        results = _mock_or_real_search(query)
        if results:
            for r in results:
                st.markdown(
                    f"""<div class="glass-card" style="margin-bottom:10px;">
                            <a href="{r['url']}" style="color:#818cf8;font-weight:700;text-decoration:none;">{r['title']}</a>
                            <div class="small muted" style="margin-top:4px;">{r['snippet']}</div>
                        </div>""",
                    unsafe_allow_html=True,
                )
            summary = chat_completion([
                {"role": "system", "content": "Summarize these web search snippets into a helpful, concise answer."},
                {"role": "user", "content": str(results)},
            ])
            st.markdown(f"<div class='sub-heading'>{icon('sparkle', 16)} Summary</div>", unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bubble-bot">{summary}</div>', unsafe_allow_html=True)


def _mock_or_real_search(query: str):
    api_key = __import__("os").environ.get("TAVILY_API_KEY")
    if api_key:
        try:
            import requests
            resp = requests.post("https://api.tavily.com/search",
                                  json={"api_key": api_key, "query": query, "max_results": 5}, timeout=10)
            data = resp.json()
            return [{"title": r["title"], "url": r["url"], "snippet": r.get("content", "")[:220]}
                    for r in data.get("results", [])]
        except Exception:
            pass
    # Fallback placeholder so the UI still demonstrates the flow
    return [
        {"title": f"About: {query}", "url": "https://example.com",
         "snippet": "Connect a search API (TAVILY_API_KEY) to see live results here."}
    ]
