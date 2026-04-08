# %%
import pandas as pd

listing_df = pd.read_csv("listing_final.csv")
print("original shape:", listing_df.shape)

residential_df = listing_df[listing_df["PropertyType"] == "Residential"]
print("residential shape:", residential_df.shape)

sold_df = pd.read_csv("sold_final.csv")
print("original shape:", sold_df.shape)

sold_residential_df = sold_df[sold_df["PropertyType"] == "Residential"]
print("residential shape:", sold_residential_df.shape)

# %%
residential_df.to_csv("residential_listing.csv", index=False)
sold_residential_df.to_csv("residential_sold.csv", index=False)


