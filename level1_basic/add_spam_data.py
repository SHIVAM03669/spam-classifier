# File: level1_basic/add_spam_data.py

import json
import random
from pathlib import Path

print("""
╔══════════════════════════════════════════════════════════════════╗
║           ADDING COMPREHENSIVE SPAM DATASET                       ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  Creating 15,000+ realistic spam examples                        ║
║  Categories: Phishing, Scams, Malware, Adult, Financial          ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
""")

# Create directory
spam_dir = Path('level1_basic/data/raw/additional_spam')
spam_dir.mkdir(parents=True, exist_ok=True)

# ================================================================
# SPAM TEMPLATES - Categorized
# ================================================================

# Category 1: Lottery & Prize Scams
lottery_templates = [
    "CONGRATULATIONS! You've won ${amount} in the {company} lottery! To claim your prize, send your full name, address, and bank details to {email}",
    "You've been selected as the WINNER of ${amount}! Your ticket number {ticket} was chosen! Reply NOW to claim!",
    "WINNER NOTIFICATION: Your email won ${amount} in the {company} International Draw. Contact claims agent immediately!",
    "Final Notice: You've won ${amount} in the {company} Sweepstakes! Respond within {hours} hours or forfeit your winnings!",
    "YOUR EMAIL HAS WON! ${amount} cash prize waiting! Click here to verify and claim your winnings today!",
    "URGENT: You are the lucky winner of ${amount}! This is not a joke! Contact us now with your details!",
    "Attention {name}! You've won a FREE {prize}! Just pay ${shipping} shipping to claim your prize now!",
    "Your mobile number has won ${amount} in the {company} mobile draw! Send your bank details to receive funds!",
    "{company} Promotional Award: Congratulations! You've won ${amount}! Reference: {ref}. Contact us to claim!",
    "LUCKY WINNER! Your email was randomly selected for ${amount} cash prize! Act now before it expires!",
]

lottery_vars = {
    'amount': ['1,000,000', '500,000', '2,500,000', '750,000', '5,000,000', '100,000', '50,000', '10,000,000'],
    'company': ['Microsoft', 'Google', 'Apple', 'Amazon', 'Coca-Cola', 'Samsung', 'Facebook', 'Walmart', 'Yahoo', 'AOL'],
    'email': ['claims@winner.com', 'prize@lottery.net', 'winner@claims.org', 'lottery@winning.com'],
    'ticket': ['45-67-89-23', '12-34-56-78', '98-76-54-32', 'AB-123-456', 'WIN-789-012'],
    'hours': ['24', '48', '72', '12'],
    'name': ['Dear Winner', 'Lucky One', 'Dear Customer', 'Dear User', 'Friend'],
    'prize': ['iPhone 15 Pro', 'MacBook Pro', 'Samsung Galaxy', 'iPad Pro', '\$1000 Gift Card', 'Tesla Model 3'],
    'shipping': ['1.99', '4.99', '9.99', '2.99'],
    'ref': ['UK/9420X2/68', 'REF-2024-WIN', 'PRIZE-45678', 'CLAIM-98765'],
}

# Category 2: Banking & Financial Phishing
banking_templates = [
    "URGENT: Your {bank} account has been compromised! Click here to verify your identity immediately or your account will be suspended.",
    "Security Alert: Unusual activity detected on your {bank} account. Login immediately to secure your account.",
    "Your {bank} account is temporarily locked due to suspicious activity. Verify your information to restore access.",
    "IMPORTANT: Your {bank} debit card ending in {card} has been blocked. Call this number immediately to unblock.",
    "{bank} Security Notice: We detected unauthorized access. For your protection, verify your account now.",
    "Your {bank} online banking access has been restricted. Update your security information to continue.",
    "ALERT: A transaction of ${amount} was attempted on your {bank} account. If unauthorized, click here!",
    "Your {bank} password will expire in {hours} hours. Update now to avoid being locked out!",
    "{bank}: Your account requires immediate verification. Failure to comply will result in account closure.",
    "Suspicious login attempt on your {bank} account from {location}. Secure your account immediately!",
    "Your {bank} credit card has been charged ${amount}. If you didn't make this purchase, click to dispute.",
    "{bank} FRAUD ALERT: Unusual spending pattern detected. Verify recent transactions now.",
]

