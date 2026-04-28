# %% 
# # Setup & Data Loading
# Run this cell first to get your tools and data ready.

import pandas as pd
import numpy as np

# Load the pre-combined data (Week 1 output)
df = pd.read_csv("sold_final.csv", low_memory=False)
print(f"Data loaded successfully! Initial shape: {df.shape}")

# %% 
# # Weeks 2-3: Structuring & EDA
# This cell fulfills the requirement to document unique property types, 
# null-counts, and numeric distributions[cite: 113, 114, 115].

print("--- WEEKS 2-3 DELIVERABLES ---")

# 1. Unique Property Types 
if "PropertyType" in df.columns:
    print("\n[Unique Property Types]")
    print(df["PropertyType"].unique())
    
    # Filter to Residential 
    df = df[df["PropertyType"] == "Residential"].copy()
    print(f"\nFiltered to Residential only. New shape: {df.shape}")

# 2. Missing Value Report (>90% check) 
print("\n[Missing Value Report]")
missing_pct = df.isnull().mean()
threshold = 0.90
high_missing_cols = missing_pct[missing_pct > threshold].index.tolist()

print(f"Columns with >90% missing values ({len(high_missing_cols)} total):")
print(high_missing_cols[:5], "...") # Preview first 5

# Drop the sparse columns (safeguarding core fields)
core_fields = ['ClosePrice', 'LivingArea', 'BedroomsTotal', 'DaysOnMarket']
cols_to_drop = [col for col in high_missing_cols if col not in core_fields]
df = df.drop(columns=cols_to_drop)
print(f"-> Dropped {len(cols_to_drop)} sparse columns.")

# 3. Numeric Distribution Summary 
print("\n[Numeric Distribution Summary]")
cols_of_interest = [c for c in core_fields if c in df.columns]
if cols_of_interest:
    stats = df[cols_of_interest].describe(percentiles=[0.25, 0.5, 0.75, 0.95]).T
    stats = stats.rename(columns={'50%': 'median'})
    print(stats[['min', 'max', 'mean', 'median', '25%', '75%', '95%']])

# df.to_csv("filtered_sold_dataset.csv", index=False) 

# %% 
# # Weeks 2-3: Mortgage Rate Enrichment
# This cell fetches FRED data and merges it, checking for nulls

print("\n--- MORTGAGE RATE MERGE ---")

# 1. Fetch FRED Data 
print("Fetching FRED Mortgage Data...")
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=['observation_date'])
mortgage.columns = ['date', 'rate_30yr_fixed']

# 2. Resample to Monthly 
mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly = mortgage.groupby('year_month')['rate_30yr_fixed'].mean().reset_index()

# 3. Merge and Validate 
# Use CloseDate for Sold data, or ListingContractDate if using Listings data
date_col = 'CloseDate' 

if date_col in df.columns:
    df['year_month'] = pd.to_datetime(df[date_col], errors='coerce').dt.to_period('M')
    df = df.merge(mortgage_monthly, on='year_month', how='left')
    
    # The validation check required by the handbook [cite: 160]
    print(f"Validation Check - Missing mortgage rates after merge: {df['rate_30yr_fixed'].isnull().sum()}")

# %% 
# # Weeks 4-5: Cleaning & Flagging
# This cell enforces data types and generates the required timeline/geographic flags

print("\n--- WEEKS 4-5 DELIVERABLES ---")
initial_rows = len(df)

# 1. Parse Dates and Enforce Numerics 
date_cols = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate']
for col in date_cols:
    if col in df.columns: df[col] = pd.to_datetime(df[col], errors='coerce')

numeric_cols = ['ClosePrice', 'LivingArea', 'DaysOnMarket', 'BedroomsTotal', 'BathroomsTotalInteger', 'Latitude', 'Longitude']
for col in numeric_cols:
    if col in df.columns: df[col] = pd.to_numeric(df[col], errors='coerce')

# 2. Data Type Confirmations 
print("\n[Data Type Confirmations]")
check_cols = [c for c in ['CloseDate', 'ClosePrice', 'Latitude'] if c in df.columns]
print(df[check_cols].dtypes)

# 3. Drop invalid numerical rows 
if 'ClosePrice' in df.columns: df = df[df['ClosePrice'] > 0]
if 'LivingArea' in df.columns: df = df[df['LivingArea'] > 0]
if 'DaysOnMarket' in df.columns: df = df[df['DaysOnMarket'] >= 0]
if 'BedroomsTotal' in df.columns and 'BathroomsTotalInteger' in df.columns:
    df = df[(df['BedroomsTotal'] >= 0) & (df['BathroomsTotalInteger'] >= 0)]

# 4. Timeline Flags 
if all(c in df.columns for c in ['ListingContractDate', 'CloseDate']):
    df['listing_after_close_flag'] = df['ListingContractDate'] > df['CloseDate']
if all(c in df.columns for c in ['PurchaseContractDate', 'CloseDate']):
    df['purchase_after_close_flag'] = df['PurchaseContractDate'] > df['CloseDate']
if all(c in df.columns for c in ['ListingContractDate', 'PurchaseContractDate', 'CloseDate']):
    df['negative_timeline_flag'] = (df['ListingContractDate'] > df['PurchaseContractDate']) | \
                                   (df['PurchaseContractDate'] > df['CloseDate'])

