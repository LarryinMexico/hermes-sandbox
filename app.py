import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env (only needed for local dev)
# In Codespaces, variables are set via Codespace Secrets directly
load_dotenv()

app = Flask(__name__)

# ── Configuration ────────────────────────────────────────────────────────────
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_API   = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


def send_message(chat_id: int, text: str) -> None:
    """Send a plain-text reply back to a Telegram chat."""
    url     = f"{TELEGRAM_API}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    resp    = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    """Simple health-check endpoint — useful for debugging."""
    return jsonify({"status": "ok", "token_loaded": bool(TELEGRAM_TOKEN)})


@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Telegram calls this endpoint for every incoming update.
    Current behaviour: echo the user's message back.
    Future: hand the text off to Hermes for intelligent processing.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "empty body"}), 400

    # ── Parse incoming message ────────────────────────────────────────────
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text    = message.get("text", "")

    if not chat_id or not text:
        # Telegram sends non-message updates (e.g. edited messages) — ignore them
        return jsonify({"ok": True})

    # ── Process ───────────────────────────────────────────────────────────
    # TODO (Phase 2): Replace this block with a call to Hermes
    #   response_text = hermes.run(text)
    response_text = f"🤖 Echo: {text}"

    # ── Reply ─────────────────────────────────────────────────────────────
    send_message(chat_id, response_text)
    return jsonify({"ok": True})


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Use 0.0.0.0 so Codespaces port-forwarding can reach the server
    app.run(host="0.0.0.0", port=5000, debug=True)
