from fastapi import FastAPI
import requests
import os

app = FastAPI()

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Clicktrans
CLICKTRANS_BASE = os.getenv(
    "CLICKTRANS_BASE",
    "https://staging-02.develop.clicktrans.pl"
)

CLICKTRANS_EMAIL = os.getenv("CLICKTRANS_EMAIL")
CLICKTRANS_PASSWORD = os.getenv("CLICKTRANS_PASSWORD")

CLICKTRANS_HEADER_NAME = os.getenv(
    "CLICKTRANS_HEADER_NAME",
    "user-partner-header"
)

CLICKTRANS_HEADER_VALUE = os.getenv(
    "CLICKTRANS_HEADER_VALUE",
    "clicktranspartner"
)


@app.get("/")
async def root():
    return {"status": "working"}


def send_telegram(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": text
    }

    requests.post(url, json=data)


def get_jwt():

    url = f"{CLICKTRANS_BASE}/api/login_check"

    headers = {
        CLICKTRANS_HEADER_NAME:
        CLICKTRANS_HEADER_VALUE
    }

    payload = {
        "username": CLICKTRANS_EMAIL,
        "password": CLICKTRANS_PASSWORD,
        "deviceUID": "PAKO-BOT"
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    print(response.status_code)
    print(response.text)

    return response.json()


@app.get("/test-login")
async def test_login():

    token = get_jwt()

    send_telegram(
        f"JWT TEST\n\n{token}"
    )

    return token