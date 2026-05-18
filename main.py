from fastapi import FastAPI
import requests
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

CLICKTRANS_BASE = os.getenv(
    "CLICKTRANS_BASE"
)

CLICKTRANS_EMAIL = os.getenv(
    "CLICKTRANS_EMAIL"
)

CLICKTRANS_PASSWORD = os.getenv(
    "CLICKTRANS_PASSWORD"
)

CLICKTRANS_HEADER_NAME = os.getenv(
    "CLICKTRANS_HEADER_NAME"
)

CLICKTRANS_HEADER_VALUE = os.getenv(
    "CLICKTRANS_HEADER_VALUE"
)


@app.get("/")
async def root():

    return {
        "status": "working"
    }


@app.get("/test-login")
async def test_login():

    headers = {
        CLICKTRANS_HEADER_NAME:
        CLICKTRANS_HEADER_VALUE
    }

    payload = {

        "email":
        CLICKTRANS_EMAIL,

        "password":
        CLICKTRANS_PASSWORD

    }

    urls = [

        f"{CLICKTRANS_BASE}/api/login",

        f"{CLICKTRANS_BASE}/api/login_check",

        f"{CLICKTRANS_BASE}/api/auth/login"

    ]

    result = {}

    for i, url in enumerate(
        urls,
        start=1
    ):

        r = requests.post(
            url,
            json=payload,
            headers=headers
        )

        result[
            f"variant_{i}"
        ] = {

            "url":
            url,

            "status":
            r.status_code,

            "response":
            r.text[:1000]

        }

    return result