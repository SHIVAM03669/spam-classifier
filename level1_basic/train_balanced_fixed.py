# File: level1_basic/train_balanced_fixed.py

import pandas as pd
import numpy as np
import re
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_auc_score
)
import joblib
import warnings
warnings.filterwarnings('ignore')

print("""
╔══════════════════════════════════════════════════════════════════╗
║           BALANCED SPAM CLASSIFIER TRAINING (FIXED)              ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  Training with balanced spam/ham data                             ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
""")

BASE_DIR = Path('level1_basic/data')
RAW_DIR = BASE_DIR / 'raw'
MODELS_DIR = Path('level1_basic/models')
MODELS_DIR.mkdir(parents=True, exist_ok=True)


# ================================================================
# HELPER FUNCTIONS
# ================================================================

import email
from email import policy
from email.parser import BytesParser
from tqdm import tqdm

def parse_email_file(filepath):
    """Parse email file and extract text"""
    try:
        with open(filepath, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)
        
        subject = str(msg.get('subject', '')) if msg.get('subject') else ''
        body = ''
        
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    try:
                        payload = part.get_payload(decode=True)
                        if payload:
                            body = payload.decode('utf-8', errors='ignore')
                        break
                    except:
                        pass
        else:
            try:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode('utf-8', errors='ignore')
            except:
                body = str(msg.get_payload())
        
        full_text = f"{subject} {body}".strip()
        return full_text[:5000] if len(full_text) > 10 else None
    except:
        return None


def process_folder(folder_path, label):
    """Process all emails in a folder"""
    emails = []
    if not folder_path.exists():
        return emails
    
    files = [f for f in folder_path.rglob('*') if f.is_file() and not f.name.startswith('.')]
    for filepath in files:
        text = parse_email_file(filepath)
        if text and len(text) > 10:
            emails.append({'text': text, 'label': label})
    return emails


# ================================================================
# STEP 1: LOAD ALL DATA
# ================================================================
print("\n" + "=" * 70)
print("📂 STEP 1: Loading All Data")
print("=" * 70)

spam_emails = []
ham_emails = []

# ─────────────────────────────────────────────────────────────────
# LOAD SPAM DATA
# ─────────────────────────────────────────────────────────────────
print("\n🔴 Loading SPAM data...")

# 1. SpamAssassin spam
for folder_name in ['spam', 'spam_2']:
    folder = RAW_DIR / 'spamassassin' / folder_name
    if folder.exists():
        emails = process_folder(folder, 'spam')
        spam_emails.extend(emails)
        print(f"   ✅ SpamAssassin {folder_name}: {len(emails)}")

# 2. Comprehensive spam (generated)
spam_json = RAW_DIR / 'additional_spam' / 'comprehensive_spam.json'
if spam_json.exists():
    try:
        with open(spam_json, 'r', encoding='utf-8') as f:
            spam_data = json.load(f)
        for item in spam_data:
            if isinstance(item, dict) and 'text' in item:
                spam_emails.append({'text': item['text'], 'label': 'spam'})
            elif isinstance(item, str):
                spam_emails.append({'text': item, 'label': 'spam'})
        print(f"   ✅ Comprehensive spam: {len(spam_data)}")
    except Exception as e:
        print(f"   ⚠️ Error loading comprehensive spam: {e}")

# 3. Phishing/Nazario examples
nazario_dir = RAW_DIR / 'nazario'
if nazario_dir.exists():
    for json_file in nazario_dir.glob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for item in data:
                if isinstance(item, dict):
                    text = item.get('text', '')
                    label = item.get('label', 'spam').lower()
                    if label == 'spam' and text:
                        spam_emails.append({'text': text, 'label': 'spam'})
            print(f"   ✅ {json_file.name}: loaded")
        except Exception as e:
            print(f"   ⚠️ {json_file.name}: {e}")

# 4. Kaggle SMS spam
sms_file = RAW_DIR / 'kaggle' / 'sms_spam.tsv'
if sms_file.exists():
    try:
        df_sms = pd.read_csv(sms_file, sep='\t', header=None, names=['label', 'text'])
        spam_sms = df_sms[df_sms['label'] == 'spam']
        for _, row in spam_sms.iterrows():
            spam_emails.append({'text': str(row['text']), 'label': 'spam'})
        print(f"   ✅ Kaggle SMS spam: {len(spam_sms)}")
    except Exception as e:
        print(f"   ⚠️ Kaggle SMS error: {e}")

