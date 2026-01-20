import requests
from bs4 import BeautifulSoup
from typing import List
from urllib.parse import urljoin, urlparse, urldefrag
from utils.retry import retry

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )
}

def fetch_website_contents(url: str) -> str:
    def _fetch():
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.content

    try:
        content = retry(_fetch, retries=3)
        soup = BeautifulSoup(content, "html.parser")

        title = soup.title.string.strip() if soup.title else "No title"

        if soup.body:
            for tag in soup.body(["script", "style", "img", "input", "noscript"]):
                tag.decompose()
            text = soup.body.get_text(separator="\n", strip=True)
        else:
            text = ""

        return f"{title}\n\n{text}"

    except Exception as e:
        return f"[WARN] Failed to fetch {url}. Reason: {str(e)}"


def normalize_url(base_url: str, link: str) -> str | None:
    """
    Convert relative URLs to absolute, remove fragments,
    normalize trailing slashes, and drop query params.
    """
    absolute = urljoin(base_url, link)
    absolute, _ = urldefrag(absolute)  # remove #fragment

    parsed = urlparse(absolute)

    if not parsed.scheme.startswith("http"):
        return None

    # Normalize trailing slash
    normalized = parsed._replace(
        query="",  # drop query params
        path=parsed.path.rstrip("/")
    ).geturl()

    return normalized


def fetch_website_links(url: str) -> List[str]:
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        base_domain = urlparse(url).netloc

        normalized_links = set()

        for tag in soup.find_all("a", href=True):
            raw_href = tag["href"]

            if raw_href.startswith("#"):
                continue

            normalized = normalize_url(url, raw_href)
            if not normalized:
                continue

            # Restrict to same domain
            if urlparse(normalized).netloc != base_domain:
                continue

            normalized_links.add(normalized)

        return sorted(normalized_links)

    except Exception:
        return []


