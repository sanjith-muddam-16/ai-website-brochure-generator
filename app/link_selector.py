import json
from typing import Dict
from openai import OpenAI
from app.scraper import fetch_website_links

client = OpenAI()

def get_relevant_brochure_links(url: str, max_links: int) -> Dict:
    system_prompt = """
You are given website links. Select links useful for a company brochure such as:
- About
- Product / Services
- Careers
- Contact
- Case Studies

Return ONLY valid JSON.
"""

    links = fetch_website_links(url)[:max_links]

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "\n".join(links)},
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)
