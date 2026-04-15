# %%
sold = pd.read_csv("filtered_sold_residential.csv")
listings = pd.read_csv("filtered_listing_residential.csv")
import pandas as pd
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=['observation_date'])
mortgage.columns = ['date', 'rate_30yr_fixed']

# %%
mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly = (
mortgage.groupby('year_month')[ 'rate_30yr_fixed']
.mean().reset_index())

# %%
sold['year_month'] = pd.to_datetime(sold['CloseDate']).dt.to_period('M')
listings['year_month'] = pd.to_datetime(
listings['ListingContractDate']).dt.to_period('M')

# %%
sold_with_rates = sold.merge(mortgage_monthly, on='year_month', how='left')
listings_with_rates = listings.merge(mortgage_monthly, on='year_month', how='left')

# %%
# Check for any unmatched rows (rate should not be null)
print(sold_with_rates['rate_30yr_fixed'].isnull().sum())
print(listings_with_rates['rate_30yr_fixed'].isnull().sum())
# Preview
print(sold_with_rates[['CloseDate', 'year_month', 'ClosePrice',
'rate_30yr_fixed']].head())


# %%
sold_with_rates.to_csv('sold_enriched.csv', index=False)
listings_with_rates.to_csv('listings_enriched.csv', index=False)


