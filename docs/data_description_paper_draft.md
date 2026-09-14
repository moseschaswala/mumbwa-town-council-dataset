# Data Article Draft

## Article Information

### Article Title

Mumbwa Town Council Public Records Dataset

### Authors

Group 22 CSC 4792 students

### Affiliations

University of Zambia

### Corresponding Author Email

moses.chsaswala@cs.unza.zm

### Keywords

Mumbwa Town Council; Constituency Development Fund; Integrated Development Plan; council resolutions; local government; Zambia

## Abstract

This data article describes a public records dataset collected from Mumbwa Town Council sources for the CSC 4792 Data Mining and Warehousing group project. The dataset currently contains Constituency Development Fund records, Integrated Development Plan records, council structure and management records, and public council resolution text. Finance data is planned as an additional category. The data were extracted from public documents and web pages, cleaned with Python and notebook workflows, validated for structure and duplicate rows, and saved as pipe-separated CSV files.

## Specifications Table

| Item | Description |
| --- | --- |
| Subject | Social Sciences |
| Specific subject area | Local government public records for Mumbwa Town Council |
| Type of data | Tables and text extracts |
| Data format | Raw documents, extracted data, processed data, and final pipe-separated CSV files |
| Data source location | Mumbwa Town Council, Zambia |
| Data accessibility | Final CSV files are prepared for GitHub and possible Kaggle publication |
| Related research article | Not applicable |

## Value Of The Data

- The data organize public Mumbwa Town Council records into reusable CSV tables.
- The CDF files support analysis of grants, community projects, and bursaries by constituency, ward, sector, project type, institution, school, and gender.
- The IDP files support analysis of implementation targets, capital investment plans, revenue projections, service availability, school infrastructure, forest reserves, and agriculture staffing.
- The council structure files support analysis of administrative and ward development committee information.
- The public council resolution table provides extracted text for reviewing meeting decisions.
- The prepared Finance folder allows financial records to be added under the same dataset structure.

## Data Description

The current final dataset contains 31 CSV tables and 2,562 rows.

| Category | Final CSV files | Rows |
| --- | ---: | ---: |
| CDF | 5 | 1,871 |
| IDP | 23 | 546 |
| Council Structure and Management | 2 | 26 |
| Meetings and Minutes | 1 | 119 |
| Finance | 0 | 0 |

The full table inventory, file paths, row counts, column counts, and column lists are stored in `docs/dataset_manifest.csv`.

## Experimental Design, Materials, And Methods

The assignment identifies Project Team 22 as Mumbwa Town Council. Source material was collected from the official council website, `https://www.mumbwacouncil.gov.zm`, and from local copies of council documents.

The CDF data were collected from the Mumbwa Town Council CDF Tracker page. Original PDFs are stored in `data/CDF/raw/pdfs/`. Some tables were scanned or image-based, so recreated machine-readable PDFs were stored in `data/CDF/intermediate/reconstructed_pdfs/`. CDF extraction, cleaning, integration, and validation were handled through scripts in `src/` and the CDF notebook.

The IDP data were extracted from `data/IDP/raw/mumbwa_idp.pdf` and selected council web pages. The final IDP layer was cleaned by removing duplicate exports, removing empty or broken final files, standardizing column names, removing repeated header rows, removing duplicate rows, fixing visible encoding artifacts, and repairing a shifted forest-reserve row.

Council structure and management data were collected from official council pages and saved as final CSV tables under `data/Council_Structure_and_Management/final/`.

Meeting and resolution records were extracted into `data/Meetings_and_Minutes/final/`. These records should receive manual text review because some PDF extraction rows may contain partial resolution text.

Finance data has not yet been added. When finance records are added, source files should be stored in `data/Finance/raw/`, working files in `data/Finance/processed/`, and final tables in `data/Finance/final/`.

## Ethics Statement

The data were extracted from publicly available council records. Some CDF bursary and grant records include personal information such as names, dates of birth, NRC numbers, or contact persons. The group should decide whether to publish those original fields or create a redacted public version before uploading to an open data platform.
