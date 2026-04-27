# File: level1_basic/process_all_datasets.py

import os
import sys
import email
from email import policy
from email.parser import BytesParser
import pandas as pd
import numpy as np
from pathlib import Path
from tqdm import tqdm
import json
import re
import warnings
warnings.filterwarnings('ignore')

print("""
╔══════════════════════════════════════════════════════════════════╗
║          ULTIMATE SPAM CLASSIFIER - DATA PROCESSOR               ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  Processing all downloaded datasets into unified format          ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
""")

BASE_DIR = Path('level1_basic/data')
RAW_DIR = BASE_DIR / 'raw'
PROCESSED_DIR = BASE_DIR / 'processed'

# Ensure directories exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def parse_email_file(filepath):
    """Parse an email file and extract content"""
    try:
        with open(filepath, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)
        
        # Extract headers
        subject = str(msg.get('subject', '')) if msg.get('subject') else ''
        sender = str(msg.get('from', '')) if msg.get('from') else ''
        
        # Extract body
        body = ''
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
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
        
        # Combine subject and body
        full_text = f"{subject} {body}".strip()
        
        if len(full_text) < 10:
            return None
        
        return {
            'subject': subject[:500],
            'body': body[:5000],
            'text': full_text[:5000],
            'sender': sender[:200],
        }
    
    except Exception as e:
        return None


def process_folder(folder_path, label, desc=""):
    """Process all email files in a folder"""
    emails = []
    
    if not folder_path.exists():
        print(f"   ⚠️ Folder not found: {folder_path}")
        return emails
    
    # Get all files
    files = list(folder_path.rglob('*'))
    files = [f for f in files if f.is_file() and not f.name.startswith('.')]
    
    if not files:
        return emails
    
    print(f"   Processing {len(files)} files from {desc}...")
    
    for filepath in tqdm(files, desc=f"   {label}", leave=False):
        email_data = parse_email_file(filepath)
        if email_data:
            email_data['label'] = label
            email_data['source'] = desc
            emails.append(email_data)
    
    return emails


# ================================================================
# PROCESS DATASET 1: SPAMASSASSIN
# ================================================================
print("\n" + "=" * 70)
print("📧 Processing SpamAssassin Dataset")
print("=" * 70)

spamassassin_emails = []

sa_spam_folders = [
    (RAW_DIR / 'spamassassin' / 'spam', 'spam', 'SA-spam'),
    (RAW_DIR / 'spamassassin' / 'spam_2', 'spam', 'SA-spam2'),
]

sa_ham_folders = [
    (RAW_DIR / 'spamassassin' / 'easy_ham', 'ham', 'SA-easy_ham'),
    (RAW_DIR / 'spamassassin' / 'easy_ham_2', 'ham', 'SA-easy_ham2'),
    (RAW_DIR / 'spamassassin' / 'hard_ham', 'ham', 'SA-hard_ham'),
]

for folder, label, desc in sa_spam_folders + sa_ham_folders:
    emails = process_folder(folder, label, desc)
    spamassassin_emails.extend(emails)

print(f"   ✅ SpamAssassin: {len(spamassassin_emails)} emails processed")


# ================================================================
# PROCESS DATASET 2: ENRON
# ================================================================
print("\n" + "=" * 70)
print("📧 Processing Enron Dataset")
print("=" * 70)

enron_emails = []
enron_base = RAW_DIR / 'enron' / 'maildir'

if enron_base.exists():
    # Get user folders (limit to avoid memory issues)
    user_folders = list(enron_base.iterdir())[:50]  # First 50 users
    
    print(f"   Processing emails from {len(user_folders)} users...")
    
    for user_folder in tqdm(user_folders, desc="   Enron users"):
        # Look for common email folders
        for subfolder in ['inbox', 'sent', 'sent_items', 'all_documents']:
            folder = user_folder / subfolder
            if folder.exists():
                emails = process_folder(folder, 'ham', f'Enron-{user_folder.name}')
                enron_emails.extend(emails[:100])  # Limit per folder
    
    print(f"   ✅ Enron: {len(enron_emails)} emails processed")
else:
    print("   ⏭️ Enron dataset not found, skipping...")


# ================================================================
# PROCESS DATASET 3: KAGGLE
# ================================================================
print("\n" + "=" * 70)
print("📧 Processing Kaggle Datasets")
print("=" * 70)

kaggle_emails = []
kaggle_dir = RAW_DIR / 'kaggle'

