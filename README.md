# ai-website-brochure-generator

End-to-end LLM application that scrapes websites, semantically selects brochure-relevant pages, builds structured context, and streams marketing-ready brochure content via a Gradio UI. Designed for incremental upgrades in robustness, context optimization, and evaluation.

# AI Website Brochure Generator

Generate professional or playful marketing brochures automatically from any company website using LLMs.

## 🚀 Features

- Scrapes website content intelligently
- Uses LLMs to select brochure-relevant pages
- Builds structured website context
- Streams brochure generation in real time
- Supports multiple writing styles
- Interactive UI via Gradio

### Robust Link Ingestion

The system performs deterministic URL normalization during crawling:

- Resolves relative links to absolute URLs
- Restricts ingestion to same-domain pages
- Canonicalizes URLs to avoid duplicate content

This ensures reliable, clean context construction for downstream LLM processing.

### Reliability & Failure Handling

The system includes basic resilience mechanisms to handle real-world failures:

- Network requests and LLM calls use exponential backoff retries
- Partial scraping failures do not terminate the pipeline
- Streaming generation degrades gracefully on transient errors

This ensures stable behavior under non-ideal network and API conditions.

### Rate-Limit Awareness

LLM requests are throttled and retried adaptively to respect API rate limits and ensure stable behavior under load.

### Structured Context Assembly

Instead of passing raw website text to the LLM, the system:

- Extracts semantic sections from each page (About, Products, Features, Careers, etc.)
- Labels content explicitly by section
- Preserves semantic boundaries during truncation

This significantly improves:

- Token efficiency
- Output consistency
- Section completeness
- Model interpretability

### Token Budget Strategy

To prevent high-value content from being truncated:

- Each section is assigned a deterministic priority weight
- The overall context budget is allocated proportionally
- High-signal sections (Products, Features) are always preserved
- Low-signal sections (Careers, Contact) cannot crowd out core content

This ensures stable, repeatable generation under strict context limits.

---

## 🧠 How It Works

1. User enters a website URL
2. Website pages are scraped and cleaned
3. LLM selects brochure-relevant links (About, Products, Careers, etc.)
4. Content is assembled into a unified context
5. LLM generates a structured brochure in Markdown
6. Output streams live to the UI

## 🏗️ Architecture
