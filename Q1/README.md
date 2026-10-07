# Q1 – mdcomputers.in product search scraper

Takes a search term, fetches the mdcomputers.in search results, and prints the listed products as JSON.

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/playwright install chromium
```

## Usage

```bash
.venv/bin/python scraper.py "external harddrive"          # term as argument
.venv/bin/python scraper.py                               # prompts for the term
.venv/bin/python scraper.py "ssd" --max-pages 1           # first results page only
.venv/bin/python scraper.py "ssd" --headed                # watch the browser
.venv/bin/python scraper.py "ssd" > results.json          # save to a file
```

## Output

```json
{
  "search_term": "external harddrive",
  "count": 45,
  "products": [
    {
      "name": "Seagate One Touch 1TB External Hard Drive",
      "url": "https://mdcomputers.in/product/seagate-one-touch-1tb-external-hard-drive-stky1000400",
      "price": 9450,
      "original_price": 10000
    }
  ]
}
```

`price` is the current selling price and `original_price` is the struck-through MRP (`null` when the item isn't discounted). Both are integers in rupees.

## Design choices

**Playwright (a real browser) instead of `requests` + BeautifulSoup.** The site is behind Cloudflare and serves an empty page to obvious bots. A real Chromium engine runs the site's JavaScript and passes those checks reliably. It is slower than raw HTTP, but correctness matters more here than speed.

**A regular Chrome user agent.** Headless Chromium advertises itself as `HeadlessChrome` and gets a blank page, so the scraper presents a normal desktop Chrome user agent. This keeps the default headless mode working; use `--headed` to watch it.

**Scoping selectors to the results grid (`div.all-product-wrapper`).** The site reuses the same product card markup (`div.product-grid-item`, `h3.product-entities-title`) in its hidden mega-menus and carousels. Selecting cards page-wide would mix CPUs and monitors into every result set and wait on hidden elements. Restricting to the results container returns exactly the listed products.

**Following pagination, with a limit.** One results page shows only 20 items, so "the listed products" for a term usually span several pages. The scraper follows the `>` (next) link until it disappears and stops at `--max-pages` (default 10) so a very broad term can't run forever.

**`domcontentloaded` instead of `load`.** The product grid is server-rendered, so it is present as soon as the HTML is parsed. Waiting for the full `load` event sometimes timed out on slow third-party scripts and added nothing.

**Graceful empty results.** A term with no matches returns `{"count": 0, "products": []}` instead of timing out or crashing.

**Prices parsed into integers, kept in two fields.** `"₹1,299"` becomes `1299`, so the numbers can be sorted, compared or summed directly. Keeping `original_price` separate preserves the discount information without making consumers parse a combined string.

### Why JSON

- **Structured and typed.** Prices are real numbers and a missing discount is a real `null`, not an empty string.
- **Machine-friendly.** The output can be piped straight into `jq`, loaded with `json.load`, or sent to an API with no extra parsing. For example, the cheapest item is `jq '.products | min_by(.price)'`.
- **Self-describing.** The wrapper records the search term and count next to the results, so a saved file still makes sense on its own.
- **Unicode-safe.** `ensure_ascii=False` keeps product names readable.
- **Clean stdout.** The interactive prompt is written to stderr, so `scraper.py > out.json` always produces valid JSON.

CSV was the main alternative. It opens nicely in a spreadsheet, but it has no types (everything is text), no standard way to represent "no discount", and no place for metadata such as the search term. JSON can still be turned into CSV in one line if needed:

```bash
jq -r '.products[] | [.name, .price, .original_price, .url] | @csv' results.json
```

## Limitations

- Depends on the site's current HTML class names. If the theme changes, the selectors at the top of `scraper.py` need updating.
- Results follow the site's own relevance ranking, so loosely related items (e.g. a USB cable for "external harddrive") are included as the site lists them.