# 5. Geographic Flags 
if 'Latitude' in df.columns and 'Longitude' in df.columns:
    df['missing_coords_flag'] = df['Latitude'].isnull() | df['Longitude'].isnull()
    df['zero_coords_flag'] = (df['Latitude'] == 0) | (df['Longitude'] == 0)
    df['positive_longitude_flag'] = df['Longitude'] > 0
    df['implausible_coords_flag'] = ~((df['Latitude'].between(32.0, 42.5)) & 
                                      (df['Longitude'].between(-125.0, -114.0))) & \
                                      df['Latitude'].notnull() & df['Longitude'].notnull()

# 6. Deliverable Printouts 
print("\n[Date Consistency Flag Counts]")
if 'listing_after_close_flag' in df.columns: print(f"Listing after Close: {df['listing_after_close_flag'].sum()}")
if 'purchase_after_close_flag' in df.columns: print(f"Purchase after Close: {df['purchase_after_close_flag'].sum()}")
if 'negative_timeline_flag' in df.columns: print(f"Negative Timeline: {df['negative_timeline_flag'].sum()}")
    
print("\n[Geographic Data Quality Summary]")
if 'missing_coords_flag' in df.columns:
    print(f"Missing Coordinates: {df['missing_coords_flag'].sum()}")
    print(f"Zero Coordinates (0,0): {df['zero_coords_flag'].sum()}")
    print(f"Positive Longitude: {df['positive_longitude_flag'].sum()}")
    print(f"Implausible/Out-of-State: {df['implausible_coords_flag'].sum()}")

final_rows = len(df)
print("\n[Row Summary: Invalid Numerics Removed]")
print(f"Rows before: {initial_rows} | Rows after: {final_rows} | Total Removed: {initial_rows - final_rows}")

# df.to_csv("sold_analysis_ready.csv", index=False) 

# %%
# # Week 6: Feature Engineering and Market Metrics
# This section engineers key market indicators for Tableau dashboards 
# and performs segment analysis to uncover market patterns.

print("\n--- WEEK 6 DELIVERABLES ---")

# 1. Engineer Key Metrics
# Using .dt.days to convert pandas timedeltas into flat integers

# Price Ratios
if all(c in df.columns for c in ['ClosePrice', 'OriginalListPrice']):
    # The image lists "Price Ratio" and "Close to Original List Ratio" with the exact same formula, 
    # so we will generate both to match the spec strictly.
    df['PriceRatio'] = df['ClosePrice'] / df['OriginalListPrice']
    df['CloseToOriginalListRatio'] = df['PriceRatio']

# Price Per Sq Ft
if all(c in df.columns for c in ['ClosePrice', 'LivingArea']):
    df['PricePerSqFt'] = df['ClosePrice'] / df['LivingArea']

# Year / Month / YrMo
if 'CloseDate' in df.columns:
    df['YrMo'] = df['CloseDate'].dt.strftime('%Y-%m')

# Timeline Metrics (Listing to Contract & Contract to Close)
if all(c in df.columns for c in ['PurchaseContractDate', 'ListingContractDate']):
    df['ListingToContractDays'] = (df['PurchaseContractDate'] - df['ListingContractDate']).dt.days

if all(c in df.columns for c in ['CloseDate', 'PurchaseContractDate']):
    df['ContractToCloseDays'] = (df['CloseDate'] - df['PurchaseContractDate']).dt.days


# 2. Sample Output Table
print("\n[Sample Output: Engineered Metrics]")
engineered_cols = ['PriceRatio', 'PricePerSqFt', 'DaysOnMarket', 'YrMo', 
                   'CloseToOriginalListRatio', 'ListingToContractDays', 'ContractToCloseDays']

# Filter to show only columns that successfully generated
existing_eng_cols = [c for c in engineered_cols if c in df.columns]
if existing_eng_cols:
    print(df[existing_eng_cols].head())


# 3. Segment Analysis
print("\n[Segmented Analysis Summaries]")

def generate_segment_summary(group_cols):
    """Safely groups by given dimensions and generates summary statistics for engineered metrics."""
    valid_groups = [c for c in group_cols if c in df.columns]
    
    # Only run if both requested grouping columns exist in the dataframe
    if len(valid_groups) == len(group_cols):
        metrics_to_summarize = [m for m in ['PriceRatio', 'PricePerSqFt', 'DaysOnMarket', 'ListingToContractDays'] if m in df.columns]
        
        if metrics_to_summarize:
            # Generate mean, median, and count to understand the distribution of the segments
            summary = df.groupby(valid_groups)[metrics_to_summarize].agg(['mean', 'median', 'count']).round(2)
            print(f"\n--- Summary by {valid_groups} ---")
            print(summary.head()) # Previewing the top 5 segments
    else:
        print(f"\nSkipping {group_cols} summary: Missing one or more required columns.")

# Generate the three specific groupings requested in the handbook
generate_segment_summary(['PropertyType', 'PropertySubType'])
generate_segment_summary(['CountyOrParish', 'MLSAreaMajor'])
generate_segment_summary(['ListOfficeName', 'BuyerOfficeName'])


# 4. Final Deliverable Table Export (Grouped by CountyOrParish or PropertyType)
if 'CountyOrParish' in df.columns:
    print("\n[Deliverable: Segmented Table (CountyOrParish)]")
    deliverable_summary = df.groupby('CountyOrParish')[existing_eng_cols].mean(numeric_only=True).round(2)
    print(deliverable_summary.head(10))
elif 'PropertyType' in df.columns:
    print("\n[Deliverable: Segmented Table (PropertyType)]")
    deliverable_summary = df.groupby('PropertyType')[existing_eng_cols].mean(numeric_only=True).round(2)
    print(deliverable_summary)

# Save the final dataset ready for Tableau
df.to_csv("sold_tableau_ready.csv", index=False)

# %%
