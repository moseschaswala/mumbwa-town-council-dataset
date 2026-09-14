# Data Sources

The dataset uses public Mumbwa Town Council records and documents. The official council website is:

`https://www.mumbwacouncil.gov.zm`

## CDF Sources

The CDF PDF links were collected from the Mumbwa Town Council CDF Tracker page:

`https://www.mumbwacouncil.gov.zm/?page_id=932`

The pipe-separated CDF source link file is saved at `data/CDF/raw/cdf_pdf_sources.csv`.

| Source ID | Document | Category | Constituency | Year | Extraction Method | Extracted Rows |
| --- | --- | --- | --- | --- | --- | ---: |
| cdf_grants_nangoma_2025 | 2025-Approve-CDF-Grants-for-Nangoma-Constituency.pdf | Grants | Nangoma | 2025 | recreated_pdf | 72 |
| cdf_grants_mumbwa_2025 | 2025-Approved-CDF-Grants-for-Mumbwa-Constituency.pdf | Grants | Mumbwa | 2025 | recreated_pdf | 67 |
| cdf_community_projects_nangoma_2025 | 2025-Approved-Community-Projects-Nangoma-Constituency.pdf | Community Projects | Nangoma | 2025 | recreated_pdf | 16 |
| cdf_community_projects_mumbwa_2025 | 2025-Approved-Community-Projects-Mumbwa-Central.pdf | Community Projects | Mumbwa | 2025 | recreated_pdf | 14 |
| cdf_skills_bursaries_nangoma_2025 | 2025-Approved-CDF-Skills-Development-Bursaries-for-Nangoma-Constituency.pdf | Skills Bursaries | Nangoma | 2025 | recreated_pdf | 381 |
| cdf_skills_bursaries_mumbwa_2025 | 2025-Approved-CDF-Skills-Development-Bursaries-for-Mumbwa-Constituency.pdf | Skills Bursaries | Mumbwa | 2025 | recreated_pdf | 399 |
| cdf_secondary_bursaries_nangoma_2025 | 2025-Approved-CDF-Secondary-Boarding-School-Bursaries-for-Nangoma-Constituency.pdf | Secondary Bursaries | Nangoma | 2025 | recreated_pdf | 294 |
| cdf_secondary_bursaries_mumbwa_2025 | 2025-Approved-CDF-Secondary-Boarding-School-Bursaries-for-Mumbwa-Constituency.pdf | Secondary Bursaries | Mumbwa | 2025 | recreated_pdf | 493 |
| cdf_not_approved_projects_nangoma_2025 | NOT-APPROVED-COMMUNITY-PROJECTS-NANGOMA.pdf | Not Approved Community Projects | Nangoma | 2025 | recreated_pdf | 76 |
| cdf_not_approved_projects_mumbwa_2025 | NOT-APPROVED-COMMUNITY-PROJECTS-MUMBWA.pdf | Not Approved Community Projects | Mumbwa | 2025 | recreated_pdf | 59 |

## IDP Sources

IDP records come mainly from `data/IDP/raw/mumbwa_idp.pdf`, supported by selected Mumbwa Town Council web pages where a final table includes a `source` or `source_url` column.

Current IDP final tables include implementation plans, capital investment plans, revenue projections, revenue collection, forest reserves, school infrastructure, electricity supply, water-supply dams, agricultural staffing, strategic community projects, and cash-for-work information.

## Council Structure and Management Sources

Council structure and management records are collected from official Mumbwa Town Council pages. The final tables keep `source_url` fields where source page links are available.

Current final tables include:

- `data/Council_Structure_and_Management/final/db-unza26-csc4792_council_administrative_data.csv`
- `data/Council_Structure_and_Management/final/db-unza26-csc4792_ward_development_committee_information.csv`

## Meetings and Minutes Sources

The meetings and minutes category currently contains public council resolution records. Source details are kept in the final table fields `source_document`, `page_number`, and `source_url`.

## Finance Sources

Finance data is planned but not yet added. Expected finance sources may include council budgets, revenue records, financial statements, audit documents, procurement notices, or related financial publications. When added, source documents should be stored in `data/Finance/raw/` and final finance source notes should be added here.

## Source Traceability

The full final-table inventory is stored in `docs/dataset_manifest.csv`. Some final tables include row-level source fields such as `source_id`, `source_document`, `source`, or `source_url`.
