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
- `assets/brand-icons.js` - Generated brand marks (see "Provider and Model Logos"). Loaded by a plain `<script>` tag before the app script, so `window.BRAND_ICONS` is always ready by first render.
- `tools/build-brand-icons.py` - Regenerates `assets/brand-icons.js`.
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
5. LiteLLM writes `0` both for genuinely free models and for models it has no price for, and the two are indistinguishable. A `0` is therefore never rendered as a price — the cell shows 「暂无」 with a tooltip instead of `0 元`/「免费」, and such models sort to the bottom of their provider card and are excluded from the cheapest-price sort. Models priced per request (`input_cost_per_request`, e.g. the Perplexity online models) show `元/次` in the input column.

To change behavior (display logic, conversion rate, filters, data sources), edit the inline script in `index.html`. The data source endpoints are defined near the top of that script (`PRICING_SOURCES`).

## Provider and Model Logos

Provider cards show a real brand logo, and each model row shows the mark of the family that built the model (so a Bedrock or OpenRouter card reveals its Anthropic / Meta / Mistral models at a glance).

- Glyphs live in `assets/brand-icons.js` as monochrome 24x24 path data drawn with `fill: currentColor`. One path serves both contexts: white on the provider tile, brand-coloured next to a model id.
- Two lookup tables in `index.html` decide which mark applies. `PROVIDER_BRANDS` maps `litellm_provider` to a slug, and unknown suffixed variants (`vertex_ai-*`, `bedrock_*`) inherit their parent's mark. `MODEL_BRANDS` is an ordered list of regexes matched against the lowercased model key, so `us.anthropic.claude-...` and `azure_ai/Llama-4-...` still resolve to Claude and Meta. First match wins, so keep the specific patterns above the general ones.
- Anything unmatched degrades on purpose: the card keeps its hashed gradient tile with two-letter initials, and the model row shows no mark. The page also renders correctly if `assets/brand-icons.js` fails to load.
- The model-row mark sits on the model-id line rather than beside the bold name. Blink only breaks a long word when it is alone on a line, so an inline glyph in front of a long name pushes the whole name to the next line; the id line already breaks anywhere, so the mark stays put and the name keeps its full column width.
- To add or recolour a brand, edit `BRANDS` in `tools/build-brand-icons.py` and rerun it (it fetches from jsDelivr), then add the matching `PROVIDER_BRANDS` / `MODEL_BRANDS` entry in `index.html`. Do not hand-edit the generated file.

## Data Sources

LiteLLM cost map (primary CDN source, plus raw-GitHub and backup fallbacks). The exact URLs are listed in `README.md` under "数据来源" and in `index.html`.
