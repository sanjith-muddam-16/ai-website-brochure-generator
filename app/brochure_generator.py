from openai import OpenAI
from app.context_builder import build_full_website_context
from utils import retry

client = OpenAI()

def create_chat_completion_with_retry(**kwargs):
    return retry(lambda:client.chat.completions.create(**kwargs),
                 retries = 3,
                 backoff = 2.0)

def generate_brochure_stream(url, max_links, max_chars, category):
    context = build_full_website_context(url, max_links)[:max_chars]

    system_prompt = "Professional brochure generation prompt..."

    stream = create_chat_completion_with_retry(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context},
        ],
        stream=True,
    )

    partial = ""
    try:
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                partial = partial + delta
                yield partial
    except Exception:
        yield partial + "\n\n Generation Interrupted due to temporary error"
