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

Mumbwa Town Council; Constituency Development Fund; local government; council publications; budgets; council meetings; Zambia

## Abstract

This data article describes a public records dataset collected from the official Mumbwa Town Council website for the CSC 4792 Data Mining and Warehousing group project. The dataset includes a completed Constituency Development Fund component and additional non-CDF council records. The CDF data cover grants, approved community projects, not-approved community projects, skills development bursaries, and secondary boarding school bursaries for Mumbwa and Nangoma constituencies. The non-CDF data are organized into separate category pipelines for financial data, IDP data, council meetings and minutes, council structure and management, and public services/legal data. Data were extracted from official web pages and public documents, cleaned with Python scripts, validated for structure and empty columns, and saved as pipe-separated CSV files.

## Specifications Table

| Item | Description |
| --- | --- |
| Subject | Social Sciences |
| Specific subject area | Local government public records for Mumbwa Town Council |
| Type of data | Tables and text extracts |
| Data format | Raw PDF/DOCX documents, extracted CSV files, cleaned CSV files, final pipe-separated CSV files |
| Data source location | Mumbwa Town Council, Zambia |
| Data accessibility | Final CSV files are prepared for upload to Kaggle |
| Related research article | Not applicable |

## Value Of The Data

- The data organize public Mumbwa Town Council records into reusable CSV files.
- The CDF files support analysis of grants, community projects, and bursaries by constituency, ward, sector, project type, institution, school, and gender.
- The non-CDF files support wider local government analysis using category-specific financial, IDP, meeting, structure, public service, and legal records.
- The category source registers preserve source URLs and local file references so users can trace extracted data back to official documents.
- The dataset can be reused by students, lecturers, local government researchers, and civic data users.

## Data Description

The CDF grants dataset contains 139 records from Mumbwa and Nangoma constituencies. It includes group names, group types, districts, constituencies, wards, zones where available, contact persons, venture types, sectors, source IDs, year, and category.

The approved CDF community projects dataset contains 30 records from Mumbwa and Nangoma constituencies. It includes project names, project descriptions, sectors, project types, districts, constituencies, wards, project sites, road distances where available, work packages where available, statuses, source IDs, year, and category.

The not-approved CDF community projects dataset contains 135 records from Mumbwa and Nangoma constituencies. It includes project names, project descriptions, sectors, project types, districts, constituencies, wards where available, project sites, comments or statuses where available, source IDs, year, and category.

The CDF skills bursaries dataset contains 780 records from Mumbwa and Nangoma constituencies. It includes student names, NRC numbers where available, provinces where available, districts, constituencies, wards, zones, gender, courses or skills, skill levels, programme durations, institutions, source IDs, year, and category.

The CDF secondary bursaries dataset contains 787 records from Mumbwa and Nangoma constituencies. It includes pupil names, provinces where available, districts, constituencies, wards, zones, gender, dates of birth where available, grades, schools, school locations, statuses where available, source IDs, year, and category.

The financial data category contains 19 publication records, 291 document text extract records, 1582 document table-cell records, and 7751 recreated text-table line records. It includes budget, financial statement, audit, and procurement-related records.

The IDP data category contains 1 publication record, 20 document text extract records, 504 recreated text-table line records, and 2 website page records. The IDP PDF did not produce usable table-cell rows, so no empty IDP table-cell final CSV was created.

The council meetings and minutes category contains 13 publication records, 129 document text extract records, 102 document table-cell records, and 4161 recreated text-table line records. It includes ordinary council meeting, special council meeting, and stakeholder meeting records.

The council structure and management category contains 11 website page records, 12 official records, 16 councillor records, 7 department records, 4 contact records, and 17 mandate function records. It includes council profile, senior management, departments, civic leaders, constituency, standing committee, mandate, and contact page text.

The public services and legal category contains 17 publication records, 260 document text extract records, 1183 document table-cell records, 6562 recreated text-table line records, 4 website page records, 3 news update records, and 6 FAQ records.

## Experimental Design, Materials, And Methods

The assignment specification identifies Project Team #22 as Mumbwa Town Council with the official website `https://www.mumbwacouncil.gov.zm`.

For the CDF data, source PDFs were collected from the Mumbwa Town Council CDF Tracker page. Original PDFs are kept in `data/CDF_Data/raw/pdfs/`. Some tables were difficult to extract directly because they were scanned or image-based, so recreated machine-readable PDFs were saved in `data/CDF_Data/intermediate/reconstructed_pdfs/`.

The CDF extraction script `src/extractor.py` reads recreated PDF tables with `pdfplumber`, adds simple source information, and saves pipe-separated extracted CSV files in `data/CDF_Data/extracted/`.

The CDF cleaning script `src/cleaner.py` reads extracted CSV files, cleans column names, removes extra spaces and line breaks, removes empty rows, removes exact duplicate rows, standardizes common columns, removes fully empty columns, and saves processed CSV files in `data/CDF_Data/processed/`.

The CDF integration script `src/integrator.py` combines only files that contain the same type of CDF data and writes final CSV files in `data/CDF_Data/final/` using the required naming convention.

For non-CDF data, the script `src/other_council_data.py` starts from the official website, publications page, news page, FAQ page, and selected council information pages. It skips CDF documents because the CDF component is already handled separately.

The non-CDF script downloads public documents into category raw document folders, creates source extracts, extracts selected website and news page text, extracts FAQ pairs, extracts PDF text with `pdfplumber`, and extracts available PDF table cells. Because some official PDFs are long or scanned, the script records `Total Pages` and `Pages Extracted` in the outputs.

The category split script `src/category_pipelines.py` separates the non-CDF material into `data/financial_data/`, `data/idp_data/`, `data/council_meetings_minutes_data/`, `data/council_structure_management_data/`, and `data/public_services_legal_data/`. Each category folder contains `raw`, `intermediate`, `extracted`, `processed`, and `final` subfolders.

The non-CDF cleaning step keeps the output column names meaningful, removes duplicate rows, removes fully empty rows, removes fully empty columns, and keeps missing values as blank/null CSV cells. Empty final CSV files are not created when a category has no extracted rows for a data type. For PDFs where text was extractable but tables were not detected, readable text-table PDFs and CSV line datasets were recreated while preserving source document names, page numbers, and line numbers.

The validation report checks final CSV row counts, column counts, separator consistency, and fully empty columns. Validation warnings are used for manual checking and do not automatically delete source records.

## Ethics Statement

The data were extracted from publicly available council documents and web pages. The dataset should still be handled responsibly because CDF bursary records include names of pupils and students. The dataset should be used for educational and civic data analysis purposes.

## Declaration Of Competing Interest

The authors declare no known competing interests.

## References

Republic of Zambia. Ministry of Local Government and Rural Development. `https://www.mlgrd.gov.zm`

Mumbwa Town Council. `https://www.mumbwacouncil.gov.zm`

Local Government Act, 2019. `https://zambialii.org/akn/zm/act/2019/2/eng@2019-04-11`

Phiri, L. (2026). A Multi-source Dataset for CS1 Failure Prediction. Kaggle.
