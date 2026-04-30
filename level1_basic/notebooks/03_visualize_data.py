# File: level1_basic/notebooks/03_visualize_data.py

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Resolve paths from this file's location so execution works from any CWD.
project_root = Path(__file__).resolve().parents[2]
data_dir = project_root / 'level1_basic' / 'data'
input_path = data_dir / 'spam.tsv'
output_path = data_dir / 'data_visualization.png'

if not input_path.exists():
    raise FileNotFoundError(
        f"Dataset not found at '{input_path}'. "
        "Run level1_basic/notebooks/01_download_data.py first."
    )

# Load data
df = pd.read_csv(input_path, sep='\t', header=None, names=['label', 'message'])
df['length'] = df['message'].apply(len)

# Create visualization
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Plot 1: Label Distribution
colors = ['#2ecc71', '#e74c3c']
df['label'].value_counts().plot(kind='bar', ax=axes[0], color=colors)
axes[0].set_title('Spam vs Ham Distribution', fontsize=14)
axes[0].set_xlabel('Label')
axes[0].set_ylabel('Count')
axes[0].tick_params(axis='x', rotation=0)

# Plot 2: Message Length Distribution
df[df['label'] == 'ham']['length'].hist(ax=axes[1], bins=50, alpha=0.7, label='Ham', color='#2ecc71')
df[df['label'] == 'spam']['length'].hist(ax=axes[1], bins=50, alpha=0.7, label='Spam', color='#e74c3c')
axes[1].set_title('Message Length Distribution', fontsize=14)
axes[1].set_xlabel('Message Length (characters)')
axes[1].set_ylabel('Frequency')
axes[1].legend()

# Plot 3: Average Length Comparison
avg_lengths = df.groupby('label')['length'].mean()
avg_lengths.plot(kind='bar', ax=axes[2], color=colors)
axes[2].set_title('Average Message Length', fontsize=14)
axes[2].set_xlabel('Label')
axes[2].set_ylabel('Average Length')
axes[2].tick_params(axis='x', rotation=0)

plt.tight_layout()
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output_path, dpi=150)
plt.show()

print("Visualization saved!")