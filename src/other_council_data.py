import csv
import re
import ssl
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd
import pdfplumber

from src.paths import OTHER_DOCUMENTS_DIR, OTHER_EXTRACTED_DIR, OTHER_PROCESSED_DIR, create_data_folders


BASE_URL = "https://www.mumbwacouncil.gov.zm/"
PUBLICATIONS_URL = BASE_URL + "?page_id=195"
NEWS_LIST_URL = BASE_URL + "?page_id=187"
FAQ_URL = BASE_URL + "?page_id=1914"
MAX_TEXT_PAGES_PER_PDF = 20
MAX_TABLE_PAGES_PER_PDF = 6
MAX_TEXT_CHARACTERS_PER_PAGE = 8000

PAGES_TO_COLLECT = {
    "home": BASE_URL,
    "who_we_are": BASE_URL + "?page_id=118",
    "senior_management": BASE_URL + "?page_id=2877",
    "departments": BASE_URL + "?page_id=770",
    "civic_leaders": BASE_URL + "?page_id=2868",
    "council_chairman": BASE_URL + "?page_id=2879",
    "nangoma_constituency": BASE_URL + "?page_id=2873",
    "mumbwa_central_constituency": BASE_URL + "?page_id=2871",
    "standing_committees": BASE_URL + "?page_id=2881",
    "mandate": BASE_URL + "?page_id=169",
    "services": BASE_URL + "?page_id=792",
    "zdsp": BASE_URL + "?page_id=2247",
    "projects": BASE_URL + "?page_id=2244",
    "cash_for_work": BASE_URL + "?page_id=2883",
    "application_forms": BASE_URL + "?page_id=1559",
    "contact_us": BASE_URL + "?page_id=275",
    "faqs": FAQ_URL,
}

CDF_WORDS = [
    "cdf",
    "bursar",
    "grant",
    "community-projects",
    "community projects",
    "constituency-development-fund",
    "constituency development fund",
]


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.current_href = None
        self.current_text = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.current_href = href
                self.current_text = []

    def handle_data(self, data):
        if self.current_href is not None:
            text = clean_text(data)
            if isinstance(text, str):
                self.current_text.append(text)

    def handle_endtag(self, tag):
        if tag == "a" and self.current_href is not None:
            text = clean_text(" ".join(self.current_text))
            self.links.append({"href": self.current_href, "text": text})
            self.current_href = None
            self.current_text = []


class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        text = clean_text(data)
        if isinstance(text, str):
            self.parts.append(text)


def clean_text(value):
    if value is None or value is np.nan:
        return np.nan

    text = str(value)
    text = re.sub(r"\s+", " ", text).strip()
    return text if text else np.nan


def has_text(value):
    return isinstance(value, str) and bool(value.strip())


def fetch_url(url):
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    context = ssl._create_unverified_context()
    with urlopen(request, context=context, timeout=60) as response:
        return response.read()


def fetch_html(url):
    return fetch_url(url).decode("utf-8", errors="replace")


def html_to_text(html):
    html = re.sub(r"(?is)<script.*?</script>", " ", html)
    html = re.sub(r"(?is)<style.*?</style>", " ", html)
    parser = TextParser()
    parser.feed(html)
    return clean_text(" ".join(parser.parts))


def page_title(html):
    match = re.search(r"(?is)<title>(.*?)</title>", html)
    if not match:
        return np.nan

    title = re.sub(r"\s+", " ", match.group(1)).strip()
    title = title.replace(" - Mumbwa Town Council", "").replace(" – Mumbwa Town Council", "")
    return clean_text(title)


def get_links(html, page_url):
    parser = LinkParser()
    parser.feed(html)
    return [{"url": urljoin(page_url, link["href"]), "text": link["text"]} for link in parser.links]


def category_from_document(title, url):
    text = f"{title} {url}".lower()

    if any(word in text for word in ["budget", "financial", "receipts", "payments"]):
        return "financial"
    if "idp" in text:
        return "idp"
    if "stakeholder" in text:
        return "stakeholder_minutes"
    if "ordinary-council" in text or "special-council" in text or "council-meeting" in text:
        return "council_minutes"
    if "audit" in text or "operations-report" in text:
        return "audit_report"
    if "procurement" in text:
        return "procurement_plan"
    if "solid-waste" in text or "dump-site" in text:
        return "solid_waste"
    if "grievance" in text:
        return "grievance"
    if "newsletter" in text or "press-statement" in text:
        return "public_relations"
    if "act" in text or "si-" in text:
        return "legislation"
    if "application" in text or "form" in text:
        return "application_forms"

    return "other_publication"