banking_vars = {
    'bank': ['Bank of America', 'Chase', 'Wells Fargo', 'Citibank', 'Capital One', 'US Bank', 'PNC', 'TD Bank', 'HSBC', 'Barclays'],
    'card': ['4532', '7891', '2345', '6789', '1234', '5678', '9012', '3456'],
    'amount': ['499.99', '899.99', '1,299.00', '2,500.00', '750.00', '299.99', '599.00'],
    'hours': ['24', '48', '12', '6'],
    'location': ['Russia', 'China', 'Nigeria', 'Unknown Location', 'Ukraine', 'North Korea'],
}

# Category 3: Tech Company Phishing
tech_templates = [
    "Your {company} account has been locked due to security concerns. Verify your identity to unlock.",
    "{company} Security Alert: Someone tried to access your account. Review your security settings now.",
    "URGENT: Your {company} ID was used to sign in from a new device. If this wasn't you, click here.",
    "Your {company} account will be deleted in {hours} hours due to inactivity. Sign in to keep your account.",
    "{company}: We detected unusual activity on your account. Verify your identity immediately.",
    "Your {company} subscription has expired. Update your payment method to continue service.",
    "{company} Notice: Your account has been restricted. Complete verification to restore access.",
    "Important: Your {company} password was found in a data breach. Change it immediately!",
    "{company}: Your storage is almost full. Upgrade now or lose your files!",
    "Your {company} account security needs attention. Update your recovery information now.",
    "{company} Alert: Verify your account to continue receiving emails and notifications.",
    "Someone requested a password reset for your {company} account. If this wasn't you, click here!",
]

tech_vars = {
    'company': ['Apple', 'Google', 'Microsoft', 'Amazon', 'Netflix', 'PayPal', 'Facebook', 'Instagram', 'Twitter', 'LinkedIn', 'Dropbox', 'iCloud'],
    'hours': ['24', '48', '72', '12'],
}

# Category 4: Delivery & Package Scams
delivery_templates = [
    "{carrier}: We attempted to deliver your package but no one was home. Schedule redelivery: {tracking}",
    "Your {carrier} package is being held at our facility due to unpaid fees of ${fee}. Pay now to release.",
    "{carrier} Delivery Notice: Your shipment requires address verification. Complete form to receive.",
    "URGENT: Your {carrier} package could not be delivered. Update your shipping address now!",
    "{carrier}: Delivery failed for package {tracking}. Reschedule delivery or it will be returned.",
    "Your {carrier} shipment has been delayed. Track your package and update delivery preferences.",
    "{carrier} Notice: Customs fee of ${fee} required for international package. Pay to receive delivery.",
    "Your package from {store} is ready for pickup. Confirm delivery details to receive.",
    "{carrier}: Your package is waiting at the post office. Schedule pickup before {date}.",
    "Delivery attempt failed: Your {carrier} package needs signature confirmation. Click to reschedule.",
]

delivery_vars = {
    'carrier': ['USPS', 'FedEx', 'UPS', 'DHL', 'Amazon', 'OnTrac', 'LaserShip'],
    'tracking': ['US9823748234', '1Z999AA10123456784', '785632145698', 'JD014600001522780461', 'TBA301938543'],
    'fee': ['1.99', '2.99', '4.99', '3.49', '5.99'],
    'store': ['Amazon', 'Walmart', 'eBay', 'Target', 'Best Buy', 'Costco'],
    'date': ['tomorrow', 'Friday', 'end of week', '48 hours'],
}

# Category 5: Job & Money Making Scams
job_templates = [
    "WORK FROM HOME: Earn ${amount} per week! No experience needed! Limited positions available!",
    "SECRET SHOPPER: Get paid ${daily} per day to shop and review stores! Start immediately!",
    "DATA ENTRY: Make ${hourly}/hour typing from home! Flexible hours! Urgent hiring!",
    "HIRING NOW: {position} needed. ${weekly}/week guaranteed. Work {hours} hours daily!",
    "Easy money! Earn ${amount} weekly just by {task}! No skills required!",
    "Make money online! Turn ${invest} into ${return} in just {days} days! Guaranteed!",
    "Work from anywhere! ${hourly}/hour for simple {task}. Start today!",
    "URGENT HIRING: {company} needs remote workers. ${weekly}/week. Apply now!",
    "Retire early! Learn how I make ${monthly}/month from home with this simple trick!",
    "Financial freedom! Make ${daily} per day with just {hours} hours of work!",
]

