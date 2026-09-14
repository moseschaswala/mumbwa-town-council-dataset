import csv
import shutil
from pathlib import Path

import numpy as np
import pandas as pd

from src.paths import DATA_DIR, OTHER_DOCUMENTS_DIR, OTHER_PROCESSED_DIR, create_data_folders


PIPE = "|"

AGGREGATE_FINAL_FILES = [
    "db-unza26-csc4792-mumbwa_town_council_publications_inventory.csv",
    "db-unza26-csc4792-mumbwa_town_council_website_pages.csv",
    "db-unza26-csc4792-mumbwa_town_council_news_updates.csv",
    "db-unza26-csc4792-mumbwa_town_council_faqs.csv",
    "db-unza26-csc4792-mumbwa_town_council_document_text_extracts.csv",
    "db-unza26-csc4792-mumbwa_town_council_document_table_cells.csv",
]

CATEGORY_PIPELINES = {
    "financial_data": {
        "folder": "financial_data",
        "final_prefix": "financial_data",
        "document_categories": ["financial", "audit_report", "procurement_plan"],
        "page_ids": [],
        "include_news": False,
        "include_faqs": False,
    },
    "idp_data": {
        "folder": "idp_data",
        "final_prefix": "idp_data",
        "document_categories": ["idp"],
        "page_ids": ["zdsp", "projects"],
        "include_news": False,
        "include_faqs": False,
    },
    "council_meetings_minutes_data": {
        "folder": "council_meetings_minutes_data",
        "final_prefix": "council_meetings_minutes_data",
        "document_categories": ["council_minutes", "stakeholder_minutes"],
        "page_ids": [],
        "include_news": False,
        "include_faqs": False,
    },
    "council_structure_management_data": {
        "folder": "council_structure_management_data",
        "final_prefix": "council_structure_management_data",
        "document_categories": [],
        "page_ids": [
            "home",
            "who_we_are",
            "senior_management",
            "departments",
            "civic_leaders",
            "council_chairman",
            "nangoma_constituency",
            "mumbwa_central_constituency",
            "standing_committees",
            "mandate",
            "contact_us",
        ],
        "include_news": False,
        "include_faqs": False,
    },
    "public_services_legal_data": {
        "folder": "public_services_legal_data",
        "final_prefix": "public_services_legal_data",
        "document_categories": [
            "legislation",
            "grievance",
            "solid_waste",
            "public_relations",
            "other_publication",
        ],
        "page_ids": ["services", "cash_for_work", "application_forms", "faqs"],
        "include_news": True,
        "include_faqs": True,
    },
}


def clean_dataframe(df):
    """Clean values without changing column names or source meaning."""
    df = df.copy()

    if df.empty:
        return df

    for column in df.columns:
        if pd.api.types.is_object_dtype(df[column]):
            df[column] = df[column].map(lambda value: value.strip() if isinstance(value, str) else value)

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


def save_csv_when_not_empty(df, output_file):
    output_file = Path(output_file)
    cleaned = clean_dataframe(df)

    if cleaned.empty:
        if output_file.exists():
            output_file.unlink()
        return cleaned

    return save_csv(cleaned, output_file)


def read_clean_csv(file_name):
    path = OTHER_PROCESSED_DIR / file_name
    if not path.exists():
        return pd.DataFrame()

    return pd.read_csv(path, sep=PIPE)


def category_root(config):
    return DATA_DIR / config["folder"]


def create_category_folders(config):
    root = category_root(config)
    folders = [
        root / "raw",
        root / "raw" / "documents",
        root / "intermediate",
        root / "extracted",
        root / "processed",
        root / "final",
    ]

    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)


def copy_category_documents(publications, config):
    documents_dir = category_root(config) / "raw" / "documents"

    for _, row in publications.iterrows():
        document_name = row.get("Document Name")
        if not isinstance(document_name, str):
            continue

        existing_category_file = documents_dir / document_name
        if existing_category_file.exists():
            continue

        source_file = OTHER_DOCUMENTS_DIR / document_name
        destination_file = documents_dir / document_name
        if source_file.exists():
            shutil.copy2(source_file, destination_file)


def filter_by_document_ids(df, document_ids):
    if df.empty or "document_id" not in df.columns:
        return pd.DataFrame(columns=df.columns)

    return df[df["document_id"].isin(document_ids)].copy()


def filter_pages(pages, page_ids):
    if pages.empty or "Page ID" not in pages.columns:
        return pd.DataFrame(columns=pages.columns)

    return pages[pages["Page ID"].isin(page_ids)].copy()