print(f"\n   📊 Total SPAM loaded: {len(spam_emails)}")


# ─────────────────────────────────────────────────────────────────
# LOAD HAM DATA
# ─────────────────────────────────────────────────────────────────
print("\n🟢 Loading HAM data...")

# 1. SpamAssassin ham
for folder_name in ['easy_ham', 'easy_ham_2', 'hard_ham']:
    folder = RAW_DIR / 'spamassassin' / folder_name
    if folder.exists():
        emails = process_folder(folder, 'ham')
        ham_emails.extend(emails)
        print(f"   ✅ SpamAssassin {folder_name}: {len(emails)}")

# 2. Enron ham (sample for balance)
enron_base = RAW_DIR / 'enron' / 'maildir'
MAX_ENRON = 25000

if enron_base.exists():
    user_folders = list(enron_base.iterdir())
    enron_count = 0
    
    for user_folder in tqdm(user_folders, desc="   Enron"):
        if enron_count >= MAX_ENRON:
            break
        if not user_folder.is_dir():
            continue
        
        for subfolder in ['inbox', 'sent']:
            if enron_count >= MAX_ENRON:
                break
            folder = user_folder / subfolder
            if folder.exists():
                emails = process_folder(folder, 'ham')
                remaining = MAX_ENRON - enron_count
                ham_emails.extend(emails[:remaining])
                enron_count += min(len(emails), remaining)
    
    print(f"   ✅ Enron: {enron_count}")

# 3. Kaggle SMS ham
if sms_file.exists():
    try:
        ham_sms = df_sms[df_sms['label'] == 'ham']
        for _, row in ham_sms.iterrows():
            ham_emails.append({'text': str(row['text']), 'label': 'ham'})
        print(f"   ✅ Kaggle SMS ham: {len(ham_sms)}")
    except:
        pass

# 4. Extended ham examples
nazario_dir = RAW_DIR / 'nazario'
if nazario_dir.exists():
    for json_file in nazario_dir.glob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for item in data:
                if isinstance(item, dict):
                    text = item.get('text', '')
                    label = item.get('label', '').lower()
                    if label == 'ham' and text:
                        ham_emails.append({'text': text, 'label': 'ham'})
        except:
            pass

print(f"\n   📊 Total HAM loaded: {len(ham_emails)}")


# ─────────────────────────────────────────────────────────────────
# COMBINE & VERIFY DATA
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("📊 Combining Data")
print("=" * 70)

all_emails = spam_emails + ham_emails

print(f"\n   Before cleaning:")
print(f"   Total: {len(all_emails):,}")
print(f"   Spam: {len(spam_emails):,}")
print(f"   Ham: {len(ham_emails):,}")

# Create DataFrame
df = pd.DataFrame(all_emails)

# Debug: Check what we have
print(f"\n   DataFrame columns: {list(df.columns)}")
print(f"   DataFrame shape: {df.shape}")

if 'label' in df.columns:
    print(f"   Unique labels: {df['label'].unique()[:10]}")

# Check for empty DataFrame
if len(df) == 0:
    print("\n❌ ERROR: No data loaded! Check your data folders.")
    print(f"   Looking in: {RAW_DIR}")
    exit(1)


# ================================================================
# STEP 2: CLEAN DATA
# ================================================================
print("\n" + "=" * 70)
print("🧹 STEP 2: Cleaning Data")
print("=" * 70)

before = len(df)

# Remove duplicates
df = df.drop_duplicates(subset=['text'])
print(f"   Removed {before - len(df):,} duplicates")

# Remove empty/short texts
df = df[df['text'].str.len() > 15]

# Remove NaN
df = df.dropna(subset=['text', 'label'])

# Normalize labels (make sure lowercase)
df['label'] = df['label'].astype(str).str.lower().str.strip()

# Filter only valid labels
df = df[df['label'].isin(['spam', 'ham'])]

# Final counts
spam_count = len(df[df['label'] == 'spam'])
ham_count = len(df[df['label'] == 'ham'])
total = len(df)

