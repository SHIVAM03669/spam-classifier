# File: level1_basic/app/app.py (UPDATED)

from flask import Flask, render_template, request, jsonify
import joblib
import re
import os

app = Flask(__name__)

# Get the directory where app.py is located
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Use absolute paths
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'spam_classifier.joblib')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'models', 'tfidf_vectorizer.joblib')

print(f"Looking for model at: {MODEL_PATH}")
print(f"Looking for vectorizer at: {VECTORIZER_PATH}")

# Check if files exist
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model not found at {MODEL_PATH}\n"
        "Please run 'python level1_basic/train_and_save.py' first!"
    )

if not os.path.exists(VECTORIZER_PATH):
    raise FileNotFoundError(
        f"Vectorizer not found at {VECTORIZER_PATH}\n"
        "Please run 'python level1_basic/train_and_save.py' first!"
    )

# Load model and vectorizer
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

print("✅ Model and vectorizer loaded successfully!")


def preprocess_text(text):
    """Simple text preprocessing"""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def predict_spam(text):
    """Predict if text is spam"""
    processed = preprocess_text(text)
    text_tfidf = vectorizer.transform([processed])
    prediction = model.predict(text_tfidf)[0]
    probability = model.predict_proba(text_tfidf)[0]
    
    return {
        'is_spam': bool(prediction),
        'label': 'SPAM' if prediction else 'NOT SPAM',
        'confidence': float(max(probability) * 100),
        'spam_probability': float(probability[1] * 100),
        'ham_probability': float(probability[0] * 100)
    }


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.is_json:
        text = request.json.get('text', '')
    else:
        text = request.form.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    result = predict_spam(text)
    return jsonify(result)


if __name__ == '__main__':
    print("\n🚀 Starting Flask server...")
    print("   Open http://localhost:5000 in your browser\n")
    app.run(debug=True, port=5000)