def write_document_pipeline(config, publications, text_extracts, table_cells):
    root = category_root(config)
    categories = config["document_categories"]

    if not categories:
        return []

    category_publications = publications[publications["Category"].isin(categories)].copy()
    document_ids = set(category_publications["document_id"].dropna())
    category_text = filter_by_document_ids(text_extracts, document_ids)
    category_tables = filter_by_document_ids(table_cells, document_ids)

    written_final_files = []

    save_csv(category_publications, root / "raw" / "publication_sources.csv")
    copy_category_documents(category_publications, config)

    save_csv(category_publications, root / "intermediate" / "selected_publications.csv")
    save_csv_when_not_empty(category_text, root / "intermediate" / "document_text_extracts_raw.csv")
    save_csv_when_not_empty(category_tables, root / "intermediate" / "document_table_cells_raw.csv")

    save_csv(category_publications, root / "extracted" / "publication_inventory.csv")
    save_csv_when_not_empty(category_text, root / "extracted" / "document_text_extracts.csv")
    save_csv_when_not_empty(category_tables, root / "extracted" / "document_table_cells.csv")

    clean_publications = save_csv(category_publications, root / "processed" / "publication_inventory_clean.csv")
    clean_text = save_csv_when_not_empty(category_text, root / "processed" / "document_text_extracts_clean.csv")
    clean_tables = save_csv_when_not_empty(category_tables, root / "processed" / "document_table_cells_clean.csv")

    final_outputs = {
        f"db-unza26-csc4792-mumbwa_town_council_{config['final_prefix']}_publications.csv": clean_publications,
        f"db-unza26-csc4792-mumbwa_town_council_{config['final_prefix']}_document_text_extracts.csv": clean_text,
        f"db-unza26-csc4792-mumbwa_town_council_{config['final_prefix']}_document_table_cells.csv": clean_tables,
    }

    for file_name, df in final_outputs.items():
        category_final = root / "final" / file_name
        cleaned = clean_dataframe(df)

        if cleaned.empty:
            for stale_file in [category_final]:
                if stale_file.exists():
                    stale_file.unlink()
            continue

        save_csv(cleaned, category_final)
        written_final_files.append(category_final)

    return written_final_files


def write_page_pipeline(config, pages):
    root = category_root(config)
    category_pages = filter_pages(pages, config["page_ids"])

    if category_pages.empty:
        return []

    save_csv(category_pages, root / "raw" / "source_pages.csv")
    save_csv(category_pages, root / "intermediate" / "selected_website_pages.csv")
    save_csv(category_pages, root / "extracted" / "website_pages.csv")
    clean_pages = save_csv(category_pages, root / "processed" / "website_pages_clean.csv")

    file_name = f"db-unza26-csc4792-mumbwa_town_council_{config['final_prefix']}_website_pages.csv"
    category_final = root / "final" / file_name
    cleaned = save_csv(clean_pages, category_final)
    return [category_final]


def write_news_pipeline(config, news):
    if not config["include_news"] or news.empty:
        return []

    root = category_root(config)
    save_csv(news, root / "raw" / "news_sources.csv")
    save_csv(news, root / "intermediate" / "news_updates_raw.csv")
    save_csv(news, root / "extracted" / "news_updates.csv")
    clean_news = save_csv(news, root / "processed" / "news_updates_clean.csv")

    file_name = f"db-unza26-csc4792-mumbwa_town_council_{config['final_prefix']}_news_updates.csv"
    category_final = root / "final" / file_name
    cleaned = save_csv(clean_news, category_final)
    return [category_final]


def write_faq_pipeline(config, faqs):
    if not config["include_faqs"] or faqs.empty:
        return []

    root = category_root(config)
    save_csv(faqs, root / "raw" / "faq_sources.csv")
    save_csv(faqs, root / "intermediate" / "faqs_raw.csv")
    save_csv(faqs, root / "extracted" / "faqs.csv")
    clean_faqs = save_csv(faqs, root / "processed" / "faqs_clean.csv")

    file_name = f"db-unza26-csc4792-mumbwa_town_council_{config['final_prefix']}_faqs.csv"
    category_final = root / "final" / file_name
    cleaned = save_csv(clean_faqs, category_final)
    return [category_final]


def remove_old_aggregate_final_files():
    return None


def create_category_pipelines():
    create_data_folders()

    publications = read_clean_csv("other_publications_inventory_clean.csv")
    pages = read_clean_csv("website_pages_clean.csv")
    news = read_clean_csv("news_updates_clean.csv")
    faqs = read_clean_csv("faqs_clean.csv")
    text_extracts = read_clean_csv("document_text_extracts_clean.csv")
    table_cells = read_clean_csv("document_table_cells_clean.csv")

    if publications.empty and pages.empty:
        raise FileNotFoundError(
            "No non-CDF processed source files were found. Run python -m src.other_council_data first."
        )

    remove_old_aggregate_final_files()
    written_files = []

    for config in CATEGORY_PIPELINES.values():
        create_category_folders(config)
        written_files.extend(write_document_pipeline(config, publications, text_extracts, table_cells))
        written_files.extend(write_page_pipeline(config, pages))
        written_files.extend(write_news_pipeline(config, news))
        written_files.extend(write_faq_pipeline(config, faqs))

    for output_file in written_files:
        df = pd.read_csv(output_file, sep=PIPE)
        print(f"Created {output_file.name}: {len(df)} rows")

    return written_files


if __name__ == "__main__":
    create_category_pipelines()