# Process SMS spam
sms_file = kaggle_dir / 'sms_spam.tsv'
if sms_file.exists():
    try:
        df_sms = pd.read_csv(sms_file, sep='\t', header=None, names=['label', 'text'])
        for _, row in df_sms.iterrows():
            kaggle_emails.append({
                'text': str(row['text']),
                'label': row['label'],
                'source': 'Kaggle-SMS',
                'subject': '',
                'body': str(row['text']),
                'sender': '',
            })
        print(f"   ✅ SMS Spam: {len(df_sms)} messages")
    except Exception as e:
        print(f"   ❌ Error processing SMS: {e}")

# Process email spam CSV
spam_csv = kaggle_dir / 'spam_emails.csv'
if spam_csv.exists():
    try:
        df_email = pd.read_csv(spam_csv, encoding='latin-1')
        # Handle different column names
        text_col = 'text' if 'text' in df_email.columns else df_email.columns[-1]
        label_col = 'label' if 'label' in df_email.columns else df_email.columns[0]
        
        for _, row in df_email.iterrows():
            kaggle_emails.append({
                'text': str(row[text_col]),
                'label': 'spam' if 'spam' in str(row[label_col]).lower() else 'ham',
                'source': 'Kaggle-Email',
                'subject': '',
                'body': str(row[text_col]),
                'sender': '',
            })
        print(f"   ✅ Email Spam: {len(df_email)} messages")
    except Exception as e:
        print(f"   ❌ Error processing email CSV: {e}")

print(f"   ✅ Kaggle Total: {len(kaggle_emails)} messages")


# ================================================================
# PROCESS DATASET 4: CSDMC/ACADEMIC
# ================================================================
print("\n" + "=" * 70)
print("📧 Processing Academic Datasets")
print("=" * 70)

academic_emails = []
csdmc_dir = RAW_DIR / 'csdmc'

# Process Ling-spam if available
lingspam_dir = csdmc_dir / 'lingspam_public'
if lingspam_dir.exists():
    spam_folders = list(lingspam_dir.rglob('*spmsg*'))
    ham_folders = list(lingspam_dir.rglob('*legit*'))
    
    for folder in spam_folders:
        if folder.is_dir():
            emails = process_folder(folder, 'spam', 'LingSpam')
            academic_emails.extend(emails)
    
    for folder in ham_folders:
        if folder.is_dir():
            emails = process_folder(folder, 'ham', 'LingSpam')
            academic_emails.extend(emails)

print(f"   ✅ Academic: {len(academic_emails)} emails processed")


# ================================================================
# PROCESS DATASET 5: NAZARIO PHISHING
# ================================================================
print("\n" + "=" * 70)
print("📧 Processing Phishing Dataset")
print("=" * 70)

phishing_emails = []
nazario_dir = RAW_DIR / 'nazario'

# Load synthetic phishing examples
phishing_json = nazario_dir / 'phishing_examples.json'
if phishing_json.exists():
    with open(phishing_json, 'r') as f:
        phishing_data = json.load(f)
    
    for item in phishing_data:
        phishing_emails.append({
            'text': item['text'],
            'label': 'spam',
            'source': 'Phishing',
            'subject': '',
            'body': item['text'],
            'sender': '',
        })
    
    print(f"   ✅ Phishing: {len(phishing_emails)} emails")


# ================================================================
# ADD CUSTOM REAL-WORLD EXAMPLES
# ================================================================
print("\n" + "=" * 70)
print("📧 Adding Custom Real-World Examples")
print("=" * 70)

custom_emails = []

# Spam examples
spam_texts = [
    "CONGRATULATIONS! You've won \$5,000,000 in our lottery! Send your bank details to claim.",
    "Make \$10,000 per week working from home! No experience needed! Limited spots!",
    "Hot singles in your area want to meet you tonight! Click here for FREE access!",
    "Your computer is infected with 47 viruses! Download our cleaner NOW!",
    "URGENT: Your bank account has been compromised! Verify immediately!",
    "FREE iPhone 15 Pro! You've been selected! Claim your prize now!",
    "Lose 30 pounds in 30 days with this miracle pill! No diet needed!",
    "Nigerian prince needs your help to transfer \$50 million. 30% commission!",
    "Your Amazon account will be suspended! Update payment information now!",
    "Bitcoin investment opportunity! 500% returns guaranteed! Act now!",
]

