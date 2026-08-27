#!/usr/bin/env python3
"""Generate the pre-rendered provider and model pages Jekyll builds into HTML.

The app in index.html fetches the LiteLLM cost map in the browser, so a crawler
sees an empty grid and 586 characters of UI chrome. This script renders the same
catalogue into files Jekyll turns into real pages, which is what makes the
prices indexable at all.

It writes two page families:

  p/<provider>/index.html   every priced model that provider sells
  m/<model>/index.html      every provider selling that model, cheapest first

Model pages exist only where two or more providers sell the model. A page for a
model one provider sells restates a single price and has nothing to compare, so
it would be a thin page competing with the provider page that already lists it.

Provider labels and categories are parsed out of index.html rather than copied
here, so the two never drift apart. The parse is strict: if those literals move
or change shape, this fails loudly instead of silently generating wrong pages.
"""

import argparse
import json
import pathlib
import re
import shutil
import sys
import urllib.request

REPO = pathlib.Path(__file__).resolve().parent.parent
INDEX_HTML = REPO / 'index.html'

SOURCES = [
    'https://cdn.jsdelivr.net/gh/BerriAI/litellm@main/model_prices_and_context_window.json',
    'https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json',
    'https://raw.githubusercontent.com/BerriAI/litellm/main/litellm/model_prices_and_context_window_backup.json',
]

TEXT_MODES = {'chat', 'completion', 'responses'}
USD_TO_CNY = 7  # matches the default rate in index.html


# --------------------------------------------------------------------------
# constants shared with index.html
# --------------------------------------------------------------------------

def _fail(message):
    sys.exit(f'build-pages: {message}\n'
             f'  index.html changed shape; update tools/build-pages.py to match.')


def load_shared_constants():
    html = INDEX_HTML.read_text(encoding='utf-8')

    official = re.search(r'const OFFICIAL_PROVIDERS = new Set\(\[(.*?)\]\);', html, re.S)
    cloud = re.search(r'const CLOUD_PROVIDER_KEYWORDS = \[(.*?)\];', html, re.S)
    labels = re.search(r'const PROVIDER_LABELS = \{(.*?)\n        \};', html, re.S)

    if not (official and cloud and labels):
        _fail('could not find OFFICIAL_PROVIDERS / CLOUD_PROVIDER_KEYWORDS / PROVIDER_LABELS')

    official_set = set(re.findall(r"'([^']+)'", official.group(1)))
    cloud_list = re.findall(r"'([^']+)'", cloud.group(1))

    # Keys are bare identifiers until they need a hyphen, at which point they
    # are quoted — 'vertex_ai-anthropic_models' and friends. Match both.
    label_map = {
        key.strip("'"): value.replace("\\'", "'")
        for key, value in re.findall(
            r"('[^']+'|[A-Za-z0-9_]+)\s*:\s*'((?:[^'\\]|\\.)*)'", labels.group(1))
    }

    # A partial parse would silently fall back to humanized ids on the pages it
    # missed, so require every entry in the literal to have come through.
    declared = len(re.findall(r'^\s*\S+\s*:', labels.group(1), re.M))
    if len(label_map) != declared:
        _fail(f'parsed {len(label_map)} of {declared} PROVIDER_LABELS entries')
    if not official_set or not cloud_list:
        _fail(f'parsed too few constants '
              f'(official={len(official_set)}, cloud={len(cloud_list)})')

    return official_set, cloud_list, label_map


# --------------------------------------------------------------------------
# naming
# --------------------------------------------------------------------------

REGION = re.compile(r'^(us|eu|apac|global|us-gov)\.')
# Bedrock and Vertex namespace models under the vendor that built them, which
# duplicates the provider rather than naming the model.
VENDOR_DOT = re.compile(
    r'^(anthropic|meta|mistral|amazon|cohere|ai21|stability|deepseek|qwen|'
    r'minimax|moonshot|openai|google|writer|luma|twelvelabs|zhipu)\.'
)
BEDROCK_REV = re.compile(r'(?:-v\d+)?:\d+$')   # -v1:0, -v2:1, :0
VERTEX_REV = re.compile(r'@\d+$')              # gemini-1.5-pro@001


def normalize_model_name(key):
    """Collapse a LiteLLM key to the model it names, dropping who resells it.

    vertex_ai/claude-opus-5, azure_ai/claude-opus-5 and
    us.anthropic.claude-opus-5-v1:0 are one model behind three resellers.
    Grouping on the stripped name is what makes a comparison page possible.
    """
    name = key.split('/')[-1]
    name = REGION.sub('', name)
    name = VENDOR_DOT.sub('', name)
    name = BEDROCK_REV.sub('', name)
    name = VERTEX_REV.sub('', name)
    return name.strip('-').lower()


def slugify(name):
    slug = re.sub(r'[^a-z0-9.\-]+', '-', name.lower()).strip('-.')
    return re.sub(r'-{2,}', '-', slug)


def humanize_provider(provider_id, labels):
    if provider_id in labels:
        return labels[provider_id]
    return ' '.join(part.capitalize() for part in re.split(r'[_\-]+', provider_id) if part)


