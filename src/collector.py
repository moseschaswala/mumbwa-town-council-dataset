from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

from src.paths import RAW_PDF_DIR, SOURCE_LIST_FILE, create_data_folders


CDF_TRACKER_URL = "https://www.mumbwacouncil.gov.zm/?page_id=932"

EXPECTED_CDF_LINKS = {
    "2025-Approved-Community-Projects-Mumbwa-Central.pdf": {
        "source_id": "cdf_community_projects_mumbwa_2025",
        "category": "Community Projects",
        "constituency": "Mumbwa",
        "year": 2025,
    },
    "NOT-APPROVED-COMMUNITY-PROJECTS-MUMBWA.pdf": {
        "source_id": "cdf_not_approved_projects_mumbwa_2025",
        "category": "Not Approved Community Projects",
        "constituency": "Mumbwa",
        "year": 2025,
    },
    "2025-Approved-CDF-Skills-Development-Bursaries-for-Mumbwa-Constituency.pdf": {
        "source_id": "cdf_skills_bursaries_mumbwa_2025",
        "category": "Skills Bursaries",
        "constituency": "Mumbwa",
        "year": 2025,
    },
    "2025-Approved-CDF-Secondary-Boarding-School-Bursaries-for-Mumbwa-Constituency.pdf": {
        "source_id": "cdf_secondary_bursaries_mumbwa_2025",
        "category": "Secondary Bursaries",
        "constituency": "Mumbwa",
        "year": 2025,
    },
    "2025-Approved-CDF-Grants-for-Mumbwa-Constituency.pdf": {
        "source_id": "cdf_grants_mumbwa_2025",
        "category": "Grants",
        "constituency": "Mumbwa",
        "year": 2025,
    },
    "2025-Approved-Community-Projects-Nangoma-Constituency.pdf": {
        "source_id": "cdf_community_projects_nangoma_2025",
        "category": "Community Projects",
        "constituency": "Nangoma",
        "year": 2025,
    },
    "NOT-APPROVED-COMMUNITY-PROJECTS-NANGOMA.pdf": {
        "source_id": "cdf_not_approved_projects_nangoma_2025",
        "category": "Not Approved Community Projects",
        "constituency": "Nangoma",
        "year": 2025,
    },
    "2025-Approve-CDF-Grants-for-Nangoma-Constituency.pdf": {
        "source_id": "cdf_grants_nangoma_2025",
        "category": "Grants",
        "constituency": "Nangoma",
        "year": 2025,
    },
    "2025-Approved-CDF-Skills-Development-Bursaries-for-Nangoma-Constituency.pdf": {
        "source_id": "cdf_skills_bursaries_nangoma_2025",
        "category": "Skills Bursaries",
        "constituency": "Nangoma",
        "year": 2025,
    },
    "2025-Approved-CDF-Secondary-Boarding-School-Bursaries-for-Nangoma-Constituency.pdf": {
        "source_id": "cdf_secondary_bursaries_nangoma_2025",
        "category": "Secondary Bursaries",
        "constituency": "Nangoma",
        "year": 2025,
    },
}


def find_pdf_links(page_url=CDF_TRACKER_URL):
    """Visit the CDF Tracker page and find PDF links."""
    response = requests.get(page_url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    pdf_links = []

    for link in soup.find_all("a", href=True):
        href = link["href"]
        text = link.get_text(" ", strip=True)

        if ".pdf" not in href.lower():
            continue

        full_url = urljoin(page_url, href)
        file_name = full_url.split("/")[-1]

        if file_name in EXPECTED_CDF_LINKS:
            details = EXPECTED_CDF_LINKS[file_name]
            pdf_links.append(
                {
                    "source_id": details["source_id"],
                    "document": file_name,
                    "category": details["category"],
                    "constituency": details["constituency"],
                    "year": details["year"],
                    "extraction_method": "recreated_pdf",
                    "title_on_site": text,
                    "source_url": full_url,
                    "tracker_page": page_url,
                }
            )

    return pdf_links


def save_source_list(pdf_links, output_file=SOURCE_LIST_FILE):
    """Save the list of PDF source links."""
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(pdf_links)
    df.to_csv(output_file, index=False, sep="|")
    return output_file


def download_pdfs(pdf_links, output_dir=RAW_PDF_DIR):
    """Download PDFs without overwriting files that already exist."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    downloaded_files = []

    for pdf_link in pdf_links:
        file_name = pdf_link["document"]
        output_file = output_dir / file_name

        if output_file.exists():
            print(f"Already exists, skipping: {output_file}")
            downloaded_files.append(output_file)
            continue

        print(f"Downloading: {file_name}")
        response = requests.get(pdf_link["source_url"], timeout=60)
        response.raise_for_status()

        output_file.write_bytes(response.content)
        print(f"Saved to: {output_file}")
        downloaded_files.append(output_file)

    return downloaded_files


def collect_cdf_pdfs():
    """Collect source links and download the CDF PDFs."""
    create_data_folders()

    pdf_links = find_pdf_links()
    source_file = save_source_list(pdf_links)
    downloaded_files = download_pdfs(pdf_links)

    print(f"Source list saved to: {source_file}")
    print(f"PDF links found: {len(pdf_links)}")
    print(f"PDF files available: {len(downloaded_files)}")

    return downloaded_files


if __name__ == "__main__":
    collect_cdf_pdfs()
