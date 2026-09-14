from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"

RAW_DIR = DATA_DIR / "raw"
RAW_PDF_DIR = RAW_DIR / "pdfs"
SOURCE_LIST_FILE = RAW_DIR / "cdf_pdf_sources.csv"
OTHER_DOCUMENTS_DIR = RAW_DIR / "other_documents"

INTERMEDIATE_DIR = DATA_DIR / "intermediate"
RECONSTRUCTED_PDF_DIR = INTERMEDIATE_DIR / "reconstructed_pdfs"

EXTRACTED_DIR = DATA_DIR / "extracted"
PROCESSED_DIR = DATA_DIR / "processed"
FINAL_DIR = DATA_DIR / "final"
OTHER_EXTRACTED_DIR = EXTRACTED_DIR / "other_council_data"
OTHER_PROCESSED_DIR = PROCESSED_DIR / "other_council_data"


def create_data_folders():
    """Create the main CDF data folders if they do not exist."""
    folders = [
        RAW_PDF_DIR,
        OTHER_DOCUMENTS_DIR,
        RECONSTRUCTED_PDF_DIR,
        EXTRACTED_DIR,
        OTHER_EXTRACTED_DIR,
        PROCESSED_DIR,
        OTHER_PROCESSED_DIR,
        FINAL_DIR,
    ]

    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
