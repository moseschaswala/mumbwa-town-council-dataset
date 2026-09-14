# Validation Report

This report summarizes the latest validation pass over the final CSV layer.

## Final Dataset Summary

| Category | Final CSV files | Rows | Columns across files | Duplicate rows | Empty columns |
| --- | ---: | ---: | ---: | ---: | ---: |
| CDF | 5 | 1,871 | 85 | 0 | 6 |
| Council Structure and Management | 2 | 26 | 11 | 0 | 0 |
| IDP | 23 | 546 | 178 | 0 | 0 |
| Meetings and Minutes | 1 | 119 | 6 | 0 | 0 |
| Finance | 0 | 0 | 0 | 0 | 0 |
| Public Services and Legal Data | 0 | 0 | 0 | 0 | 0 |

Total current final tables: 31.

Total current final rows: 2,562.

## Cleaning Actions Completed

- Removed duplicate IDP final exports ending in `(1).csv`.
- Removed an empty IDP final export for future demand for services.
- Removed a broken partial IDP human and social development export because a clean version of the same topic exists.
- Removed a duplicate water-supply table that had a misleading production-trend filename.
- Renamed the cash-for-work file from `csc4794` to `csc4792`.
- Shortened redundant IDP filenames that repeated `db_unza26_csc4792`.
- Standardized IDP column names to lowercase `snake_case`.
- Removed repeated IDP header rows that appeared as data.
- Removed exact duplicate IDP rows.
- Fixed visible text encoding artifacts where possible.
- Repaired a shifted row in the forest reserves final table.
- Created `docs/dataset_manifest.csv`.

## Remaining Notes

The CDF community projects and not-approved community projects files keep a few fully blank columns. These columns are retained because the CDF tables were combined from source PDFs with related but not perfectly identical structures.

The public council resolutions table should receive manual text review before formal publication because some rows may contain partial resolution fragments from PDF text extraction.

CDF bursary and grant files contain personal information from public documents. Before publishing the dataset publicly, the group should decide whether to keep those fields or create redacted public versions.

Finance data has not yet been added. When it is added, rerun validation and update this report.
