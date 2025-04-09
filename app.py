# app.py
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests

load_dotenv()  # Loads variables from .env file

app = Flask(__name__)

# Your Telnyx API key from your .env file
TELNYX_API_KEY = os.getenv("TELNYX_API_KEY")
TELNYX_CONTROL_URL = "https://api.telnyx.com/v2"

# Health Check endpoint
@app.route("/")
def index():
    return "Heroku Telnyx Integration is Running."

# Example: Webhook endpoint for inbound call events
@app.route("/telnyx/webhook", methods=["POST"])
def telnyx_webhook():
    event = request.json
    print("Received event:", event)
    # Here you can route based on event type; for example:
    # event_type = event.get("data", {}).get("event_type", "")
    # if event_type == "call.initiated":
    #     # Code to answer the call, play greeting, etc.
    #     pass
    return jsonify({"status": "received"}), 200

# Example: Endpoint to initiate an outbound call (if needed)
@app.route("/make_call", methods=["POST"])
def make_call():
    data = request.json
    to_number = data.get("to")
    from_number = data.get("from")
    # Customize the parameters as required by Telnyx API
    url = f"{TELNYX_CONTROL_URL}/calls"
    headers = {
        "Authorization": f"Bearer {TELNYX_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "from": from_number,
        "to": to_number,
        "connection_id": os.getenv("TELNYX_CONNECTION_ID"),
        # Other required parameters...
    }
    response = requests.post(url, json=payload, headers=headers)
    return jsonify(response.json()), response.status_code

# Example: Endpoint to serve customized voicemail greeting
@app.route("/voicemail_greeting", methods=["GET"])
def voicemail_greeting():
    # In a real app, you might generate the greeting dynamically.
    # For example, use URL parameters to customize the greeting.
    user_first_name = request.args.get("first_name", "User")
    # Here, consider modifying a stored audio file or appending the name via text-to-speech.
    # For now, we serve a static file (assumes you've stored the file in a /static directory)
    return app.send_static_file("Ari_Voicemail.mp3")

if __name__ == "__main__":
    app.run(debug=True)
