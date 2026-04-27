# File: level1_basic/notebooks/02_explore_data.py

import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('level1_basic/data/spam.tsv', sep='\t', header=None, names=['label', 'message'])

# Basic statistics
print("=" * 50)
print("DATASET EXPLORATION")
print("=" * 50)

# 1. Check for missing values
print("\n1. Missing Values:")
print(df.isnull().sum())

# 2. Label distribution
print("\n2. Label Distribution:")
print(df['label'].value_counts())
print(f"\nSpam percentage: {(df['label'] == 'spam').mean() * 100:.2f}%")

# 3. Message length analysis
df['length'] = df['message'].apply(len)
df['word_count'] = df['message'].apply(lambda x: len(x.split()))

print("\n3. Message Length Statistics:")
print(df.groupby('label')[['length', 'word_count']].mean())

# 4. Sample messages
print("\n4. Sample SPAM messages:")
print("-" * 50)
for msg in df[df['label'] == 'spam']['message'].head(3):
    print(f"• {msg[:100]}...")
    print()

print("\n5. Sample HAM (not spam) messages:")
print("-" * 50)
for msg in df[df['label'] == 'ham']['message'].head(3):
    print(f"• {msg[:100]}...")
    print()