from flask import Flask, request, jsonify
import json
from rasa_agent import get_intent_from_rasa

# Load responses from responses.json
with open("data/responses.json") as file:
    responses = json.load(file)["responses"]

app = Flask(__name__)

# Fallback for unknown intents
FALLBACK_RESPONSE = "I'm sorry, I didn't understand that. Could you rephrase?"

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    intent = get_intent_from_rasa(user_message)
    response = responses.get(intent, [FALLBACK_RESPONSE])
    return jsonify({"response": response[0]})

if __name__ == "__main__":
    app.run(port=8000, debug=True)
