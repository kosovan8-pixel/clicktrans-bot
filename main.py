from fastapi import FastAPI, Request
import requests

app = FastAPI()

import os

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

    requests.post(url, json=data)


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