# Kaggle Dataset Description Draft

## Title

Mumbwa Town Council CDF Dataset

## Subtitle

Pipe-separated CSV records for 2025 CDF grants, projects, and bursaries from Mumbwa Town Council.

## Description

This dataset contains Constituency Development Fund records collected from Mumbwa Town Council PDF documents. It covers Mumbwa and Nangoma constituencies and includes grants, approved community projects, not-approved community projects, skills development bursaries, and secondary boarding school bursaries.

The data were extracted from recreated machine-readable PDF tables using `pdfplumber`, cleaned with simple Python scripts, and saved as pipe-separated CSV files. A short `source_id` column is included so records can be traced back to the source documents listed in the documentation.

## Files

| File | Description | Rows |
| --- | --- | ---: |
| db-unza26-csc4792-mumbwa_town_council_cdf_grants.csv | Youth, women, and community empowerment grants | 139 |
| db-unza26-csc4792-mumbwa_town_council_cdf_community_projects.csv | Approved community projects | 30 |
| db-unza26-csc4792-mumbwa_town_council_cdf_not_approved_community_projects.csv | Community projects that were not approved | 135 |
| db-unza26-csc4792-mumbwa_town_council_cdf_skills_bursaries.csv | Skills development bursaries | 780 |
| db-unza26-csc4792-mumbwa_town_council_cdf_secondary_bursaries.csv | Secondary boarding school bursaries | 787 |

## Suggested Use

The dataset can be used for student analysis of CDF records by constituency, ward, sector, project type, school, institution, and bursary category.

## Separator

All CSV files use the pipe character `|` as the column separator.

Example in pandas:

```python
import pandas as pd

df = pd.read_csv("db-unza26-csc4792-mumbwa_town_council_cdf_grants.csv", sep="|")
df.head()
```

## Source

Mumbwa Town Council website: `https://www.mumbwacouncil.gov.zm`