def categorize(provider_id, official, cloud_keywords):
    if provider_id in official:
        return 'official', '官方/直连'
    if any(keyword in provider_id for keyword in cloud_keywords):
        return 'cloud', '云平台'
    return 'platform', '聚合/托管'


# --------------------------------------------------------------------------
# pricing
# --------------------------------------------------------------------------

def extract_pricing(entry):
    """Mirror extractPricing() in index.html, including the tiered-price rule."""
    if isinstance(entry.get('input_cost_per_token'), (int, float)) and \
       isinstance(entry.get('output_cost_per_token'), (int, float)):
        return entry['input_cost_per_token'], entry['output_cost_per_token'], False

    tiers = entry.get('tiered_pricing')
    if isinstance(tiers, list) and tiers:
        first = tiers[0]
        if isinstance(first, dict) and \
           isinstance(first.get('input_cost_per_token'), (int, float)) and \
           isinstance(first.get('output_cost_per_token'), (int, float)):
            return first['input_cost_per_token'], first['output_cost_per_token'], True

    return None


def format_price(cny_per_million):
    """LiteLLM writes 0 both for free models and for ones it has no price for,
    and the two are indistinguishable — so 0 is never rendered as a price."""
    if not cny_per_million:
        return None
    if cny_per_million < 0.01:
        return f'{cny_per_million:.4f}'.rstrip('0').rstrip('.')
    if cny_per_million < 1:
        return f'{cny_per_million:.3f}'.rstrip('0').rstrip('.')
    return f'{cny_per_million:.2f}'.rstrip('0').rstrip('.')


def format_context(entry):
    tokens = entry.get('max_input_tokens') or entry.get('max_tokens')
    if not isinstance(tokens, (int, float)) or tokens <= 0:
        return '-'
    if tokens >= 1_000_000:
        return f'{tokens / 1_000_000:g}M'
    if tokens >= 1000:
        return f'{tokens / 1000:g}k'
    return str(int(tokens))


# --------------------------------------------------------------------------
# catalogue
# --------------------------------------------------------------------------

def fetch_catalog(local_path=None):
    if local_path:
        return json.loads(pathlib.Path(local_path).read_text(encoding='utf-8'))

    errors = []
    for url in SOURCES:
        try:
            with urllib.request.urlopen(url, timeout=60) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as error:  # noqa: BLE001 - report every source before failing
            errors.append(f'{url}: {error}')
    sys.exit('build-pages: every pricing source failed:\n  ' + '\n  '.join(errors))


def build_records(raw, official, cloud_keywords, labels):
    records = []
    for key, entry in raw.items():
        if key == 'sample_spec' or not isinstance(entry, dict):
            continue
        if entry.get('mode') not in TEXT_MODES:
            continue

        pricing = extract_pricing(entry)
        if not pricing:
            continue

        input_usd, output_usd, tiered = pricing
        provider_id = entry.get('litellm_provider') or 'unknown'
        category_id, category_label = categorize(provider_id, official, cloud_keywords)

        records.append({
            'key': key,
            'model': normalize_model_name(key),
            'provider_id': provider_id,
            'provider_name': humanize_provider(provider_id, labels),
            'category': category_label,
            'category_id': category_id,
            'input': input_usd * 1_000_000 * USD_TO_CNY,
            'output': output_usd * 1_000_000 * USD_TO_CNY,
            'input_usd': input_usd * 1_000_000,
            'output_usd': output_usd * 1_000_000,
            'context': format_context(entry),
            'tiered': tiered,
        })

    return records


def row(record):
    """One rendered table row. Prices are strings or None, never a bare 0."""
    return {
        'key': record['key'],
        'model': record['model'],
        'input': format_price(record['input']),
        'output': format_price(record['output']),
        'input_usd': format_price(record['input_usd']),
        'output_usd': format_price(record['output_usd']),
        'context': record['context'],
        'tiered': record['tiered'],
    }


def yaml_dump(value, indent=0):
    """Minimal YAML writer for front matter — every value here is a scalar,
    list or dict of strings, so json.dumps gives valid, unambiguous YAML."""
    pad = '  ' * indent
    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            if isinstance(v, (dict, list)):
                lines.append(f'{pad}{k}:')
                lines.append(yaml_dump(v, indent + 1))
            else:
                lines.append(f'{pad}{k}: {json.dumps(v, ensure_ascii=False)}')
        return '\n'.join(lines)
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, dict):
                body = yaml_dump(item, indent + 1).lstrip()
                lines.append(f'{pad}- {body}')
            else:
                lines.append(f'{pad}- {json.dumps(item, ensure_ascii=False)}')
        return '\n'.join(lines)
    return f'{pad}{json.dumps(value, ensure_ascii=False)}'


def write_page(path, front_matter):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('---\n' + yaml_dump(front_matter) + '\n---\n', encoding='utf-8')


