# Data Dictionary

This dictionary describes the main columns used in the final Mumbwa Town Council dataset. The exact column list for every final CSV is stored in `docs/dataset_manifest.csv`.

All final CSV files use `|` as the separator.

## Common Source Columns

| Column | Meaning |
| --- | --- |
| `source_id` | Short source code for CDF rows, linked to the CDF source table in `docs/data_sources.md`. |
| `source_document` | Source document name or title. |
| `source_url` | Web page or document URL where the record came from. |
| `source` | Source URL or short source note. |
| `year` | Year of the record where available. |
| `source_year` | Year of the source document where available. |

## CDF Columns

### Common CDF Columns

| Column | Meaning | Example |
| --- | --- | --- |
| `record_number` | Row number from the PDF table. | `1` |
| `constituency` | Constituency name. | `Nangoma` |
| `year` | Year of the record. | `2025` |
| `cdf_category` | Type of CDF data. | `Grants` |
| `source_id` | Short source code linking the row to the source table. | `cdf_grants_mumbwa_2025` |

### Grants

| Column | Meaning | Example |
| --- | --- | --- |
| `group_name` | Name of the grant recipient group. | `Tubalange Women's Club` |
| `group_type` | Type of group. | `Women` |
| `district` | District name. | `Mumbwa` |
| `ward` | Ward name. | `Makebo` |
| `zone` | Zone name. | `Kashinka` |
| `contact_person` | Contact person for the group. | `Tana Choongo` |
| `venture_type` | Type of venture funded. | `Village Banking` |
| `sector` | Sector of the venture. | `Finance` |

### Community Projects

| Column | Meaning | Example |
| --- | --- | --- |
| `project_name` | Name of the CDF project. | `Construction of 1x2 Classroom Block` |
| `project_description` | Short project description. | `Construction of Kantengwa Bridge` |
| `sector` | Project sector. | `Education` |
| `type_of_project` | Type of work. | `Construction` |
| `ward` | Ward name. | `Shimbizhi` |
| `zone` | Zone name if available. | `Malima` |
| `project_site_location` | Project location. | `Malombe Primary School` |
| `distance_km` | Road distance in kilometres if available. | `14` |
| `year_funded` | Year funded in the PDF. | `2025` |
| `work_package` | Work package described in the PDF. | `1x2 Classroom Block` |
| `scope_of_works` | Scope of works described in the PDF. | `Grading and gravelling` |
| `status` | Project status where available. | `Approved` |
| `comments` | Comments from the PDF where available. | `Not enough funds` |

### Skills Bursaries

| Column | Meaning | Example |
| --- | --- | --- |
| `student_name` | Name of the student. | `Suwilanji Phiri` |
| `nrc_no` | NRC number if available. | `123456/78/9` |
| `province` | Province name if available. | `Central` |
| `district` | District name. | `Mumbwa` |
| `ward` | Ward name. | `Mupona` |
| `zone` | Zone name. | `Bulungu` |
| `gender` | Student gender. | `F` |
| `course_or_skill` | Course or skill programme. | `Food and Nutrition` |
| `skill_level` | Level of study. | `Diploma` |
| `programme_duration` | Programme duration. | `36 Months` |
| `institution` | Training institution. | `Natural Resources Development College` |

### Secondary Bursaries

| Column | Meaning | Example |
| --- | --- | --- |
| `pupil_name` | Name of the pupil. | `Phiri Gift James` |
| `date_of_birth` | Date of birth from the PDF if available. | `27/10/2009` |
| `grade` | Grade from the PDF. | `8` |
| `grade_started_on_bursary` | Grade when bursary started. | `9` |
| `new_grade_2025` | New grade in 2025 if available. | `10` |
| `school_name` | Name of school. | `Mumbwa Secondary` |
| `school_location` | School district or location. | `Mumbwa` |
| `status` | Status if available. | `Approved` |

## IDP Columns

IDP tables use several repeated column groups.

### Implementation Plan Columns