print(f"\n   After cleaning:")
print(f"   Total: {total:,}")
print(f"   Spam: {spam_count:,} ({spam_count/total*100:.1f}%)" if total > 0 else "   Spam: 0")
print(f"   Ham: {ham_count:,} ({ham_count/total*100:.1f}%)" if total > 0 else "   Ham: 0")

# Safety check
if total == 0:
    print("\n❌ ERROR: No data after cleaning!")
    print("   Debug info:")
    print(f"   Original spam_emails: {len(spam_emails)}")
    print(f"   Original ham_emails: {len(ham_emails)}")
    exit(1)


# ================================================================
# STEP 3: BALANCE DATASET
# ================================================================
print("\n" + "=" * 70)
print("⚖️ STEP 3: Balancing Dataset")
print("=" * 70)

# Calculate ideal balance (aim for ~35% spam)
target_spam_ratio = 0.35
current_spam_ratio = spam_count / total

print(f"   Current spam ratio: {current_spam_ratio*100:.1f}%")
print(f"   Target spam ratio: {target_spam_ratio*100:.1f}%")

if current_spam_ratio < 0.20:
    # Too little spam - undersample ham
    target_ham = int(spam_count / target_spam_ratio * (1 - target_spam_ratio))
    
    print(f"   Undersampling ham from {ham_count:,} to {target_ham:,}")
    
    df_spam = df[df['label'] == 'spam']
    df_ham = df[df['label'] == 'ham'].sample(n=min(target_ham, ham_count), random_state=42)
    
    df = pd.concat([df_spam, df_ham], ignore_index=True)
    
elif current_spam_ratio > 0.50:
    # Too much spam - undersample spam
    target_spam = int(ham_count * target_spam_ratio / (1 - target_spam_ratio))
    
    print(f"   Undersampling spam from {spam_count:,} to {target_spam:,}")
    
    df_spam = df[df['label'] == 'spam'].sample(n=min(target_spam, spam_count), random_state=42)
    df_ham = df[df['label'] == 'ham']
    
    df = pd.concat([df_spam, df_ham], ignore_index=True)
else:
    print(f"   Dataset is reasonably balanced, keeping as is.")

# Shuffle
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Final counts
spam_count = len(df[df['label'] == 'spam'])
ham_count = len(df[df['label'] == 'ham'])
total = len(df)

print(f"\n   Final balanced dataset:")
print(f"   Total: {total:,}")
print(f"   Spam: {spam_count:,} ({spam_count/total*100:.1f}%)")
print(f"   Ham: {ham_count:,} ({ham_count/total*100:.1f}%)")


# ================================================================
# STEP 4: PREPROCESSING
# ================================================================
print("\n" + "=" * 70)
print("🔧 STEP 4: Preprocessing")
print("=" * 70)

def preprocess(text):
    if not isinstance(text, str):
        return ""
    
    text = text.lower()
    
    # Replace patterns with tokens
    text = re.sub(r'http\S+|www\.\S+', ' __URL__ ', text)
    text = re.sub(r'\S+@\S+', ' __EMAIL__ ', text)
    text = re.sub(r'\$\s?\d+(?:[,\.]\d+)*', ' __MONEY__ ', text)
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', ' __PHONE__ ', text)
    text = re.sub(r'\b\d+\b', ' __NUM__ ', text)
    text = re.sub(r'[!]{2,}', ' __EXCLAIM__ ', text)
    
    # Remove special characters
    text = re.sub(r'[^a-zA-Z_\s]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

print("   Applying preprocessing...")
df['processed'] = df['text'].apply(preprocess)
df['label_encoded'] = (df['label'] == 'spam').astype(int)

# Remove too short
df = df[df['processed'].str.len() > 5]

print(f"   ✅ Preprocessed {len(df):,} emails")


# ================================================================
# STEP 5: FEATURE EXTRACTION
# ================================================================
print("\n" + "=" * 70)
print("🔢 STEP 5: Feature Extraction (TF-IDF)")
print("=" * 70)

tfidf = TfidfVectorizer(
    max_features=15000,
    min_df=2,
    max_df=0.9,
    ngram_range=(1, 3),
    sublinear_tf=True,
)

X = tfidf.fit_transform(df['processed'])
y = df['label_encoded'].values

print(f"   ✅ Feature matrix: {X.shape[0]:,} samples, {X.shape[1]:,} features")


# ================================================================
# STEP 6: TRAIN/TEST SPLIT
# ================================================================
print("\n" + "=" * 70)
print("✂️ STEP 6: Train/Test Split")
print("=" * 70)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"   ✅ Training: {X_train.shape[0]:,} samples")
print(f"   ✅ Testing: {X_test.shape[0]:,} samples")


