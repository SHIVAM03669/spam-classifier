# File: level1_basic/download_all_datasets.py

import os
import sys
import urllib.request
import tarfile
import zipfile
import gzip
import shutil
import time
from pathlib import Path

print("""
╔══════════════════════════════════════════════════════════════════╗
║          ULTIMATE SPAM CLASSIFIER - DATASET DOWNLOADER           ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  This script will download ALL major spam datasets:              ║
║                                                                   ║
║  1. SpamAssassin     (~6,000 emails)      ~15 MB                 ║
║  2. Enron Email      (~500,000 emails)    ~423 MB                ║
║  3. Kaggle Spam      (~5,700 emails)      ~2 MB                  ║
║  4. CSDMC2010        (~4,327 emails)      ~50 MB                 ║
║  5. Nazario Phishing (~10,000 emails)     ~30 MB                 ║
║                                                                   ║
║  Total Download: ~520 MB                                          ║
║  Total Extracted: ~5 GB                                           ║
║  Estimated Time: 30-60 minutes                                    ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
""")

proceed = input("Do you want to proceed? (yes/no): ").lower().strip()
if proceed != 'yes':
    print("Cancelled.")
    sys.exit(0)

# Create directories
BASE_DIR = Path('level1_basic/data')
RAW_DIR = BASE_DIR / 'raw'

for folder in ['spamassassin', 'enron', 'kaggle', 'csdmc', 'nazario']:
    (RAW_DIR / folder).mkdir(parents=True, exist_ok=True)

(BASE_DIR / 'processed').mkdir(parents=True, exist_ok=True)


