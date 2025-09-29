from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("IG_VERIFY_TOKEN", "my_verify_token")
PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN", "")
IG_USER_ID = os.getenv("IG_USER_ID", "")
API_VERSION = os.getenv("FB_API_VERSION", "v17.0")

@app.route("/")
def index():
    return "✅ GoatBot Instagram is running!", 200

# ✅ Verify webhook
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

# ✅ Handle incoming messages
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    app.logger.info("Webhook event: %s", data)

    if data.get("entry"):
        for entry in data["entry"]:
            if "messaging" in entry:
                for event in entry["messaging"]:
                    sender_id = event.get("sender", {}).get("id")
                    if not sender_id:
                        continue
                    if "message" in event:
                        text = event["message"].get("text", "")
                        handle_message(sender_id, text)
    return "OK", 200

def handle_message(sender_id, text):
    text = (text or "").strip().lower()
    if any(greet in text for greet in ["hi", "hello", "hey"]):
        send_text_message(sender_id, "👋 Hi! Ami GoatBot. Ki help korte pari?")
    elif "help" in text:
        send_text_message(sender_id, "📌 Commands: help, info, contact")
    elif "info" in text:
        send_text_message(sender_id, "ℹ️ Ami ekta Instagram bot — GoatBot style!")
    else:
        send_text_message(sender_id, f"🤖 Tumi likhecho: {text}")

def send_text_message(recipient_id, message_text):
    if not PAGE_ACCESS_TOKEN or not IG_USER_ID:
        app.logger.error("❌ Missing PAGE_ACCESS_TOKEN or IG_USER_ID")
        return

    url = f"https://graph.facebook.com/{API_VERSION}/{IG_USER_ID}/messages"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    params = {"access_token": PAGE_ACCESS_TOKEN}
    resp = requests.post(url, params=params, json=payload, timeout=10)
    app.logger.info("Send message response: %s - %s", resp.status_code, resp.text)
    return resp

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