# ================================================================
# STEP 7: TRAIN MODELS
# ================================================================
print("\n" + "=" * 70)
print("🤖 STEP 7: Training Models")
print("=" * 70)

models = {
    'Naive Bayes': MultinomialNB(alpha=0.1),
    'Logistic Regression': LogisticRegression(
        max_iter=1000, 
        class_weight='balanced', 
        n_jobs=-1,
        random_state=42
    ),
    'SGD Classifier': SGDClassifier(
        loss='modified_huber', 
        max_iter=1000, 
        class_weight='balanced', 
        n_jobs=-1, 
        random_state=42
    ),
    'Linear SVM': CalibratedClassifierCV(
        LinearSVC(C=1.0, max_iter=2000, class_weight='balanced', dual='auto'), 
        cv=3
    ),
}

results = {}

for name, model in models.items():
    print(f"\n🔄 Training {name}...")
    
    try:
        # Train
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        
        # Get probabilities
        if hasattr(model, 'predict_proba'):
            y_proba = model.predict_proba(X_test)[:, 1]
        else:
            y_proba = y_pred
        
        # Calculate metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        try:
            auc = roc_auc_score(y_test, y_proba)
        except:
            auc = 0
        
        results[name] = {
            'model': model,
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1': f1,
            'auc': auc,
            'predictions': y_pred,
        }
        
        print(f"   ✅ Accuracy: {acc*100:.2f}% | Precision: {prec*100:.2f}% | Recall: {rec*100:.2f}% | F1: {f1*100:.2f}%")
        
    except Exception as e:
        print(f"   ❌ Error training {name}: {e}")


# ================================================================
# STEP 8: MODEL COMPARISON
# ================================================================
print("\n" + "=" * 70)
print("📊 STEP 8: Model Comparison")
print("=" * 70)

print(f"\n{'Model':<25} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1':<12}")
print("-" * 73)

best_name = None
best_f1 = 0

for name, r in results.items():
    print(f"{name:<25} {r['accuracy']*100:>6.2f}%     {r['precision']*100:>6.2f}%     {r['recall']*100:>6.2f}%     {r['f1']*100:>6.2f}%")
    
    if r['f1'] > best_f1:
        best_f1 = r['f1']
        best_name = name

print("-" * 73)
print(f"\n🏆 Best Model: {best_name} (F1: {best_f1*100:.2f}%)")


# ================================================================
# STEP 9: DETAILED EVALUATION
# ================================================================
print("\n" + "=" * 70)
print("📈 STEP 9: Detailed Evaluation")
print("=" * 70)

best_model = results[best_name]['model']
y_pred_best = results[best_name]['predictions']

print(f"\n📊 Classification Report ({best_name}):")
print("-" * 55)
print(classification_report(y_test, y_pred_best, target_names=['Ham', 'Spam']))

cm = confusion_matrix(y_test, y_pred_best)
print(f"""
📊 Confusion Matrix:
                    Predicted
                 Ham        Spam
Actual Ham      {cm[0][0]:>6,}     {cm[0][1]:>6,}
Actual Spam     {cm[1][0]:>6,}     {cm[1][1]:>6,}

✅ True Negatives (Ham correct):     {cm[0][0]:>6,}
⚠️ False Positives (Ham → Spam):    {cm[0][1]:>6,}
⚠️ False Negatives (Spam → Ham):    {cm[1][0]:>6,}
✅ True Positives (Spam correct):    {cm[1][1]:>6,}
""")


# ================================================================
# STEP 10: SAVE MODEL
# ================================================================
print("=" * 70)
print("💾 STEP 10: Saving Model")
print("=" * 70)