job_vars = {
    'amount': ['5,000', '3,000', '10,000', '7,500', '2,500'],
    'daily': ['200', '400', '500', '300', '350'],
    'hourly': ['50', '75', '100', '65', '85'],
    'weekly': ['2,000', '3,500', '5,000', '4,000', '6,000'],
    'monthly': ['15,000', '20,000', '25,000', '10,000', '30,000'],
    'position': ['Social Media Manager', 'Virtual Assistant', 'Customer Service Rep', 'Data Entry Clerk', 'Email Processor'],
    'hours': ['2-3', '3-4', '4-5', '1-2'],
    'task': ['clicking ads', 'filling surveys', 'posting on social media', 'watching videos', 'reading emails'],
    'invest': ['100', '500', '250', '1,000'],
    'return': ['10,000', '50,000', '25,000', '100,000'],
    'days': ['7', '14', '30', '3'],
    'company': ['Google', 'Amazon', 'Apple', 'Facebook', 'Netflix'],
}

# Category 6: Health & Pharmaceutical Spam
health_templates = [
    "MIRACLE WEIGHT LOSS: Lose {pounds} pounds in {days} days! No diet, no exercise! Doctor approved!",
    "ED PILLS: Buy {drug} online without prescription! Lowest prices! Discrete shipping!",
    "DIABETES CURE: Big pharma hides this! Simple {food} cures diabetes in {weeks} weeks!",
    "ANTI-AGING: Look {years} years younger with this {product}! Celebrities use this secret!",
    "Pain relief! {drug} available without prescription! Fast shipping! Order now!",
    "SHOCKING: Doctors don't want you to know this {body_part} remedy! Works in {days} days!",
    "Lose belly fat FAST! This weird trick burns {pounds} pounds in {days} days!",
    "HAIR REGROWTH: Grow thick hair in {weeks} weeks with this natural {product}!",
    "Sleep better tonight! Natural {product} works instantly! No side effects!",
    "MUSCLE BUILDER: Gain {pounds} pounds of muscle in {weeks} weeks! No steroids!",
]

health_vars = {
    'pounds': ['30', '20', '50', '15', '40', '10'],
    'days': ['7', '14', '30', '21', '10'],
    'weeks': ['2', '3', '4', '1'],
    'years': ['10', '15', '20', '25'],
    'drug': ['Viagra', 'Cialis', 'Xanax', 'Ambien', 'Oxycontin', 'Adderall'],
    'food': ['fruit', 'vegetable', 'herb', 'spice', 'berry'],
    'product': ['cream', 'pill', 'supplement', 'serum', 'formula'],
    'body_part': ['joint', 'back', 'knee', 'heart', 'brain'],
}

# Category 7: Investment & Crypto Scams
investment_templates = [
    "CRYPTO ALERT: {coin} will {multiplier}x in {days} days! Insider info! Get in NOW!",
    "Investment opportunity: {percent}% returns guaranteed! Limited spots available!",
    "I turned ${invest} into ${return} trading {market}! Learn my secret strategy FREE!",
    "{coin} is about to EXPLODE! Buy now before it's too late! {percent}% gains expected!",
    "FOREX SECRET: Make ${daily}/day with this simple strategy! Works every time!",
    "Stock tip: Buy {ticker} NOW! Our picks are {percent}% accurate! Huge gains coming!",
    "Real estate millions: Make money flipping houses with NO money down! Free seminar!",
    "{coin} GIVEAWAY: Send {amount} {coin}, get {multiplier}x back! Elon Musk promotion!",
    "Binary options: ${daily} daily profits! 95% win rate! Start with just ${invest}!",
    "NFT opportunity: This collection will 100x! Mint now before it sells out!",
]

investment_vars = {
    'coin': ['Bitcoin', 'Ethereum', 'Dogecoin', 'Shiba Inu', 'XRP', 'Solana', 'Cardano'],
    'multiplier': ['10', '100', '1000', '50', '500'],
    'days': ['7', '30', '14', '3', '60'],
    'percent': ['500', '200', '1000', '300', '50'],
    'invest': ['100', '500', '1000', '250'],
    'return': ['10,000', '50,000', '100,000', '25,000'],
    'daily': ['500', '1,000', '2,500', '5,000'],
    'market': ['forex', 'crypto', 'stocks', 'options', 'binary options'],
    'ticker': ['AAPL', 'TSLA', 'GME', 'AMC', 'NVDA'],
    'amount': ['0.1', '0.5', '1', '0.01'],
}

