from openai import OpenAI
from app.context_builder import build_full_website_context

client = OpenAI()

def generate_brochure_stream(url, max_links, max_chars, category):
    context = build_full_website_context(url, max_links)[:max_chars]

    system_prompt = "Professional brochure generation prompt..."

    stream = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context},
        ],
        stream=True,
    )

    output = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            output += delta
            yield output
