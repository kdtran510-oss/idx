# %%
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt

# load the datasets (assuming they are already defined as df_filtered and df_sold_filtered)
listing_final = df_filtered
sold_final = df_sold_filtered

# print total row/column count
print("Listing Final - Rows:", listing_final.shape[0], "Columns:", listing_final.shape[1])
print("Sold Final - Rows:", sold_final.shape[0], "Columns:", sold_final.shape[1])

# print data types for all columns
print("\nListing Final Data Types:")
print(listing_final.dtypes)
print("\nSold Final Data Types:")
print(sold_final.dtypes)

# unique values in PropertyType column
print("\nListing Final - Unique PropertyType values:")
print(listing_final['PropertyType'].unique())
print("\nSold Final - Unique PropertyType values:")
print(sold_final['PropertyType'].unique())

# fields to analyze
fields = ['ClosePrice', 'ListPrice', 'OriginalListPrice', 'LivingArea', 'LotSizeAcres', 'BedroomsTotal', 'BathroomsTotalInteger', 'DaysOnMarket', 'YearBuilt']

# generate histograms, boxplots, and percentile summaries
for field in fields:
    if field in listing_final.columns:
        print(f"\nListing Final - {field} Percentiles:")
        print(listing_final[field].describe())
        
        # histogram
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        listing_final[field].dropna().hist(bins=50)
        plt.title(f'Listing Final - {field} Histogram')
        
        # boxplot
        plt.subplot(1, 2, 2)
        sns.boxplot(x=listing_final[field].dropna())
        plt.title(f'Listing Final - {field} Boxplot')
        plt.show()
        
        # identify extreme outliers using IQR
        Q1 = listing_final[field].quantile(0.25)
        Q3 = listing_final[field].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = listing_final[(listing_final[field] < lower_bound) | (listing_final[field] > upper_bound)]
        print(f"Listing Final - {field} Extreme Outliers Count: {len(outliers)}")
    
    if field in sold_final.columns:
        print(f"\nSold Final - {field} Percentiles:")
        print(sold_final[field].describe())
        
        # histogram
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        sold_final[field].dropna().hist(bins=50)
        plt.title(f'Sold Final - {field} Histogram')
        
        # boxplot
        plt.subplot(1, 2, 2)
        sns.boxplot(x=sold_final[field].dropna())
        plt.title(f'Sold Final - {field} Boxplot')
        plt.show()
        
        # identify extreme outliers using IQR
        Q1 = sold_final[field].quantile(0.25)
        Q3 = sold_final[field].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = sold_final[(sold_final[field] < lower_bound) | (sold_final[field] > upper_bound)]
        print(f"Sold Final - {field} Extreme Outliers Count: {len(outliers)}")


# %%
listing_residential = listing_final[listing_final['PropertyType'] == 'Residential']
sold_residential = sold_final[sold_final['PropertyType'] == 'Residential']

# %%
# market-related fields: prices, square footage, dates, beds/baths, etc.
market_fields = [
    'ClosePrice', 'ListPrice', 'OriginalListPrice', 'LivingArea', 'LotSizeAcres',
    'BedroomsTotal', 'BathroomsTotalInteger', 'DaysOnMarket', 'YearBuilt',
    'BuildingAreaTotal', 'TaxAnnualAmount', 'AssociationFee', 'ContractStatusChangeDate',
    'PurchaseContractDate', 'ListingContractDate', 'CloseDate'
]

# metadata fields: IDs, system info, agent/office IDs, etc.
metadata_fields = [
    'ListingKey', 'ListingId', 'ListingKeyNumeric', 'MLSAreaMajor', 'MlsStatus',
    'OriginatingSystemName', 'OriginatingSystemSubName', 'ListAgentEmail',
    'ListAgentFullName', 'BuyerAgentMlsId', 'BuyerAgentFirstName', 'BuyerAgentLastName',
    'ListAgentFirstName', 'ListAgentLastName', 'ListOfficeName', 'BuyerOfficeName',
    'CoListOfficeName', 'CountyOrParish', 'StateOrProvince', 'PostalCode'
]


# %%
listing_removed = summary['listing_data']['total_rows'] - summary['listing_data']['filtered_rows']
sold_removed = summary['sold_data']['total_rows'] - summary['sold_data']['filtered_rows']

print(f"Rows removed during filtering:")
print(f"  Listing data: {listing_removed}")
print(f"  Sold data: {sold_removed}")

# %%
# choose the filtered residential dataframe to analyze
residential_df = listing_residential

def missing_data_report(df):
    total_rows = len(df)
    missing_count = df.isna().sum()
    missing_pct = missing_count / total_rows * 100
    summary = pd.DataFrame({
        'Column': df.columns,
        'Missing_Count': missing_count.values,
        'Missing_Percent': missing_pct.values
    })
    summary = summary.sort_values(by='Missing_Percent', ascending=False).reset_index(drop=True)
    return summary

missing_summary = missing_data_report(residential_df)

threshold = 0.90
high_missing_columns = missing_summary[missing_summary['Missing_Percent'] > threshold * 100]['Column'].tolist()

print("Columns with >90% missing values:")
print(high_missing_columns)

def drop_sparse_columns(df, threshold=0.90, core_fields=None):
    core_fields = [] if core_fields is None else list(core_fields)
    missing_pct = df.isna().mean()
    cols_to_drop = [col for col, pct in missing_pct.items() if pct > threshold and col not in core_fields]
    return df.drop(columns=cols_to_drop), cols_to_drop

core_fields = ['ClosePrice', 'LivingArea', 'BedroomsTotal']
cleaned_residential_df, dropped_columns = drop_sparse_columns(residential_df, threshold=threshold, core_fields=core_fields)

print("Dropped columns (non-core with >90% missing values):")
print(dropped_columns)

clean_summary = missing_summary[missing_summary['Missing_Count'] > 0].copy()
clean_summary = clean_summary[['Column', 'Missing_Count', 'Missing_Percent']]
clean_summary = clean_summary.sort_values(by='Missing_Percent', ascending=False).reset_index(drop=True)

clean_summary


# %%
import pandas as pd

# assuming we use the sold_final dataframe for the statistics, as it contains the relevant columns
# if you meant a different dataframe like residential_df, replace sold_final with it

columns_of_interest = ['ClosePrice', 'LivingArea','DaysOnMarket']

# generate descriptive statistics including 25th, 50th (median), 75th, and 95th percentiles
stats = sold_final[columns_of_interest].describe(percentiles=[0.25, 0.5, 0.75, 0.95])

# transpose for better readability (rows as columns, columns as stats)
stats_table = stats.T

# display the table
print(stats_table)


# %%
cleaned_residential_df.to_csv('filtered_residential_data.csv', index=False)


