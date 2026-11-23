"""
Quotes to Scrape - learning project
Run: python scraper.py
Install: pip install requests beautifulsoup4
"""

import json
import time
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com/"
HEADERS = {
    "User-Agent": "StudentLearningScraper/1.0 (educational use)"
}
TIMEOUT = 10
DELAY_SECONDS = 1
OUTPUT_DIR = Path(__file__).resolve().parent


def extract_quote_cards(soup):
    """Extract quote text, author and tags from one parsed page."""
    records = []

    for card in soup.select("div.quote"):
        quote_node = card.select_one("span.text")
        author_node = card.select_one("small.author")

        # Defensive checks: skip incomplete cards rather than crashing.
        if quote_node is None or author_node is None:
            continue

        records.append({
            "text": quote_node.get_text(strip=True),
            "author": author_node.get_text(strip=True),
            "tags": [tag.get_text(strip=True) for tag in card.select("a.tag")]
        })

    return records


def scrape_quotes():
    """Scrape all quote pages, following the Next link politely."""
    session = requests.Session()
    session.headers.update(HEADERS)

    next_url = BASE_URL
    all_quotes = []
    visited_urls = set()

    while next_url:
        if next_url in visited_urls:
            print(f"Stopping because a page URL repeated: {next_url}")
            break
        visited_urls.add(next_url)

        try:
            response = session.get(next_url, timeout=TIMEOUT)
            response.raise_for_status()
        except requests.RequestException as error:
            print(f"Request failed for {next_url}: {error}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        page_quotes = extract_quote_cards(soup)
        all_quotes.extend(page_quotes)
        print(f"Collected {len(page_quotes)} quotes from {next_url}")

        next_link = soup.select_one("li.next a")
        next_url = urljoin(next_url, next_link["href"]) if next_link and next_link.get("href") else None

        if next_url:
            time.sleep(DELAY_SECONDS)

    return all_quotes


def save_outputs(quotes):
    """Write machine-readable JSON and a human-readable text file."""
    json_path = OUTPUT_DIR / "quotes.json"
    text_path = OUTPUT_DIR / "quotes.txt"

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(quotes, file, indent=2, ensure_ascii=False)

    with text_path.open("w", encoding="utf-8") as file:
        for number, quote in enumerate(quotes, start=1):
            file.write(f"{number}. {quote['text']}\n")
            file.write(f"   Author: {quote['author']}\n")
            file.write(f"   Tags: {', '.join(quote['tags']) or 'None'}\n\n")

    print(f"\nSaved {len(quotes)} quotes to {json_path.name} and {text_path.name}")


def print_summary(quotes):
    """Print total records, most frequent author and most frequent tag."""
    print("\n--- Scraping summary ---")
    print(f"Total quotes: {len(quotes)}")

    if not quotes:
        print("No records were collected; check the network or page structure.")
        return

    author_counts = Counter(item["author"] for item in quotes)
    tag_counts = Counter(tag for item in quotes for tag in item["tags"])

    author, author_count = author_counts.most_common(1)[0]
    print(f"Most quoted author: {author} ({author_count} quotes)")

    if tag_counts:
        tag, tag_count = tag_counts.most_common(1)[0]
        print(f"Most common tag: {tag} ({tag_count} uses)")
    else:
        print("Most common tag: No tags found")


def main():
    quotes = scrape_quotes()
    save_outputs(quotes)
    print_summary(quotes)


if __name__ == "__main__":
    main()
