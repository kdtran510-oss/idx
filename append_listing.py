import pandas as pd
import glob

files = sorted(glob.glob("/Users/khoatran/Desktop/da5/csvs/CRMLSSold*.csv"))  # adjust pattern to match your filenames
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

print(f"Loaded {len(files)} files, {len(df)} total rows")

print(df.info())
print(df.describe())
print(df.isnull().sum())

df.to_csv("sold_final.csv", index=False)