import json
import random
import numpy as np
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from flask import Flask, request, jsonify

# Load intents file
with open("src/intents.json") as file:
    intents = json.load(file)

# Initialize Flask app
app = Flask(__name__)

# Preprocess data for intent classification
def preprocess_intents(intents):
    tags = []
    patterns = []
    responses = {}
    
    for intent in intents["intents"]:
        tag = intent["tag"]
        tags.append(tag)
        responses[tag] = intent["responses"]
        
        for pattern in intent["patterns"]:
            patterns.append((pattern, tag))
    
    return patterns, tags, responses

patterns, tags, responses = preprocess_intents(intents)

# Prepare training data
X_train = [pattern[0] for pattern in patterns]
y_train = [pattern[1] for pattern in patterns]

# Vectorize text patterns
vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)

# Train a classifier (Logistic Regression)
clf = LogisticRegression()
clf.fit(X_train_vectorized, y_train)

# Function to predict intent
def predict_intent(text):
    text_vectorized = vectorizer.transform([text])
    tag = clf.predict(text_vectorized)[0]
    return tag

# Route to handle chat messages
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    intent_tag = predict_intent(user_message)
    response = random.choice(responses[intent_tag])
    
    return jsonify({"response": response})

if __name__ == "__main__":
    nltk.download("punkt")
    app.run(debug=True)

