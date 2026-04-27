# File: level1_basic/notebooks/01_download_data.py

import pandas as pd
import urllib.request
import os

# Create data directory
os.makedirs('level1_basic/data', exist_ok=True)

# Download the dataset
url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
urllib.request.urlretrieve(url, 'level1_basic/data/spam.tsv')

print("Dataset downloaded successfully!")

# Load and view the data
df = pd.read_csv('level1_basic/data/spam.tsv', sep='\t', header=None, names=['label', 'message'])

print("\n--- First 10 rows ---")
print(df.head(10))

print("\n--- Dataset Info ---")
print(f"Total messages: {len(df)}")
print(f"Spam messages: {len(df[df['label'] == 'spam'])}")
print(f"Ham messages: {len(df[df['label'] == 'ham'])}")