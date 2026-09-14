import re
from pathlib import Path

import pandas as pd
import pdfplumber

from src.paths import EXTRACTED_DIR, RECONSTRUCTED_PDF_DIR, create_data_folders


PDF_DETAILS = {
    "2025-approve-cdf-grants-for-nangoma-constituency-recreated_tables.pdf": {
        "category": "grants",
        "constituency": "Nangoma",
        "year": 2025,
        "source_id": "cdf_grants_nangoma_2025",
        "source_document": "2025-Approve-CDF-Grants-for-Nangoma-Constituency.pdf",
    },
    "2025-approved-cdf-grants-for-mumbwa-constituency-recreated_tables.pdf": {
        "category": "grants",
        "constituency": "Mumbwa",
        "year": 2025,
        "source_id": "cdf_grants_mumbwa_2025",
        "source_document": "2025-Approved-CDF-Grants-for-Mumbwa-Constituency.pdf",
    },
    "2025_approved_community_projects_nangoma_constituency_recreated_tables.pdf": {
        "category": "community_projects",
        "constituency": "Nangoma",
        "year": 2025,
        "source_id": "cdf_community_projects_nangoma_2025",
        "source_document": "2025-Approved-Community-Projects-Nangoma-Constituency.pdf",
    },
    "2025_approved_community_projects_mumbwa_central_recreated_tables.pdf": {
        "category": "community_projects",
        "constituency": "Mumbwa",
        "year": 2025,
        "source_id": "cdf_community_projects_mumbwa_2025",
        "source_document": "2025-Approved-Community-Projects-Mumbwa-Central.pdf",
    },
    "not-approved-community-projects-nangoma-recreated-tables.pdf": {
        "category": "not_approved_community_projects",
        "constituency": "Nangoma",
        "year": 2025,
        "source_id": "cdf_not_approved_projects_nangoma_2025",
        "source_document": "NOT-APPROVED-COMMUNITY-PROJECTS-NANGOMA.pdf",
    },
    "not-approved-community-projects-mumbwa-recreated-tables.pdf": {
        "category": "not_approved_community_projects",
        "constituency": "Mumbwa",
        "year": 2025,
        "source_id": "cdf_not_approved_projects_mumbwa_2025",
        "source_document": "NOT-APPROVED-COMMUNITY-PROJECTS-MUMBWA.pdf",
    },
    "2025-approved-cdf-skills-development-bursaries-for-nangoma-constituency-recreated_tables.pdf": {
        "category": "skills_bursaries",
        "constituency": "Nangoma",
        "year": 2025,
        "source_id": "cdf_skills_bursaries_nangoma_2025",
        "source_document": "2025-Approved-CDF-Skills-Development-Bursaries-for-Nangoma-Constituency.pdf",
    },
    "2025-approved-cdf-skills-development-bursaries-for-mumbwa-constituency-recreated_tables.pdf": {
        "category": "skills_bursaries",
        "constituency": "Mumbwa",
        "year": 2025,
        "source_id": "cdf_skills_bursaries_mumbwa_2025",
        "source_document": "2025-Approved-CDF-Skills-Development-Bursaries-for-Mumbwa-Constituency.pdf",
    },
    "2025-approved-cdf-secondary-boarding-school-bursaries-for-nangoma-constituency-recreated_tables.pdf": {
        "category": "secondary_bursaries",
        "constituency": "Nangoma",
        "year": 2025,
        "source_id": "cdf_secondary_bursaries_nangoma_2025",
        "source_document": "2025-Approved-CDF-Secondary-Boarding-School-Bursaries-for-Nangoma-Constituency.pdf",
    },
    "2025-approved-cdf-secondary-boarding-school-bursaries-for-mumbwa-constituency-recreated_tables.pdf": {
        "category": "secondary_bursaries",
        "constituency": "Mumbwa",
        "year": 2025,
        "source_id": "cdf_secondary_bursaries_mumbwa_2025",
        "source_document": "2025-Approved-CDF-Secondary-Boarding-School-Bursaries-for-Mumbwa-Constituency.pdf",
    },
}


def clean_cell(value):
    if value is None:
        return ""

    text = str(value)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_column_name(value, index):
    name = clean_cell(value).lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = name.strip("_")

    if not name:
        name = f"column_{index + 1}"

    return name


def make_unique_columns(header):
    columns = []
    used_columns = {}

    for index, value in enumerate(header):
        column = clean_column_name(value, index)

        if column in used_columns:
            used_columns[column] += 1
            column = f"{column}_{used_columns[column]}"
        else:
            used_columns[column] = 1

        columns.append(column)

    return columns


def looks_like_header(row):
    first_cell = clean_cell(row[0]).lower() if row else ""
    joined = " ".join(clean_cell(cell).lower() for cell in row)

    if first_cell in ["no", "no.", "s/n", "sn"]:
        return True

    header_words = ["name of", "project", "constituency", "ward", "district"]
    return sum(word in joined for word in header_words) >= 3


def find_header_row(table):
    for index, row in enumerate(table[:4]):
        if looks_like_header(row):
            return index

    return None


def is_repeated_header(row):
    return looks_like_header(row)


def extract_pdf_tables(pdf_file):
    rows = []
    current_columns = None

    with pdfplumber.open(pdf_file) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables() or []

            for table_number, table in enumerate(tables, start=1):
                if not table:
                    continue

                header_index = find_header_row(table)

                if header_index is not None:
                    current_columns = make_unique_columns(table[header_index])
                    data_rows = table[header_index + 1 :]
                elif current_columns is not None:
                    data_rows = table
                else:
                    current_columns = make_unique_columns(table[0])
                    data_rows = table[1:]

                for row in data_rows:
                    if not row or is_repeated_header(row):
                        continue

                    clean_row = [clean_cell(cell) for cell in row]
                    if not any(clean_row):
                        continue

                    while len(clean_row) < len(current_columns):
                        clean_row.append("")

                    clean_row = clean_row[: len(current_columns)]
                    row_data = dict(zip(current_columns, clean_row))
                    row_data["page_number"] = page_number
                    row_data["table_number"] = table_number
                    rows.append(row_data)

    return pd.DataFrame(rows)


def output_name(pdf_file, details):
    return f"{details['year']}_{details['constituency'].lower()}_{details['category']}.csv"


def extract_all_reconstructed_pdfs(input_dir=RECONSTRUCTED_PDF_DIR, output_dir=EXTRACTED_DIR):
    create_data_folders()
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_files = []

    for pdf_file in sorted(input_dir.glob("*.pdf")):
        details = PDF_DETAILS.get(pdf_file.name.lower())
        if details is None:
            print(f"Skipping unknown PDF: {pdf_file.name}")
            continue

        print(f"Extracting: {pdf_file.name}")
        df = extract_pdf_tables(pdf_file)
        df["source_id"] = details["source_id"]
        df["source_document"] = details["source_document"]
        df["constituency"] = details["constituency"]
        df["year"] = details["year"]
        df["cdf_category"] = details["category"]
        df["extraction_method"] = "recreated_pdf"

        output_file = output_dir / output_name(pdf_file, details)
        if output_file.exists():
            print(f"Already exists, skipping: {output_file}")
            print()
            continue

        df.to_csv(output_file, index=False, sep="|")
        print(f"Rows extracted: {len(df)}")
        print(f"Saved to: {output_file}")
        print()
        output_files.append(output_file)

    return output_files


if __name__ == "__main__":
    extract_all_reconstructed_pdfs()
