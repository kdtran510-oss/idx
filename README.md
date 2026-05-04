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
  
# Week 2-3 Continued Progress
## Set Up
- Fetched mortgage rate data using FERD
- Resampled weekly rates to monthly averages
- Created a matching year_month key
- Merged sold, listing, and validated the merge

## Organization
- Exported new listing and sold datasets as a CSV

# Week 4-5 Data Cleaning and Prep
## Set Up
- Converted core date fields into standardized datetime formats
- Enforced numeric data types for key analysis 
- Removed invalid records where ClosePrice or LivingArea were less than or equal to zero
- Filtered out records with negative values for DaysOnMarket, BedroomsTotal, or BathroomsTotalInteger

## Quality FLagging
- Created listing_after_close_flag and purchase_after_close_flag to identify logical date inconsistencies
- Engineered a negative_timeline_flag to catch records where the listing or purchase date occurred after the closing date
- Implemented geographic auditing 
- Flagged implausible coordinates

## Organization
- Exported and finalized clean records
- Documented transformations

# Week 6 Feature Engineering and Market Metrics
## Engineered Metrics
- Calculated Price Ratio and Close-to-Original List Ratio to measure negotiation strength and price reduction history
- Developed Price Per Sq Ft metrics to normalize property values across different living area sizes
- Constructed YrMo time-series variables from closing dates to enable monthly market trend analysis
- Engineered Listing to Contract Days and Contract to Close Days to measure escrow duration and market velocity

## Segment Analysis
- Performed multi-dimensional aggregations grouped by Property Type and SubType to uncover property-specific performance
- Conducted geographic market analysis by grouping metrics by County/Parish and MLS Area
- Generated competitive intelligence summaries by segmenting performance by Listing Office and Buyer Office

## Deliverables
- Exported final processed datasets for both Sold and Listing pipelines for integration into Tableau dashboards
- Implemented robust aggregation logic to handle mixed data types and ensure mathematical accuracy
- Documented all engineered feature formulas and purposes

# Week 7 Outlier Detection and Data Quality
## Outlier Detection Logic
- Applied the Interquartile Range (IQR) method to identify statistical outliers in Close Price, Living Area, and Days on Market
- Established mathematical lower and upper bounds using the 1.5x IQR threshold to isolate extreme data points
- Calculated the percentage shift in medians before and after filtering to quantify the impact of statistical noise

## Data Quality & Flagging
- Implemented non-destructive boolean flags (e.g., _is_outlier) to preserve raw records while enabling targeted filtering
- Developed a vectorized filtering mechanism to generate a "clean" dataset where records must pass all quality checks
- Generated comparison reports documenting specific bounds, outlier counts, and total row removals for transparency

### Deliverables
- Exported listing_full_flagged.csv containing the complete dataset with integrated quality markers
- Produced listing_clean_filtered.csv as a high-integrity source for advanced statistical analysis
- Documented field-specific statistical summaries including distribution bounds and median variance

