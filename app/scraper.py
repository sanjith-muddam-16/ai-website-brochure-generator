import requests
from bs4 import BeautifulSoup
from typing import List

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )
}

def fetch_website_contents(url: str) -> str:
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.title.string.strip() if soup.title else "No title"

        if soup.body:
            for tag in soup.body(["script", "style", "img", "input", "noscript"]):
                tag.decompose()
            text = soup.body.get_text(separator="\n", strip=True)
        else:
            text = ""

        return f"{title}\n\n{text}"

    except Exception as e:
        return f"Failed to fetch content from {url}. Error: {str(e)}"


def fetch_website_links(url: str) -> List[str]:
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        links = []
        for tag in soup.find_all("a"):
            href = tag.get("href")
            if href and not href.startswith("#"):
                links.append(href)

        return list(set(links))

    except Exception:
        return []