def should_skip_cdf_document(title, url):
    text = f"{title} {url}".lower()
    return any(word in text for word in CDF_WORDS)


def document_id_from_url(url):
    name = Path(urlparse(url).path).stem.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name).strip("_")
    return name[:90]


def collect_publication_documents():
    html = fetch_html(PUBLICATIONS_URL)
    links = get_links(html, PUBLICATIONS_URL)
    rows = []
    seen_urls = set()

    for link in links:
        url = link["url"]
        title = clean_text(link["text"])
        path = urlparse(url).path

        if url in seen_urls:
            continue
        if not re.search(r"\.(pdf|docx?)$", path, re.IGNORECASE):
            continue
        if should_skip_cdf_document(title, url):
            continue

        seen_urls.add(url)
        document_name = Path(path).name
        rows.append(
            {
                "document_id": document_id_from_url(url),
                "Document Name": document_name,
                "Title From Website": title,
                "Category": category_from_document(title, url),
                "File Type": Path(path).suffix.lower().replace(".", ""),
                "Source URL": url,
                "Source Page": PUBLICATIONS_URL,
            }
        )

    return rows


def collect_website_pages():
    rows = []

    for page_id, url in PAGES_TO_COLLECT.items():
        html = fetch_html(url)
        rows.append(
            {
                "Page ID": page_id,
                "Page Title": page_title(html),
                "Page URL": url,
                "Page Text": html_to_text(html),
            }
        )

    return rows


def collect_news_updates():
    html = fetch_html(NEWS_LIST_URL)
    links = get_links(html, NEWS_LIST_URL)
    post_urls = []

    for link in links:
        url = link["url"]
        if "?p=" in url and url not in post_urls:
            post_urls.append(url)

    rows = []
    for url in post_urls:
        html = fetch_html(url)
        text = html_to_text(html)
        title = page_title(html)
        published_match = re.search(r"Published ([A-Za-z]+ \d{1,2}, \d{4})", text or "")
        author_match = re.search(r"By ([A-Za-z ]+)", text or "")

        rows.append(
            {
                "News Title": title,
                "Published Date": published_match.group(1) if published_match else np.nan,
                "Author": clean_text(author_match.group(1)) if author_match else np.nan,
                "News URL": url,
                "News Text": text,
            }
        )

    return rows


def collect_faq_rows():
    html = fetch_html(FAQ_URL)
    text = html_to_text(html)
    parts = re.split(r"(What [^?]+\?|How [^?]+\?)", text)
    rows = []

    for index in range(1, len(parts), 2):
        question = clean_text(parts[index])
        answer = clean_text(parts[index + 1] if index + 1 < len(parts) else "")
        if has_text(question) and has_text(answer):
            answer = re.split(r"Contact Information|COMPLAINTS|Ministry of", answer)[0]
            rows.append({"Question": question, "Answer": clean_text(answer), "Source URL": FAQ_URL})

    return rows


def save_dataframe(rows, output_file):
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)

    if df.empty:
        return df

    df = df.replace(r"^\s*$", np.nan, regex=True)
    df = df.dropna(axis=1, how="all")
    df = df.drop_duplicates()
    df.to_csv(output_file, index=False, sep="|", quoting=csv.QUOTE_MINIMAL)
    return df


def download_documents(documents):
    OTHER_DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    downloaded = []

    for document in documents:
        url = document["Source URL"]
        file_name = document["Document Name"]
        output_file = OTHER_DOCUMENTS_DIR / file_name

        if not output_file.exists():
            try:
                print(f"Downloading: {file_name}", flush=True)
                output_file.write_bytes(fetch_url(url))
            except Exception as error:
                print(f"Could not download {file_name}: {error}", flush=True)
                continue

        downloaded.append(
            {
                **document,
                "Local File": str(output_file),
                "File Size Bytes": output_file.stat().st_size,
            }
        )

    return downloaded


