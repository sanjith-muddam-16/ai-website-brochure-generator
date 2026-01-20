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

## 🧠 How It Works

1. User enters a website URL
2. Website pages are scraped and cleaned
3. LLM selects brochure-relevant links (About, Products, Careers, etc.)
4. Content is assembled into a unified context
5. LLM generates a structured brochure in Markdown
6. Output streams live to the UI

## 🏗️ Architecture
