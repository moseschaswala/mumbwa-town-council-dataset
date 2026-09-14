# CDF Validation Report

## Final Dataset Checks

|Final CSV File|Rows|Pipe Separated|Duplicate Rows|Missing Main Name|Missing Record Number|
|-|-:|-|-:|-:|-:|
|db-unza26-csc4792-mumbwa\_town\_council\_cdf\_grants.csv|139|Yes|0|0|0|
|db-unza26-csc4792-mumbwa\_town\_council\_cdf\_community\_projects.csv|30|Yes|0|0|0|
|db-unza26-csc4792-mumbwa\_town\_council\_cdf\_not\_approved\_community\_projects.csv|135|Yes|0|0|0|
|db-unza26-csc4792-mumbwa\_town\_council\_cdf\_skills\_bursaries.csv|780|Yes|0|0|0|
|db-unza26-csc4792-mumbwa\_town\_council\_cdf\_secondary\_bursaries.csv|787|Yes|0|0|0|

## Notes For Manual Checking

Some blank cells are expected because Mumbwa and Nangoma PDF tables do not always use the same columns.

Examples:

* Some Nangoma bursary tables have province, while some Mumbwa bursary tables do not.
* Some Mumbwa bursary tables have ward and zone, while some Nangoma tables do not.
* Approved community project tables and road project tables use different columns.
* Not-approved community project tables do not always include ward, zone, or status.

These records were not deleted. They should be checked against the original PDFs if a lecturer or group member asks about missing values.