# Category 8: Romance & Adult Scams
romance_templates = [
    "Hot singles in your area want to meet you tonight! Click for FREE membership!",
    "Hi! I'm {name} from {country}. I saw your profile and felt a connection. Write me back!",
    "{number} women viewed your profile today! See who's interested! Upgrade now!",
    "Lonely {nationality} women seeking American men! Find your soulmate! Join free!",
    "DATING ALERT: {name} wants to meet you! She's only {distance} miles away!",
    "Adult content warning: Someone shared private photos. Click to see who!",
    "Meet {nationality} brides! Beautiful women waiting for you! Free registration!",
    "Your secret admirer revealed! {name} has a crush on you! Click to see!",
    "{name} sent you a private message! She wants to meet tonight! View now!",
    "Find love today! {number} matches waiting for you! Premium access FREE!",
]

romance_vars = {
    'name': ['Anna', 'Maria', 'Svetlana', 'Olga', 'Natasha', 'Elena', 'Irina', 'Jessica', 'Ashley', 'Emma'],
    'country': ['Russia', 'Ukraine', 'Philippines', 'Colombia', 'Brazil', 'Thailand'],
    'nationality': ['Russian', 'Ukrainian', 'Asian', 'Latin', 'European'],
    'number': ['5', '12', '23', '8', '15', '31'],
    'distance': ['2', '5', '10', '3', '7'],
}

# Category 9: Threat & Extortion
threat_templates = [
    "I HACKED YOUR COMPUTER: I have all your private {data}. Send ${amount} in Bitcoin or I send everything to your contacts.",
    "FBI WARNING: Your computer was used for illegal activities. Pay ${fine} to avoid prosecution.",
    "IRS NOTICE: You owe back taxes of ${amount}. Pay immediately to avoid arrest!",
    "Your Social Security number has been suspended due to suspicious activity. Call now to reactivate!",
    "POLICE ALERT: Warrant issued for your arrest. Pay ${fine} online to clear your record!",
    "FINAL WARNING: Legal action will be taken in {hours} hours. Your SSN has been compromised!",
    "I recorded you through your webcam. Send ${amount} Bitcoin or the video goes public!",
    "Your {account} password is {password}. I know everything. Send ${amount} to keep it private.",
    "CIA NOTICE: Your internet activity is being monitored. Pay ${fine} to avoid investigation!",
    "URGENT: Your identity was stolen. Call this number immediately to protect yourself!",
]

threat_vars = {
    'data': ['photos', 'browser history', 'files', 'messages', 'videos'],
    'amount': ['2,000', '1,500', '3,000', '5,000', '1,000'],
    'fine': ['500', '750', '1,000', '299', '450'],
    'hours': ['24', '48', '12', '72'],
    'account': ['email', 'Facebook', 'banking', 'iCloud'],
    'password': ['password123', 'qwerty', '12345678', 'letmein'],
}

# Category 10: Free Stuff & Rewards
freebie_templates = [
    "Congratulations! You've been selected for a ${amount} {store} gift card! Complete survey to claim!",
    "FREE {product}! You're our {number}th visitor! Click to claim your prize!",
    "You've won a FREE {product}! Just pay ${shipping} shipping! Limited time!",
    "{store} is giving away FREE ${amount} gift cards! Take short survey to claim yours!",
    "EXCLUSIVE: Get a FREE {product} - only {number} left! Claim before they're gone!",
    "Your reward is waiting! ${amount} {store} gift card ready to ship! Verify your address!",
    "FREE SAMPLE: Get {product} absolutely FREE! Just pay shipping of ${shipping}!",
    "Claim your FREE {product} today! No purchase necessary! Limited availability!",
    "{store} customer appreciation: FREE ${amount} voucher for you! Use code: {code}",
    "You've earned a FREE {product}! Complete registration to receive your reward!",
]

freebie_vars = {
    'amount': ['100', '250', '500', '1,000', '50'],
    'store': ['Amazon', 'Walmart', 'Target', 'Best Buy', 'Costco', 'Home Depot', 'Starbucks'],
    'product': ['iPhone', 'AirPods', 'iPad', 'Samsung TV', 'PS5', 'Nintendo Switch', 'MacBook'],
    'number': ['1,000,000', '100,000', '500,000', '10,000'],
    'shipping': ['4.99', '9.99', '1.99', '2.99'],
    'code': ['WINNER2024', 'FREEBIE', 'CLAIM100', 'REWARD50'],
}


