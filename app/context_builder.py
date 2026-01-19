from app.scraper import fetch_website_contents
from app.link_selector import get_relevant_brochure_links

def build_full_website_context(url: str, max_links: int) -> str:
    main_content = fetch_website_contents(url)
    links_data = get_relevant_brochure_links(url, max_links)

    blocks = []
    for item in links_data.get("links", []):
        text = fetch_website_contents(item["url"])
        blocks.append(f"\n--- {item['type'].upper()} PAGE ---\n{text}")

    return main_content + "\n".join(blocks)
