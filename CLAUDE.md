# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

llmprice.cn is a static website comparing LLM API prices across major providers. The site is hosted on GitHub Pages at https://llmprice.cn.

Pricing data is **not** maintained in this repo. The page pulls the full model catalog live from [LiteLLM's cost map](https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json) in the browser at runtime, groups models by `litellm_provider`, and renders every priced chat/completion/responses model. There is no hardcoded price table to keep up to date.

## Tech Stack

- **Static Site Generator**: Jekyll with minima remote theme (solarized skin)
- **Hosting**: GitHub Pages
- **Domain**: llmprice.cn (configured in CNAME)

## Key Files

- `index.html` - The actual app. A standalone card-based UI (separate from the Jekyll theme) whose inline `<script>` fetches LiteLLM data, converts USD/token prices to CNY per 1M tokens, and handles provider filtering and search.
- `README.md` - Project documentation only (architecture, data sources, FAQ). No longer holds price data.
- `features.md` - Feature comparison table (Web Search, Tool Calling, multimodal support)
- `_config.yml` - Jekyll configuration
- `_includes/google-analytics.html` - Google Analytics integration

## Development

Run Jekyll locally:
```bash
bundle exec jekyll serve
```

## How Pricing Works

Prices are loaded client-side, so visitors always see current data without any commit:

1. The page reads the last successful LiteLLM sync from `localStorage` for an instant first paint.
2. It then fetches the latest LiteLLM cost map (CDN source, with raw-GitHub and backup fallbacks).
3. Models are grouped by `litellm_provider`; only entries with pricing and `mode in {chat, completion, responses}` are shown.
4. LiteLLM maintains `USD / token`; the page converts to `元 / 百万 Token` at a default `$1 = ¥7` (adjustable in the page header). Tiered-price models show the first tier.

To change behavior (display logic, conversion rate, filters, data sources), edit the inline script in `index.html`. The data source endpoints are defined near the top of that script (`PRICING_SOURCES`).

## Data Sources

LiteLLM cost map (primary CDN source, plus raw-GitHub and backup fallbacks). The exact URLs are listed in `README.md` under "数据来源" and in `index.html`.
