# File: level1_basic/notebooks/05_feature_extraction.py

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# Load processed data
df = pd.read_csv('level1_basic/data/processed_spam.csv')

# Sample texts for demonstration
sample_texts = [
    "free money win prize",
    "meeting tomorrow office",
    "free prize winner congratulations",
    "project deadline tomorrow"
]

print("=" * 60)
print("FEATURE EXTRACTION DEMONSTRATION")
print("=" * 60)

# Method 1: Bag of Words (CountVectorizer)
print("\n1. BAG OF WORDS (CountVectorizer)")
print("-" * 40)

count_vectorizer = CountVectorizer()
count_matrix = count_vectorizer.fit_transform(sample_texts)

print(f"Vocabulary: {count_vectorizer.get_feature_names_out()}")
print(f"\nCount Matrix Shape: {count_matrix.shape}")
print(f"(4 documents, {count_matrix.shape[1]} unique words)\n")

# Display as DataFrame for clarity
count_df = pd.DataFrame(
    count_matrix.toarray(),
    columns=count_vectorizer.get_feature_names_out(),
    index=[f"Doc {i+1}" for i in range(len(sample_texts))]
)
print("Count Matrix:")
print(count_df)


# Method 2: TF-IDF
print("\n\n2. TF-IDF (Term Frequency - Inverse Document Frequency)")
print("-" * 40)

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(sample_texts)

print(f"Vocabulary: {tfidf_vectorizer.get_feature_names_out()}")
print(f"\nTF-IDF Matrix Shape: {tfidf_matrix.shape}\n")

# Display as DataFrame
tfidf_df = pd.DataFrame(
    tfidf_matrix.toarray().round(3),
    columns=tfidf_vectorizer.get_feature_names_out(),
    index=[f"Doc {i+1}" for i in range(len(sample_texts))]
)
print("TF-IDF Matrix:")
print(tfidf_df)


# Apply TF-IDF to our actual dataset
print("\n\n3. APPLYING TF-IDF TO SPAM DATASET")
print("-" * 40)

# Use TF-IDF with some parameters
tfidf = TfidfVectorizer(
    max_features=3000,    # Use top 3000 words
    min_df=2,             # Word must appear in at least 2 documents
    max_df=0.95,          # Ignore words appearing in >95% documents
    ngram_range=(1, 2)    # Use single words and word pairs
)

X = tfidf.fit_transform(df['processed_message'].fillna(''))

print(f"Feature Matrix Shape: {X.shape}")
print(f"Number of documents: {X.shape[0]}")
print(f"Number of features: {X.shape[1]}")

# Show some features
print(f"\nSample features: {tfidf.get_feature_names_out()[:20]}")

# Save the vectorizer for later use
import joblib
joblib.dump(tfidf, 'level1_basic/models/tfidf_vectorizer.joblib')
print("\nTF-IDF vectorizer saved!")