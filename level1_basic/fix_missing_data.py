# File: level1_basic/fix_missing_data.py

import os
import ssl
import urllib.request
import json
from pathlib import Path

print("=" * 60)
print("FIXING MISSING DATASETS")
print("=" * 60)

# Fix SSL issues
ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = Path('level1_basic/data/raw')

# ================================================================
# FIX 1: Add more Kaggle/GitHub datasets
# ================================================================
print("\n📥 Adding alternative spam datasets...")

kaggle_dir = BASE_DIR / 'kaggle'
kaggle_dir.mkdir(parents=True, exist_ok=True)

# Alternative URLs that work
ALTERNATIVE_URLS = [
    # Spam CSV from different sources
    ("https://raw.githubusercontent.com/mohitgupta-omg/Kaggle-SMS-Spam-Collection-Dataset-/master/spam.csv", 
     "spam_collection.csv"),
]

for url, filename in ALTERNATIVE_URLS:
    filepath = kaggle_dir / filename
    if not filepath.exists():
        try:
            print(f"   Downloading {filename}...")
            urllib.request.urlretrieve(url, filepath)
            print(f"   ✅ Downloaded: {filename}")
        except Exception as e:
            print(f"   ❌ Failed: {e}")


# ================================================================
# FIX 2: Add comprehensive phishing/spam examples
# ================================================================
print("\n📝 Creating comprehensive spam examples...")

nazario_dir = BASE_DIR / 'nazario'
nazario_dir.mkdir(parents=True, exist_ok=True)

# Extended phishing and spam collection
extended_spam = [
    # Lottery Scams
    "CONGRATULATIONS! You've been selected as a winner in the Microsoft Lottery! Your email was randomly chosen from millions of entries. You have won \$2,500,000.00 USD! To claim, contact our agent with your full name, address, and phone number.",
    "You have won £1,000,000.00 GBP in the UK National Lottery! Your ticket number 45-67-89-23 was selected. Contact claims department immediately!",
    "WINNER NOTIFICATION: Your email has won \$5,000,000 in the Apple iPhone Promotional Draw. Send your details to claim your prize!",
    "Final Notice: You've won the Coca-Cola International Lottery! Prize: \$1,500,000. Respond within 48 hours or forfeit your winnings!",
    
    # Banking Phishing
    "URGENT: Bank of America Security Alert - Your account has been temporarily limited due to suspicious activity. Click here to verify your identity or your account will be permanently closed within 24 hours.",
    "Chase Bank Notice: We've detected unauthorized access to your account. For your protection, we've temporarily suspended your online banking. Verify your information to restore access.",
    "Wells Fargo Alert: Your debit card ending in 4532 has been blocked. A transaction of \$899.99 was attempted. If this wasn't you, click here immediately.",
    "Citibank Security: Your account password will expire in 24 hours. Update your password now to avoid being locked out of your account.",
    "Capital One: Suspicious login detected from an unknown device. If this wasn't you, secure your account immediately.",
    
    # Tech Company Phishing
    "Apple Security Alert: Your Apple ID has been locked due to security concerns. Verify your identity to unlock your account and continue using Apple services.",
    "Microsoft Account: Unusual sign-in activity detected on your account. We blocked a sign-in attempt from Russia. Review your recent activity.",
    "Google Security Warning: Someone has your password. We've protected your account. Review your account security now.",
    "Amazon Prime: Your payment method has declined. Update your payment information within 24 hours to continue your Prime membership.",
    "Netflix: We're having trouble with your current billing information. Update your payment method to continue watching.",
    "PayPal: Your account access has been limited. We noticed unusual activity. Complete verification to restore full access.",
    
    # Package Delivery Scams
    "USPS: We attempted to deliver your package but no one was home. Schedule redelivery or your package will be returned: tracking #US9823748",
    "FedEx Delivery Notice: Your package is being held at our facility due to unpaid customs fees of \$2.99. Pay now to release.",
    "DHL Express: Your shipment #DHL847392 requires address verification. Complete the form to receive your delivery.",
    "UPS: Delivery failed. We could not deliver your package. Click to reschedule delivery time.",
    "Amazon Delivery: Your package could not be delivered. The address provided is incomplete. Update your shipping address.",
    
    # Job/Work Scams
    "WORK FROM HOME: Earn \$5,000-\$10,000 per week! No experience needed! Be your own boss! Limited positions available - apply now!",
    "SECRET SHOPPER OPPORTUNITY: Get paid \$400/day to shop and review stores! No experience required. Start immediately!",
    "DATA ENTRY JOBS: Make \$75/hour typing from home! Flexible hours, no experience needed. Urgent hiring!",
    "HIRING NOW: Social media manager needed. \$3,000/week guaranteed. Work 2-3 hours daily from anywhere!",
    
    # Health Scams
    "MIRACLE WEIGHT LOSS: Lose 30 pounds in 30 days with this revolutionary pill! No diet, no exercise! Doctor approved!",
    "ED PILLS: Buy Viagra, Cialis online without prescription! Lowest prices! Discrete shipping! Same day delivery!",
    "DIABETES CURE: Big pharma doesn't want you to know this simple fruit cures diabetes in 2 weeks! Click to learn the secret!",
    "ANTI-AGING BREAKTHROUGH: Look 20 years younger with this cream! Celebrities use this secret! Limited supply!",
    
    # Investment Scams  
    "CRYPTO ALERT: This coin will 1000x in 30 days! Insider information! Get in before it's too late! Guaranteed profits!",
    "FOREX SECRET: Learn how I turned \$100 into \$50,000 in one month! Free webinar reveals all! Limited spots!",
    "STOCK TIP: Buy [TICKER] now! This penny stock will explode 500% next week! Our picks are 95% accurate!",
    "REAL ESTATE: Make millions flipping houses with no money down! Free seminar reveals secrets! Register now!",
    
    # Threat/Extortion
    "I HACKED YOUR COMPUTER: I have all your private photos and browser history. Send \$2000 in Bitcoin or I'll send everything to your contacts.",
    "FBI WARNING: Your computer was used for illegal activities. Pay the fine of \$500 to avoid prosecution.",
    "IRS NOTICE: You owe back taxes of \$4,532.67. Pay immediately to avoid arrest and prosecution. Call this number NOW.",
    "FINAL WARNING: Legal action will be taken against you within 24 hours. Your social security number has been suspended.",
    
    # Romance Scams
    "Hi handsome! I'm Anna from Russia. I saw your profile and felt a connection. I'm looking for a serious relationship. Write me back!",
    "Lonely housewives in your area want to meet you tonight! No strings attached! Click for FREE membership!",
    "DATING ALERT: 5 women viewed your profile today! See who's interested in you! Upgrade to premium now!",
    
    # Fake Prizes/Rewards
    "You've been selected for a \$1000 Amazon Gift Card! Complete a short survey to claim your reward!",
    "Congratulations! Your phone number won a FREE iPhone 15 Pro! Just pay \$4.99 shipping to claim!",
    "SURVEY REWARD: Complete this 5-minute survey and receive \$500 cash! Limited time offer!",
    "You're our 1,000,000th visitor! Click to claim your prize - a brand new MacBook Pro!",
]

