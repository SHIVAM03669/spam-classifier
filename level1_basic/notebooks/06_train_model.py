# File: level1_basic/notebooks/06_train_model.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("SPAM CLASSIFIER - MODEL TRAINING")
print("=" * 60)

# Step 1: Load and prepare data
print("\n📁 Step 1: Loading data...")
df = pd.read_csv('level1_basic/data/processed_spam.csv')

# Handle any missing values
df['processed_message'] = df['processed_message'].fillna('')

# Convert labels to binary (0 = ham, 1 = spam)
df['label_encoded'] = (df['label'] == 'spam').astype(int)

X = df['processed_message']
y = df['label_encoded']

print(f"   Total samples: {len(df)}")
print(f"   Spam: {sum(y)} | Ham: {len(y) - sum(y)}")


# Step 2: Feature Extraction
print("\n🔢 Step 2: Extracting features (TF-IDF)...")
tfidf = TfidfVectorizer(
    max_features=3000,
    min_df=2,
    max_df=0.95,
    ngram_range=(1, 2)
)
X_tfidf = tfidf.fit_transform(X)
print(f"   Feature matrix shape: {X_tfidf.shape}")


# Step 3: Split data
print("\n✂️ Step 3: Splitting data (80% train, 20% test)...")
X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf, y, 
    test_size=0.2, 
    random_state=42,
    stratify=y  # Maintain spam/ham ratio in both sets
)
print(f"   Training samples: {X_train.shape[0]}")
print(f"   Testing samples: {X_test.shape[0]}")


# Step 4: Train multiple models
print("\n🤖 Step 4: Training models...")
print("-" * 60)

models = {
    'Naive Bayes': MultinomialNB(),
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'Support Vector Machine': SVC(kernel='linear', probability=True),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
}

results = {}

for name, model in models.items():
    print(f"\n   Training {name}...")
    
    # Train
    model.fit(X_train, y_train)
    
    # Predict
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    results[name] = {
        'model': model,
        'accuracy': accuracy,
        'predictions': y_pred
    }
    
    print(f"   ✅ {name}: {accuracy:.4f} ({accuracy*100:.2f}%)")


# Step 5: Compare models
print("\n\n📊 Step 5: Model Comparison")
print("=" * 60)
print(f"{'Model':<30} {'Accuracy':<15}")
print("-" * 45)

best_model_name = None
best_accuracy = 0

for name, result in results.items():
    print(f"{name:<30} {result['accuracy']*100:.2f}%")
    if result['accuracy'] > best_accuracy:
        best_accuracy = result['accuracy']
        best_model_name = name

print("-" * 45)
print(f"\n🏆 Best Model: {best_model_name} ({best_accuracy*100:.2f}%)")


# Step 6: Detailed evaluation of best model
print("\n\n📈 Step 6: Detailed Evaluation of Best Model")
print("=" * 60)

best_model = results[best_model_name]['model']
y_pred_best = results[best_model_name]['predictions']

print(f"\nClassification Report for {best_model_name}:")
print("-" * 45)
print(classification_report(y_test, y_pred_best, target_names=['Ham', 'Spam']))

print("\nConfusion Matrix:")
print("-" * 45)
cm = confusion_matrix(y_test, y_pred_best)
print(f"""
                 Predicted
              Ham    Spam
Actual Ham    {cm[0][0]:<6} {cm[0][1]:<6}
Actual Spam   {cm[1][0]:<6} {cm[1][1]:<6}
""")

print(f"""
Interpretation:
• True Negatives (Ham correctly identified):  {cm[0][0]}
• False Positives (Ham incorrectly as Spam):  {cm[0][1]}
• False Negatives (Spam incorrectly as Ham):  {cm[1][0]}
• True Positives (Spam correctly identified): {cm[1][1]}
""")


# Step 7: Save the best model
print("\n💾 Step 7: Saving model and vectorizer...")
print("-" * 45)

joblib.dump(best_model, 'level1_basic/models/spam_classifier.joblib')
joblib.dump(tfidf, 'level1_basic/models/tfidf_vectorizer.joblib')

print("✅ Model saved: level1_basic/models/spam_classifier.joblib")
print("✅ Vectorizer saved: level1_basic/models/tfidf_vectorizer.joblib")


# Step 8: Test with custom messages
print("\n\n🧪 Step 8: Testing with Custom Messages")
print("=" * 60)

test_messages = [
    "Congratulations! You've won a free iPhone! Click here now!",
    "Hi, can we schedule a meeting for tomorrow at 2pm?",
    "URGENT: Your bank account has been compromised! Verify now!",
    "Don't forget to buy milk on your way home.",
    "FREE ENTRY to win \$10000 cash! Text WIN to 80800",
    "The project deadline has been extended to Friday."
]

print("\nPredictions:")
print("-" * 60)

for msg in test_messages:
    # Preprocess (simplified)
    import re
    processed = re.sub(r'[^a-zA-Z\s]', '', msg.lower())
    
    # Transform and predict
    msg_tfidf = tfidf.transform([processed])
    prediction = best_model.predict(msg_tfidf)[0]
    probability = best_model.predict_proba(msg_tfidf)[0]
    
    label = "🚫 SPAM" if prediction == 1 else "✅ HAM"
    confidence = max(probability) * 100
    
    print(f"\n{label} ({confidence:.1f}% confident)")
    print(f"   \"{msg[:60]}{'...' if len(msg) > 60 else ''}\"")

print("\n" + "=" * 60)
print("Training complete! 🎉")