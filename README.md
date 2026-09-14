# mumbwa-town-council-dataset

Group 22 CSC_4792 mini project.

This repository is for the full Mumbwa Town Council group dataset.

Different group members can add different parts, such as financial data, IDP data, council profile and administrative data, council meeting data, ward committee data, and other council records.

The files added here focus on the CDF part of the project.

## CDF Folder Structure

- `data/raw/pdfs/` keeps the original PDF files.
- `data/intermediate/reconstructed_pdfs/` keeps recreated PDFs made from scanned tables.
- `data/extracted/` keeps CSV files extracted from PDFs.
- `data/processed/` keeps cleaned CSV files.
- `data/final/` keeps final datasets ready for analysis.

## Simple CDF Workflow

1. Download or save original PDFs in `data/raw/pdfs/`.
2. If a PDF table is scanned, recreate it and save it in `data/intermediate/reconstructed_pdfs/`.
3. Extract tables from PDFs and save CSV files in `data/extracted/`.
4. Clean the CSV files and save new files in `data/processed/`.
5. Combine matching datasets only, then save them in `data/final/`.

## How To Clean CSV Files

To run the full CDF workflow:

```bash
python -m src.collector
python -m src.extractor
python -m src.cleaner
python -m src.integrator
```

The collector starts from the Mumbwa Town Council CDF Tracker page and saves the PDF source links in `data/raw/cdf_pdf_sources.csv`.

The extractor creates pipe-separated CSV files in `data/extracted/`.

The cleaner creates pipe-separated CSV files in `data/processed/`.

The integrator creates final assignment-ready CSV files in `data/final/`.

To clean only extracted CSV files, run:

```bash
python -m src.cleaner
```

You can also open `notebooks/03_data_cleaning.ipynb` and run the cells one by one.

## Final CDF Datasets

- `db-unza26-csc4792-mumbwa_town_council_cdf_grants.csv`
- `db-unza26-csc4792-mumbwa_town_council_cdf_community_projects.csv`
- `db-unza26-csc4792-mumbwa_town_council_cdf_not_approved_community_projects.csv`
- `db-unza26-csc4792-mumbwa_town_council_cdf_skills_bursaries.csv`
- `db-unza26-csc4792-mumbwa_town_council_cdf_secondary_bursaries.csv`

## Notes

- Original PDFs should not be overwritten.
- Extracted CSV files should not be overwritten.
- Final CSV files use the pipe character `|` as the separator.
- The CDF final datasets use a short `source_id`. Full PDF source details are kept in `data/raw/cdf_pdf_sources.csv` and `docs/data_sources.md`.
- Other group members can add their own datasets without changing the CDF files.
- Validation checks only show warnings. They do not delete suspicious records.
