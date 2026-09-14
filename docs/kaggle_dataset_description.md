# Kaggle Dataset Description Draft

## Title

Mumbwa Town Council Public Records Dataset

## Subtitle

Pipe-separated CSV records for CDF, IDP, council structure, and public council resolutions from Mumbwa Town Council.

## Description

This dataset contains public records collected from Mumbwa Town Council sources for a CSC 4792 Data Mining and Warehousing group project. It currently includes Constituency Development Fund records, Integrated Development Plan records, council structure and management records, and public council resolution text. Finance data is expected to be added as a later category.

The dataset is organized as multiple related CSV tables rather than one combined table. This keeps different record types separate and easier to analyze. All final CSV files use the pipe character `|` as the separator because several text fields contain commas.

## Current Files

| Category | Final CSV files | Rows |
| --- | ---: | ---: |
| CDF | 5 | 1,871 |
| IDP | 23 | 546 |
| Council Structure and Management | 2 | 26 |
| Meetings and Minutes | 1 | 119 |
| Finance | 0 | 0 |

The full file list is available in `docs/dataset_manifest.csv`.

## Suggested Use

The dataset can support student analysis of:

- CDF grants, projects, and bursaries by constituency, ward, sector, institution, school, and gender.
- IDP implementation targets, capital investment plans, revenue projections, service availability, and infrastructure indicators.
- Council administrative and ward development committee records.
- Public council resolution text.
- Finance records once the finance category is added.

## Reading The Data

```python
import pandas as pd

df = pd.read_csv("data/IDP/final/db-unza26-csc4792_revenue_projection_for_first_five_years_of_implementation_plan.csv", sep="|")
df.head()
```

## Source

Mumbwa Town Council website: `https://www.mumbwacouncil.gov.zm`

## Privacy And Responsible Use

Some CDF bursary and grant records include personal information from public documents, including names and identification-related fields. Before publishing publicly, the group should consider whether to upload the original files or a redacted public version.
