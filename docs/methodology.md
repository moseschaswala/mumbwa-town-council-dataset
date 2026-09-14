# Dataset Methodology

This document explains how the Mumbwa Town Council group dataset is organized and prepared. The dataset is a multi-table dataset, not one combined CSV, because CDF records, IDP plans, council structure records, meeting resolutions, and financial records describe different subjects.

## Source Collection

Source records are collected from the official Mumbwa Town Council website and council documents. Category folders keep the raw source material separate from cleaned and final outputs.

Current source categories:

- `data/CDF/raw/` contains CDF source links and original PDF files.
- `data/IDP/raw/` contains the Mumbwa IDP PDF source.
- `data/Council_Structure_and_Management/raw/` is reserved for council profile, management, councillor, and ward committee source material.
- `data/Meetings_and_Minutes/raw/` is reserved for meeting and council resolution source material.
- `data/Finance/raw/` is prepared for budget, revenue, audit, procurement, and related financial sources that will be added later.
- `data/Public_Services_and_Legal_Data/` is prepared for public service and legal records.

## Notebooks and Scripts

The notebooks in `notebooks/` show the category workflows used by group members. The Python modules in `src/` contain reusable helpers for collection, extraction, cleaning, integration, and validation.

The CDF notebook shows a complete workflow from web scraping, PDF downloading, table extraction, cleaning, CSV creation, and final data production. Other category notebooks should follow the same general structure where possible:

1. Define source pages or documents.
2. Download or load source documents.
3. Extract text or tables.
4. Clean column names and values.
5. Save intermediate files when useful.
6. Save final analysis-ready CSV files to the category `final/` folder.
7. Validate row counts, duplicate rows, empty columns, and required fields.

## CDF Processing

The CDF data came from PDF documents downloaded from the Mumbwa Town Council CDF Tracker page. Some PDF tables were scanned or difficult to extract directly, so recreated machine-readable PDFs were produced and stored in `data/CDF/intermediate/reconstructed_pdfs/`.

The CDF process uses:

- `src/collector.py` for source collection.
- `src/extractor.py` for PDF table extraction.
- `src/cleaner.py` for cleaning extracted tables.
- `src/integrator.py` for combining same-type CDF records.
- `src/validator.py` for basic validation checks.

Final CDF files are saved in `data/CDF/final/`.

## IDP Processing

The IDP data are extracted from the Mumbwa IDP PDF and selected council web pages. The final IDP layer was cleaned by:

- Removing duplicate final exports.
- Removing empty or broken final exports.
- Fixing an incorrect `csc4794` filename typo.
- Removing repeated header rows that appeared as data.
- Standardizing column names to lowercase `snake_case`.
- Removing exact duplicate rows.
- Fixing text encoding artifacts where possible.
- Repairing one shifted row in the forest reserves table.

Final IDP files are saved in `data/IDP/final/`.

## Council Structure and Management

Council structure and management records are stored separately from CDF and IDP records. These files cover administrative, councillor, ward development committee, and related management information where available. Final files are saved in `data/Council_Structure_and_Management/final/`.

## Meetings and Minutes

Meeting and resolution data are stored in `data/Meetings_and_Minutes/final/`. The current public council resolutions file should be treated as a text-extraction dataset. Some rows may contain partial resolution text and should be manually checked against the source document before formal publication.

## Finance Data

Finance data has not yet been added, but the repository already contains `data/Finance/raw/`, `data/Finance/processed/`, and `data/Finance/final/`. When finance records are added, they should follow the same structure:

- Keep source documents in `raw/`.
- Keep working cleaned files in `processed/`.
- Put only publication-ready tables in `final/`.
- Add finance table entries to `docs/dataset_manifest.csv`.
- Add finance column definitions to `docs/data_dictionary.md`.
- Add finance sources to `docs/data_sources.md`.
- Update validation results in `docs/validation_report.md`.

## Final Dataset Rules

Only files with the same meaning and compatible columns should be combined. Different record types should stay separate. For example, CDF grants, CDF bursaries, IDP implementation plans, revenue projections, school infrastructure tables, council resolutions, and finance tables should remain separate final CSV tables.

All final CSV files use `|` as the separator.

## Validation

Validation checks include:

- Whether each final CSV can be read with `sep="|"`.
- Row and column counts.
- Exact duplicate rows.
- Empty columns.
- Duplicate-looking filenames.
- Obvious filename errors.
- Category-level final-table totals.

The current validation summary is stored in `docs/validation_report.md`.

## Publication Note

Before public publication, the group should review sensitive personal fields in CDF bursary and grant data. Public records can still contain personal information, so a redacted public version may be safer for Kaggle or other open platforms.
