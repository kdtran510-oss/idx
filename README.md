# Week 0-1 Progress 
## Environment & Data Setup
- Set up local environment in VS Code
- Downloaded all raw MLS CSV files from the FTP raw directory
## Script Management & Execution
- Reviewed and organized the extraction scripts (crmls_sold.py and crmls_listed.py)
- Generated February & March 2026 outputs: CRMLSSold202602.csv and CRMLSListing202602.csv 
## Validation & Organization
- Performed basic validation checks on generated CSV files.
- Appended all Sold and Listing CSV files to the recent calendar month
- Filtered both to PropertyType == 'Residential'
- Included row counts for pre/post aggregation and filter

# Week 2-3 Progress
## Data Understanding
- Identified the number of rows and columns in the aggregated CSV
- Reviewed column data types and identified columns with missing values
- Flagged columns with >90% missing values to consider for column dropping
- Produced statistical summaries for numerical columns like ClosePrice, LivingArea, etc
## Organization
- Saved filtered dataset into a new CSV
  
# Week 2-3 Continued  Progress
## Set Up
- Fetched mortgage rate data using FERD
- Resampled weekly rates to monthly averages
- Created a matching year_month key
- Merged sold, listing, and validated the merge

## Organization
- Exported new listing and sold datasets as a CSV
