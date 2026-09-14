# Data Article Draft

## Article Information

### Article Title

Mumbwa Town Council Constituency Development Fund Dataset

### Authors

Group 22 CSC 4792 students

### Affiliations

University of Zambia

### Corresponding Author Email

moses.chsaswala@cs.unza.zm

### Keywords

Mumbwa Town Council; Constituency Development Fund; CDF grants; community projects; bursaries; Zambia local government

## Abstract

This data article describes the Constituency Development Fund part of a wider Mumbwa Town Council group dataset. The CDF data include approved youth, women, and community empowerment grants; approved community projects; not-approved community projects; skills development bursaries; and secondary boarding school bursaries. The source PDF documents were collected from the Mumbwa Town Council website for Mumbwa and Nangoma constituencies. Some PDF tables were scanned or difficult to extract directly, so recreated machine-readable PDFs were used for table extraction. Tables were extracted with `pdfplumber`, cleaned with simple Python scripts, validated for duplicate rows and missing key fields, and saved as pipe-separated CSV files. The data can be reused for simple analysis of CDF records by constituency, ward, sector, project type, school, institution, gender, and bursary category.

## Specifications Table

| Item | Description |
| --- | --- |
| Subject | Social Sciences |
| Specific subject area | Local government CDF grants, projects, and bursaries for Mumbwa Town Council |
| Type of data | Tables |
| Data format | Raw, extracted, cleaned, final pipe-separated CSV files |
| Data source location | Mumbwa Town Council, Zambia |
| Data accessibility | Final CSV files are prepared for upload to Kaggle |
| Related research article | Not applicable |

## Value Of The Data

- The data provide organized CDF records from Mumbwa Town Council PDF documents.
- Students, lecturers, local government researchers, and civic data users can reuse the data.
- The data can support analysis by constituency, ward, sector, project type, school, institution, and bursary category.
- The extracted and processed files make PDF table data easier to check, analyze, and share.
- The `source_id` field helps users trace each record back to the PDF document without making every CSV row too long.

## Data Description

The grants dataset contains 139 records from Mumbwa and Nangoma constituencies. It includes group names, group types, wards, zones, contact persons, venture types, sectors, source IDs, year, and category.

The approved community projects dataset contains 30 records from Mumbwa and Nangoma constituencies. It includes project names, project descriptions, sectors, project types, wards, project sites, road distances where available, work packages, scope of works, status, source IDs, year, and category.

The not-approved community projects dataset contains 135 records from Mumbwa and Nangoma constituencies. It includes project names, project descriptions, sectors, project types, project sites, comments, status where available, source IDs, year, and category.

The skills bursaries dataset contains 780 records from Mumbwa and Nangoma constituencies. It includes student names, NRC numbers where available, districts, wards, zones, gender, courses or skills, skill levels, programme durations, institutions, source IDs, year, and category.

The secondary bursaries dataset contains 787 records from Mumbwa and Nangoma constituencies. It includes pupil names, districts, wards, zones, gender, dates of birth where available, grades, schools, school locations, status where available, source IDs, year, and category.

## Experimental Design, Materials, And Methods

The source documents were collected from the Mumbwa Town Council website. The assignment specification identifies Project Team #22 as Mumbwa Town Council with the official website `https://www.mumbwacouncil.gov.zm`.

Original PDF files were kept in `data/CDF/raw/pdfs/` and were not modified.

Some tables were difficult to extract directly because they were scanned or image-based. Those tables were recreated into machine-readable PDFs and saved in `data/CDF/intermediate/reconstructed_pdfs/`.

The extraction script `src/extractor.py` reads each recreated PDF with `pdfplumber`, extracts tables page by page, adds simple source information, and saves pipe-separated CSV files in `data/CDF/extracted/`.

The cleaning script `src/cleaner.py` reads extracted CSV files, cleans column names, removes extra spaces and line breaks, removes empty rows, removes exact duplicate rows, standardizes common columns, and saves processed pipe-separated CSV files in `data/CDF/processed/`.

The integration script `src/integrator.py` combines only files that contain the same type of CDF data. It creates final pipe-separated CSV files in `data/CDF/final/` using the required file naming convention.

The validation script `src/validator.py` provides simple checks for missing values, duplicate rows, missing required columns, and invalid amount values. Validation warnings are used for manual checking and do not automatically delete records.

## Ethics Statement

The data were extracted from publicly available council documents. The records should still be handled responsibly because bursary files include names of pupils and students. The dataset should be used for educational and civic data analysis purposes.

## Declaration Of Competing Interest

The authors declare no known competing interests.

## References

Republic of Zambia. Ministry of Local Government and Rural Development. `https://www.mlgrd.gov.zm`

Mumbwa Town Council. `https://www.mumbwacouncil.gov.zm`

Local Government Act, 2019. `https://zambialii.org/akn/zm/act/2019/2/eng@2019-04-11`
