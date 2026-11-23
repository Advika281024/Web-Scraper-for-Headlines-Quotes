# Quotes Web Scraper

A beginner-friendly Python web-scraping project that collects quote text, author names and tags from **https://quotes.toscrape.com/**, a website designed for scraping practice.

## Files

- `scraper.py` — requests pages, parses HTML with BeautifulSoup, follows pagination and writes output files.
- `quotes.json` — sample output containing the first page's 10 records.
- `quotes.txt` — the same sample records in a readable format.
- Running the scraper replaces both output files with the full dataset it successfully collects.

## Requirements

- Python 3.8 or later
- Internet connection

Install dependencies:

```bash
python -m pip install requests beautifulsoup4
```

## Run

Open a terminal in this folder and execute:

```bash
python scraper.py
```

The program creates/updates `quotes.json` and `quotes.txt` in the project folder. It also prints the total number of quotes, the most frequently quoted author and the most common tag.

## How it works

1. `requests.Session()` sends an HTTP GET request with a descriptive User-Agent and a 10-second timeout.
2. `raise_for_status()` detects unsuccessful HTTP responses.
3. `BeautifulSoup(..., "html.parser")` parses the returned HTML.
4. CSS selectors `div.quote`, `span.text`, `small.author` and `a.tag` extract each record.
5. The scraper follows `li.next a` until there is no next page.
6. It waits one second between page requests and writes UTF-8 JSON and text output.

## Source choice and permission note

The project uses **Quotes to Scrape**, a public practice website created specifically for learning web scraping. It does not collect personal data, access login-only pages or target a production news website. The included `quotes.json` and `quotes.txt` are a sample of the first page; run the script to collect the full practice dataset.

For any other website, check its terms of use and `https://example.com/robots.txt` (replace the domain), follow applicable laws and site rules, identify your client honestly, and keep request rates low. Public accessibility alone does not automatically grant permission to scrape every site.

## Politeness and error handling

- 10-second request timeout.
- One-second delay between page requests.
- Descriptive User-Agent header.
- HTTP errors and network failures are caught and reported.
- Missing quote or author elements are checked before text extraction.
- Repeated page URLs are detected to avoid an accidental loop.

## Expected output

After a successful run, the terminal prints progress for each page and a summary similar to:

```text
--- Scraping summary ---
Total quotes: 100
Most quoted author: ...
Most common tag: ...
```

The exact summary depends on the current contents of the practice website.