# Ham examples
ham_texts = [
    "Hi team, the meeting has been moved to 3 PM tomorrow. Please update your calendars.",
    "Your order has shipped! Track your package at the link in your account.",
    "Thanks for your application. We'd like to schedule an interview next week.",
    "Reminder: Your dentist appointment is scheduled for tomorrow at 10 AM.",
    "The project deadline has been extended to Friday. Let me know if you need help.",
    "Happy birthday! Hope you have a wonderful day. Let's catch up soon!",
    "Your flight confirmation: NYC to LAX on March 15th, departing at 8:00 AM.",
    "I've attached the quarterly report. Please review and send feedback.",
    "Can we reschedule our 1:1 to Thursday? I have a conflict on Tuesday.",
    "Your package has been delivered and left at the front door.",
]

for text in spam_texts:
    custom_emails.append({'text': text, 'label': 'spam', 'source': 'Custom', 
                          'subject': '', 'body': text, 'sender': ''})

for text in ham_texts:
    custom_emails.append({'text': text, 'label': 'ham', 'source': 'Custom',
                          'subject': '', 'body': text, 'sender': ''})

print(f"   ✅ Custom: {len(custom_emails)} emails")


# ================================================================
# COMBINE ALL DATASETS
# ================================================================
print("\n" + "=" * 70)
print("📊 Combining All Datasets")
print("=" * 70)

all_emails = (
    spamassassin_emails + 
    enron_emails + 
    kaggle_emails + 
    academic_emails + 
    phishing_emails + 
    custom_emails
)

# Create DataFrame
df = pd.DataFrame(all_emails)

print(f"\n📊 Combined Dataset Statistics:")
print(f"   Total emails: {len(df):,}")
print(f"   Columns: {list(df.columns)}")

# Data cleaning
print("\n🧹 Cleaning data...")

# Remove duplicates
before = len(df)
df = df.drop_duplicates(subset=['text'])
print(f"   Removed {before - len(df):,} duplicates")

# Remove empty texts
df = df[df['text'].str.len() > 10]

# Remove NaN
df = df.dropna(subset=['text', 'label'])

print(f"\n📊 Final Dataset Statistics:")
print(f"   Total emails: {len(df):,}")
print(f"   Spam: {len(df[df['label'] == 'spam']):,} ({len(df[df['label'] == 'spam'])/len(df)*100:.1f}%)")
print(f"   Ham: {len(df[df['label'] == 'ham']):,} ({len(df[df['label'] == 'ham'])/len(df)*100:.1f}%)")

print(f"\n📊 Emails by Source:")
print(df['source'].value_counts().to_string())


# ================================================================
# BALANCE DATASET (OPTIONAL)
# ================================================================
print("\n" + "=" * 70)
print("⚖️ Balancing Dataset")
print("=" * 70)

spam_count = len(df[df['label'] == 'spam'])
ham_count = len(df[df['label'] == 'ham'])

print(f"   Current: {spam_count:,} spam, {ham_count:,} ham")

# If very imbalanced, balance by undersampling majority class
if ham_count > spam_count * 3:
    print("   Dataset is imbalanced. Undersampling ham...")
    
    df_spam = df[df['label'] == 'spam']
    df_ham = df[df['label'] == 'ham'].sample(n=min(spam_count * 2, ham_count), random_state=42)
    
    df = pd.concat([df_spam, df_ham], ignore_index=True)
    print(f"   After balancing: {len(df[df['label'] == 'spam']):,} spam, {len(df[df['label'] == 'ham']):,} ham")

# Shuffle
df = df.sample(frac=1, random_state=42).reset_index(drop=True)


# ================================================================
# SAVE PROCESSED DATA
# ================================================================
print("\n" + "=" * 70)
print("💾 Saving Processed Data")
print("=" * 70)

# Save full dataset
full_path = PROCESSED_DIR / 'combined_emails.csv'
df.to_csv(full_path, index=False)
print(f"   ✅ Full dataset: {full_path}")

# Save smaller version for quick testing
sample_path = PROCESSED_DIR / 'sample_emails.csv'
df.sample(n=min(10000, len(df)), random_state=42).to_csv(sample_path, index=False)
print(f"   ✅ Sample dataset: {sample_path}")

# Save statistics
stats = {
    'total_emails': len(df),
    'spam_count': int(len(df[df['label'] == 'spam'])),
    'ham_count': int(len(df[df['label'] == 'ham'])),
    'sources': df['source'].value_counts().to_dict(),
}

stats_path = PROCESSED_DIR / 'dataset_stats.json'
with open(stats_path, 'w') as f:
    json.dump(stats, f, indent=2)
print(f"   ✅ Statistics: {stats_path}")

print("""
╔══════════════════════════════════════════════════════════════════╗
║                   PROCESSING COMPLETE! ✅                         ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  Next step: Train the model                                       ║
║  > python level1_basic/train_ultimate_model.py                   ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
""")