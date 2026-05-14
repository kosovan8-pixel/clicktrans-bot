from fastapi import FastAPI
import requests
import os

app = FastAPI()

# Railway Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


@app.get("/")
async def root():
    return {"status": "working"}


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": text
    }

    response = requests.post(url, json=data)

    print(response.text)


@app.post("/webhook/new-auction")
async def new_auction(data: dict):

    print("NEW AUCTION:")
    print(data)

    title = data.get("title", "No title")
    from_city = data.get("fromLocalizationShort", "Unknown")
    to_city = data.get("toLocalizationShort", "Unknown")
    budget = data.get("budget", "No budget")

    message = f"""
🚛 NEW AUCTION

📦 {title}

📍 {from_city}
➡️ {to_city}

💰 Budget: {budget}
"""

    send_telegram_message(message)

    return {"ok": True}

@app.get("/test-telegram")
async def test_telegram():

    send_telegram_message("🔥 Railway Telegram test")

    return {"ok": True}