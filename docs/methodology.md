# CDF Data Methodology

This document explains only the CDF part of the Mumbwa Town Council group project.

Other group members may add financial data, IDP data, council profile and administrative data, council meeting data, ward committee data, and other council records in their own files.

## Data Source

The CDF data came from PDF documents downloaded from the Mumbwa Town Council website.

The documents include grants, community projects, skills bursaries, secondary boarding school bursaries, and not-approved community projects for Mumbwa and Nangoma constituencies.

## PDF Collection

Original PDF files are kept in `data/raw/pdfs/`.

These files should not be changed because they are the source documents used for checking the data.

The collection process starts from the Mumbwa Town Council CDF Tracker page: `https://www.mumbwacouncil.gov.zm/?page_id=932`.

The source link list is saved in `data/raw/cdf_pdf_sources.csv`.

The collection script is `src/collector.py`.

## Recreated PDFs

Some PDF tables were scanned images and could not be extracted properly using `pdfplumber`.

For those files, the tables were recreated into machine-readable PDFs. The recreated PDFs are kept in `data/intermediate/reconstructed_pdfs/`.

## Table Extraction

Tables should be extracted from the original PDF when possible.

If the original PDF is scanned, tables should be extracted from the recreated PDF.

Extracted CSV files should be saved in `data/extracted/`.

For this CDF dataset, the recreated PDFs were used because they contain machine-readable tables. The extraction script is `src/extractor.py`.

The extracted CSV files use the pipe character `|` as the column separator.

The extracted files keep source details for checking. The cleaned and final files use a shorter `source_id` to avoid repeating long PDF names in every row.

## Data Cleaning

Cleaning is done with simple Python functions in `src/cleaner.py`.

The cleaning steps remove extra spaces, clean column names, remove empty rows, remove exact duplicate rows, and clean amount values.

Cleaned CSV files are saved in `data/processed/`.

The cleaning script is `src/cleaner.py`.

## Data Checking

Validation is done with simple warning functions in `src/validator.py`.

The checks show missing values, duplicate rows, missing required columns, and invalid amount values.

The validation functions do not delete suspicious data. Any warning should be checked against the original PDF.

## Final Datasets

Only files with the same type of CDF data should be combined.

For example, grants from Mumbwa and Nangoma can be combined into `data/final/grants.csv`.

Different data types should stay separate unless their columns make sense together.

For this project, the final files follow the assignment naming rule:

- `db-unza26-csc4792-mumbwa_town_council_cdf_grants.csv`
- `db-unza26-csc4792-mumbwa_town_council_cdf_community_projects.csv`
- `db-unza26-csc4792-mumbwa_town_council_cdf_not_approved_community_projects.csv`
- `db-unza26-csc4792-mumbwa_town_council_cdf_skills_bursaries.csv`
- `db-unza26-csc4792-mumbwa_town_council_cdf_secondary_bursaries.csv`

All final CSV files are saved in `data/final/` and use `|` as the separator.