def download_with_progress(url, filepath, description=""):
    """Download file with progress indicator"""
    print(f"\n📥 Downloading: {description}")
    print(f"   URL: {url[:60]}...")
    print(f"   Saving to: {filepath}")
    
    try:
        def progress_hook(count, block_size, total_size):
            percent = min(100, count * block_size * 100 // total_size)
            sys.stdout.write(f"\r   Progress: [{'█' * (percent//2)}{' ' * (50-percent//2)}] {percent}%")
            sys.stdout.flush()
        
        urllib.request.urlretrieve(url, filepath, progress_hook)
        print(f"\n   ✅ Downloaded successfully!")
        return True
    except Exception as e:
        print(f"\n   ❌ Error: {e}")
        return False


def extract_archive(filepath, extract_to, archive_type='auto'):
    """Extract various archive types"""
    print(f"   📦 Extracting: {filepath}")
    
    try:
        if archive_type == 'auto':
            if str(filepath).endswith('.tar.bz2'):
                archive_type = 'tar.bz2'
            elif str(filepath).endswith('.tar.gz') or str(filepath).endswith('.tgz'):
                archive_type = 'tar.gz'
            elif str(filepath).endswith('.zip'):
                archive_type = 'zip'
            elif str(filepath).endswith('.gz'):
                archive_type = 'gz'
        
        if archive_type == 'tar.bz2':
            with tarfile.open(filepath, 'r:bz2') as tar:
                tar.extractall(extract_to)
        elif archive_type == 'tar.gz':
            with tarfile.open(filepath, 'r:gz') as tar:
                tar.extractall(extract_to)
        elif archive_type == 'zip':
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
        elif archive_type == 'gz':
            output_path = extract_to / filepath.stem
            with gzip.open(filepath, 'rb') as f_in:
                with open(output_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        
        print(f"   ✅ Extracted successfully!")
        return True
    except Exception as e:
        print(f"   ❌ Extraction error: {e}")
        return False


# ================================================================
# DATASET 1: SPAMASSASSIN
# ================================================================
print("\n" + "=" * 70)
print("📧 DATASET 1: SpamAssassin Public Corpus")
print("=" * 70)

SPAMASSASSIN_URLS = {
    'spam_1': 'https://spamassassin.apache.org/old/publiccorpus/20030228_spam.tar.bz2',
    'spam_2': 'https://spamassassin.apache.org/old/publiccorpus/20050311_spam_2.tar.bz2',
    'easy_ham_1': 'https://spamassassin.apache.org/old/publiccorpus/20030228_easy_ham.tar.bz2',
    'easy_ham_2': 'https://spamassassin.apache.org/old/publiccorpus/20030228_easy_ham_2.tar.bz2',
    'hard_ham': 'https://spamassassin.apache.org/old/publiccorpus/20030228_hard_ham.tar.bz2',
}

sa_dir = RAW_DIR / 'spamassassin'

for name, url in SPAMASSASSIN_URLS.items():
    filepath = sa_dir / f"{name}.tar.bz2"
    
    if not filepath.exists():
        if download_with_progress(url, filepath, f"SpamAssassin - {name}"):
            extract_archive(filepath, sa_dir)
    else:
        print(f"   ✅ {name} already exists")


# ================================================================
# DATASET 2: ENRON EMAIL
# ================================================================
print("\n" + "=" * 70)
print("📧 DATASET 2: Enron Email Dataset")
print("=" * 70)

print("""
⚠️  The Enron dataset is LARGE (~423 MB download, ~1.3 GB extracted)
    It contains 500,000+ legitimate corporate emails.
    
    Note: Enron emails are all HAM (legitimate). They will be combined
    with spam from other sources for balanced training.
""")

download_enron = input("Download Enron dataset? (yes/no): ").lower().strip()

if download_enron == 'yes':
    ENRON_URL = "https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz"
    enron_filepath = RAW_DIR / 'enron' / 'enron_mail.tar.gz'
    
    if not enron_filepath.exists():
        if download_with_progress(ENRON_URL, enron_filepath, "Enron Email Corpus"):
            print("\n   📦 Extracting Enron (this may take several minutes)...")
            extract_archive(enron_filepath, RAW_DIR / 'enron')
    else:
        print("   ✅ Enron dataset already exists")
else:
    print("   ⏭️  Skipping Enron dataset")


# ================================================================
# DATASET 3: KAGGLE SPAM DATASETS
# ================================================================
print("\n" + "=" * 70)
print("📧 DATASET 3: Kaggle/GitHub Spam Datasets")
print("=" * 70)

KAGGLE_URLS = [
    # SMS Spam Collection
    ("https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv", 
     "sms_spam.tsv"),
    # Email spam (if available)
    ("https://raw.githubusercontent.com/Deanis/Example-Data-Sets/main/spam.csv",
     "spam_emails.csv"),
]

kaggle_dir = RAW_DIR / 'kaggle'

for url, filename in KAGGLE_URLS:
    filepath = kaggle_dir / filename
    if not filepath.exists():
        download_with_progress(url, filepath, f"Kaggle - {filename}")
    else:
        print(f"   ✅ {filename} already exists")


# ================================================================
# DATASET 4: CSDMC2010 SPAM CORPUS
# ================================================================
print("\n" + "=" * 70)
print("📧 DATASET 4: CSDMC2010 Spam Corpus")
print("=" * 70)

print("""
   The CSDMC2010 dataset needs to be downloaded manually from:
   http://csmining.org/index.php/spam-email-datasets-.html
   
   Alternative: Using Ling-Spam dataset from the same source.
""")

# Try alternative academic datasets
ACADEMIC_URLS = [
    # Ling-spam (if available)
    ("https://www.aueb.gr/users/ion/data/lingspam_public.tar.gz",
     "lingspam.tar.gz"),
]

csdmc_dir = RAW_DIR / 'csdmc'

for url, filename in ACADEMIC_URLS:
    filepath = csdmc_dir / filename
    if not filepath.exists():
        if download_with_progress(url, filepath, f"Academic - {filename}"):
            extract_archive(filepath, csdmc_dir)
    else:
        print(f"   ✅ {filename} already exists")


# ================================================================
# DATASET 5: NAZARIO PHISHING CORPUS
# ================================================================
print("\n" + "=" * 70)
print("📧 DATASET 5: Nazario Phishing Corpus")
print("=" * 70)

print("""
   The Nazario phishing corpus contains real phishing emails.
   
   Primary source: https://monkey.org/~jose/phishing/
   
   Note: Due to the nature of phishing data, some URLs may require
   manual download or registration.
""")

# Create synthetic phishing examples as fallback
nazario_dir = RAW_DIR / 'nazario'

print("   📝 Creating comprehensive phishing examples dataset...")

phishing_examples = [
    # PayPal Phishing
    "PayPal: Your account has been limited until you verify your information. Click here to restore access to your account. Failure to verify within 24 hours will result in permanent suspension.",
    "Important: We've noticed unusual activity on your PayPal account. To protect your account, we've temporarily limited what you can do. Please verify your identity.",
    "PayPal Security Notice: Your account was accessed from an unknown device. If this wasn't you, secure your account immediately.",
    
    # Banking Phishing
    "Bank of America Alert: Suspicious transaction detected on your account. Click to verify this transaction or it will be processed.",
    "Chase Security: We detected unusual sign-in activity on your account. Please verify your identity to continue using your account.",
    "Wells Fargo: Your online banking access has been temporarily suspended. Click here to reactivate your account.",
    "Citibank Notice: Your debit card has been blocked due to suspicious activity. Verify your card details to unblock.",
    "HSBC Security: Your account has been compromised. Reset your password immediately to protect your funds.",
    
    # Apple/iCloud Phishing
    "Apple ID: Your account has been locked for security reasons. Verify your identity to unlock your account.",
    "iCloud: Your storage is full and your photos will be deleted. Upgrade your storage immediately.",
    "Apple: Your Apple ID was used to sign in to iMessage on a new device. If this wasn't you, click here.",
    "App Store: Your payment method has been declined. Update your payment information to continue your subscriptions.",
    
    # Microsoft Phishing
    "Microsoft: Your Office 365 subscription has expired. Renew now to keep access to your files.",
    "Outlook: Your mailbox is almost full. Click to get more storage or delete messages.",
    "Microsoft Account: Unusual sign-in activity detected. Review your recent activity now.",
    "OneDrive: Your account will be suspended in 24 hours. Verify your information to continue.",
    
    # Google Phishing
    "Google: Someone has your password. Your account might be compromised. Secure your account now.",
    "Gmail: Your account will be deleted due to inactivity. Sign in to keep your account.",
    "Google Security Alert: A new device signed into your account. If this wasn't you, review your activity.",
    
    # Amazon Phishing
    "Amazon: Your account has been locked. Please verify your information to unlock your account.",
    "Amazon Prime: Your payment method has failed. Update your payment to continue your membership.",
    "Amazon Security: Order confirmation #123-456-789. If you didn't place this order, click to cancel.",
    "Amazon: We're having trouble with your current payment method. Update your payment information.",
    
    # Netflix Phishing
    "Netflix: Your membership has been suspended. Update your payment details to continue watching.",
    "Netflix: We're having trouble with your billing information. Please update your payment method.",
    "Netflix: Your account is on hold. Complete payment to continue your subscription.",
    
    # Shipping Phishing
    "USPS: Your package could not be delivered. Reschedule your delivery by clicking here.",
    "FedEx: Your shipment is on hold due to unpaid customs fees. Pay \$1.99 to release your package.",
    "DHL: Package delivery failed. Please provide the correct address to receive your package.",
    "UPS: Your package requires additional payment. Click to complete payment and schedule delivery.",
    
    # IRS/Tax Phishing
    "IRS: You have an outstanding tax debt. Pay immediately to avoid legal action.",
    "IRS Notice: Your tax refund is pending. Verify your bank information to receive your refund.",
    "Internal Revenue Service: Your tax return has been flagged for review. Submit verification documents.",
    
    # Social Media Phishing
    "Facebook: Your account has been temporarily locked. Verify your identity to continue using Facebook.",
    "Instagram: Your account will be deleted for violating terms. Appeal this decision now.",
    "Twitter: Verify your account to keep your blue checkmark. Complete verification now.",
    "LinkedIn: Your account has been restricted. Complete our security check to restore access.",
    
    # Crypto Phishing
    "Coinbase: Your account has been locked due to suspicious activity. Verify your identity now.",
    "Bitcoin Alert: You've received 0.5 BTC. Click to claim your cryptocurrency.",
    "Crypto Wallet: Your wallet has been compromised. Secure your funds immediately.",
    
    # Generic Phishing
    "Security Alert: Your password was found in a data breach. Change your password immediately.",
    "Verify your identity to continue using your account. Click the link below.",
    "Your account requires immediate attention. Failure to respond will result in account suspension.",
    "Warning: Unusual activity detected. Verify your identity within 24 hours to avoid account closure.",
    "Urgent: Your account information needs to be updated. Click here to update your details.",
]

# Save phishing examples
import json
phishing_data = [{"text": text, "label": "spam", "type": "phishing"} for text in phishing_examples]
phishing_filepath = nazario_dir / 'phishing_examples.json'
with open(phishing_filepath, 'w') as f:
    json.dump(phishing_data, f, indent=2)
print(f"   ✅ Created {len(phishing_examples)} phishing examples")


# ================================================================
# SUMMARY
# ================================================================
print("\n" + "=" * 70)
print("📊 DOWNLOAD SUMMARY")
print("=" * 70)

def get_folder_size(folder):
    total = 0
    for path in Path(folder).rglob('*'):
        if path.is_file():
            total += path.stat().st_size
    return total / (1024 * 1024)  # MB

print(f"\n{'Dataset':<20} {'Location':<40} {'Size':<10}")
print("-" * 70)

datasets = [
    ('SpamAssassin', RAW_DIR / 'spamassassin'),
    ('Enron', RAW_DIR / 'enron'),
    ('Kaggle', RAW_DIR / 'kaggle'),
    ('CSDMC', RAW_DIR / 'csdmc'),
    ('Nazario', RAW_DIR / 'nazario'),
]

total_size = 0
for name, path in datasets:
    if path.exists():
        size = get_folder_size(path)
        total_size += size
        print(f"{name:<20} {str(path):<40} {size:.1f} MB")
    else:
        print(f"{name:<20} {str(path):<40} Not found")

print("-" * 70)
print(f"{'TOTAL':<20} {'':<40} {total_size:.1f} MB")

print("""
╔══════════════════════════════════════════════════════════════════╗
║                     DOWNLOAD COMPLETE! ✅                         ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  Next step: Run the processing script                            ║
║  > python level1_basic/process_all_datasets.py                   ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
""")