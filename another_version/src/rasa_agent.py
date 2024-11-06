import requests
import json

RASA_SERVER_URL = "http://localhost:5005/model/parse"

def get_intent_from_rasa(message):
    payload = {
        "text": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(RASA_SERVER_URL, data=json.dumps(payload), headers=headers)
    response_data = response.json()
    intent = response_data['intent']['name'] if response_data['intent']['confidence'] > 0.7 else "fallback"
    return intent
