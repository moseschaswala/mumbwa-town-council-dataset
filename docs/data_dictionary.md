# CDF Data Dictionary

This dictionary describes the columns used in the final CDF datasets.

## Common Columns

|Column|Meaning|Example|
|-|-|-|
|record\_number|Row number from the PDF table|1|
|constituency|Constituency name|Nangoma|
|year|Year of the record|2025|
|cdf\_category|Type of CDF data|Grants|
|source\_id|Short source code linking the row to the source table|cdf_grants_mumbwa_2025|

Full PDF names and extraction methods are documented in `docs/data_sources.md`.

## Grants Columns

|Column|Meaning|Example|
|-|-|-|
|group\_name|Name of the group that received the grant|Tubalange Women's Club|
|group\_type|Type of group|Women|
|district|District name|Mumbwa|
|ward|Ward name|Makebo|
|zone|Zone name|Kashinka|
|contact\_person|Contact person for the group|Tana Choongo|
|venture\_type|Type of venture funded|Village Banking|
|sector|Sector of the venture|Finance|

## Community Project Columns

|Column|Meaning|Example|
|-|-|-|
|project\_name|Name of the CDF project|Construction of 1x2 Classroom Block|
|project\_description|Short project description|Construction of Kantengwa Bridge|
|sector|Project sector|Education|
|type\_of\_project|Type of work|Construction|
|district|District name|Mumbwa|
|ward|Ward name|Shimbizhi|
|zone|Zone name if available|Malima|
|project\_site\_location|Project location|Malombe Primary School|
|distance\_km|Road distance in kilometres if available|14|
|year\_funded|Year funded in the PDF|2025|
|work\_package|Work package described in the PDF|1x2 Classroom Block|
|scope\_of\_works|Scope of works described in the PDF|Grading and gravelling|
|status|Project status|Approved|
|comments|Comments from the PDF|Not enough funds|

## Skills Bursary Columns

|Column|Meaning|Example|
|-|-|-|
|student\_name|Name of the student|Suwilanji Phiri|
|nrc\_no|NRC number if available|123456/78/9|
|province|Province name if available|Central|
|district|District name|Mumbwa|
|ward|Ward name|Mupona|
|zone|Zone name|Bulungu|
|gender|Student gender|F|
|course\_or\_skill|Course or skill programme|Food and Nutrition|
|skill\_level|Level of study|Diploma|
|programme\_duration|Programme duration|36 Months|
|institution|Training institution|Natural Resources Development College|

## Secondary Bursary Columns

|Column|Meaning|Example|
|-|-|-|
|pupil\_name|Name of the pupil|Phiri Gift James|
|province|Province name if available|Central|
|district|District name|Mumbwa|
|ward|Ward name|Mupona|
|zone|Zone name|Welfare|
|gender|Pupil gender|M|
|date\_of\_birth|Date of birth from the PDF if available|27/10/2009|
|grade|Grade from the PDF|8|
|grade\_started\_on\_bursary|Grade when bursary started|9|
|new\_grade\_2025|New grade in 2025 if available|10|
|school\_name|Name of school|Mumbwa Secondary|
|school\_location|School district/location|Mumbwa|
|status|Status if available|Approved|