model_path = MODELS_DIR / 'spam_classifier.joblib'
vectorizer_path = MODELS_DIR / 'tfidf_vectorizer.joblib'
info_path = MODELS_DIR / 'model_info.json'

joblib.dump(best_model, model_path)
joblib.dump(tfidf, vectorizer_path)

model_info = {
    'model_type': best_name,
    'metrics': {
        'accuracy': float(results[best_name]['accuracy']),
        'precision': float(results[best_name]['precision']),
        'recall': float(results[best_name]['recall']),
        'f1_score': float(results[best_name]['f1']),
        'auc_roc': float(results[best_name]['auc']),
    },
    'dataset': {
        'total_samples': int(total),
        'spam_samples': int(spam_count),
        'ham_samples': int(ham_count),
        'spam_ratio': float(spam_count / total),
    },
    'features': int(X.shape[1]),
}

with open(info_path, 'w') as f:
    json.dump(model_info, f, indent=2)

print(f"   ✅ Model saved: {model_path}")
print(f"   ✅ Vectorizer saved: {vectorizer_path}")
print(f"   ✅ Info saved: {info_path}")


# ================================================================
# STEP 11: TESTING
# ================================================================
print("\n" + "=" * 70)
print("🧪 STEP 11: Testing with Examples")
print("=" * 70)

test_cases = [
    # Spam examples
    ("URGENT: You've won \$1,000,000! Click here to claim now!", "SPAM"),
    ("Your PayPal account has been compromised! Verify immediately!", "SPAM"),
    ("Make \$5000/week working from home! No experience needed!", "SPAM"),
    ("Hot singles in your area want to meet tonight!", "SPAM"),
    ("FREE iPhone! You've been selected as our winner!", "SPAM"),
    ("Your bank account is at risk! Update your information now!", "SPAM"),
    
    # Ham examples
    ("Hi team, meeting moved to 3 PM tomorrow.", "HAM"),
    ("Your Amazon order has shipped. Track your package.", "HAM"),
    ("Can we schedule a call for next Tuesday?", "HAM"),
    ("Thanks for dinner last night! It was great.", "HAM"),
    ("The quarterly report is attached for review.", "HAM"),
    ("Reminder: Your dentist appointment is tomorrow at 10 AM.", "HAM"),
]

print("\n🧪 Test Results:\n")
correct = 0

for text, expected in test_cases:
    processed = preprocess(text)
    vec = tfidf.transform([processed])
    pred = best_model.predict(vec)[0]
    
    if hasattr(best_model, 'predict_proba'):
        proba = best_model.predict_proba(vec)[0]
        conf = max(proba) * 100
    else:
        conf = 95
    
    label = "SPAM" if pred == 1 else "HAM"
    is_correct = label == expected
    correct += is_correct
    
    icon = "✓" if is_correct else "✗"
    emoji = "🚫" if label == "SPAM" else "✅"
    
    print(f"{icon} {emoji} {label} ({conf:.0f}%) | Expected: {expected}")
    print(f"   \"{text[:50]}...\"")
    print()

print(f"Test Accuracy: {correct}/{len(test_cases)} ({correct/len(test_cases)*100:.0f}%)")


# ================================================================
# FINAL SUMMARY
# ================================================================
print("\n" + "=" * 70)
print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                    TRAINING COMPLETE! 🎉                          ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  📊 Dataset:                                                       ║
║     • Total:    {total:>10,}                                       
║     • Spam:     {spam_count:>10,} ({spam_count/total*100:.1f}%)                             
║     • Ham:      {ham_count:>10,} ({ham_count/total*100:.1f}%)                             
║                                                                   ║
║  🤖 Best Model: {best_name:<25}                                   
║     • Accuracy:   {results[best_name]['accuracy']*100:>8.2f}%                             
║     • Precision:  {results[best_name]['precision']*100:>8.2f}%                             
║     • Recall:     {results[best_name]['recall']*100:>8.2f}%                             
║     • F1 Score:   {results[best_name]['f1']*100:>8.2f}%                             
║                                                                   ║
║  📁 Files:                                                         ║
║     • {model_path}
║     • {vectorizer_path}
║                                                                   ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  🚀 Next Step: Run the web app                                     ║
║     > python level1_basic/app/app.py                              ║
║     > Open: http://localhost:5000                                 ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
""")