# ================================================================
# GENERATE SPAM EMAILS
# ================================================================
def generate_from_template(templates, variables, count):
    """Generate spam emails from templates with variable substitution"""
    generated = []
    
    for _ in range(count):
        template = random.choice(templates)
        email = template
        
        for var_name, var_values in variables.items():
            if '{' + var_name + '}' in email:
                email = email.replace('{' + var_name + '}', random.choice(var_values))
        
        generated.append(email)
    
    return generated


print("📧 Generating spam emails...\n")

all_spam = []

# Generate from each category
categories = [
    ("Lottery & Prize Scams", lottery_templates, lottery_vars, 1500),
    ("Banking Phishing", banking_templates, banking_vars, 2000),
    ("Tech Company Phishing", tech_templates, tech_vars, 2000),
    ("Delivery Scams", delivery_templates, delivery_vars, 1500),
    ("Job & Money Scams", job_templates, job_vars, 1500),
    ("Health & Pharma Spam", health_templates, health_vars, 1500),
    ("Investment & Crypto", investment_templates, investment_vars, 1500),
    ("Romance & Adult", romance_templates, romance_vars, 1200),
    ("Threat & Extortion", threat_templates, threat_vars, 1000),
    ("Free Stuff & Rewards", freebie_templates, freebie_vars, 1300),
]

for name, templates, variables, count in categories:
    emails = generate_from_template(templates, variables, count)
    all_spam.extend(emails)
    print(f"   ✅ {name}: {len(emails)} emails")


# Add some additional variations
print("\n📝 Adding variations and edge cases...")

# Subject line variations
subject_prefixes = [
    "URGENT: ", "IMPORTANT: ", "ACTION REQUIRED: ", "⚠️ ", "🚨 ", 
    "RE: ", "FW: ", "FINAL NOTICE: ", "[IMPORTANT] ", "*** ",
    "Don't miss: ", "Limited time: ", "Exclusive: ", "Breaking: ",
]

# Add more variations
additional_variations = []
for spam in random.sample(all_spam, min(2000, len(all_spam))):
    prefix = random.choice(subject_prefixes)
    additional_variations.append(prefix + spam)

all_spam.extend(additional_variations)
print(f"   ✅ Added {len(additional_variations)} variations")


# Add common spam phrases as standalone
common_spam_phrases = [
    "Click here now!", "Limited time offer!", "Act now!", "Don't miss out!",
    "You've been selected!", "Congratulations winner!", "Claim your prize!",
    "Free gift inside!", "No credit card required!", "100% free!",
    "Make money fast!", "Work from home!", "Be your own boss!",
    "Lose weight now!", "No diet needed!", "Doctors hate this!",
    "One weird trick!", "You won't believe!", "Secret revealed!",
    "Limited spots available!", "Expires today!", "Final notice!",
    "Your account is at risk!", "Verify immediately!", "Urgent action needed!",
    "Unsubscribe to stop receiving!", "This is not spam!", "You opted in!",
] * 50

all_spam.extend(common_spam_phrases)
print(f"   ✅ Added {len(common_spam_phrases)} common phrases")


# ================================================================
# SAVE SPAM DATA
# ================================================================
print(f"\n📊 Total spam emails generated: {len(all_spam)}")

# Remove duplicates
all_spam = list(set(all_spam))
print(f"   After removing duplicates: {len(all_spam)}")

# Create data structure
spam_data = [{"text": text, "label": "spam"} for text in all_spam]

# Save as JSON
output_path = spam_dir / 'comprehensive_spam.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(spam_data, f, indent=2, ensure_ascii=False)

print(f"\n💾 Saved to: {output_path}")

# Also save a CSV for easy viewing
import csv
csv_path = spam_dir / 'comprehensive_spam.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['text', 'label'])
    writer.writeheader()
    writer.writerows(spam_data)

print(f"💾 Also saved as CSV: {csv_path}")

print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                    SPAM DATA CREATED! ✅                          ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  📊 Statistics:                                                    ║
║     • Total spam emails: {len(all_spam):>10,}                              
║     • Categories: 10                                              ║
║     • Saved to: level1_basic/data/raw/additional_spam/           ║
║                                                                   ║
║  Next: Run the training script again                              ║
║  > python level1_basic/train_balanced.py                         ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
""")