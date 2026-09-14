import csv
import html
import re
from pathlib import Path

import numpy as np
import pandas as pd
import pdfplumber
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Table, TableStyle

from src.paths import DATA_DIR


PIPE = "|"
MAX_PAGES_PER_DOCUMENT = 20

CATEGORY_FOLDERS = [
    "financial_data",
    "idp_data",
    "council_meetings_minutes_data",
    "public_services_legal_data",
]


def clean_dataframe(df):
    df = df.copy()

    if df.empty:
        return df

    for column in df.columns:
        if pd.api.types.is_object_dtype(df[column]):
            df[column] = df[column].map(lambda value: re.sub(r"\s+", " ", value).strip() if isinstance(value, str) else value)

    df = df.replace(r"^\s*$", np.nan, regex=True)
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")
    df = df.drop_duplicates()
    return df.reset_index(drop=True)


def save_csv(df, output_file):
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df = clean_dataframe(df)
    df.to_csv(output_file, index=False, sep=PIPE, quoting=csv.QUOTE_MINIMAL)
    return df


def read_csv_if_exists(path):
    path = Path(path)
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep=PIPE)


def document_ids_with_tables(category_root):
    table_file = category_root / "processed" / "document_table_cells_clean.csv"
    table_df = read_csv_if_exists(table_file)
    if table_df.empty or "document_id" not in table_df.columns:
        return set()
    return set(table_df["document_id"].dropna().astype(str))


def extract_lines_from_pdf(pdf_file, document_id, category, document_name):
    rows = []

    try:
        with pdfplumber.open(pdf_file) as pdf:
            total_pages = len(pdf.pages)
            pages_to_extract = min(total_pages, MAX_PAGES_PER_DOCUMENT)

            for page_index, page in enumerate(pdf.pages[:pages_to_extract], start=1):
                text = page.extract_text() or ""
                lines = [line.strip() for line in text.splitlines() if line.strip()]

                for line_number, line in enumerate(lines, start=1):
                    rows.append(
                        {
                            "document_id": document_id,
                            "Category": category,
                            "Document Name": document_name,
                            "Total Pages": total_pages,
                            "Pages Extracted": pages_to_extract,
                            "Page Number": page_index,
                            "Line Number": line_number,
                            "Transcribed Text": line,
                        }
                    )
    except Exception as error:
        rows.append(
            {
                "document_id": document_id,
                "Category": category,
                "Document Name": document_name,
                "Total Pages": np.nan,
                "Pages Extracted": 0,
                "Page Number": np.nan,
                "Line Number": np.nan,
                "Transcribed Text": f"EXTRACTION ERROR: {error}",
            }
        )

    return rows


def create_recreated_pdf(rows, output_file):
    if not rows:
        return

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    body_style = styles["BodyText"]
    body_style.fontSize = 6
    body_style.leading = 7

    story = []
    grouped = {}
    for row in rows:
        grouped.setdefault(row["Page Number"], []).append(row)

    for page_number, page_rows in grouped.items():
        title = f"{page_rows[0]['Document Name']} - page {page_number}"
        story.append(Paragraph(title, styles["Heading3"]))
        table_data = [["Line Number", "Transcribed Text"]]
        for row in page_rows:
            table_data.append([str(row["Line Number"]), Paragraph(html.escape(row["Transcribed Text"]), body_style)])

        table = Table(table_data, colWidths=[60, 700], repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("FONTSIZE", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.append(table)
        story.append(PageBreak())

    document = SimpleDocTemplate(str(output_file), pagesize=landscape(A4), leftMargin=18, rightMargin=18, topMargin=18, bottomMargin=18)
    document.build(story)


def recreate_category_tables(category_folder):
    category_root = DATA_DIR / category_folder
    publications = read_csv_if_exists(category_root / "processed" / "publication_inventory_clean.csv")
    if publications.empty:
        return []

    table_document_ids = document_ids_with_tables(category_root)
    all_rows = []
    review_rows = []

    for _, publication in publications.iterrows():
        document_id = str(publication["document_id"])
        if document_id in table_document_ids:
            continue

        document_name = publication["Document Name"]
        if not str(document_name).lower().endswith(".pdf"):
            review_rows.append(
                {
                    "document_id": document_id,
                    "Document Name": document_name,
                    "Reason": "not_pdf",
                }
            )
            continue

        pdf_file = category_root / "raw" / "documents" / document_name
        if not pdf_file.exists():
            review_rows.append(
                {
                    "document_id": document_id,
                    "Document Name": document_name,
                    "Reason": "source_pdf_missing",
                }
            )
            continue

        rows = extract_lines_from_pdf(pdf_file, document_id, publication["Category"], document_name)
        usable_rows = [row for row in rows if row.get("Transcribed Text") and not str(row["Transcribed Text"]).startswith("EXTRACTION ERROR")]

        if not usable_rows:
            review_rows.append(
                {
                    "document_id": document_id,
                    "Document Name": document_name,
                    "Reason": "no_extractable_text",
                }
            )
            continue

        all_rows.extend(usable_rows)
        recreated_pdf = category_root / "intermediate" / "recreated_tables" / f"{Path(document_name).stem}_recreated_text_table.pdf"
        create_recreated_pdf(usable_rows, recreated_pdf)

    recreated_df = pd.DataFrame(all_rows)
    review_df = pd.DataFrame(review_rows)

    if not recreated_df.empty:
        save_csv(recreated_df, category_root / "intermediate" / "recreated_tables" / "recreated_text_table_lines_raw.csv")
        save_csv(recreated_df, category_root / "extracted" / "recreated_text_table_lines.csv")
        processed = save_csv(recreated_df, category_root / "processed" / "recreated_text_table_lines_clean.csv")
        final_name = f"db-unza26-csc4792-mumbwa_town_council_{category_folder}_recreated_text_table_lines.csv"
        final_df = save_csv(processed, category_root / "final" / final_name)
        print(f"Created {final_name}: {len(final_df)} rows")

    if not review_df.empty:
        save_csv(review_df, category_root / "processed" / "manual_review_needed_for_unreadable_tables.csv")
        print(f"Review needed in {category_folder}: {len(review_df)} documents")

    return all_rows


def recreate_unreadable_tables():
    outputs = []
    for category_folder in CATEGORY_FOLDERS:
        outputs.extend(recreate_category_tables(category_folder))
    return outputs


if __name__ == "__main__":
    recreate_unreadable_tables()
