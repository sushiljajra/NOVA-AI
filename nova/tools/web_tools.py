import webbrowser
import warnings

# Suppress the rename warning if duckduckgo_search is used
warnings.filterwarnings("ignore", category=RuntimeWarning, module="duckduckgo_search")

try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS

def search_web(query: str, max_results: int = 5) -> str:
    """
    Searches the live web using DuckDuckGo to find real-time information, news, solutions, or documentation.
    """
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                title = r.get("title", "No Title")
                href = r.get("href", "")
                body = r.get("body", "")
                results.append(f"Title: {title}\nURL: {href}\nSummary: {body}\n")

        if not results:
            return f"No search results found for query: '{query}'"
        return "\n---\n".join(results)
    except Exception as e:
        return f"Error executing web search: {str(e)}"

def open_browser(url: str) -> str:
    """
    Opens a website or URL in the user's default web browser.
    """
    try:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        webbrowser.open(url)
        return f"Opened {url} in your default browser."
    except Exception as e:
        return f"Error opening URL: {str(e)}"

