from fastapi import FastAPI
import requests
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

CLICKTRANS_EMAIL = os.getenv(
    "CLICKTRANS_EMAIL"
)

CLICKTRANS_PASSWORD = os.getenv(
    "CLICKTRANS_PASSWORD"
)

HEADER_NAME = os.getenv(
    "CLICKTRANS_HEADER_NAME"
)

HEADER_VALUE = os.getenv(
    "CLICKTRANS_HEADER_VALUE"
)

BASE = os.getenv(
    "CLICKTRANS_BASE",
    "https://staging-02.develop.clicktrans.pl"
)


@app.get("/")
async def root():

    return {
        "status": "working"
    }


def send_telegram_message(text):

    if not BOT_TOKEN:
        return

    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )

    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": text
        }
    )


def login_variant_1():

    url = f"{BASE}/api/login_check"

    payload = {
        "_username":
            CLICKTRANS_EMAIL,

        "_password":
            CLICKTRANS_PASSWORD
    }

    headers = {
        HEADER_NAME:
            HEADER_VALUE
    }

    r = requests.post(
        url,
        json=payload,
        headers=headers
    )

    return {
        "variant": 1,
        "status": r.status_code,
        "response": r.text
    }


def login_variant_2():

    url = f"{BASE}/api/login_check"

    payload = {
        "username":
            CLICKTRANS_EMAIL,

        "password":
            CLICKTRANS_PASSWORD
    }

    headers = {
        HEADER_NAME:
            HEADER_VALUE
    }

    r = requests.post(
        url,
        json=payload,
        headers=headers
    )

    return {
        "variant": 2,
        "status": r.status_code,
        "response": r.text
    }


def login_variant_3():

    url = f"{BASE}/api/login_check"

    payload = {
        "username":
            CLICKTRANS_EMAIL,

        "password":
            CLICKTRANS_PASSWORD
    }

    headers = {
        HEADER_NAME:
            HEADER_VALUE
    }

    r = requests.post(
        url,
        data=payload,
        headers=headers
    )

    return {
        "variant": 3,
        "status": r.status_code,
        "response": r.text
    }


@app.get("/test-login")
async def test_login():

    return {
        "v1":
            login_variant_1(),

        "v2":
            login_variant_2(),

        "v3":
            login_variant_3()
    }


@app.post(
    "/webhook/new-auction"
)
async def new_auction(
    data: dict
):

    send_telegram_message(
        str(data)
    )

    return {
        "ok": True
    }


@app.post(
    "/webhook/update-auction"
)
async def update_auction(
    data: dict
):

    return {
        "ok": True
    }