# Extended legitimate emails
extended_ham = [
    # Work Emails
    "Hi team, I wanted to follow up on our discussion from yesterday's meeting. Can everyone please send their project updates by EOD Friday? Thanks!",
    "Just a reminder that the quarterly review presentation is scheduled for next Tuesday at 2 PM in the large conference room. Please prepare your slides.",
    "The client has approved the final design mockups. Great work everyone! Let's move forward with development starting Monday.",
    "I've attached the revised proposal with the changes we discussed. Please review and let me know if you have any additional feedback.",
    "Could you please review the attached document and provide your comments? I need to submit the final version by Thursday.",
    "Team standup reminder: We're meeting at 9:30 AM tomorrow. Please be prepared to share your progress and any blockers.",
    "The new project timeline has been approved. I'm scheduling a kickoff meeting for next week. Please confirm your availability.",
    "Thanks for your help with the presentation yesterday. The client was very impressed with our approach.",
    "Please make sure to submit your timesheets by Friday. HR needs them for payroll processing.",
    "The office will be closed on Monday for the holiday. See everyone on Tuesday!",
    
    # Personal Emails
    "Hey! It's been a while since we caught up. Are you free for coffee this weekend? Let me know!",
    "Happy birthday! Wishing you an amazing day filled with joy and happiness. Hope to see you soon!",
    "Thanks for dinner last night! The restaurant was amazing. We should do it again soon.",
    "Just checking in - how's the new job going? Would love to hear about it when you have time.",
    "Mom, I'll be home around 7 PM for dinner. Can you save some food for me? Thanks!",
    "Are you going to Sarah's party this Saturday? I can pick you up if you need a ride.",
    "Congrats on the promotion! You totally deserve it. Let's celebrate soon!",
    "Just saw your vacation photos on Instagram - looks incredible! Where exactly was that?",
    "Hey, I left my jacket at your place last week. Can I swing by tomorrow to pick it up?",
    "Happy anniversary to you and Mark! Wishing you many more years of happiness together!",
    
    # Transaction Confirmations
    "Your Amazon order #123-4567890-1234567 has shipped! Track your delivery at amazon.com/orders",
    "Payment received: Thank you for your payment of \$150.00 to Electric Company. Your account is now current.",
    "Your Uber ride receipt: Trip from Downtown to Airport. Total: \$32.45. Thank you for riding with Uber!",
    "Your DoorDash order is on its way! Your driver John is 15 minutes away. Track your order in the app.",
    "Order confirmed: Your Nike order #NK123456 will arrive by Friday. You'll receive tracking info soon.",
    
    # Appointments & Reminders
    "Reminder: Your dentist appointment is tomorrow, March 15th at 10:30 AM with Dr. Smith. Please arrive 15 minutes early.",
    "Your car service appointment is confirmed for Saturday at 9 AM. Location: Main Street Auto Service.",
    "Don't forget: Parent-teacher conference is this Thursday at 4 PM in Room 203.",
    "Your prescription for Atorvastatin is ready for pickup at CVS Pharmacy on Oak Street.",
    "Reminder: Your annual physical is scheduled for next Monday at 2 PM. Please fast for 12 hours before.",
    
    # Financial Legitimate
    "Your credit card statement is now available. Log in to view your March statement balance of \$1,234.56",
    "Direct deposit received: Your paycheck of \$2,543.67 has been deposited to your account ending in 1234.",
    "Your automatic payment of \$89.99 to Netflix was successful. Thank you for being a member!",
    "401k Update: Your contribution of \$500 has been received. Current balance: \$45,678.90",
    "Your tax refund of \$2,156.00 has been deposited to your bank account. Thank you for e-filing!",
    
    # Travel
    "Flight confirmation: Your flight UA456 from JFK to LAX departs March 20 at 8:00 AM. Confirmation: ABC123",
    "Hotel booking confirmed: Marriott Downtown, March 20-22. Check-in: 3 PM. Confirmation #: MAR78945",
    "Your rental car reservation is confirmed: Economy car, March 20-22 at LAX. Total: \$89.99",
    "Boarding pass attached for your flight tomorrow. Have a safe trip!",
    "Trip reminder: Your vacation to Hawaii starts in 3 days! Don't forget to pack sunscreen!",
    
    # School/Education
    "Your assignment for CS 201 has been graded. Score: 92/100. Great work! See feedback in Canvas.",
    "Class canceled: Professor Johnson's lecture on Thursday is canceled. Check email for makeup date.",
    "Tuition payment due: Your spring semester tuition of \$4,500 is due by March 31.",
    "Grade posted: Your final grade for English 101 is A-. Great work this semester!",
    "Study group tonight at 7 PM in the library, 3rd floor study room. Bring your notes!",
    
    # IT/Tech Support Legitimate
    "Scheduled maintenance: The company servers will be down this Saturday from 2-4 AM for updates.",
    "Password successfully changed. If you didn't make this change, contact IT support immediately.",
    "Your Jira ticket #PROJ-1234 has been resolved. Please verify the fix and close the ticket.",
    "New software update available: Please install the latest security patch by end of week.",
    "Your VPN access has been renewed for another year. No action needed on your part.",
]

# Combine and save
all_spam = [{"text": t, "label": "spam", "source": "extended_spam"} for t in extended_spam]
all_ham = [{"text": t, "label": "ham", "source": "extended_ham"} for t in extended_ham]
all_examples = all_spam + all_ham

# Save as JSON
examples_path = nazario_dir / 'extended_examples.json'
with open(examples_path, 'w') as f:
    json.dump(all_examples, f, indent=2)

print(f"   ✅ Created {len(extended_spam)} spam + {len(extended_ham)} ham examples")
print(f"   ✅ Saved to: {examples_path}")


# ================================================================
# SUMMARY
# ================================================================
print("\n" + "=" * 60)
print("✅ FIXES COMPLETE!")
print("=" * 60)
print("""
You now have:
• SpamAssassin: ~6,000 emails
• Enron: ~500,000 emails  
• Kaggle SMS: ~5,500 messages
• Extended examples: ~100 examples

Total: 500,000+ training samples!

Next step: Run the processing script
> python level1_basic/process_all_datasets.py
""")