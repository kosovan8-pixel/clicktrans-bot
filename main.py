from fastapi import FastAPI, Request
import requests

app = FastAPI()

BOT_TOKEN = "8852507061:AAHUXjXRNpYjE3lmxUUeOO7uoOwpNkbadMM"
CHAT_ID = "560174831"


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