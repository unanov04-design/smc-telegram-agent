import os
import json
import logging
from flask import Flask, request
import requests

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # твій токен
CHAT_ID        = os.getenv("CHAT_ID")         # id чату/каналу

def send_telegram_message(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        r = requests.post(url, json=payload)
        if r.status_code != 200:
            logging.error(f"Telegram error: {r.text}")
    except Exception as e:
        logging.error(f"Send TG error: {e}")

@app.route("/", methods=["POST"])
def webhook():
    try:
        data = request.get_data(as_text=True)
        logging.info(f"Raw data: {data}")
        j = json.loads(data)

        sym   = j.get("sym","?")
        tf    = j.get("tf","?")
        patt  = j.get("pattern","?")
        side  = j.get("side","?")
        entry = j.get("entry","?")
        sl    = j.get("sl","?")
        tp    = j.get("tp","?")
        rr    = j.get("rr","?")
        poi   = j.get("poi","?")
        bias  = j.get("htf_bias","?")
        asia  = j.get("asia","?")
        smt   = j.get("smt","?")
        news  = j.get("news","?")
        sess  = j.get("session","?")
        note  = j.get("note","")

        msg = (
            f"📊 <b>SMC Signal</b>\n"
            f"──────────────\n"
            f"🔹 <b>Instrument:</b> {sym}  ({tf})\n"
            f"🔹 <b>Side:</b> {side}\n"
            f"🔹 <b>Pattern:</b> {patt}\n"
            f"🔹 <b>POI (H1):</b> {poi}\n"
            f"🔹 <b>HTF bias (D1):</b> {bias}\n"
            f"──────────────\n"
            f"🎯 <b>Entry:</b> {entry}\n"
            f"❌ <b>SL:</b> {sl}\n"
            f"✅ <b>TP:</b> {tp}\n"
            f"⚖️ <b>RR:</b> {rr}\n"
            f"──────────────\n"
            f"⏰ <b>Session:</b> {sess}\n"
            f"🌏 <b>Asia:</b> {asia}\n"
            f"📈 <b>SMT:</b> {smt}\n"
            f"📰 <b>News:</b> {news}\n"
            f"──────────────\n"
            f"{note}"
        )

        send_telegram_message(msg)
        return "ok", 200

    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return "error", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
