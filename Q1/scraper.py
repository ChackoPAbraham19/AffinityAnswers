#imports
import argparse
import json
import re
import sys
from urllib.parse import urlencode

from playwright.sync_api import sync_playwright

BASE_URL = "https://mdcomputers.in/"
# Search results live here; the same card markup is also reused in hidden menus/carousels
RESULTS = "div.all-product-wrapper"
# The default "HeadlessChrome" user agent gets an empty page, so present as regular Chrome
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"
)


def search_url(term, page):
    return BASE_URL + "?" + urlencode({"route": "product/search", "search": term, "page": page})


def parse_price(text):
    """'₹1,299' -> 1299; None if there is no number."""
    digits = re.sub(r"[^\d]", "", text or "")
    return int(digits) if digits else None


def extract_products(page):
    products = []
    for card in page.query_selector_all(f"{RESULTS} div.product-grid-item"):
        link = card.query_selector("h3.product-entities-title a")
        if not link:
            continue
        # Discounted items: <span.del> holds the MRP, <span.ins> the selling price.
        # Non-discounted items have just a single amount inside .price.
        old_el = card.query_selector(".price .del")
        new_el = card.query_selector(".price .ins") or card.query_selector(".price")
        products.append({
            "name": link.inner_text().strip(),
            "url": link.get_attribute("href"),
            "price": parse_price(new_el.inner_text()) if new_el else None,
            "original_price": parse_price(old_el.inner_text()) if old_el else None,
        })
    return products


def has_next_page(page):
    return any(a.inner_text().strip() == ">" for a in page.query_selector_all("ul.pagination a"))


def scrape(term, max_pages, headed=False):
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed)
        page = browser.new_page(user_agent=USER_AGENT)
        for page_no in range(1, max_pages + 1):
            # Results are server-rendered; waiting for full "load" can hang on third-party scripts
            page.goto(search_url(term, page_no), wait_until="domcontentloaded")
            products = extract_products(page)
            results.extend(products)
            if not products or not has_next_page(page):
                break
        browser.close()
    return results


def main():
    parser = argparse.ArgumentParser(description="Search mdcomputers.in and output products as JSON.")
    parser.add_argument("term", nargs="?", help="search term (prompted for if omitted)")
    parser.add_argument("--max-pages", type=int, default=10, help="max result pages to fetch (default: 10)")
    parser.add_argument("--headed", action="store_true", help="show the browser window")
    args = parser.parse_args()

    if args.term is None:
        # Prompt on stderr so stdout stays pure JSON when piped
        print("Search term: ", end="", file=sys.stderr, flush=True)
        args.term = sys.stdin.readline()
    term = args.term.strip()
    if not term:
        parser.error("search term must not be empty")

    products = scrape(term, args.max_pages, args.headed)
    json.dump(
        {"search_term": term, "count": len(products), "products": products},
        sys.stdout, indent=2, ensure_ascii=False,
    )
    print()


if __name__ == "__main__":
    main()
