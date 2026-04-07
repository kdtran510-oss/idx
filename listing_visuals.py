import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('listing_final.csv')
print(df.head())

Q1 = df['ListPrice'].quantile(0.25)
Q3 = df['ListPrice'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df_filtered = df[(df['ListPrice'] >= lower_bound) & (df['ListPrice'] <= upper_bound)]

plt.figure(figsize=(10, 6))
plt.hist(df_filtered['ListPrice'].dropna(), bins=50, edgecolor='black')
plt.title('Distribution of List Prices (Outliers Removed)')
plt.xlabel('List Price')
plt.ylabel('Frequency')
plt.show()

df['PropertyType'].value_counts().head(10).plot(kind='bar', figsize=(10, 6))
plt.title('Top 10 Property Types')
plt.xlabel('Property Type')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.show()

df['PropertySubType'].value_counts().head(10).plot(kind='bar', figsize=(10, 6))
plt.title('Top 10 Property Subtypes')
plt.xlabel('Property Subtype')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.show()