| Column | Meaning |
| --- | --- |
| `strategy` | IDP strategy or objective. |
| `programme` | Programme area. |
| `activity` | Planned activity. |
| `location_by_priority` | Priority location or target area. |
| `target_2024` to `target_2028` | Year-by-year implementation targets. |
| `responsible_agency` | Responsible institution or agency. |

### Capital Investment Plan Columns

| Column | Meaning |
| --- | --- |
| `strategy` | Development strategy or objective. |
| `activity` | Investment activity. |
| `input` | Required input or resource. |
| `cost_2024` to `cost_2028` | Estimated annual costs. |
| `proposed_source_of_funding` | Proposed funding source. |
| `source_of_information` | Institution or source that supplied the information. |

### Revenue Columns

| Column | Meaning |
| --- | --- |
| `income_details` | Revenue line item. |
| `year_1` to `year_5` | Five-year revenue projection values. |
| `annual_budget_2020` to `annual_budget_2022` | Annual budget values for revenue collection records. |
| `annual_revenue_collected_2020` to `annual_revenue_collected_2022` | Revenue collected by year. |
| `percent_2020` to `percent_2022` | Collection performance percentage by year. |

### Service and Infrastructure Columns

| Column | Meaning |
| --- | --- |
| `serial_number` | Row number from the source table. |
| `school_category` | School type or category. |
| `number_of_schools` | Number of schools in the category. |
| `number_of_classrooms` | Number of classrooms. |
| `number_of_toilets` | Number of toilets. |
| `zesco` | Number of facilities connected through ZESCO. |
| `solar_power` | Number of facilities using solar power. |
| `connected_to_national_grid` | Number of facilities connected to the national grid. |
| `dam_name` | Name of dam or water-supply facility. |
| `status` | Condition or implementation status. |
| `use` | Main use of the water source. |

### Environmental and Agricultural Columns

| Column | Meaning |
| --- | --- |
| `name_of_forest` | Forest reserve name. |
| `area_ha` | Area in hectares. |
| `location` | Location of the forest reserve or service area. |
| `distance_from_mumbwa_town_center_km` | Distance from Mumbwa town centre in kilometres. |
| `block` | Agricultural block. |
| `camp` | Agricultural camp. |
| `number_of_staff` | Number of available staff. |
| `standard_farmers_per_staff` | Expected farmer-to-staff service standard. |
| `total_number_of_farmers` | Total number of farmers in the camp. |
| `farmers_without_staff_service` | Estimated farmers not covered by available staff. |
| `percent_farmers_without_staff_service` | Percentage of farmers without staff service. |

## Council Structure and Management Columns

| Column | Meaning |
| --- | --- |
| `council_name` | Name of the council. |
| `record_type` | Type of council record. |
| `category` | Administrative category. |
| `description` | Text description from the source. |
| `year` | Record year where available. |
| `information_type` | Type of ward development committee information. |
| `constituency` | Constituency linked to the record. |
| `title` | Title of the ward development committee record. |
| `source_url` | Source page URL. |

## Meetings and Minutes Columns

| Column | Meaning |
| --- | --- |
| `council_name` | Name of the council. |
| `year` | Year of the meeting or source document. |
| `source_document` | Meeting or council document name. |
| `page_number` | Page number in the source document. |
| `resolution_text` | Extracted public resolution text. |
| `source_url` | Source document URL. |

## Finance Columns

Finance data has not yet been added. When it is added, expected columns may include:

| Column | Meaning |
| --- | --- |
| `financial_year` | Financial year covered by the record. |
| `budget_line` | Budget or account line item. |
| `revenue_source` | Revenue source or income category. |
| `expenditure_category` | Spending category. |
| `amount_zmw` | Amount in Zambian Kwacha. |
| `document_type` | Budget, financial statement, audit, procurement, or related source type. |
| `source_document` | Source document name. |
| `source_url` | Source URL where available. |

Finance column names should be updated in this dictionary after the final finance files are added.

## Sensitive Fields

The following fields may contain personal information and should be reviewed before public publication:

- `student_name`
- `pupil_name`
- `date_of_birth`
- `nrc_no`
- `contact_person`
