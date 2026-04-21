# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set a clean visual style for the charts
sns.set_theme(style="whitegrid")

def run_eda(file_path, dataset_name):
    """Loads data, generates summary statistics, and plots distributions."""
    print(f"\n{'='*50}")
    print(f" EXPLORATORY DATA ANALYSIS: {dataset_name}")
    print(f"{'='*50}")

    # 1. Load Data
    try:
        df = pd.read_csv(file_path, low_memory=False)
        print(f"\n[Dataset Shape]: {df.shape[0]} rows, {df.shape[1]} columns")
    except FileNotFoundError:
        print(f"File {file_path} not found. Skipping...")
        return

    # 2. Missing Value Report
    print("\n[Missing Value Report (>90% Missing)]")
    missing_pct = df.isnull().mean()
    high_missing = missing_pct[missing_pct > 0.90]
    
    if not high_missing.empty:
        print(f"Found {len(high_missing)} columns with >90% missing data.")
        print(high_missing.head().to_string(), "...\n")
    else:
        print("No columns have >90% missing data.\n")

    # 3. Numeric Distributions & Visualizations
    print("\n[Numeric Distributions & Visualizations]")
    
    # The exact fields requested by the intern handbook for Week 2-3
    fields = [
        'ClosePrice', 'ListPrice', 'OriginalListPrice', 'LivingArea', 
        'LotSizeAcres', 'BedroomsTotal', 'BathroomsTotalInteger', 
        'DaysOnMarket', 'YearBuilt'
    ]

    for field in fields:
        if field in df.columns:
            print(f"\n--- Analyzing {field} ---")
            
            # Drop nulls just for accurate math/plotting
            field_data = df[field].dropna()
            
            # Print Percentiles
            print(field_data.describe(percentiles=[0.25, 0.5, 0.75, 0.95]))
            
            # Calculate IQR & Outliers (Your Week 7 logic)
            Q1 = field_data.quantile(0.25)
            Q3 = field_data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = field_data[(field_data < lower_bound) | (field_data > upper_bound)]
            print(f"Extreme Outliers Count (IQR Method): {len(outliers)}")

            # Generate Visualizations
            fig, axes = plt.subplots(1, 2, figsize=(12, 4))
            
            # Histogram
            sns.histplot(field_data, bins=50, ax=axes[0], color='skyblue')
            axes[0].set_title(f'{dataset_name} - {field} Histogram')
            
            # Boxplot (Fixed the cutoff here!)
            sns.boxplot(x=field_data, ax=axes[1], color='lightgreen')
            axes[1].set_title(f'{dataset_name} - {field} Boxplot')
            
            plt.tight_layout()
            
            # This is the line that actually draws the graph on your screen!
            plt.show()

# %%
# EXECUTION BLOCK (This is the "Start Button" that runs your code)
if __name__ == "__main__":
    
    # Run EDA on the pre-appended Listings dataset
    run_eda("listing_final.csv", "Listings Data")
    
    # Run EDA on the pre-appended Sold dataset
    run_eda("sold_final.csv", "Sold Data")
# %%
