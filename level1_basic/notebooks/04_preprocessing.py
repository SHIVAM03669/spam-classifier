# File: level1_basic/notebooks/04_preprocessing.py

import pandas as pd
import re
import nltk

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Load data
df = pd.read_csv('level1_basic/data/spam.tsv', sep='\t', header=None, names=['label', 'message'])

# Initialize tools
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


def preprocess_text(text):
    """
    Complete text preprocessing pipeline
    """
    # Step 1: Convert to lowercase
    text = text.lower()
    
    # Step 2: Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    
    # Step 3: Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Step 4: Remove phone numbers
    text = re.sub(r'\b\d{10,}\b', '', text)
    
    # Step 5: Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Step 6: Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Step 7: Tokenize
    tokens = word_tokenize(text)
    
    # Step 8: Remove stopwords and apply stemming
    processed_tokens = []
    for token in tokens:
        if token not in stop_words and len(token) > 2:
            # Apply stemming
            stemmed = stemmer.stem(token)
            processed_tokens.append(stemmed)
    
    # Step 9: Join tokens back
    return ' '.join(processed_tokens)


# Test the preprocessing
print("=" * 60)
print("PREPROCESSING EXAMPLES")
print("=" * 60)

test_messages = [
    "FREE!!! You've WON \$1000 CASH! Call 0800-123-456 NOW!!!",
    "Hi John, are you coming to the meeting tomorrow at 3pm?",
    "URGENT: Your account has been compromised! Click http://fake.com"
]

for msg in test_messages:
    print(f"\nOriginal:  {msg}")
    print(f"Processed: {preprocess_text(msg)}")
    print("-" * 60)

# Apply preprocessing to entire dataset
print("\nProcessing entire dataset...")
df['processed_message'] = df['message'].apply(preprocess_text)

# Save processed data
df.to_csv('level1_basic/data/processed_spam.csv', index=False)
print("Processed data saved to 'processed_spam.csv'")

# Show sample
print("\n--- Sample Processed Data ---")
print(df[['label', 'message', 'processed_message']].head())