def cheapest(rows):
    """Ties are common — a reseller usually matches the vendor's list price — so
    break them toward the direct vendor rather than whichever row sorted first."""
    priced = [r for r in rows if r['input']]
    if not priced:
        return None
    return min(priced, key=lambda r: (float(r['input']),
                                      r['category'] != '官方/直连',
                                      r['provider_name']))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', help='local LiteLLM json instead of fetching')
    parser.add_argument('--out', default=str(REPO), help='repo root to write into')
    args = parser.parse_args()

    out = pathlib.Path(args.out)
    official, cloud_keywords, labels = load_shared_constants()
    records = build_records(fetch_catalog(args.data), official, cloud_keywords, labels)

    for stale in ('p', 'm'):
        shutil.rmtree(out / stale, ignore_errors=True)

    by_provider = {}
    for record in records:
        by_provider.setdefault(record['provider_id'], []).append(record)

    by_model = {}
    for record in records:
        by_model.setdefault(record['model'], {}).setdefault(record['provider_id'], record)

    # Decide which models get a page before rendering anything, so provider rows
    # can carry the link directly. Resolving it in Liquid instead would mean
    # scanning the model list once per row — millions of comparisons per build.
    slugs = {}
    for model, providers in by_model.items():
        if len(providers) < 2:
            continue  # nothing to compare; the provider page already lists it
        slug = slugify(model)
        if not slug:
            continue
        if slug in slugs:
            sys.exit(f'build-pages: slug collision {slug!r} between '
                     f'{slugs[slug]!r} and {model!r}')
        slugs[slug] = model
    model_slug = {model: slug for slug, model in slugs.items()}

    def sort_rows(rows):
        # Unpriced models sink to the bottom: they are LiteLLM gaps, not bargains.
        # Ties go to the direct vendor over a reseller matching its list price.
        return sorted(rows, key=lambda r: (r['input'] is None,
                                           float(r['input']) if r['input'] else 0,
                                           r.get('category') != '官方/直连',
                                           r.get('provider_name', '')))

    # ---- provider pages ------------------------------------------------
    providers_index = []
    for provider_id, group in sorted(by_provider.items(), key=lambda kv: -len(kv[1])):
        rows = sort_rows([dict(row(r), compare_slug=model_slug.get(r['model'], ''))
                          for r in group])
        name = group[0]['provider_name']
        category = group[0]['category']
        write_page(out / 'p' / provider_id / 'index.html', {
            'layout': 'provider',
            'permalink': f'/p/{provider_id}/',
            'title': f'{name} API 价格 - {len(rows)} 个模型报价对比',
            'description': f'{name}（{provider_id}）全部 {len(rows)} 个可定价大模型的 API '
                           f'输入与输出价格，单位 元/百万 Token，数据取自 LiteLLM 官方成本表。',
            'crumb': name,
            'heading': f'{name} API 价格',
            'lede': f'{name} 共有 {len(rows)} 个可定价文本模型，'
                    f'下表按输入价格从低到高排列，单位 元/百万 Token。',
            'provider_id': provider_id,
            'provider_name': name,
            'category': category,
            'model_count': len(rows),
            'rows': rows,
        })
        providers_index.append({
            'id': provider_id, 'name': name, 'category': category, 'count': len(rows),
        })

    # ---- model pages ---------------------------------------------------
    models_index = []
    for slug, model in slugs.items():
        providers = by_model[model]
        rows = sort_rows([dict(row(r), provider_id=r['provider_id'],
                               provider_name=r['provider_name'], category=r['category'])
                          for r in providers.values()])
        best = cheapest(rows)
        write_page(out / 'm' / slug / 'index.html', {
            'layout': 'model',
            'permalink': f'/m/{slug}/',
            'title': f'{model} 价格对比 - {len(rows)} 家厂商报价',
            'description': (f'{model} 在 {len(rows)} 家厂商的 API 报价对比'
                            + (f'，最低 {best["provider_name"]} {best["input"]} 元/百万 Token'
                               if best else '')
                            + '，含输入输出价格与上下文长度。'),
            'crumb': model,
            'heading': f'{model} 价格对比',
            'lede': (f'{len(rows)} 家厂商提供 {model}，'
                     + (f'当前最便宜的是 {best["provider_name"]}，'
                        f'输入 {best["input"]} 元/百万 Token。'
                        if best else '下表列出各家报价。')),
            'model_name': model,
            'provider_count': len(rows),
            'cheapest_provider': best['provider_name'] if best else '',
            'cheapest_input': best['input'] if best else '',
            'rows': rows,
        })
        models_index.append({'slug': slug, 'name': model, 'providers': len(rows)})

    # ---- index used by the homepage to link into everything -------------
    models_index.sort(key=lambda m: (-m['providers'], m['name']))
    (out / '_data').mkdir(exist_ok=True)
    (out / '_data' / 'catalog.json').write_text(
        json.dumps({'providers': providers_index, 'models': models_index},
                   ensure_ascii=False, indent=1),
        encoding='utf-8')

    print(f'build-pages: {len(records)} priced models -> '
          f'{len(providers_index)} provider pages + {len(models_index)} model pages')


if __name__ == '__main__':
    main()
