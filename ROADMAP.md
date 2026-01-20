# Roadmap – Production Hardening & System Evolution

This document outlines the current limitations of the system, why they exist, how they impact behavior and quality, and the planned engineering steps to evolve the project from a functional prototype into a production-grade LLM application.

---

## Phase 1 – Reliability & Robustness

### 1.1 Missing Retry & Failure Handling — ✅ Implemented

**Problem addressed**  
The initial system assumed ideal network and API behavior, causing transient failures during scraping or LLM calls to terminate the pipeline.

**Solution implemented**

- Introduced a centralized retry utility with exponential backoff
- Wrapped network scraping operations with retry logic
- Wrapped OpenAI API calls with retry logic
- Added graceful degradation for streaming interruptions

**Impact**

- Improved resilience to transient network and API failures
- Partial failures no longer crash the generation pipeline
- More stable user experience under real-world conditions

---

### 1.2 No Rate-Limit Awareness

**Why it exists**  
Rate-limit handling is intentionally deferred to avoid premature complexity during prototyping.

**Impact on the system**

- Concurrent usage may trigger API throttling
- Requests may fail unpredictably under load

**Planned improvements**

- Centralized request throttling
- Adaptive retry with rate-limit headers
- Queue-based request scheduling

---

### 1.3 URL Normalization Gaps — ✅ Implemented

**Problem addressed**  
Initial link extraction returned raw `href` values, leading to broken relative URLs, external domain noise, and duplicate pages.

**Solution implemented**

- All extracted links are normalized to absolute URLs
- Crawling is restricted to same-domain pages only
- Canonical URL normalization removes fragments, query parameters, and trailing slash inconsistencies

**Impact**

- Reliable page fetching
- Cleaner, domain-specific context
- Reduced duplication and token waste

---

## Phase 2 – Context Quality & LLM Efficiency

### 2.1 Unstructured Context Input

**Why it exists**  
Raw page text is passed directly to the model to validate end-to-end feasibility.

**Impact on the system**

- Token usage is inefficient
- Important content may be diluted
- Model must infer structure implicitly

**Planned improvements**

- Page chunking with semantic boundaries
- Section-level labeling (About, Products, Careers, etc.)
- Relevance-weighted context assembly

---

### 2.2 No Token Budget Strategy

**Why it exists**  
Token limits are currently enforced via truncation for simplicity.

**Impact on the system**

- Potential loss of high-value content
- Non-deterministic content prioritization

**Planned improvements**

- Deterministic token allocation per section
- Priority-based truncation
- Model-aware context sizing

---

## Phase 3 – Evaluation & Guardrails

### 3.1 No Output Verification

**Why it exists**  
The initial focus is on generation quality rather than validation.

**Impact on the system**

- Possible hallucinated claims
- Missing or underdeveloped sections
- Inconsistent tone adherence

**Planned improvements**

- Self-critique pass using a secondary LLM call
- Section completeness checks
- Hallucination likelihood scoring

---

### 3.2 No Confidence Thresholding

**Why it exists**  
All generated outputs are currently treated as valid.

**Impact on the system**

- Low-confidence generations are not flagged
- Users may receive suboptimal content without warning

**Planned improvements**

- Confidence scoring on generated sections
- Explicit fallback messaging when confidence is low
- Optional regeneration strategies

---

## Phase 4 – Performance & Scalability

### 4.1 Blocking I/O Operations

**Why it exists**  
The system uses synchronous requests for clarity and ease of debugging.

**Impact on the system**

- Slower response times
- Inefficient resource usage during scraping

**Planned improvements**

- Async scraping using `aiohttp`
- Concurrent page fetching
- Improved throughput under load

---

### 4.2 No Caching Layer

**Why it exists**  
Caching is deferred to avoid premature optimization.

**Impact on the system**

- Repeated scraping of identical pages
- Unnecessary latency and network usage

**Planned improvements**

- In-memory or disk-based caching
- Cache invalidation strategies
- Reuse of previously processed content

---

## Phase 5 – Compliance & Ethical Crawling

### 5.1 robots.txt Awareness

**Why it exists**  
Initial development prioritizes functional flow over crawl governance.

**Impact on the system**

- Potential violation of site crawling policies

**Planned improvements**

- Respect robots.txt rules
- User-configurable crawl constraints
- Transparent crawling behavior

---

## Long-Term Vision

The end goal is a fully production-grade LLM system with:

- Deterministic context construction
- Robust failure handling
- Evaluated and validated outputs
- Scalable, ethical, and efficient data ingestion

Each phase will be implemented incrementally to preserve clarity, testability, and system correctness.
