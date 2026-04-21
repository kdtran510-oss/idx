import pandas as pd
import glob

def aggregate_monthly_files(file_pattern, output_filename, dataset_name):
    """Finds, concatenates, and saves monthly MLS files without filtering."""
    print(f"\n--- Processing {dataset_name} Data ---")
    
    # 1. Find all matching files
    files = sorted(glob.glob(file_pattern))
    if not files:
        print(f"No files found matching: {file_pattern}")
        return
        
    print(f"Found {len(files)} {dataset_name} files to combine.")
    
    # 2. Concatenate all files into one DataFrame
    df = pd.concat([pd.read_csv(f, low_memory=False) for f in files], ignore_index=True)
    print(f"Row count AFTER concatenation: {len(df)}")
        
    # 3. Save to final master CSV
    df.to_csv(output_filename, index=False)
    print(f"Successfully saved to {output_filename}")


if __name__ == "__main__":
    
    # Process Listings Data
    aggregate_monthly_files(
        file_pattern="/Users/khoatran/Desktop/da5/csvs/CRMLSListing*.csv",
        output_filename="listing_final.csv",
        dataset_name="Listings"
    )
    
    # Process Sold Data
    aggregate_monthly_files(
        file_pattern="/Users/khoatran/Desktop/da5/csvs/CRMLSSold*.csv",  # Adjust if your sold files are named differently
        output_filename="sold_final.csv",
        dataset_name="Sold"
    )