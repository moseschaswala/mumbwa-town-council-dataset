# mumbwa-town-council-dataset

Group 22 CSC 4792 mini project dataset for Mumbwa Town Council public records.

The repository stores source documents, notebooks, scripts, documentation, and final pipe-separated CSV tables for council-related records. The dataset is organized by topic so each group member can work inside their assigned folder without mixing unrelated data.

## Current Dataset Coverage

| Category | Final CSV files | Final rows | Status |
| --- | ---: | ---: | --- |
| CDF | 5 | 1,871 | Ready for analysis |
| IDP | 23 | 546 | ready for analysis |
| Council Structure and Management | 2 | 26 | Ready for analysis |
| Meetings and Minutes | 1 | 119 | Needs manual text-quality review |
| Finance | 3 |  | ready for analysis |

The full table list is in `docs/dataset_manifest.csv`.

## Repository Structure

```text
data/
  CDF/
    raw/
    extracted/
    processed/
    intermediate/
    final/
  Council_Structure_and_Management/
    raw/
    processed/
    final/
  Finance/
    raw/
    processed/
    final/
  IDP/
    raw/
    processed/
    final/
  Meetings_and_Minutes/
    raw/
    processed/
    final/
  Public_Services_and_Legal_Data/
docs/
notebooks/
src/
```

## Data Format

All final CSV files use the pipe character `|` as the separator. This is used because several council text fields contain commas.

```python
import pandas as pd

df = pd.read_csv(
    "data/CDF/final/db-unza26-csc4792-mumbwa_town_council_cdf_grants.csv",
    sep="|"
)
```

## Documentation

- `docs/dataset_manifest.csv` lists every final table, row count, column count, file path, and column names.
- `docs/data_sources.md` describes the main source locations and category-specific source handling.
- `docs/data_dictionary.md` explains the main column groups used across the final data.
- `docs/methodology.md` explains collection, extraction, cleaning, validation, and final dataset creation.
- `docs/validation_report.md` summarizes the latest final-table validation checks.
- `docs/kaggle_dataset_description.md` is a draft description for publishing the dataset.

## Privacy Note

Some public CDF bursary records include personal information such as student or pupil names, dates of birth, NRC numbers, and contact persons. Before publishing to a public platform, the group should decide whether to publish the original files or create a redacted public version.

## Finance Data

The Finance folder is already part of the dataset structure. When financial data is added, place source files in `data/Finance/raw/`, cleaned working files in `data/Finance/processed/`, final CSV files in `data/Finance/final/`, and update `docs/dataset_manifest.csv`, `docs/data_dictionary.md`, `docs/data_sources.md`, and `docs/validation_report.md`.
