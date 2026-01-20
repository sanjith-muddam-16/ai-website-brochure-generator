from typing import List, Dict
from collections import defaultdict
from bs4 import BeautifulSoup
from app.scraper import fetch_website_contents, fetch_website_links

SECTION_KEYWORDS = {
    "ABOUT": ["about", "who we are", "company"],
    "PRODUCTS": ["product", "solution", "platform"],
    "FEATURES": ["feature", "capability"],
    "PRICING": ["pricing", "plans"],
    "CAREERS": ["career", "jobs"],
    "CONTACT": ["contact", "reach"],
}

SECTION_ORDER = [
    "ABOUT",
    "PRODUCTS",
    "FEATURES",
    "PRICING",
    "CAREERS",
    "CONTACT",
    "OTHER",
]

SECTION_WEIGHTS = {
    "ABOUT": 2,
    "PRODUCTS": 4,
    "FEATURES": 4,
    "PRICING": 2,
    "CAREERS": 1,
    "CONTACT": 1,
    "OTHER": 1,
}

def allocate_budget(
    sections: dict[str, list[str]],
    max_chars: int
) -> str:
    total_weight = sum(
        SECTION_WEIGHTS.get(section, 1)
        for section in sections
    )

    final_blocks = []

    for section in SECTION_ORDER:
        if section not in sections:
            continue

        content = sections[section]
        weight = SECTION_WEIGHTS.get(section, 1)

        section_budget = int(max_chars * (weight / total_weight))

        joined = "\n".join(content)
        trimmed = joined[:section_budget]

        if trimmed.strip():
            final_blocks.append(f"\n[{section}]\n{trimmed}")

    return "\n".join(final_blocks)

def classify_section(text: str) -> str:
    lower = text.lower()
    for section, keywords in SECTION_KEYWORDS.items():
        if any(k in lower for k in keywords):
            return section
    return "OTHER"


def extract_structured_sections(html: str) -> Dict[str, List[str]]:
    soup = BeautifulSoup(html, "html.parser")
    sections = defaultdict(list)

    for tag in soup.find_all(["h1", "h2", "h3", "p"]):
        text = tag.get_text(strip=True)
        if not text or len(text) < 40:
            continue

        section = classify_section(text)
        sections[section].append(text)

    return sections


def build_full_website_context(url: str, max_links: int, max_chars: int) -> str:
    links = fetch_website_links(url)[:max_links]
    pages = []

    for link in links:
        raw_html = fetch_website_contents(link)
        structured = extract_structured_sections(raw_html)

        page_context = allocate_budget(structured, max_chars)
        pages.append(f"=== PAGE: {link} ===\n{page_context}")

    return "\n\n".join(pages)