def extract_pdf_text_and_tables(downloaded_documents):
    text_rows = []
    table_rows = []

    for document in downloaded_documents:
        if document["File Type"] != "pdf":
            continue

        pdf_file = Path(document["Local File"])
        try:
            with pdfplumber.open(pdf_file) as pdf:
                page_count = len(pdf.pages)
                text_page_limit = min(page_count, MAX_TEXT_PAGES_PER_PDF)
                table_page_limit = min(page_count, MAX_TABLE_PAGES_PER_PDF)
                print(
                    f"Extracting {pdf_file.name}: {text_page_limit} text pages, "
                    f"{table_page_limit} table pages, {page_count} total pages",
                    flush=True,
                )

                for page_number, page in enumerate(pdf.pages[:text_page_limit], start=1):
                    try:
                        page_text = clean_text(page.extract_text())
                    except Exception as error:
                        print(
                            f"Could not extract text from {pdf_file.name} page {page_number}: {error}",
                            flush=True,
                        )
                        continue

                    if has_text(page_text):
                        text_rows.append(
                            {
                                "document_id": document["document_id"],
                                "Category": document["Category"],
                                "Document Name": document["Document Name"],
                                "Total Pages": page_count,
                                "Pages Extracted": text_page_limit,
                                "Page Number": page_number,
                                "Page Text": page_text[:MAX_TEXT_CHARACTERS_PER_PAGE],
                            }
                        )

                for page_number, page in enumerate(pdf.pages[:table_page_limit], start=1):
                    try:
                        tables = page.extract_tables() or []

                        for table_number, table in enumerate(tables, start=1):
                            if not isinstance(table, list) or not table:
                                continue

                            header_row = table[0] if isinstance(table[0], list) else []
                            header = [clean_text(cell) for cell in header_row]
                            for row_number, row in enumerate(table[1:], start=1):
                                if not isinstance(row, list):
                                    continue

                                for column_index, value in enumerate(row):
                                    clean_value = clean_text(value)
                                    if not has_text(clean_value):
                                        continue

                                    column_name = header[column_index] if column_index < len(header) else np.nan
                                    if not has_text(column_name):
                                        column_name = f"Column {column_index + 1}"

                                    table_rows.append(
                                        {
                                            "document_id": document["document_id"],
                                            "Category": document["Category"],
                                            "Document Name": document["Document Name"],
                                            "Total Pages": page_count,
                                            "Pages Extracted": table_page_limit,
                                            "Page Number": page_number,
                                            "Table Number": table_number,
                                            "Row Number": row_number,
                                            "Column Name": column_name,
                                            "Value": clean_value,
                                        }
                                    )
                    except Exception as error:
                        print(
                            f"Skipped malformed tables in {pdf_file.name} page {page_number}: {error}",
                            flush=True,
                        )
                        continue
        except Exception as error:
            print(f"Could not extract {pdf_file.name}: {error}", flush=True)

    return text_rows, table_rows


def create_other_council_datasets():
    create_data_folders()
    print("Collecting non-CDF publication links from the council website.", flush=True)
    publications = collect_publication_documents()
    print("Collecting main council website pages.", flush=True)
    pages = collect_website_pages()
    print("Collecting council news updates.", flush=True)
    news = collect_news_updates()
    print("Collecting FAQs.", flush=True)
    faqs = collect_faq_rows()
    print(f"Downloading or reusing {len(publications)} non-CDF documents.", flush=True)
    downloaded = download_documents(publications)
    text_rows, table_rows = extract_pdf_text_and_tables(downloaded)

    save_dataframe(publications, OTHER_EXTRACTED_DIR / "other_publications_inventory.csv")
    save_dataframe(downloaded, OTHER_PROCESSED_DIR / "other_publications_inventory_clean.csv")
    save_dataframe(pages, OTHER_PROCESSED_DIR / "website_pages_clean.csv")
    save_dataframe(news, OTHER_PROCESSED_DIR / "news_updates_clean.csv")
    save_dataframe(faqs, OTHER_PROCESSED_DIR / "faqs_clean.csv")
    save_dataframe(text_rows, OTHER_PROCESSED_DIR / "document_text_extracts_clean.csv")
    save_dataframe(table_rows, OTHER_PROCESSED_DIR / "document_table_cells_clean.csv")

    print("Saved non-CDF source extracts. Run python -m src.category_pipelines to create category final CSVs.")


if __name__ == "__main__":
    create_other_council_datasets()
